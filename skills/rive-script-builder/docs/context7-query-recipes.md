# Context7 Query Recipes

Use these recipes when querying Context7 library `/rive-app/rive-docs`.

Recommended flow:
1. Resolve once: `resolve-library-id("rive-docs") -> /rive-app/rive-docs`
2. Query with focused, single-purpose prompts.
3. If result is ambiguous, run a narrower follow-up query.

## Protocol Queries

1. Node lifecycle and callbacks
- `Node script lifecycle methods: init, advance, update, draw, pointerDown/Move/Up/Exit signatures and constraints`

2. Layout lifecycle and measurement
- `Layout script measure and resize behavior, and how it differs from Node scripts`

3. Converter binding direction
- `Converter script convert and reverseConvert usage for one-way and two-way data binding`

4. Path Effect lifecycle
- `Path Effect script update and advance behavior, required return type, and input handling`

5. Transition Condition constraints
- `Transition Condition evaluate lifecycle frequency and side-effect restrictions`

6. Listener Action side effects
- `Listener Action perform usage with pointerEvent and recommended side-effect patterns`

7. Util and Test relation
- `How Util scripts are structured and how Test scripts validate Util logic`

## Data and Input Queries

8. Script input definitions
- `How to define script inputs with defaults and late() assignments`

9. Data-bound input constraints
- `Script inputs data binding behavior and why scripts cannot set normal input values`

10. ViewModel via context
- `Accessing viewModel and rootViewModel from Context with getNumber/getTrigger/getViewModel examples`

11. Property listeners and cleanup
- `addListener/removeListener best practices for ViewModel properties and triggers`

12. ViewModel typed inputs
- `Input<Data.X> usage patterns for read/write access to nested view model properties`

## Pointer and Interaction Queries

13. PointerEvent API
- `PointerEvent fields position and id, and event hit handling including translucent mode`

14. Multi-touch state management
- `Recommended multi-touch tracking pattern using pointer id in Node scripts`

15. Nested pointer forwarding
- `How to forward pointer events from main artboard to instantiated child artboards`

## Path and Rendering Queries

16. PathData iteration and measure
- `PathData command iteration, contours(), and measure() usage`

17. PathMeasure operations
- `PathMeasure positionAndTangent, extract, and warp behavior`

18. Path mutation safety
- `Path draw and mutation timing constraints, including reset-after-draw rules`

## Debugging and Testing Queries

19. Debug panel workflow
- `Rive scripting debug workflow using Problems and Console panels`

20. Test script matchers
- `Test script setup(test: Tester), case/group usage, expect matchers and never inversion`

## Follow-up Narrowing Templates

- `In /scripting/protocols/path-effect-scripts, show exact update method expectations and return value semantics`
- `In /scripting/api-reference/interfaces/context, list currently exposed methods and scheduling APIs`
- `In /scripting/script-inputs, clarify differences between normal inputs and ViewModel inputs`

## Output Discipline

When using these recipes in the skill:
- keep source attribution explicit (`Context7 /rive-app/rive-docs`)
- if uncertain, ask clarification before coding
- if Context7 is unavailable, fall back to `sync_rive_docs.py` and note fallback reason
