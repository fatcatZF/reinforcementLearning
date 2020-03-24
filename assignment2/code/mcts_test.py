#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 23:45:50 2020

@author: Z Fang
"""

from my_hex import MyHexBoard
from player import MCTSAgent
import matplotlib.pyplot as plt


board = {(0,0):1,(0,1):3,(0,2):3,(1,0):3,(1,1):2,(1,2):2,(2,0):1,(2,1):3,(2,2):3}
hex_board = MyHexBoard(3, board=board) # Create a hexboard with given board

test_agent=MCTSAgent(hex_board, MyHexBoard.RED) #Create a test agent with given hexBoard

position_times={} #record the returned position and corresponding times

for i in range(1000):
    position = test_agent.find_optimal_move(10,1)
    if position not in position_times.keys():
        position_times[position]=1
    else:
        position_times[position]+=1
        

labels = list(position_times.keys()) #positions as labels
sizes = list(position_times.values())#returned times as sizes
plt.pie(sizes, labels=labels)
plt.axis('equal')
plt.show()

    