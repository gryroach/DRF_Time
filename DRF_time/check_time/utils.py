import datetime
import requests
from dateutil import parser

# url world time API
url = 'http://worldtimeapi.org/api/timezone/Europe/Moscow/'


def check_time_by_global(serializer, delta=False):
    response_datetime = parser.parse(requests.request("GET", url).json()['datetime'])
    if delta:
        delta = datetime.timedelta(hours=int(serializer.data.get('delta').split(':')[0]),
                                   minutes=int(serializer.data.get('delta').split(':')[1]),
                                   seconds=int(serializer.data.get('delta').split(':')[2]))
        input_time = datetime.datetime(year=response_datetime.year, month=response_datetime.month,
                                       day=response_datetime.day,
                                       hour=int(serializer.data.get('time').split(':')[0]),
                                       minute=int(serializer.data.get('time').split(':')[1]),
                                       second=int(serializer.data.get('time').split(':')[2]))
        return abs(response_datetime.timestamp() - input_time.timestamp()) <= delta.total_seconds()
    else:
        return serializer.data.get('time') == response_datetime.strftime("%H:%M")
