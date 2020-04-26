#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 00:35:41 2020

@author: Z Fang

https://github.com/fatcatZF/reinforcementLearning

"""
import gym
import numpy as np
#from nn_models import build_train_model

MAX_NUM_OF_EPISODES=1000



def play_game_randomly(number_of_games, verbose=False, render=False):
    winning_times=0
    env = gym.envs.make("MountainCar-v0")
    for game_i in range(number_of_games):
        env.reset()
        if render:
            env.render()
        num_of_steps=0
        while(True):
            num_of_steps+=1
            action=env.action_space.sample()
            observation,reward,done,info=env.step(action)
            if done:
                break
        if num_of_steps<200:
            winning_times+=1
        if verbose:
            print("game:{}, number of steps:{}, final position: {}".format(game_i+1, num_of_steps, observation[0]))
    
    env.close()
    winning_rate=winning_times/number_of_games
    print("winning rate: ", winning_rate)
    
    return winning_rate    



def play_game_reward_based_on_energy(verbose=False):
    env = gym.envs.make("MountainCar-v0")
    env.reset()
    step = 1 #To record number of steps
    previous_observations=[]
    sum_reward=0
    game_memory=[]
    #x_lowest=-0.5
    while(True):
        action=env.action_space.sample()
        observation, env_reward, done, info=env.step(action)
        reward=env_reward
        if len(previous_observations)>0:
            previous_observation=previous_observations[-1]
            h0=abs(previous_observation[0]-(-0.5))
            h1=abs(observation[0]-(-0.5))
            v0=abs(previous_observation[1])
            v1=abs(observation[1])
            game_memory.append((previous_observation,action))
            e0=0.5*v0**2+h0 # energy of previous state
            e1=0.5*v1**2+h1 # energy of current state
            if e1>e0:
                reward=e1-e0
                
        sum_reward+=reward
        if verbose:
            print("Step: {}".format(step))
            print("Action: {}".format(action))
            print("Observation: {}".format(observation))
            print("reward: {}".format(reward))
            print("is done: {}".format(done))
            print("info: {}".format(info))
        step+=1
        previous_observations.append(observation)
        if done:
            break 
        
        
    return game_memory, sum_reward   
    
                
    



def play_game_reward_based_on_energy_v1(verbose=False):
    """
    In this version 
    the reward based on increased energy of the mountain car
    for the velocity, we only consider the positive velocity
    
    """
    env = gym.envs.make("MountainCar-v0")
    env.reset()
    step = 1 #To record number of steps
    previous_observations=[]
    sum_reward=0
    game_memory=[]
    while(True):
        action=env.action_space.sample()
        observation, env_reward, done, info=env.step(action)
        reward=env_reward
        if len(previous_observations)>0:
            previous_observation=previous_observations[-1]
            h0=abs(previous_observation[0]-(-0.5))
            h1=abs(observation[0]-(-0.5))
            v0 = abs(previous_observation[1])
            v1 = abs(observation[1])
           
            game_memory.append((previous_observation,action))
            if not done and h1>h0 and v1>0 and v0>0 and v1 >v0:
                reward=(h1-h0)+0.5*(v1**2-v0**2)
            elif not done and h1>h0:
                reward=h1-h0
            elif not done and v1>0 and v0>0 and v1 >v0 :
                reward=0.5*(v1**2-v0**2)
            else:
                reward=env_reward
            
        sum_reward+=reward
        if verbose:
            print("Step: {}".format(step))
            print("Action: {}".format(action))
            print("Observation: {}".format(observation))
            print("reward: {}".format(reward))
            print("is done: {}".format(done))
            print("info: {}".format(info))
        step+=1
        previous_observations.append(observation)
        if done:
            break  
        
    #print("sum of rewards: ", sum_reward)
    
    return game_memory, sum_reward





 
        
 
def play_game_reward_based_on_position(verbose=False):
    """
    method of Ashok Tankala
    https://medium.com/coinmonks/solving-curious-case-of-mountaincar-reward-problem-using-openai-gym-keras-tensorflow-in-python-d031c471b346
    
    """
    env = gym.envs.make("MountainCar-v0")
    env.reset()
    step = 1 #To record number of steps
    previous_observations=[]
    sum_reward=0
    game_memory=[]
    while(True):
        action=env.action_space.sample()
        observation, env_reward, done, info=env.step(action)
        reward=env_reward
        if len(previous_observations)>0:
            previous_observation=previous_observations[-1]
            game_memory.append((previous_observation, action))
            if observation[0]>-0.2:
                reward=1
                
        sum_reward+=reward
        if verbose:
            print("Step: {}".format(step))
            print("Action: {}".format(action))
            print("Observation: {}".format(observation))
            print("reward: {}".format(reward))
            print("is done: {}".format(done))
            print("info: {}".format(info))
            
        step+=1
        previous_observations.append(observation)
        if done:
            break 
        
        
    return game_memory, sum_reward
        
        
play_funcs = {'position':play_game_reward_based_on_position,
              'energy':play_game_reward_based_on_energy,
              'energy_v1':play_game_reward_based_on_energy_v1}        
            
    
    
       

def prepair_training_data(sum_reward_threshold, number_of_episodes=MAX_NUM_OF_EPISODES,
                          play_func=play_game_reward_based_on_energy_v1, verbose=False):
    training_data=[]
    accepted_scores=[]
    
    for episode in range(number_of_episodes):
        game_memory, sum_reward=play_func()
        if sum_reward>=sum_reward_threshold:
            accepted_scores.append(sum_reward)
            for data in game_memory:
                if data[1]==0: #push left
                    label=[1,0,0]
                elif data[1]==1: #do nothing
                    label=[0,1,0]
                elif data[1]==2: #push right
                    label=[0,0,1]
                
                training_data.append((data[0],label))
                
    if verbose:
        print("accepted scores: ", accepted_scores)
    
    return training_data   

   
    
    
def test_play(number_of_games, model, verbose=False, render=False):
    env = gym.envs.make("MountainCar-v0")
    winning_times=0
    average_number_of_steps=0
    for game_i in range(number_of_games):
        env.reset()
        num_of_steps=0
        previous_observation=None
        while(True):
            if render:
                env.render()
            num_of_steps+=1
            
            if previous_observation is None:
                action=env.action_space.sample()
            else:
                action=np.argmax(model.predict(previous_observation.reshape((-1,2))))
            
            observation,reward,done,info=env.step(action)
            previous_observation=observation
            
            if done:
                break
        
        average_number_of_steps+=num_of_steps    
        if num_of_steps < 200:
            winning_times+=1
        if verbose:
            print("game:{}, number of steps:{}, final position: {}".format(game_i+1, num_of_steps, previous_observation[0]))
    
    env.close()
    winning_rate=winning_times/number_of_games
    average_number_of_steps=average_number_of_steps/number_of_games
    #print("winning rate: ", winning_rate)
    #print("average number of steps: ", average_number_of_steps)
    
    return winning_rate, average_number_of_steps
    
    
    
    
    

