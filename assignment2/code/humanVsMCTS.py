#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 22:16:46 2020

@author: zzfang
"""

import time
from my_hex import MyHexBoard
from player import MCTSAgent, Human


print("Welcome to Hex!")
time.sleep(2.5)
print("^ --- ^")
print("(~ v ~)")


size_of_board = int(input("Please input the size of board: "))
hexBoard = MyHexBoard(size_of_board)




print("Game Start!")
print("-----------")
print("Please enter the color which you want to play(Blue or Red): ")
human_color = input().lower()

if human_color == 'blue':
    human_color = MyHexBoard.BLUE
    agent = MCTSAgent(hexBoard, MyHexBoard.RED)
    
else:
    human_color = MyHexBoard.RED
    agent = MCTSAgent(hexBoard, MyHexBoard.BLUE)
    
human = Human(hexBoard,human_color)


while(not hexBoard.game_over):
    hexBoard.print()
    print("Please enter the coordinate:")
    cx = int(input())
    cy = int(input())
    human.make_move((cx,cy))
    if hexBoard.game_over:
        break
    agent.make_move()
    

print("Game Over")


if hexBoard.check_win(human_color):
    print("Congratuations! You win the game")
else:
    print("You lost!")

hexBoard.print()

