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

def gdp(t):
    t = t.upper()
    
    rmv = r"(PHI.)|(PHI)"
    t = re.sub(rmv, "", t)
    
    ed_tb = r"(RPT.EDITS_EX_CODES_OUTPUT)"
    t = re.sub(ed_tb, r"IDENTIFIER(:EDIT_OUTPUT_TABLE)", t)
    
    rpt = r"(RPT.)"
    t = re.sub(rpt, r"CONFIGURATION.", t)
    
    clm_sd = r"(CLAIM_SID)"
    t = re.sub(clm_sd, r"CLAIM_HEADER_SID", t)
    
    diagpoa = r"(DIAG_CD_)(\d)_"
    t = re.sub(diagpoa, r"DIAG_CD_\2_",t)
    
    diag = r"(DIAG_CD_)(\d)"
    t = re.sub(diag, r"DIAG_CD_0\2",t)
    
    con_cd = r"(CONDITION_CD_)(\d\D)"
    t = re.sub(con_cd, r"CONDITION_CD_0\2",t)
    
    adj = r"(ADJUDICATION_)(\w*)"
    t = re.sub(adj, r"ADJC_\2", t)
    
    dn_cd = r"(DENIAL_CD_)(\d)"
    t = re.sub(dn_cd, r"ADJC_REASON_CD_\2", t)
    
    dn_ds = r"(DENIAL_DESC_)(\d)"
    t = re.sub(dn_ds, r"ADJC_REASON_DESC_\2", t)
    
    claim_ = r"(ADMIT_DIAG_CD|ADMIT_DT|ADMIT_SOURCE|ADMIT_TIME|ADMIT_TYPE|CREATE_DT|DISCHARGE_STATUS_CD|DISCHARGE_TIME|LENGTH_OF_STAY_ACTUAL_CNT|RURAL_IND|TRAUMA_IND)"
    t = re.sub(claim_, r"CLAIM_\1", t)
    
    claim_fac_ = r"(DRG_ALLOWED_AMT|DRG_BILLED_AMT|DRG_PAID_AMT)"
    t = re.sub(claim_fac_, r"CLAIM_FACILITY_\1", t)
    
    line_sq = r"(CLAIM_LINE_SEQ)"
    t = re.sub(line_sq, r"\1_NUM", t)
    
    ben_pa = r"(BENEFIT_PACKAGE)"
    t = re.sub(ben_pa, r"CLAIM_PAYER_TYPE", t)
    
    line = r"(PAYMENT_TYPE)"
    t = re.sub(line, r"LINE_\1", t)
    
    clm_sts = r"CLAIM(_STATUS_)(\w*)"
    t = re.sub(clm_sts, r"LINE\1\2", t)
    
    dos = r"DOS_YEAR_MONTH"
    t = re.sub(dos, r"CLAIM_YEAR_MONTH_SERVICE_DT", t)
    
    icd_ind = r"(ICD_VERSION_IND)"
    t = re.sub(icd_ind, r"DIAG_\1", t)
    
    fac_ = r"(BILL_TYPE_CD|DRG_VERSION_PAID)"
    t = re.sub(fac_, r"FACILITY_\1", t)
    
    fac_apr_ = r"(DRG_CD_BILLED|DRG_CD_PAID|DRG_SEVERITY_BILLED|DRG_SEVERITY_PAID)"
    t = re.sub(fac_apr_, r"FACILITY_APR_\1", t)
    
    fin_st = r"AAR_FINAL_STATUS_CD = 'Y'"
    t = re.sub(fin_st, r"DP_ACTIVE_RECORD_FLAG = TRUE", t)
    
    return t

with col1:
    txt = st.text_area('Text to Convert', '')
with col2:
    st.code(gdp(txt), language = "sql")


