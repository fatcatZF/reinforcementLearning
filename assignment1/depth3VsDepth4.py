#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:23:55 2020

@author: zzfang
"""

from trueskill import Rating, rate_1vs1
from player import Agent
from my_hex import MyHexBoard
from evaluation import *
import random
import time



"""
Comparing the performance of agent searching with heuristic evaluation of depth 3
and that of searching with heuristic evaluation of depth 4

"""






def play(time_of_play,  board_size=4):
    ratings_fatCat = []
    ratings_greedyCat = []
    
    beginning_time = time.time()
    rating_fatCat = Rating()
    rating_greedyCat = Rating()
    
    win_times_f=0 #wintimes of fat cat
    win_times_g=0 #wintimes of greedy cat
    
    #Initializing the rating for each agent
    print("rating of fat cat: ", rating_fatCat)
    print("rating of greedy cat: ", rating_greedyCat)
    for i in range(time_of_play):
        hexBoard = MyHexBoard(board_size, dict()) 
        #initialize an empty hexBoard whose size is 4
        colors_of_agents = (MyHexBoard.RED, MyHexBoard.BLUE)
        color_of_fatCat = random.choice(colors_of_agents)
        color_of_greedyCat = hexBoard.get_opposite_color(color_of_fatCat)
        #Random decide the color of each agent
        fatCat = Agent(hexBoard,color_of_fatCat) 
        #agent that searches depth 3 with dummyEvaluation
        greedyCat = Agent(hexBoard,color_of_greedyCat) 
        #agent that searches depth 3 with heuristicEvaluation
        first_move_color = random.choice(colors_of_agents)
        while(not hexBoard.game_over):
            if first_move_color==fatCat.agent_color:
                if hexBoard.game_over:
                    break
                fatCat.make_move(3)
                if hexBoard.game_over:
                    break
                greedyCat.make_move(4)
            else:
                if hexBoard.game_over:
                    break
                greedyCat.make_move(4)
                if hexBoard.game_over:
                    break
                fatCat.make_move(3)
                
        #Check the results of each agent
        if hexBoard.check_win(color_of_fatCat):
            print("Fat Cat wins")
            win_times_f+=1
            hexBoard.print()
            rating_fatCat, rating_greedyCat = rate_1vs1(rating_fatCat, rating_greedyCat)
            
        else:
            print("Greedy Cat wins")
            win_times_g+=1
            hexBoard.print()
            rating_greedyCat, rating_fatCat = rate_1vs1(rating_greedyCat, rating_fatCat)
            
        ratings_fatCat.append(rating_fatCat)
        ratings_greedyCat.append(rating_greedyCat)
            
        print("new rating of fat cat: ", rating_fatCat)
        print("new rating of greedy cat: ", rating_greedyCat)
        
        
    end_time = time.time()
    print("win times of fat cat: ",win_times_f)
    print("win times of greedy cat: ", win_times_g)
    
    print("Time of The Game; ", end_time-beginning_time)
            
            
    return ratings_fatCat, ratings_greedyCat# The rating of last time










if __name__=="__main__":
    board_size = input("Please input the size of board: ")
    time_of_play = input("Please input the times of play: ")
    ratings_fatCat = []
    ratings_greedyCat = []
    ratings_fatCat, ratings_greedyCat = play(time_of_play=int(time_of_play), board_size=int(board_size))
