import numpy as np
import cv2
import os
import sys

# Displays all images in a database

class Display:
    def __init__(self, database_path, display_size, image_type):
        self.database_path = database_path
        self.database = {}
        self.display_size = display_size
        self.image_to_display = np.zeros(display_size)
        self.image_type = image_type

    def load_images_from_database(self):
        for filename in os.listdir(self.database_path):
            if filename.endswith(self.image_type):
                img = cv2.imread(self.database_path + '/' + filename)
                img = cv2.resize(img, self.display_size)
                self.database[filename[:-len(self.image_type)]] = img

    def show_images_loaded(self):
        for key, img in self.database.items():
            cv2.imshow(key,img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__ == "__main__":
    path = sys.path[0] + '/database'
    disp = Display(database_path=path, display_size=(1800,900), image_type='.jpg')
    disp.load_images_from_database()
    while(True):
        cv2.imshow('Image', disp.database[input('>>>')])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

