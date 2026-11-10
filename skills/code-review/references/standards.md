# Standards

Read the coding guidelines and the lint rules.

The authorities are `AGENTS.md`, the coding guidelines, and each of the project's own skills whose rules govern a kind of file in your list, such as a skill on hand-written SQL for a migration. A project's own skill is one committed in the repository that `skills-lock.json`, the lockfile of the `skills` CLI, does not list; a listed skill is third-party advice, not a standard. In a project with no lockfile, every committed skill is its own. Skip anything the lint rules report.

Standards owns the rules a reader can answer yes or no: where a file goes, what a module may import, how a thing is named, and which constructs are allowed on what terms. It also owns consistency, which no source writes down: new code takes the naming, parameters and shape of existing code with the same role.

Two kinds of rule belong to other reviewers:

- **Correctness**: a rule whose breach harms a user or the data.
- **Complexity**: a rule judged by cost, such as one against near-duplicates or steps that change nothing, and code contorted to satisfy a rule.

Worst first, by how much a breach misleads a reader or erodes the structure. Quote the rule for every finding except one of consistency, which locates the existing code instead.
