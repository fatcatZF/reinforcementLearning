#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:18:21 2020

@author: zzfang
"""

import numpy as np
from my_hex import MyHexBoard
import operator
import random
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






class StateNode():
   def __init__(self,hexBoard:MyHexBoard, agent_color, move_parent=None, w=0, n=0, cp=2):
       """
       hexBoard: a MyHexBoard object represent the board of hex
       parent: the parent of this node
       w: wintimes
       n: number of times this node has been visited
       cp: coefficient of exploration
       move_parent: the parent of this node and its corresponding move (move, parent)
       """
       self.hexBoard=hexBoard
       self.agent_color = agent_color
       self.parents={} #record the move and corresponding parent node
       self.w=w
       self.n=n
       self.cp=cp
       self.children={} #record the move and corresponding children node
       self.triedMoves=[]
       if move_parent!=None: #if this node is added by its parent through a move
           self.parents[move_parent[0]]=move_parent[1]
           
   def add_child(self, move):
       #use the move(a coordinate) to generate a child state
       hexBoard_copy = MyHexBoard(self.hexBoard.size, self.hexBoard.board.copy()) #copy the hexBoard
       hexBoard_copy.place(move, self.agent_color)
       opposite_color = hexBoard_copy.get_opposite_color(self.agent_color)
       child = StateNode(hexBoard_copy, opposite_color, move_parent=(move, self))
       #The agent color of the child node should be opposite to current agent color
       self.children[move]=child
       self.triedMoves.append(move) #record this tried move
       
   
   def get_children(self):
       #return a children's dictionary
       return self.children
   
   def get_parents(self):
       #return parents' dictionary
       return self.parents
   
   def get_untriedMoves(self):
       all_moves = self.hexBoard.getMoveList()
       return [move for move in all_moves if move not in self.triedMoves]
   
   def compute_children_uct(self):
       #Compute the uct value for every possible move/child
       children_uct = {}
       for move in self.triedMoves:
           children_uct[move]=self.compute_uct(self.children[move])
           
       return children_uct
   
    
   def compute_uct(self, child):
       #Compute the uct of one child
       nj = child.n 
       wj = child.w
       n = self.n 
       return wj/nj+self.cp*np.sqrt(np.log(n)/nj)
       
       
       
   
   


def mcts(agent, hexBoard:MyHexBoard, itermax, cp, tuning=False):
    """
    args:
      agent: an MCTSAgent object using mcts
      hexBoard: a MyHexBoard object 
      itermax: maxnumber of iteration
      cp: coefficient of exploration(to control exploration/exploitation tradeoff)

    Return:
      The child visited max times
    """
    agent_color = agent.agent_color
    rootnode = StateNode(hexBoard, agent_color, cp=cp)
    expand_time=0

    for i in range(itermax):
        node = rootnode
        path = [] # to store the node in the mcts process
        path.append(node)

        
        #Select
        #select the child with max uct value
        while node.get_untriedMoves()==[] and list(node.children.keys())!=[]:
            #node is fully expanded and non-terminal(has children)
            expand_time+=1
            children_uct = node.compute_children_uct()#compute the uct of children/moves
            move = max(children_uct.items(),key=operator.itemgetter(1))[0]
            node = node.children[move]
            path.append(node)
    
            
        #Expand
        #get untried moves of a node and randomly select one
        if node.get_untriedMoves()!=[]: #if we can expand(i.e. state/node is non terminal)
            untriedMoves = node.get_untriedMoves()
            move = random.choice(untriedMoves)
            node.add_child(move) #add child and descend tree
            node = node.children[move]
            path.append(node) #add the expanded node to the path
            
        #Playout
        while node.hexBoard.getMoveList()!=[] and not node.hexBoard.game_over:#while state is non-terminal
            move_list = node.hexBoard.getMoveList()
            move = random.choice(move_list)
            node.add_child(move)
            node = node.children[move] 
            path.append(node)
            
        #Check the result(win or loss) and Backpropagation
        delta_n = 1
        if node.hexBoard.check_win(agent_color):
            delta_w=1
        else:
            delta_w=0
            
        for j in range(len(path)-1,-1,-1):
            #update w and n of the nodes in the path
            node = path[j]
            node.n+=delta_n
            node.w+=delta_w
            
            
    
    children_of_root = rootnode.children
    move_visitTime = {} #move and corresponding visited times
    for move in children_of_root.keys():
        move_visitTime[move]=children_of_root[move].n
        
        
    if tuning==True:
        #return the optimal move and expand times
        return max(move_visitTime.items(),key=operator.itemgetter(1))[0], expand_time
        
        
    return max(move_visitTime.items(),key=operator.itemgetter(1))[0]
    
        
            
            
            
            
    
    
    
    
    
    
    


        
        
        
        
        
        
        
        
        
        
        
        