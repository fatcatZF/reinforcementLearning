#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:35:54 2020

@author: z fang
"""

from hex_skeleton import HexBoard

class MyHexBoard(HexBoard):
    
    def __init__(self, board_size, board=dict()):
        self.board = board
        self.size = board_size
        self.game_over = False
        if self.board==dict():
            #print("board is empty")
            for x in range(board_size):
              for y in range (board_size):
                self.board[x,y] = HexBoard.EMPTY
    
    
    
    def getMoveList(self):
        #Explore all the possible possitions(empty coordinates) to move
        movelist = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i,j]==3:
                    movelist.append((i,j))
                    
        return movelist
    
    
    
    def tryMove(self, move, color):
        #return a MyHexBoard object to simulate the move
        try_board = self.board.copy()
        try_board[move]=color
        try_hexBoard=MyHexBoard(self.size,board=try_board.copy())
        if try_hexBoard.check_win(HexBoard.RED) or try_hexBoard.check_win(HexBoard.BLUE):
            try_hexBoard.game_over = True
        return try_hexBoard
        
        
        
    
    
    def unMakeMove(self):
        pass

