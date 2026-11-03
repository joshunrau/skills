---
name: writing-software-specs
description: Draft or edit a software specification (SPEC.md) for a platform or feature. Use when creating, revising, or extending a spec.
---

# Writing Software Specs

A spec is the top-level source of truth for a platform or feature before it is implemented. It establishes decided foundations for an implementer.

## Reader

An experienced human software engineer who reads the whole document and builds from it. "The implementer" below means this reader.

## Structure

Build from `references/skeleton.md`. Sections run from most to least foundational. A lower section serves the sections above it and never contradicts them. The body is every section except Definitions.

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
- A term is defined in the same edit that first uses it: inline if one top-level section uses it, in Definitions if more than one does. When an inline term is first used in a second top-level section, the same edit moves its definition to Definitions.
- Defined terms are the dependency index. When a decision changes, find every use of each defined term it introduces or relies on, and re-read each rule that uses them.
- The spec states current decisions only. A resolved entry leaves Blocking Decisions or Open Decisions and its answer enters the body. History lives in version control.

## After Each Revision That Changes a Decision or a Term

Spawn a fresh Opus subagent. Give it only the spec and `references/checklist.md`, never the conversation, with this prompt:

> Report only violations of the checklist. Give the location of each. The spec may not yet cover every topic: an absent topic is not a violation, but text that is present must satisfy the checklist. A conflict already cited by a Blocking Decisions entry is not a violation. Reporting nothing is the expected result for a sound spec.

Apply each finding or reject it. Tell the user each rejected finding and the reason. The revision is complete when every finding has one outcome.

Wording-only edits skip this. Renaming a defined term is not wording-only.

## Format and Style

Headings and emphasis:

- Section heading: `### **1. {Section}.**`
- Subsection heading: `**1.1 {Subsection}.**` followed by its text on the same line. A subsection that needs them has sub-subsections in the same form: `**1.1.1 {Sub-subsection}.**`
- Title case for headings and defined terms.
- Bold marks a term at its definition and the label of a list item. Italics mark a value from a set the spec enumerates that has no literal form, such as a status or a mode. Code spans mark literal text: anything that appears exactly as written in code, a file, a command line or a message the software sends or receives, such as an identifier, a flag, a header or a literal value. A value that is both enumerated and literal takes a code span. No other emphasis.
- A term used in more than one top-level section is defined in Definitions. A term used in one top-level section only is defined inline, in bold, at its first use, and is not in Definitions. An inline definition follows the same rules as a Definitions entry.

Sentences and paragraphs:

- Short declarative sentences in the present tense that state behavior as fact: "is", not "should". No RFC 2119 keywords.
- One idea per sentence. Commas, colons and periods in place of em dashes.
- Earn every detail: keep a sentence only if it changes what the implementer builds or their understanding of why a rule exists.
- The subject of a sentence is the thing the rule governs, such as an input, a stored item, a message or an actor, not the system being specified. The passive is allowed, and is the usual form when the actor is the system. The system is the subject only of a sentence about the system as a whole.
- A sentence names the set it governs. A quantifier with no noun ("everything", "anything", "whatever") or a clause standing in for a set ("what the input contains", "whichever applies") is a defect unless that sentence or the one before it enumerates the set.
- A paragraph holds one rule in at most six sentences. A case list that follows a rule's lead sentence does not count toward the six.
- Choose the exact word over the approximate one: "within five seconds", not "quickly"; "rounded to the nearest cent", not "rounded".
- Use a technical term when it says something more precisely than plain words and the implementer would know it without looking it up: "case-insensitive", not "ignoring capital letters"; "every read returns the most recently saved value", not "reads are linearizable".

Lists:

- Prose by default. No tables.
- A rule with a fixed set of cases is a lead sentence that names the set, then one list item per case: a bold label, the condition, and the outcome last. Two cases are still a list.
- Any other list is a genuine enumeration, or a few sub-rules under one clause.

What is not written:

