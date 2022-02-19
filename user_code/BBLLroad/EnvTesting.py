import myBallBalancerEnv as BBE
import math
import random
env = BBE.BallBalancerEnv()
#print(env.action_space.sample())
#print(env.observation_space.sample())
#print(9.8*math.sin(random.random()*(math.pi/2)))
episodes = 1
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0 
    
    while not done:
        env.render()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score+=reward
        print(done)
    print('Episode:{} Score:{}'.format(episode, score))
