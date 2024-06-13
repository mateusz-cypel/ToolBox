import qrcode

from models.qr_generator import QRImageDateTime, QRImageDetails
from services.time import time_service, TimeService


QR_IMAGE_OUTPUT_FILEPATH = "QR_OUTPUT.png"


class QRGeneratorService:
    def __init__(self, time_service: TimeService, default_file_path: str = QR_IMAGE_OUTPUT_FILEPATH):
        self._default_file_path = default_file_path
        self._time_service = time_service

    def generate(self, text: str, path: str | None = None) -> QRImageDetails:
        if path is None:
            path = self._default_file_path

        image = qrcode.make(text)
        image.save(path)

        dt = self._time_service.now()
        return QRImageDetails(
            created_at=QRImageDateTime(
                datetime=dt.datetime,
                offset=dt.offset
            ),
            file_path=path,
            encoded_text=text,
        )


qr_generator_service = QRGeneratorService(
    time_service=time_service
)