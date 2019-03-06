import cv2
import person
import numpy as np

def defineCrossingLine():
	startX = 500
	endX   = 500
	startY = 200
	endY   = 800
	crossingLine = (startX, startY, endX, endY)
	return crossingLine
    #line is in format (xStart,yStart, xEnd,  yEnd)


def drawCrossingLine(crossingLine, img):
	startPoint = (crossingLine[0], crossingLine[1])
	endPoint   = (crossingLine[2], crossingLine[3])
	color      = (255,0,0)
	lineThickness = 2

	cv2.line(img,startPoint,endPoint,color,lineThickness) 


def distanceToLineFromCoordinate(line, coordinate):
	#assume line is in format (xStart,yStart, xEnd,  yEnd)
	#assume coordinate is a np array in format [x1, y1]

	linePoint1 = np.array([int(line[0]), int(line[1])])
	linePoint2 = np.array([int(line[2]), int(line[3])])	

	distance = abs(np.cross(linePoint2-linePoint1,coordinate-linePoint1)/np.linalg.norm(linePoint2-linePoint1))
	return distance  #row vector of the position for coordinate




def countPersons(listOfTrackedPersons, previousCount, crossingLine):
	"""
	This function is going to be called in each iteration of main loop. 
	Assume that a person's coordinates are updated.
	This function returns how many persons that has crossed a line, and updates a person's counted variable.
	A person is counted if a person's last coordinate is close to the crossing line (defined by a threshold)

	inputs:
	*listOfTrackedPersons: (list) [person1, person2, person3,....].	Each person has a history of coordinates
	*previousCount: (int) 3
	*crossingLine: (tuple) (startX, startY, endX, endY). is the line, when person crosses it the person is counted
	

	output:
	*updated number of counted persons
	*updated personList
	"""

	threshold = 5 		#number of pixels
	newCount = previousCount

	for person in listOfTrackedPersons:
		if (person.counted == False and distanceToLineFromCoordinate(crossingLine, person.get_last_position()) < threshold):
			if ( checkIfPersonHasCrossedLine(person, croossingLine) == True ):
				person.set_counted(True)
				newCount += 1

	return newCount, listOfTrackedPersons



def checkIfPersonHasCrossedLine(person, line):
	#has crossed if last position was behind line and current point is in front of line
	#assume that persons walk from left to right in the image.
	#ASSUME LINE IS STRAIGHT DOWN IN THE IMAGE, THUS startX = endX

	coordinateHistory = person.get_position_history()
	isIn
	if (len(coordinateHistory) >= 2):
		if (isPointBehindLine(coordinateHistory[-1], line) == False and isPointBehindLine(coordinateHistory[-2], line) == True):
			return True

def isPointBehindLine(coordinate, line):
	#coordinate: (x,y)
	#assume the line is STRAIGH DOWN, THUS startX = endX (startX, startY, endX, endY)
	assert startX == endX
	if (coordinate[0] < line[startX] ):
		return True
	elif (coordinate[0] > line[startX] and coordinate[1] >= startY and coordinate[1] <= endY):
		return True

def testCount():
	print("testing count")
	person1 = person.Person((300, 300), 1)
	person2 = person.Person((400, 400), 2)
	person3 = person.Person((500, 500), 3)

	personList = [person1, person2, person3]
	crosslingLine = defineCrossingLine()
	prevCount = 0

	n, l = countPersons(personList, prevCount, crosslingLine)
	print(n)
	print(l)


testCount()








	



