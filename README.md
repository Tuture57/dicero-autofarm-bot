# AutoFarm - Dungeon Bot

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)

An automation bot for a dungeon mobile game, mirrored to PC via MirrorTo. Handles all game states autonomously: attack loop, skill selection, dice selection, fortune wheel, and confirmation popups.

## Prerequisites

- **Windows 11** (required, uses Windows-only APIs)
- **Python 3.10+**
- **MirrorTo** - Android mirroring app running with the game visible at a fixed window size
- **Administrator rights** - the app auto-elevates on launch (a UAC prompt will appear)

## Installation

1. Clone or download this repository.
2. Copy `config.json.example` to `config.json`.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Start the bot:
   ```
   python main.py
   ```

## Usage

Running `python main.py` opens an interactive menu with three options:

- **Calibrate templates** - capture reference images for scene detection (run once, or after resizing/moving the MirrorTo window)
- **Run bot** - start the automation loop
- **Quit** - exit the program

Press `Ctrl+C` at any time to stop and return to the menu.

## Recalibration

If the bot stops detecting game states correctly after moving or resizing the MirrorTo window, select **Calibrate templates** from the menu and follow the on-screen prompts to re-capture reference images.

## Author

[@Tuture57](https://github.com/Tuture57)

