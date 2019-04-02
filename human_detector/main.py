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
import display

# Paths
#video_path = sys.path[0] + '/above_vid.mp4'
video_path = sys.path[0] + '/front_vid.mp4'
model_path = sys.path[0] + '/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
model_2_path = sys.path[0] + '/ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03/frozen_inference_graph.pb'
#ip_camera_path = 'rtsp://admin:autogruppe4@129.241.205.244//Streaming/Channels/102'
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

    # Initialize ferry and display
    keypress = 0
    path = sys.path[0] +'/database'
    disp = display.Display(database_path= sys.path[0] + '/database',
                           display_size=(600,600),
                           image_type='.jpg')
    disp.load_images_from_database()

    state = {
        'at_terminal': False,
        'at_other_terminal' : True,
        'button_pressed' : False,
        'boarding' : True,
        'first_person_boarded': False,
        'arriving' : False,
        'departing' : False,
        'full': False
    }
    # The time the ferry waits at the other side before responding to the button being pressed.
    FERRY_WAIT_TIME = 20
    # The time the ferry uses to cross
    FERRY_CROSS_TIME = 10
    # The time the ferry waits after a person has boarded before departing.
    BOARDED_DEPARTURE_TIME = 30
    # The time the ferry waits before it departs after it is full
    FULL_DEPARTURE_TIME = 5
    # When the button gets pressed
    button_pressed_time = 0
    # When the ferry arrives at a terminal
    arrival_time = time.time()
    # When a ferry leaves the terminal
    departure_time = 0
    #Time of the Ferry being full
    full_time = 0
    #Time of the first person boarding the ferry
    boarded_time = 0

    first_frame = True
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

        # Ferry visual communication system:
        keypress = cv2.waitKey(1)

        if keypress == ord("q"):
            break

        # Ferry at the oposite terminal of the display
        if state['at_other_terminal']:
            if keypress == ord('a') and not state['button_pressed']:
                state['button_pressed'] = True

            if state['button_pressed']:
                if time.time() - arrival_time > FERRY_WAIT_TIME:
                    cv2.imshow('state', disp.database['arriving'])
                    state['button_pressed'] = False
                    state['at_other_terminal'] = False
                    state['arriving'] = True
                    departure_time = time.time()
                else:
                    # TODO add the counter time.time() - arrival_time to the image
                    cv2.imshow('state', disp.database['ferry_called'])
            else:
                if time.time() - arrival_time > FERRY_WAIT_TIME:
                    cv2.imshow('state', disp.database['call_ferry'])
                else:
                    # TODO add the counter time.time() - arrival_time to the image
                    cv2.imshow('state', disp.database['ferry_busy'])

        # Ferry at the displays terminal
        elif state['at_terminal']:
            if currentPersonCount == 10:
                if not state['full']:
                    full_time = time.time()
                    state['full'] = True
                    cv2.imshow('state', disp.database['ferry_full'])
                else:
                    cv2.imshow('state', disp.database['ferry_full'])
                    if (time.time() - full_time > FULL_DEPARTURE_TIME):
                        state['departing'] = True
                        state['at_terminal'] = False
                        departure_time = time.time()

            elif currentPersonCount == 0:
                cv2.imshow('state', disp.database['boarding0'])
                state['first_person_boarded'] = False
            else:
                cv2.imshow('state', disp.database['boarding1'])
                state['full'] = False
                if not state['first_person_boarded']:
                    state['first_person_boarded'] = True
                    boarded_time = time.time()
                else:
                    if time.time() - boarded_time > BOARDED_DEPARTURE_TIME:
                        state['departing'] = True
                        state['at_terminal'] = False
                        departure_time = time.time()

        # Ferry crossing
        else:
            if (time.time() - departure_time > FERRY_CROSS_TIME):
                if state['arriving']:
                    state['arriving'] = False
                    state['at_terminal'] = True
                    arrival_time = time.time()

                elif state['departing']:
                    state['departing'] = False
                    state['at_other_terminal'] = True
                    arrival_time = time.time()
            else:
                if state['arriving']:
                    cv2.imshow('state', disp.database['arriving'])

                elif state['departing']:
                    cv2.imshow('state', disp.database['departing'])

        # START: SECTION FOR TESTING PASSENGER FUNCTIONALITY
        if keypress == ord('p') and currentPersonCount < 10:
            currentPersonCount += 1

        if keypress == ord('m') and currentPersonCount > 0:
            currentPersonCount -= 1
        # END

    cv2.destroyAllWindows()



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
