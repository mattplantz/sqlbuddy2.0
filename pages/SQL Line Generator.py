import streamlit as st
import re

st.title('SQL Buddy')
col1, col2 = st.columns(2, gap='medium')
with st.sidebar:
    mode = st.selectbox("Choose what to add in front of elements in list", ('SUM', 'COUNT', 'AVG', 'Other'))
    if mode == 'Other':
    	other = st.text_input('Type what you would like in front of the elements in the list')

with col1:
	txt = st.text_area('List of Elements', '''line_billed_amt, line_unit_cnt, line_allowed_amt''')

txt = re.sub(r'\s+', ' ', txt)
cols_list = txt.split(',')
cols_list = [x.strip(' ') for x in cols_list]
new_list = []
header = mode
if mode == 'Other':
	header = other
for item in cols_list:
	item = re.sub(r'line_', '', item)
	new = header + '(' + item + ') as ' + item
	new_list.append(new)

with col2:
	st.text(',\n'.join(new_list))