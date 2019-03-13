import threading as th
import cv2
import numpy as np
import detectorAPI
import tracker
import person
import sys
import time
from getFrame import GetFrame
from showFrame import ShowFrame
from processFrame import ProcessFrame
import counter
 
video_path = sys.path[0] + '/TownCentreXVID.avi'
model_path = sys.path[0] + '/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
model_2_path = sys.path[0] + '/ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03/frozen_inference_graph.pb'
ip_camera_path = 'rtsp://admin:autogruppe4@192.168.0.100//Streaming/Channels/102'
web_cam = 0

#video_path = r'''C:\Users\Henning\Desktop\EiT\TownCentreXVID.avi'''
#model_path = r'''C:\Users\Henning\Desktop\EiT\faster_rcnn_inception_v2_coco_2018_01_28\frozen_inference_graph.pb'''



if __name__ ==  "__main__":
    cap = cv2.VideoCapture(video_path)
    detector = detectorAPI.DetectorAPI(path_to_ckpt=model_path)
    r, frameInit  = cap.read()
    cap.release()
    centroidsInit, scoresInit, classesInit, numInit = detector.processFrame(frameInit)
    positionsInit = detector.listOfPersons(centroidsInit, scoresInit, classesInit)
    
    #frame_grabber = GetFrame(video_path).start()
    #frame_shower = ShowFrame(frame=frameInit).start()
    #frame_processor = ProcessFrame(frame=frameInit,detector=detector,centroids=centroidsInit,classes=classesInit,scores=scoresInit,num=numInit).start()
    tracker = tracker.Tracker()
    
    time.sleep(0.01)

    tracker.fill_persondict(positionsInit)
    
    source = cv2.VideoCapture(video_path)
    previousCount = 0
    currentPersonCount = 0
    crossingLine = counter.defineCrossingLine()


    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (50,50)
    fontScale              = 1
    fontColor              = (0,0,0)
    lineType               = 2


    while True:
        #frame = frame_grabber.frame # Grab a frame

        (flag, frame) = source.read()
        counter.drawCrossingLine(crossingLine, frame)
        #frame_processor.unprocessedFrame = frame # Process the frame
        #frameWithCentroids = detector.addCentroidsToFrame(frame_processor.centroids, frame_processor.scores, frame_processor.classes, frame_processor.num, frame)
        #print(frame_processor.positions)
        
        centroids, scores, classes, num = detector.processFrame(frame)
        positions = detector.listOfPersons(centroids, scores, classes)
        tracker.tracking_algorithm(positions)

        frameWithCentroids = detector.addCentroidsToFrame(centroids, scores, classes, num, frame)

        #frame_shower.frame = imageWithPath # Dispaly the frame
        
        for ID,person in tracker.personDict.items():
            #print("History length for person ",ID," :", person.position_history)
            print("person ", ID, ": is counted? ", person.get_counted())
            frameWithCentroids = tracker.personDict[ID].draw_path(frameWithCentroids)
            cv2.circle(frameWithCentroids, person.position_history[-1], radius=int(person.threshold), color=(255,0,0), thickness=3, lineType=8, shift=0)
            isCounted = counter.countPerson(person, crossingLine)
            if (isCounted == True):
                person.set_counted(True)
                currentPersonCount += isCounted
        
        #print("NUM COUNTED: ", currentPersonCount)
        string = "Counted persons: " + str(currentPersonCount)
        cv2.putText(frameWithCentroids, string, bottomLeftCornerOfText, font, fontScale,    fontColor,    lineType)
        #cv2.putText(frameWithCentroids, str(currentPersonCount),(100,100), font, 1, (200,0,0), 3, cv2.LINE_AA)
        #cv2.putText(frameWithCentroids, currentPersonCount, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
        cv2.imshow("Video", frameWithCentroids)
        print("\n\n")
        if cv2.waitKey(1) == ord("q"):
            break
        #frame_shower.frame = frameWithCentroids # Dispaly the frame
        #assert input(">>>") == "y"
