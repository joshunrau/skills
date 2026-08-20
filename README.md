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

## Skills

| Skill | Description |
| --- | --- |
| [interview](skills/interview/SKILL.md) | A relentless interview to sharpen a plan or design. |

## Adding a New Skill

1. Create a directory under `skills/` named after the skill (lowercase, hyphens allowed).
2. Add a `SKILL.md` file with `name` and `description` frontmatter:

   ```markdown
   ---
   name: my-skill
   description: Brief explanation of what the skill does and when to use it.
   ---

   # My Skill

   Instructions for the agent to follow when this skill is activated.
   ```

3. Add the skill to the table above.
