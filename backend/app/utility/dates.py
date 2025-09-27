from datetime import datetime, UTC

def force_utc(v: datetime) -> datetime:
    if v.tzinfo is None: # assume naive -> UTC
        return v.replace(tzinfo=UTC)
    return v.astimezone(UTC)