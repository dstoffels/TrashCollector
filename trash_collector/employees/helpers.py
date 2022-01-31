import datetime

def parse_date(day) -> datetime.date:
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    if day in weekdays:
        todays_date = datetime.date.today()
        todays_index = todays_date.weekday()
        day_index = weekdays.index(day)
        difference = day_index - todays_index
        return todays_date + datetime.timedelta(days=difference)
    else:
        return datetime.datetime.strptime(day, '%Y-%m-%d').date()