#!/usr/bin/env python
# coding: utf-8

# In[7]:


get_ipython().system('pip install pygame')
get_ipython().system('pip install tensorflow==2.3.0')
get_ipython().system('pip install gym')
get_ipython().system('pip install keras')
get_ipython().system('pip install keras-rl2')


# # Environment Class Declaration

# In[75]:


from cmath import sin
from gym import Env
from gym import spaces
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
    ### Observation Space
    #The observation is a `ndarray` with shape `(4,)` where the elements correspond to the following:
    #| Num | Observation           | Min                  | Max                |
    #|-----|-----------------------|----------------------|--------------------|
    #| 0   | Ball Position         | -max_state           | max_state          |
    #| 1   | Ball Velocity         | -Inf                 | Inf                |
    
    ### Action Space
    #The action space is Discrete 3 (clockwise(0), no turn (1), counterclockwise (2))
    
    def __init__(self):
        #Defining our action space, can have three possible actions: clockwise turn, counterclockwise turn, and do not move
        self.action_space = Discrete(3)
        #max position of the ball before it falls off stick
        self.max_state = 20.0
        self.max_reward_position = self.max_state / 4
        
        high = np.array(
            [
                float(self.max_state), #Ball Position
                np.finfo(np.float32).max #Max Ball Velocity
            ]
        )
        
        #Ball possible positions (low, high)
        self.observation_space = spaces.Box(-high, high)
        
        #Ball starting position
        self.position = random.randint(-self.max_state,self.max_state)/2.0
        #how many times the machine switches actions
        self.balancing_actions = 50
        #the angle of the stick -90, 90 for completely vertical
        self.stick_angle = 0
        #acceleration adds to velocity
        self.ball_velocity = 0.0
        #for rendering environment
        self.screen = None
        #screen dimensions (1000 by 1000 square)
        self.screen_dim = 800
        
    def step(self, action):
        self.balancing_actions-= 1
        
        #lets say for each action, the stick rotates 3 degrees
        self.stick_angle += (action-1)*3;
        
        #acceleration adds to velocity
        acc = -math.sin(math.radians(self.stick_angle)) * 9.81
        self.ball_velocity += acc
        
        # assuming each step is 1 sec, then self.position increments by velocity
        self.position += self.ball_velocity
        
        #reward system
        done = False
        if self.position >=-self.max_reward_position and self.position <=self.max_reward_position: 
            reward = 1 
        elif self.position >= self.max_state or self.position <= -self.max_state:
            reward = -1
            self.position = 0
            done = True
        else: 
            reward = -1 
        
        if self.balancing_actions <= 0: 
            done = True
        
        
        # Set placeholder for info
        info = {}
        
        # Return step information
        return np.array((self.position, self.ball_velocity), dtype=np.float32), reward, done, info
    
    def render(self, mode="human"):
        #defining variables
        stateToWidthRatio = 18
        stickWidth = self.max_state * stateToWidthRatio * 2
        stickHeight = stickWidth / 15
        stickX = self.screen_dim / 2
        stickY = 2 * self.screen_dim / 3;
        ballRadius = 40.0
        disStickToBall = stickHeight/2+ballRadius
        newX = stickX + disStickToBall * math.sin(math.radians(self.stick_angle))
        newY = stickY - disStickToBall * math.cos(math.radians(self.stick_angle))
        ballX = newX - self.position * stateToWidthRatio * math.cos(math.radians(self.stick_angle))
        ballY = newY - self.position * stateToWidthRatio * math.sin(math.radians(self.stick_angle))
        
        l, r, t, b = (
            -stickWidth / 2,
            stickWidth / 2,
            stickHeight / 2,
            -stickHeight / 2,
        )
        
        #rotate stick by stick_angle
        stickCoords = []
        for coord in [(l, b), (l, t), (r, t), (r, b)]:
            coord = pygame.math.Vector2(coord).rotate_rad(math.radians(self.stick_angle))
            stickCoords.append(coord)
        
        #add stickX and stickY to stickCoords
        stickCoords = [(c[0] + stickX, c[1] + stickY) for c in stickCoords]

        #rendering image of environment, starting screen
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.screen_dim, self.screen_dim))
        
        # Fill background
        background = pygame.display.get_surface()
        background = background.convert()
        background.fill((200, 200, 200))
        
        # Display some text
        font = pygame.font.Font(None, 36)
        string = "Position: " + str(self.position)
        text = font.render(string, 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)
        
        # Draw Stick
        gfxdraw.aapolygon(background, stickCoords, (129, 132, 203))
        gfxdraw.filled_polygon(background, stickCoords, (129, 132, 203))
        
        # Draw Ball
        gfxdraw.aacircle(
            background,
            int(ballX),
            int(ballY),
            int(ballRadius),
            (202, 152, 101),
        )
        gfxdraw.filled_circle(
            background,
            int(ballX),
            int(ballY),
            int(ballRadius),
            (202, 152, 101),
        )
        
        #This will pump the event queue and close the window and program
        #if the user clicks the close button of the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
                
        # Blit everything to the screen
        self.screen.blit(background, (0, 0))
        pygame.display.flip()
        return True
    
    def setAngle(angle)
        self.stick_angle = angle
        
    def setBallPosition(position)
        self.position = position
                         
    def reset(self):
        #reseting enviroment
        #ball placed at new random position
        self.position = random.randint(-self.max_state,self.max_state)/2
        #reseting balancing time
        self.balancing_actions = 50 
        #reseting velocity
        self.ball_velocity = 0.0
        #the angle of the stick -90, 90 for completely vertical
        self.stick_angle = 0
        return np.array((self.position, self.ball_velocity), dtype=np.float32)
    
    def close(self):
        pygame.display.quit() 
        pygame.quit()


# # Random Sampling Of Environment

# In[101]:


#import BallBalancerEnv as BBE
import math
import random
import time
env = BallBalancerEnv()

episodes = 10
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0 
    
    while not done:
        env.render()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score+=reward
        
        #help make it visual
        time.sleep(0.05)
    print('Episode:{} Score:{}'.format(episode, score))
    
env.close()


# # Training Environment

# In[69]:


get_ipython().system('pip install stable-baselines3[extra]')
import gym 
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy


# In[76]:


env = DummyVecEnv([lambda: env])
del model
model = PPO('MlpPolicy', env, verbose = 1)
model.learn(total_timesteps=50000)


# In[98]:


model.learn(total_timesteps=20000)


# In[618]:


from stable_baselines3.common.evaluation import evaluate_policy
evaluate_policy(model, env, n_eval_episodes=10, render=False)
env.close()


# # Test Model

# In[103]:


import math
import random
import time
env = BallBalancerEnv()

episodes = 50
score_sum = 0
for episode in range(1, episodes+1):
    obs = env.reset()
    score = 0
    
    while True:
        action, _states = model.predict(obs)
        
        #TODO: link actions to servo motor output
        
        #TODO: (maybe?) update _states to better represent real world's observations.
        # i.e. in the env:
        #    self.stick_angle = [the servo motor's current angle];
        #    self.ball_position = [the real ball position];
        
        #
        env.setAngle()
        
        #position goes from -1 to 1
        env.setPosition()
        
        obs, rewards, done, info = env.step(action)
        score += rewards
        
        #comment out these lines to make testing go faster
        env.render()
        time.sleep(0.05)
        
        if done: 
            print('Episode:{} Score:{}'.format(episode, score))
            score_sum += score
            break
        
env.close()
score_average = score_sum / episodes
print('Average Score:{}'.format(score_average))


# In[ ]:





# In[ ]:




