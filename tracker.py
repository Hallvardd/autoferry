from person import Person


class Tracker:

    def __init__(self, threshold:float = 0.1):
        self.idCounter = 0
        self.persons = {}
        self.threshold = threshold

    def add_person(self, position):
        self.persons[self.idCounter] = {Person(self.idCounter,position)}
        self.idCounter += 1


    def remove_person(self,personId:int):
        self.persons.pop(personId)

    def flush_person_dict(self):
        self.persons = {}


    def fill_persondict(self, positions: [(int,int)]):
        # should be called when making a new list of persons
        for p in positions:
            self.add_person(p)

    def update_persondict(self, postition : [(int,int)]):
        return 0
