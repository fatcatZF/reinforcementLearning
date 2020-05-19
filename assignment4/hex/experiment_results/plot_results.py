#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 19:58:21 2020

@author: s2289164
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np

with open("./self_ep5simN100cp1AgainstIDTT.pkl", 'rb') as f:
    data = pickle.load(f)
    
    
    
    
mus_idtt = [x.mu for x in data['ratings_idtt']]
mus_self_ep5simN100cp1 =[x.mu for x in data['ratings_selfplay']] 
episodes = range(1,11)    
    
plt.plot(episodes,mus_idtt, color='green',label='ID-TT')
plt.plot(episodes, mus_self_ep5simN100cp1, color='blue',label='self-play')
plt.xticks(np.arange(1,11))
plt.xlabel("episodes")
plt.ylabel("elo rating")
plt.grid()
plt.legend()
plt.show()