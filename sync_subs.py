import pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ===== Helper functions =====

def load_creds(account):
    """Load OAuth token (pickle format)."""
    with open(f"token_{account}.pkl", "rb") as f:
        return pickle.load(f)

def get_subscriptions(creds):
    """Lấy danh sách subscriptions {channelId: channelName}."""
    youtube = build("youtube", "v3", credentials=creds)
    subs = {}
    request = youtube.subscriptions().list(
        part="snippet",
        mine=True,
        maxResults=50
    )
    while request:
        try:
            response = request.execute()
        except HttpError as e:
            print(f"❌ Error fetching subscriptions: {e}")
            break
        for item in response.get("items", []):
            cid = item["snippet"]["resourceId"]["channelId"]
            cname = item["snippet"]["title"]
            subs[cid] = cname
        request = youtube.subscriptions().list_next(request, response)
    return subs

def get_subscription_map(creds):
    """Trả về map {channelId: subscriptionId} để unsubscribe nhanh hơn."""
    youtube = build("youtube", "v3", credentials=creds)
    subs_map = {}
    request = youtube.subscriptions().list(
        part="id,snippet",
        mine=True,
        maxResults=50
    )
    while request:
        try:
            response = request.execute()
        except HttpError as e:
            print(f"❌ Error fetching subscriptions for map: {e}")
            break
        for item in response.get("items", []):
            subs_map[item["snippet"]["resourceId"]["channelId"]] = item["id"]
        request = youtube.subscriptions().list_next(request, response)
    return subs_map

def subscribe_to_channel(creds, channel_id, channel_name):
    """Đăng ký channel mới."""
    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "resourceId": {
                "kind": "youtube#channel",
                "channelId": channel_id
            }
        }
    }
    try:
        youtube.subscriptions().insert(
            part="snippet",
            body=body
        ).execute()
        return f"[+] Subscribed to: {channel_name}"
    except HttpError as e:
        return f"❌ Error subscribing {channel_name}: {e}"

def unsubscribe_from_channel(creds, channel_id, channel_name, subs_map):
    """Huỷ đăng ký channel (dùng subs_map để tìm nhanh)."""
    youtube = build("youtube", "v3", credentials=creds)
    if channel_id not in subs_map:
        return f"⚠️ Not subscribed (skip): {channel_name}"
    try:
        youtube.subscriptions().delete(id=subs_map[channel_id]).execute()
        return f"[-] Unsubscribed from: {channel_name}"
    except HttpError as e:
        return f"❌ Error unsubscribing {channel_name}: {e}"

# ===== Main sync logic =====

if __name__ == "__main__":
    creds_A = load_creds("A")  # Account chính
    creds_B = load_creds("B")  # Account phụ

    # Lấy danh sách subscriptions
    subs_A = get_subscriptions(creds_A)
    subs_B = get_subscriptions(creds_B)

    need_to_sub = set(subs_A.keys()) - set(subs_B.keys())
    need_to_unsub = set(subs_B.keys()) - set(subs_A.keys())

    # Ước lượng quota
    base_cost = 2  # subscriptions.list gọi 2 lần
    add_cost = len(need_to_sub) * 50
    remove_cost = len(need_to_unsub) * 50
    total = base_cost + add_cost + remove_cost

    print("📊 Ước lượng trước khi sync:")
    print(f" - Số kênh cần thêm: {len(need_to_sub)} (tốn {add_cost} units)")
    print(f" - Số kênh cần huỷ: {len(need_to_unsub)} (tốn {remove_cost} units)")
    print(f" - Gọi list: {base_cost} units")
    print(f"👉 Tổng dự kiến: {total} units (giới hạn free 10,000 units/ngày)\n")

    notifications = []

    # Thêm kênh còn thiếu
    for cid in need_to_sub:
        notifications.append(subscribe_to_channel(creds_B, cid, subs_A[cid]))

    # Huỷ kênh thừa
    if need_to_unsub:
        subs_map_B = get_subscription_map(creds_B)
        for cid in need_to_unsub:
            notifications.append(unsubscribe_from_channel(creds_B, cid, subs_B[cid], subs_map_B))

    # In thông báo cuối
    if notifications:
        print("\n".join(notifications))
    else:
        print("✅ Không có gì để thay đổi.")

    print("🎉 Đồng bộ hoàn tất!")
