#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:37:51 2020

@author: zzfang
"""

from trueskill import Rating, rate_1vs1
from player import Agent
from my_hex import MyHexBoard
from evaluation import *
import random
import time



"""
Comparing the performance of agent searching with dummy evaluation with depth 3
and that of searching with heuristic evaluation with depth 4

"""

def play(time_of_play, ratings_sillyCat, ratings_greedyCat, board_size=4):
    
    
    beginning_time = time.time()
    rating_sillyCat = Rating()
    rating_greedyCat = Rating()
    
    win_times_s=0 #wintimes of fat cat
    win_times_g=0 #wintimes of silly cat
    
    #Initializing the rating for each agent
    print("rating of silly cat: ", rating_sillyCat)
    print("rating of fat cat: ", rating_greedyCat)
    for i in range(time_of_play):
        hexBoard = MyHexBoard(board_size, dict()) 
        #initialize an empty hexBoard whose size is 4
        colors_of_agents = (MyHexBoard.RED, MyHexBoard.BLUE)
        color_of_sillyCat = random.choice(colors_of_agents)
        color_of_greedyCat = hexBoard.get_opposite_color(color_of_sillyCat)
        #Random decide the color of each agent
        sillyCat = Agent(hexBoard,color_of_sillyCat,eval_func=dummyEvaluation) 
        #agent that searches depth 3 with dummyEvaluation
        greedyCat = Agent(hexBoard,color_of_greedyCat) 
        #agent that searches depth 3 with heuristicEvaluation
        first_move_color = random.choice(colors_of_agents)
        while(not hexBoard.game_over):
            if first_move_color==sillyCat:
                sillyCat.make_move(3)
                greedyCat.make_move(4)
            else:
                greedyCat.make_move(4)
                sillyCat.make_move(3)
                
        #Check the results of each agent
        if hexBoard.check_win(color_of_sillyCat):
            print("Silly Cat wins")
            win_times_s+=1
            hexBoard.print()
            rating_sillyCat, rating_greedyCat = rate_1vs1(rating_sillyCat, rating_greedyCat)
            
        else:
            print("Greedy Cat wins")
            win_times_g+=1
            hexBoard.print()
            rating_greedyCat, rating_sillyCat = rate_1vs1(rating_greedyCat, rating_sillyCat)
            
        ratings_greedyCat.append(rating_greedyCat)
        ratings_sillyCat.append(rating_sillyCat)
            
        print("new rating of greedy cat: ", rating_greedyCat)
        print("new rating of silly cat: ", rating_sillyCat)
        
        
    end_time = time.time()
    print("win times of greedy cat: ",win_times_g)
    print("win times of silly cat: ", win_times_s)
    
    print("Time of The Game; ", end_time-beginning_time)
            
            
    return ratings_sillyCat, ratings_greedyCat# The rating of last time





