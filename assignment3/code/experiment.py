#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 19:23:58 2020

@author: Z Fang

"""

from mc_games import prepair_training_data, test_play, play_funcs
from nn_models import build_train_model
import pickle

def pipeline(play_func, threshold, number_of_episodes, experiment_times=10, verbose=False):
    """
    play_func: selected function to play
    threshold: the minimal sum of rewards required
    number_of_episodes: number of episodes in each experiment
    """
    
    winning_rates=[]#to record the winning rate in each experiment
    number_of_steps=[] #to record the average number_of_steps in each experiment
    number_of_training_examples=[] #to record the numbber of training examples in each experiment
    
    for experiment_time in range(experiment_times):
        training_data = prepair_training_data(threshold, number_of_episodes, play_func)
        # to obtain training_data
        if len(training_data)==0:
            print("No training data obtained in Experiment {}".format(experiment_time+1))
            continue 
        model = build_train_model(training_data)
        # use the training data to train a neural network model
        winning_rate, average_number_of_steps=test_play(100, model)
        winning_rates.append(winning_rate)
        number_of_steps.append(average_number_of_steps)
        number_of_training_examples.append(len(training_data))
        
        if verbose:
            print("Experiment:{}, Winning rate: {}, Average of Steps: {}".format(experiment_time+1,
                                                                                 winning_rate,
                                                                                 average_number_of_steps,
                                                                                 ))
    return winning_rates, number_of_steps, number_of_training_examples 
        
        


def run_recordData(play_func_name, threshold_range, 
                   episodes_range, experiment_times, verbose=True):
    
    threshold_range=list(threshold_range)
    episodes_range=list(episodes_range)
    
    #winning_rates_file = './experiment_data/'+str(play_func_name)+'_wr'
    #number_of_steps_file = './experiment_data/'+str(play_func_name)+'_ns'
    #number_of_training_file='/experiment_data/'+str(play_func_name)+'_nt'
    
    wr_records = {}
    ns_records = {}
    nt_records = {}
    
    for episodes in episodes_range:
        for threshold in threshold_range:
            key = (episodes, threshold)
            
            winning_rates,number_of_steps, number_of_training = pipeline(play_funcs[play_func_name],
                                                                         threshold,
                                                                         episodes,
                                                                         experiment_times)
            
            if len(winning_rates)!=0:
              mean_wr = sum(winning_rates)/len(winning_rates)
              mean_average_steps = sum(number_of_steps)/len(number_of_steps)
              mean_training = sum(number_of_training)/len(number_of_training)
            
              wr_records[key]=(winning_rates, mean_wr)
              ns_records[key]=(number_of_steps, mean_average_steps)
              nt_records[key] = mean_training
            
            if verbose:
                print("Episodes: {}, Threshold: {}".format(episodes, threshold))
                print("winning rates: ",winning_rates)
                print("average winning rates: ", mean_wr)
                print("number of average steps: ", number_of_steps)
                print("mean average steps: ", mean_average_steps)
                print("average number of training examples: ", mean_training)
            
    
    #with open(winning_rates_file, 'wb') as f:
       # pickle.dump(wr_records, f, protocol=pickle.HIGHEST_PROTOCOL)
        
    #with open(number_of_steps_file, 'wb') as f:
        #pickle.dump(ns_records, f, protocol=pickle.HIGHEST_PROTOCOL)
        
    #with open(number_of_training_file, 'wb') as f:
       # pickle.dump(nt_records, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        
    return wr_records, ns_records, nt_records
        
    
    
    







           
        
        
    
