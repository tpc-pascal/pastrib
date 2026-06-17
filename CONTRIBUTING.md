# Hướng dẫn Đóng góp (Contributing Guidelines)

Vui lòng đọc kỹ các hướng dẫn dưới đây trước khi bắt đầu đóng góp.

---

## 🛠 1. Thiết lập môi trường phát triển (Setup)

1. Fork repo về tài khoản cá nhân.
2. Clone repo về máy:
    ```bash
    git clone https://github.com/tpc-pascal/pastrib.git
    cd pastrib
    ```
3. Đảm bảo bạn đã cài Python 3.10+ và Git.
4. Code structure:
    - `git_date_modifier/base.py` — các hàm dùng chung (git wrapper, `write_log`, `format_duration`)
    - `git_date_modifier/spread.py` — logic spread + content generators + extension list
    - `git_date_modifier/specific.py` — logic specific mode

---

## 🌿 2. Quy trình gửi đóng góp (Git Workflow)

1. **Fork** dự án về tài khoản cá nhân của bạn.
2. **Tạo Branch mới:**
   - Tính năng mới: `git checkout -b feat/ten-tinh-nang`
   - Sửa lỗi: `git checkout -b fix/ten-loi`
   - Tài liệu: `git checkout -b docs/ten-tai-lieu`
3. **Commit:** Sử dụng tiếng Việt hoặc tiếng Anh, nhưng phải rõ nghĩa.
   - *Ví dụ:* `feat: bổ sung tính năng spread theo tuần`
4. **Push & PR:** Đẩy branch lên GitHub và tạo **Pull Request**.

---

## 📝 3. Quy chuẩn viết mã (Coding Standards)

- **Nhất quán:** Tuân thủ các quy tắc đặt tên đã có sẵn trong dự án.
- **Comment:** Giải thích các logic phức tạp, đặc biệt là phần xử lý ngày tháng hoặc filter-branch.

---

## 🧪 4. Kiểm thử (Testing)

Trước khi gửi Pull Request, vui lòng đảm bảo:

- Code chạy được trên máy cá nhân với `--dry-run` trước khi chạy thật.
- Nếu thêm nội dung troll mới hoặc extension mới, kiểm tra với spread `--dry-run`.
- Nếu sửa `write_log`, kiểm tra cả spread và specific đều ghi log đúng.
- Không làm ảnh hưởng đến lịch sử Git hiện tại của người dùng khác.
- Kiểm tra syntax: `python -m py_compile git_date_modifier/*.py`

---

## 📧 Liên hệ

Nếu có bất kỳ thắc mắc nào:

- [Mở một Issue](https://github.com/tpc-pascal/pastrib/issues) trên repo này.
- Gửi câu hỏi qua phần [Thảo luận (Discussions)](https://github.com/tpc-pascal/pastrib/discussions) của dự án.
