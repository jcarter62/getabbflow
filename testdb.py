from timeutil import TimeUtil
import arrow
import time, datetime

#
# def floor_minutes(dt: arrow, minutes: int) -> arrow:
#     curr_min = dt.datetime.minute
#     offset = curr_min % minutes
#     new_minute = curr_min - offset
#     return dt.floor('minute').replace(minute=new_minute)
#
# def floor_hours(dt: arrow, hours: int) -> arrow:
#     curr_hour = dt.datetime.hour
#     offset = curr_hour % hours
#     new_hour = curr_hour - offset
#     return dt.floor('hour').replace(hour=new_hour)

while True:
    curtime = arrow.utcnow()
    tu = TimeUtil()

    t5min = tu.t5min(curtime)
    t5mins = datetime.datetime.fromtimestamp(t5min)
    qtrhr = tu.qtrhr(curtime)
    qtrhrs = datetime.datetime.fromtimestamp(qtrhr)
    qtrday = tu.qtrday(curtime)
    qtrdays = datetime.datetime.fromtimestamp(qtrday)

    print('%s\t%d\t%s\t%d\t%s\t%d\t%s' % (curtime, t5min, t5mins, qtrhr, qtrhrs, qtrday, qtrdays))
    time.sleep(2.5)
