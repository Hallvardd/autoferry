import cv2
import threading as th

class GetFrame:
    def __init__(self,source):
        self.stream = cv2.VideoCapture(source) 
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        
    def start(self):
        th.Thread(target=self.grab, args=(),daemon=True).start()
        return self
    
    def grab(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                
    def stop(self):
        self.stopped = True