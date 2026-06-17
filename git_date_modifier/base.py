import os
import subprocess
import sys
from datetime import datetime


def write_log(repo, lines):
    """Append a block of lines to log.txt at the repo root."""
    log_path = os.path.join(repo, "log.txt")
    with open(log_path, "a", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")


def format_duration(delta):
    total = int(delta.total_seconds())
    if total < 60:
        return f"{total}s"
    elif total < 3600:
        return f"{total // 60}m {total % 60}s"
    else:
        h = total // 3600
        m = (total % 3600) // 60
        s = total % 60
        return f"{h}h {m}m {s}s"


def git(args, repo, check=True):
    cmd = ["git"] + args
    return subprocess.run(cmd, capture_output=True, text=True, cwd=repo, check=check)


def die(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def validate_repo(repo):
    r = git(["rev-parse", "--git-dir"], repo, check=False)
    if r.returncode != 0:
        die(f"Not a git repository: {repo}")


def check_clean_tree(repo):
    r = git(["status", "--porcelain"], repo)
    if r.stdout.strip():
        die("Working tree is not clean. Commit or stash changes first.")


def resolve_branch(repo, branch):
    if branch:
        return branch
    r = git(["rev-parse", "--abbrev-ref", "HEAD"], repo)
    b = r.stdout.strip()
    if b == "HEAD":
        die("Detached HEAD. Use --branch to specify which branch to rewrite.")
    return b


def ensure_git_config(repo):
    def _resolve():
        name = None
        email = None

        r = git(["config", "user.name"], repo, check=False)
        if r.returncode == 0 and r.stdout.strip():
            name = r.stdout.strip()
        r = git(["config", "user.email"], repo, check=False)
        if r.returncode == 0 and r.stdout.strip():
            email = r.stdout.strip()

        if name and email:
            return name, email

        actor = os.environ.get("GITHUB_ACTOR")
        if actor:
            name = actor
            email = f"{actor}@users.noreply.github.com"

        if not name or not email:
            r = git(["config", "--global", "user.name"], repo, check=False)
            if r.returncode == 0 and r.stdout.strip():
                name = r.stdout.strip()
            r = git(["config", "--global", "user.email"], repo, check=False)
            if r.returncode == 0 and r.stdout.strip():
                email = r.stdout.strip()

        if not name:
            name = os.environ.get("GIT_AUTHOR_NAME") or "Pastrib"
        if not email:
            email = os.environ.get("GIT_AUTHOR_EMAIL") or "pastrib@local"

        return name, email

    name, email = _resolve()
    for key, val in [("user.name", name), ("user.email", email)]:
        r = git(["config", key], repo, check=False)
        if r.returncode != 0 or not r.stdout.strip():
            git(["config", key, val], repo)


def parse_datetime(s):
    s = s.strip().strip('"').strip("'")
    patterns = [
        ("%Y-%m-%d %H:%M:%S", "YYYY-MM-DD HH:MM:SS"),
        ("%Y-%m-%dT%H:%M:%S", "YYYY-MM-DDTHH:MM:SS"),
        ("%Y-%m-%d", "YYYY-MM-DD"),
    ]
    for fmt, _ in patterns:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    die(f"Invalid date format: '{s}'. Use YYYY-MM-DD HH:MM:SS or YYYY-MM-DD")


def confirm(yes, message):
    if yes:
        return
    print()
    print("⚠️  WARNING:", message)
    print()
    ans = input("Type 'yes' to confirm: ").strip().lower()
    if ans != "yes":
        print("Aborted.")
        sys.exit(0)


def _commit_ts(repo, commit, fmt):
    r = git(["log", "-1", f"--format={fmt}", commit], repo)
    return int(r.stdout.strip())


def author_ts(repo, commit):
    return _commit_ts(repo, commit, "%at")


def committer_ts(repo, commit):
    return _commit_ts(repo, commit, "%ct")


def get_parents(repo, commit):
    r = git(["rev-parse", "--verify", f"{commit}^@", "--"], repo, check=False)
    if r.returncode != 0:
        return []
    return [h for h in r.stdout.strip().split("\n") if h.strip()]


def get_children(repo, commit_hash):
    r = git(
        [
            "rev-list",
            "--parents",
            "--reverse",
            "--ancestry-path",
            f"{commit_hash}..HEAD",
        ],
        repo,
        check=False,
    )
    if r.returncode != 0:
        return []
    children = []
    for line in r.stdout.strip().split("\n"):
        parts = line.strip().split()
        if not parts:
            continue
        child = parts[0]
        parents = parts[1:]
        if commit_hash in parents:
            children.append((child, committer_ts(repo, child)))
    return children


def has_pgp_signature(repo, commit):
    r = git(["log", "-1", "--format=%G?", commit], repo, check=False)
    sig = r.stdout.strip()
    return sig in ("G", "F", "U", "B", "X", "E")


COMMIT_FILTER_SIGN = """\
sig=$(git log -1 --format="%G?" "$GIT_COMMIT" 2>/dev/null)
if [ -n "$sig" ] && [ "$sig" != "N" ]; then
    exec git commit-tree -S "$@"
fi
exec git commit-tree "$@"
"""


def detect_signing_key(repo):
    r = git(["config", "user.signingkey"], repo, check=False)
    if r.returncode == 0 and r.stdout.strip():
        return True

    try:
        r = subprocess.run(
            ["gpg", "--list-secret-keys", "--keyid-format=LONG"],
            capture_output=True, text=True, check=False, timeout=10,
        )
        if r.returncode == 0:
            for line in r.stdout.split("\n"):
                if "sec" in line:
                    parts = line.strip().split("/")
                    if len(parts) >= 2:
                        key_id = parts[1].split()[0]
                        git(["config", "user.signingkey", key_id], repo, check=False)
                        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return False


def print_push_instructions(repo, branch):
    has_remote = git(["remote", "get-url", "origin"], repo, check=False).returncode == 0
    in_ci = "GITHUB_ACTIONS" in os.environ
    print()
    if in_ci:
        print("Running in GitHub Actions - force push handled by the workflow.")
    else:
        print("History rewritten! All hashes have changed. To update remote:")
        print()
        print(f"    git push origin {branch} --force")
        print()
        if has_remote:
            print("For other branches sharing this history:")
            print(f"    git push origin --all --force")
            print()
        print("To UNDO (restore backup before any further changes):")
        print(f"    git reset --hard refs/original/refs/heads/{branch}")
        print()
