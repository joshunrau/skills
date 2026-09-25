---
name: writing-skills-for-agents
description: Draft or edit skills for Claude or other agents. Use for drafting, editing, reviewing, or editing any skills.
---

# Writing Skills for Agents

Rule: another agent reading this skill, with zero prior context and no files other than those committed in the repo, should be able to understand everything in the skill completely.

Test: have a subagent verify this.

## Anti-Patterns

### Example 1

**Context:** `find-prospects` is used when the agent is asked to find or research sales prospects. It searches university and research-institute directories for principal investigators in the company's target fields and records each one, with a verified email, in a prospect database.

~~~~markdown
## PI Discovery Run (Jun 2026) — Atlantic Provinces

UNB, Memorial, and Dalhousie were processed in parallel (one subagent each). Results:

| University | Unique PIs | Fields |
|---|---|---|
| UNB (id=6) | 29 | psych(29), clinical(9), neuro(7), cognitive(5), psychiatry(0) |
| Memorial (id=3) | 52 | psych(31), neuro(15), psychiatry(14), clinical(10), cognitive(7) |
| Dalhousie (id=27) | 76 | psychiatry(42), psych(22), neuro(10) |

**Dalhousie gap:** The Psychiatry department directory uses JS pagination (116 faculty, 5 pages).
Only page 1 was captured via `web_extract`. Pages 2–5 require browser tools. Dalhousie is
undercounted — likely 80+ additional PIs remain. Same issue affects Psychology & Neuroscience.

**Subagent budget:** Both Memorial and Dalhousie subagents exhausted the 45-API-call cap. Large
medical schools routinely need 60+ calls.
~~~~


### Example 2

**Context:** `discover-institutions` is used to find new institutions to prospect, such as universities, hospital research institutes and health-authority research centres. It describes how to search for them and how to check that their researcher directories are worth extracting before adding them to the database.

**Excerpt:**

~~~~markdown
## Canadian Hospital Research Institute Directory URLs

Verified June 2026. Direct links to researcher directories at hospital-based and health-authority
research institutes across Western Canada. These are the "hidden" clinical research pools —
researchers listed here often don't appear in university departmental faculty directories.

### British Columbia

| Institute | Directory URL | Scale |
|---|---|---|
| Vancouver Coastal Health Research Institute (VCHRI) | https://www.vchri.ca/researcher-directory | 2,400+ investigators, A-Z browsable, 5+ pages |
| BC Children's Hospital Research Institute (BCCHR) | https://www.bcchr.ca/research/find-a-researcher/ | 480+ researchers, 30 pages, filterable by theme |
| Providence Health Care Research Institute | https://www.providenceresearch.ca/en/researcher-directory | ~140 researchers, 9 pages, filterable by specialty (psychiatry, neurology, etc.) |
| Women's Health Research Institute (WHRI) | https://www.whri.org/find-a-researcher | 9 pages, searchable by research theme (182 maternal/fetal health) |
~~~~

## Example 3

**Context:** `find-prospects` is used when the agent is asked to find or research sales prospects. It searches university and research-institute directories for principal investigators in the company's target fields and records each one, with a verified email, in a prospect database.

**Excerpt:**

~~~~markdown
### Drupal SAML Login Gate (McGill)

**Symptom:** After passing Azure WAF, the rendered page shows: "Access denied. You may need to
login to access this page." The page template is `page-saml-denied`.

**How it works:** Specific Drupal nodes are restricted to authenticated users via McGill's SSO
(SAML). Not a bot detection — this is access control. The node requires McGill credentials.

**Bypassable?** No. Requires actual McGill login credentials. This is a hard blocker — mark the
field Tier 3 and move on.
~~~~

## Example 4

**Context:** `find-prospects` is used when the agent is asked to find or research sales prospects. It searches university and research-institute directories for principal investigators in the company's target fields and records each one, with a verified email, in a prospect database.

**Excerpt:**

~~~~markdown
**Workaround when found:** Check for unprotected sub-pages listing the same faculty. At McGill, the
main `/psychology/people-0/faculty` requires SAML login, but
`/psychology/graduate/program-tracks/clinical/clinical-faculty` (clinical track sub-page) is public
and lists 16 clinical faculty with profile links.
~~~~

