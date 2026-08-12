# Installation & Testing — step by step

This guide takes you from "nothing installed" to "playing the games".
Follow the steps in order. If something breaks, see **"If it doesn't work"**
at the bottom.

You need **Python 3.10 or newer** (tested on 3.12).

---

## Step 0. Check that Python is installed

Open a terminal and type:

```bash
python3 --version
```

If you see something like `Python 3.12.3`, you're good — go to step 1.

If it says `command not found` or the version is below 3.10:
- **Windows:** install from [python.org](https://www.python.org/downloads/)
  (tick **"Add Python to PATH"** during setup).
- **macOS:** `brew install python` or from python.org.
- **Linux (Ubuntu):** `sudo apt install python3 python3-venv python3-pip python3-tk`

---

## Step 1. Get the project

If you have git:

```bash
git clone https://github.com/Nikita-devel/python-arcade.git
cd python-arcade
```

Or unzip the `python-arcade.zip` you were given and enter the folder:

```bash
cd path/to/python-arcade
```

---

## Step 2. Create a virtual environment (recommended)

A virtual environment is a private box of libraries just for this project.

```bash
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

When it's active you'll see `(venv)` at the start of the terminal line.

---

## Step 3. Install the libraries

```bash
pip install -r requirements.txt
```

> On Linux you may also need tkinter for Pong and the GPS tool:
> `sudo apt install python3-tk`

---

## Step 4. Run the menu

```bash
python main.py
```

Click **PROGRAMS** to play, **GUIDE** to read how each game works, or **QUIT**
to exit. Use the mouse or the **left/right arrow keys** to change pages.

---

## Step 5. Test everything (checklist)

**Menu:**
- [ ] Buttons light up green on hover.
- [ ] Background music plays (if your computer has sound).
- [ ] `<` `>` on screen AND the keyboard arrow keys change pages.
- [ ] **BACK** returns to the main menu.

**Games:**

| Game           | Controls                          | How to quit    |
| -------------- | --------------------------------- | -------------- |
| Connect 4      | Mouse + left click on a column    | ESC after a win|
| Flappy Bird    | SPACE to flap                     | Exit button    |
| Pong           | Z/S (left), Up/Down (right)       | ESC            |
| Snake          | Arrow keys; Q quit, C play again  | Q              |
| Space Shooter  | Arrow keys + SPACE to shoot       | Close window   |
| AeroBlaster    | Arrows/A,D + SPACE                | Close window   |
| Beta Minecraft | Mouse + WASD; L/R click blocks    | P              |
| GPS Analyse    | "Start" button, pick a CSV        | Quit button    |

- [ ] After a game closes, the menu comes back and music resumes.
- [ ] In **GUIDE**, each game shows its OWN instructions.

---

## If it doesn't work

**`ModuleNotFoundError: No module named 'pygame'` (or numpy/pandas/ursina)**
The libraries didn't install. Make sure the venv is active (`(venv)` shown)
and run again:
```bash
pip install -r requirements.txt
```

**`No module named 'tkinter'` (Linux)**
```bash
sudo apt install python3-tk
```

**`pygame.error: ... No such file or directory` (can't find an image/sound)**
Run the menu from the **project root folder** (where `main.py` is), not from
inside a game folder.

**`command not found: python`**
Use `python3` instead of `python` in every command above.

---

If you get stuck, note which step and the exact error text.
