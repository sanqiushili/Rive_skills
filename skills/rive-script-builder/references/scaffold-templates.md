# Scaffold Templates

Use these minimal templates as the first draft. Extend only after approval when a pending plan is required.

## Node

```luau
export type MyNode = {}

local function init(self: MyNode, context: Context): boolean
  return true
end

local function advance(self: MyNode, seconds: number): boolean
  return true
end

local function draw(self: MyNode, renderer: Renderer)
end

return function(): Node<MyNode>
  return {
    init = init,
    advance = advance,
    draw = draw,
  }
end
```

## Layout

```luau
export type MyLayout = {}

local function init(self: MyLayout, context: Context): boolean
  return true
end

local function measure(self: MyLayout): Vector
  return Vector.xy(100, 100)
end

local function resize(self: MyLayout, size: Vector)
end

local function draw(self: MyLayout, renderer: Renderer)
end

return function(): Layout<MyLayout>
  return {
    init = init,
    measure = measure,
    resize = resize,
    draw = draw,
  }
end
```

## Converter

```luau
export type MyConverter = {}

local function init(self: MyConverter): boolean
  return true
end

local function convert(self: MyConverter, input: DataInputs): DataOutput
  local out: DataValueNumber = DataValue.number()
  if input:isNumber() then
    out.value = (input :: DataValueNumber).value
  else
    out.value = 0
  end
  return out
end

local function reverseConvert(self: MyConverter, input: DataOutput): DataInputs
  local out: DataValueNumber = DataValue.number()
  if input:isNumber() then
    out.value = (input :: DataValueNumber).value
  else
    out.value = 0
  end
  return out
end

return function(): Converter<MyConverter, DataValueNumber, DataValueNumber>
  return {
    init = init,
    convert = convert,
    reverseConvert = reverseConvert,
  }
end
```

## Path Effect

```luau
export type MyPathEffect = {
  context: Context,
}

local function init(self: MyPathEffect, context: Context): boolean
  self.context = context
  return true
end

local function update(self: MyPathEffect, inPath: PathData): PathData
  local out = Path.new()
  return out
end

local function advance(self: MyPathEffect, seconds: number): boolean
  return true
end

return function(): PathEffect<MyPathEffect>
  return {
    init = init,
    update = update,
    advance = advance,
    context = late(),
  }
end
```

## Transition Condition

```luau
export type MyTransitionCondition = {
  context: Context,
}

local function init(self: MyTransitionCondition, context: Context): boolean
  self.context = context
  return true
end

local function evaluate(self: MyTransitionCondition): boolean
  return false
end

return function(): TransitionCondition<MyTransitionCondition>
  return {
    init = init,
    evaluate = evaluate,
    context = late(),
  }
end
```

## Listener Action

```luau
export type MyListenerAction = {
  context: Context,
}

local function init(self: MyListenerAction, context: Context): boolean
  self.context = context
  return true
end

local function perform(self: MyListenerAction, pointerEvent: PointerEvent)
end

return function(): ListenerAction<MyListenerAction>
  return {
    init = init,
    perform = perform,
    context = late(),
  }
end
```

## Util

```luau
export type MathPair = {
  sum: number,
  diff: number,
}

local function combine(a: number, b: number): MathPair
  return {
    sum = a + b,
    diff = a - b,
  }
end

return {
  combine = combine,
}
```

## Test

```luau
local MyUtil = require('MyUtil')

function setup(test: Tester)
  local case = test.case
  local group = test.group

  group('MyUtil', function()
    case('combine', function(expect)
      local value = MyUtil.combine(4, 2)
      expect(value.sum).is(6)
      expect(value.diff).is(2)
    end)
  end)
end

return function(): Tests
  return setup
end
```
