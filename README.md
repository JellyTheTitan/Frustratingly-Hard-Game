# Frustratingly Hard Game
A game made with Python. Very hard... tread if you dare.

# How to Play
You are a red square. Using either [W][A][S][D] or the arrow keys, 
you need to guide it to a big cyan portal. There are just 
two levels you need to complete. Beat those and you get an award.

# How to Mod
FHG is designed to be very easy to mod. You can add your own
custom levels and splash texts (probably the most fun part).

Read on for a tutorial.

## Levels
The way that FHG creates and setups the levels is by using the
`levels.json` file located in the `Frustratingly-Hard-Game`
folder.

FHG reads levels from a JSON object (or a dictonary, in Python's
case). Here is an example of the first level:

```json
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
Same as `player`.

### `projectiles`
This is an array of objects, each one being a single projectile.

A projectile looks like this:

```json
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
`move-style` is used for how the projectile moves.

(There is an unused `"diagonal"` type, but fully works. Use that if
you wish.)

`display` doesn't have very much to it... just a color and a shade.
`display/color` is an array, and if you notice, there are three
numbers, signifying that it is in RGB value. In the example above,
it is the color blue. `display/inner-square-shade` describes how darker the
smaller square is compared to the main one.

For more directions and move types, look in the `main.py` file and it's variables
for more info.

### `walls`
`walls` (similar to `projectiles`), consists of an array of objects.

Here is a wall:

```json
{
    "x": -320,
    "y": 240,
    "width": 640,
    "height": 145,
    "color": [1, 50, 32],
    "inner-square-shade": 30
}
```
Pretty simple compared to `projectiles`, you just need to put in the
given info, like a width and height, position, etc.

## Splash Texts
The most fun part to mod, you can add your own splash texts (the texts
that appear before the game starts). It is ***very*** customizable,
with no limits.

Here is a splash text:
```json
{
    "texts": [
        "This line lasts for 2 seconds and is red",
        "This line lasts for 4 seconds and is green",
        "This line lasts for 1 second and is purple"
    ],
    "delays": [
        2,
        4
        1
    ],
    "text-data": {
        "spacing": 30,
        "color": [
            [255, 0, 0],
            [0, 255, 0],
            [255, 0, 255]
        ],
        "size": 30
    }
}
```

Something cool to remember is everything (excluding `texts`)
can be either one value or a list values; FHG is smart enough
to tell which is the difference (note that if something is a
list, it must correlate with the amount of lines that `texts` contains).
