"""
Date related
"""

from datetime import datetime, timedelta


def validate_date(date_str: str, fmt: str = "%Y-%m-%d") -> bool:
    try:
        datetime.strptime(date_str, fmt)
        return True
    except ValueError:
        return False


def generate_date_range(start_date: str, end_date: str) -> list:
    formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d")
    formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d")

    date_range_length = (formatted_end_date - formatted_start_date).days + 1

    date_list = [
        (formatted_start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(date_range_length)
    ]

    return date_list
