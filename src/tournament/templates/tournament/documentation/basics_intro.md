{% extends "tournament/documentation/documentation.html" %}

{% block title %}Documentation - Introducing Halite{% endblock %}

{% block docs %}
{% markdown %}

# Introducing Halite

In [the last tutorial]({% url 'tournament:documentation' page_name="getting_started" %}),
we showed how to submit a demo bot to the leaderboard. In this short tutorial, we will go over
the files included in a starter package, running a game of halite, and the rules of halite.

### A look at the starter package

Your starter package should contain these files.

<table class="table">
    <tr>
        <th>Filename</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>MyBot</td>
        <td>Your main file. Starts containing the code for a random bot.</td>
    </tr>
    <tr>
        <td>RandomBot</td>
        <td>A random bot to test changes to your bot against.</td>
    </tr>
    <tr>
        <td>runGame.sh</td>
        <td>Script to run a game on Linux/macOS</td>
    </tr>
</table>

The file you need to change is MyBot. Regardless of what you do with your code, MyBot will be
considered your main file on our game servers.

### Testing your bot

To play games of Halite locally, you will need the game environment.
You can download the game environment [here](https://github.com/nmalaguti/halite-matches/releases").
Place the downloaded binary `halite` in your starter kit folder.

To simulate a game, simply issue the command ./runGame.sh (Linux and macOS). This command will run a game
between my MyBot and RandomBot (both are just copies of each other at this point) on a grid of size 30x30.

The output should look like this and the details of the game will be stored in a file with the
"hlt" extension (`35538-124984302.hlt` in the example below).

```plaintext
$ ./runGame.sh
python MyBot.py
python RandomBot.py
Init Message sent to player 2.
Init Message sent to player 1.
Init Message received from player 1, MyPythonBot.
Init Message received from player 2, RandomPythonBot.
Turn 1
Turn 2
Turn 3
Turn 4
…
Turn 299
Turn 300
Map seed was 124984302
Opening a file at 35538-124984302.hlt
Player #1, MyPythonBot, came in rank #1!
Player #2, RandomPythonBot, came in rank #2!
```

### Visualizing a game

The console output from the game environment gives just the outcome of the game. To replay the game, drag and drop the file to
[the visualizer]({% url "tournament:visualizer" %}). Since the starter pack is very bad at playing Halite, your visualization
will be quite dull.

{% minimal_replay "582452-4192079766.hlt.gz" %}

### Halite game rules

What do all of these pretty squares mean?

Halite is played on a rectangular grid. Players own pieces on this grid. Some pieces are unowned and so belong to the map until
claimed by players. Each piece has a strength value associated with it.

At each turn, bots decide how to move the pieces they own. Valid moves are: `STILL`, `NORTH`, `EAST`, `SOUTH`, `WEST`.
When a piece remains `STILL`, its strength is increased by the production value of the site it is on. When a piece moves,
it leaves behind a piece with the same owner and a strength of zero.

When two or more pieces from the same player try to occupy the same site, the resultant piece gets the sum of their strengths
(this strength is capped at `255`).

When pieces with different owners move onto the same site or cardinally adjacent sites, the pieces are forced to fight, and each
piece loses strength equal to the strength of its opponent. When a player's piece moves onto an unowned site, that piece and the
unowned piece fight, and each piece loses strength equal to the strength of its opponent.

When a piece loses all of its strength, it dies and is removed from the grid.

For the full rules, see [here]({% url 'tournament:documentation' page_name="game_rules" %}).

### How do we program a bot?

Move on to [Improving the Random Bot]({% url 'tournament:documentation' page_name="improve_random" %}).

{% endmarkdown %}
{% endblock %}
