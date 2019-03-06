from person import Person
import math
import copy


class Tracker:
    def __init__(self, threshold:float = 0.1):
        self.idCounter = 0
        self.personDict = {}
        self.threshold = threshold

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

    def update_persondict(self, postition : [(int,int)], ID):
        return 0

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
            
    def calculate_distance(self, point, positions):
        closest_dist = 100000
        closest_point = (-1,-1)
        if positions == []:
            return point,0
        else:
            for position in positions:
                dist = math.sqrt( (position[0] - point[0])**2 + (position[1] - point[1])**2 )
                if dist < closest_dist:
                    closest_dist = dist
                    closest_point = position
        return closest_point, closest_dist

    def tracking_algorithm(self, newPositions):
        for Id, person in copy.copy(self.personDict).items():
            if newPositions == []:
                break
            lastPosition = person.position_history[-1]
            closest_point, closest_dist = self.calculate_distance(lastPosition, newPositions)
            if closest_dist < person.threshold:
                self.personDict[Id].update(closest_point)
                newPositions.remove(closest_point)
            elif closest_dist >= person.maxthreshold:
                self.remove_person(Id)

        for point in newPositions:
            self.add_person(point)

'''
    def tracking_algorithm(self, dictionary):
        personsInFrame = len(dictionary)
        personsRegistered = len(self.personDict)
        personsUpdated = []
        personsOut = [] 
        personsAdded = []
        if not dictionary                            # List of human(IDs) that have updated their history
        # Update history
        for position in dictionary:                        # Loop through all new points detected.
            dictionary[position].sort(key=lambda x:x[1])   # For each point, sort the person-coordiante tuples by distance to point. Shortest distancefirst
            for Id,dist in dictionary[position]:           # Loop over all person-coordinate tuples                     
                if (Id not in personsUpdated) and dist < 200:
                    self.personDict[Id].update(position)
                    personsUpdated.append(Id)
                    break
                else:
                    personsAdded.append(Id)
                    break


        for Id,person in self.personDict.items():
            if Id not in personsUpdated:
                personsOut.append(Id) 

        for Id in personsOut:
            self.remove_person(Id)

'''

