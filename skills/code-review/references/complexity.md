# Complexity

Read the coding guidelines and the lint rules.

Judge the code on its own terms: is it more complicated than its evident purpose justifies? Do not open the product specification until every finding is written; reading it earlier makes complexity look justified.

Report a cost, not a taste: lines, levels of indirection, or concepts a reader must hold. The checks:

- **Purpose not evident**: the reason for the code cannot be read from its names and body. When the purpose looks like a product requirement rather than a need of the code, mark the cause Specification, provisionally.
- **Workaround for a safe assertion**: a rewrite larger than the `as` or `!` it avoids, when the fact holds for every input the function admits.
- **Defensive check inside trusted code**: re-validation of data the system wrote or already validated at the boundary.
- **Helper with one caller** whose body reads as well in place.
- **Abstraction with one user**: a generic, parameter, option or interface with exactly one concrete use.
- **Pure indirection**: a function whose body is a call to another with the same arguments, or a type that only renames another.
- **Near-duplicates** where one general function would do.
- **A step that does not change the result.**
- **Code made barbarous by a rule**: a shape that exists to satisfy a guideline or a lint rule rather than the problem.
- **Unclear organization**: a split or file boundary that makes the module harder to navigate.

Once every finding is written, assign each a cause, which becomes its group in the report:

- **Lint Rule**: the shape exists to satisfy a lint rule. The likeliest cause to be wrong and the cheapest to change. Quote the rule from the lint rules. When the project has none, the cause is a lint rule only where the code shows it, such as a disable comment or a shape that a widely used rule demands: name the rule by its id.
- **Guideline**: the shape exists to satisfy `AGENTS.md` or the coding guidelines. A considered principle, so this cause is rare. Quote the line and say why the principle fails here, rather than that it was inconvenient.
- **Specification**: a clause of the product specification requires the code. Now open the specification and check every finding against it, not only the provisional ones: a clause under Structural Technical Decisions or Deferred can require structure whose purpose the code does not show. A clause requires the code only when no simpler code would satisfy it. Quote the clause. A provisional finding that no clause requires moves to Code, saying that nothing requires it, as does every provisional finding when the project has no product specification.
- **Code**: everything else; fix the code.

In the Lint Rule, Guideline and Specification groups, Recommended Fix is the proposed amendment. For Specification, add what the amendment gives up: what users would lose, or what else rests on a clause under Structural Technical Decisions or Deferred. When the clause fixes a means, sits outside Structural Technical Decisions and keeps no Deferred capability possible, the amendment is to state the behavior alone and leave the means to the implementer. Return the findings grouped by cause, worst first within each group, by cost.
