#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:13:36 2020

@author: zzfang
"""

import numpy as np 
from my_hex import MyHexBoard

def dummyEvaluation(hexBoard=None):
    #This dummy evaluation function is a random number generator
    return np.random.randint(0,10)



def gameOverEvaluation(hexBoard:MyHexBoard):
    pass


def heuristicEvaluation(hexBoard:MyHexBoard):
    pass