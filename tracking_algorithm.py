import operator

# Each human-object has a direction variable
# Each human-oobject has a history of  points
# Input is a dictionary: D = {(x_coordinate, y_coordinate): (human_id, dist)}
# First: The closest point is the same ID


def tracking_algorithm(dictionary):
	personsUpdated = [] 							# List of human(IDs) that have updated their history
	for point in dictionary: 						# Loop through all new points detected.
		dictionary[point].sort(key=lambda x:x[1])   # For each point, sort the person-coordiante tuples by distance to point. Shortest distancefirst
		for element in dictionary[point]: 			# Loop over all person-coordinate tuples
			(ID,dist) = element						
			if ID not in personsUpdated:			# If the first person-coordinate tuple is free (not in personsUpdated)... 
				#trackerDictionary[ID].update(key)  # add the point to the history of the closest person.
				personsUpdated.append(ID)			# Update the list of persons that have updated their history
				print(ID,dist)
				break