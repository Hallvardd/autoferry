from __future__ import division
import numpy as np
import string
import matplotlib.pyplot as plt

class KalmanFilter:
    def __init__(self, x0, p0, Q, R):
        self.N = 5
        self.A = np.array([[1,0,0,0,1,0],
                           [0,1,0,0,0,1],
                           [1,0,0,0,0,0],
                           [0,1,0,0,0,0],
                           [(1/self.N),0,-(1/self.N),0,(1-1/self.N),0],
                           [0,(1/self.N),0,-(1/self.N),0,(1-1/self.N)]], dtype='float')

        self.H = np.array([[1,0,0,0,0,0],
                           [0,1,0,0,0,0]], dtype='float')
        self.Q = Q
        self.R = R
        self.K = None
        self.x_bar = x0
        self.x_hat = None
        self.p_bar = p0
        self.p_hat = None

    def update_kalman_gain(self):
        self.K = self.p_bar @ self.H.T @ np.linalg.inv(self.H @ self.p_bar @ self.H.T + self.R)
        #print("K shape: ", self.K.shape)

    def state_estimate_update(self, y):
        if None in y: 
            self.x_hat = self.x_bar
        elif y.shape == (2,1):
            self.x_hat = self.x_bar + self.K @ (y - self.H @ self.x_bar)
            #print("Update :", self.K @ (y - self.H @ self.x_bar))
            #print("X_hat shape: ", self.x_hat.shape)
        else:
            print("Measurement error")

    def covariance_update(self):
        self.p_hat = (np.eye(6) - self.K @ self.H) @  self.p_bar @ (np.eye(6) - self.K @ self.H).T + self.K @ self.R @ self.K.T

    def state_estimation_propagation(self):
        self.x_bar = self.A @ self.x_hat

    def covariance_propagation(self):
        self.p_bar = self.A @ self.p_hat @ self.A.T + self.Q
    
    def measurement_transform(self, point):
        if point == None:
            return np.array([[None],[None]])
        else:
            px,py = point
            return np.array([[px],[py]])

    def update(self, point):
        y = self.measurement_transform(point)
        self.update_kalman_gain()
        self.state_estimate_update(y)
        self.covariance_update()
        self.state_estimation_propagation()
        self.covariance_propagation()

    def get_position_state(self):
        return (int(self.x_hat[0]), int(self.x_hat[1]))


if __name__ == "__main__":
    x0 = np.array([[10],[10],[0],[0],[20],[20]])
    p0 = np.eye(6, dtype='float')
    Q = 0.01*np.eye(6)
    R = 0.01*np.eye(2)
    kf = KalmanFilter(x0, p0, Q, R)
    
    test_img = np.zeros([100,100])
    test_img[int(x0[0])][int(x0[1])] = 100
    while True:
        px = int(input("X-coordinate: "))
        py = int(input("Y-coordinate: "))
        if (px or py) == -1:
            print("Not int")
            kf.update(None)
        else:
            kf.update((px,py))
        
        print("Current point :", kf.get_position_state())
        print("State vector :", kf.x_hat)
        
        test_img[int(kf.x_hat[0])][int(kf.x_hat[1])] = 100
        plt.imshow(test_img)
        plt.show()
