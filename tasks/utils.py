from datetime import date, timedelta


def get_end_of_week():
    today = date.today()
    # Calculate the number of days until the end of the week (Sunday)
    days_until_sunday = 6 - today.weekday()  # 0 is Monday, 6 is Sunday
    end_of_week = today + timedelta(days=days_until_sunday)
    return end_of_week
