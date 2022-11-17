import streamlit as st
import re

#st.title('SQL Buddy')
col1, col2 = st.columns(2, gap='medium')
paren1 = '('
paren2 = ')'
		
with st.sidebar:
	kind = st.radio('What would you like to do to the list', ['Add Text in Front', 'Convert to Table Notation'])	
	if kind == 'Add Text in Front':
		mode = st.selectbox("Choose what to add in front of elements in list", ('SUM', 'COUNT', 'AVG', 'Other'))
		if mode == 'Other':
			mode = st.text_input('Type what you would like in front of the elements in the list')
	else:
		mode = ''
		end = ''
		quotes = st.checkbox('Add Quotes?')
		if quotes:
			paren1 = "('"
			paren2 = "')"
	deli = st.selectbox("Select Delimeter", (',', ';', '|', 'Other'))
	if deli == 'Other':
		deli = st.text_input('Please type in Delimeter')

with col1:
	txt = st.text_area('List of Elements', '''line_billed_amt, line_unit_cnt, line_allowed_amt''', label_visibility="collapsed")

txt = re.sub(r'\s+', ' ', txt)
cols_list = txt.split(deli)
cols_list = [x.strip(' ') for x in cols_list]
new_list = []



for item in cols_list:
	if kind == 'Add Text in Front':
		item = re.sub(r'line_', '', item)
		end = ' as ' + item
	new = mode + paren1 + item + paren2 + end
	new_list.append(new)

with col2:
	st.text(',\n'.join(new_list))
