# Common Errors and Fixes

Use this guide before final handoff.

## Error: `Key 'markNeedsAdvance' not found in external type 'Context'`

Cause:
- Current exposed Context type does not include `markNeedsAdvance`.

Fix:
- Use `context:markNeedsUpdate()`.
- Keep animation clocks in `advance`, schedule refresh with `markNeedsUpdate`.

## Error: Script not listed when attaching to artboard

Cause candidates:
- Script has compile/type errors.
- Returned table missing required lifecycle methods.

Fix:
1. Check Problems panel first.
2. Ensure factory return table includes required methods.
3. Reopen attach menu after errors are fixed.

## Error: Input not visible in right sidebar

Cause candidates:
- Field missing from type or return table.
- Wrong selection target in editor.

Fix:
1. Define input in type as `Input<T>`.
2. Set default in return table (or `late()`).
3. Select script instance (or converter object) to view inputs.

## Error: Data binding set but value does not update

Cause candidates:
- Binding target type mismatch.
- Script expects writable behavior from normal inputs.

Fix:
1. Verify source and target data types.
2. For writable runtime data, use view model access via context or ViewModel inputs.

## Error: Transition behavior unstable

Cause candidates:
- `evaluate` includes side effects or heavy logic.

Fix:
1. Keep `evaluate` pure and fast.
2. Move mutation logic to listener action or node script.

## Error: Path effect too slow on complex shapes

Cause candidates:
- Sampling density too high.
- Missing cap on generated points.

Fix:
1. Increase `grainSize`.
2. Lower `maxPoints`.
3. Clamp jitter and roughness ranges.

## Error: Pointer interaction not firing as expected

Cause candidates:
- Handler not registered in return table.
- Event not consumed when needed.
- Nested artboard events not forwarded.

Fix:
1. Ensure `pointerDown/Move/Up/Exit` are in returned table.
2. Call `event:hit()` where capture is required.
3. For nested instances, forward translated pointer events manually.

## Error: Converter reverse path behaves unexpectedly

Cause candidates:
- `reverseConvert` missing for two-way binding.
- Reverse math not consistent with forward conversion.

Fix:
1. Add `reverseConvert` when two-way is required.
2. Document non-bijective behavior explicitly.

## Error: Tests pass individually but fail together

Cause candidates:
- Shared mutable state across cases.

Fix:
1. Reinitialize state per case.
2. Keep util functions pure.
3. Avoid cross-case mutation.
