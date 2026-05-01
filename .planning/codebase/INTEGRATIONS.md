# Integrations

## MirrorTo (Android mirroring app)
- **Role**: renders the Android game as a window on Windows desktop
- **Interface**: Win32 HWND identified by window title containing "MirrorTo"
- **Data consumed**: window pixel content via BitBlt; window rect via GetWindowRect
- **Data produced**: mouse clicks via pyautogui (coordinates mapped back to screen space)

## Android Game (dungeon auto-farmer target)
- **Interface**: purely visual — no ADB, no game API
- **States recognised**: dungeon, wheel, select_skill, select_dice, confirm_popup, unknown
- **Interaction**: simulated mouse clicks at detected template centers

## No external APIs, no network calls, no file I/O beyond template PNGs.
