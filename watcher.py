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

# Stores ticket prices in file for future reference
def updateTicketFile(event, filePath):
    newPrice = {
        'date': str(datetime.now()),
        'minPrice': event['minPrice']
    }

    # if event has previously recorded data, we load that in
    if os.path.exists(filePath):
        with open(filePath, 'r') as file:
            event = json.load(file)
    else:
        event['minPriceHistory'] = []

    event['minPriceHistory'].append(newPrice)

    with open(filePath, 'w') as file:
        json.dump(event, file)
    



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
            eventMap[performerId] = {
                'team': teamName,
                'games': []
            }

        for event in events:
            filePath = 'ticketFiles/' + teamName + '/e_' + str(event['id']) + '.json'
            dirPath = os.path.dirname(filePath)

            if not os.path.exists(dirPath):
                os.mkdir(dirPath)

            updateTicketFile(event, filePath)
            eventMap[performerId]['games'].append(event['id'])

    with open('ticketFiles_map.json', 'w') as file:
        json.dump(eventMap, file)
