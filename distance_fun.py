import numpy as np
import tensorflow as tf
import cv2
from person import Person
import math

person1 = Person((500,300), 1)
person1.add_position((600,300))
person2 = Person((300, 250), 2)
person3 = Person((600, 230), 3)
personList = [person1, person2, person3]

p1 = (600,300)
p2 = (300,300)
p3 = (200,320)
coordList = [p1, p2, p3]



def calculateDistanceFromPersonsToPoints(personList, coordinateList):
	#assume personLIst and Coodinate list are arrays of person objects and coordinate tuples on the form: [person1, person2, ...] and [(x1,y1), (x2, y2)]	d = []
	#it also works if personList and coordinateList are numpy arrays
	assert len(personList) == len(coordinateList)

	distances = []
	distanceObject = []
	for i in range(len(coordinateList)):
		d = []
		for j in range(len(personList)):
			distance = math.sqrt( (coordinateList[i][0] - personList[j].get_last_position()[0])**2 + (coordinateList[i][1] - personList[j].get_last_position()[1])**2 )
			d.append(  (personList[j].get_idNr(), distance)   )
		distanceDict = {tuple(coordinateList[i]): d}
		distanceObject.append(distanceDict)	
	print(distanceObject)

	return distanceObject #returned value is an np array where each element contains an np array of distances for a person. element 0 in distances contains distance from person 0 to all coordinates in coordiateList 
	



