import datetime

from django.utils import timezone


def check_time(serializer, delta=False):
    if delta:
        delta = datetime.timedelta(hours=int(serializer.data.get('delta').split(':')[0]),
                                   minutes=int(serializer.data.get('delta').split(':')[1]),
                                   seconds=int(serializer.data.get('delta').split(':')[2]))
        input_time = datetime.datetime(year=timezone.datetime.now().year, month=timezone.datetime.now().month,
                                       day=timezone.datetime.now().day,
                                       hour=int(serializer.data.get('time').split(':')[0]),
                                       minute=int(serializer.data.get('time').split(':')[1]),
                                       second=int(serializer.data.get('time').split(':')[2]))
        return abs(timezone.datetime.now() - input_time) <= delta
    else:
        return serializer.data.get('time') == timezone.localtime().strftime("%H:%M")
