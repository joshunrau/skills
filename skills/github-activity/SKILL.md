---
name: github-activity
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
| `merged` | Pull requests the user merged (authored by others) |
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

Write the recap to `ACTIVITY.md` in the current working directory, unless the user names another path or asks for it inline. Overwrite the file if it already exists.

Known data quirks (from the GitHub events API, not script bugs): merge pushes may report "0 commits", and PR titles can be missing from `events` output. The search-based subcommands (`prs`, `reviews`, `commits`) have the authoritative details.

## Output format

The same shape every time, so recaps from different weeks read as one series.

**Structure.** Three levels of bullets, never more:

1. One top-level bullet per repo: the bare repo name in bold with the owner stripped (`**checkout-service**`, not `acme/checkout-service`). Order repos by total activity, busiest first. Every repo gets its own bullet, even one holding a single item.
2. Items under the repo, one per unit of work, followed by the category bullets described below.
3. Detail bullets under an item, from none to five.

**No opening and no closing.** No title, no date range, no lead paragraph, no totals line. The first line of the recap is the first repo.

**No numbers.** Never report counts, not in the repo name, not in the category bullets, not as a tally at the end. Name the items instead, or characterize them.

**Links.** Every PR and issue reference is a markdown link, so it is clickable: `[#412](https://github.com/acme/checkout-service/pull/412)`. Take the URL from the `url` field in the script's `--json` output. Commits have no URL, so an item built only from direct commits carries no reference at all; do not invent one.

**Items.** One item per PR. When a PR makes several separate changes, list them as detail bullets under that one item; do not split the PR across items or chain the changes with "Also". PRs that follow up on each other may share one item carrying both links. Work without a PR (direct commits, releases, issue cleanup) is clustered into themed items. Drop merge commits entirely.

Write each item as a proper past-tense sentence with an implied subject, stating what changed. Most items need nothing more. Give the reason only for a significant change whose reason is not obvious from the change itself, and put it in a detail bullet rather than appending it to the item. Small or self-explanatory work never gets a reason.

**Details.** A major feature or PR gets detail bullets naming its notable changes, up to five, written like items. A small PR gets none.

**Plain language.** Describe a code change literally, as a change to code. Avoid inflated verbs and buzzwords: no minted, leveraged, orchestrated, harnessed, empowered, unlocked, surfaced, or delivered. Prefer added, removed, fixed, renamed, moved, split, replaced, and rewrote. Do not reuse PR titles or conventional-commit prefixes.

**No em dashes.** Never write an em dash. Use a comma, a colon, parentheses, or a second sentence. The single exception is text quoted verbatim from a source.

**Open work.** Work that has not landed stays in its repo, phrased in the present participle, with `open` noted alongside the reference.

**Leave out trivia.** Omit activity too small to mention, such as a single short comment on an issue.

**Category bullets.** Close each repo with these category bullets, in this order, omitting any that would be empty. Each is a bare label whose children are one PR or issue per line, named in a short phrase and linked. These children never get detail bullets.

- `Merged`: PRs by others that the user reviewed and that have merged (`reviews` entries with state `MERGED`), plus PRs the user merged (the `merged` list). List each PR once.
- `Reviewed`: the remaining PRs the user reviewed, still open or closed without merging. A PR under `Merged` never appears here.
- `Filed Issues`: issues the user opened that are still open. An issue the user both filed and closed within the window does not appear here; the fix is already an item of its own, and listing the filing reports the same work twice.
- `Discussed`: included only when comments amount to real work. Its children are the topics the thread covered, never individual comments.

A repo whose only activity falls under these categories gets its bold name and the category bullets alone.

### Example

```markdown
- **checkout-service**
  - Added the missing database indexes that cart queries depend on ([#412](https://github.com/acme/checkout-service/pull/412))
  - Fixed an authorization gap in order deletion ([#418](https://github.com/acme/checkout-service/pull/418))
    - Any store manager could delete another store's orders
  - Rewrote payment retries ([#424](https://github.com/acme/checkout-service/pull/424))
    - Moved retries from the browser to a background job
    - Spaced attempts on a backoff schedule
    - Added a banner showing when the next attempt will run
    - Logged each failed attempt with the provider's error code
  - Reworking refund expiry so a lapsed refund can be reissued ([#421](https://github.com/acme/checkout-service/pull/421), open)
  - Merged
    - Bulk coupon import ([#419](https://github.com/acme/checkout-service/pull/419))
    - Currency rounding in order totals ([#415](https://github.com/acme/checkout-service/pull/415))
  - Reviewed
    - Async export of order history ([#420](https://github.com/acme/checkout-service/pull/420))
  - Filed Issues
    - Order totals drift by a cent on multi-currency carts ([#409](https://github.com/acme/checkout-service/issues/409))
- **report-builder**
  - Rebuilt template loading so templates compile at boot and load by name from a mounted directory
  - Split the template SDK into its own package, released on the same version line as the app
  - Rewrote the reference pages as a field tree instead of tables
- **design-system**
  - Stacked number radio fields vertically when there are few options ([#119](https://github.com/acme/design-system/pull/119))
- **docs-site**
  - Discussed
    - Heading capitalization
    - The deprecation banner wording
    - Whether the changelog belongs in the sidebar
- **sdk-python**
  - Reviewed
    - The async client's timeout defaults ([#77](https://github.com/acme/sdk-python/pull/77))
```

In that example, `design-system` also had an issue reporting the right-justified radio group, filed and closed inside the same window. It has no `Filed Issues` bullet, because the item above already covers that work.
