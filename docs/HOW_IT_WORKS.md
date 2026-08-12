# How It Works — a friendly walkthrough

This page explains how the arcade menu works, step by step, in plain language.
It's written for someone who is **just starting to learn Python**. Read it with
`main.py` open next to you.

---

## 1. The big idea

The program is really two things:

1. **A menu** (`main.py`) — the screen with the buttons.
2. **A bunch of games** (inside `games/`) — each one its own little program.

The menu's job is simple: *show buttons, and when you click a game, start it.*

---

## 2. What is a "game loop"?

Every game — including this menu — runs the same pattern over and over, many
times per second:

```
while True:          # forever...
    1. Look at what happened (did the mouse move? did you click?)
    2. Update things    (change the page, launch a game...)
    3. Draw everything  (background, buttons, text)
```

One trip through that loop is called a **frame**. If it happens 60 times a
second, that's "60 FPS". Because it's so fast, your eyes see smooth movement,
just like a flip-book.

You'll see `while True:` in every screen function (`main_menu`,
`programs_screen`, `guide_screen`). That's the game loop.

---

## 3. Drawing the screen

Three lines you'll see a lot:

```python
SCREEN.blit(BG, (0, 0))     # paint the background first
button.update(SCREEN)       # then draw a button on top
pygame.display.update()     # finally, show the finished frame
```

Think of it like painting: you paint the background, then the things on top,
then you reveal the whole picture at once with `pygame.display.update()`.
Order matters — whatever you draw last appears on top.

---

## 4. The Button class

Look at `menu_lib/button.py`. Instead of writing "draw some text and check if
the mouse is on it" over and over, we wrote it **once** as a class called
`Button`. Then everywhere in the menu we just do:

```python
button = Button(None, (x, y), "PLAY", font, "White", "Green")
button.changeColor(mouse_position)   # turn green if hovered
button.update(SCREEN)                # draw it
```

This is one of the most important ideas in programming: **write it once, reuse
it many times.** If you want to change how all buttons look, you change one file.

A `Button` knows three tricks:

- `update()` — draw itself.
- `checkForInput(point)` — "is this (x, y) point inside me?" (used to detect clicks).
- `changeColor(point)` — light up when the mouse hovers over it.

---

## 5. Detecting a click (the tricky part)

Here's something subtle that trips up beginners.

The mouse being **held down** is different from a **click**. If you check
"is the button pressed?" every frame, then a single quick click might be caught
on 3 or 4 frames in a row, and your game reacts several times to one click.

The fix: pygame gives us **events**. A click creates exactly **one**
`MOUSEBUTTONDOWN` event. So we react to the event, not to the button state:

```python
for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 = left click
        if button.checkForInput(mouse_pos):
            launch_game(...)
```

One event → one action. This is why the menu handles all clicks inside the
`for event in pygame.event.get():` loop.

---

## 6. How a game gets launched

When you click a game, the menu doesn't run the game *inside itself*. Instead,
it starts the game as a **separate program**, exactly like typing
`python games/snake/snake_game.py` in a terminal:

```python
subprocess.Popen([sys.executable, full_path]).wait()
```

- `sys.executable` is the exact Python that's running the menu (safer than
  writing `"python"`, which might not exist or point at the wrong version).
- `.wait()` means "pause the menu here until the player closes the game."

**Why do it this way?** If a game has a bug and crashes, only *that* program
dies. The menu keeps running. It's like each game is in its own room — if one
room catches fire, the rest of the house is fine.

---

## 7. Pages (pagination)

There are 8 games but only room for 5 on screen. So the list is split into
**pages**. This little formula rounds up to find how many pages we need:

```python
total_pages = (len(GAMES) + GAMES_PER_PAGE - 1) // GAMES_PER_PAGE
```

Then we show just a **slice** of the list for the current page:

```python
start = page * GAMES_PER_PAGE
visible = GAMES[start:start + GAMES_PER_PAGE]
```

The `<` and `>` arrows just add or subtract 1 from `page`.

---

## 8. One list, used twice

Notice that `main.py` has a single list called `GAMES`. Both the PROGRAMS
screen (to launch games) and the GUIDE screen (to show instructions) read from
it. Each entry has a name, a file path, and its how-to-play text.

That means when you add a new game, you edit **one** list, and it shows up in
both places automatically. Try it: add a new dictionary to `GAMES` and run the
menu again.

---

## 9. Your turn — small experiments

Good ways to learn are to change one thing and see what happens:

- Change a button color from `"Green"` to `"Red"`.
- Change `GAMES_PER_PAGE` from 5 to 3 and watch the pages change.
- Add your own game folder and a new entry in the `GAMES` list.
- Change the menu title text in `main_menu()`.

Break things, read the error messages, fix them. That's exactly how you learn.
Have fun! 🚀
