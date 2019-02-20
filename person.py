import numpy as np

class Person:
    def __init__(self, initial_pos:int, idNr:int):
        self.idNr = idNr
        self.positions = []
        self.add_postion(initial_pos)
        # Directions are set as a value between 0 and 2pi.
        # Initialized as -1.0 for unknown.
        self.direction = -1.0

    def add_postion(self, position):
        self.positions.append(position)

    def get_positions(self):
        return self.positions

    def get_last_position(self):
        return self.positions[-1]

    def update_direction(self):

        if(len(self.positions) > 2):
            p1 = self.positions[-3]
            p2 = self.positions[-2]
            p3 = self.positions[-1]
            # vectors
            v1 = (p2[0] - p1[0], p2[1] - p1[1])
            v2 = (p3[0] - p2[0], p3[1] - p2[1])

            self.direction  = np.tan(v1[0] + v2[0], v1[0] + v2[1])

    def get_direction(self):
        return self.direction

    def update(self, position):
        self.add_postion(position)
        self.update_direction()



per = Person(1, 1)
print (per.get_last_position())
