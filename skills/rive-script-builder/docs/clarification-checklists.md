# Clarification Checklists

Ask only unresolved questions that materially affect implementation. Skip what is already explicit.

## Global Checklist

1. Target behavior
- What should happen visually or logically?
- What should not happen?

2. Protocol and scope
- Single protocol or combined protocols?
- New script or modify existing script?

3. Inputs and data
- Which values are configurable inputs?
- Which values come from view model or data binding?

4. Runtime constraints
- Frame-rate sensitivity?
- Need fixed-step simulation?
- Expected performance limits?

5. Integration location
- Where will script be attached (artboard, layout, converter, transition, listener, stroke effect)?

6. Acceptance criteria
- What observable behavior proves success?

## Node Checklist

- Need draw only, interaction, or both?
- Need pointer events and multi-touch tracking?
- Need artboard instancing at runtime?
- Need fixed-step advance?
- Which inputs are editable in sidebar?

## Layout Checklist

- Is custom size proposal needed (`measure`)?
- What should happen in `resize`?
- Parent layout constraints and expected fit behavior?

## Converter Checklist

- Source DataValue type and target DataValue type?
- One-way or two-way data binding?
- Null or type-mismatch fallback behavior?

## Path Effect Checklist

- Geometry transform goal (warp, boil, text path, etc.)?
- Static or time-based effect?
- Any path quality/performance constraints?

## Transition Condition Checklist

- Exact allow/deny rule?
- Which view model properties are involved?
- Any debounce/hysteresis behavior needed?
- Confirm no side effects in evaluate path.

## Listener Action Checklist

- Trigger source listener?
- Required side effects (set view model, fire trigger, update context)?
- Pointer-event usage required?

## Util Checklist

- What functions should be pure and reusable?
- Which custom types should be exported?
- Any shared constants to centralize?

## Test Checklist

- Which Util functions are high risk?
- Expected edge cases and boundaries?
- Case and group naming for diagnostics?

## Approval Gate Wording

Use explicit gate before coding:

- "This is the pending implementation plan. Reply with explicit approval (for example: 同意/开始写/approved/go ahead) and I will generate the script."
