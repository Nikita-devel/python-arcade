"""
Beta Minecraft — a tiny 3D block-building demo built with Ursina.

What changed and WHY:
  * The old code loaded a texture file called 'grass.png' that does NOT
    exist in this folder. Ursina couldn't find it, so the game crashed at
    startup. We now use Ursina's built-in 'white_cube' texture and tint it
    green, so the game needs no external image and always runs.
  * We added a friendly error message if the 'ursina' library isn't
    installed, telling you exactly how to install it.

Controls:
  * Mouse : look around
  * WASD  : walk
  * Left click  : remove a block
  * Right click : add a block
  * P     : quit
"""

import sys

# Ursina is a heavy 3D library and is not always installed. If it's
# missing, we explain how to get it instead of showing a confusing crash.
try:
    from ursina import (Ursina, Button, Sky, scene, color, mouse,
                        destroy, application, camera)
    from ursina.prefabs.first_person_controller import FirstPersonController
except ImportError:
    print("The 'ursina' library is required for Beta Minecraft.")
    print("Install it with:  pip install ursina")
    sys.exit(1)


app = Ursina()

player = FirstPersonController()
Sky()

# We build a 20x20 floor of blocks. Each block is a clickable Button in 3D.
# 'white_cube' is a texture that ships WITH ursina (no file needed); tinting
# it green gives us grass without any grass.png.
blocks = []


def make_block(position):
    """Create one grass block at the given (x, y, z) position."""
    block = Button(
        color=color.lime.tint(-0.2),   # greenish, slight variation
        model='cube',
        texture='white_cube',          # built-in, no external file
        position=position,
        parent=scene,
        origin_y=0.5,
    )
    return block


for i in range(20):
    for j in range(20):
        blocks.append(make_block((j, 0, i)))


def input(key):
    """Handle clicks: build or remove blocks, and quit on 'p'."""
    # Find the block the mouse is pointing at (if any).
    for block in blocks:
        if block.hovered:
            if key == 'right mouse down':
                # Add a new block on the face we're looking at.
                new_block = make_block(block.position + mouse.normal)
                blocks.append(new_block)
            elif key == 'left mouse down':
                # Remove the block we clicked.
                blocks.remove(block)
                destroy(block)
            break  # only act on the first hovered block

    if key == 'p':
        application.quit()


app.run()
