{% extends "tournament/documentation/documentation.html" %}

{% block title %}Documentation - Bot Next Steps{% endblock %}

{% block docs %}
{% markdown %}

# So you've improved the RandomBot. Now what?

You've already read [Improving the Random Bot]({% url 'tournament:documentation' page_name="improve_random" %}) and you want
to know what to do next.

## Reduce Waste

Waste is unnecessary moves that don't improve your position and prevent you from maximizing your production each turn.

Some ways to reduce waste:

1. don't attack cells you can't defeat
2. don't move cells unless you have a use for them
3. don't move cells further than you have to
4. be careful of constantly moving cells over your high production areas or cells swapping repeatedly

### Stay still when you can't defeat a cell

The ImprovedBot took care of some waste over RandomBot by adding a rule about attacking a cell with
more strength than you, but it doesn't cover every situation.

If a cell is on the border, let's have it wait until it can attack successfully.

```python
def get_move(square):
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner != myID and neighbor.strength < square.strength:
            return Move(square, direction)

    if square.strength < square.production * 5:
        return Move(square, STILL)

    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))
    if not border:
        return Move(square, random.choice((NORTH, WEST)))
    else:
        # wait until we are strong enough to attack
        return Move(square, STILL)
```

{% replay "621660-1943320012.hlt.gz" %}

You can see that PatientBot, by staying still, is able to grow faster and defeat ImprovedBot.

### Move towards the border

Right now both PatientBot and ImprovedBot move in a northwesterly direction. In most games this
means that a lot of production and time is wasted moving from the southeast to the northwest.

Instead of moving randomly, let's move towards the nearest border.

```python
def find_nearest_enemy_direction(square):
    direction = NORTH
    # don't get stuck in an infinite loop
    max_distance = min(game_map.width, game_map.height) / 2
    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current = square
        
        while current.owner == myID and distance < max_distance:
            distance += 1
            current = game_map.get_target(current, d)
            
        if distance < max_distance:
            direction = d
            max_distance = distance
            
    return direction


def get_move(square):
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner != myID and neighbor.strength < square.strength:
            return Move(square, direction)

    if square.strength < square.production * 5:
        return Move(square, STILL)

    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))
    if not border:
        return Move(square, find_nearest_enemy_direction(square))
    else:
        # wait until we are strong enough to attack
        return Move(square, STILL)
```

{% replay "622076-1943320012.hlt.gz" %}

AmbiturnerBot has higher production and territory just by moving in all directions.

## Increase Growth Rate

Optimizing your growth rate is a great way to improve your standing in the rankings.
Early, mid, and late game growth are crucial to defeating strong bots.

### Early game growth

Early game growth is all about effectively using your resources to capture nearby valuable areas of
the map. But what does valuable mean? The visualizer does a good job helping you identify metrics
that may be valuable, namely *territory*, *production*, and *strength*.

The AmbiturnerBot optimizes for territory, usually capturing the lowest cost enemy cell it can.
This is good because territory is how you win games but raw territory doesn't necessarily help much
in the early game. Instead you probably want to optimize for production. Good early game production
will fuel your bot through the rest of the game.

```python
def get_move(square):
    target, direction = max(
        (
            (neighbor, direction)
            for direction, neighbor in enumerate(game_map.neighbors(square))
            if neighbor.owner != myID
        ),
        default=(None, None),
        key=lambda t: t[0].production,
    )
    
    if target is not None and target.strength < square.strength:
        return Move(square, direction)
    elif square.strength < square.production * 5:
        return Move(square, STILL)

    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))
    if not border:
        return Move(square, find_nearest_enemy_direction(square))
    else:
        # wait until we are strong enough to attack
        return Move(square, STILL)
```

{% replay "622688-3808448360.hlt.gz" %}

But wait! ProductionBot lost! I thought you said production was good!?

#### Picking a heuristic

Production is good, but you can't focus on *just* production. AmbiturnerBot is winning because it
uses a better heuristic.

How can we improve ProductionBot to start winning?

```python
def heuristic(square):
    return square.production / square.strength if square.strength else square.production


def get_move(square):
    target, direction = max(
        (
            (neighbor, direction)
            for direction, neighbor in enumerate(game_map.neighbors(square))
            if neighbor.owner != myID
        ),
        default=(None, None),
        key=lambda t: heuristic(t[0]),
    )

    if target is not None and target.strength < square.strength:
        return Move(square, direction)
    elif square.strength < square.production * 5:
        return Move(square, STILL)

    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))
    if not border:
        return Move(square, find_nearest_enemy_direction(square))
    else:
        # wait until we are strong enough to attack
        return Move(square, STILL)
```

{% replay "623838-1388988469.hlt.gz" %}

## Take *Overkill* Into Account

Combat is a huge part of Halite, and being bad at it can ruin an otherwise good bot.

One of the crucial things to know about combat is
[overkill]({% url 'tournament:documentation' page_name="game_rules" %}#overkill)

> each piece decreases the strength of every adjacent or coinciding opposing piece by its own strength

Let's update our heuristic to take overkill into account.

```python
def heuristic(square):
    if square.owner == 0 and square.strength > 0:
        return square.production / square.strength
    else:
        # return total potential damage caused by overkill when attacking this square
        return sum(
            neighbor.strength
            for neighbor in game_map.neighbors(square)
            if neighbor.owner not in (0, myID)
        )
```

{% replay "624279-1175499152.hlt.gz" %}

You'll notice that both bots behave almost identically until they start to fight, then OverkillBot
takes DiscerningBot apart!

## Next Steps

This is a pretty good start for our bot. More things to think about are:

### Combining cells to attack sooner

Our bot spends a lot of time with cells at the border that are just waiting until
they have enough strength to attack an enemy. What if we combined some of them
together to attack sooner?

### Moving inner cells to higher value border areas

Right now we move every cell to its nearest border, but what if the nearest border
isn't particularly valuable? We should find ways to direct those resources towards
valuable parts of the map.

### Avoid combining cells together that exceed 255 strength

Ensure that strength is not lost to the 255 cap. OverkillBot loses a lot of strength (especially
when routing pieces) to combining pieces whose strengths sum to over 255. Avoiding this could make
a big difference.

One additional detail about the 255 cap - the cap applies before combat occurs so if 2 200 strength
cells attack one 220 strength cell in the same turn, the resulting cell will have 35 strength,
not 180 strength.

## Watch your bot and other bots compete

Look for inefficiencies in your playstyle. Look for ways to improve your heuristic. Take past and
future moves into account.

Check out [halint](https://github.com/erdman/halint) to process your replays and get feedback about ways to improve.

**May the best bot win!**

{% endmarkdown %}
{% endblock %}
