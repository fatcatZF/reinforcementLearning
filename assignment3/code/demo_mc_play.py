#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 17:03:08 2020

@author: Z Fang

Demo the play process based on energy and velocity
"""

from nn_models import build_train_model
from mc_games import prepair_training_data, play_funcs, test_play

print("collecting training data")
training_data = prepair_training_data(-25, play_func=play_funcs['energy_v1'] ,verbose=False)
print("training model")
model = build_train_model(training_data)

test_play(10, model, render=True, verbose=True) 
#render the play process and return winning rate and average steps