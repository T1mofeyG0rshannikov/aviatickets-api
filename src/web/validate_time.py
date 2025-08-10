from datetime import datetime

from src.exceptions import InvalidCreateLogRequest


def validate_time(time: str) -> datetime:
    try:
        return datetime.strptime(time, "%d:%m:%Y.%H:%M:%S")
    except ValueError:
        raise InvalidCreateLogRequest("Invalid time format. Use DD:MM:YYYY.hh:mm:ss")
