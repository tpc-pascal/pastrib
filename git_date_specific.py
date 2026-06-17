#!/usr/bin/env python3
"""
Git Date Specific — Change a single commit's author & committer date.

Usage:
  python git_date_specific.py --commit-hash <hash> --new-date "YYYY-MM-DD HH:MM:SS"
  python git_date_specific.py --commit-hash <hash> --new-date "YYYY-MM-DD" --dry-run
"""

import argparse
import os
import sys

# Ensure package directory is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from git_date_modifier.specific import run


def main():
    p = argparse.ArgumentParser(
        prog="git_date_specific",
        description="Change a single commit's date with parent/child validation.",
    )
    p.add_argument("--repo-path", default=".", help="Path to git repository (default: .)")
    p.add_argument("--branch", default=None, help="Branch to rewrite (default: current)")
    p.add_argument("--commit-hash", required=True, help="Full or abbreviated commit hash")
    p.add_argument("--new-date", required=True, help="New date: YYYY-MM-DD [HH:MM:SS]")
    p.add_argument("--yes", action="store_true", help="Skip interactive confirmation")
    p.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")

    args = p.parse_args()
    run(
        repo=args.repo_path,
        commit_hash=args.commit_hash,
        new_date=args.new_date,
        branch=args.branch,
        yes=args.yes,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
