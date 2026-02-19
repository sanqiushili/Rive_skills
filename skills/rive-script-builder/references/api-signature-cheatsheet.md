# API Signature Cheatsheet

This file is the offline quick reference for common Rive scripting signatures and data contracts.

## Protocol Factories

### Node

```lua
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

```lua
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

```lua
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

```lua
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

```lua
return function(): TransitionCondition<MyTransitionCondition>
  return {
    init = init,
    evaluate = evaluate,
    context = late(),
  }
end
```

### Listener Action

```lua
return function(): ListenerAction<MyListenerAction>
  return {
    init = init,
    perform = perform,
    context = late(),
  }
end
```

### Util

```lua
return {
  helperA = helperA,
  helperB = helperB,
}
```

### Test

```lua
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

## Path and Geometry Essentials

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

## Tester and Expect

- `test.case(name, fn)`
- `test.group(name, fn)`
- `expect(value).is(expected)`
- `expect(value).greaterThan(number)`
- `expect(value).greaterThanOrEqual(number)`
- `expect(value).lessThan(number)`
- `expect(value).lessThanOrEqual(number)`
- `expect(value).never.is(expected)`
