from typing import Optional

_current_data: Optional[dict] = None


def set_data(data: dict) -> None:
    global _current_data
    _current_data = data


def get_data() -> Optional[dict]:
    return _current_data


def has_data() -> bool:
    return _current_data is not None
