import cv2
import threading

class CameraManager:
    def __init__(self, source=0):
        self.source = source
        self.cap = cv2.VideoCapture(self.source)
        # cv2.VideoCapture không an toàn khi nhiều luồng (thread) cùng gọi read()
        # đồng thời (ví dụ Flask chạy đa luồng, nhiều route cùng lấy frame).
        # Lock đảm bảo tại một thời điểm chỉ một luồng được đọc/mở lại camera.
        self._lock = threading.Lock()

    def get_frame(self):
        with self._lock:
            if not self.cap.isOpened():
                self.cap.open(self.source)
            success, frame = self.cap.read()
        return success, frame

    def release(self):
        with self._lock:
            if self.cap.isOpened():
                self.cap.release()

camera_stream = CameraManager(0)