#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 20:15:17 2020

@author: zzfang
"""

from my_hex import MyHexBoard
import networkx as nx
from networkx.classes.function import set_node_attributes
import numpy as np

def boardToGraph(hexBoard:MyHexBoard):
    
    board = hexBoard.board
    board_graph = nx.Graph() #Create board graph
    node_list = list(board.keys())
    board_graph.add_nodes_from(node_list)
    board_graph.add_nodes_from(['top','down','left','right'])
    colors = board.copy()
    colors['top']='outside'
    colors['down']='outside'
    colors['left'] = 'outside'
    colors['right']='outside'
    set_node_attributes(board_graph, colors, 'color')
    
    edge_list = []
    for node in node_list:
        neighbors = hexBoard.get_neighbors(node)
        for neighbor in neighbors:
                edge = (node,neighbor)
                if edge not in edge_list:
                    edge_list.append(edge)
                
                
                
    
    for node in node_list:
        if node[0]==0:
            edge = ('left',node)
            if edge not in edge_list:
                edge_list.append(edge)
        
        if node[0]==hexBoard.size-1:
            edge = ('right',node)
            if edge not in edge_list:
                edge_list.append(edge)
                
        if node[1]==0:
            edge = ('down',node)
            if edge not in edge_list:
                edge_list.append(edge)
                
        if node[1]==hexBoard.size-1:
            edge = ('top', node)
            if edge not in edge_list:
                edge_list.append(edge)
        
        
    board_graph.add_edges_from(edge_list)
    
    return board_graph



def getWeightedSubgraph(board_graph:nx.Graph, agent_color):
    
    nodes_color = []
    node_list = list(board_graph.nodes())
    
    colors = nx.get_node_attributes(board_graph, 'color')
    nodes_color = [node for node in node_list if colors[node]==agent_color or colors[node]==MyHexBoard.EMPTY]
    
    
    if agent_color == MyHexBoard.RED:
        nodes_color.append('top')
        nodes_color.append('down')
    else:
        nodes_color.append('left')
        nodes_color.append('right')
        
    subgraph = board_graph.subgraph(nodes_color)
    
    edges = subgraph.edges()
    
    for edge in edges:
        if colors[edge[0]]==agent_color or colors[edge[1]]==agent_color:
            subgraph[edge[0]][edge[1]]['weight']=0
        else:
            subgraph[edge[0]][edge[1]]['weight']=1
    
    
    
    return subgraph




def findShortestPath(subgraph:nx.Graph, source, target):
    if nx.has_path(subgraph, source, target):
        return nx.shortest_path(subgraph, source=source, target=target, weight='weight')
    return None


def computeScoreOfPath(subgraph:nx.Graph, path):
    if path==None:
        return np.inf
    colors = nx.get_node_attributes(subgraph, 'color')
    score = 0
    for node in path:
        if colors[node]==MyHexBoard.EMPTY:
            score+=1
            
    return score
    
    
    
    











        
    
    
    
        
        
        
        
        
        
        
        
        
        
                
                
                
                
    
    