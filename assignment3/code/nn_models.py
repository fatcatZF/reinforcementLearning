#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 00:44:31 2020

@author: Z Fang
"""

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np

def build_mlp_model(input_size, output_size):
    model = Sequential()
    model.add(Dense(128, input_dim=input_size, activation='relu'))
    model.add(Dense(output_size, activation='softmax'))
    model.compile(loss='mse', optimizer=Adam())
    
    return model 



def build_train_model(training_data, num_of_epochs=20, build_func=build_mlp_model):
    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]))
    y = np.array([i[1] for i in training_data]).reshape(-1, len(training_data[0][1]))
    
    model=build_func(input_size=len(X[0]), output_size=len(y[0]))
    model.fit(X, y, epochs=num_of_epochs)
    
    return model