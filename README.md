# Ticket Watcher
This project monitors ticket prices using an api from vivid seats and compiles this data over time for analysis

## Technical overview
This project consists of two peices:
- a python script (watcher.py) that collects data
- a web page to browse and display the data
In addition, the python script must be ran at a regular interval. I'm currently using a cron job to do this

## Running the project
Python3 and a web browser are the only dependencies

Run `python3 watcher.py` at regular intervals to collect data. Current teams to collect data from are listed in the `performerIds` dictionary in `watcher.py`

Run `python3 -m http.server` to set up a local web server and navigate to [localhost:8000](localhost:8000)
