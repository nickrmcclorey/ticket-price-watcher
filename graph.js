let eventDate = document.getElementById('event_date')
let eventTitle = document.getElementById('event_title')

function loadTicketGraph() {
    fetch('/ticketFiles/e_3684275.json')
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

loadTicketGraph()