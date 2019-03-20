from person import Person
import math
import copy


class Tracker:
    def __init__(self, threshold:float = 0.1):
        self.idCounter = 0
        self.personDict = {}

    def add_person(self, position):
        self.personDict[self.idCounter] = Person(self.idCounter, position)
        self.idCounter += 1

    def remove_person(self,personId:int):
        self.personDict.pop(personId)

    def flush_person_dict(self):
        self.personDict = {}

    def fill_persondict(self, positions: [(int,int)]):
        # should be called when making a new list of persons
        for p in positions:
            self.add_person(p)

#    def update_person_dict(self, position : [(int,int)], ID):
#        self.personDict[ID].update(position)

    def calculate_distance(self, point, positions):
        closest_dist = 1E10
        closest_point = (-1,-1)
        if positions == []:
            return closest_point, closest_dist
        else:
            for position in positions:
                dist = math.sqrt((position[0] - point[0])**2 + (position[1] - point[1])**2)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_point = position
        return closest_point, closest_dist

    def tracking_algorithm(self, newPositions):
        for Id, person in copy.copy(self.personDict).items():
            lastPosition = person.position_history[-1]
            closest_point, closest_dist = self.calculate_distance(lastPosition, newPositions)
            person.update_threshold()
            person.update_max_skipped()
            v = (closest_point[0] - person.position_history[-1][0], closest_point[1] - person.position_history[-1][1])
            dir_to_cp = person.generate_dir_rads(v)

            if closest_dist <= person.threshold and (person.direction >= dir_to_cp + 0.5 or person.direction <= dir_to_cp - 0.5):
                #self.update_person_dict(closest_point, Id)
                person.update(closest_point)
                person.estimator.update(closest_point)
                person.skipped = 0
                newPositions.remove(closest_point)
            elif closest_dist > person.threshold and (person.direction <= dir_to_cp + 0.5 and person.direction >= dir_to_cp - 0.5):
                person.estimator.update(None)
                new_point = person.estimator.get_position_state()
                person.add_position(new_point)
                person.skipped +=1
                if person.skipped == person.maxSkipped: 
                    self.remove_person(Id)
        
        for point in newPositions:
            self.add_person(point)

    
    
'''    
    # Functions currently not used    
    def eliminate_duplicate_positions(self, positions):
        for position1 in positions:
            for position2 in positions:
                dist = math.sqrt((position1[0]-position2[0])**2 + (position1[1]-position2[1])**2)
                print(dist)
                if 0 < dist < 2:
                    positions.pop(position2)
    
    
    def calculateDistanceFromPersonsToPoints(self, personList, positions):
        distanceDict = {}
        if not personList:
            return distanceDict

        for i in range(len(positions)):
            d = []
            for Id,person in personList.items(): # ERROR: iterates over both keys and persons.
                distance = math.sqrt( (positions[i][0] - person.get_last_position()[0])**2 + (positions[i][1] - person.get_last_position()[1])**2 )
                d.append((Id,distance))
            distanceDict[positions[i]] = d
        return distanceDict 
'''    
