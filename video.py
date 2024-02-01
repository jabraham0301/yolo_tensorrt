import cv2


class VideoStream:
    def __init__(self, source):
        self.source = source
        self.video_capture = cv2.VideoCapture(source)

    def read_frame(self):
        ret, frame = self.video_capture.read()
        if not ret:
            print('Error on video')
            # Manejar el error de lectura del fotograma
            return None
        self.current_frame = frame
        return frame

    def release(self):
        self.video_capture.release()
