import arrow


class TimeUtil:

    def floor_minutes(self, dt: arrow, minutes: int) -> arrow:
        curr_min = dt.datetime.minute
        offset = curr_min % minutes
        new_minute = curr_min - offset
        return dt.floor('minute').replace(minute=new_minute)

    def floor_hours(self, dt: arrow, hours: int) -> arrow:
        curr_hour = dt.datetime.hour
        offset = curr_hour % hours
        new_hour = curr_hour - offset + 1
        return dt.floor('hour').replace(hour=new_hour)

    def t5min(self, dt: arrow) -> int:
        result = self.floor_minutes(dt=dt, minutes=5).timestamp
        return result

    def qtrhr(self, dt: arrow) -> int:
        result = self.floor_minutes(dt=dt, minutes=15).timestamp
        return result

    def qtrday(self, dt: arrow) -> int:
        result = self.floor_hours(dt=dt, hours=6).timestamp
        return result
