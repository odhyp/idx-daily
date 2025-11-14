"""
Date utilities
"""

from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"


def is_valid_date(date_str: str, date_format: str = DATE_FORMAT) -> bool:
    """Return True if date_str matches format, otherwise False."""
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def is_valid_non_future(date_str: str, date_format: str = DATE_FORMAT) -> bool:
    """Return True if date_str is not in the future, otherwise False."""
    try:
        d = datetime.strptime(date_str, date_format)
    except ValueError:
        return False
    return d.date() <= datetime.today().date()


def validate_date(date_str: str) -> bool:
    """Validate date input"""
    return is_valid_date(date_str) and is_valid_non_future(date_str)


def generate_date_range(
    start_date: str, end_date: str, date_format: str = DATE_FORMAT
) -> list:
    """Generate a list of dates between start_date and end_date,
    skipping weekends."""
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)

    if end < start:
        raise ValueError("end_date must not be earlier than start_date!")

    dates = []
    current = start
    while current <= end:
        if current.weekday() < 5:
            dates.append(current.strftime(date_format))
        current += timedelta(days=1)
    return dates


def count_days(start_date: str, end_date: str, date_format: str = DATE_FORMAT) -> str:
    """Count business days between start_date and end_date,
    skipping weekends."""
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)

    if end < start:
        raise ValueError("end_date must not be earlier than start_date!")

    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            count += 1
        current += timedelta(days=1)
    return str(count)
