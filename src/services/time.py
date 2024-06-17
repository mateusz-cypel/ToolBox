from datetime import datetime

from models.time import DateTime


class TimeService:
    @classmethod
    def now(cls) -> DateTime:
        dt = datetime.utcnow()
        return DateTime(
            datetime=dt,
            offset=0
        )


time_service = TimeService()
