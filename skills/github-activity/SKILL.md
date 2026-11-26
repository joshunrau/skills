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

**Structure.**

1. One top-level bullet per repo: the bare repo name in bold with the owner stripped (`**checkout-service**`, not `acme/checkout-service`). Order repos by total activity, busiest first. Every repo gets its own bullet, even one holding a single item. Put a blank line between repo bullets.
2. Items under the repo, one per unit of work, followed by the category bullets described below.
3. Detail bullets under an item, from none to five.

Nesting goes deeper in two cases only. A theme item adds a level above the PRs it groups. A PR that exists only to make another PR possible nests under the detail bullet it supports, not beside it.

**No opening and no closing.** No title, no date range, no lead paragraph, no totals line. The first line of the recap is the first repo.

**Numbers.** Never count activity: no tallies of PRs, commits or issues, in the repo name, the category bullets, or at the end. A before-and-after figure that shows the size of a change is welcome, as a parenthetical: `(40 min -> 12 min)`.

**Links.** Every PR and issue reference is a markdown link, so it is clickable: `[#412](https://github.com/acme/checkout-service/pull/412)`. Take the URL from the `url` field in the script's `--json` output. Commits have no URL, so an item built only from direct commits carries no reference at all; do not invent one. A one-line summary of a repo's small PRs and maintenance (see Maintenance) carries no links either.

**Items.** One item per PR. When a PR makes several separate changes, list them as detail bullets under that one item; do not split the PR across items or chain the changes with "Also". PRs that follow up on each other may share one item carrying both links. Work without a PR (direct commits, releases, issue cleanup) is clustered into themed items. Drop merge commits entirely.

When several PRs in a repo serve one goal, group them under a theme item that names the goal ("Faster local builds and CI"). Under a theme, each PR is a short title-case label naming its area ("Test Suite", "Moved to the New Bundler"), and its details carry the changes.

Every other item is a past-tense sentence with an implied subject. Lead with what the work achieves, not how: "Updated to support only the new runtime" rather than "Replaced the module loader". The mechanism goes in a detail bullet. Mark a breaking change or a major release in parentheses: `(breaking change)`, `(new major version)`.

Give the reason only for a significant change whose reason is not obvious from the change itself, and put it in a detail bullet rather than appending it to the item. Small or self-explanatory work never gets a reason.

A PR closed in favour of a replacement is not mentioned. Link only the PR that landed, and leave out the history of how it got there.

**Details.** A major PR gets detail bullets naming its headline changes, up to five, written like items. Leave out side effects a reader would not ask about, such as a lint rule, test or doc change made along the way. A short parenthetical can carry scope: `(except the admin app)`. A small PR gets none.

**Maintenance.** Routine upkeep, such as dependency, runtime, package manager and release-tooling bumps, gets no item of its own. Fold it into a clause of the repo's main item ("and updated the release workflow"). A repo whose work is all small changes and upkeep gets a single sentence.

**Plain language.** Describe a code change literally, as a change to code. Describe a new setting by what it does, not by its identifier. Avoid inflated verbs and buzzwords: no minted, leveraged, orchestrated, harnessed, empowered, unlocked, surfaced, or delivered. Prefer added, removed, fixed, renamed, moved, split, replaced, and rewrote. Do not reuse PR titles or conventional-commit prefixes.

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
  - Faster local builds and CI
    - Test Suite ([#430](https://github.com/acme/checkout-service/pull/430))
      - Cut the suite down to the tests that need a browser (40 min -> 12 min)
      - Ran the suite against production builds rather than dev servers
      - Added a setting to skip the fraud-check call in tests
    - Moved to the New Bundler ([#427](https://github.com/acme/checkout-service/pull/427))
      - Replaced webpack with the new bundler (except the admin app)
        - Rewrote the asset plugin against the bundler's API ([#426](https://github.com/acme/checkout-service/pull/426))
      - Replaced the old minifier with the bundler's own
  - Fixed an authorization gap in order deletion ([#418](https://github.com/acme/checkout-service/pull/418))
    - Any store manager could delete another store's orders
  - Reworking refund expiry so a lapsed refund can be reissued ([#421](https://github.com/acme/checkout-service/pull/421), open)
  - Merged
    - Bulk coupon import ([#419](https://github.com/acme/checkout-service/pull/419))
    - Currency rounding in order totals ([#415](https://github.com/acme/checkout-service/pull/415))
  - Reviewed
    - Async export of order history ([#420](https://github.com/acme/checkout-service/pull/420))
  - Filed Issues
    - Order totals drift by a cent on multi-currency carts ([#409](https://github.com/acme/checkout-service/issues/409))

- **http-client**
  - Updated to support only the new runtime and drop the runtime dependency on the old compiler (breaking change) ([#88](https://github.com/acme/http-client/pull/88))
    - Replaced the third-party module loader with the client's own
    - Resolved imports with a native resolver

- **config-presets**
  - Adjusted to support only the new runtime (new major version) and updated the release workflow

- **docs-site**
  - Discussed
    - Heading capitalization
    - The deprecation banner wording
    - Whether the changelog belongs in the sidebar
```

In that example, `http-client` also had an earlier PR for the same change, closed after review found regressions. It is left out, because only the replacement landed. `config-presets` had a PR for the runtime change and two for dependency bumps, summed up in one unlinked line.
