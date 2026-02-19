# Protocol Router

Use this document to choose the correct Rive scripting protocol and enforce lifecycle constraints.

## Decision Tree

1. Need custom drawing, per-frame simulation, pointer handling, or runtime artboard instances?
- Choose `Node`.

2. Need layout measurement or resize-driven child positioning?
- Choose `Layout`.

3. Need data transformation between view model values and bound properties?
- Choose `Converter`.

4. Need procedural path geometry modification on strokes?
- Choose `Path Effect`.

5. Need custom boolean transition logic in state machine transitions?
- Choose `Transition Condition`.

6. Need side effects when a state machine listener fires?
- Choose `Listener Action`.

7. Need reusable shared helpers only?
- Choose `Util`.

8. Need unit tests for pure script logic (usually Util functions)?
- Choose `Test`.

## Multi-Protocol Combinations

- `Node + Util`: rendering or interaction plus extracted helper logic.
- `Converter + Util`: transformation plus shared math/string helpers.
- `Util + Test`: production logic plus deterministic unit tests.
- `Transition Condition + Util`: pure condition logic plus reusable predicates.
- `Listener Action + Util`: event side effects plus helper abstraction.

Prefer smallest viable combination.

## Lifecycle and Method Contracts

### Node

Common lifecycle:
- `init(self, context)`
- `advance(self, seconds)` optional
- `update(self)` optional
- `draw(self, renderer)`
- `pointerDown/pointerMove/pointerUp/pointerExit` optional

Notes:
- For scene attach troubleshooting, include at least `init` and `draw` in returned table.
- Use `event:hit()` for pointer capture behavior.

### Layout

Includes Node behavior plus layout-specific methods:
- `resize(self, size)` required
- `measure(self)` optional

Notes:
- `measure` affects layouts primarily when fit is Hug.

### Converter

Core methods:
- `convert(self, input)` required
- `reverseConvert(self, input)` optional (needed for 2-way binding)
- `init(self)` optional
- `advance(self, seconds)` optional

Notes:
- Input and output types must be DataValue types.

### Path Effect

Core methods:
- `update(self, inPath)` required
- `init(self, context)` optional
- `advance(self, seconds)` optional

Notes:
- `update` receives original `PathData` and must return path used for rendering.

### Transition Condition

Core methods:
- `evaluate(self)` required
- `init(self, context)` optional

Notes:
- `evaluate` runs every frame while transition is active.
- Keep fast and side-effect free.

### Listener Action

Core methods:
- `perform(self, pointerEvent)` required
- `init(self, context)` optional

Notes:
- Put side effects in `perform`.

### Util

Pattern:
- Return a table of helper functions.
- Export custom types when needed.

### Test

Pattern:
- Implement `setup(test: Tester)`.
- Use `test.case`, `test.group`, and `expect` matchers.

## Data and Input Constraints

- Inputs control scripts, but scripts do not set normal input values.
- To read or write runtime data, use view model access through context or view-model-typed inputs.

## Language and Safety Constraints

- Follow user language in all responses.
- If API details are uncertain, state assumptions and ask before coding.
- Do not invent methods that are not in docs.
