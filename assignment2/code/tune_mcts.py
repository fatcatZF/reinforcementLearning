#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 12:35:57 2020

@author: Z Fang
"""

import numpy as np
from player import Agent, MCTSAgent
from my_hex import MyHexBoard
from trueskill import Rating, rate_1vs1
import random 




def play(itermax, cp, time_of_play=20, board_size=3):
    """
    itermax: maximal iteration times
    cp: exploration/exploitation tradeoff
    
    return: win times, rating of mcts, average expand times
    """
    rating_mctsAgent = Rating() # initial rating of mcts agent
    rating_alphabetaAgent = Rating() #initial rating of alphabeta agent
    win_times_m=0 #initialize wintime of MCTS Agent
    total_expand_times=0
    
    for i in range(time_of_play):
        hexBoard = MyHexBoard(board_size, dict()) 
        #initialize an empty hexBoard whose size is 3
        colors_of_agents = (MyHexBoard.RED, MyHexBoard.BLUE)
        color_of_mctsAgent = random.choice(colors_of_agents)#random select color of mcts agent
        color_of_alphabetaAgent = hexBoard.get_opposite_color(color_of_mctsAgent)
        
        mctsAgent = MCTSAgent(hexBoard,color_of_mctsAgent) 
        #agent that searches depth 4 with dummyEvaluation
        alphabetaAgent = Agent(hexBoard,color_of_alphabetaAgent) 
        #mcts agent  
        
        first_move_color = random.choice(colors_of_agents)#randomly decide which agent move first
        total_expand_times_in_this_game=0 #record total expand time in game i
        while(not hexBoard.game_over):
            if first_move_color==mctsAgent.agent_color:
                if hexBoard.game_over:
                    break
                expand_times=mctsAgent.make_move(itermax, cp, tuning=True)
                total_expand_times_in_this_game+=expand_times
                if hexBoard.game_over:
                    break
                alphabetaAgent.make_move(4) #depth of alphabeta Agent
            else:
                if hexBoard.game_over:
                    break
                alphabetaAgent.make_move(4)
                if hexBoard.game_over:
                    break
                expand_times=mctsAgent.make_move(itermax, cp, tuning=True)
                total_expand_times_in_this_game+=expand_times
        


        total_expand_times+=total_expand_times_in_this_game #compute the total expand times
        
        #Check the results of each agent
        if hexBoard.check_win(color_of_mctsAgent):
            #print("MCTS Agent wins")
            win_times_m+=1
            #hexBoard.print()
            rating_mctsAgent, rating_alphabetaAgent = rate_1vs1(rating_mctsAgent, rating_alphabetaAgent)
            
        else:
            #print("alphabeta Agent wins")
            rating_alphabetaAgent, rating_mctsAgent = rate_1vs1(rating_alphabetaAgent, rating_mctsAgent)
            
            
    average_expand_times=total_expand_times/time_of_play #compute average_expand_times
    
    return win_times_m, rating_mctsAgent.mu, average_expand_times






if __name__=="__main__":
    print("start tuning...")
    repeat_times=10 #Repeating the game 10 times to make the result more convincing
    itermaxs = np.arange(10,110,10) # try itermax from 1o to 1oo
    cps = np.arange(0,3.2,0.2) #try cp(exploration/exploitation tradeoff) from 0 to 3
    
    all_pairs=[]
    for itermax in itermaxs:
        for cp in cps:
            all_pairs.append((itermax,cp))
    
    
    #load the saved data
    itermax_cp_expandtimes=np.load("./tuning_data/itermax_cp_expandtimes.npy").item()
    itermax_cp_wintimes=np.load("./tuning_data/itermax_cp_wintimes.npy").item()
    itermax_cp_mus=np.load("./tuning_data/itermax_cp_mus.npy").item()
    
    tried_pairs=list(itermax_cp_wintimes.keys())
    untried_pairs=[pair for pair in all_pairs if pair not in tried_pairs]#to find untried pairs
    
    tried_number=0
    for pair in untried_pairs:
        print("remaining pairs: ", len(untried_pairs)-tried_number)
        itermax_cp_expandtimes[pair]=[]
        itermax_cp_wintimes[pair]=[]
        itermax_cp_mus[pair]=[]
        
        for i in range(repeat_times):
            win_times_m, mu, average_expand_times=play(pair[0],pair[1])
            itermax_cp_wintimes[pair].append(win_times_m)
            itermax_cp_expandtimes[pair].append(average_expand_times)
            itermax_cp_mus[pair].append(mu)
            
        #Save the result
        np.save("./tuning_data/itermax_cp_wintimes.npy",itermax_cp_wintimes)
        np.save("./tuning_data/itermax_cp_mus.npy",itermax_cp_mus)
        np.save("./tuning_data/itermax_cp_expandtimes.npy",itermax_cp_expandtimes)
        
        tried_number+=1
        
    
    
    


            
        
            
        
        
        
        
        
        
        
        
        
        

