# Case Recipes

Use these recipes as starting points for common user requests.

## 1) Crayon / Rough Edge Path Effect

Intent:
- Add rough hand-drawn edge texture to path outlines.

Protocol:
- `Path Effect`

Core strategy:
1. Measure path length.
2. Sample positions with `positionAndTangent`.
3. Build normal vectors and apply bounded noise offsets.
4. Return rebuilt path with optional animation via `advance`.

Recommended inputs:
- `roughness: Input<number>`
- `grainSize: Input<number>`
- `jitter: Input<number>`
- `seed: Input<number>`
- `animated: Input<boolean>`
- `speed: Input<number>`
- `animationFps: Input<number>`
- `maxPoints: Input<number>`

Performance notes:
- Clamp sampling density.
- Use `maxPoints` guard.

## 2) Fixed-Step Motion Node

Intent:
- Consistent motion across variable frame rates.

Protocol:
- `Node`

Core strategy:
1. Store `accumulator`.
2. Use `fixedStep` input.
3. Run bounded while-loop updates (`MAX_STEPS`).

Recommended inputs:
- `speed`
- `fixedStep`

## 3) Data Converter with Safe Fallback

Intent:
- Convert and optionally reverse-convert values robustly.

Protocol:
- `Converter`

Core strategy:
1. Check input DataValue type.
2. Convert with deterministic fallback.
3. If two-way binding required, implement reverse path with symmetry rules.

Recommended inputs:
- conversion-specific constants (for example offset/scale)

## 4) Transition Gate by ViewModel State

Intent:
- Control state-machine transition by combined conditions.

Protocol:
- `Transition Condition`

Core strategy:
1. Cache view model refs in `init`.
2. Keep `evaluate` pure and cheap.
3. Return boolean only, no side effects.

## 5) Listener Side-Effect Action

Intent:
- Trigger side effects when listener fires.

Protocol:
- `Listener Action`

Core strategy:
1. Resolve target properties in `init`.
2. Execute updates in `perform`.
3. Keep side effects explicit and local.

## 6) Util + Test Pair

Intent:
- Extract reusable pure logic and validate with unit tests.

Protocol:
- `Util` plus `Test`

Core strategy:
1. Put business logic in Util.
2. Write grouped test cases.
3. Cover normal + boundary inputs.

## Delivery Checklist per Recipe

Before coding:
- Confirm protocol choice.
- Confirm input surface.
- Confirm acceptance behavior.

After coding:
- Give editor wiring steps.
- Give debugging checkpoints.
- Give parameter presets for quick validation.
