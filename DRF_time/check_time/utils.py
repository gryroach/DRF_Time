import datetime
import requests
from dateutil import parser
from django.http import HttpResponseBadRequest

# url world time API
url = 'http://worldtimeapi.org/api/timezone/Europe/Moscow/'


def download_time(path):
    try:
        return parser.parse(requests.request("GET", path).json()['datetime'])
    except requests.exceptions.ConnectionError:
        return HttpResponseBadRequest("The time server is not responded.")
    except KeyError:
        return HttpResponseBadRequest("The time server address is not valid.")


def check_time_by_global(serializer, delta=None):
    response_datetime = download_time(url)
    if isinstance(response_datetime, datetime.datetime):
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
    else:
        return str(response_datetime.content).strip('\'b\'')
