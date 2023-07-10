{% extends "tournament/documentation/documentation.html" %}

{% block title %}Documentation - Improving the Random Bot{% endblock %}

{% block docs %}
    <h1>Improving the Random Bot</h1>
    <p>In this tutorial, we'll go through the code that powers the random bot and add a couple heuristics to it. This will hopefully help
        you fully understand Halite and set you on your way to leaderboard domination.</p>

    <h3>Prerequisites</h3>
    <p>Make sure that you have read <a href="{% url 'tournament:documentation' page_name="basics_intro" %}">Introducing Halite</a> and followed the setup
        procedures described there.</p>
    <p>Now open up the MyBot file in your favorite editor and let's get started!</p>

    <h3>Important Considerations</h3>
    <p>When writing a halite bot, be sure to stay away from functions like <code>System.out.print</code>, <code>cout</code>,
        <code>print</code>, etc. Bots use stdout and stdin to communicate with the game environment. You will be ejected from a game of
        Halite if you print debugging info to stdout. Instead, print to a log file.</p>

    <h3>A Look At the Random Bot</h3>
    <p>Now that you know how the game works, how do the two random starter bots work? How does one code a Halite bot? Here is the source
        from the main file of our python starter bot:</p>

    <pre><code class="language-python">import random

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
    hlt.send_frame(moves)</code></pre>

    <p>Let's walk through it line by line.</p>

    <p>First we make some imports from the hlt.py helper file that is included in the starter package:</p>

    <pre><code class="language-python">import random

import hlt
from hlt import EAST, NORTH, SOUTH, STILL, WEST, Move, Square</code></pre>

    <p>Then we get our ID (each player has a unique identifier that is associated with their pieces) and the initial game map from the
        environment. We send back the name of our bot. This is used in game replays.</p>

    <pre><code class="language-python">myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBot")</code></pre>

    <p>Now we start our game loop. Each turn, update the current map from the game environment:</p>
    <p></p>

    <pre><code class="language-python">while True:
    game_map.get_frame()</code></pre>

    <p>Let's create our list of moves by cycling through all the pieces on the map. If a piece is owned by us, let's instruct it to move in
        a random direction.</p>

    <pre><code class="language-python">    moves = [
        Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL)))
        for square in game_map
        if square.owner == myID
    ]</code></pre>

    <p>Finally, let's send all of our moves to the environment:</p>

    <pre><code class="language-python">hlt.send_frame(moves)</code></pre>

    <p>And that's RandomBot!</p>

    <h3>Utilizing Our Production</h3>

    <p>From the rules outlined in <a href="{% url 'tournament:documentation' page_name="basics_intro" %}">Introducing Halite</a>, we know that when a piece
        moves, it gains no strength and leaves behind a piece with zero strength. It easily follows from this that moving zero strength
        pieces is a terrible idea, since:</p>
    <ul>
        <li>A zero strength piece that moves will necessarily stay at zero strength, because pieces don't gain strength for any turn that
            they move.
        </li>
        <li>A zero strength piece won't ever conqueror any territory, because it has no strength with which to damage other pieces.</li>
    </ul>
    <p>Let's wrap the movement logic inside a function of its own. This function will take a piece as input and will return the piece's
        movement.</p>

    <pre><code class="language-python">def get_move(square):
    return Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL)))


while True:
    game_map.get_frame()
    moves = [get_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
    </code></pre>

    <p>Now we can improve our bot by making sure that we tell all of our zero strength pieces to remain still.</p>

    <pre><code class="language-python">def get_move(square):
    if square.strength == 0:
        return Move(square, STILL)

    return Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL)))</code></pre>

    <div
            class="thumbnail center-block replay"
            data-replay-url="{% static "tournament/replays/576286-4192079766.hlt.gz" %}"
            data-replay-is-minimal="true"
            data-replay-max-height="500">
    </div>

    <p>Our bot still moves its pieces around a lot (only a bit over one out of five turns will a piece stay still). This costs us a lot of
        strength since a piece doesn't gain any strength on turns that it moves. To increase our utilization of our production, let's have
        pieces only move once their strength equals their production times some factor <var>X</var>. We're using 5 as the value of <var>X</var> in this example,
        but this is arbitrary.</p>

    <pre><code class="language-python">def get_move(square):
    if square.strength < square.production * 5:
        return Move(square, STILL)

    return Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL)))</code></pre>

    <div
            class="thumbnail center-block replay"
            data-replay-url="{% static "tournament/replays/578243-4192079766.hlt.gz" %}"
            data-replay-is-minimal="true"
            data-replay-max-height="500">
    </div>

    <h3>Moving to Our Borders</h3>
    <p>When building a Halite bot, one of our goals should be moving strength out of your territory quickly and with little production loss.
        Our current bot is terrible at this. Its pieces move randomly around our territory, going nowhere, costing us production, and often
        losing strength to the strength cap. </p>
    <p>To improve this, let's just mandate that our pieces move only north and west. Since the map is wrap-around, we can still capture all
        of the board with this strategy! </p>

    <pre><code class="language-python">def get_move(square):
    if square.strength < square.production * 5:
        return Move(square, STILL)

    return Move(square, random.choice((NORTH, WEST)))</code></pre>

    <div
            class="thumbnail center-block replay"
            data-replay-url="{% static "tournament/replays/578847-4192079766.hlt.gz" %}"
            data-replay-is-minimal="true"
            data-replay-max-height="500">
    </div>

    <h3>Improving our Attack</h3>
    <p>Once our pieces get to our borders, we don't want them to randomly attack just any square (or worse, move back into our territory),
        as we do now. One problem with this random strategy is that we may attack a map square that has more strength than us. This is
        unproductive (pun implied) since moving onto the map square costs us a turn of production and we don't actually gain anything. We
        just diminish the squares strength.</p>
    <p>To improve on our current combat, if there is an enemy or map square that is adjacent to one of our pieces with less strength than
        our piece, let's take it.</p>

    <pre><code class="language-python">def get_move(square):
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner != myID and neighbor.strength < square.strength:
            return Move(square, direction)

    if square.strength < square.production * 5:
        return Move(square, STILL)

    return Move(square, random.choice((NORTH, WEST)))</code></pre>

    <div
            class="thumbnail center-block replay"
            data-replay-url="{% static "tournament/replays/580255-4192079766.hlt.gz" %}"
            data-replay-is-minimal="true"
            data-replay-max-height="500"></div>

    <h3>What's Next?</h3>
    <p>That's really up to you! How you improve your bot from here is where you step into the competition.</p>
    <p>That said, if you're looking for more ideas or a stronger starting base, read through <a
            href="{% url 'tournament:documentation' page_name="next_steps" %}">Next Steps</a> for a tutorial that walks you through
        improving your combat, piece management, and expansion.</p>
    <p>Good luck!</p>

{% endblock %}
