#!/usr/bin/env python
from collections import defaultdict
from flask import Flask, render_template
from icalendar import Calendar
import requests
from datetime import datetime
import pytz
from itertools import groupby
from operator import itemgetter
import configparser
import os

app = Flask(__name__)

def read_config(ini_file):
    if not os.path.exists(ini_file):
        raise FileNotFoundError(f"The configuration file {ini_file} does not exist.")

    config = configparser.ConfigParser()
    config.read(ini_file)

    return config

# URL of the .ics file
config = read_config('/etc/caltab-conf/config.ini')
ICS_URL = config['Calendar']['url']


def fetch_calendar(url):
    # Fetch the .ics file
    r = requests.get(url)
    # Parse the .ics file
    cal = Calendar.from_ical(r.text)
    return cal

def organize_events_by_week(cal):
    # Get the current time in UTC
    now = datetime.now(pytz.utc)

    # First, filter out past events and sort the remaining ones
    future_events = [
        {
            'summary': str(component.get('summary')),
            'location': str(component.get('location')),
            'start': component.get('dtstart').dt,
            'end': component.get('dtend').dt,
        }
        for component in cal.walk('vevent')
        if component.get('dtend').dt > now  # filter out past events
    ]
    future_events.sort(key=lambda x: (x['start'].isocalendar()[1], x['start']))

    # Now group by week and then by day within each week
    events_by_week = defaultdict(lambda: defaultdict(list))
    for week, events in groupby(future_events, key=lambda x: x['start'].isocalendar()[1]):
        for event in events:
            day = event['start'].date()
            events_by_week[week][day].append(event)

    # Sort the days within the weeks
    for week, days in events_by_week.items():
        events_by_week[week] = dict(sorted(days.items()))

    return dict(sorted(events_by_week.items()))

@app.route('/')
def calendar_view():
    cal = fetch_calendar(ICS_URL)
    events_by_week = organize_events_by_week(cal)
    # Sort weeks
    sorted_weeks = sorted(events_by_week.keys())
    return render_template('calendar.html', events_by_week=events_by_week, sorted_weeks=sorted_weeks)

if __name__ == '__main__':
    app.run(debug=True)

