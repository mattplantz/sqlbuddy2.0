"""
Created on Thu Jun 15 12:01:49 2023

@author: mplantz

Goal: Search a string of text for a specific supstring
"""

import streamlit as st

st.header("Text Finding Wizard")
st.subheader('Please input both the whole text you want to search and the text you hope to find.')

def exists(srch, fnd):
    srch = srch.lower()
    fnd = find.lower()
    start = srch.find(fnd)
    if start == -1:
        return 'String does not exist in search :('
    elif srch == '' and fnd == '':
        return ''
    else:
        return 'String exists in search :)'
    
    
def search(srch, fnd, length):
    srch = srch.lower()
    fnd = find.lower()
    start = srch.find(fnd)
    ln = len(fnd)
    end = start+ln
    start_extended = start - length
    end_extended = end + length
    if start == -1:
        return 'String does not exist in search :('
    else:
        return srch[start_extended:end_extended]

col1, col2 = st.columns(2, gap = 'medium')

with col1:
    all_text = st.text_area('Text to SEARCH','')
with col2:
    find = st.text_area('Text to FIND','')


with st.sidebar:
    kind = st.radio('What would you like to do?',['Check if search exists','Extract text surrounding match'])
    lng = st.number_input(label = 'Number of characters around match to return'
                          , min_value = 0
                          , max_value = 100
                          , value = 0)


if kind == 'Check if search exists':
    st.write(exists(all_text, find))
if kind == 'Extract text surrounding match':
    st.write(search(all_text, find, lng))
