import threading as th
import cv2
import numpy as np
import detectorAPI
import tracker
import person
from getFrame import GetFrame
from showFrame import ShowFrame
from processFrame import ProcessFrame
import os

#video_path = '/home/henning/Desktop/EiT/human_detector/TownCentreXVID.avi'
#model_path = '/home/henning/Desktop/EiT/human_detector/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
#ip_camera_path = 'rtsp://admin:autogruppe4@192.168.0.100//Streaming/Channels/102'

video_path = str(os.sys.path[0]) + '/TownCentreXVID.avi'
model_path = str(os.sys.path[0]) + '/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
#model_path = str(os.sys.path[0]) + '/ssd_mobilenet/frozen_inference_graph.pb'
#model_path = str(os.sys.path[0]) + '/ssdlite_mobilenet_v2/frozen_inference_graph.pb'
ip_camera_path = 'rtsp://admin:autogruppe4@192.168.0.100//Streaming/Channels/102'
web_cam = 0



if __name__ ==  "__main__":
    cap = cv2.VideoCapture(video_path)
    detector = detectorAPI.DetectorAPI(path_to_ckpt=model_path)
    r, frameInit  = cap.read()
    cap.release()
    centroidsInit, scoresInit, classesInit, numInit = detector.processFrame(frameInit)

    frame_grabber = GetFrame(video_path).start()
    frame_shower = ShowFrame(frame=frameInit).start()
    frame_processor = ProcessFrame(frame=frameInit,detector=detector,centroids=centroidsInit,classes=classesInit,scores=scoresInit,num=numInit).start()
    tracker = tracker.Tracker()

    while True:
        frame = frame_grabber.frame # Grab a frame
        frame_processor.unprocessedFrame = frame # Process the frame
        frameWithBoxes = detector.addBoxesToFrame(frame_processor.centroids, frame_processor.scores, frame_processor.classes, frame_processor.num, frame)

        if not tracker.personDict:
            tracker.fill_persondict(frame_processor.positions)
        else:
            distances = tracker.calculateDistanceFromPersonsToPoints(tracker.personDict, frame_processor.positions)
            tracker.tracking_algorithm(distances)

        frame_shower.frame = frameWithBoxes # Dispaly the frame

