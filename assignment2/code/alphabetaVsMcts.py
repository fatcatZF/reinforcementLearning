#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 22:58:15 2020

@author: Abhishek
"""



from trueskill import Rating, rate_1vs1
from player import MCTSAgent, Agent
from my_hex import MyHexBoard
from evaluation import *
import random
import time



"""
Comparing the performance of alphabeta agent 
and mcts agent
"""






def play(time_of_play, board_size=4):
    
    ratings_mctsAgent=[] #ratings of mcts agent
    ratings_alphabetaAgent=[] # ratings of alphabeta agent
    beginning_time = time.time() 
    rating_mctsAgent = Rating() # initial rating of mcts agent
    rating_alphabetaAgent = Rating() #initial rating of alphabeta agent
    
    win_times_m=0 #wintimes of mcts agent
    win_times_a=0 #wintimes of alphabeta agent
    
    #Initializing the rating for each agent
    print("rating of fat cat: ", rating_mctsAgent)
    print("rating of greedy cat: ", rating_alphabetaAgent)
    for i in range(time_of_play):
        hexBoard = MyHexBoard(board_size, dict()) 
        #initialize an empty hexBoard whose size is 4
        colors_of_agents = (MyHexBoard.RED, MyHexBoard.BLUE)
        color_of_mctsAgent = random.choice(colors_of_agents)
        color_of_alphabetaAgent = hexBoard.get_opposite_color(color_of_mctsAgent)
        #Random decide the color of each agent
        mctsAgent = MCTSAgent(hexBoard,color_of_mctsAgent) 
        #agent that searches depth 3 with dummyEvaluation
        alphabetaAgent = Agent(hexBoard,color_of_alphabetaAgent) 
        #agent that searches  with iterative deepen and tranposition table
        first_move_color = random.choice(colors_of_agents)
        while(not hexBoard.game_over):
            if first_move_color==mctsAgent.agent_color:
                if hexBoard.game_over:
                    break
                mctsAgent.make_move()
                if hexBoard.game_over:
                    break
                alphabetaAgent.make_move(4) #depth of alphabeta Agent
            else:
                if hexBoard.game_over:
                    break
                alphabetaAgent.make_move(4)
                if hexBoard.game_over:
                    break
                mctsAgent.make_move()
                
        #Check the results of each agent
        if hexBoard.check_win(color_of_mctsAgent):
            print("MCTS Agent wins")
            win_times_m+=1
            hexBoard.print()
            rating_mctsAgent, rating_alphabetaAgent = rate_1vs1(rating_mctsAgent, rating_alphabetaAgent)
            
        else:
            print("alphabeta Agent wins")
            win_times_a+=1
            hexBoard.print()
            rating_alphabetaAgent, rating_mctsAgent = rate_1vs1(rating_alphabetaAgent, rating_mctsAgent)
            
        ratings_mctsAgent.append(rating_mctsAgent)
        ratings_alphabetaAgent.append(rating_alphabetaAgent)
            
        print("new rating of mcts agent: ", rating_mctsAgent)
        print("new rating of alphabeta agent: ", rating_alphabetaAgent)
        
        
    end_time = time.time()
    print("win times of mcts agent: ",win_times_m)
    print("win times of alphabeta agent: ", win_times_a)
    
    print("Time of The Game; ", end_time-beginning_time)
            
            
    return ratings_mctsAgent, ratings_alphabetaAgent # The rating of last time



if __name__=="__main__":
    board_size = input("Please input the size of board: ")
    time_of_play = input("Please input the times of play: ")
    ratings_mctsAgent = []
    ratings_alphabetaAgent = []
    ratings_mctsAgent, ratings_alphabetaAgent = play(time_of_play=int(time_of_play), board_size=int(board_size))
