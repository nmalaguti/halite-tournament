$(() => {
    const loadReplay = async ($elem) => {
        const replayUrl = $elem.data("replay-url")
        const isMinimal = !!$elem.data("replay-is-minimal")
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
                const text = await response.text()
                showGame(textToGame(text), $elem, {
                    showmovement: true,
                    isminimal: isMinimal,
                })
            }
        }
    }

    $("div[data-replay-url]").each((i, elem) => {
        loadReplay($(elem))
    })
})
