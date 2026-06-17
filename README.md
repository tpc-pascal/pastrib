# pastrib
Chỉnh sửa commit date (specific) và lấp đầy contribution graph (spread) với nội dung troll đa dạng. Chạy trực tiếp trên repo — cả local lẫn GitHub Actions.

<p align="center">
  <img src="assets/logo.svg" alt="Pastrib Logo" width="400">
</p>

[![Open In GitHub](https://img.shields.io/badge/GitHub-tpc--pascal%2Fpastrib-181717?logo=github&logoColor=white)](https://github.com/tpc-pascal/pastrib)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-ready-2088FF?logo=github-actions&logoColor=white)](https://github.com/tpc-pascal/pastrib/actions)

> Công cụ chỉnh sửa ngày tháng commit Git (specific) và tự động lấp đầy contribution graph (spread). Chạy được local hoặc qua GitHub Actions.

**Lý do ra đời:** Bạn muốn có một contribution graph xanh mướt nhưng có những ngày trống? Hoặc cần sửa lại ngày tháng của một commit cũ? Công cụ này giúp bạn làm cả hai — sửa ngày commit cụ thể bằng `git filter-branch` (tự động validate parent/child date, re-sign PGP nếu có) hoặc tự động tạo commit lấp đầy các ngày trống trong khoảng thời gian mong muốn. Mỗi commit được tạo ra với nội dung troll, file extension đa dạng (`.py`, `.js`, `.rs`, `.md`, ...) và workflow run được ghi log tự động.

---

## Tính năng

- **Specific mode** — Sửa ngày commit cụ thể bằng `git filter-branch`; tự động kiểm tra `new-date ≥ parent date` (error), `new-date ≤ child date` (warning); timezone luôn `+0700`
- **Spread mode** — Duyệt từng ngày trong `[start-date, end-date]`; ngày đã có commit → SKIP; ngày trống → tạo 2-3 commits (random giờ 08-18h, `+0700`); mỗi ngày tạo file với extension ngẫu nhiên từ 44 loại (`.py`, `.js`, `.rs`, `.go`, `.json`, `.html`, `.sh`, ...) và nội dung troll dev Việt Nam; dùng `git commit` với env date (không cần force push)
- **Dry run** — Xem trước thay đổi trước khi áp dụng (`--dry-run`)
- **Auto log** — Mỗi lần chạy thành công tự động ghi `log.txt` ở root với thông tin: thời gian, duration, mode, branch, kết quả
- **GitHub Actions** — Chạy trực tiếp trên CI: chọn mode, nhập dates, chọn branch → workflow tự động push
- **Cleanup** — Script và GitHub Action để dọn dẹp thư mục `dummy/` sinh ra khi spread

---

## Cấu trúc thư mục

```
pastrib/
├── .github/workflows/
│   ├── rewrite_history.yml      # Rewrite Git History workflow
│   └── cleanup_dummy.yml        # Cleanup Dummy Folder workflow
├── assets/
│   └── logo.svg                 # Logo dự án
├── git_date_modifier/           # Core Python package
│   ├── __init__.py
│   ├── base.py                  # Shared utilities (git, write_log, ...)
│   ├── spread.py                # Spread mode logic + troll content generators
│   └── specific.py              # Specific mode logic
├── scripts/
│   └── cleanup_dummy.py         # Script dọn dẹp dummy folder
├── git_date_specific.py         # Specific mode — sửa ngày commit
├── git_date_spread.py           # Spread mode — lấp contribution graph
├── .gitignore                   # Ignore log.txt
├── GUIDE.md                     # Hướng dẫn sử dụng chi tiết
├── CONTRIBUTING.md              # Hướng dẫn đóng góp
├── CREDITS.md                   # Credits & tham khảo
└── README.md                    # File này
```

---

## Tech Stack

| Layer | Công nghệ |
|---|---|
| Language | Python 3.10+ |
| VCS | Git |
| CI/CD | GitHub Actions |

---

## Tác giả

**tpc-pascal** — [GitHub](https://github.com/tpc-pascal)

---

## License

MIT — xem file [LICENSE](./LICENSE).
