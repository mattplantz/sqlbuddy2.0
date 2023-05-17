# -*- coding: utf-8 -*-
"""
Created on Wed May 17 12:33:31 2023

@author: mplantz
"""
import streamlit as st
import re

st.header('GDP Conversion Buddy')
st.subheader('Please paste the text you want to convert to GDP model')

col1, col2 = st.columns(2, gap ='medium')

def upper_fmt(t):
    t = t.upper()
    
    rmv = r"(PHI)|(PHI.)"
    t = re.sub(rmv, "", t)
    
    ed_tb = r"(RPT.EDITS_EX_CODES_OUTPUT)"
    t = re.sub(ed_tb, r"IDENTIFIER(:EDIT_OUTPUT_TABLE)", t)
    
    rpt = r"(.RPT)"
    t = re.sub(rpt, r".CONFIGURATION", t)
    
    btc = r"(BILL_TYPE_CD)"
    t = re.sub(btc, r"FACILITY_\1", t)
    
    clm_sd = r"(CLAIM_SID)"
    t = re.sub(clm_sd, r"CLAIM_HEADER_SID", t)
    
    diag = r"(DIAG_CD_)(\d\D)"
    t = re.sub(diag, r"DIAG_CD_0\2",t)
    
    return t

with col1:
    txt = st.text_area('Text to Convert', '')
with col2:
    st.code(upper_fmt(txt), language = "sql")


