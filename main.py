import detectorAPI as odapi
import time
import cv2


if __name__ == "__main__":
    start_time = time.clock()
    run_time = time.clock()
    fps = 10
    model_path = '/home/hallvard/gcvenv/autoferry/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
    video_path = '/home/hallvard/Videos/TownCentreXVID.avi'
    odapi = odapi.DetectorAPI(path_to_ckpt=model_path)
    threshold = 0.7

    # Use video:
    # cap = cv2.VideoCapture(video_path)

    # Use webcam
    cap = cv2.VideoCapture(0)

    # Use ip-cam
    #cap = cv2.VideoCapture('rtsp://admin:autogruppe4@192.168.0.100//Streaming/Channels/101')

    cap.set(cv2.CAP_PROP_FPS, fps)
    cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
    while True:
        r, img = cap.read()
        #img = cv2.resize(img, (1280, 720))

        # Visualization of the results of a detection.
        number_of_humans = 0
        if run_time-start_time > 10.0:
            boxes, scores, classes, num = odapi.processFrame(img)
            for i in range(len(boxes)):
                # Class 1 represents human,
                # Class 2 represents bicycle,
                # Class 18 represents dog,
                # Class 33 represents suitcase
                if (classes[i] == 1) and (scores[i] > threshold):
                    box = boxes[i]
                    number_of_humans += 1
                    cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)
                elif (classes[i] == 2) and (scores[i] > threshold):
                    box = boxes[i]
                    cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),(0,255,0),2)
                elif classes[i] == 18 and scores[i] > threshold:
                    box = boxes[i]
                    cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),(0,0,255),2)

        else:
            run_time = run_time = time.clock()


        cv2.imshow("preview", img)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

    # TODO find the middle of the rectangle.
        # find a way of knowing how the box moves
            # use a kalman filter, with a model of human movement.
            # Dissapearing boxes.
            # Dynamic way of finding the history of the boxes.
            # Person class.
                # ID pos
    # find when a rectangle crosses the line.
    # implement a buffer zone where the counting happens
    # method for.
