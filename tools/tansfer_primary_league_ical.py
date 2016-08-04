# coding: utf-8

import os
import json
import pytz
import traceback
from datetime import datetime, timedelta
from icalendar import Calendar, Event

SOURCE_PATH = 'source/pl/2017'
DEST_PATH = 'static/calendars/pl/2017'

def parse(path):
    with open(path) as f:
        data = json.loads(f.read())
        contents = data['content']
        for content in contents:
            dt = (content['kickoff'].get('label', '')
                  .replace('BST', '+0100')
                  .replace('GMT', '+0000'))
            if not dt:
                continue
            else:
                # sample: Tue 4 Apr 2017, 19:45 Etc/GMT+1
                dt_str = (' ').join(dt.strip().split(' ')[1:])
                try:
                    dt = datetime.strptime(dt_str, '%d %b %Y, %H:%M %z')
                except:
                    continue

            teams = content['teams']
            team_1 = teams[0]['team']['name']
            team_2 = teams[1]['team']['name']
            loc = content['ground']['name']
            city = content['ground']['city']
            yield (team_1, team_2,
                   dt.astimezone(pytz.timezone('UTC')),
                   loc, city)

def tansfer(path):
    cal = Calendar()

    for t1, t2, dt, loc, city in parse(path):
        event = Event()
        event['SUMMARY'] = '%s vs %s' % (t1, t2)
        event['DTSTART'] = dt
        event['DTEND'] = dt + timedelta(hours=2)
        event['LOCATION'] = '%s, %s' % (loc, city)
        cal.add_component(event)
    file_name = path.split('/')[-1].split('.')[0] + '.ics'
    dest = os.path.join(DEST_PATH, file_name.replace(' ', '_'))
    with open(dest, 'wb') as f:
        f.write(cal.to_ical())

if __name__ == '__main__':
    for file_name in os.listdir(SOURCE_PATH):
        tansfer(os.path.join(SOURCE_PATH, file_name))
