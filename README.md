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
```

### Skills That Need Another Skill

`writing-software-specs` and `writing-implementation-plans` each load `writing-normative-prose`.
