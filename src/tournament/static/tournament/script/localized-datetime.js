const DateTime = luxon.DateTime
$(() => {
    $("span[data-date-time]").each((i, elem) => {
        const datetime = DateTime.fromISO($(elem).data("date-time"))
        const date = datetime.toLocaleString({
            ...DateTime.DATE_SHORT,
            month: '2-digit',
            day: '2-digit',
        })
        const time = datetime.toLocaleString({
            ...DateTime.TIME_WITH_SHORT_OFFSET,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
        })
        $(elem).text(`${date} ${time}`)
    })
})
