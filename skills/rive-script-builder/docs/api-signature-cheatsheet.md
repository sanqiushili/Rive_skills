# API Signature Cheatsheet

This file is the offline quick reference for common Rive scripting signatures and data contracts.

## Runtime Facts

- Rive scripting is sandboxed Luau inside Rive, not Roblox or browser JavaScript.
- No file I/O, network, `os.execute`, `loadstring`, or Roblox globals.
- Attachable protocols return a factory function so each attached instance gets fresh state.
- Keep long loops and heavy synchronous work out of lifecycle callbacks.
- Use `print()` for editor Console debugging.

## Type and Factory Rules

- Prefer `export type ScriptName = { ... }` for attachable scripts.
- Use PascalCase script names and match the main type name when practical.
- Rive objects created in `init`, editor-assigned references, ViewModel inputs, and computed late fields use `late()` in the factory table.
- Primitive inputs use direct defaults, for example `speed = 1`.
- `Input<Trigger>` uses `function() end` as its default.
- Avoid mutable module-level state in attachable scripts.

## Protocol Factories

### Node

```luau
return function(): Node<MyNode>
  return {
    init = init,
    advance = advance,
    update = update,
    draw = draw,
    pointerDown = pointerDown,
    pointerMove = pointerMove,
    pointerUp = pointerUp,
    pointerExit = pointerExit,
  }
end
```

### Layout

```luau
return function(): Layout<MyLayout>
  return {
    init = init,
    measure = measure,
    resize = resize,
    draw = draw,
  }
end
```

### Converter

```luau
return function(): Converter<MyConverter, DataValueNumber, DataValueNumber>
  return {
    init = init,
    convert = convert,
    reverseConvert = reverseConvert,
    advance = advance,
  }
end
```

### Path Effect

```luau
return function(): PathEffect<MyPathEffect>
  return {
    init = init,
    update = update,
    advance = advance,
    context = late(),
  }
end
```

### Transition Condition

```luau
return function(): TransitionCondition<MyTransitionCondition>
  return {
    init = init,
    evaluate = evaluate,
    context = late(),
  }
end
```

### Listener Action

```luau
return function(): ListenerAction<MyListenerAction>
  return {
    init = init,
    perform = perform,
    context = late(),
  }
end
```

### Util

```luau
return {
  helperA = helperA,
  helperB = helperB,
}
```

### Test

```luau
function setup(test: Tester)
  local case = test.case
  local group = test.group
end
```

## Lifecycle Summary

- `init(self, context?) -> boolean`
- `advance(self, seconds) -> boolean` optional
- `update(self, ...)`:
  - Node: input change callback
  - PathEffect: `update(self, inPath) -> PathData`
- `draw(self, renderer)` for drawable protocols
- `evaluate(self) -> boolean` for transition conditions
- `perform(self, pointerEvent)` for listener actions
- `draw` should render from current state and avoid mutation.
- `evaluate` should be fast and side-effect free.

## Context / Data Access

Common context methods:
- `context:markNeedsUpdate()`
- `context:viewModel()`
- `context:rootViewModel()`
- `context:dataContext()`
- `context:image(name)` / `context:blob(name)` / `context:audio(name)`

Important:
- `markNeedsAdvance` is not available in exposed Context type.
- Use `markNeedsUpdate()` for update scheduling.

## ViewModel Accessors

- `getNumber(name)`
- `getString(name)`
- `getBoolean(name)`
- `getColor(name)`
- `getTrigger(name)`
- `getList(name)`
- `getViewModel(name)`
- `getEnum(name)`

## Inputs and Data Binding Rules

- Inputs appear in editor sidebar when defined in type table and return table.
- Inputs can be data bound in editor.
- Scripts do not set normal input values directly.
- Writable runtime data should go through view model properties.
- Primitive `Input<T>` values are read directly (`self.speed`), not with `.value`.
- ViewModel data values expose `.value` for reads and writes.
- Bind strings to the Text Run, not the parent Text object.

