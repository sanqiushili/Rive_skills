#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "error: $*" >&2
  exit 1
}

require_file() {
  local path="$1"
  [[ -f "$path" ]] || fail "missing required file: $path"
}

skill_dir="skills/rive-script-builder"
skill_file="$skill_dir/SKILL.md"

require_file "README.md"
require_file "README.zh-CN.md"
require_file "LICENSE"
require_file "$skill_file"
require_file "$skill_dir/agents/openai.yaml"
require_file "$skill_dir/scripts/sync_rive_docs.py"

grep -q '^name: rive-script-builder$' "$skill_file" \
  || fail "SKILL.md must declare name: rive-script-builder"

grep -q '^description: ' "$skill_file" \
  || fail "SKILL.md must include a description"

grep -q 'version: "2.0.0"' "$skill_file" \
  || fail "SKILL.md metadata must include version 2.0.0"

grep -q 'npx skills add https://github.com/sanqiushili/Rive_skills --skill rive-script-builder' README.md \
  || fail "README.md must include the skills.sh install command"

grep -q 'npx skills add https://github.com/sanqiushili/Rive_skills --skill rive-script-builder' README.zh-CN.md \
  || fail "README.zh-CN.md must include the skills.sh install command"

grep -q 'CC BY 4.0' LICENSE \
  || fail "LICENSE must declare CC BY 4.0"

if git grep -n '/Users/' -- ':(exclude)tooling/validate-skill.sh' ':(exclude)skills/rive-script-builder/docs/source-scripting/**'; then
  fail "repository contains local absolute paths"
fi

if git ls-files | grep -q '\.DS_Store$'; then
  fail ".DS_Store files must not be tracked"
fi

echo "Skill repository validation passed."
