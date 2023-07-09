{% extends "tournament/documentation/documentation.html" %}

{% block title %}Documentation - Bot Next Steps{% endblock %}

{% block docs %}

    <h1>So you've improved the RandomBot. Now what?</h1>

    You've already read <a href="{% url 'tournament:documentation' page_name="improve_random" %}">Improving the Random Bot</a> and you want
    to know what to do next.

    <h2>Reduce Waste</h2>

    <p>Waste is unnecessary moves that don't improve your position and prevent you from maximizing your production each turn.</p>

    <p>Some ways to reduce waste:</p>

    <ol>
        <li>don't attack cells you can't defeat</li>
        <li>don't move cells unless you have a use for them</li>
        <li>don't move cells further than you have to</li>
        <li>be careful of constantly moving cells over your high production areas <br>or cells swapping repeatedly</li>
    </ol>

    <h3>Stay still when you can't defeat a cell</h3>

    <p>The Improved Bot took care of some waste over RandomBot by adding a rule about attacking a cell with more strength than you, but it doesn't cover every situation.</p>

    <p>If a cell is on the border, let's have it wait until it can attack successfully.</p>

    <pre><code class="lang-javascript">function move(loc) {
    const site = gameMap.getSite(loc);
    let border = false;

    for (let d of CARDINALS) {
        const neighborSite = gameMap.getSite(loc, d);
        if (neighborSite.owner != id) {
            border = true;
            if (neighborSite.strength &lt; site.strength) {
                return new Move(loc, d);
            }
        }
    }

    if (site.strength &lt; (site.production * 5)) {
        return new Move(loc, STILL);
    }

    // if the cell isn't on the border
    if (!border) {
        return new Move(loc, Math.random() &gt; 0.5 ? NORTH : WEST);
    }

    // otherwise wait until you can attack
    return new Move(loc, STILL);
}</code></pre>

    <p><a href="https://web.archive.org/web/20161210080437/https://nmalaguti.github.io/halite-visualizer/?url=https%3A%2F%2Fdl.dropboxusercontent.com%2Fu%2F57961%2F114761-1943320012.hlt" rel="nofollow">Watch ImproveBot vs PatientBot</a></p>

    <p>You can see that PatientBot, by staying still, is able to grow faster and defeat ImproveBot.</p>

    <h3>Move towards the border</h3>

    <p>Right now both Patient Bot and Improve Bot move in a northwesterly direction. In most games this means that a lot of production and time is wasted moving from the southeast to the northwest.</p>

    <p>Instead of moving randomly, let's move towards the nearest border.</p>

    <pre><code class="lang-javascript">function findNearestEnemyDirection(loc) {
    let direction = NORTH;
    // don't get stuck in an infinite loop
    let maxDistance = Math.min(gameMap.width, gameMap.height) / 2;

    for (let d of CARDINALS) {
        let distance = 0;
        let current = loc;
        let site = gameMap.getSite(current, d);
        while (site.owner == id &amp;&amp; distance &lt; maxDistance) {
            distance++;
            current = gameMap.getLocation(current, d);
            site = gameMap.getSite(current);
        }

        if (distance &lt; maxDistance) {
            direction = d;
            maxDistance = distance;
        }
    }

    return direction;
}

function move(loc) {
    const site = gameMap.getSite(loc);
    let border = false;

    for (let d of CARDINALS) {
        const neighborSite = gameMap.getSite(loc, d);
        if (neighborSite.owner != id) {
            border = true;
            if (neighborSite.strength &lt; site.strength) {
                return new Move(loc, d);
            }
        }
    }

    if (site.strength &lt; (site.production * 5)) {
        return new Move(loc, STILL);
    }

    // if the cell isn't on the border
    if (!border) {
        return new Move(loc, findNearestEnemyDirection(loc));
    }

    // otherwise wait until you can attack
    return new Move(loc, STILL);
}</code></pre>

    <p><a href="https://web.archive.org/web/20161210080437/https://nmalaguti.github.io/halite-visualizer/?url=https%3A%2F%2Fdl.dropboxusercontent.com%2Fu%2F57961%2F115537-2843744213.hlt" rel="nofollow">Watch AmbiturnerBot vs PatientBot</a></p>

    <p>AmbiturnerBot has higher production and territory just by moving in all directions. <a href="https://www.youtube.com/watch?v=8hJ1HDcMowk">Derek Zoolander would be jealous</a>.</p>

    <h2>Increase Growth Rate</h2>

    <p>Optimizing your growth rate is a great way to improve your standing in the rankings. Early, mid, and late game growth are crucial to defeating strong bots.</p>

    <h3>Early game growth</h3>

    <p>Early game growth is all about effectively using your resources to capture nearby valuable areas of the map. But what does valuable mean? The visualizer does a good job helping you identify metrics that may be valuable, namely <em>territory</em>, <em>production</em>, and <em>strength</em>.</p>

    <p>The AmbiturnerBot optimizes for territory, usually capturing the lowest cost enemy cell it can. This is good because territory is how you win games but raw territory doesn't necessarily help much in the early game. Instead you probably want to optimize for production. Good early game production will fuel your bot through the rest of the game.</p>

    <pre><code class="lang-javascript">// I've taken a dependency on lodash https://lodash.com
