# Editor Wiring Recipes

Use these steps after script generation so users can attach and run scripts correctly.

## Create a Script

Use either entry:

1. Assets panel
- Click `+`
- Choose `Script`
- Choose protocol type

2. Toolbar script tool
- Click dropdown next to Script button
- Choose protocol type

Naming rule:
- Use PascalCase script asset name.
- Keep main type name aligned with script name.

## Attach by Protocol

### Node

1. Right-click target artboard.
2. Select script from list.
3. Position script object in scene.
4. Select script/group and set inputs in right sidebar.

### Layout

1. Add/select a Layout in scene.
2. Create Layout script.
3. Add script as child of that Layout.

### Converter

1. In Data panel click `+`.
2. Choose `Converters -> Script -> <YourConverter>`.
3. Bind converter where needed.

### Path Effect

1. Select stroke on target shape.
2. Open Effects tab.
3. Click `+` and choose Script Effect.
4. Select your path-effect script.
5. Configure effect inputs.

### Transition Condition

1. Select transition in state machine.
2. Click `+` to add condition.
3. Select scripted transition condition.
4. Configure script inputs.

### Listener Action

1. Select listener in state machine.
2. Click `+` and choose scripted action.
3. In Run dropdown, pick your script.
4. Configure inputs.

### Util

- Do not attach to scene directly.
- Use `require('UtilScriptName')` from other scripts.

### Test

1. Create Test script.
2. Right-click Test script in Assets panel.
3. Select `Run Tests`.

## Inputs and Data Binding

1. Select script instance (or converter) to expose inputs in right sidebar.
2. Set value directly, or right-click input field and choose Data Bind.
3. Bind to view model property where needed.

Remember:
- Inputs control scripts.
- Scripts do not set normal input values directly.

## Troubleshooting Checklist

If script does not appear or run:

1. Confirm script exists in Assets panel.
2. Check Problems panel for syntax/type/binding errors.
3. Confirm returned table includes required lifecycle methods for that protocol.
4. Confirm binding targets exist and types match.
