# Conformance

Read the product specification in full, and the plan if your prompt names one. They are the authority, the specification first where they disagree. Report three kinds of finding, each naming its kind in the title:

- **Contradiction**: the code does what a clause forbids, or does differently what a clause fixes.
- **Missing**: a clause governs behavior the code already carries out, and the code omits what the clause requires. A feature the code never starts is not missing.
- **Unrequested**: something a user can do, or a business rule such as a validation, permission or limit, that no clause asks for. Apart from a deferred decision, described below, no other choice that the clauses leave open is a finding, such as the means of reaching a result that a clause states, or presentation: a loading state, an empty state, a label or the layout.

When the plan is the only authority, report Unrequested findings in `ref` mode only: a plan covers one piece of work, so it asks for little of the code that stands outside the change.

Worst first, by how much a user would be affected, then by how costly the breach is to reverse. Quote the clause for every Contradiction and Missing finding.

The rules below hold only for a specification in the form that the `writing-software-specs` skill gives one: an Overview, numbered axioms, then numbered sections. Four rules govern how it is read:

- **Axioms**: each axiom holds for every instance of what it names, without exception, and no later section repeats it. Check every instance in the listed files against each axiom.
- **Completeness**: a clause is complete as written, and the specification never adds "and nothing else". Where a clause says who may act, which values are accepted or which states exist, code that admits one more is a Contradiction, not Unrequested.
- **Consequences**: what follows from two or more clauses binds the code as each of them does, though no sentence states it. A purpose you suppose a clause to have binds nothing.
- **Literal text**: text in a code span is literal. The code, or the message, file or command line that the text belongs to, carries it exactly as written. A value in italics has no literal form, and the code names it as it likes.

Some parts of the specification bind in their own way:

- **Out of Scope**: code that serves a listed item is a Contradiction.
- **Structural Technical Decisions**: each fixes a means, so code that reaches the same result another way is a Contradiction.
- **Deferred**: each entry names a capability left out for now and what keeps it possible. Code that provides the capability, or that removes what keeps it possible, is a Contradiction.
- **Blocking Decisions and Open Decisions**: each entry is a question the user has deferred, with the sections it affects. Code that settles the question where no clause does is Unrequested, whatever kind of behavior settles it: quote the entry, and make Recommended Fix the question to put to the user. A clause in a section that a Blocking Decisions entry names holds until the user answers, so a finding that rests on one stands, and quotes the entry after the clause.
