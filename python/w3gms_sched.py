#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from ics import Calendar, Event
import datetime
import pytz

re_year = re.compile( '<span.+>(\d{4})<.*/span>' )
re_night = re.compile( '.+(January|Febuary|March|April|May|June|July|August|September|October|November|Decemeber)\s+(\d+).+[^a-zA-Z]+([a-zA-Z]{1,2}\d[a-zA-Z]+).+' )

months = {
    'January': 1, 'Febuary': 2, 'March': 3,
    'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9,
    'October': 10, 'November': 11, 'Decemeber': 12
}

location = 'Parksburg, PA (146.985Mhz PL 100hz)'
ics_file = '/working/htdocs/w3gms.ics'
debug = False

sched = [
    {
        'schedule': 'https://w3gmsrepeater.com/workbench-host-schedule/',
        'url': 'https://w3gmsrepeater.com/the-workbench-net/',
        'desc': 'Amateur Radio round table focusing on technical discussion. Bring your questions and have the elmers on the w3gms repeater lend a hand. Newcomers are strongly encouraged to join the net. No question is too simple.',
        'summary': 'Workbench with: ',
        'start_hour': 20,
        'start_minute': 0,
        'end_hour': 21,
        'end_minute': 0,
    },
    {
        'schedule': 'https://w3gmsrepeater.com/round-table-host-sked/',
        'url': 'https://w3gmsrepeater.com/985-thursday-night-round-table/',
        'desc': 'Join us every Thursday evening at 8:30pm for a Round Table qso.  This is an informal round table type QSO.  Any topic can be discussed and brought up by anyone participating.  We are looking for volunteers to take a turn hosting the weekly round table.  New check ins are always welcome and encouraged.  This is a place and time to come together and further the hobby.',
        'summary': 'Thursday RT with: ',
        'start_hour': 20,
        'start_minute': 30,
        'end_hour': 22,
        'end_minute': 0,
    }
]

# function to pull and parse the schedule webpage
def pull_schedule(url_schedule, desc, url_desc, summary, start_hour, start_minute, end_hour, end_minute):
    
    sch_list = []
    sch_dict = {}
    
    req = Request(url_schedule)
    html_page = urlopen(req)

    soup = BeautifulSoup(html_page, "html")

    year = ''
    for link in soup.findAll( ['span', 'p'] ): # they don't always use the 'span' tag
        str_link = str(link)
        if re_year.match( str_link ):
            year = re_year.sub('\\1', str_link)
        elif re_night.match( str_link ):
            day = re_night.sub('\\2', str_link)
            callsign = re_night.sub('\\3', str_link).lower()
            d = {
                'year': int(year),
                'month': months[re_night.sub('\\1', str_link)],
                'day': int(day),
                'callsign': callsign,
                'desc': desc,
                'url': url_desc,
                'name': summary + callsign,
                'start_hour': start_hour,
                'start_minute': start_minute,
                'end_hour': end_hour,
                'end_minute': end_minute,
            }
            # don't want dups so storing in dict with string based key
            key = str(d['year']) + str(d['month']) + str(d['day'])
            sch_dict[ key ] = d

    # converting dict contents to a list for farther consumption
    sch_list = list( sch_dict.values() )
    return sch_list

# pull the data for each item in the configuration
rt_list = []
for c in sched:
    rt_list.extend( pull_schedule( c['schedule'] , c['desc'], c['url'], c['summary'], c['start_hour'], c['start_minute'], c['end_hour'], c['end_minute'] ) )


# take the calendar items and build an ical object then write it out to the file
cal = Calendar()

i=1
for rt in rt_list:
    e = Event()
    e.name = rt['name']
    e.begin = datetime.datetime(rt['year'], rt['month'], rt['day'], rt['start_hour'], rt['start_minute'], 0, tzinfo=pytz.timezone('US/Eastern'))
    e.end = datetime.datetime(rt['year'], rt['month'], rt['day'], rt['end_hour'], rt['end_minute'], 0, tzinfo=pytz.timezone('US/Eastern'))
    e.location = location
    e.url = rt['url']
    e.description = rt['desc']
    e.organizer = 'bob@ruddy.net'
    if i == 1:
        cal.events.add(e)
    if debug:
        i += 1

with open(ics_file, 'w') as my_file:
    my_file.writelines(cal)

