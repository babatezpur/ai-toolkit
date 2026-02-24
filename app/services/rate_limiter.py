from datetime import date, datetime, timezone
from app import db
from app.models.user import User

DAILY_LIMIT = 30


def check_rate_limit(user: User):
    """
    Checks if the user has remaining requests for today.
    If it's a new day, resets the counter first.

    Args:
        user: The User model instance

    Returns:
        tuple: (allowed: bool, remaining: int)
    """
    today = date.today()

    # New day — reset the counter
    if user.last_request_date != today:
        user.daily_request_count = 0
        user.last_request_date = date.today()
        db.session.commit()

    remaining = DAILY_LIMIT - user.daily_request_count
    return remaining, remaining > 0


def increment_request_count(user: User):
    """
    Increments the user's daily request count by 1.
    Call this AFTER a successful OpenAI call.

    Args:
        user: The User model instance
    """
    user.daily_request_count += 1
    db.session.commit()