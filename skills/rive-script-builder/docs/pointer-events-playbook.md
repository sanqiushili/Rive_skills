# Pointer Events Playbook

Use this file when a script handles taps, drags, multi-touch, or forwarded events.

## Supported Protocols

Pointer callbacks are available in:
- Node scripts
- Layout scripts

Callbacks:
- `pointerDown(self, event)`
- `pointerMove(self, event)`
- `pointerUp(self, event)`
- `pointerExit(self, event)`

## PointerEvent Essentials

From API reference:
- `event.position` is local-space pointer position.
- `event.id` is stable pointer identifier (important for multi-touch).
- `event:hit()` marks handled and stops propagation.
- `event:hit(true)` allows translucent pass-through behavior.

## Multi-Touch Pattern

Track active pointers by `event.id`:

```lua
type MyNode = {
  activePointers: {[number]: Vec2D},
}

local function pointerDown(self: MyNode, event: PointerEvent)
  self.activePointers[event.id] = event.position
  event:hit()
end

local function pointerMove(self: MyNode, event: PointerEvent)
  if self.activePointers[event.id] then
    self.activePointers[event.id] = event.position
    event:hit()
  end
end

local function pointerUp(self: MyNode, event: PointerEvent)
  self.activePointers[event.id] = nil
  event:hit()
end
```

Always clean pointer state in `pointerUp`/`pointerExit`.

## Nested Artboard Forwarding

Rive listens for pointer events on the main artboard.
For instantiated/nested artboards, forward events manually:
1. Convert parent-space coordinates into child local space.
2. Create forwarded event with `PointerEvent.new(id, localPos)`.
3. Call child pointer handler.

## Routing Strategy

Clarify these choices:
- Should parent consume pointer first or child first?
- Which handlers call `event:hit()`?
- Do we need translucent propagation (`hit(true)`)?
- How should simultaneous pointers map to entities?

## Debug Checklist

- Print `event.id` and coordinates in each handler.
- Verify `event:hit()` is used only where intended.
- Confirm pointer IDs are removed on release/exit.
- In nested forwarding, verify coordinate transform before dispatch.

