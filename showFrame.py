import cv2
import threading as th

class ShowFrame:
    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        th.Thread(target=self.show, args=(), daemon=True).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True