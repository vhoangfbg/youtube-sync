<div align="center">

# 🎬 YouTube Subscription Sync

Tự động đồng bộ kênh đăng ký giữa hai tài khoản YouTube | Powered by Python & GitHub Actions

[![YouTube API](https://img.shields.io/badge/YouTube-API-red.svg)](https://developers.google.com/youtube/v3)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## 📚 Mục Lục
- [Tính Năng](#-tính-năng)
- [Hướng Dẫn Cài Đặt](#-hướng-dẫn-cài-đặt)
- [Cấu Trúc Project](#-cấu-trúc-project)
- [Lưu Ý Quan Trọng](#-lưu-ý-quan-trọng)
- [Tips & Gợi Ý](#-tips--gợi-ý)

## ✨ Tính Năng
- 🔄 Tự động đồng bộ kênh đăng ký giữa 2 tài khoản
- 🤖 Chạy tự động mỗi ngày qua GitHub Actions 
- 📊 Hiển thị log chi tiết quá trình đồng bộ
- 🔑 Bảo mật với OAuth 2.0

## 🚀 Hướng Dẫn Cài Đặt

### 1. Clone Project
```bash
git clone <repository-url>
cd YoutubeSync
```

### 2. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### 3. Thiết Lập Google OAuth

1. Truy cập [Google Cloud Console](https://console.cloud.google.com)
2. Tạo Project mới
3. Kích hoạt **YouTube Data API v3**
4. Tạo OAuth 2.0 credentials:
   - Application type: Desktop
   - Tải và lưu file là `client_secret.json`

### 4. Tạo Token Xác Thực
```bash
python get_token.py
```
> ℹ️ Chạy script 2 lần:
> - Lần 1: Đăng nhập Account A (chính)
> - Lần 2: Đăng nhập Account B (phụ)

### 5. Chạy Thử
```bash
python sync_subs.py
```

## 📁 Cấu Trúc Project

| File | Mô Tả |
|------|--------|
| `sync_subs.py` | Script đồng bộ chính |
| `get_token.py` | Tạo OAuth token |
| `requirements.txt` | Dependencies |
| `token_A.pkl` | Token tài khoản A |
| `token_B.pkl` | Token tài khoản B |

## ⚠️ Lưu Ý Quan Trọng

- **API Quota**: 
  - Giới hạn miễn phí: 10,000 units/ngày
  - Đăng ký/hủy: 50 units/lần
  - Lấy danh sách: 1 unit/request

## 💡 Tips & Gợi Ý

- 📋 Kiểm tra log sau mỗi lần chạy
- 💾 Backup các file token để tránh mất quyền truy cập
- ⏰ Có thể chạy thủ công qua tab Actions trên GitHub
- 🔄 Script tự động chạy lúc 2:00 UTC mỗi ngày

---
<div align="center">
Made with ❤️ by vhoangfbg
</div>