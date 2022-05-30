from datetime import datetime
import requests
import json
import os

# return array of events with info such as lowest ticket price
def getVividLowestPrices(performerId):
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }) # Vivid returns 403 Forbidden without these headers

    url = 'https://www.vividseats.com/hermes/api/v1/productions?pageSize=50&performerId=' + str(performerId)
    response = s.get(url)
    if response.status_code != 200:
        print('Failed to get content at url:', url)
        exit(1)

    j = json.loads(response.content.decode('utf-8'))

    return j['items']
    
def updateTeamFile(events, teamName, teamId):
    output = {
        'teamName': teamName,
        'games': {}
    }

    if os.path.exists('ticketFiles/' + teamName + '.json'):
        with open('ticketFiles/' + teamName + '.json', 'r') as file:
            g = json.load(file)
            output['games'] = g['games']
    
    for event in events:
        gameId = str(event['id'])
        outputGame = {
            'date': event['utcDate'],
            'venue': event['venue']['name'],
            'title': event['name'],
            'ticketPriceHistory': []
        }

        if gameId in output['games']:
            outputGame['ticketPriceHistory'] = output['games'][gameId]['ticketPriceHistory']
        priceHistory = outputGame['ticketPriceHistory']

        if len(priceHistory) > 2 and priceHistory[-1]['minPrice'] == priceHistory[-2]['minPrice']:
            priceHistory[-1]['date'] = str(datetime.now())
        else:
            priceHistory.append({
                'date': str(datetime.now()),
                'minPrice': event['minPrice']
            })

    with open('ticketFiles/' + teamName + '.json', 'w') as file:
        json.dump(output, file)


if __name__ == '__main__':
    events = []
    performerIds = {
        "lions": 238,
        "reds": 173,
        "bengals": 172
    }

    eventMap = {}
    if os.path.exists('ticketFiles_map.json'):
        with open('ticketFiles_map.json', 'r') as file:
            eventMap = json.loads(file.read())

    for teamName, performerId in performerIds.items():
        events = getVividLowestPrices(performerId)

        if performerId not in eventMap:
            eventMap[teamName] = performerId

        updateTeamFile(events, teamName, str(performerId))

    with open('ticketFiles_map.json', 'w') as file:
        json.dump(eventMap, file)
