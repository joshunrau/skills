---
name: gh-activity
description: Summarize your GitHub activity (commits, PRs authored, PRs reviewed, issues, comments) across an org or specific repos since a given date. Useful for standup notes, weekly recaps, or answering "what did I work on?".
disable-model-invocation: true
---

# GitHub Activity Summary

Fetch the user's GitHub activity with the bundled `scripts/gh_activity.py` script in this skill's directory. It wraps the `gh` CLI and reuses the caller's existing authentication, so no tokens are needed. Requires `gh` to be installed and logged in (`gh auth status` to verify).

## IMPORTANT: invoke without sandbox

Always run the script with the Bash sandbox disabled (`dangerouslyDisableSandbox: true`). When `gh` is spawned from Python inside a macOS sandbox, TLS certificate verification can fail intermittently with keychain error `OSStatus -26276`. The script only reads from the GitHub API via the user's own `gh` auth, so running it unsandboxed is expected and authorized.

## Usage

```sh
python3 <skill-dir>/scripts/gh_activity.py [subcommand] [repos ...] [flags]
```

Subcommands (default is `summary`; bare repo names after the script path are treated as scope):

| Subcommand | What it returns |
|---|---|
| `summary` | Everything below, grouped by repo, with a totals line |
| `commits` | Commits the user authored |
| `prs` | Pull requests the user authored |
| `reviews` | Pull requests the user reviewed (authored by others) |
| `issues` | Issues the user opened |
| `events` | Raw event feed: pushes, branch create/delete, comments |

Flags (valid on every subcommand):

- `repos ...`: positional repo names to scope to; bare names require `--owner`, or use full `owner/name` form (default: no repo filter)
- `--owner OWNER`: org/user to scope to (default: no scope, activity everywhere)
- `--since WHEN`: start date, given as `YYYY-MM-DD`, `<N>d` (e.g. `7d`), or a weekday name meaning the most recent past one (default: `friday`)
- `--user LOGIN`: GitHub login to report on (default: the authenticated user)
- `--json`: machine-readable output. Each PR and issue carries a `url` field, which the text output omits

Examples:

```sh
python3 <skill-dir>/scripts/gh_activity.py                          # summary, all activity, since last Friday
python3 <skill-dir>/scripts/gh_activity.py --owner some-org         # summary scoped to an org
python3 <skill-dir>/scripts/gh_activity.py some-org/some-repo       # summary scoped to one repo
python3 <skill-dir>/scripts/gh_activity.py commits --since 7d       # commits from the last week
python3 <skill-dir>/scripts/gh_activity.py reviews --since 2026-08-01
```

## Presenting results

Interpret the scope and date range from the user's request ("my work in org X since last Friday", "this week") and pass them via `--owner`/`repos`/`--since`. Run `summary --json` first unless the user asked for one specific slice; the JSON carries the PR and issue URLs the recap needs for links.

Then rewrite the output in the format below. Do not paste the script's output back; it is source material, not the deliverable.

Known data quirks (from the GitHub events API, not script bugs): merge pushes may report "0 commits", and PR titles can be missing from `events` output. The search-based subcommands (`prs`, `reviews`, `commits`) have the authoritative details.

## Output format

The same shape every time, so recaps from different weeks read as one series.

**Sections.** One section per repo, opened by the bare repo name in bold with the owner stripped (`**checkout-service**`, not `acme/checkout-service`). Use bold, not a markdown heading. Order the sections by how much total activity each repo holds, busiest first. Every repo gets its own section, even one holding a single item.

**No opening and no closing.** No title, no date range, no lead paragraph, no totals line. The first line of the recap is the first repo name.

**No numbers.** Never report counts, not in the repo name, not in the trailing bullets, not as a tally at the end. Name the items instead, or characterize them.

**Links.** Every PR and issue reference is a markdown link, so it is clickable: `[#412](https://github.com/acme/checkout-service/pull/412)`. Take the URL from the `url` field in the script's `--json` output. Commits have no URL, so a bullet built only from direct commits carries no reference at all; do not invent one.

**Bullets.** Each bullet is one unit of work, not one commit. Drop merge commits entirely. Where a PR exists it anchors the bullet; where a repo has only direct commits, cluster related commits into themed bullets rather than listing them.

Write bullets in past tense with an implied subject. State what changed, then add a clause naming the problem it solved when that is not self-evident from the change. Two lines at most.

**Plain language.** Describe a code change literally, as a change to code. Avoid inflated verbs and buzzwords: no minted, leveraged, orchestrated, harnessed, empowered, unlocked, surfaced, or delivered. Prefer added, removed, fixed, renamed, moved, split, replaced, and rewrote. Do not reuse PR titles or conventional-commit prefixes.

**No em dashes.** Never write an em dash. Use a comma, a colon, parentheses, or a second sentence. The single exception is text quoted verbatim from a source.

**Open work.** Work that has not landed stays in its repo section, phrased in the present participle, with `open` noted alongside the reference.

**Trailing bullets.** Close the list with these bullets, in this order, omitting any that would be empty:

- `Reviewed:` PRs the user reviewed, named and linked.
- `Filed:` issues the user opened that are still open. An issue the user both filed and closed within the window does not appear here; the fix is already a bullet of its own, and listing the filing reports the same work twice.
- `Discussed:` included only when comments amount to real work. Give the topics the thread covered, never a list of individual comments.

A repo whose only activity is a review or a discussion gets its bold name and those trailing bullets alone.

### Example

```markdown
**checkout-service**
- Added the database indexes that every cart query depends on, which were missing entirely ([#412](https://github.com/acme/checkout-service/pull/412))
- Closed an authorization gap that let any store manager delete another store's orders ([#418](https://github.com/acme/checkout-service/pull/418))
- Reworking refund expiry so a lapsed refund can be reissued rather than recreated ([#421](https://github.com/acme/checkout-service/pull/421), open)
- Reviewed: bulk coupon import ([#419](https://github.com/acme/checkout-service/pull/419)), the retry banner on failed payments ([#415](https://github.com/acme/checkout-service/pull/415))
- Filed: order totals drift by a cent on multi-currency carts ([#409](https://github.com/acme/checkout-service/issues/409))

**report-builder**
- Rebuilt template loading so templates compile at boot and load by name from a mounted directory, instead of shipping inside the app
- Split the template SDK into its own package, released on the same version line as the app
- Rewrote the reference pages as a field tree instead of tables

**design-system**
- Stacked number radio fields vertically when there are few options, so the second choice is no longer pushed to the right edge ([#119](https://github.com/acme/design-system/pull/119))

**docs-site**
- Discussed: heading capitalization, the deprecation banner wording, and whether the changelog belongs in the sidebar

**sdk-python**
- Reviewed: the async client's timeout defaults ([#77](https://github.com/acme/sdk-python/pull/77))
```

In that example, `design-system` also had an issue reporting the right-justified radio group, filed and closed inside the same window. It has no `Filed:` bullet, because the fix above it already covers that work.
