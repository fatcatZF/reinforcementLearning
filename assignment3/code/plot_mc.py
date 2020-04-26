#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 02:09:00 2020

@author: Z Fang

"""

import matplotlib.pyplot as plt
import pickle 


def get_data(file_path):
    with open(file_path, 'rb') as handle:
        data = pickle.load(handle)
        
    keys = data.keys()
    values = data.values()
    episodes = [key[0] for key in keys][0]
    thresholds = [key[1] for key in keys]
    average_values = [value[1] for value in values]
    
    
    return episodes, thresholds, average_values
    
    
    
    



def make_linechart(x_values, y_values, y_label, title=''):
    plt.title(title)
    plt.plot(x_values, y_values)
    plt.xlabel("threshold")
    plt.ylabel(y_label)
    plt.grid()
    plt.legend()
    


def visualize_data(file_path, y_label="Average Winning Rate"):
    episodes, thresholds, average_values = get_data(file_path)
    make_linechart(thresholds, average_values, y_label=y_label, title="episodes: {}".format(episodes))
    



if __name__=="__main__":
    visualize_data("./experiment_data/energyV1_wr.pickle")



    
    