    # Code adapted from Tensorflow Object Detection Framework
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb
# Tensorflow Object Detection Detector

import numpy as np
import tensorflow as tf
import cv2
import time


class DetectorAPI:
    def __init__(self, path_to_ckpt):
        self.path_to_ckpt = path_to_ckpt

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')


    def processFrame(self, image):
        image_np_expanded = np.expand_dims(image, axis=0)
        start_time = time.time()
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        end_time = time.time()
        #print("Elapsed Time:", end_time-start_time)

        im_height, im_width,_ = image.shape
        point_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            point_list[i] = (int(((boxes[0,i,1]*im_width)+(boxes[0,i,3]*im_width))/2), int(((boxes[0,i,0] * im_height)+(boxes[0,i,2] * im_height))/2))
        return point_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        self.default_graph.close()

    def addCentroidsToFrame(self, centroids, scores, classes, num, img):
        threshold = 0.8
        for i in range(len(centroids)):
            if (classes[i] == 1) and (scores[i] > threshold):
                cv2.circle(img, centroids[i], radius=2, color=(255,0,0), thickness=3, lineType=8, shift=0)
                #cv2.circle(img, centroids[i], radius=10, color=(0,0,255), thickness=3, lineType=8, shift=0)
                #cv2.circle(img, centroids[i], radius=50, color=(0,0,255), thickness=3, lineType=8, shift=0)
        return img 

    def listOfPersons(self, centroids, scores, classes):
        threshold = 0.8
        personList = []
        for i in range(len(centroids)):
            if (classes[i] == 1) and (scores[i] > threshold):
                personList.append(centroids[i])
        return personList

