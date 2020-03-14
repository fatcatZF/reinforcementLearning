#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:13:36 2020

@author: zzfang
"""

import numpy as np 
from my_hex import MyHexBoard
from boardToGraph import boardToGraph, getWeightedSubgraph, findShortestPath, computeScoreOfPath

def dummyEvaluation(hexBoard=None, agent_color=None):
    #This dummy evaluation function is a random number generator
    return np.random.randint(0,10)



def heuristicEvaluation(hexBoard:MyHexBoard, agent_color):
    
    human_color = hexBoard.get_opposite_color(agent_color)
    board_graph = boardToGraph(hexBoard)
    agent_subgraph = getWeightedSubgraph(board_graph, agent_color)
    human_subgraph = getWeightedSubgraph(board_graph, human_color)
    
    if agent_color== MyHexBoard.RED:
        agent_path = findShortestPath(agent_subgraph,'down','top')
        human_path = findShortestPath(human_subgraph,'left','right')
    else:
        agent_path = findShortestPath(agent_subgraph,'left','right')
        human_path = findShortestPath(human_subgraph, 'down','top')
    
    agent_score = computeScoreOfPath(agent_subgraph, agent_path)
    human_score = computeScoreOfPath(human_subgraph, human_path)
    
    return human_score-agent_score
    
        
    