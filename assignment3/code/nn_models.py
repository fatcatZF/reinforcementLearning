#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 00:44:31 2020

@author: Z Fang
https://github.com/fatcatZF/reinforcementLearning

"""

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
from keras.callbacks import EarlyStopping
from keras.utils.vis_utils import plot_model


def build_mlp_model(input_size, output_size, is_plot=False):
    model = Sequential()
    model.add(Dense(128, input_dim=input_size, activation='relu'))
    model.add(Dense(output_size, activation='softmax'))
    model.compile(loss='mse', optimizer=Adam())
    
    if is_plot:
        plot_model(model, to_file='mlp_model.png', show_shapes=True, show_layer_names=True)
    
    return model 



def build_train_model(training_data, build_func=build_mlp_model, fit_params=None, verbose=0):
    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]))
    y = np.array([i[1] for i in training_data]).reshape(-1, len(training_data[0][1]))
    
    if fit_params is None:
        fit_params={
            "epochs":100,
            "validation_split":0.3,
            "callbacks":[EarlyStopping(patience=5, monitor="val_loss")]
            }
    
    
    model=build_func(input_size=len(X[0]), output_size=len(y[0]))
    model.fit(X, y, verbose=verbose, **fit_params)
    
    return model