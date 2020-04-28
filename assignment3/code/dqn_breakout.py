#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:56:43 2020

@author: Z Fang

https://github.com/fatcatZF/reinforcementLearning

"""

import numpy as np
import gym
import tensorflow as tf
import keras
import random
import matplotlib.pyplot as plt
from IPython.display import clear_output
import random
from keras.utils.vis_utils import plot_model
import copy


def frameProcessor(frame, target_height=84, target_width=84, is_contrast=False, is_plot=False):
    """
    convert the frame to a 84X84 greyscale image
    """
    frame_processed = tf.image.rgb_to_grayscale(frame)
    #convert the frame to greyscale image
    frame_processed = tf.image.crop_to_bounding_box(frame_processed,
                                                   34, 0, 160, 160)
    #downsampling the frame
    frame_processed = tf.image.resize(frame_processed, (target_height, target_width),
                                     method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    
    frame_processed = frame_processed.numpy().reshape((target_height, target_width))
    
    if is_contrast:
        frame_processed[np.where(frame_processed>0)]=1
        frame_processed = frame_processed.astype(np.uint8) 
        
    if is_plot:
        plt.imshow(frame_processed)
        
    
    return frame_processed


def build_cnn_model(model_shape=(84,84,4), output_dim=4, is_contrast=False, is_plot=False):
    state_input = keras.layers.Input(model_shape, name='state_input')
    if is_contrast:
        normalized = keras.layers.Lambda(lambda x: x)(state_input)
        
    else:
        normalized = keras.layers.Lambda(lambda x: x/255)(state_input)
    conv_1 = keras.layers.convolutional.Convolution2D(
              16, (8,8), strides=(4,4), activation='relu')(normalized)
    conv_2 = keras.layers.convolutional.Convolution2D(
              32, (4,4), strides=(2,2), activation='relu')(conv_1)
    conv_flattened=keras.layers.core.Flatten()(conv_2)
    hidden = keras.layers.Dense(256, activation='relu')(conv_flattened)
    output = keras.layers.Dense(output_dim)(hidden)

    model = keras.models.Model(inputs=state_input, outputs=output)
    #optimizer=keras.optimizers.RMSprop(lr=0.00025, rho=0.95, epsilon=0.01)
    optimizer = keras.optimizers.Adam()
    model.compile(optimizer, loss='mse')
    
    if is_plot:
        plot_model(model, to_file='cnn_model.png', show_shapes=True, show_layer_names=True)
    
    return model


#Implement DQN with keras
class DQN():
    def __init__(self,  is_contrast, build_func=build_cnn_model):
        self.model=build_func(is_contrast=is_contrast)
        
        
    def update(self, state, y):
        """
        Update the weights of the network given 
        a training example
        args:
          state: the input to predict
          y: the label
        """
        self.model.fit(np.array([state]), np.array([y]), verbose=0)
        
    def predict(self, state):
        """Compute Q values of all actions for one state"""
        return self.model.predict(np.array([state]))[0]
    
    #def replay(self, replay_buffer, gamma):
        #old replay function
        #batch = replay_buffer.get_minibatch()
        #states=[]
        #targets = []
        #for state, action, next_state, reward, is_done in batch:
            #states.append(state)
            #q_values = self.predict(state)
            #q_values_list = q_values.tolist()
            #if is_done:
                #q_values_list[action]=reward
            #else:
                #q_values_next=self.predict(next_state)
                #q_values_list[action]=reward+gamma*np.max(q_values_next)
                
            #targets.append(np.array(q_values_list))
            
        #states=np.array(states)
        #targets=np.array(targets)
        
        #self.model.fit(states, targets, verbose=0)
        

        
    def replay(self, replay_buffer, gamma):
        """new replay function"""
        #Try to improve replay speed
        batch = replay_buffer.get_minibatch()
        batch_t = list(map(list, zip(*batch))) #Transpose batch list
        states = batch_t[0]
        actions = batch_t[1]
        next_states = batch_t[2]
        rewards = batch_t[3]
        is_dones = batch_t[4]
        
        
        states = np.array(states)
        actions = np.array(actions)
        next_states = np.array(next_states)
        rewards = np.array(rewards)
        is_dones = np.array(is_dones)
        
        is_dones_indices = np.where(is_dones==True)[0]
        
        all_q_values = self.model.predict(states) # predicted q_values of all states
        all_q_values_next = self.model.predict(next_states)
        #Update q values
        all_q_values[range(len(all_q_values)),actions]=rewards+gamma*np.max(all_q_values_next, axis=1)
        all_q_values[is_dones_indices, actions[is_dones]]=rewards[is_dones_indices]
        
        self.model.fit(states, all_q_values, verbose=0)
        

class DDQN(DQN):
    def __init__(self, is_contrast, build_func=build_cnn_model):
        self.model=build_func(is_contrast=is_contrast)
        self.target=copy.deepcopy(self.model)
        
    def replay(self, replay_buffer, gamma):
        """new replay function"""
        #Try to improve replay speed
        batch = replay_buffer.get_minibatch()
        batch_t = list(map(list, zip(*batch))) #Transpose batch list
        states = batch_t[0]
        actions = batch_t[1]
        next_states = batch_t[2]
        rewards = batch_t[3]
        is_dones = batch_t[4]
        
        
        states = np.array(states)
        actions = np.array(actions)
        next_states = np.array(next_states)
        rewards = np.array(rewards)
        is_dones = np.array(is_dones)
        
        is_dones_indices = np.where(is_dones==True)[0]
        
        all_q_values = self.model.predict(states) # predicted q_values of all states
        all_q_values_next = self.target.predict(next_states)
        #Update q values
        all_q_values[range(len(all_q_values)),actions]=rewards+gamma*np.max(all_q_values_next, axis=1)
        all_q_values[is_dones_indices, actions[is_dones]]=rewards[is_dones_indices]
        
        self.model.fit(states, all_q_values, verbose=0)
        
        

class ReplayBuffer():
    """Replay buffer stores the last N transitions"""
    def __init__(self, max_size=100000, history=4, batch_size=32):
        """
        Args: 
          max_size: Number of stored transitions
          history: Number of frames stacked to create a state
          batch_size: Number of transitions returned in a minibatch
          
        """
        self.max_size=max_size
        self.history=history
        self.batch_size=batch_size
        self.clear_amount = int(max_size*0.1)
        # When the memory is full, clear the first 10% elements
        self.frames = [None]*(max_size+1)
        self.actions = [None]*(max_size+1)
        self.next_frames = [None]*(max_size+1)
        self.rewards = [None]*(max_size+1)
        self.is_dones = [None]*(max_size+1)
        self.end=0
        self.indices=[None]*batch_size
        
    def add_experience(self, frame,action, next_frame, reward, is_done):
        """
        form of data: (frame, action, next_frame, reward, is_done)
        
        """
        if self.end==self.max_size: #check whether the memory is full
            self.end-=self.clear_amount
            # Delete the first 10% elements
            del self.frames[:self.clear_amount]
            del self.actions[:self.clear_amount]
            del self.next_frames[:self.clear_amount]
            del self.rewards[:self.clear_amount]
            del self.is_dones[:self.clear_amount]
            #extend the memory
            to_extend = [None]*self.clear_amount
            self.frames.extend(to_extend)
            self.actions.extend(to_extend)
            self.next_frames.extend(to_extend)
            self.rewards.extend(to_extend)
            self.is_dones.extend(to_extend)
            
        self.frames[self.end]=frame
        self.actions[self.end]=action
        self.next_frames[self.end]= next_frame
        self.rewards[self.end]= reward
        self.is_dones[self.end]=is_done
        self.end+=1
        
        
    def get_current_state(self):
        """create current state if there exists at least 4 non-terminal(?) frames ?"""
        #We assume there are 4 non_terminal frames
        #What if there are terminal frames?
        state = self.next_frames[self.end-4:self.end]
        
        #print(state)
        #print(self.end)
        state = [frame.tolist() for frame in state]
        
        #print(np.array(state).shape)
        state = np.array(state)
        state = np.transpose(state, axes=(1,2,0))
        return state
    
    
    def get_valid_indices(self):
        for i in range(self.batch_size):
            while True:
                index = random.randint(self.history, self.end-1)
                
                if True in self.is_dones[index-self.history:index]:
                    continue
                    
                #print("Find valid index")
                    
                break
            self.indices[i]=index
            
    def get_minibatch(self):
        """
        Returns a minibatch 
        """
        #next_states = []
        #actions = []
        batch = []
        self.get_valid_indices()
        
        for idx in self.indices:
            state = self.frames[idx-self.history+1:idx+1]
            state = [frame.tolist() for frame in state]
            state = np.array(state)
            state = np.transpose(state, axes=(1,2,0))
            next_state = self.next_frames[idx-self.history+1:idx+1]
            next_state = np.array(next_state)
            next_state = np.transpose(next_state, axes=(1,2,0))
            #states.append(np.array(state).reshape((84,84,4)))
            #next_states.append(np.array(next_state).reshape(84,84,4))
            action = self.actions[idx]
            reward = self.rewards[idx]
            is_done = self.is_dones[idx]
            
            batch.append((state, action, next_state, reward, is_done))
            
        #states = np.array(states)
        #next_states = np.array(next_states)
        
        return batch
    


def plot_res(values, title=''):   
    ''' Plot the reward curve and histogram of results over time.'''
    # Update the window after each episode
    clear_output(wait=True)
    
    # Define the figure
    
    plt.title(title)
    plt.plot(values, label='Average Rewards')
    plt.axhline(15, c='red',ls='--', label='goal')
    plt.xlabel('Episodes')
    plt.ylabel('Average Reward last 30 episodes')
    x = range(len(values))
    
    # Calculate the trend
    try:
        z = np.polyfit(x, values, 1)
        p = np.poly1d(z)
        plt.plot(x,p(x),"--", label='trend')
    except:
        print('')
        
    plt.legend()
    plt.show()
    
       
    
def q_learning(env, model, episodes, gamma=0.99, epsilon_init=1, 
              eps_decay=9e-5,max_size=100000, batch_size=32, title="DQN", is_contrast=False,
              is_plot=False, verbose=False, 
               use_single_example=False, update_frequency="episode", double=False,
               update_threshold=3000, target_update_frequency=10):
    final=[]# to store total rewards of every game
    average_rewards = [] #to store average reward last 30 times
    replay_time=0
    exploit_time=0
    single_update_times=0
    rbf = ReplayBuffer(max_size=max_size, batch_size=batch_size)# to store replay experience
    episode_i=0
    total_game_steps=0
    for episode in range(episodes):
        episode_i+=1
        
        if double:
            if episode_i%target_update_frequency==0 and episode_i>=update_threshold:
                model.target.set_weights(model.model.get_weights())
        
        
        # reset state
        frame = env.reset()
        is_done = False
        total = 0
        game_steps=0
        epsilon = max(epsilon_init-eps_decay*episode,0.1)
        exploit_time_of_episode=0
        while not is_done:
            #epsilon-greedy
            replay_this_step=False
            
            
            whether_exploit=random.random()
            if whether_exploit < epsilon or game_steps<4:
                
                action = env.action_space.sample()
            else:
                current_state=rbf.get_current_state()
                q_values = model.predict(current_state)
                action = np.argmax(q_values)
                exploit_time+=1
                exploit_time_of_episode+=1
            #Take action and add reward to total
            next_frame, reward, is_done, _ = env.step(action)
            #Update total rewards and replay buffer
            total+=reward
            frame_processed = frameProcessor(frame, is_contrast=is_contrast)
            next_frame_processed = frameProcessor(next_frame, is_contrast=is_contrast)
            #data = [frame, action, next_frame, reward, is_done]
            #print(type(data))
            rbf.add_experience(frame_processed, action, next_frame_processed, reward, is_done)
            game_steps+=1
                            
            
            if  update_frequency=='step' and episode_i>=3000:
                    if rbf.end>=4*batch_size:
            
                       model.replay(rbf, gamma)
                       replay_time+=1
                       replay_this_step=True
            
            elif update_frequency=='buffsize': 
                #only execute replay when replay buffer is full
                if rbf.end>=rbf.max_size:
                    model.replay(rbf,gamma)
                    replay_time+=1
                    replay_this_step=True
                
            
            if game_steps>=4 and use_single_example and random.random()<0.2 and reward>=3:
                next_state = rbf.get_current_state()
                q_values_next = model.predict(next_state)
                q_values[action]=reward+gamma*np.max(q_values_next)
                model.update(current_state, q_values)
                single_update_times+=1    
                
            frame = next_frame
        
        
        if update_frequency=='episode' and episode_i>=3000:
            if rbf.end>=4*batch_size:
            
                       model.replay(rbf, gamma)
                       replay_time+=1
                       #replay_this_step=True
            
        #Update epsilon
        #epsilon = max(epsilon*eps_decay, 0.1)
        final.append(total)
        total_game_steps+=game_steps
        
        
        
        if len(final)<30:
            average_reward = sum(final)/len(final)
            
        else:
            average_reward = sum(final[-30:])/30
            
        average_rewards.append(average_reward)
        
        if is_plot:
            plot_res(average_rewards, title)
           
        if verbose:
            print("episode: {}, average_reward: {}, reward of this time: {}, tatal game steps: {} ".format(episode_i,
                                                                                  average_reward,
                                                                                  total, total_game_steps))
            
            print("replay times: ", replay_time)            
            print("Single Update times: ", single_update_times)            
            print("exploit times: ", exploit_time)            
            print("total exploit rate: ", exploit_time/total_game_steps)            
            print("exploit rate of this episode: ", exploit_time_of_episode/game_steps)            
            print("Replay Buff taken: ", rbf.end)
            
        
        
            
        
    return final, average_rewards





def experiment():
    print("Please input the parametres: ")
    episodes = int(input("please input episodes: "))
    max_size=int(input("please input the max size of replay buffer: "))
    batch_size=int(input("please input the batch size: "))
    update_frequency=input("please input update frequency: episode, buffsize or step: ")
    if update_frequency=="episode":
        update_threshold=int(input("from which episode the training of the predict model starts?: "))
    is_contrast=input("Do you want to use setAllNonZeroPixelsToOne preprocessing(True or False): ")
    if is_contrast=="True":
        is_contrast=True
    else:
        is_contrast=False
    use_single_example=input("Do you want to use hybrid training method(True or False): ")
    if using_single_example=="True":
        using_single_example=True
    else:
        using_single_example=False
    
    
    double = input("Do you want to use DDQN(True or False): ")
    
    #print(double)
    
    if double=="True":
        target_update_frequency=int(input("Please input the target network update frequency: "))
        
    
    env = gym.envs.make("BreakoutDeterministic-v4")
        
    if double:
        dqn=DDQN(is_contrast)
    else:
        dqn=DQN(is_contrast)
        
    final, average_rewards = q_learning(env, dqn, episodes,
                                        is_contrast=is_contrast,
                                        verbose=True,
                                        use_single_example=use_single_example,
                                        is_plot=True,
                                        max_size=max_size,
                                        batch_size=batch_size,
                                        update_threshold=update_threshold,
                                        double=double)







        
    
if __name__ == "__main__":
    
    experiment()
    


