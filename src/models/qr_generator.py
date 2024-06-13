from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class QRImageDateTime:
    datetime: datetime
    offset: int

    def __str__(self) -> str:
        sign = "-" if self.offset < 0 else "+"
        value = f"{'0' if self.offset < 10 else ''}{self.offset}"
        offset = f"(UTC{sign}{value}:00)"

        fmt = "%d/%m/%Y %H:%M"
        dt = self.datetime.strftime(fmt)

        return f"{dt} {offset}"


@dataclass(frozen=True)
class QRImageDetails:
    created_at: QRImageDateTime
    file_path: str
    encoded_text: str
