# skills

My personal collection of [agent skills](https://skills.sh), installable with the skills CLI.

## Installation

Install all skills from this repo:

```sh
npx skills add joshunrau/skills
```

Or install a single skill:

```sh
npx skills add joshunrau/skills --skill interview
```

## Requirements

### Reference Files

A skill never names a path in your project. It names a file or directory by its role, and your `AGENTS.md` gives the path of each role under a `## Reference Files` heading, one entry per role, with the role first:

```md
## Reference Files

- Coding guidelines: `docs/CODING_GUIDELINES.md`
- Product specification: `SPEC.md`
- Plans directory: `docs/plans/`
- Scratch directory: `scratch/`
- Lint rules: `docs/LINT_RULES.md`
```

The lint rules are a file that describes what the project's linter enforces, such as a document generated from its rules.

### Generated Files

`code-inspection` leaves out each file that `.gitattributes` marks `linguist-generated`:

```
src/route-tree.gen.ts linguist-generated
```

### Skills That Need Another Skill

`writing-software-specs` and `writing-implementation-plans` each load `writing-normative-prose`.
