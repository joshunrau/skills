---
name: gh-activity
description: Summarize your GitHub activity (commits, PRs authored, PRs reviewed, issues, comments) across an org or specific repos since a given date. Useful for standup notes, weekly recaps, or answering "what did I work on?".
disable-model-invocation: true
---

# GitHub Activity Summary

Fetch the user's GitHub activity with the bundled `scripts/gh_activity.py` script in this skill's directory. It wraps the `gh` CLI and reuses the caller's existing authentication — no tokens needed. Requires `gh` to be installed and logged in (`gh auth status` to verify).

## IMPORTANT: invoke without sandbox

Always run the script with the Bash sandbox disabled (`dangerouslyDisableSandbox: true`). When `gh` is spawned from Python inside a macOS sandbox, TLS certificate verification can fail intermittently with keychain error `OSStatus -26276`. The script only reads from the GitHub API via the user's own `gh` auth, so running it unsandboxed is expected and authorized.

## Usage

```sh
python3 <skill-dir>/scripts/gh_activity.py [subcommand] [repos ...] [flags]
```

Subcommands (default is `summary` — bare repo names after the script path are treated as scope):

| Subcommand | What it returns |
|---|---|
| `summary` | Everything below, grouped by repo, with a totals line |
| `commits` | Commits the user authored |
| `prs` | Pull requests the user authored |
| `reviews` | Pull requests the user reviewed (authored by others) |
| `issues` | Issues the user opened |
| `events` | Raw event feed: pushes, branch create/delete, comments |

Flags (valid on every subcommand):

- `repos ...` — positional repo names to scope to; bare names require `--owner`, or use full `owner/name` form (default: no repo filter)
- `--owner OWNER` — org/user to scope to (default: no scope — activity everywhere)
- `--since WHEN` — start date: `YYYY-MM-DD`, `<N>d` (e.g. `7d`), or a weekday name meaning the most recent past one (default: `friday`)
- `--user LOGIN` — GitHub login to report on (default: the authenticated user)
- `--json` — machine-readable output

Examples:

```sh
python3 <skill-dir>/scripts/gh_activity.py                          # summary, all activity, since last Friday
python3 <skill-dir>/scripts/gh_activity.py --owner some-org         # summary scoped to an org
python3 <skill-dir>/scripts/gh_activity.py some-org/some-repo       # summary scoped to one repo
python3 <skill-dir>/scripts/gh_activity.py commits --since 7d       # commits from the last week
python3 <skill-dir>/scripts/gh_activity.py reviews --since 2026-08-01
```

## Presenting results

Interpret the scope and date range from the user's request ("my work in org X since last Friday", "this week") and pass them via `--owner`/`repos`/`--since`. Run `summary` first unless the user asked for one specific slice.

Then write a readable narrative for the user, not a dump of the raw output: group related work into themes (e.g. a feature that spans several repos, review work vs. authored work), note which days were active, and call out anything open or in progress. Keep the raw per-repo detail available but lead with the story.

Known data quirks (from the GitHub events API, not script bugs): merge pushes may report "0 commits", and PR titles can be missing from `events` output — the search-based subcommands (`prs`, `reviews`, `commits`) have the authoritative details.
