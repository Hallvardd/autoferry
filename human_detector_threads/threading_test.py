import threading as th
import time
import cv2
import numpy as np
import DetectorAPI
import queue
import time
 
video_path = '/home/henning/Desktop/EiT/human_detector/TownCentreXVID.avi'
model_path = '/home/henning/Desktop/EiT/human_detector/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
ip_camera_path = 'rtsp://admin:autogruppe4@192.168.0.100//Streaming/Channels/102'

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


class ProcessFrame():
    def __init__(self, frame, detector, boxes, scores, classes, num):
        self.unprocessedFrame = frame
        self.processedFrame = frame
        self.detector = detector
        self.stopped = False
        self.boxes = boxes
        self.scores = scores
        self.classes = classes
        self.num = num
	
    def start(self):
    	th.Thread(target=self.process, args=(), daemon=True).start()
    	return self
    
    def process(self):
        while not self.stopped:
            self.boxes, self.scores, self.classes, self.num = self.detector.processFrame(self.unprocessedFrame) #Process frame and generate boxes and scores.
            #self.processedFrame = self.detector.addBoxesToFrame(self.boxes, self.classes, self.scores, self.frame) #Add boxes to current frame
       
    def stop(self):
        self.stopped = True


if __name__ ==  "__main__":
    cap = cv2.VideoCapture(video_path)
    detector = DetectorAPI.DetectorAPI(path_to_ckpt=model_path)
    r, frameInit  = cap.read()
    cap.release()
    boxesInit, scoresInit, classesInit, numInit = detector.processFrame(frameInit)
    
    frame_grabber = GetFrame(video_path).start()
    frame_shower = ShowFrame(frame=frameInit).start()
    frame_processor = ProcessFrame(frame=frameInit,detector=detector,boxes=boxesInit,classes=classesInit,scores=scoresInit,num=numInit).start()

    while True:
        frame = frame_grabber.frame # Grab a frame
        frame_processor.unprocessedFrame = frame # Process the frame
        frameWithBoxes = detector.addBoxesToFrame(frame_processor.boxes, frame_processor.scores, frame_processor.classes, frame_processor.num, frame)
        frame_shower.frame = frameWithBoxes # Dispaly the frame

