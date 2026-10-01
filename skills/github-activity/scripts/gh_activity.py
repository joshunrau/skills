#!/usr/bin/env python3
"""Summarize your GitHub activity, optionally scoped to an org or specific repos.

Requires the `gh` CLI, already authenticated (`gh auth login`).

Usage:
  gh_activity.py [repos ...]                  # summary across all repos (or just the listed ones)
  gh_activity.py summary [repos ...]          # same as above
  gh_activity.py commits [repos ...]          # commits you authored
  gh_activity.py prs [repos ...]              # PRs you authored
  gh_activity.py reviews [repos ...]          # PRs you reviewed (authored by others)
  gh_activity.py issues [repos ...]           # issues you opened
  gh_activity.py events [repos ...]           # raw event feed (pushes, comments, branches, ...)

Common options (valid on every subcommand):
  --owner OWNER    GitHub org/user to scope to (default: no scope — all your activity)
  --since WHEN     Start date: YYYY-MM-DD, <N>d (e.g. 7d), or a weekday name
                   meaning the most recent one in the past (default: friday)
  --user LOGIN     GitHub login to report on (default: the authenticated user)
  --json           Emit machine-readable JSON instead of text
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys

COMMANDS = ("summary", "commits", "prs", "reviews", "issues", "events")
WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def gh(*args: str) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"error: gh {' '.join(args[:2])} failed: {result.stderr.strip()}")
    return result.stdout


def gh_json(*args: str):
    out = gh(*args).strip()
    return json.loads(out) if out else []


def parse_concat_json(text: str) -> list:
    """`gh api --paginate` emits back-to-back JSON arrays; decode and flatten them."""
    decoder = json.JSONDecoder()
    items, pos = [], 0
    text = text.strip()
    while pos < len(text):
        value, end = decoder.raw_decode(text, pos)
        items.extend(value if isinstance(value, list) else [value])
        pos = end
        while pos < len(text) and text[pos].isspace():
            pos += 1
    return items


def parse_since(value: str) -> dt.date:
    today = dt.date.today()
    v = value.strip().lower()
    if v.endswith("d") and v[:-1].isdigit():
        return today - dt.timedelta(days=int(v[:-1]))
    if v in WEEKDAYS:
        delta = (today.weekday() - WEEKDAYS.index(v)) % 7 or 7
        return today - dt.timedelta(days=delta)
    try:
        return dt.date.fromisoformat(v)
    except ValueError:
        sys.exit(f"error: cannot parse --since {value!r} (use YYYY-MM-DD, <N>d, or a weekday name)")


def qualify(owner: str | None, repo: str) -> str:
    if "/" in repo:
        return repo
    if not owner:
        sys.exit(f"error: repo {repo!r} must be qualified as owner/name when --owner is not given")
    return f"{owner}/{repo}"


def scope_args(owner: str | None, repos: list[str]) -> list[str]:
    """Flags limiting a `gh search` to the requested repos or owner (no flags = no scope)."""
    if repos:
        args: list[str] = []
        for repo in repos:
            args += ["--repo", qualify(owner, repo)]
        return args
    return ["--owner", owner] if owner else []


# --- fetchers ---------------------------------------------------------------


def fetch_commits(user: str, since: dt.date, owner: str | None, repos: list[str]) -> list[dict]:
    rows = gh_json(
        "search", "commits", "--author", user, "--author-date", f">={since}",
        "--limit", "100", "--json", "repository,commit,sha", *scope_args(owner, repos),
    )
    commits = [
        {
            "repo": row["repository"]["fullName"],
            "date": row["commit"]["author"]["date"][:10],
            "sha": row["sha"][:7],
            "message": row["commit"]["message"].splitlines()[0],
        }
        for row in rows
    ]
    return sorted(commits, key=lambda c: c["date"], reverse=True)


def _fetch_pr_like(kind: str, filter_flag: str, user: str, since: dt.date, owner: str | None, repos: list[str]) -> list[dict]:
    rows = gh_json(
        "search", kind, filter_flag, user, "--updated", f">={since}", "--limit", "100",
        "--json", "repository,number,title,state,author,updatedAt,url", *scope_args(owner, repos),
    )
    items = [
        {
            "repo": row["repository"]["nameWithOwner"],
            "number": row["number"],
            "title": row["title"],
            "state": row["state"],
            "author": (row.get("author") or {}).get("login", ""),
            "updated": row["updatedAt"][:10],
            "url": row["url"],
        }
        for row in rows
    ]
    return sorted(items, key=lambda i: i["updated"], reverse=True)


def fetch_prs(user: str, since: dt.date, owner: str | None, repos: list[str]) -> list[dict]:
    return _fetch_pr_like("prs", "--author", user, since, owner, repos)


def fetch_reviews(user: str, since: dt.date, owner: str | None, repos: list[str]) -> list[dict]:
    reviewed = _fetch_pr_like("prs", "--reviewed-by", user, since, owner, repos)
    return [pr for pr in reviewed if pr["author"] != user]


def fetch_issues(user: str, since: dt.date, owner: str | None, repos: list[str]) -> list[dict]:
    return _fetch_pr_like("issues", "--author", user, since, owner, repos)


def describe_event(event: dict) -> str:
    payload = event.get("payload") or {}
    kind = event["type"]
    if kind == "PushEvent":
        messages = [c["message"].splitlines()[0] for c in payload.get("commits") or []]
        ref = (payload.get("ref") or "").removeprefix("refs/heads/")
        pushed = f"pushed {len(messages)} commit(s) to {ref}"
        return f"{pushed}: {' | '.join(messages)}" if messages else pushed
    if kind == "PullRequestEvent":
        pr = payload.get("pull_request") or {}
        return f"{payload.get('action')} PR #{pr.get('number')}: {pr.get('title') or ''}".strip(": ")
    if kind == "PullRequestReviewEvent":
        pr = payload.get("pull_request") or {}
        return f"reviewed PR #{pr.get('number')}: {pr.get('title') or ''}".strip(": ")
    if kind in ("IssuesEvent", "IssueCommentEvent"):
        issue = payload.get("issue") or {}
        action = "commented on" if kind == "IssueCommentEvent" else payload.get("action")
        return f"{action} #{issue.get('number')}: {issue.get('title') or ''}".strip(": ")
    if kind == "CreateEvent":
        return f"created {payload.get('ref_type')} {payload.get('ref') or ''}".strip()
    if kind == "DeleteEvent":
        return f"deleted {payload.get('ref_type')} {payload.get('ref')}"
    return kind


def fetch_events(user: str, since: dt.date, owner: str | None, repos: list[str]) -> list[dict]:
    raw = gh("api", f"users/{user}/events?per_page=100", "--paginate")
    wanted = {qualify(owner, r).lower() for r in repos} if repos else None
    prefix = owner.lower() + "/" if owner else None
    events = []
    for event in parse_concat_json(raw):
        name = event["repo"]["name"]
        if prefix and not name.lower().startswith(prefix):
            continue
        if wanted is not None and name.lower() not in wanted:
            continue
        if event["created_at"][:10] < since.isoformat():
            continue
        events.append(
            {
                "date": event["created_at"][:10],
                "time": event["created_at"],
                "repo": name,
                "type": event["type"],
                "detail": describe_event(event),
            }
        )
    return sorted(events, key=lambda e: e["time"], reverse=True)


# --- output -----------------------------------------------------------------


def print_commits(commits: list[dict]) -> None:
    for c in commits:
        print(f"{c['date']}  {c['repo']}  {c['sha']}  {c['message']}")


def print_pr_like(items: list[dict]) -> None:
    for i in items:
        by = f"  by {i['author']}" if i["author"] else ""
        print(f"{i['updated']}  {i['repo']}#{i['number']}  [{i['state']}]  {i['title']}{by}")


def print_events(events: list[dict]) -> None:
    for e in events:
        print(f"{e['date']}  {e['repo']}  {e['detail']}")


def print_summary(user: str, since: dt.date, owner: str | None, data: dict) -> None:
    scope = f"in {owner}" if owner else "across GitHub"
    print(f"Activity for {user} {scope} since {since}\n")
    repo_names = sorted(
        {item["repo"] for section in data.values() for item in section},
        key=str.lower,
    )
    if not repo_names:
        print("No activity found.")
        return
    sections = [
        ("commits", "Commits", lambda c: f"{c['date']}  {c['sha']}  {c['message']}"),
        ("prs", "PRs authored", lambda p: f"#{p['number']}  [{p['state']}]  {p['title']}"),
        ("reviews", "PRs reviewed", lambda p: f"#{p['number']}  [{p['state']}]  {p['title']}  by {p['author']}"),
        ("issues", "Issues opened", lambda i: f"#{i['number']}  [{i['state']}]  {i['title']}"),
        ("comments", "Comments", lambda e: f"{e['date']}  {e['detail']}"),
    ]
    for repo in repo_names:
        print(repo)
        for key, label, fmt in sections:
            items = [i for i in data[key] if i["repo"] == repo]
            if not items:
                continue
            print(f"  {label} ({len(items)}):")
            for item in items:
                print(f"    {fmt(item)}")
        print()
    totals = ", ".join(
        f"{len(data[key])} {label.lower()}" for key, label, _ in sections if data[key]
    )
    print(f"Totals: {totals or 'nothing'}")


# --- main -------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("repos", nargs="*", metavar="repo",
                        help="repo name(s) to scope to (default: all repos in the org)")
    common.add_argument("--owner", help="org/user to scope to (default: no scope — all your activity)")
    common.add_argument("--since", default="friday",
                        help="start date: YYYY-MM-DD, <N>d, or weekday name (default: friday)")
    common.add_argument("--user", help="GitHub login to report on (default: authenticated user)")
    common.add_argument("--json", action="store_true", help="emit JSON instead of text")

    parser = argparse.ArgumentParser(
        prog="gh_activity.py",
        description="Summarize your GitHub activity, optionally scoped to an org or specific repos (uses the gh CLI).",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("summary", parents=[common], help="full summary grouped by repo (default)")
    sub.add_parser("commits", parents=[common], help="commits you authored")
    sub.add_parser("prs", parents=[common], help="pull requests you authored")
    sub.add_parser("reviews", parents=[common], help="pull requests you reviewed (authored by others)")
    sub.add_parser("issues", parents=[common], help="issues you opened")
    sub.add_parser("events", parents=[common], help="raw event feed (pushes, comments, branches, ...)")
    return parser


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    # No subcommand (or a bare repo scope) means "summary".
    if not argv or (argv[0] not in COMMANDS and argv[0] not in ("-h", "--help")):
        argv.insert(0, "summary")
    args = build_parser().parse_args(argv)

    user = args.user or gh("api", "user", "--jq", ".login").strip()
    since = parse_since(args.since)

    if args.command == "summary":
        data = {
            "commits": fetch_commits(user, since, args.owner, args.repos),
            "prs": fetch_prs(user, since, args.owner, args.repos),
            "reviews": fetch_reviews(user, since, args.owner, args.repos),
            "issues": fetch_issues(user, since, args.owner, args.repos),
            "comments": [
                e for e in fetch_events(user, since, args.owner, args.repos)
                if e["type"] == "IssueCommentEvent"
            ],
        }
        if args.json:
            print(json.dumps({"user": user, "owner": args.owner, "since": since.isoformat(), **data}, indent=2))
        else:
            print_summary(user, since, args.owner, data)
        return

    fetchers = {
        "commits": (fetch_commits, print_commits),
        "prs": (fetch_prs, print_pr_like),
        "reviews": (fetch_reviews, print_pr_like),
        "issues": (fetch_issues, print_pr_like),
        "events": (fetch_events, print_events),
    }
    fetch, show = fetchers[args.command]
    items = fetch(user, since, args.owner, args.repos)
    if args.json:
        print(json.dumps(items, indent=2))
    elif items:
        show(items)
    else:
        print("No results.")


if __name__ == "__main__":
    main()
