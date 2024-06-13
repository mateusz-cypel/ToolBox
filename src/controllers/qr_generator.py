from services.qr_generator import QRGeneratorService, qr_generator_service
from views.qr_generator import QRGeneratorView, qr_generator_view


class QRGeneratorController:
    def __init__(self, view: QRGeneratorView, qr_generator_service: QRGeneratorService):
        self._view = view
        self._view.bind_on_qr_generate_button_press(self.generate_qr_code())
        self._qr_generator_service = qr_generator_service

    @property
    def view(self):
        return self._view

    def generate_qr_code(self):
        def callback(instance):
            message = self._view.message
            details = self._qr_generator_service.generate(message)
            self._view.update_view(
                source=details.file_path,
                updated_at=str(details.created_at)
            )
        return callback


qr_generator_controller = QRGeneratorController(
    view=qr_generator_view,
    qr_generator_service=qr_generator_service
)
