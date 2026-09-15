from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def get_current_datetime(timezone: str) -> str:
    """Returns the current date and time for a given timezone."""

    try:
        current_time = datetime.now(ZoneInfo(timezone))

        return current_time.strftime(
            "%A, %B %d, %Y at %I:%M %p"
        )

    except ZoneInfoNotFoundError:
        return (
            f"I couldn't find the timezone '{timezone}'. "
            "Please provide a valid IANA timezone, "
            "such as 'Asia/Kolkata', 'Asia/Tokyo', "
            "or 'America/New_York'."
        )