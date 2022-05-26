
function createGraph(game) {
    df = new dfd.DataFrame(game.ticketPriceHistory)
    
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

    let eventDate = document.getElementById('event_date')
    let eventTitle = document.getElementById('event_title')
    let gameTime = new Date(game.date)
    eventDate.textContent = gameTime.toDateString() + ' at ' + gameTime.toLocaleTimeString([], {hour: 'numeric', minute: '2-digit'})
    eventTitle.textContent = game.title
}

function loadGames() {
    fetch('/ticketFiles_map.json')
        .then(response => response.json())
        .then((teams) => {
            let select = document.getElementById('teamSelect')
            for (let team in teams) {
                let option = document.createElement('option')
                option.value = team
                option.textContent = team
                select.appendChild(option)
            }

            select.onchange = loadGamesForTeam
        })
}

function loadGamesForTeam(event) {
    let teamName = event.srcElement.value;
    let ul = document.getElementById('gameList')
    ul.innerHTML = ''

    fetch('/ticketFiles/' + teamName + '.json')
        .then(response => response.json())
        .then(team => {
            let innerHTML = '<div><h2>' + teamName + '</h2><ul>'

            let ids = organizeGameIds(team.games)
            for (let gameId of ids) {
                let game = team.games[gameId]
                let li = document.createElement('li')
                li.textContent = new Date(game.date).toDateString() + ' ' + game.title
                li.addEventListener('click', () => createGraph(game))
                ul.appendChild(li)
            }
        })
}

function organizeGameIds(games) {
    let ids = Object.keys(games)
    let chronologicalIds = []
    while (ids.length > 0) {
        let earliestGameId = ids[0]
        let earliestGameTime = new Date(games[earliestGameId].date)
        for (let id of ids) {
            let thisGameTime = new Date(games[id].date)
            if (thisGameTime < earliestGameTime) {
                earliestGameTime = thisGameTime
                earliestGameId = id
            }
        }
    
        chronologicalIds.push(earliestGameId)
        console.log(earliestGameId)
        ids = ids.filter(x => x != earliestGameId)
    }
    return chronologicalIds
}

loadGames()
