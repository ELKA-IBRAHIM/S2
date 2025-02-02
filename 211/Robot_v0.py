# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20  2023
Updated on Tue Jan 30  2024
Updated on Tue Jan 28  2024

@author: Kieffer
"""

import numpy as np
import matplotlib.pyplot as plt

class Robot_in_Room:
    walls = np.array([])
    nb_walls = 0
    
    p = np.array([])
    
    sensors = np.array([])
    nb_sensors = 0
    
    y = np.array([])
    
    def __init__(self,p):
        # Location of walls (global frame)
        self.walls = np.array([[[0,8],[0,0]],
                          [[6,8],[0,8]],
                          [[6,6],[6,8]],
                          [[10,6],[6,6]],
                          [[10,0],[10,6]],
                          [[0,0],[10,0]],
                          [[6,2],[5,4]],
                          [[5,4],[7,5]],
                          [[7,5],[8,3]],
                          [[8,3],[6,2]]])
        
        self.nb_walls = self.walls.shape[0]
        
        # Location of sensors (robot frame)
        self.sensors = np.array([[0.5,0.25,np.pi/4],
                                 [0.5,-0.25,-np.pi/4],
                                 [-0.5,0.25,3*np.pi/4],
                                 [-0.5,-0.25,-3*np.pi/4]])
        
        self.nb_sensors = self.sensors.shape[0]
        
        # Position and orientation of robot frame
        self.p = p
        
        self.y = self.get_sensor_readings()
        
    # Return sensor location and orientation in global frame
    def sensor_glob_frame(self):
        s = np.zeros([self.nb_sensors,3])
        for m in range(self.nb_sensors):
            s[m,0] = self.p[0]+self.sensors[m,0]*np.cos(self.p[2])-self.sensors[m,1]*np.sin(self.p[2])
            s[m,1] = self.p[1]+self.sensors[m,0]*np.sin(self.p[2])+self.sensors[m,1]*np.cos(self.p[2])
            s[m,2] = self.sensors[m,2] + self.p[2]
            
        return s
    
    # Check whether sensor on right side of wall
    def visible(self,s,wall):
        sensor = self.sensor_glob_frame() #Tous les capteurs!!!
        print(sensor)
        xs = sensor[0]
        ys = sensor[1]
        
        
        t = [wall[0][0]-wall[0][1], wall[1][0]-wall[1][1]]
        n = [-t[1], t[0]]

        vec = np.array([xs - wall[1][0], ys-wall[1][1]])

        signe = vec[0]*n[0] + vec[1]*n[1]

        return signe > 0

                
    
    # Get Sensor Readings
    def get_sensor_readings(self):
        # simulated distances
        ym = np.zeros(self.nb_sensors)

        # A compléter
        return ym
        
    # Plots
    def plot(self):
        # Walls
        for m in range(self.nb_walls):
            plt.plot(self.walls[m,:,0], self.walls[m,:,1], 'b', linestyle="-")
            
        # Sensors
        s = self.sensor_glob_frame()
        for i in range(self.nb_sensors):
            plt.plot([s[i,0],s[i,0] + self.y[i]*np.cos(s[i,2])], \
                     [s[i,1],s[i,1] + self.y[i]*np.sin(s[i,2])], 'ro', linestyle="--")

        plt.axis('square')
        plt.show()

      

walls = np.array([[[0,8],[0,0]],
                          [[6,8],[0,8]],
                          [[6,6],[6,8]],
                          [[10,6],[6,6]],
                          [[10,0],[10,6]],
                          [[0,0],[10,0]],
                          [[6,2],[5,4]],
                          [[5,4],[7,5]],
                          [[7,5],[8,3]],
                          [[8,3],[6,2]]])



p_star = np.array([2,2,0.8])     
    
myproblem = Robot_in_Room(p_star)

ym = myproblem.get_sensor_readings()        
myproblem.plot()
            
#print('Simulated distances : ',ym)

s = np.array([0.5,0.25,np.pi/4])
print(myproblem.sensor_glob_frame())
#for wall in walls:
    #print(myproblem.visible(s,wall))
    