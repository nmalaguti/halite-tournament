{% extends "tournament/documentation/documentation.html" %}

{% block title %}Documentation - Improving the Random Bot{% endblock %}

{% block docs %}
{% markdown %}

# Improving the Random Bot

In this tutorial, we'll go through the code that powers the random bot and add a couple heuristics to it.
This will hopefully help you fully understand Halite and set you on your way to leaderboard domination.

### Prerequisites

Make sure that you have read [Introducing Halite]({% url 'tournament:documentation' page_name="basics_intro" %})
and followed the setup procedures described there. Now open up the MyBot file in your favorite editor and let's get started!

### Important Considerations

When writing a halite bot, be sure to stay away from functions like `print`. Bots use stdout and stdin
to communicate with the game environment. You will be ejected from a game of Halite if you print
debugging info to stdout. Instead, print to a log file.

### A Look At the Random Bot

Now that you know how the game works, how do the two random starter bots work? How does one code a Halite bot?
Here is the source from the main file of our python starter bot:

```python
import random

import hlt
from hlt import EAST, NORTH, SOUTH, STILL, WEST, Move, Square

myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBot")

while True:
    game_map.get_frame()
    moves = [
        Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL)))
        for square in game_map
        if square.owner == myID
    ]
    hlt.send_frame(moves)
```

Let's walk through it line by line.

First we make some imports from the `hlt.py` helper file that is included in the starter package:

```python
import random

import hlt
from hlt import EAST, NORTH, SOUTH, STILL, WEST, Move, Square
```

Then we get our ID (each player has a unique identifier that is associated with their pieces) and the initial
game map from the environment. We send back the name of our bot. This is used in game replays.

```python
myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBot")
```

Now we start our game loop. Each turn, update the current map from the game environment:
    

```python
while True:
    game_map.get_frame()
```

Let's create our list of moves by cycling through all the pieces on the map. If a piece is owned by us,
let's instruct it to move in a random direction.

```python
    moves = [
        Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL)))
        for square in game_map
        if square.owner == myID
    ]
```

Finally, let's send all of our moves to the environment:

```python
    hlt.send_frame(moves)
```

And that's RandomBot!

### Utilizing Our Production

From the rules outlined in [Introducing Halite]({% url 'tournament:documentation' page_name="basics_intro" %}),
we know that when a piece moves, it gains no strength and leaves behind a piece with zero strength. It easily
follows from this that moving zero strength pieces is a terrible idea, since:

- A zero strength piece that moves will necessarily stay at zero strength, because pieces don't gain strength for any turn that
  they move.
- A zero strength piece won't ever conqueror any territory, because it has no strength with which to damage other pieces.

Let's wrap the movement logic inside a function of its own. This function will take a piece as input and will
return the piece's movement.

```python
def get_move(square):
    return Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL)))


while True:
    game_map.get_frame()
    moves = [get_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
```

Now we can improve our bot by making sure that we tell all of our zero strength pieces to remain still.

```python
def get_move(square):
    if square.strength == 0:
        return Move(square, STILL)

    return Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL)))
```

{% minimal_replay "576286-4192079766.hlt.gz" %}

Our bot still moves its pieces around a lot (only a bit over one out of five turns will a piece stay still).
This costs us a lot of strength since a piece doesn't gain any strength on turns that it moves. To
increase our utilization of our production, let's have pieces only move once their strength equals their
production times some factor <var>X</var>. We're using 5 as the value of <var>X</var> in this example,
but this is arbitrary.

```python
def get_move(square):
    if square.strength < square.production * 5:
        return Move(square, STILL)

    return Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL)))
```

{% minimal_replay "578243-4192079766.hlt.gz" %}

### Moving to Our Borders

When building a Halite bot, one of our goals should be moving strength out of your territory quickly
and with little production loss. Our current bot is terrible at this. Its pieces move randomly around
our territory, going nowhere, costing us production, and often losing strength to the strength cap. 

To improve this, let's just mandate that our pieces move only north and west. Since the map is
wrap-around, we can still capture all of the board with this strategy! 

```python
def get_move(square):
    if square.strength < square.production * 5:
        return Move(square, STILL)

    return Move(square, random.choice((NORTH, WEST)))
```

{% minimal_replay "578847-4192079766.hlt.gz" %}


### Improving our Attack

Once our pieces get to our borders, we don't want them to randomly attack just any square (or worse, move back into our territory),
as we do now. One problem with this random strategy is that we may attack a map square that has more strength than us. This is
unproductive (pun implied) since moving onto the map square costs us a turn of production and we don't actually gain anything. We
just diminish the squares strength.

To improve on our current combat, if there is an enemy or map square that is adjacent to one of our pieces with less strength than
our piece, let's take it.

```python
def get_move(square):
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner != myID and neighbor.strength < square.strength:
            return Move(square, direction)

    if square.strength < square.production * 5:
        return Move(square, STILL)

    return Move(square, random.choice((NORTH, WEST)))
```

{% minimal_replay "580255-4192079766.hlt.gz" %}

### What's Next?

That's really up to you! How you improve your bot from here is where you step into the competition.

That said, if you're looking for more ideas or a stronger starting base, read through
[Next Steps]({% url 'tournament:documentation' page_name="next_steps" %}) for a tutorial that walks
you through improving your combat, piece management, and expansion.

Good luck!

{% endmarkdown %}
{% endblock %}
