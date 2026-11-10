---
name: writing-software-specs
description: Draft or edit the product specification for a platform or feature. Use when creating, revising, or extending a spec.
---

# Writing Software Specs

A spec is the top-level source of truth for a platform or feature before it is implemented. It establishes decided foundations for an implementer.

The spec is the file that `AGENTS.md` lists as the product specification under `## Reference Files`. When none is listed there, ask the user for the path.

## Reader

An experienced human software engineer who reads the whole document and builds from it. "The implementer" below means this reader.

## Structure

Build from `references/skeleton.md`. Sections run from most to least foundational. A lower section serves the sections above it and never contradicts them. The body is every section after Axioms except Blocking Decisions and Open Decisions.

The spec reads from top to bottom. Each passage is understandable from what precedes it, and each sentence is understandable without following its citations. When a reader would naturally wonder about a topic that a later section settles, point to that section in a few words, rather than leave the question open or bend the text to avoid the topic.

## Missing Decisions

A decision is missing when text being written, or already written, cannot be stated exactly without it and no existing decision settles it. A topic the spec does not yet address is not a missing decision.

Ask the user about every missing decision as soon as it surfaces. Never settle one by assumption.

If the user defers a decision, record it by what already exists:

- **Blocking Decision:** text already in the spec depends on the decision or presumes an answer to it. Record it with the sections it affects. Existing text stays as it is. Until no entries remain, the spec takes no new rules or sections. The permitted changes are resolving entries, editing Blocking Decisions and Open Decisions, applying checklist findings, and wording-only edits.
- **Open Decision:** no text in the spec depends on the decision yet. Record it with the sections it would affect. Work continues, but text that would depend on the decision is not written until it is resolved. Text found to depend on an Open Decision is removed.

## Axioms

An axiom is one sentence that ends by citing the core requirement it serves, such as "(R1)". It states a result that at least two different mechanisms could satisfy. It carries no exceptions.

- Mechanism, rejected: "The editor saves every keystroke to the server within one second (R1)."
- Result, accepted: "A user never loses text they have typed (R1)."

An axiom may carry a boundary clause, which limits its scope by a general condition that applies uniformly: "while that data exists". An exception carves out a specific case, actor or situation: "except for administrators", "unless the device is offline". Boundaries are allowed. Exceptions are not.

When adding an axiom, check it against each existing axiom: does fully honoring either one ever require limiting the other? If so, ask the user which promise yields, and add a boundary clause to that axiom. For example, "Changes to data are attributable and reconstructable" conflicts with "A user can permanently delete their data." If the first yields, it becomes "Changes to data are attributable and reconstructable while that data exists."

An axiom that seems to need an exception has a missing decision behind it. Find that decision and ask the user.

## Detail

- A section is never more precise than the decisions it depends on.
- The spec is exact only about behavior that is costly to change and about structural technical decisions. Everything else leaves room for the implementer.
- A section that keeps gaining special cases about another section signals a missing decision upstream. Find that decision and ask the user before writing more.
- A requested detail that depends on a missing or open decision waits until the user settles that decision.

## Consistency

- Any internal contradiction is a defect. Silence is acceptable. When two rules answer the same case differently, fix the wording if existing decisions settle it. Otherwise ask the user which rule holds. If the user defers, record it as a Blocking Decision.
- One term per concept, one concept per term. A rename replaces every occurrence in the same edit.
- A term is defined once, in bold, at its first use in the body, in the same edit that first uses it. A sentence that only says what a later section covers may name a term before its definition and is not its first use. The defining sentence is a body sentence: when the rule that governs a thing also says what it is, that one sentence is the definition. A category is defined by a criterion, not by listing its members.
- Overview and Axioms define no terms. A term used there is the one the body defines.
- Defined terms are the dependency index. When a decision changes, find every use of each defined term it introduces or relies on, and re-read each rule that uses them.
- The spec states current decisions only. A resolved entry leaves Blocking Decisions or Open Decisions and its answer enters the body. History lives in version control.

## After Each Revision That Changes a Decision or a Term

Spawn a fresh Opus subagent. Give it only the spec and `references/checklist.md`, never the conversation, with this prompt:

> Report only violations of the checklist. Give the location of each. The spec may not yet cover every topic: an absent topic is not a violation, but text that is present must satisfy the checklist. A conflict already cited by a Blocking Decisions entry is not a violation. Reporting nothing is the expected result for a sound spec.

Apply each finding or reject it. Tell the user each rejected finding and the reason. The revision is complete when every finding has one outcome.

Wording-only edits skip this. Renaming a defined term is not wording-only.

## Format and Style

Clarity comes before brevity. Cut a sentence that adds nothing the implementer needs to build or to understand a rule. Keep the context, transitions and connecting words that make a rule easy to follow, even when the rule would still be exact without them.