function move(loc) {
    const site = gameMap.getSite(loc);

    const target = _.chain(CARDINALS)
        .map((direction) =&gt; ({
            direction,
            site: gameMap.getSite(loc, direction)
        }))
        // only enemy cells
        .filter((cell) =&gt; cell.site.owner !== id)
        // sort by production descending
        .orderBy([(cell) =&gt; cell.site.production], ['desc'])
        .first()
        .value();

    if (target &amp;&amp; target.site.strength &lt; site.strength) {
        return new Move(loc, target.direction);
    }

    if (site.strength &lt; (site.production * 5)) {
        return new Move(loc, STILL);
    }

    // if the cell isn't on the border
    if (CARDINALS.every((d) =&gt; gameMap.getSite(loc, d).owner === id)) {
        return new Move(loc, findNearestEnemyDirection(loc));
    }

    // otherwise wait until you can attack
    return new Move(loc, STILL);
}</code></pre>

    <p><a href="https://web.archive.org/web/20161210080437/https://nmalaguti.github.io/halite-visualizer/?url=https%3A%2F%2Fdl.dropboxusercontent.com%2Fu%2F57961%2F116501-3808448360.hlt" rel="nofollow">Watch AmbiturnerBot vs ProductionBot</a></p>

    <p>But wait! ProductionBot lost! I thought you said production was good!?</p>

    <h4>Picking a heuristic</h4>

    <p>Production is good, but you can't focus on <em>just</em> production. AmbiturnerBot is winning because it uses a better heuristic.</p>

    <p>How can we improve ProductionBot to start winning?</p>

    <p></p><pre><code class="lang-javascript">function heuristic(site) {
    return site.production / site.strength;
}

function move(loc) {
    const site = gameMap.getSite(loc);

    const target = _.chain(CARDINALS)
        .map((direction) =&gt; ({
            direction,
            site: gameMap.getSite(loc, direction)
        }))
        // only enemy cells
        .filter((cell) =&gt; cell.site.owner !== id)
        // sort by heuristic descending
        .orderBy([(cell) =&gt; heuristic(cell.site)], ['desc'])
        .first()
        .value();

    if (target &amp;&amp; target.site.strength &lt; site.strength) {
        return new Move(loc, target.direction);
    }

    if (site.strength &lt; (site.production * 5)) {
        return new Move(loc, STILL);
    }

    // if the cell isn't on the border
    if (CARDINALS.every((d) =&gt; gameMap.getSite(loc, d).owner === id)) {
        return new Move(loc, findNearestEnemyDirection(loc));
    }

    // otherwise wait until you can attack
    return new Move(loc, STILL);
}</code></pre>

    <p><a href="https://web.archive.org/web/20161210080437/https://nmalaguti.github.io/halite-visualizer/?url=https%3A%2F%2Fdl.dropboxusercontent.com%2Fu%2F57961%2F117723-735321296.hlt" rel="nofollow">Watch AmbiturnerBot vs DiscerningBot</a></p>

    <p>Well, DiscerningBot still lost, but it <em>was</em> leading in the beginning. Once it made contact with the enemy though, it looks like it just ran away!</p>

    <p>We have a bug! When strength is 0 (like after enemies fight) our heuristic will make the value Infinity! Let's fix that.</p>

    <pre><code class="lang-javascript">function heuristic(site) {
    if (site.strength) {
        return site.production / site.strength;
    } else {
        return site.production;
    }
}</code></pre>

    <p><a href="https://web.archive.org/web/20161210080437/https://nmalaguti.github.io/halite-visualizer/?url=https%3A%2F%2Fdl.dropboxusercontent.com%2Fu%2F57961%2F118377-1388988469.hlt" rel="nofollow">Watch AmbiturnerBot vs DiscerningBot - Round 2</a></p>

    <p>Whoo! DiscerningBot has started winning!</p>

    <h2>Take <em>Overkill</em> Into Account</h2>

    <p>Combat is a huge part of Halite, and as we just saw, being bad at it can ruin an otherwise good bot.</p>

    <p>One of the crucial things to know about combat is <a href="{% url 'tournament:documentation' page_name="game_rules" %}#overkill">overkill</a>:</p>

    <blockquote><p>each piece decreases the strength of every adjacent or coinciding opposing piece by its own strength</p></blockquote>

    <p>Let's update our heuristic to take overkill into account.</p>

    <pre><code class="lang-javascript">function heuristic(cell) {
    if (cell.site.owner === 0 &amp;&amp; cell.site.strength &gt; 0) {
        return cell.site.production / cell.site.strength;
    } else {
        // attacking an enemy
        let totalDamage = 0;
        for (let d of CARDINALS) {
            let site = gameMap.getSite(cell.loc, d);
            if (site.owner !== 0 &amp;&amp; site.owner !== id) {
                totalDamage += site.strength;
            }
        }

        return totalDamage;
    }
}

