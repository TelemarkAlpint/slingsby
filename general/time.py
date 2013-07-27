from pytz import timezone, utc
from datetime import datetime

nor = timezone('Europe/Oslo')
eng = timezone('America/New_York')

def now():
    return datetime.now(tz=nor)

def aware_time(time):
    if not time.tzinfo:
        return nor.normalize(nor.localize(time))
    else:
        return time

def aware_from_utc(time):
    if not time.tzinfo:
        return time.replace(tzinfo=utc)
    else:
        return time

def aware_from_nor(time):
    if not time.tzinfo:
        return time.replace(tzinfo=nor)
    else:
        return time

def utc_to_nor(utc):
    utcdate = aware_from_utc(utc)
    return utcdate.astimezone(nor)

def nor_to_utc(nordate):
    nordate = aware_from_nor(nordate)
    return nordate.astimezone(utc)

def is_past(date):
    dst_aware_datetime = aware_time(date)
    time_now = now()
    seconds_since_date = (time_now - dst_aware_datetime).total_seconds()
    return seconds_since_date > 0

def is_future(date):
    return not is_past(date)

def days_since(date):
    return days_between(now(), date)

def days_between(date1, date2):
    dst_date1 = aware_time(date1)
    dst_date2 = aware_time(date2)
    days_passed = dst_date1.toordinal() - dst_date2.toordinal()
    return days_passed

def seconds_since(date):
    return seconds_between(now(), date
                           )
def seconds_between(date1, date2):
    dst_date1 = aware_time(date1)
    dst_date2 = aware_time(date2)
    return int((dst_date1 - dst_date2).total_seconds())

def seconds_to(date):
    return seconds_between(date, now())
