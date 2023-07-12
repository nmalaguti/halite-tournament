$(() => {
    const loadReplay = async ($elem) => {
        const replayUrl = $elem.data("replay-url")
        const isMinimal = !!$elem.data("replay-is-minimal")
        const maxHeight = $elem.data("replay-max-height")
        if (replayUrl) {
            if (!isMinimal) {
                $elem.html(`<h1><span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span> Downloading replay...</h1>`);
            }
            const response = await fetch(replayUrl)
            if (!response.ok) {
                if (!isMinimal) {
                    $elem.html(`<h1>Replay <a href="${replayUrl}">${replayUrl}</a> failed to download!</h1>`);
                }
            } else {
                if (!isMinimal) {
                    $elem.html(`<h1><span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span> Preparing replay...</h1>`);
                }
                let data = await response.arrayBuffer()
                let text
                try {
                    text = pako.inflate(data, {to: 'string'});
                } catch (err) {
                    text = new TextDecoder().decode(data);
                }
                try {
                    showGame(textToGame(text), $elem, {
                        showmovement: true,
                        isminimal: isMinimal,
                        maxHeight: maxHeight,
                        replayUrl: replayUrl,
                    })
                } catch (err) {
                    if (!isMinimal) {
                        $elem.html(`<h1>Replay <a href="${replayUrl}">${replayUrl}</a> failed to parse! ${err}</h1>`);
                    }
                }

            }
        }
    }

    $("div[data-replay-url]").each((i, elem) => {
        loadReplay($(elem))
    })
})
