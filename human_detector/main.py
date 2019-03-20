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

# Paths
video_path = sys.path[0] + '/TownCentreXVID.avi'
model_path = sys.path[0] + '/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
model_2_path = sys.path[0] + '/ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03/frozen_inference_graph.pb'
ip_camera_path = 'rtsp://admin:autogruppe4@192.168.0.100//Streaming/Channels/102'
web_cam = 0




if __name__ ==  "__main__":
    video_size = (1000,1000,3)
    # Initialize detector
    detector = detectorAPI.DetectorAPI(path_to_ckpt=model_path)
    centroidsInit, scoresInit, classesInit, numInit = detector.processFrame(np.zeros(video_size))
    positionsInit = detector.listOfPersons(centroidsInit, scoresInit, classesInit)
    
    # Initialize tracker
    tracker = tracker.Tracker()
    time.sleep(0.01)
    tracker.fill_persondict(positionsInit)
    
    # Initialize video stream
    source = cv2.VideoCapture(video_path)
    
    # Initialize counter
    previousCount = 0
    currentPersonCount = 0
    crossingLine = counter.defineCrossingLine()
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (50,50)
    fontScale              = 1
    fontColor              = (0,0,0)
    lineType               = 2

    while True:
        # Read frame
        (flag, frame) = source.read()
        
        # Visualize counting line
        counter.drawCrossingLine(crossingLine, frame)

        # Compute the centroids, scores and classes of all detected objects.
        centroids, scores, classes, num = detector.processFrame(frame)
        
        # Formats the centroids to a list of coordinates for the objects we want to track.
        positions = detector.listOfPersons(centroids, scores, classes)
        
        # Starts tracking the objects given in the position list.
        tracker.tracking_algorithm(positions)
        
        # Adds centroids to the frame for easier visualization.
        frameWithCentroids = detector.addCentroidsToFrame(centroids, scores, classes, num, frame)
        
        # Loops through all persons and draws the tracking path and search region
        # Counts all person crossing the line.
        for ID,person in tracker.personDict.items():
            #print("History length for person ",ID," :", person.position_history)
            #print("person ", ID, ": is counted? ", person.get_counted())
            frameWithCentroids = tracker.personDict[ID].draw_path(frameWithCentroids)
            cv2.circle(frameWithCentroids, person.position_history[-1], radius=int(person.threshold), color=(255,0,0), thickness=3, lineType=8, shift=0)
            isCounted = counter.countPerson(person, crossingLine)
            #if ID == 3:
            #    cv2.circle(frameWithCentroids, person.position_history[-1], radius=int(person.threshold), color=(255,255,0), thickness=4, lineType=8, shift=0)
            #    print(person.direction)
            isCounted = counter.countPerson(person, crossingLine)

            if (isCounted == True):
                person.set_counted(True)
                currentPersonCount += isCounted
    
        #assert input('>>>') == 'y'
        
        # Display count
        cv2.putText(frameWithCentroids, "Counted persons: " + str(currentPersonCount), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
        
        # Display image
        cv2.imshow("Video", frameWithCentroids)
        if cv2.waitKey(1) == ord("q"):
            break
        
        #cv2.putText(frameWithCentroids, str(currentPersonCount),(100,100), font, 1, (200,0,0), 3, cv2.LINE_AA)
        #cv2.putText(frameWithCentroids, currentPersonCount, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
        #print("\n\n")
        
        #print('TEMP COUNTER: ',temp_counter)
        #temp_counter += 1
        #if temp_counter >= 100:
        #    centroids = []
        #    scores = []
        #    classes = []
        #    num = []
        #else:
        
