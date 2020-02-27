#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 00:05:58 2020

@author: zzfang
"""
import numpy as np
from my_hex import MyHexBoard
from evaluation import dummyEvaluation
from search import alphabeta
import operator

INF = np.inf


class Agent:
    def __init__(self,hexBoard:MyHexBoard, agent_color,search_func=alphabeta, eval_func=dummyEvaluation):
        self.hexBoard=hexBoard
        self.agent_color = agent_color
        self.eval_func = eval_func
        self.search_func = search_func
        
    
    def find_optimal_move(self,depth):
        #find the optimal move according to minimax score
        movelist = self.hexBoard.getMoveList()
        move_score = dict()
        for move in movelist:
            move_score[move]=self.search_func(self,self.hexBoard.tryMove(move,self.agent_color), depth, self.eval_func, current_color=self.agent_color)
            
        return max(move_score.items(),key=operator.itemgetter(1))[0]
    
       
    def make_move(self,depth):
        #make move according to the result of optimal move
        best_move = self.find_optimal_move(depth)
        self.hexBoard.place(best_move, self.agent_color)
        
        
class Human:
    def __init__(self, hexBoard:MyHexBoard, human_color):
        self.hexBoard = hexBoard
        self.human_color = human_color
        
    def make_move(self, move):
        self.hexBoard.place(move,self.human_color)