# 🎮 Python Arcade

A collection of classic games wrapped in a single fullscreen menu, built with
**Python** and **pygame**. Launch the menu, pick a game, play, and come back —
the menu handles everything.

This started as a set of "pet projects" for learning game programming. It's a
great codebase to read if you're just starting out: each game is small,
self-contained, and heavily commented.

---

## 🕹️ Games included

| Game            | What it is                                | Built with        |
| --------------- | ----------------------------------------- | ----------------- |
| Puissance 4     | Connect Four, two players                 | pygame + numpy    |
| Flappy Bird     | Tap to fly through the pipes              | pygame            |
| Pong            | The classic two-paddle bounce game        | turtle + pygame   |
| Snake           | Eat, grow, don't bite yourself            | pygame            |
| Space Shooter   | Blast waves of enemy ships                | pygame            |
| AeroBlaster     | Fast-paced action shooter                 | pygame            |
| Beta Minecraft  | Tiny 3D block-building demo               | ursina            |
| GPS Analyse     | Utility: analyse a GPS track from a CSV   | tkinter + pandas  |

---

## 🚀 Getting started

You need **Python 3.10 or newer**.

**1. Get the code**

```bash
git clone https://github.com/Nikita-devel/python-arcade.git
cd python-arcade
```

**2. (Recommended) Create a virtual environment**

A virtual environment is a private box of libraries just for this project, so
it doesn't interfere with the rest of your computer.

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

**3. Install the libraries**

```bash
pip install -r requirements.txt
```

> On Linux you may also need tkinter for a few games:
> `sudo apt install python3-tk`

**4. Run the menu**

```bash
python main.py
```

Click **PROGRAMS** to play, **GUIDE** to read how each game works, or **QUIT**
to exit. Inside a game, look for a **BACK** button or read its guide for the
exit key.

---

## 📁 Project structure

```
python-arcade/
├── main.py                 # The menu. Start here.
├── requirements.txt        # Libraries to install.
├── assets/                 # Menu background, font, and sounds.
│   └── audio/
├── menu_lib/               # Reusable menu code.
│   ├── button.py           # The clickable Button class.
│   └── explanations.py     # How-to-play text for each game.
├── games/                  # One folder per game, each self-contained.
│   ├── connect4/
│   ├── flappy-bird/
│   ├── pong/
│   ├── snake/
│   ├── SpaceShooter/
│   ├── AeroblasterSource/
│   ├── minecraft/
│   └── gps/
└── docs/
    ├── HOW_IT_WORKS.md     # A friendly walkthrough of how the menu works.
    └── INSTALL_UA.md       # Покрокова інструкція встановлення (українською).
```

Each game lives in its own folder with its own assets, so you can copy a single
game out and run it on its own if you want.

---

## 🧠 New to this? Read `docs/HOW_IT_WORKS.md`

If you're learning Python, [`docs/HOW_IT_WORKS.md`](docs/HOW_IT_WORKS.md)
explains — in plain language — how the menu draws buttons, detects clicks, and
launches games. Start there, then open `main.py` and follow along.

---

## 🙌 Credits

The menu, structure, and game integration were written by
[Nikita-devel](https://github.com/Nikita-devel).

Some individual games (Aeroblaster, Space Shooter) are based on well-known
open-source pygame tutorials; see the notes inside their folders. Assets
(sounds, sprites, fonts) belong to their respective creators and are used here
for a non-commercial learning project.

---

## 📄 License

Released under the MIT License — see [LICENSE](LICENSE). You're free to read,
run, modify, and learn from this code.
