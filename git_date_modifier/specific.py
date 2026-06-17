import random
import sys
from datetime import datetime

from .base import (
    git,
    die,
    validate_repo,
    check_clean_tree,
    resolve_branch,
    ensure_git_config,
    parse_datetime,
    confirm,
    author_ts,
    committer_ts,
    get_parents,
    get_children,
    detect_signing_key,
    COMMIT_FILTER_SIGN,
    print_push_instructions,
    write_log,
    format_duration,
)


def run(repo, commit_hash, new_date, branch=None, yes=False, dry_run=False):
    start_time = datetime.now()
    validate_repo(repo)
    if not yes:
        check_clean_tree(repo)
    branch = resolve_branch(repo, branch)

    r = git(["rev-parse", "--verify", f"{commit_hash}^{{commit}}"], repo, check=False)
    if r.returncode != 0:
        die(f"Commit '{commit_hash}' not found.")
    full_hash = git(["rev-parse", commit_hash], repo).stdout.strip()

    raw_new_date = new_date.strip()
    is_date_only = len(raw_new_date) == 10 and raw_new_date.count("-") == 2

    new_dt = parse_datetime(new_date)

    if is_date_only:
        hour = random.randint(8, 18)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        new_dt = new_dt.replace(hour=hour, minute=minute, second=second)

    new_s = new_dt.strftime("%Y-%m-%d %H:%M:%S")
    new_ts = int(new_dt.timestamp())

    cur_author = author_ts(repo, full_hash)
    cur_committer = committer_ts(repo, full_hash)

    parents = get_parents(repo, full_hash)
    if parents:
        parent_tss = [committer_ts(repo, p) for p in parents]
        max_parent = max(parent_tss)
        if new_ts < max_parent:
            die(
                f"New date ({new_s}) is BEFORE parent commit "
                f"({datetime.fromtimestamp(max_parent).strftime('%Y-%m-%d %H:%M:%S')})."
            )

    children = get_children(repo, full_hash)
    if children:
        min_child_ts = min(cts for _, cts in children)
        if new_ts > min_child_ts:
            child_hash = next(ch for ch, cts in children if cts == min_child_ts)
            print(
                f"Warning: New date ({new_s}) is AFTER child commit "
                f"{child_hash[:8]} "
                f"({datetime.fromtimestamp(min_child_ts).strftime('%Y-%m-%d %H:%M:%S')})."
            )
            print("  Proceeding anyway (you may be intentionally fixing history).")

    if new_ts == cur_author and new_ts == cur_committer:
        print("New date is identical to current date. Nothing to do.")
        return

    old_s = datetime.fromtimestamp(cur_author).strftime("%Y-%m-%d %H:%M:%S")

    if dry_run:
        print(f"[DRY RUN] Would change {full_hash[:12]}: {old_s}  ->  {new_s}")
        return

    confirm(
        yes,
        f"This will change commit {full_hash[:12]} date:\n"
        f"  {old_s}  ->  {new_s}\n"
        f"on branch '{branch}'.\n"
        "All subsequent commits will receive new hashes.",
    )

    ensure_git_config(repo)
    can_sign = detect_signing_key(repo)
    if can_sign:
        print("GPG signing key detected - will re-signed signed commits.")

    env_filter = (
        f'if [ "$GIT_COMMIT" = "{full_hash}" ]\n'
        f"then\n"
        f'    export GIT_AUTHOR_DATE="{new_ts} +0700"\n'
        f'    export GIT_COMMITTER_DATE="{new_ts} +0700"\n'
        f"fi"
    )

    print(f"Rewriting branch '{branch}' ...")
    cmd = ["filter-branch", "-f", "--env-filter", env_filter]
    if can_sign:
        cmd.extend(["--commit-filter", COMMIT_FILTER_SIGN])
    cmd.extend(["--", branch])
    r = git(cmd, repo, check=False)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        die("filter-branch failed.")

    end_time = datetime.now()
    duration = end_time - start_time

    write_log(repo, [
        f"=== Run: {start_time.strftime('%Y-%m-%d %H:%M:%S')} → {end_time.strftime('%H:%M:%S')} ({format_duration(duration)}) ===",
        f"  Mode:       specific",
        f"  Branch:     {branch}",
        f"  Commit:     {full_hash}",
        f"  Old date:   {old_s}",
        f"  New date:   {new_s}",
        f"  Status:     Success",
        "─" * 55,
    ])

    print(f"Done! Commit {full_hash[:12]} date updated to {new_s}.")
    print_push_instructions(repo, branch)
