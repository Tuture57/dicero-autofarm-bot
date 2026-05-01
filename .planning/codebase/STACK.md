# Stack

## Language & Runtime
- Python 3.x (Windows 11, no version pinned in requirements.txt)

## Dependencies (`requirements.txt`)
| Package | Purpose |
|---|---|
| `pyautogui` | Mouse clicks, failsafe |
| `opencv-python` (cv2) | Template matching, image processing |
| `Pillow` (PIL / ImageGrab) | Imported in bot.py but not yet used for capture |
| `numpy` | Array ops on pixel data |
| `pywin32` (win32gui, win32con, win32ui) | Window enumeration, BitBlt screen capture |

## System-level calls
- `ctypes.windll.shcore.SetProcessDpiAwareness(2)` — DPI awareness for correct window geometry
- `win32gui.GetWindowRect` — window coordinates
- `win32gui.GetWindowDC` + `win32ui.CreateDCFromHandle` + `BitBlt` — screenshot path

## No frameworks, no database, no networking.
