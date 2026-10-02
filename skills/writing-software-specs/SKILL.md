---
name: writing-software-specs
description: Draft or edit a software specification (SPEC.md) for a platform or feature. Use when creating, revising, or extending a spec.
---

# Writing Software Specs

A spec is the top-level source of truth for a platform or feature before it is implemented. It establishes decided foundations for an implementer, not every implementation detail. 

## Structure

Build from `references/skeleton.md`. Sections run from most to least foundational. A lower section serves the sections above it and never contradicts them.

## Axioms

An axiom is one sentence. It traces to a core requirement in Section 1. It states a result that at least two different mechanisms could satisfy. It carries no exceptions and names no specific entity.

- Mechanism, rejected: "The editor saves every keystroke to the server within one second."
- Result, accepted: "A user never loses text they have typed." 

When adding an axiom, ask of each existing one: does fully honoring one ever require limiting the other? If so, resolve it with a boundary clause inside one sentence: "Changes to data are attributable and reconstructable while that data exists."

An axiom that seems to need an exception has a missing decision behind it. Determine the missing decision and definitively resolve it with the user.

## Detail

- A section is never more precise than the decisions it depends on.
- Precision arrives early only for user-visible behavior that is costly to change, or for a structural technical decision.
- Each structural technical decision states the behavior or constraint it serves and the trade-off it accepts.
- A section that keeps gaining special cases about another section signals a missing decision upstream. Find that decision before writing more.
- A requested detail that depends on an open decision stays out of the spec. Its parent decision goes to Open Questions.

## Consistency

- Any internal contradiction is a defect. Silence is acceptable. When two rules answer the same case differently, fix the wording if existing decisions settle it. Otherwise add an open question that names both rules.
- One term per concept, one concept per term. A rename replaces every occurrence in the same edit.
- Defined terms are the dependency index. When a decision changes, find every use of its terms and re-read each rule that uses them.
- The spec states current decisions only. A resolved question leaves Open Questions and its answer enters the body. History lives in version control.

## After Each Revision That Changes a Decision

Spawn a fresh Sonnet subagent. Give it only the spec and `references/checklist.md`, never the conversation, with this prompt:

> Report only violations of the checklist. Give the location of each. The spec may be incomplete: missing rules or concepts are not a problem. Reporting nothing is the expected result for a sound spec.

Apply each finding or reject it with a reason. The revision is complete when every finding has one outcome.

Wording-only edits skip this.

## Format and Style

- Section heading: `### **1\. {Section}.**`
- Subsection heading: `**1.1 {Subsection}.**` followed by its text on the same line.
- Title case for headings and defined terms.
- Prose by default. Bullets only for genuine enumerations, or a few sub-rules under one clause. No tables.
- Short declarative sentences in the present tense that state behavior as fact: "is", not "should". No RFC 2119 keywords.
- Active voice, one idea per sentence. Commas, colons and periods in place of em dashes.
- Earn every detail: keep a sentence only if it changes what the implementer builds or their understanding of why a rule exists.
- Cross-reference another section only for a real dependency.
