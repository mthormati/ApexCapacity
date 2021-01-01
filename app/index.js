fetch('http://localhost:8080/')
.then(response => response.text())
.then(data => {
    const dataByLine = data.split('\n').filter(line => line.length > 0)

    var dataByDay = new Array(7)
    for (var i = 0; i < dataByLine.length; i++) {
        const dataInLine = dataByLine[i].split(' ')
        const dayOfWeek = dataInLine[0]
        const time = dataInLine[1]
        if (time < '10:00' || time > '22:30') continue
        if (!dataByDay[dayOfWeek]) {
            dataByDay[dayOfWeek] = []
        }
        dataByDay[dayOfWeek].push(new DataPoint(dataInLine[1], dataInLine[5], dataInLine[4]))
    }
    for (var i = 0; i < dataByDay.length; i++) {
        dataByDay[i].sort((a, b) => {
            if (a.time < b.time) return -1
            if (a.time > b.time) return 1
            return 0
        })
    }

    const allCtx = document.querySelectorAll('canvas')
    for (var i = 0; i < allCtx.length; i++) {
        const dayOfWeek = allCtx[i].id
        const labels = dataByDay[i].map(dataPoint => dataPoint.time)
        const mostRecents = dataByDay[i].map(dataPoint => dataPoint.mostRecent)
        const averages = dataByDay[i].map(dataPoint => dataPoint.average)
        const myChart = new Chart(allCtx[i], {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Most Recent',
                    data: mostRecents,
                    borderColor: ['rgba(54, 162, 235, 1)'],
                    borderWidth: 2,
                    fill: false
                },{
                    label: 'Average',
                    data: averages,
                    borderColor: ['rgba(255, 206, 86, 1)'],
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                responsive: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                title: {
                    display: true,
                    text: dayOfWeek
                }
            }
        })
    }    
})

class DataPoint {
    constructor(time, mostRecent, average) {
        this.time = time
        this.mostRecent = mostRecent
        this.average = average
    }
}
