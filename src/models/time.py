from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DateTime:
    datetime: datetime
    offset: int
