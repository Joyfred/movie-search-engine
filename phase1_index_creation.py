# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:50:44 2020

@author: JOYFRED JESURAJA
"""
import json

with open("movies.json", "r") as data_file:
    movies = json.load(data_file)
    
title_index = dict()
for movie in movies:
    title_index[movie['title']] = movie['id']

description_data = dict()
for movie in movies:
    description_data[movie['description']] = movie['id']
    
    
