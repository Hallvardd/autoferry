import numpy as np
import math
import os

class Person:
    def __init__(self, idNr:int, initial_pos:(int,int)):
        self.idNr = idNr
        self.counted = False
        self.position_history = []
        self.closest_points = []
        self.add_position(initial_pos)
        # Directions are set as a value between 0 and 2pi.
        # Initialized as -1.0 for unknown.
        self.direction = -1.0

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

    def update_direction(self):
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


    def get_direction(self) -> float:
        return self.direction

    def update(self, position):
        self.add_position(position)
        self.update_direction()
