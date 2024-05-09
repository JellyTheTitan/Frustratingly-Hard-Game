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
case). Here is an example:

```
"player": {
  "start-x": 0,
  "start-y": 0
}
```
