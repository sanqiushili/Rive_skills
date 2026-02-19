# Rive Skills Monorepo

This repository is structured for publishing multiple Rive-related skills.

## Layout

```text
skills/               # publishable skill packages
templates/skill/      # starter template for new skills
tooling/              # local release and validation scripts
catalog/skills.json   # lightweight index of published skills
docs/                 # release playbooks
.github/workflows/    # CI validation and release packaging
```

## Quick Commands

```bash
# create a new skill skeleton
bash tooling/new-skill.sh rive-example-skill

# validate all skills
bash tooling/validate-skill.sh

# pack all skills to ./dist
bash tooling/pack-all.sh
```

## Conventions

- One skill per folder under `skills/<skill-name>/`.
- Required files per skill: `SKILL.md`, `agents/openai.yaml`, `package.json`.
- Keep references, scripts, and assets inside each skill folder.
- Do not keep nested git repositories inside `skills/`.