Input defaults:

| Field kind | Factory default |
|---|---|
| `Input<number/string/boolean/Color>` | literal value |
| `Input<Trigger>` | `function() end` |
| `Input<Data.X>` | `late()` |
| `Input<Artboard<Data.X>>` | `late()` |
| Rive objects created in `init` | `late()` |
| Plain fields | literal or `late()` |

## Path and Geometry Essentials

Prefer `Vector` in generated code.

Path commands:
- `moveTo`
- `lineTo`
- `quadTo`
- `cubicTo`
- `close`

Path measurement:
- `path:measure().length`
- `measure:positionAndTangent(distance)`
- `measure:extract(dst, startDistance, endDistance, startWithMove?)`

## Pointer Events

- `pointerDown(self, event)`
- `pointerMove(self, event)`
- `pointerUp(self, event)`
- `pointerExit(self, event)`

Event fields:
- `event.position`
- `event.id`

Event handling:
- `event:hit()`

## Color Essentials

- Use `Color.rgb(r, g, b)` or `Color.rgba(r, g, b, a)`.
- Colors are immutable.
- Use static channel helpers such as `Color.red(c)` and `Color.red(c, value)`.
- Do not assume `c.r`, `c.g`, `c.b` fields.

## Drawing Essentials

Path:
- `Path.new()`
- `path:moveTo(Vector.xy(x, y))`
- `path:lineTo(Vector.xy(x, y))`
- `path:quadTo(control, endPoint)`
- `path:cubicTo(outControl, inControl, endPoint)`
- `path:close()` for filled shapes
- `path:reset()` only before drawing or on a later frame after drawing

Paint:
- `Paint.with({ style = "fill", color = Color.rgb(...) })`
- `Paint.with({ style = "stroke", thickness = 4, cap = "round", join = "round", color = Color.rgb(...) })`
- `paint:copy({ ... })` for variants

Renderer:
- `renderer:drawPath(path, paint)`
- Balance `renderer:save()` and `renderer:restore()`.
- Use `renderer:transform(Mat2D.withTranslation(x, y))` for local drawing transforms.
- Keep `draw(self, renderer)` pure.

## Luau Syntax Guardrails

- Not equal is `~=`, not `!=`.
- Boolean operators are `and`, `or`, `not`, not `&&`, `||`, `!`.
- String concatenation is `..`; interpolation uses backticks: `` `Score: {score}` ``.
- Only `false` and `nil` are falsy; `0` and `""` are truthy.
- Use `(value :: DataValueNumber)` for casts.
- Do not use JavaScript `import`/`export default`; Rive Util imports use `require("UtilName")`.

## Common Mistakes to Avoid

| Mistake | Correct pattern |
|---|---|
| `self.size.value` for primitive inputs | `self.size` |
| `late()` for `Input<Trigger>` | `function() end` |
| `c.r`, `c.g`, `c.b` | `Color.red(c)`, `Color.green(c)`, `Color.blue(c)` |
| Mutating state in `draw()` | mutate in `advance()`, `update()`, or event callbacks |
| Using `context` in `update(self)` | `Node.update` has only `self` |
| `PathEffect.update(self, inPath, node)` | `update(self, inPath): PathData` |
| Writing normal `Input<T>` values | write ViewModel properties instead |
| Binding text strings to parent Text object | bind to the Text Run |
| Forgetting factory return type | return `Node<T>`, `Layout<T>`, `Converter<T,In,Out>`, etc. |

## Tester and Expect

- `test.case(name, fn)`
- `test.group(name, fn)`
- `expect(value).is(expected)`
- `expect(value).greaterThan(number)`
- `expect(value).greaterThanOrEqual(number)`
- `expect(value).lessThan(number)`
- `expect(value).lessThanOrEqual(number)`
- `expect(value).never.is(expected)`
