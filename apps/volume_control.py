"""
Project Volume Control
"""
from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from core.abstract_middleware import BaseMiddleware
from core.hand_land_marks import HandLandMarks
from core.hand_tracking import HandDetector, HandPointsBold
from core.range_fingers import RangeFingers
from core.utils import FpsShowInfo
from core.video_capture import OpenCvVideoCapture


class VolumeControlMiddleware(BaseMiddleware):
    """Classe para executar controle de volume com os dedos."""

    _MIN_LENGTH, _MAX_LENGTH = 15, 194

    def __init__(self, next_middleware=None):
        super().__init__(next_middleware=next_middleware)
        # Cria o HandDetector.
        self._detector = HandDetector(
            fps=FpsShowInfo(color=(90, 90, 90)),
            bold_points=HandPointsBold(
                bold_points=[
                    HandLandMarks.THUMB_TIP,
                    HandLandMarks.INDEX_FINGER_TIP,
                ],
            ),
        )
        # Ativa os controles de áudio.
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self._volume = cast(interface, POINTER(IAudioEndpointVolume))
        # Recupera o valores de máximo e mínimos de volume.
        vol_range = self._volume.GetVolumeRange()
        # Ativa o comando de distância entre dedos
        self._volume_range_control = RangeFingers(
            self._detector,
            self._MIN_LENGTH,
            self._MAX_LENGTH,
            vol_range,
            color=(255, 0, 255),
        )

    def _process(self, frame):
        """Executa o processamento principal."""
        frame = self._detector.find_hands(frame)
        # Se recuperou a posição dos dedos.
        if self._detector.points:
            # Recupera o volume ajustado de acordo com a distância entre dedos e seu range.
            vol = self._volume_range_control.process(frame).value
            # Ajusta o volume
            self._volume.SetMasterVolumeLevel(vol, None)
        # imprime a caixa visualizadora de volume
        frame = self._volume_range_control.show(frame, (0, 255, 0))
        return frame


def main():
    """Método de teste."""
    OpenCvVideoCapture(middleware=VolumeControlMiddleware()).execute()


if __name__ == "__main__":
    main()
