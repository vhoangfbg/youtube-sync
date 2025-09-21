from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def save_token(account_name):
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    with open(f"token_{account_name}.pkl", "wb") as f:
        pickle.dump(creds, f)
    print(f"Đã lưu token cho {account_name}")

if __name__ == "__main__":
    save_token("A")  # lần 1 chạy → login account A
    save_token("B")  # lần 2 chạy → login account B
