import flet as ft
import cv2
import asyncio
import base64
from video import VideoStream
from object_tracker import InferDet


class CameraWidget(ft.UserControl):
    def __init__(self, camera_input):
        super().__init__()
        self.video = VideoStream(camera_input)
        self.camera_input = camera_input
        self.ia_tracker = InferDet()

    async def did_mount_async(self):
        self.running = True
        asyncio.create_task(self.update_frame())

    async def will_unmount_async(self):
        self.running = False

    async def update_frame(self):
        while self.running:
            frame = self.video.read_frame()

            if self.camera_input == 0:
                annotated_frame = self.ia_tracker.update(frame)
                self.img.src_base64 = base64.b64encode(
                    cv2.imencode('.jpg', cv2.resize(annotated_frame, (1024, 768)))[1]).decode()
            else:
                self.img.src_base64 = base64.b64encode(cv2.imencode('.jpg', cv2.resize(frame, (1024, 768)))[1]).decode()
            await self.update_async()
            await asyncio.sleep(0.001)

    def build(self):
        if self.camera_input == 0:
            self.img = ft.Image(fit=ft.ImageFit.COVER)
        else:
            self.img = ft.Image(width=280, height=280)
        return self.img
