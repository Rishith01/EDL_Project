# VS Code setup for MicroPython import errors

Use this checklist on your local machine so VS Code (Pylance) stops showing red-underlined imports such as `machine`, `micropython`, and `uasyncio`.

## 1) Install VS Code extensions

Install these from the Extensions marketplace:

1. **Python** (`ms-python.python`)
2. **Pylance** (`ms-python.vscode-pylance`)
3. **MicroPico** (`paulober.pico-w-go`) – optional but useful for flashing/running on boards

## 2) Create a local virtual environment

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 3) Install desktop + analysis dependencies

These help VS Code resolve imports used in this repository:

```bash
pip install pyserial opencv-python PyQt5
pip install adafruit-circuitpython-motorkit
```

## 4) Install MicroPython type stubs

Install stubs for static analysis (these are not flashed to the board):

```bash
pip install micropython-rp2-stubs
```

If you use another board/port, install the matching stubs package (for example ESP32 variants).

## 5) Point Pylance to stub locations

Create `.vscode/settings.json` in this repo:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.extraPaths": [
    "${workspaceFolder}/Master_RPI/micropython",
    "${workspaceFolder}/Slave_RPI/micropython"
  ],
  "python.analysis.typeCheckingMode": "basic"
}
```

For stubborn `machine`/`uasyncio` warnings, add your installed site-packages stubs path into `extraPaths` too. You can find it with:

```bash
python -c "import site; print(site.getsitepackages())"
```

## 6) Files to download for board deployment (optional)

For a MicroPython board workflow, download:

1. **MicroPython firmware UF2/BIN** for your board from the official MicroPython downloads page.
2. Any board-specific libraries (if not frozen in firmware), copied to the board `lib/` folder.

> Note: packages installed with `pip` on your laptop are for editor support and host-side scripts; board runtime modules must exist in board firmware or on-board filesystem.

## 7) Quick verification

After setup:

```bash
python -c "import serial, cv2, PyQt5; print('Host deps OK')"
python -c "import adafruit_motorkit; print('MotorKit OK')"
```

Then in VS Code:
- Select the `.venv` interpreter.
- Run **Developer: Reload Window**.
- Re-open a file in `Master_RPI/micropython/` and confirm import warnings are gone or significantly reduced.
