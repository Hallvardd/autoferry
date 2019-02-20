import numpy as np
import tensorflow as tf
import cv2
from person import Person


def movePerson(stepX, stepY,  person):
	position = person.get_last_position()
	#print("newPos", newPos[1])
	newPosition = (position[0] + stepX, position[1] + stepY)
	person.add_position(newPosition)
	return person


def plotPersonDot(img, person):
	x = (person.get_last_position())[0]
	y = (person.get_last_position())[1]
	cv2.line(img, (int(x), int(y)), (int(x),int(y)), (0,255,0), 2)




def distanceToLine(line, dots):
	#assume line is in format (xStart,yStart, xEnd,  yEnd)
	#assume dot is in format a numpy matrix[[x1, y1],
	# 						  				[x2, y2]]
	#each row are dots for a different person
	#also works if dots has one entry of(x,y)
	linePoint1 = np.array([int(line[0]), int(line[1])])
	linePoint2 = np.array([int(line[2]), int(line[3])])	


	distance = abs(np.cross(linePoint2-linePoint1,dots-linePoint1)/np.linalg.norm(linePoint2-linePoint1))
	return distance  #row vector of the position for all dots

def count(personList, crossingLine):
	#personList is np row array of person objects
	epsilon = 3 #unit is pixels
	counter = 0

	for i in range (personList.shape[0]):
		personPosition = np.array(personList[i].get_last_position() )
		if distanceToLine(crossingLine, personPosition) < epsilon and personList[i].get_counted() == False:
			counter += 1
			personList[i].set_counted(True)
	return counter




def countingLoop():
    #img = np.zeros((512,512,3), np.uint8)
    cap = cv2.VideoCapture('rtsp://admin:autogruppe4@192.168.0.100//Streaming/Channels/101')    
    lineX = 800
    point1 = (lineX-100,200)
    point2 = (lineX+300,600)
    crossingLine = (point1[0], point1[1], point2[0], point2[1])
    color = (255,0,0)
    lineThickness = 2
    time = 0
    counter = 0
    epsilon = 3
    stepX = 1
    stepY = 0
    person1 = Person((500,300), 0)
    person2 = Person((300, 250), 0)
    person3 = Person((600, 230), 0)
    personList = np.array([person1, person2, person3])

    while True:
        time += 1
        r, img = cap.read()
        img = cv2.resize(img, (1280, 720))
        cv2.line(img,point1,point2,color,lineThickness) 

        for i in range(personList.shape[0]): 
            personList[i] = movePerson(stepX, stepY,  personList[i])
            plotPersonDot(img, personList[i])
        counter += count(personList, crossingLine)
        print(counter)
        cv2.imshow("preview", img)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break



countingLoop()

#there is a problem when a person bounding box dissapear
#functionality to convert list of persons to a matrix of dot positions as a matrix array
#check if direction of a person is towards the crossingline 
#must define when counter resets - must probably recieve external signal.

#keep a list of persons: check that list size is same as number of boxes. 