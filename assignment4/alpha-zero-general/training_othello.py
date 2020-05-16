#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 20:07:26 2020

@author: z fang
"""

import logging

import coloredlogs

from Coach import Coach
from othello.OthelloGame import OthelloGame as Game
from othello.pytorch.NNet import NNetWrapper as nn
from utils import *

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')

args = dotdict(
    {
     'numIters':50,# Number of complete self-play games to simulate during a new iteration.
     'numEps':10,
     'tempThreshold':15,
     'updateThreshold':0.6, # During arena playoff, new neural net will be accepted if threshold or more of games are won.
     'maxlenOfQueue':200000,  # Max Number of game examples to train the neural networks.
     'numMCTSSims':20, # Number of games moves for MCTS to simulate.
     'arenaCompare':20,  # Number of games to play during arena play to determine if new net will be accepted.
     'cpuct':1,
     
     'checkpoint':'./temp',
     'load_model':False,  #whether load an existing model to train this model
     'load_folder_file':('/dev/models/8X100X50','best.pth.tar'),
     'numItersForTrainExamplesHistory':20,
     }
    )

def main():
    log.info('Loading %s...', Game.__name__)
    g = Game(6)
    
    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)
    
    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file)
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
        
    else:
        log.warning('Not loading a checkpoint!')
    
    
    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)
    
    
    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()
        
    
    log.info('Starting the learning process 🎉')
    c.learn()
    
    
    
if __name__=="__main__":
    main()
    
    
    
    
    
    
        
        