#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 23:45:56 2020

@author: zzfang
"""

from trueskill import Rating, rate_1vs1
from player import MCTSAgent, IterativeAgent
from my_hex import MyHexBoard
from evaluation import *
import random
import time



"""
Comparing the performance of iterative agent 
and mcts agent
"""






def play(time_of_play, board_size=4):
    
    ratings_mctsCat=[]
    ratings_iCat=[]
    beginning_time = time.time()
    rating_mctsCat = Rating()
    rating_iCat = Rating()
    
    win_times_m=0 #wintimes of fat cat
    win_times_i=0 #wintimes of greedy cat
    
    #Initializing the rating for each agent
    print("rating of fat cat: ", rating_mctsCat)
    print("rating of greedy cat: ", rating_iCat)
    for i in range(time_of_play):
        hexBoard = MyHexBoard(board_size, dict()) 
        #initialize an empty hexBoard whose size is 4
        colors_of_agents = (MyHexBoard.RED, MyHexBoard.BLUE)
        color_of_mctsCat = random.choice(colors_of_agents)
        color_of_iCat = hexBoard.get_opposite_color(color_of_mctsCat)
        #Random decide the color of each agent
        mctsCat = MCTSAgent(hexBoard,color_of_mctsCat) 
        #agent that searches depth 3 with dummyEvaluation
        iCat = IterativeAgent(hexBoard,color_of_iCat) 
        #agent that searches  with iterative deepen and tranposition table
        first_move_color = random.choice(colors_of_agents)
        while(not hexBoard.game_over):
            if first_move_color==mctsCat.agent_color:
                if hexBoard.game_over:
                    break
                mctsCat.make_move()
                if hexBoard.game_over:
                    break
                iCat.make_move(6) #duration of search
            else:
                if hexBoard.game_over:
                    break
                iCat.make_move(6)
                if hexBoard.game_over:
                    break
                mctsCat.make_move()
                
        #Check the results of each agent
        if hexBoard.check_win(color_of_mctsCat):
            print("MCTS Cat wins")
            win_times_m+=1
            hexBoard.print()
            rating_mctsCat, rating_iCat = rate_1vs1(rating_mctsCat, rating_iCat)
            
        else:
            print("icat wins")
            win_times_i+=1
            hexBoard.print()
            rating_iCat, rating_mctsCat = rate_1vs1(rating_iCat, rating_mctsCat)
            
        ratings_mctsCat.append(rating_mctsCat)
        ratings_iCat.append(rating_iCat)
            
        print("new rating of mcts cat: ", rating_mctsCat)
        print("new rating of icat: ", rating_iCat)
        
        
    end_time = time.time()
    print("win times of mcts cat: ",win_times_m)
    print("win times of i cat: ", win_times_i)
    
    print("Time of The Game; ", end_time-beginning_time)
            
            
    return ratings_mctsCat, ratings_iCat# The rating of last time



if __name__=="__main__":
    board_size = input("Please input the size of board: ")
    time_of_play = input("Please input the times of play: ")
    ratings_mctsCat = []
    ratings_iCat = []
    ratings_mctsCat, ratings_iCat = play(time_of_play=int(time_of_play), board_size=int(board_size))
