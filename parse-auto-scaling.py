TIMEZONE = 'Asia/Taipei'

TIME_AND_LIMIT = {'00:00': 320,
                  '01:00': 300,
                  '02:00': 280,
                  '02:30': 260,
                  '03:00': 240,
                  '03:30': 220,
                  '04:00': 200,
                  '04:30': 175,
                  '05:00': 150,
                  '08:00': 160,
                  '09:00': 190,
                  '12:00': 210,
                  '13:00': 220,
                  '17:00': 270,
                  '21:00': 280,
                  '22:00': 290,
                  '22:30': 300,
                  '23:00': 320}

###########################################################################

import getpass
import pytz
import requests
import sched
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def get_now():
    return datetime.now(pytz.timezone(TIMEZONE))


def get_limit(now):
    hour = now.hour
    minute = now.minute

    closest_time_in_minute = 9999
    closest_limit = None

    for t, l in TIME_AND_LIMIT.items():
        h, m = map(int, t.split(':'))
        d = (hour - h) * 60 + (minute - m)
        if d >= 0 and d < closest_time_in_minute:
            closest_time_in_minute = d
            closest_limit = l

    return closest_limit


def set_limit():
    global limit

    new_limit = get_limit(get_now())

    if new_limit and new_limit != limit:
        limit = new_limit

        for retry in range(5):
            try:
                with requests.Session() as s:
                    r = s.get('https://www.parse.com/login')
                    soup = BeautifulSoup(r.text, 'html.parser')
                    token = soup.find('input', {'name': 'authenticity_token'})['value']

                    payload = {'user_session[email]': PARSE_EMAIL,
                               'user_session[password]': PARSE_PASSWORD,
                               'authenticity_token': token}
                    s.post('https://www.parse.com/user_session', data=payload)

                    r = s.get('https://www.parse.com/account')
                    soup = BeautifulSoup(r.text, 'html.parser')
                    token = soup.find('meta', {'name': 'csrf-token'})['content']
                    headers = {'X-CSRF-Token': token}
                    s.put('https://www.parse.com/plans/' + PARSE_APP_ID + '?new_limit=' + str(limit), headers=headers)
            except ConnectionError as err:
                print('ConnectionError: ' + str(err) + ' - Retry... ' + retry)
                time.sleep(1)
            except TypeError as err:
                print('TypeError: ' + str(err) + ' - Retry... ' + retry)
                time.sleep(1)
            else:
                print(PARSE_APP_ID + ': ' + str(limit).rjust(3) + ' req/s (' + get_now().strftime('%Y-%m-%d %H:%M') + ')')
                break

    else:
        print(PARSE_APP_ID + ': ---       (' + get_now().strftime('%Y-%m-%d %H:%M') + ')')

    next_minute = (datetime.now() + timedelta(minutes=1)).replace(second=0)
    sc.enterabs(time.mktime(next_minute.timetuple()), 1, set_limit)



PARSE_APP_ID   = input('Parse App Id: ')
PARSE_EMAIL    = input('Parse E-mail: ')
PARSE_PASSWORD = getpass.getpass('Parse Password: ')


limit = None

sc = sched.scheduler(time.time, time.sleep)
sc.enter(0, 1, set_limit)
sc.run()
