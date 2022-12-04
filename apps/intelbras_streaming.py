from core.video_capture import OpenCvCamCaptureByRtsp
from decouple import config

data = {
    'username': config('user_name', cast=str, default='admin'),
    'password': config('password', cast=str),
    'ip': config('ips', cast=str, default='localhost,').split(',')[0],
    'port': '554',
    'rote': '/cam/realmonitor?channel=1&subtype=0',
}

OpenCvCamCaptureByRtsp(**data).execute()
