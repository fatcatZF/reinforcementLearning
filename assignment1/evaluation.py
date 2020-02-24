#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:13:36 2020

@author: zzfang
"""

import numpy as np 

def dummyEvaluation(mode='running'):
    #This dummy evaluation function is a random number generator
    if mode=='debugging':
        return 1
    return np.random.randint(0,10)