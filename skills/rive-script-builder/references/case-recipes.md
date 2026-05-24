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

## Known-Good Compact Examples

Use these as shape references when a user request is close. Rename the script/type to match the user's feature.

### Input-Driven Progress Bar

Protocol:
- `Node`

Pattern:
- Build paths in `update`, not `draw`.
- Read primitive inputs directly.
- Use `late()` for `Path` and `Paint`.

```luau
export type ProgressBar = {
  width: Input<number>,
  height: Input<number>,
  current: Input<number>,
  maximum: Input<number>,
  bgPath: Path,
  fillPath: Path,
  bgPaint: Paint,
  fillPaint: Paint,
}

local function rebuild(self: ProgressBar)
  local maxValue = math.max(0.0001, self.maximum)
  local t = math.max(0, math.min(1, self.current / maxValue))
  local fillWidth = self.width * t

  self.bgPath:reset()
  self.bgPath:moveTo(Vector.xy(0, 0))
  self.bgPath:lineTo(Vector.xy(self.width, 0))
  self.bgPath:lineTo(Vector.xy(self.width, self.height))
  self.bgPath:lineTo(Vector.xy(0, self.height))
  self.bgPath:close()

  self.fillPath:reset()
  self.fillPath:moveTo(Vector.xy(0, 0))
  self.fillPath:lineTo(Vector.xy(fillWidth, 0))
  self.fillPath:lineTo(Vector.xy(fillWidth, self.height))
  self.fillPath:lineTo(Vector.xy(0, self.height))
  self.fillPath:close()
end

local function init(self: ProgressBar, context: Context): boolean
  self.bgPath = Path.new()
  self.fillPath = Path.new()
  self.bgPaint = Paint.with({ style = "fill", color = Color.rgb(50, 50, 56) })
  self.fillPaint = Paint.with({ style = "fill", color = Color.rgb(80, 200, 140) })
  rebuild(self)
  return true
end

local function update(self: ProgressBar)
  rebuild(self)
end

local function draw(self: ProgressBar, renderer: Renderer)
  renderer:drawPath(self.bgPath, self.bgPaint)
  renderer:drawPath(self.fillPath, self.fillPaint)
end

return function(): Node<ProgressBar>
  return {
    init = init,
    update = update,
    draw = draw,
    width = 200,
    height = 20,
    current = 35,
    maximum = 100,
    bgPath = late(),
    fillPath = late(),
    bgPaint = late(),
    fillPaint = late(),
  }
end
```

### Percent Text Converter

Protocol:
- `Converter`

Pattern:
- Check type before casting.
- Implement `reverseConvert` only when two-way binding is needed.

```luau
export type PercentText = {}

local function convert(self: PercentText, input: DataInputs): DataOutput
  local out: DataValueString = DataValue.string()
  if input:isNumber() then
    out.value = `{math.floor((input :: DataValueNumber).value)}%`
  else
    out.value = ""
  end
  return out
end

local function reverseConvert(self: PercentText, input: DataOutput): DataInputs
  local out: DataValueNumber = DataValue.number()
  if input:isString() then
    local raw = (input :: DataValueString).value:gsub("%%", "")
    out.value = tonumber(raw) or 0
  else
    out.value = 0
  end
  return out
end

return function(): Converter<PercentText, DataValueNumber, DataValueString>
  return {
    convert = convert,
    reverseConvert = reverseConvert,
  }
end
```

### Pointer Toggle Node

Protocol:
- `Node`

Pattern:
- Register pointer handlers in the factory table.
- Call `event:hit()` when this script should consume the event.
- Keep drawing separate from pointer state mutation.

```luau
export type PointerToggle = {
  path: Path,
  offPaint: Paint,
  onPaint: Paint,
  active: boolean,
}

local function init(self: PointerToggle, context: Context): boolean
  self.path = Path.new()
  self.path:moveTo(Vector.xy(-50, -25))
  self.path:lineTo(Vector.xy(50, -25))
  self.path:lineTo(Vector.xy(50, 25))
  self.path:lineTo(Vector.xy(-50, 25))
  self.path:close()
  self.offPaint = Paint.with({ style = "fill", color = Color.rgb(90, 96, 110) })
  self.onPaint = Paint.with({ style = "fill", color = Color.rgb(80, 180, 255) })
  self.active = false
  return true
end

local function pointerDown(self: PointerToggle, event: PointerEvent)
  self.active = not self.active
  event:hit()
end

local function draw(self: PointerToggle, renderer: Renderer)
  renderer:drawPath(self.path, self.active and self.onPaint or self.offPaint)
end

return function(): Node<PointerToggle>
  return {
    init = init,
    draw = draw,
    pointerDown = pointerDown,
    path = late(),
    offPaint = late(),
    onPaint = late(),
    active = false,
  }
end
```