## Example 5

**Context:** `find-prospects` is used when the agent is asked to find or research sales prospects. It searches university and research-institute directories for principal investigators in the company's target fields and records each one, with a verified email, in a prospect database.

**Excerpt:**

~~~~markdown
## Dalhousie-Specific Notes

- Psychology & Neuroscience: `https://www.dal.ca/faculty/science/psychology_neuroscience/faculty-staff/our-faculty.html` — 55 faculty, 10 per page, 6 pages. Emails on listing. Results container class: `cmp-profilefinder__results`.
- Psychiatry: `https://medicine.dal.ca/departments/department-sites/psychiatry/our-people/faculty.html` — 116 faculty, 25 per page, 5 pages. Emails on profile pages only.
- Both use the same AEM-based framework with identical pagination pattern.
~~~~

## Example 6

**Context:** `find-prospects` is used when the agent is asked to find or research sales prospects. It searches university and research-institute directories for principal investigators in the company's target fields and records each one, with a verified email, in a prospect database.

**Excerpt:**

~~~~markdown
## Affected Sites

- **Université de Sherbrooke** — `/recherche/specialistes/details/*` profile pages
- **CRCHUS** axis pages also TYPO3-based but `web_extract` works for listing pages (not individual profiles)
~~~~

## Example 7

**Context:** `find-prospects` is used when the agent is asked to find or research sales prospects. It searches university and research-institute directories for principal investigators in the company's target fields and records each one, with a verified email, in a prospect database.

**Excerpt:**

~~~~markdown
### CRCHUS (Centre de recherche du CHUS)
- **Page:** `crchus.ca/axes-de-recherche` — 6 research axes with ~300 total researchers
- **Best axis for bulk extraction:** Santé: populations, organisation, pratiques (`crchus.ca/axes-de-recherche/sante-populations-organisation-pratiques`) — 26+ researchers with UdeS specialist profile links
- **Email pattern:** `Firstname.Lastname@USherbrooke.ca`
- **Blocking:** Listing pages accessible via `web_extract`; individual profile pages behind TYPO3 TSPD — use `requests` with Chrome UA (see `references/typo3-tspd-bypass.md`)
- **Result:** 21 clinical research PIs from Santé Populations axis alone

### CDRV (Centre de recherche sur le vieillissement)
- **Page:** `cdrv.ca/recherche/chercheurs` — Axe Autonomisation + Axe Géroscience, ~60 researchers
- **Best for:** FMSS-affiliated researchers doing clinical aging/geriatric research
- **Email pattern:** `Firstname.Lastname@USherbrooke.ca`
- **Blocking:** Same TYPO3 TSPD as UdeS profile pages
- **Result:** 11 clinical research PIs (rehabilitation, nursing, surgery, occupational therapy)
~~~~

## Example 8

**Context:** `find-prospects` is used when the agent is asked to find or research sales prospects. It searches university and research-institute directories for principal investigators in the company's target fields and records each one, with a verified email, in a prospect database.

**Excerpt:**

~~~~markdown
## What Google snippets contain (Brock University case study)

For Brock's Drupal-based site, Google snippets included:
- Full name
- Academic rank (Professor, Associate Professor, Assistant Professor)
- Email address (full `@brocku.ca` address)
- Office location and phone extension
- Department
- Partial research description (first 1-2 sentences of profile page)

Example snippet:
> "Professor, Ph.D. (U. of Toronto), Canada Research Chair in Cognitive Neuroscience of Aging Office: [redacted] [redacted] [redacted]@brocku."
~~~~

## Example 9

**Context**: `reviewing-run-extracts` is used when an agent is asked to review extracted data/turns/reasoning from an agent framework to optimize it.

~~~~markdown
## Ground Rules
  - ...
  - Earlier review decisions and the owner's rulings are information with their reasoning, never authority. Checkers
  and critics attack them freely. While checkers were told those decisions were "agreed direction", the regression
  checks rejected 1 fix in 30. Once that framing was dropped, they rejected 11 in 61.
~~~~
