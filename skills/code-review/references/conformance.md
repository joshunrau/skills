# Conformance

Read the product specification in full, and the plan if your prompt names one. They are the authority, the specification first where they disagree. Report three kinds of finding, each naming its kind in the title:

- **Contradiction**: the code does what a clause forbids, or does differently what a clause fixes.
- **Missing**: a clause governs behaviour the code already carries out, and the code omits what the clause requires. A feature the code never starts is not missing.
- **Unrequested**: something a user can do, or a business rule such as a validation, permission or limit, that no clause asks for. Presentation that no clause covers, such as a loading state, an empty state, a label or the layout, is the implementer's to choose and is not a finding.

When the plan is the only authority, report Unrequested findings in `ref` mode only: a plan covers one piece of work, so it asks for little of the code that stands outside the change.

Worst first, by how much a user would be affected. Quote the clause for every Contradiction and Missing finding.
