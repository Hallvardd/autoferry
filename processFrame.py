import detectorAPI
import cv2
import threading as th

class ProcessFrame():
    def __init__(self, frame, detector, centroids, scores, classes, num):
        self.unprocessedFrame = frame
        self.detector = detector
        self.stopped = False
        self.centroids = centroids
        self.scores = scores
        self.classes = classes
        self.num = num
        self.positions = []
	
    def start(self):
    	th.Thread(target=self.process, args=(), daemon=True).start()
    	return self
    
    def process(self):
        while not self.stopped:
            self.centroids, self.scores, self.classes, self.num = self.detector.processFrame(self.unprocessedFrame) #Process frame and generate boxes and scores.
            self.positions = self.detector.listOfPersons(self.centroids, self.scores, self.classes)
            print(self.positions)

    def stop(self):
        self.stopped = True