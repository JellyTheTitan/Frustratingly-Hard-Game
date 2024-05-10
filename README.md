# Frustratingly Hard Game
A game made with Python. Very hard... tread if you dare.

# How to Play
You are a red square. You need to guide it to a big cyan portal.
There are just two levels you need to complete. Beat those and
you get an award.

# How to Mod
FHG is designed to be very easy to mod. Yuo can add your own
custom levels and splash texts (probably the most fun part).

Read on for a tutorial.

## Levels
The way that FHG creates and setups the levels is by using the
`levels.json` file located in the `Frustratingly-Hard-Game`
folder.

FHG reads levels from a JSON object (or a dictonary, in Python's
case). Here is an example of the first level:

```
{
    "player": {
      "start-x": -300,
      "start-y": -5
    },
    "portal": {
      "start-x": 260,
      "start-y": -5
    },
    "projectiles": [
      {
        "data": {
          "size": 32,
          "speed": 5,
          "move-style": "side to side",
          "range": 100,
          "start-x": -30,
          "start-y": 5,
          "start-dir": "left"
        },
        "display": {
          "color": [0, 0, 255],
          "inner-square-shade": 80
        }
      },
      {
        "data": {
          "size": 32,
          "speed": 5,
          "move-style": "side to side",
          "range": 100,
          "start-x": -115,
          "start-y": 65,
          "start-dir": "right"
        },
        "display": {
          "color": [0, 0, 255],
          "inner-square-shade": 80
        }
      }
    ],
    "walls": [
      {
        "x": -320,
        "y": 240,
        "width": 640,
        "height": 145,
        "color": [1, 50, 32],
        "inner-square-shade": 30
      },
      {
        "x": -320,
        "y": -95,
        "width": 640,
        "height": 145,
        "color": [1, 50, 32],
        "inner-square-shade": 30
      }
    ]
  }
```

Lets break this level down a bit:

### `player`
This object defines the player's data; more specifically, where the
player will start when the level is loaded.

### `portal`
Same as the `player`.

### `projectiles`
This is an array of objects, each one being a single projectile.

A projectile looks like this:

```
{
  "data": {
    "size": 32,
    "speed": 5,
    "move-style": "side to side",
    "range": 100,
    "start-x": -30,
    "start-y": 5,
    "start-dir": "left"
  },
  "display": {
    "color": [0, 0, 255],
    "inner-square-shade": 80
  }
}
```

The `data` key is used to define how the projectile behaves. Most of it
is self explanatory, but there are a few that may need some explaining.
`start-dir` defines what direction the projectile will start moving, and
`move-style` is used how the projectile moves.

(There is an unused `"diagonal"` type, but fully works. Use that if
you wish to do so.)
