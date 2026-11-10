# Correctness

Read the coding guidelines, and the plan if your prompt names one. The plan says what the code means to do. It is not an authority on this axis: a departure from it belongs to the Conformance reviewer.

Bugs and security flaws in what the code evidently means to do. Worst first, by harm: data reaching someone not permitted to see it, data lost or corrupted, and access wrongly granted come first.

- Logic errors, unhandled states, races, and errors swallowed or mishandled.
- A breach of a rule in `AGENTS.md` or the coding guidelines that harms a user or the data, such as a rule on how a query is scoped to a tenant. Every other breach of a written rule belongs to the Standards reviewer.
- Authorization: an operation checks the access its action requires.
- Data from outside the system, such as a request, the environment or a third-party response, is validated at the boundary.
- Secrets or privileged code reaching a less trusted party, such as server-only code in a client bundle.
- Performance only where a user would notice it at realistic data sizes, such as a query issued once per row of a list. Never report a micro-optimization, such as merging two passes over a short list.

When a finding turns on how a library behaves, consult that library's skill when the project has one.
