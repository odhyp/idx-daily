"""
Date utilities
"""

from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"


def validate_date(date_str: str, date_format: str = DATE_FORMAT) -> bool:
    """Return True if date_str matches format, otherwise False."""
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def is_valid_range(start_date: str, end_date: str, fmt: str = DATE_FORMAT) -> bool:
    """Return True if end_date is the same or after start_date."""
    try:
        start = datetime.strptime(start_date, fmt)
        end = datetime.strptime(end_date, fmt)
        return end >= start
    except ValueError:
        return False


def generate_date_range(
    start_date: str, end_date: str, date_format: str = DATE_FORMAT
) -> list:
    """Generate a list of dates between start_date and end_date,
    skipping weekends."""
    if not is_valid_range(start_date, end_date, date_format):
        raise ValueError("end_date must not be earlier than start_date!")

    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)

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
    if not is_valid_range(start_date, end_date, date_format):
        raise ValueError("end_date must not be earlier than start_date!")

    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)

    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            count += 1
        current += timedelta(days=1)
    return str(count)
