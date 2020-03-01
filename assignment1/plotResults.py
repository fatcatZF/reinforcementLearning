#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 22:02:46 2020

@author: z fang
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_result(xlist, y1list, y2list, agent_labels):
    plt.plot(xlist, y1list, color = 'red', label=agent_labels[0])
    plt.plot(xlist, y2list, color = 'blue', label=agent_labels[1])
    plt.xticks(np.arange(1,21))
    plt.xlabel("Number of Games")
    plt.ylabel("Skill(Mean Value)")
    plt.grid()
    plt.legend()
    plt.show()
    
    
def plot_cv(xlist, cv1, cv2, agent_labels):
    plt.plot(xlist, cv1, color='green', label=agent_labels[0])
    plt.plot(xlist, cv2, color='yellow', label=agent_labels[1])
    plt.xticks((np.arange(1, 21)))
    plt.xlabel("Number of Games")
    plt.ylabel("Coefficient of Variance")
    plt.grid()
    plt.legend()
    plt.show()