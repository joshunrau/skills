---
name: writing-software-specs
description: Draft or edit a software specification (SPEC.md) for a platform or feature. Use when creating, revising, or extending a spec.
---

# Writing Software Specs

A spec is the top-level source of truth for a platform or feature before it is implemented. It establishes a foundation, not every implementation detail. It grows over time: an early draft may state only behavior, and later edits add technical decisions.

## Reader

An implementer: a coding agent, or a software engineer who understands the domain. Leave domain concepts unexplained. Define everything specific to the project.

## Drafting

1. Explore the current repo for facts: existing code, docs, and any prior spec. Do not explore outside the current repo unless explicitly asked.
2. Draft the full spec in the format below. Write only what has been decided. An undecided point is one the spec would state once decided: behavior, or a foundational decision (see Style). Each becomes an entry in Appendix A with a recommendation; never fill it with a guess or a placeholder. Anything else is left to the implementer and stays out of the spec.
3. Review the draft (see Review).
4. Revise.

## Editing

1. Read the whole spec before changing anything.
2. Make the change.
3. Update every other section the change affects.
4. Remove any contradiction between sections.
5. Resolve or add entries in Appendix A.
6. Review the spec (see Review) after any edit that adds, removes, or changes a rule, a concept, or an axiom. Wording fixes need no review.

The spec describes the system as currently intended. Do not record history, changelogs, or superseded plans; version control holds them.

## Format

Number every section except Appendix A. Within the Overview and each concept section, write numbered clauses, each with a bold short title, such as `**1.1 Purpose:**`.

### 1. Overview

Briefly state the purpose of the software or feature, then anything else relevant to this spec, such as core requirements or target users. State the scope of the spec and what is out of scope. Include one generic clause in the scope stating that anything the spec does not specify is left to the implementer. Do not repeat this per rule.

### 2. Axioms

A short numbered list labeled A1, A2, and so on. Each axiom is a bold statement plus one or two sentences. An axiom describes a property of the system, not a feature. Axioms explain why the rules exist, so the rules can be derived from them. They are abstract principles, not structural decisions or implementation details.

### 3 onward: Concepts

One section per concept, titled `## N. {Concept}`. A concept is a thing in the system that has its own rules: an entity, a component, a workflow, or an interface. Order the sections so that nothing is used before it is defined.

### Appendix A: Open Decisions

One entry per undecided point, each with a bold short title. In a short paragraph, state the question, the concept it blocks (by name), the options considered, and the recommended option with a one-clause reason. When a decision is made, delete the entry and write the answer into the body. Leave no trace that it was open.

## Style

- The body is purely normative. Write short declarative sentences in the present tense that state behavior as fact: "is", not "should". Do not use RFC 2119 keywords.
- Use active voice and one idea per sentence.
- Write prose by default. Use bullets only for genuine enumerations, or for a few sub-rules under one clause.
- Bold a defined term once, where it is defined. Afterwards use it consistently: one term per concept, never a synonym. Italicize enumerated values, such as states and reasons.
- Never cite another section or clause of the spec. The only citations are axioms, written inline as a parenthetical, such as (A1), after the rule that enforces the axiom.
- Give rationale only when a rule is contestable, costly, or not self-explanatory, and then in one clause.
- Include implementation detail only where it fixes user-facing behavior or is a foundational decision: one that other parts of the system build on and that is costly to reverse.
- Earn every detail. Cut anything that changes neither what the implementer builds nor their understanding of why a rule exists.
- Do not use em dashes.

## Review

Spawn a fresh subagent. Give it only the spec and this skill, with this brief:

> Report only (a) lines that break a rule in this skill and (b) places where the spec contradicts itself. Give the location of each. The spec may be incomplete: missing rules or concepts are not a problem, but a missing section or Overview element that this skill requires is. Do not suggest rewordings, stylistic preferences, or additions. Reporting nothing is the expected result for a sound spec.

Fix each reported problem. If a fix requires a decision, add it to Appendix A instead. Run at most two review rounds. If the second round still reports problems, stop and list them for the user.
