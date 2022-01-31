from typing import List
from datetime import datetime

def get_datetime(timestamp: str, valid_formats: List[str], url: str) -> datetime:
    dt = None
    for format in valid_formats:
        try:
            dt = datetime.strptime(timestamp, format)
        except ValueError:
            pass

    if dt is None:
        raise Exception(f'Could not parse timestamp format of timestamp: "{timestamp}" url: {url}')

    return dt