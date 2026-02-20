# Quality Gates

Use these gates before shipping any script response.

## Gate 1: Clarification Complete

Before coding, verify:
- protocol choice is explicit
- unresolved decisions are asked as targeted questions
- assumptions are listed
- user gave explicit approval to start coding

If approval is missing, do not output final script code.

## Gate 2: API Contract Safety

Before implementation, verify:
- factory return type matches chosen protocol
- required lifecycle methods exist and signatures match docs
- no unverified API names are used
- data access pattern is valid (inputs vs ViewModel)

## Gate 3: Runtime Behavior Safety

Before final code:
- deterministic behavior in critical callbacks (`update`, `evaluate`)
- side effects isolated to allowed locations (`perform`, controlled callbacks)
- listeners have cleanup strategy
- pointer event routing/consumption strategy is explicit

## Gate 4: Integration Completeness

Final answer must include:
- full Luau code
- editor wiring steps
- debug checklist
- test suggestions (or Test script when Util logic exists)

## Gate 5: Source Transparency

When consulting docs:
- prefer `search/show --source auto`
- keep source mode visible (`online`, `cache`, or `offline`)
- if fallback occurred, include fallback reason

If online docs and offline docs diverge, prefer online and state that explicitly.

## Gate 6: Regression Checklist

Before handoff, quickly check:
- input defaults and `late()` usage are coherent
- protocol lifecycle function table is complete
- path/pointer edge cases are handled
- code style is minimal and maintainable

