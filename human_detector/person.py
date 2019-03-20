from __future__ import division
import numpy as np
import math
import os
import cv2
import kalmanFilter
import nonLinReg
import statistics as stat

class Person:
    def __init__(self, idNr:int, initial_pos:(int,int)):
        self.idNr = idNr
        self.counted = False
        self.position_history = []
        self.add_position(initial_pos)
        # Directions are set as a value between 0 and 2pi.
        # Initialized as -1.0 for unknown.
        self.direction = -1.0
        self.minThreshold = 15
        self.maxThreshold = 70
        self.skipped = 0
        self.maxSkipped = 3 
        self.threshold = self.minThreshold
        self.estimator = kalmanFilter.KalmanFilter(x0=np.array([[initial_pos[0]],
                                                                [initial_pos[1]],
                                                                [initial_pos[0]],
                                                                [initial_pos[1]],
                                                                [self.minThreshold],
                                                                [self.minThreshold]]),
                                                   p0 = 0.1*np.eye(6, dtype='float'), 
                                                   Q = 0.01*np.eye(6), 
                                                   R = math.sqrt(5)*np.eye(2))

    def get_idNr(self) -> int:
        return self.idNr

    def get_counted(self) -> bool:
        return self.counted

    def set_counted(self, counted:bool):
        self.counted = counted

    def add_position(self, position:float):
        self.position_history.append(position)

    def get_position_history(self) -> [(int,int)]:
        return self.position_history

    def get_last_position(self) -> (int,int) :
        return self.position_history[-1]

    def generate_dir_rads(self, vector) -> float:
        direction = -1.0
        if (vector[0] < 0 and vector[1] > 0):
            direction = np.pi/2 + np.arctan(vector)[1]
        elif(vector[0] < 0 and vector[1] < 0) :
            direction = np.pi + np.abs(np.arctan(vector)[1])
        elif(vector[0] > 0 and vector[1] < 0):
            direction = ((3*np.pi)/2) + np.abs(np.arctan(vector)[1])
        else:
            direction = np.arctan(vector)[1]
        return direction

    def update_direction2(self):
        if(len(self.position_history) > 2):
            # the last 3 recorded points.
            p1 = self.position_history[-3]
            p2 = self.position_history[-2]
            p3 = self.position_history[-1]
            # vectors
            v1 = (p2[0] - p1[0], p2[1] - p1[1])
            v2 = (p3[0] - p2[0], p3[1] - p2[1])
            # Added vector
            v3 = np.array([v1[0] + v2[0], v1[0] + v2[1]])
            self.direction = self.generate_dir_rads(v3)

        elif(len(self.position_history) == 2):
            p1 = self.position_history[-2]
            p2 = self.position_history[-1]
            # vectors
            v1 = (p2[0] - p1[0], p2[1] - p1[1])
            self.direction = self.generate_dir_rads(v1)

    def update_direction(self):
        directions = []
        if len(self.position_history) >= 5:    
            for i in range(int(len(self.position_history)/5)):
                batch = self.position_history[i*5:(i+1)*5]
                p1 = batch[0]
                p2 = batch[-1]
                v = (p2[0] - p1[0], p2[1] - p1[1])
                directions.append(self.generate_dir_rads(v))
        else:
            p1 = self.position_history[0]
            p2 = self.position_history[-1]
            v = (p2[0] - p1[0], p2[1] - p1[1])
            directions.append(self.generate_dir_rads(v))
        
        self.direction = stat.mean(directions)
        

    def get_direction(self) -> float:
        return self.direction

    def update(self, position):
        self.add_position(position)
        self.update_direction()

    def draw_path(self,img):
        for i in range(len(self.position_history)-1):
            p1 = self.position_history[i]
            p2 = self.position_history[i+1]
            cv2.line(img,p1,p2,(0,255,0),1)
        return img

    def update_threshold(self):
        self.threshold = (self.skipped/self.maxSkipped)*self.maxThreshold + self.minThreshold

    def update_max_skipped(self):
        if len(self.position_history) > 5:
            self.skippedMax = 7
        else:
            self.skippedMax = 2 # Assume detection where wrong if two detectios appear in four frames
