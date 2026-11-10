---
name: writing-implementation-plans
description: Draft or edit an implementation plan in the plans directory. Use when creating, revising, or extending a plan.
---

# Writing Implementation Plans

An implementation plan records what the user decided about a piece of work, and the order in which it is built. It is one file, `<topic>.md`, in the plans directory.

## Project Files

This skill names three places in the project by role: the plans directory, the product specification and the scratch directory. `AGENTS.md` gives the path of each under `## Reference Files`.

- **The plans directory and the scratch directory.** Ask the user for the path of one that is not listed there. The scratch directory is one that git ignores.
- **The product specification.** A project that lists none has none. Its plans cite no specification and have no Spec Amendments.

A plan names each of the three by its path.

## Readers

- **The implementer** builds one phase at a time. It has the repository, the plan and the handoff from the phase before, and no memory of the conversation that produced the plan.
- **The user** reads the plan to check that each decision is recorded as they made it.

## What a Plan Holds

- **The decisions carry the plan.** Each states what is true once the work is done, such as what a person sees, what is stored or what is refused. The phases only put the decisions in an order to build, so they are short.
- **A plan says what, and roughly where.** It says how only where the user decided how. An implementation written into a plan is a guess made before the code exists, and it buries the decisions that the user has to check.
- **A plan holds no record of progress.** What a phase did, and the state the work is in, go in the handoff, which Process describes.

## Structure

Build a new plan from `references/skeleton.md`. Decisions, Phases and Process are in every plan. Any other section is omitted when it would be empty.

## Decisions

- **Numbering.** One numbered list runs through the whole section, across its headings, so that "Decision 12" names the same decision for the life of the plan. A number never changes.
- **Later changes.** A decision added later takes the next number and goes at the end of the section, under a new heading when the last one does not fit it. A Markdown formatter renumbers a list in sequence, so a number placed anywhere else is rewritten. An addition to an existing decision, such as one more item out of scope, is written into that decision. A withdrawn decision keeps its number and reads "Withdrawn.", followed by a trace when Editing a Plan asks for one.
- **Scope first.** The first group states what is in scope, what is out of scope with what the work leaves ready for each excluded item, and each rule of the repository that the user waived for this work.
- **Form.** A decision is a bold sentence that states the outcome, then a few sentences at most. A fixed set of cases follows as a nested list.
- **Outcome, not means.** The outcome is something a person could observe or a test could check. The means is stated only when the user decided the means.
- **Identifiers.** An identifier appears when its name was decided, such as a model, a route or a label, or when it locates existing code that changes.
- **Mechanisms.** A mechanism that several decisions rely on, or that takes more than a short paragraph to state, gets a section of its own after Decisions. It is written there once, and the decisions link to it.
- **The user's.** Everything the user decided is a numbered decision, a spec amendment or a step of the Process, even where another section works it out further.
- **Precision.** A decision is never more exact than what the user decided. A detail that nobody decided is the implementer's, and the plan is silent on it.

## Missing Decisions and Unverified Facts

A decision is missing when a sentence of the plan cannot be written without it and no existing decision settles it.

- **Ask.** Put each missing decision to the user as soon as it surfaces, with a recommended answer. Never settle one by assumption.
- **Undecided.** A decision the user defers is recorded under Undecided, as the question and what it affects. Text that would depend on it is not written. When the user resolves it, the answer becomes a decision and the entry is removed.
- **Facts.** A fact that the repository or a short trial can settle is looked up, never asked and never left open.
- **To Verify While Building.** A fact that only building can settle is recorded there, with what follows from each answer. It belongs there only when every answer changes the means and leaves every decision standing. When an answer would change a decision, that decision is missing.

## Phases

- A phase is a heading and at most seven bullets. Each bullet names something the phase builds, in the words of the decisions, and cites a decision by number where the link is not plain. Work that needs more bullets is two phases.
- A phase leaves the repository passing its checks, so that it can be reviewed on its own.
- A phase has no steps, no list of files, no list of tests and no "done when". What every phase shares is said once, in the sentence that opens the section or in Process.

## Process

Process states what follows each phase. Two steps are in every plan, in this order:

1. **An independent review** of the phase's changes, by a reviewer that starts with none of the author's context. Ask the user which review.
2. **The handoff**, rewritten for the next phase, as the skeleton words it. It lives in the scratch directory, which git ignores, since each phase replaces it in full.

Any further step, such as a stop for the user's approval or a commit, is in a plan only when the user decided it for that plan. It goes at the point in the sequence where the user wants it to happen.

## Editing a Plan

