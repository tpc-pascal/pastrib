## Hướng dẫn sử dụng

### Yêu cầu

- Python 3.10+
- Git
- GitHub account (cho GitHub Actions)

### Cài đặt

```bash
git clone https://github.com/tpc-pascal/pastrib.git
cd pastrib
```

Không cần cài thêm thư viện — toàn bộ dùng thư viện chuẩn của Python và Git.

---

### Dummy files & nội dung

Khi spread mode tạo commit, mỗi ngày sẽ có một file với extension ngẫu nhiên từ **44 loại**:

Python `.py` · JavaScript `.js` · TypeScript `.ts` · Rust `.rs` · Go `.go` · Java `.java`
C `.c/.h` · C++ `.cpp` · C# `.cs` · Kotlin `.kt` · Swift `.swift` · PHP `.php`
Ruby `.rb` · Dart `.dart` · Lua `.lua` · R `.r` · Perl `.pl` · Elixir `.ex/.exs`
Shell `.sh` · Batch `.bat` · PowerShell `.ps1`
Web `.html/.css/.scss/.less` · Vue `.vue` · Svelte `.svelte`
Data `.json/.yaml/.yml/.toml/.csv/.xml` · Config `.ini/.cfg/.env/.lock`
Doc `.md/.txt` · SQL `.sql`

Nội dung mỗi file là các câu chuyện troll dev Việt Nam (deadline, deploy 18h thứ 6, "chạy trên máy tao mà", copy-paste Stack Overflow...), phù hợp với từng loại extension.

### Log tự động

Mỗi lần chạy thành công, **spread** hoặc **specific** đều ghi log vào `log.txt` tại thư mục root với các thông tin:
- Thời gian chạy (start → end) và thời lượng
- Mode (spread / specific)
- Branch, tham số đầu vào
- Kết quả (số commit tạo, số ngày filled/skipped, commit cũ → mới)
- Status: Success

Log được append — giữ lịch sử tất cả các lần chạy.

> File `log.txt` đã được thêm vào `.gitignore` nên sẽ không bị commit lên Git.

### Chạy thử (Dry Run)

Trước khi chạy thật, luôn dùng `--dry-run` để xem trước thao tác:

#### Spread — Lấp contribution graph

```bash
python git_date_spread.py \
  --start-date "2024-01" \
  --end-date "2024-06" \
  --dry-run
```

#### Specific — Sửa ngày commit

```bash
python git_date_specific.py \
  --commit-hash a1b2c3d \
  --new-date "2025-06-15 14:30:00" \
  --dry-run
```

### Chạy thật

Bỏ `--dry-run` để áp dụng thay đổi:

```bash
python git_date_spread.py --start-date "2024-01" --end-date "2024-06"
```

### Push lên GitHub

```bash
git push origin main
```

> ⚠ Với **Specific mode**, cần force push vì lịch sử bị rewrite:
> ```
> git push origin <branch> --force
> ```

### Dọn dẹp dummy folder

```bash
python scripts/cleanup_dummy.py
```

Hoặc dùng GitHub Actions → "Cleanup Dummy Folder".

---

### Chạy trên GitHub Actions

1. Vào GitHub → **Actions** tab
2. Chọn workflow **Rewrite Git History**
3. Nhập tham số (mode, dates, branch)
4. Run workflow — tự động push kết quả

> 💢 Do at your own risk! Công cụ này can thiệp trực tiếp vào lịch sử Git.
