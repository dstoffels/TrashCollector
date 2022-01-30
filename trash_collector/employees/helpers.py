from datetime import date, datetime

def parse_date(day) -> date:
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    if day in weekdays:
        todays_date = date.today()
        todays_index = todays_date.weekday()
        day_index = weekdays.index(day)
        difference = day_index - todays_index
        return date(todays_date.year, todays_date.month, todays_date.day + difference)
    else:
        return datetime.strptime(day, '%Y-%m-%d').date()