Load the `writing-normative-prose` skill. Every rule in it applies to a spec. The rules below add to it.

Headings and emphasis:

- Section heading: `### **1. {Section}.**`
- Subsection heading: `**1.1 {Subsection}.**` followed by its text on the same line. A subsection that needs them has sub-subsections in the same form: `**1.1.1 {Sub-subsection}.**`
- Title case for headings.
- Bold marks a term at its definition and the label of a list item. Italics mark a value from a set the spec enumerates that has no literal form, such as a status or a mode. A value that is both enumerated and literal takes a code span. No other emphasis.

Paragraphs:

- A paragraph holds one rule in at most six sentences. A case list that follows a rule's lead sentence does not count toward the six.

Lists:

- Prose by default. No tables.
- A list that is not the case list of a rule is a genuine enumeration, or a few sub-rules under one clause.

What is not written:

- Rationale. No "because", "so that", "therefore", "this serves" or trade-off anywhere. A sentence that explains why a rule exists is rationale even without these words.
- A rule a second time. A sentence that relies on a rule written elsewhere carries its section number, such as "the ownership check (4.2)".
- A restatement of an axiom. No sentence in the body restates an axiom or cites one. A rule that chooses how an axiom is met is a decision and is written. A property an axiom gives every instance of something, such as every error message, is not repeated in the rule for one instance. A message whose content is a decision of its own, such as an error code a client matches on, is written once, where the rule that produces it is defined.
- A consequence that follows from stated rules.
- A closure clause: a clause whose only content is that nothing beyond the rule happens or exists, such as "and nothing else" or "and no other". A rule is complete as written. A clause that gives everything outside the rule an outcome, such as "any other value is rejected", is a rule and stays. A lead sentence that states a set is closed, such as "a job is in exactly one of the following states", is part of the rule and stays.
- An example of a rule that is already exact in words. An example appears only for a syntax or a format, where it shows the exact shape.
- A bare citation to a later section. A citation points backward only, as a bare section number in parentheses at the end of the clause that relies on it. A later section is referred to by words that say what it covers, such as "The authorization mechanism is described in 5.1." A core requirement is cited by axioms and nowhere else.

## Anti-Patterns

Each pair shows text the checklist rejects and the text that replaces it. All are from a fictional spec for a job scheduler with an HTTP API: a job has a schedule, each scheduled time starts a run, and an API key owns the jobs it creates.

**Rationale.**

- Rejected: "A failed run is retried at most three times, so that a failing job cannot hold a worker indefinitely. This serves R2."
- Accepted: "A failed run is retried at most three times."

**Restating an axiom.** The spec has axiom A3: "Every refused request carries the reason for its refusal (R4)."

- Rejected: "The handler loads the job and compares its `ownerKeyId` with the requesting key. A mismatch is refused with status 403, and the response body explains in plain language that the job was not found (A3)."
- Accepted: "The handler loads the job and compares its `ownerKeyId` with the requesting key. A mismatch is refused with status 403."

**A rule written twice.** Section 4.2 says the handler requires the owner key.

- Rejected, in 7.3: "The handler cancels the job's queued runs. It requires the owner key (4.2)."
- Accepted, in 7.3: "The handler (4.2) cancels the job's queued runs."

**A definition apart from its rule.**

- Rejected: "An **owner key** is the API key that owns a job." Later: "The API key that creates a job owns it."
- Accepted: "The API key that creates a job is its **owner key**."

**A derived consequence.**

- Rejected: "A job has exactly one schedule, and a schedule belongs to exactly one job. Two jobs therefore never share a schedule."
- Accepted: "A job has exactly one schedule, and a schedule belongs to exactly one job."

**A closure clause.**

- Rejected: "A job is paused by its owner key, and nothing else pauses a job."
- Accepted: "A job is paused by its owner key."
- Stays, because it gives the complement an outcome: "A request with any other method is refused with status 405."

**A bare forward citation.** Retries are defined in 6.2.

- Rejected, in 5.1: "A run ends in one of three states, `succeeded`, `failed` or `cancelled`, and a failed run may be retried (6.2)."
- Accepted, in 5.1: "A run ends in one of three states: `succeeded`, `failed` or `cancelled`. Retries of a failed run are described in 6.2."

**A non-foundational implementation detail.** The behavior is exact. How the implementer achieves it is theirs.

- Rejected: "Queued runs live in a `runs` table with an index on `(jobId, scheduledAt)`. A `pollRuns` worker queries it every 500 ms and claims a run with `SELECT ... FOR UPDATE SKIP LOCKED`."
- Accepted: "A queued run starts within one second of its scheduled time. Two workers never start the same run."