function move(loc) {
    const site = gameMap.getSite(loc);

    const target = _.chain(CARDINALS)
        .map((direction) =&gt; ({
            direction,
            loc: gameMap.getLocation(loc, direction),
            site: gameMap.getSite(loc, direction)
        }))
        // only enemy cells
        .filter((cell) =&gt; cell.site.owner !== id)
        // sort by production descending
        .orderBy([(cell) =&gt; heuristic(cell)], ['desc'])
        .first()
        .value();

    if (target &amp;&amp; target.site.strength &lt; site.strength) {
        return new Move(loc, target.direction);
    }

    if (site.strength &lt; (site.production * 5)) {
        return new Move(loc, STILL);
    }

    // if the cell isn't on the border
    if (CARDINALS.every((d) =&gt; gameMap.getSite(loc, d).owner === id)) {
        return new Move(loc, findNearestEnemyDirection(loc));
    }

    // otherwise wait until you can attack
    return new Move(loc, STILL);
}</code></pre>

    <p><a href="https://web.archive.org/web/20161210080437/https://nmalaguti.github.io/halite-visualizer/?url=https%3A%2F%2Fdl.dropboxusercontent.com%2Fu%2F57961%2F120916-1175499152.hlt" rel="nofollow">Watch OverkillBot vs DiscerningBot</a></p>

    <p>You'll notice that both bots behave almost identically until they start to fight, then OverkillBot takes DiscerningBot apart!</p>

    <h2>Next Steps</h2>

    <p>This is a pretty good start for our bot. More things to think about are:</p>

    <h3>Combining cells to attack sooner</h3>

    <p>Our bot spends a lot of time with cells at the border that are just waiting until they have enough strength to attack an enemy. What if we combined some of them together to attack sooner?</p>

    <h3>Moving inner cells to higher value border areas</h3>

    <p>Right now we move every cell to its nearest border, but what if the nearest border isn't particularly valuable? We should find ways to direct those resources towards valuable parts of the map.</p>

    <h3>Avoid combining cells together that exceed 255 strength</h3>

    <p>Ensure that strength is not lost to the 255 cap. OverkillBot loses a lot of strength (especially when routing pieces) to combining pieces whose strengths sum to over 255. Avoiding this could make a big difference.</p>

    <p>One additional detail about the 255 cap - the cap applies before combat occurs so if 2 200 strength cells attack one 220 strength cell in the same turn, the resulting cell will have 35 strength, not 180 strength.</p>

    <h2>Watch your bot and other bots compete</h2>

    <p>Look for inefficiencies in your playstyle. Look for ways to improve your heuristic. Take past and future moves into account.</p>

    <p>Check out <a href="https://github.com/erdman/halint">halint</a> to process your replays and get feedback about ways to improve.</p>

    <p><a href="https://web.archive.org/web/20161210080437/https://nmalaguti.github.io/halite-visualizer/?url=https%3A%2F%2Fdl.dropboxusercontent.com%2Fu%2F57961%2F131612-3893351690.hlt" rel="nofollow">Bonus: watch all 6 bots compete</a></p>

    <p><strong>May the best bot win!</strong></p>

{% endblock %}
