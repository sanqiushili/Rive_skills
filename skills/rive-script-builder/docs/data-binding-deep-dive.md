# Data Binding Deep Dive

Use this file when a script must read or write runtime data through View Models.

## Access Paths

There are three primary access patterns:

1. Through `Context` in `init(self, context)`.
2. Through a ViewModel-typed input (`Input<Data.YourType>`).
3. Through data-bound plain inputs (read-only from script side).

From `Context`, common entry points are:
- `context:viewModel()` for local bound data.
- `context:rootViewModel()` for root artboard data.
- `context:dataContext()` when parent traversal is required.

## Read and Write Rules

Read and write by resolving typed properties first, then accessing `.value`.

Common property accessors:
- `getNumber`
- `getString`
- `getBoolean`
- `getColor`
- `getTrigger`
- `getList`
- `getViewModel`
- `getEnum`

Example:

```lua
type MyNode = {
  context: Context,
}

local function init(self: MyNode, context: Context): boolean
  self.context = context

  local vm = context:viewModel()
  if not vm then
    return false
  end

  local score = vm:getNumber("score")
  if score then
    score.value = score.value + 1
  end

  local launch = vm:getTrigger("launch")
  if launch then
    launch:fire()
  end

  return true
end
```

## Listener Lifecycle

Use listeners for property changes and triggers, but always plan cleanup.

Recommended pattern:
1. Save callback references on `self`.
2. Add listeners in `init`.
3. Remove listeners when they are no longer needed.

If listener callbacks should refresh script state, call:
- `context:markNeedsUpdate()`

## Nested View Models

Use `getViewModel` for nested structures:

```lua
local vm = context:viewModel()
if vm then
  local profile = vm:getViewModel("profile")
  if profile then
    local age = profile:getNumber("age")
  end
end
```

## Interaction With Script Inputs

Important constraint:
- Inputs can control scripts, but scripts cannot set normal input values.

If runtime writes are needed, use:
- context-accessed view model properties, or
- ViewModel-typed inputs (`Input<Data.X>`).

## Current Boundary

The docs page for creating ViewModel instances is marked "Coming soon".
Do not assume unsupported runtime creation APIs unless confirmed by live docs.

## Clarification Questions

Ask these before implementation:
- Which ViewModel path is authoritative (local or root)?
- Which properties are read-only vs writable?
- Do we need trigger firing or only value updates?
- Where should listeners be attached, and when should they be removed?

