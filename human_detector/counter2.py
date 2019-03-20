import cv2
import person
import numpy as np


def defineCrossingLine():
	startX = 940
	endX   = 940
	startY = 50
	endY   = 300
	crossingLine = (startX, startY, endX, endY)
	return crossingLine
    #line is in format (xStart,yStart, xEnd,  yEnd)


def drawCrossingLine(crossingLine, img):
	startPoint = (crossingLine[0], crossingLine[1])
	endPoint   = (crossingLine[2], crossingLine[3])
	color      = (255,0,0)
	lineThickness = 2

	cv2.line(img,startPoint,endPoint,color,lineThickness) 




def point_to_line_dist(point, line):
    """Calculate the distance between a point and a line segment.
	from : https://stackoverflow.com/questions/27161533/find-the-shortest-distance-between-a-point-and-line-segments-not-line
    To calculate the closest distance to a line segment, we first need to check
    if the point projects onto the line segment.  If it does, then we calculate
    the orthogonal distance from the point to the line.
    If the point does not project to the line segment, we calculate the 
    distance to both endpoints and take the shortest distance.

    :param point: tuple (x,y), describing the point.
    :type point: numpy.core.multiarray.ndarray
    :param line: list of endpoint arrays of form [P1, P2]
    :type line: list of numpy.core.multiarray.ndarray
    :return: The minimum distance to a point.
    :rtype: float
    """
    

    point = np.array([point[0], point[1]])
    line = np.array([ [line[0], line[1]] , [line[2], line[3]]])

    unit_line = line[1] - line[0]
    norm_unit_line = unit_line / np.linalg.norm(unit_line)

    # compute the perpendicular distance to the theoretical infinite line
    segment_dist = (
        np.linalg.norm(np.cross(line[1] - line[0], line[0] - point)) /
        np.linalg.norm(unit_line)
    )

    diff = (
        (norm_unit_line[0] * (point[0] - line[0][0])) + 
        (norm_unit_line[1] * (point[1] - line[0][1]))
    )

    x_seg = (norm_unit_line[0] * diff) + line[0][0]
    y_seg = (norm_unit_line[1] * diff) + line[0][1]

    endpoint_dist = min(
        np.linalg.norm(line[0] - point),
        np.linalg.norm(line[1] - point)
    )

    # decide if the intersection point falls on the line segment
    lp1_x = line[0][0]  # line point 1 x
    lp1_y = line[0][1]  # line point 1 y
    lp2_x = line[1][0]  # line point 2 x
    lp2_y = line[1][1]  # line point 2 y
    is_betw_x = lp1_x <= x_seg <= lp2_x or lp2_x <= x_seg <= lp1_x
    is_betw_y = lp1_y <= y_seg <= lp2_y or lp2_y <= y_seg <= lp1_y
    if is_betw_x and is_betw_y:
        return segment_dist
    else:
        # if not, then return the minimum distance to the segment endpoints
        return endpoint_dist


def countPerson(person, crossingLine):
	"""
	This function is going to be called in each iteration of main loop. 
	Assume that a person's coordinates are updated.
	This function returns how many persons that has crossed a line, and updates a person's counted variable.
	A person is counted if a person's last coordinate is close to the crossing line (defined by a threshold)

	inputs:
	*person is one person object.	Each person has a history of coordinates
	*previousCount: (int) 3
	*crossingLine: (tuple) (startX, startY, endX, endY). is the line, when person crosses it the person is counted
	
	
	output:
	*updated number of counted persons
	*isCounted is True if person is counted
	"""

	threshold = 10		#number of pixels
	num_points_threshold = 3
	#newCount = previousCount
	isCounted = False
	#print("DISTANCE FROM LINE   ", point_to_line_dist( person.get_last_position(), crossingLine))
	#point_to_line_dist( person.get_last_position(), crossingLine)
	num_points_behind_line, num_points_in_front_of_line  = checkNumOfPointsBehindAndInFrontOfLine(person, crossingLine)
	print("num points behind line: ", num_points_behind_line, "   num points in front of line ", num_points_in_front_of_line)
	if (person.counted == False
		and num_points_behind_line >= num_points_threshold and num_points_in_front_of_line >= num_points_threshold):
			if (len(person.get_position_history()) >= 5 ):			#a person must have existed longer than 5 frames before counted
				isCounted = True
				print("COUNTED")
				#newCount += 1		

	return isCounted


def checkNumOfPointsBehindAndInFrontOfLine(person, line):
	#ASSUME LINE IS STRAIGHT DOWN IN THE IMAGE, THUS startX = endX
	LINE_X_INDEX = 0
	POINT_X_INDEX = 0
	POINT_Y_INDEX = 1
	LINE_Y_INDEX = 2
	assert line[LINE_X_INDEX] == line[LINE_Y_INDEX]
	coordinateHistory = person.get_position_history()
	count_in_front = 0
	count_behind = 0
	if (len(coordinateHistory) >= 2):
		for i in range(len(coordinateHistory)):
			if (personIsInYRange(coordinateHistory[-i][POINT_Y_INDEX], line) and coordinateHistory[-i][POINT_X_INDEX] < line[LINE_X_INDEX]):
				count_behind += 1
			elif (personIsInYRange(coordinateHistory[-i][POINT_Y_INDEX], line) and coordinateHistory[-i][POINT_X_INDEX] >= line[LINE_X_INDEX]):
				count_in_front += 1
	return count_behind, count_in_front

def personIsInYRange(y, line):
	if (y >= line[3] and y <= line[1]):
		return True
	else:
		return False


def checkIfPersonHasCrossedLine(person, line):
	#has crossed if last position was behind line and current point is in front of line
	#assume that persons walk from left to right in the image.
	#ASSUME LINE IS STRAIGHT DOWN IN THE IMAGE, THUS startX = endX

	coordinateHistory = person.get_position_history()

	if (len(coordinateHistory) >= 2):
		if (isPointBehindLine(coordinateHistory[-1], line) == False and isPointBehindLine(coordinateHistory[-3], line) == True):
			return True

def isPointBehindLine(coordinate, line):
	#coordinate: (x,y)
	#assume the line is STRAIGH DOWN, THUS startX = endX (startX, startY, endX, endY)
	startX, startY, endX, endY = line
	assert startX == endX
	if (coordinate[0] < line[startX] ):
		return True
	elif (coordinate[0] > line[startX] and coordinate[1] >= startY and coordinate[1] <= endY):
		return True

def testCount():
	print("testing count")
	person1 = person.Person(1, (300, 300))
	person2 = person.Person(2, (400, 400))
	person3 = person.Person(3, (500, 500))

	personList = [person1, person2, person3]
	crosslingLine = defineCrossingLine()
	prevCount = 0

	d = point_to_line_dist((840,122), crosslingLine)
	print("dist ", d)
	#n, l = countPerson(person1, prevCount, crosslingLine)
	#print(n)
	#print(l)