- Rationale. No "because", "so that", "therefore", "this serves" or trade-off anywhere. In a behavior section or a Structural Technical Decision, a sentence stays only if it changes what the implementer builds.
- A rule a second time. A rule is written once. A sentence elsewhere that relies on it carries the section number, never the rule's content.
- A restatement of an axiom. No sentence in the body restates an axiom or cites one. A rule that chooses how an axiom is met is a decision and is written. A property an axiom gives every instance of something, such as every error message, is not repeated in the rule for one instance. A message whose content is a decision of its own, such as an error code a client matches on, is written once, where the rule that produces it is defined.
- A consequence that follows from stated rules.
- A closure clause: a clause whose only content is that nothing beyond the rule happens or exists, such as "and nothing else" or "and no other". A rule is complete as written. A clause that gives everything outside the rule an outcome, such as "any other value is rejected", is a rule and stays. A lead sentence that states a set is closed, such as "a job is in exactly one of the following states", is part of the rule and stays.
- An example of a rule that is already exact in words. An example appears only for a syntax or a format, where it shows the exact shape.
- A citation to a later section. A citation points backward only, as a bare section number in parentheses at the end of the clause that relies on it. A sentence that relies on a later section carries no citation. A core requirement is cited by axioms and nowhere else.

## Anti-Patterns

Each pair shows text the checklist rejects and the text that replaces it. All are from a fictional spec for a job scheduler with an HTTP API: a job has a schedule, each scheduled time starts a run, and an API key owns the jobs it creates.

**Rationale.**
- Rejected: "A failed run is retried at most three times, so that a failing job cannot hold a worker indefinitely. This serves R2."
- Accepted: "A failed run is retried at most three times."

**Restating an axiom.** The spec has axiom A3: "Every refused request carries the reason for its refusal (R4)."
- Rejected: "The handler loads the job and compares its `ownerKeyId` with the requesting key. A mismatch is refused with status 403, and the response body explains in plain language that the job was not found (A3)."
- Accepted: "The handler loads the job and compares its `ownerKeyId` with the requesting key. A mismatch is refused with status 403."

**A rule written twice.** Section 4.2 says the handler requires the owner key.
- Rejected, in 7.3: The handler cancels the job's queued runs. It requires the owner key (4.2)."
- Accepted, in 7.3: The handler (4.2) cancels the job's queued runs."

**A derived consequence.**
- Rejected: "A job has exactly one schedule, and a schedule belongs to exactly one job. Two jobs therefore never share a schedule."
- Accepted: "A job has exactly one schedule, and a schedule belongs to exactly one job."

**A closure clause.**
- Rejected: "A job is paused by its owner key, and nothing else pauses a job."
- Accepted: "A job is paused by its owner key."
- Stays, because it gives the complement an outcome: "A request with any other method is refused with status 405."

**A forward citation.** Retries are defined in 6.2.
- Rejected, in 5.1: "A run ends in one of three states, `succeeded`, `failed` or `cancelled`, and a failed run may be retried (6.2)."
- Accepted, in 5.1: "A run ends in one of three states: `succeeded`, `failed` or `cancelled`."

**A quantifier over an unnamed set.**
- Rejected: "Everything a request carries is validated before it is acted on."
- Accepted: "Every request body is parsed with the JSON Schema of its endpoint before the handler runs. A body the schema rejects is refused with status 400."

**The system as subject.**
- Rejected: "The scheduler checks the schedule expression. The scheduler rejects an expression with a field out of range."
- Accepted: "A `schedule` with a field out of its range is refused with status 400."

**A fixed set of cases in prose.**
- Rejected: "After a run fails, a new run is queued when the job's retry limit is not reached, no run is queued when the job is paused or deleted, and otherwise the job waits for its next scheduled time."
- Accepted: "After a run fails, one of three things follows:
  - **Retry.** The job's `retryLimit` is not reached: a new run is queued.
  - **Cancel.** The job is paused or deleted: no run is queued.
  - **Wait.** Otherwise: the job waits for its next scheduled time."

**A non-foundational implementation detail.** The behavior is exact. How the implementer achieves it is theirs.
- Rejected: "Queued runs live in a `runs` table with an index on `(jobId, scheduledAt)`. A `pollRuns` worker queries it every 500 ms and claims a run with `SELECT ... FOR UPDATE SKIP LOCKED`."
- Accepted: "A queued run starts within one second of its scheduled time. Two workers never start the same run."
