let eventDate = document.getElementById('event_date')
let eventTitle = document.getElementById('event_title')

function loadTicketGraph(event) {
    fetch('/ticketFiles/reds/e_' + event.target.textContent + '.json')
        .then(response => response.json())
        .then(createGraph);
}

function createGraph(ticket) {
    df = new dfd.DataFrame(ticket.minPriceHistory)

    const layout = {
        title: 'Min Ticket Price',
        xaxis: {
            title: 'Date'
        },
        yaxis: {
            title: "Price in Dollars"
        }
    }

    const config = {
        columns: ['minPrice']
    }

    const new_df = df.setIndex({column: 'date'})
    new_df.plot("graph").line({config, layout})
    console.log(ticket)
    eventDate.textContent = new Date(ticket.utcDate).toLocaleString()
    eventTitle.textContent = ticket.name
}

function loadGames() {
    fetch('/ticketFiles_map.json')
        .then(response => response.json())
        .then(buildGameList)
}

function buildGameList(teamsData) {
    // console.log(teamsData)
    let gameDiv = document.getElementById('gameList')
    let innerHTML = '';
    for (teamId in teamsData) {
        let teamName = teamsData[teamId].team
        let gameIds = teamsData[teamId].games
        
        innerHTML += '<div><h2>' + teamName + '</h2><ul>'
        for (gameId of gameIds) {
            innerHTML += '<li>' + gameId + "</li>"
        }
        innerHTML += '</ul></div>'
    }
    gameDiv.innerHTML = innerHTML

    for (let element of document.getElementsByTagName('li')) {
        element.addEventListener('click', loadTicketGraph, false)
    }
}

loadGames()

