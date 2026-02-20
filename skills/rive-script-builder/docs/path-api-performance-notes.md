# Path API and Performance Notes

Use this file when writing Path Effect scripts or other path-heavy logic.

## Path Effect Lifecycle

Core contract:
- `update(self, inPath)` is required and must return a path.
- `init(self, context)` is optional.
- `advance(self, seconds)` is optional for time-based animation.

Use `update` for deterministic geometry transformation.
Use `advance` only when animation depends on elapsed time.

## PathData and Path Operations

Useful operations:
- iterate commands via `ipairs(pathData)`
- command count with `#pathData`
- `pathData:contours()` for contour traversal
- `pathData:measure()` for full-path measurements

Path building:
- `Path.new()`
- `moveTo`, `lineTo`, `quadTo`, `cubicTo`, `close`
- `add(otherPath, transform?)`

Measurement:
- `measure.length`
- `measure:positionAndTangent(distance)`
- `measure:extract(dst, startDistance, endDistance, startWithMove?)`
- `measure:warp(point)`

## Performance Guardrails

1. Keep `update` deterministic and as lightweight as possible.
2. Avoid unnecessary per-frame allocations when parameters did not change.
3. Precompute reusable data in `init` or on input change paths.
4. Use fixed-step throttling when visual style does not require full-frame updates.

## Draw-Mutation Safety

Per Path API docs:
- Do not mutate or `reset` a `Path` in the same frame after drawing it.
- If a path was drawn, mutate/reset it in a later frame.

## Compatibility Note: markNeedsAdvance

Current docs can be inconsistent:
- PathEffect interface text may mention `markNeedsAdvance()`.
- `Context` API reference currently exposes `markNeedsUpdate()` but not `markNeedsAdvance()`.

Practical rule for this skill:
- Do not call APIs that are not present in current `Context` reference.
- Prefer designs that work with `advance` + input/state changes.
- If continuous refresh is needed from callbacks, use `context:markNeedsUpdate()`.

## FPS/Rate Control Pattern

For stylized effects (e.g. boil/crayon jitter), expose rate controls:
- `fps` (or `updateRate`)
- `speed`
- `amplitude`

Then gate visual state updates on accumulated time so motion speed is user-visible.

## Debug Checklist

- Verify `update` always returns a valid path.
- Confirm contour/measure math handles empty paths.
- Check boundary clamping for distance-based sampling.
- Validate visible speed changes when `fps`/`speed` changes.

