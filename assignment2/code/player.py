#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 00:05:58 2020

@author: zzfang
"""
import numpy as np
from my_hex import MyHexBoard
from evaluation import *
from search import *
import operator
import time

INF = np.inf


class Agent:
    # alphabeta Agent
    def __init__(self,hexBoard:MyHexBoard, agent_color,search_func=alphabeta, eval_func=heuristicEvaluation):
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
        
        
        
        
class IterativeAgent:
    def __init__(self,hexBoard:MyHexBoard, agent_color, transpositionTable=dict(), search_func=alphabetaWithTranspositionTable, eval_func=heuristicEvaluation):
        self.hexBoard=hexBoard
        self.agent_color = agent_color
        self.eval_func = eval_func
        self.search_func = search_func
        self.transpositionTable = transpositionTable
        
    
    def find_optimal_move(self,duration):
        #find the optimal move according to minimax score
        movelist = self.hexBoard.getMoveList()
        move_score = dict()
        t0 = time.time()
        depth = 0
        t1 = time.time()
        while(t1-t0<duration):
          for move in movelist:
             move_score[move]=self.search_func(self,self.hexBoard.tryMove(move,self.agent_color), depth, self.eval_func, current_color=self.agent_color)
          depth += 1
          t1 = time.time()
        #print("Searched Depth: ", depth)
            
        return max(move_score.items(),key=operator.itemgetter(1))[0]
    
       
    def make_move(self,duration):
        #make move according to the result of optimal move
        best_move = self.find_optimal_move(duration)
        self.hexBoard.place(best_move, self.agent_color)   
        
        
class MCTSAgent:
    def __init__(self, hexBoard:MyHexBoard, agent_color, search_func=mcts):
        self.hexBoard=hexBoard
        self.agent_color=agent_color
        #self.itermax=itermax
        #self.cp=cp
        self.search_func=search_func
        
    def find_optimal_move(self,itermax, cp, tuning=False):
        best_move = self.search_func(self, self.hexBoard, itermax, cp, tuning=tuning)
        return best_move
    
    def make_move(self, itermax=10, cp=0.2, tuning=False):
        if tuning==True:
            best_move, expand_time=self.find_optimal_move(itermax, cp, tuning=True)
        else:
            best_move=self.find_optimal_move(itermax,cp)
        self.hexBoard.place(best_move, self.agent_color)
        
        if tuning==True:
            return expand_time
        
        
  

      
        
        
        
        
        
        
        
        
