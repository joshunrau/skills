# Plan Skeleton

Each heading below is followed by what belongs there. Decisions, Phases and Process are in every plan. Any other section is omitted when it would be empty. The sections keep this order.

The plan's title is `# {Topic}`. One paragraph follows it: what the work delivers, and when and how the decisions were made, with the document they started from when there was one. When the work serves sections of the product specification, the paragraph cites them and says which of the plan and the specification holds where the two disagree.

## Decisions

### Scope and Delivery

What is in scope, as one decision with a list. What is out of scope, as one decision with a list, each item with what the work leaves ready for it. Each rule of the repository that the user waived for this work, with the limits of the waiver. Any other decision about the work as a whole, such as whether existing data has to survive it.

### {Area}

One heading for each area of the work, ordered so that an area depends only on the areas before it. The numbering continues from the group before.

## Spec Amendments

The new wording of each sentence that the work changes in the product specification or adds to it, and each sentence that it removes, each with its section. They are numbered as decisions are: a number never changes, and a later amendment takes the next. The section opens by naming the phase that applies them, with the `writing-software-specs` skill loaded.

## Data Model

One entry for each model that the work adds or changes: what a new model holds, and what changes in an existing one. In words, never as a schema.

## {Mechanism}

One section for each mechanism that the decisions link to, named for what it describes. A list of rules, each opening with a bold label or a bold sentence.

## Placement

Where the new code goes, by folder or module and by kind of file, and each import between modules that the work adds. The section opens by saying that these are intentions: each phase settles them when it starts, and stops to propose a change where the structure does not fit. When `AGENTS.md` states rules for the repository's structure, or names a file that does, the opening names that place as what each phase settles the intentions against.

## Phases

One sentence that says what every phase ends on, with a link to Process. Then one heading for each phase:

### 1. {Title}

At most seven bullets.

## Process

What follows each phase, as a numbered list. Every plan has these two steps, worded for the plan:

1. **{The review the user chose}**, by a reviewer that starts with none of the author's context.
2. **The handoff is rewritten** at `{scratch directory}/{topic}_handoff.md`. It serves the next phase only and replaces the one before it in full:
   - what now exists that the next phase builds on, by file and name;
   - what the phase changed in this plan, by section or decision number;
   - what the next phase does first, and anything left unfinished.

   A change to a decision, a mechanism, a placement or a phase is written into this plan, with the `writing-implementation-plans` skill loaded. The handoff only says where.

A step that the user decided for this plan is added at the point in the sequence where it happens. The section ends by saying that each phase starts by reading the plan and the handoff.

## To Verify While Building

One entry for each fact that only building can settle: a bold label, the question, and what follows from each answer.

## Tests

Which kinds of new code get which kinds of test, and any limit on how the tests are written. Never a list of cases.

## Undecided

One entry for each decision the user deferred: the question, and what it affects.
