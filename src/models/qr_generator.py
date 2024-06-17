from dataclasses import dataclass
from datetime import datetime


QR_IMAGE_DATETIME_STR_FORMAT = "%d/%m/%Y %H:%M"


@dataclass(frozen=True)
class QRImageDateTime:
    datetime: datetime
    offset: int

    def __str__(self) -> str:
        offset = f"(UTC{self.offset:+03d}:00)"
        dt = self.datetime.strftime(QR_IMAGE_DATETIME_STR_FORMAT)
        return f"{dt} {offset}"


@dataclass(frozen=True)
class QRImageDetails:
    created_at: QRImageDateTime
    file_path: str
    encoded_text: str
