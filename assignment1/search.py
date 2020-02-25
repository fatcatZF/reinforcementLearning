#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:18:21 2020

@author: zzfang
"""
import operator
import numpy as np
from my_hex import MyHexBoard
from evaluation import dummyEvaluation

INF = np.inf

class Agent:
    def __init__(self,hexBoard:MyHexBoard, agent_color,eval_func=dummyEvaluation):
        self.hexBoard=hexBoard
        self.agent_color = agent_color
        self.eval_func = eval_func
        
        
    
    def alphabeta(self,hexBoard, eval_func, current_color=MyHexBoard.BLUE, alpha=-INF, beta=INF):
        #compute the minimax score of every possible move of current color
        opposite_color = hexBoard.get_opposite_color(current_color)
        movelist = hexBoard.getMoveList()
        next_states = [hexBoard.tryMove(move,current_color) for move in movelist]
        # Record all next states(hexBoards)
        
        if hexBoard.game_over:
            return eval_func()
        
        elif current_color == self.agent_color:
            #computing max value
            g = -INF                
            for state in next_states:
                g = max(g, self.alphabeta(state,eval_func, current_color=opposite_color,alpha=alpha, beta=beta))
                alpha = max(alpha,g)
                if g>=beta:
                    break #beta cutoff
                    
        elif current_color == self.hexBoard.get_opposite_color(self.agent_color):
            #computing min value
            g = INF
            for state in next_states:
                g = min(g, self.alphabeta(state, eval_func, current_color=opposite_color, alpha=alpha, beta=beta))
                beta = min(beta,g)
                if g<=alpha:
                    break #cutoff
                    
        else: 
            print("Wrong Color")
            
        return g
        
        
    
    def find_optimal_move(self):
        #find the optimal move according to minimax score
        movelist = self.hexBoard.getMoveList()
        move_score = dict()
        for move in movelist:
            move_score[move]=self.alphabeta(self.hexBoard.tryMove(move,self.agent_color), self.eval_func, current_color=self.agent_color)
            
        #print(move_score)
            
        return max(move_score.items(),key=operator.itemgetter(1))[0]
    
       
    def make_move(self):
        #make move according to the result of optimal move
        best_move = self.find_optimal_move()
        self.hexBoard.place(best_move, self.agent_color)
        
        
        
        
        
        
        
        
        
        
        
        