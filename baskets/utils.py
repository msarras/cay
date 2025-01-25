from datetime import date, timedelta


def get_end_of_week():
    today = date.today()
    # Calculate the number of days until the end of the week (Sunday)
    days_until_sunday = 6 - today.weekday()  # 0 is Monday, 6 is Sunday
    end_of_week = today + timedelta(days=days_until_sunday)
    return end_of_week


def get_beginning_of_week():
    today = date.today()
    days_to_subtract = today.weekday()  # Monday is 0 and Sunday is 6
    beginning_of_week_date = today - timedelta(days=days_to_subtract)
    return beginning_of_week_date
