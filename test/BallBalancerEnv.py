from cmath import sin
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random
import math
import pygame
from pygame import gfxdraw
from pandas import array
from typing import Optional
from os import path

class BallBalancerEnv(Env):
    def __init__(self):
        #Defining our action space, can have three possible actions: clockwise turn, counterclockwise turn, and do not move
        self.action_space = Discrete(3)
        #Ball possible positions (low, high)
        self.observation_space = Box(low=np.array([-20]), high=np.array([20]))
        #Ball starting position
        self.state = self.observation_space.sample()/2

        #how many times the machine switches actions
        self.balancing_actions = 50
        #how much time has passed since machine started balancing the ball
        self.time_passed = 0.0

        #for rendering environment
        self.screen = None
        #screen dimensions (1000 by 1000 square)
        self.screen_dim = 1000
    
    def step(self, action):
        self.balancing_actions-= 1 
        self.time_passed += 0.05
        #a little funky, might have to check math here; this calculates how much the ball moves for 0.05 sec after angle changes
        self.state += float((action - 1))*float((9.8*math.sin(random.random()*(math.pi/4))))*self.time_passed*self.time_passed/2
        print(self.state)
        #reward system, have no idea why this is so buggy
        if self.state >=-5 and self.state <=5: 
            reward =1 
        elif self.state >= 20 or self.state <= -20:
            reward = -1
            done = True
        else: 
            reward = -1 
        
        if self.balancing_actions <= 0: 
            done = True
        else:
            done = False
        
        # Set placeholder for info
        info = {}
        
        # Return step information
        return self.state, reward, done, info
    
    def render(self):
        #rendering image of environment, WIP    
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.screen_dim, self.screen_dim))
        self.surf = pygame.Surface((self.screen_dim, self.screen_dim))
        self.surf.fill((213, 242, 98))


    
    def reset(self):
        #reseting enviroment
        #ball placed at new random position
        self.state = self.observation_space.sample()/2
        #reseting balancing time
        self.balancing_actions = 50 
        return self.state
