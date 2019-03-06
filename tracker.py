from person import Person
import math


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

    def tracking_algorithm(self, dictionary):
        personsUpdated = []                                # List of human(IDs) that have updated their history
        for position in dictionary:                        # Loop through all new points detected.
            dictionary[position].sort(key=lambda x:x[1])   # For each point, sort the person-coordiante tuples by distance to point. Shortest distancefirst
            found = False
            for element in dictionary[position]:           # Loop over all person-coordinate tuples
                (ID,dist) = element
                if ID not in personsUpdated:
                    self.personDict[ID].update(position)
                    personsUpdated.append(ID)
                    found = True
                    break
            if not found:
                self.add_person(position)

    def calculateDistanceFromPersonsToPoints(self, personList, positions):
        distanceDict = {}
        for i in range(len(positions)):
            d = []
            for Id,person in personList.items():
                distance = math.sqrt( (positions[i][0] - person.get_last_position()[0])**2 + (positions[i][1] - person.get_last_position()[1])**2 )
                d.append((Id,distance))
            distanceDict[positions[i]] = d
        return distanceDict #returned value is an np array where each element contains an np array of distances for a person. element 0 in distances contains distance from person 0 to all coordinates in coordiateList