These rules hold from the moment a plan is first written, and they bind an implementer who edits it during a phase.

- **When.** A change to a decision, a mechanism, a placement or the content of a phase is written into the plan in the phase that makes it.
- **Whose.** The numbered decisions, the spec amendments and the Process are the user's. Put a change to one of them to the user before making it, unless the plan's Process says otherwise. Every other section is the implementer's to change, as long as each decision still holds.
- **Current text.** The changed text states the new decision and nothing of the old one, except for a trace.
- **Trace.** One sentence follows the new text in two cases: something the user decided was changed at the prompting of a review or an implementer, or the replaced text is a trap that a later phase could return to. The sentence says what was replaced, who changed it and why.
- **Settled facts.** When an entry under To Verify While Building is settled, it keeps its label and states the fact found and the means that follows from it, in place of the question. An entry that no later phase relies on is removed.
- **No progress.** The plan gains no status, no mark that a phase is done, no date or commit of a phase, and no account of what a phase did.

## Format and Style

- **Prose.** Load the `writing-normative-prose` skill. Every rule in it applies to a plan.
- **Rationale.** Apart from a trace, at most a clause, and only where the implementer would otherwise undo or misapply the decision.
- **No code blocks and no tables.** Wording that was decided, such as a label, a message or a sentence of the product specification, is quoted inline.
- **Emphasis.** Headings are in title case. Bold marks the sentence that states a decision and the label of a list item.
- **Citations.** A section of the product specification is cited by its bare number in parentheses, such as "(4.2)". A decision is cited as "decision 12", an amendment as "amendment 3", and another section of the plan by a link.

## Anti-Patterns

Each pair shows text this skill rejects and the text that replaces it. All are from a fictional plan that lets the owner of a scheduled job pause it.

**A task in place of a decision.**

- Rejected: "4. **Add a `pausedAt` column to `Job` and check it in the worker.**"
- Accepted: "4. **A paused job starts no run.** A run that started before the pause finishes."

**An implementation written in advance.**

- Rejected: "`pauseJob({ jobId, keyId })` in `src/modules/jobs/jobs.server.ts` loads the job, compares its `ownerKeyId` with `keyId`, sets `pausedAt` to the current time and returns the row."
- Accepted, as a decision: "5. **Only the key that owns a job pauses or resumes it.** Any other key is refused as forbidden."
- Accepted, under Placement: "Pausing and resuming go in the jobs module's server file, beside the function that creates a job."

**A phase that holds the content.**

Rejected:

```markdown
### 2. Pausing

- Add `pausedAt` to `Job` in the schema and generate the migration.
- Write `pauseJob` and `resumeJob`. Each refuses a key that does not own the job.
- Specs: a paused job, a job paused twice, a key that is not the owner.
- Done when `pnpm check` passes.
```

Accepted:

```markdown
### 2. Pausing

- Pausing and resuming, with their refusals (decision 5).
- A paused job starts no run (decision 4).
- Resuming starts none of the skipped runs (decision 9).
```

**More exact than what was decided.** The user decided only that the list shows which jobs are paused.

- Rejected: "7. **A paused job shows a grey "Paused" badge to the right of its name**, with the time of the pause in a tooltip."
- Accepted: "7. **The job list shows which jobs are paused.**"

**A missing decision filed as a fact to verify.**

- Rejected, under To Verify While Building: "Whether a job that is resumed starts the runs it skipped."
- Accepted: the question is put to the user, and the answer becomes a decision.
- Stays, because only building can settle it and each answer changes only the means: "**A pause during a run.** Whether the queue library still reports a run as finished when its job is paused midway. If it does, the run is recorded as it is now. If it does not, the worker records it."

**Progress in the plan.**

- Rejected: "### 2. Pausing (Done)", or "Phase 1 is built. Phase 2 has its migration, and the worker is untouched."
- Accepted: the plan says neither. The handoff says the second.

**A trace that guards nothing.** The plan's author moved a bullet from one phase to another. The user decided neither placing, and no later phase would move it back.

- Rejected, in phase 3: "The job list shows which jobs are paused (decision 7). Moved here from phase 2, which had grown too large."
- Accepted: "The job list shows which jobs are paused (decision 7)."
- Stays, in a mechanism section, because the replaced text is a trap: "**A paused job is skipped when its run is due.** The implementer of phase 2 changed this from skipping it when the run is queued, which let a job that was paused after queueing still run."
- Stays, because a review changed what the user decided: "9. **Resuming starts none of the runs that the pause skipped.** The user first chose to start them all, and agreed to skip them when the review of phase 2 found that a job paused for a week would start 168 runs at once."
