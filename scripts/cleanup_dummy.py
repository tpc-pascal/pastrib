#!/usr/bin/env python3
import os
import subprocess
import sys


def git(args, cwd=None, check=True):
    cmd = ["git"] + args
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=cwd or repo_root, check=check
    )
    return result


def main():
    global repo_root
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dummy_dir = os.path.join(repo_root, "dummy")

    if not os.path.isdir(dummy_dir):
        print("Không tìm thấy folder dummy/.")
        sys.exit(1)

    folders = sorted(
        [d for d in os.listdir(dummy_dir) if os.path.isdir(os.path.join(dummy_dir, d))]
    )

    if not folders:
        print("Không có folder nào trong dummy/.")
        sys.exit(0)

    print("=== Các folder trong dummy/ ===")
    for i, f in enumerate(folders, 1):
        print(f"  {i}. {f}")

    print()
    try:
        choice = int(input("Chọn số để xoá folder: ").strip())
        if choice < 1 or choice > len(folders):
            print("Số không hợp lệ.")
            sys.exit(1)
    except ValueError:
        print("Vui lòng nhập số.")
        sys.exit(1)

    folder = folders[choice - 1]
    confirm = input(f"Xoá dummy/{folder}? (yes): ").strip().lower()
    if confirm != "yes":
        print("Huỷ.")
        sys.exit(0)

    git(["rm", "-r", f"dummy/{folder}"])
    git(["commit", "-m", f"chore: xóa dummy folder {folder}"])
    git(["push"])
    print(f"Đã xoá dummy/{folder} và push lên remote.")


if __name__ == "__main__":
    main()
