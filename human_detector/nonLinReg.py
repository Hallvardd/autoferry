import numpy as np
import statistics as stat
import matplotlib.pyplot as plt

class Estimator:
    def __init__(self):
        self.window_length = 300
        self.deg = 4
        self.x = np.empty((0, self.deg))
        self.y = np.empty((0, 1))
        self.w = np.zeros((self.deg, 1))
        self.index = 0
        self.distance_history = [0]*self.window_length
        self.distance = 0
        self.previous_point = (-1,-1)

    def update_weights(self):
        self.w = np.linalg.pinv(self.x.T @ self.x) @ self.x.T @ self.y

    def generate_x_vector(self,x):
        x_vector = np.zeros(self.deg)
        x_vector[0] = 1 
        for i in range(1,self.deg):
            x_vector[i] = x**i    
        return x_vector.reshape((self.deg,1))

    def add_new_point(self, new_point):
        if self.previous_point == (-1,-1):
            self.previous_point = new_point
        (x,y) = new_point
        x_vector = self.generate_x_vector(x).T
        y_vector = np.array([[float(y)]])
        print(self.y)
        print(y_vector)
        if self.x.shape[0] < self.window_length:
            self.x = np.concatenate((self.x, x_vector),axis=0)
            self.y = np.concatenate((self.y, y_vector),axis=0)
        else:
            self.x[self.index % self.window_length][:] = x_vector
            self.y[self.index % self.window_length][:] = y_vector
            
        self.distance_history[self.index % self.window_length] =  float(new_point[0]-self.previous_point[0])
        self.previous_point = new_point
        self.distance = 0.85*stat.mean(self.distance_history)
        
        self.index += 1 
    
    def get_estimate(self):
        x_est = self.previous_point[0] + self.distance
        y_est = float(self.w.T @ self.generate_x_vector(x_est))
        return (int(x_est), int(y_est))


if __name__ == "__main__":
    estimator = Estimator()
    x_points = np.array([[30],[30],[30],[40],[50],[60],[70],[80],[90],[100],[100],[100],[100],[100],[100],[100]]) + np.random.normal(loc=0.0, scale=4.0, size=(16,1))
    y_points = np.array([[10],[20],[30],[40],[50],[60],[70],[80],[90],[100],[120],[140],[150],[160],[180],[190]]) + np.random.normal(loc=0.0, scale=4.0, size=(16,1))
   
    counter = 0
    while True:
        img = np.zeros((200,200,3))
        
        for x,y in zip(x_points,y_points):
            img[int(x)][int(y)] = (255,0,0) 

        new_point = (x_points[counter],y_points[counter])
        
        estimator.add_new_point(new_point)
        estimator.update_weights()
        
        # Generate curve
        x,y = [],[]
        
        for i in range(0,200,1):
            x.append(i)
            y.append(float(estimator.generate_x_vector(i).T @ estimator.w))
        
        for x1,y1 in zip(x,y):
            if abs(y1) > 200:
                break
            else:
                img[int(x1)][int(y1)] = (0,255,0)
        
        # Estimate next
        est_x,est_y = estimator.get_estimate()
        img[int(est_x)][int(est_y)] = (0,0,255)

        plt.imshow(img)
        plt.show()

        counter += 1
