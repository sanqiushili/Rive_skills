# Debug and Test Playbook

Use this workflow to validate script correctness quickly and consistently.

## 1) Static Validation First

Open Debug Panel -> Problems.

Check:
- Syntax errors
- Type mismatches
- Missing or invalid bindings

Rule:
- Fix Problems items before runtime debugging.

## 2) Runtime Inspection

Open Debug Panel -> Console.

Use targeted `print()` logs for:
- Lifecycle entry (`init`, `advance`, `draw`, `convert`, `perform`, `evaluate`)
- Input values
- View model reads and writes
- Pointer event IDs and positions

Avoid noisy logs in final script handoff.

## 3) Protocol-Specific Runtime Checks

### Node and Layout

- Confirm draw path executes.
- Confirm pointer handlers call `event:hit()` when expected.
- Confirm `resize` responds to layout size changes.
- For frame-sensitive motion, validate fixed-step behavior if used.

### Converter

- Validate input type branch behavior.
- Validate fallback behavior for mismatched types.
- If two-way binding enabled, validate `reverseConvert` symmetry expectations.

### Path Effect

- Validate `update` output path correctness.
- Validate `advance` behavior for time-based transforms.

### Transition Condition

- Ensure evaluate result matches rule.
- Ensure no side effects inside evaluate path.

### Listener Action

- Validate action fires only on expected listener event.
- Validate side effects update intended data only.

### Util

- Keep functions pure where possible.
- Move protocol-dependent logic out of util layer.

### Test

- Prefer focused `case` blocks with descriptive names.
- Group related cases with `group`.
- Cover edge values and type boundaries.

## 4) Unit Testing Pattern (Util-Focused)

1. Require util script.
2. Write grouped test cases.
3. Assert normal and edge inputs.
4. Run tests from Assets panel.
5. Resolve all failing expectations before release.

## 5) Final Acceptance Checklist

A script handoff is ready when:

1. Protocol selection is justified.
2. Required lifecycle methods are present.
3. Wiring steps are explicit and executable.
4. Problems panel is clean.
5. Runtime behavior matches expected scenario.
6. For util logic, test coverage includes critical branches.

## Scenario Checks for This Skill

1. Ambiguous request should trigger clarification first.
2. Without explicit approval, provide plan only.
3. With explicit approval, provide code plus wiring and tests.
4. Protocol routing should match Node/Layout/Converter/Path Effect/Transition/Listener/Util/Test requirements.
5. Response language should follow user input language.
