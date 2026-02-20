# Script Inputs Deep Dive

Use this file when script behavior is configured from the editor sidebar.

## Input Design Model

Define inputs in two places:
1. Type declaration (`Input<T>` fields).
2. Return table defaults.

If value must be assigned at runtime in editor, use `late()`.

```lua
type MyNode = {
  speed: Input<number>,
  noise: Input<number>,
  character: Input<Data.Character>,
}

return function(): Node<MyNode>
  return {
    init = init,
    update = update,
    speed = 1.0,
    noise = 0.2,
    character = late(),
  }
end
```

## Where Inputs Appear

From official docs:
- Node/Layout script inputs appear when selecting that script node.
- Converter script inputs appear in the Data Panel when selecting converter.

## Change Propagation

`update(self, ...)` is called when inputs change.

Use this for:
- recomputing cached values
- validating input ranges
- rebuilding precomputed geometry

Avoid heavy work in `update` if changes can happen frequently.

## Data Binding Constraints

Inputs can be data bound in the editor.

Hard constraint:
- Scripts cannot set normal input values.

When runtime writes are needed, write to ViewModel properties instead.

## ViewModel-Typed Inputs

Use ViewModel input when script must both read and write bound data:
- `Input<Data.YourViewModel>`

Then access nested properties directly:

```lua
if self.character then
  self.character.x.value = 10
end
```

## Artboard Inputs

Scripts can also accept artboard inputs:
- `Input<Artboard<Data.YourViewModel>>`

Use this when script logic needs an instantiated artboard and data coupling.

## Common Mistakes

1. Declared in type but missing in return table (input not exposed correctly).
2. Needed runtime assignment but forgot `late()`.
3. Trying to write to normal input values at runtime.
4. Missing `update` handling after adding dynamic inputs.

## Clarification Questions

Ask before coding:
- Which values should be designer-tunable vs data-bound?
- Which inputs need defaults, and which must be assigned via `late()`?
- Do we need one-way read binding or two-way ViewModel writes?
- What is acceptable update frequency for input-driven recomputation?

