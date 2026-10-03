---
name: writing-software-specs
description: Draft or edit a software specification (SPEC.md) for a platform or feature. Use when creating, revising, or extending a spec.
---

# Writing Software Specs

A spec is the top-level source of truth for a platform or feature before it is implemented. It establishes decided foundations for an implementer, not every implementation detail.

## Structure

Build from `references/skeleton.md`. Sections run from most to least foundational. A lower section serves the sections above it and never contradicts them.

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
- The spec is exact only about user-visible behavior that is costly to change and about structural technical decisions. Everything else leaves room for the implementer.
- Each structural technical decision states the behavior or constraint it serves and the trade-off it accepts.
- A section that keeps gaining special cases about another section signals a missing decision upstream. Find that decision and ask the user before writing more.
- A requested detail that depends on a missing or open decision waits until the user settles that decision.

## Consistency

- Any internal contradiction is a defect. Silence is acceptable. When two rules answer the same case differently, fix the wording if existing decisions settle it. Otherwise ask the user which rule holds. If the user defers, record it as a Blocking Decision.
- One term per concept, one concept per term. A rename replaces every occurrence in the same edit.
- A term enters Definitions in the same edit that first uses it in the body.
- Defined terms are the dependency index. When a decision changes, find every use of each defined term it introduces or relies on, and re-read each rule that uses them.
- The spec states current decisions only. A resolved entry leaves Blocking Decisions or Open Decisions and its answer enters the body. History lives in version control.

## After Each Revision That Changes a Decision or a Term

Spawn a fresh Opus subagent. Give it only the spec and `references/checklist.md`, never the conversation, with this prompt:

> Report only violations of the checklist. Give the location of each. The spec may not yet cover every topic: an absent topic is not a violation, but text that is present must satisfy the checklist. A conflict already cited by a Blocking Decisions entry is not a violation. Reporting nothing is the expected result for a sound spec.

Apply each finding or reject it. Tell the user each rejected finding and the reason. The revision is complete when every finding has one outcome.

Wording-only edits skip this. Renaming a defined term is not wording-only.

## Format and Style

- Section heading: `### **1. {Section}.**`
- Subsection heading: `**1.1 {Subsection}.**` followed by its text on the same line.
- Title case for headings and defined terms.
- Prose by default. Bullets only for genuine enumerations, or a few sub-rules under one clause. No tables.
- Short declarative sentences in the present tense that state behavior as fact: "is", not "should". No RFC 2119 keywords.
- Active voice, one idea per sentence. Commas, colons and periods in place of em dashes.
- Earn every detail: keep a sentence only if it changes what the implementer builds or their understanding of why a rule exists.
- Cross-reference another section only for a real dependency.
