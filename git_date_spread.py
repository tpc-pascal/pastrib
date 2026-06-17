#!/usr/bin/env python3
"""
Git Date Spread — Fill empty days in contribution graph with dummy commits.
Always operates on the repository containing this script.

Usage:
  python git_date_spread.py --start-date "YYYY-MM-DD" --end-date "YYYY-MM-DD"
  python git_date_spread.py --start-date "2024-01" --end-date "2024-06" --dry-run
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from git_date_modifier.spread import run


def main():
    p = argparse.ArgumentParser(
        prog="git_date_spread",
        description="Fill empty days in contribution graph with dummy commits.",
    )
    p.add_argument("--branch", default=None, help="Branch to work on (default: current)")
    p.add_argument("--start-date", required=True, help="Start date: YYYY-MM-DD [HH:MM:SS]")
    p.add_argument("--end-date", required=True, help="End date: YYYY-MM-DD [HH:MM:SS]")
    p.add_argument("--run-date", default="", help="Run date (folder name under dummy/). Default: today")
    p.add_argument("--yes", action="store_true", help="Skip interactive confirmation")
    p.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")

    args = p.parse_args()
    run(
        start_date=args.start_date,
        end_date=args.end_date,
        branch=args.branch,
        yes=args.yes,
        dry_run=args.dry_run,
        run_date=args.run_date or None,
    )


if __name__ == "__main__":
    main()
