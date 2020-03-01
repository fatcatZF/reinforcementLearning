#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:18:21 2020

@author: zzfang
"""

import numpy as np
from my_hex import MyHexBoard
#from player import Agent


INF = np.inf





def alphabeta(agent, hexBoard:MyHexBoard, depth, eval_func, current_color=MyHexBoard.BLUE, alpha=-INF, beta=INF):
        #compute the minimax score of every possible move of current color
        opposite_color = hexBoard.get_opposite_color(current_color)
        movelist = hexBoard.getMoveList()
        next_states = [hexBoard.tryMove(move,current_color) for move in movelist]
        # Record all next states(hexBoards)
        
        if hexBoard.game_over or depth==0:
            return eval_func(hexBoard,agent.agent_color)
        
        elif current_color == agent.agent_color:
            #computing max value
            g = -INF                
            for state in next_states:
                g = max(g, alphabeta(agent,state, depth-1, eval_func, current_color=opposite_color,alpha=alpha, beta=beta))
                alpha = max(alpha,g)
                if g>=beta:
                    break #beta cutoff
                    
        elif current_color == hexBoard.get_opposite_color(agent.agent_color):
            #computing min value
            g = INF
            for state in next_states:
                g = min(g, alphabeta(agent,state,depth-1, eval_func, current_color=opposite_color, alpha=alpha, beta=beta))
                beta = min(beta,g)
                if g<=alpha:
                    break #cutoff
                    
        else: 
            print("Wrong Color")
            
        return g



def alphabetaWithTranspositionTable(agent, hexBoard:MyHexBoard, depth, eval_func, current_color=MyHexBoard.BLUE, alpha=INF, beta=INF):
    #alphabeta prunning with transposition table
    transpositionTable = agent.transpositionTable #accept transposition table from iterative agent
    opposite_color = hexBoard.get_opposite_color(current_color)
    movelist = hexBoard.getMoveList()
    next_states = [hexBoard.tryMove(move,current_color) for move in movelist]
        # Record all next states(hexBoards)
        
    board_key = tuple(hexBoard.board.items())
    if board_key in transpositionTable.keys():
        return transpositionTable[board_key]
    
    
    if hexBoard.game_over or depth==0:
        return eval_func(hexBoard,agent.agent_color)
        
    elif current_color == agent.agent_color:
            #computing max value
        g = -INF                
        for state in next_states:
            
            g = max(g, alphabeta(agent,state, depth-1, eval_func, current_color=opposite_color,alpha=alpha, beta=beta))
            alpha = max(alpha,g)
            if g>=beta:
                break #beta cutoff
                    
    elif current_color == hexBoard.get_opposite_color(agent.agent_color):
            #computing min value
        g = INF
        for state in next_states:
            g = min(g, alphabeta(agent,state,depth-1, eval_func, current_color=opposite_color, alpha=alpha, beta=beta))
            beta = min(beta,g)
            if g<=alpha:
                break #cutoff
                    
    else: 
        print("Wrong Color")
        
    transpositionTable[board_key]=g
            
    return g

    
    
    
    
    
    
    
    
    
    
    


        
        
        
        
        
        
        
        
        
        
        
        