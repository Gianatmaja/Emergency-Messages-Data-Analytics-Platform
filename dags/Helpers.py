#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 14:27:56 2022

@author: gianatmaja
"""
import numpy as np
import pandas as pd

import re
import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

def tokenize(text):
    
    # Normalize text
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    
    # Get stopwords
    stop_words = stopwords.words("english")
    
    #tokenize
    words = word_tokenize(text)
    
    #stemming
    stemmed = [PorterStemmer().stem(w) for w in words]
    
    #lemmatizing
    words_lemmed = [WordNetLemmatizer().lemmatize(w) for w in stemmed if w not in stop_words]
   
    return words_lemmed

def get_ln_id(lan):
    language_ID = [ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17,
                   18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                   35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
                   52, 53]
    language = ['af', 'an', 'br', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'en', 'eo',
                'es', 'et', 'eu', 'fi', 'fo', 'fr', 'ga', 'hr', 'ht', 'id', 'it',
                'jv', 'ku', 'la', 'lb', 'lt', 'lv', 'mg', 'ms', 'mt', 'nb', 'nl',
                'nn', 'no', 'oc', 'pl', 'pt', 'qu', 'ro', 'rw', 'sk', 'sl', 'sq',
                'sv', 'sw', 'tl', 'tr', 'vi', 'vo', 'wa', 'xh', 'zu']
    Language_dict = dict(zip(language, language_ID))
    ln_id = Language_dict[lan]
    return ln_id


def get_date_id(date_str):
    date_int = str(date_str[:2] + date_str[3:5] + date_str[6:10])
    return date_int


def get_cat_id(category):
    if (category == 'N/A'):
        cat_id = 1
    elif (category == 'Low'):
        cat_id = 2
    elif (category == 'Med'):
        cat_id = 3
    else:
        cat_id = 4
    return cat_id