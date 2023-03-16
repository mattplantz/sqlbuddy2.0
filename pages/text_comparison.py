# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 09:17:25 2023

@author: mplantz

Source: https://towardsdatascience.com/side-by-side-comparison-of-strings-in-python-b9491ac858
"""

import streamlit as st
import re
import difflib
from difflib import SequenceMatcher

st.header('Text Comparison')
st.subheader('please paste the text you want to compare in the two separate text boxes')

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def tokenize(s):
    return re.split('\s+', s)
def untokenize(ts):
    return ' '.join(ts)
        
def equalize(s1, s2):
    l1 = tokenize(s1)
    l2 = tokenize(s2)
    res1 = []
    res2 = []
    prev = difflib.Match(0,0,0)
    for match in difflib.SequenceMatcher(a=l1, b=l2).get_matching_blocks():
        if (prev.a + prev.size != match.a):
            for i in range(prev.a + prev.size, match.a):
                res2 += ['_' * len(l1[i])]
            res1 += l1[prev.a + prev.size:match.a]
        if (prev.b + prev.size != match.b):
            for i in range(prev.b + prev.size, match.b):
                res1 += ['_' * len(l2[i])]
            res2 += l2[prev.b + prev.size:match.b]
        res1 += l1[match.a:match.a+match.size]
        res2 += l2[match.b:match.b+match.size]
        prev = match
    return untokenize(res1), untokenize(res2)

def insert_newlines(string, every=64, window=10):
    result = []
    from_string = string
    while len(from_string) > 0:
        cut_off = every
        if len(from_string) > every:
            while (from_string[cut_off-1] != ' ') and (cut_off > (every-window)):
                cut_off -= 1
        else:
            cut_off = len(from_string)
        part = from_string[:cut_off]
        result += [part]
        from_string = from_string[cut_off:]
    return result

def show_comparison(s1, s2, width=40, margin=10, sidebyside=True, compact=False):
    s1, s2 = equalize(s1,s2)

    if sidebyside:
        s1 = insert_newlines(s1, width, margin)
        s2 = insert_newlines(s2, width, margin)
        if compact:
            for i in range(0, len(s1)):
                lft = re.sub(' +', ' ', s1[i].replace('_', '')).ljust(width)
                rgt = re.sub(' +', ' ', s2[i].replace('_', '')).ljust(width) 
                st.write(lft + ' | ' + rgt + ' | ')        
        else:
            for i in range(0, len(s1)):
                lft = s1[i].ljust(width)
                rgt = s2[i].ljust(width)
                st.write(lft + ' | ' + rgt + ' | ')
    else:
        st.write(s1)
        st.write(s2)
        
col1, col2 = st.columns(2, gap ='medium')

with st.sidebar:
    side_by_side = st.checkbox('Side by Side Comparison')
    vert = st.checkbox('Stacked Text Comparison')
    similarity_score= st.checkbox('Similarity Score')

with col1:
    s1 = st.text_area('text one to compare', '')
with col2:
    s2 = st.text_area('text two to compare', '')

if side_by_side:
    try:
        show_comparison(s1, s2, sidebyside = True, compact = False)
    except:
        st.text('sorry. issue with comparison')
        
if vert:
    try:
        show_comparison(s1, s2, sidebyside = False, compact = True)
    except:
        st.text('sorry. issue with comparison')

if similarity_score:
    try:
        st.write(round(similar(s1,s2),4))
    except:
        st.text('Sorry. Issue with Similarity Score')
