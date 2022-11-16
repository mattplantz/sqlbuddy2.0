import streamlit as st
import re
from sql_formatter.core import format_sql

def split_sql(sql, mode):
    queries = sql.split(';')
    new_sql = []
    for query in queries:
    	if mode == 'in':
        	new_sql.append(in_to_inner_join(query))
    return ''.join(new_sql)

#change an in statement to an innner join on a temp table if the size fo list in the in is greater than min_list
def in_to_inner_join(sql, min_list=0):
    find_list = r"(?i)([\w.]+) *in *[(]+([\w', ]+)[)]+"
    pattern = re.compile(find_list)
    for match in pattern.finditer(sql):
        var = match.group(1)
        col_name = re.sub('\.', '_', var)
        col_name = col_name[:col_name.find('_')]
        vals = match.group(2)
        vals = vals.split(',')
        vals = [x.strip(' ') for x in vals]
        varchar_size = len(max(vals, key=len))+1
        line_1 = f'\nDROP TABLE IF EXISTS #{col_name}_VALUES; \nCREATE TABLE #{col_name}_VALUES ({col_name} VARCHAR({varchar_size}));'
        line_2 = 'INSERT INTO #{}_VALUES VALUES {}'.format(col_name,' '.join('({}),'.format(i) for i in vals))
        create_table = line_1 +  '\n' + line_2[:-1]
        sql = re.sub(r'(?i)(SELECT [\s\S]+)', r'{};\n\n\1;'.format(create_table), sql)
        sql = re.sub(find_list, '', sql)
        sql = re.sub(r'(?i)WHERE', f'INNER JOIN #{col_name}_VALUES {col_name[:4]} ON {col_name[:4]}.{col_name} = {var}\nWHERE', sql)
        sql = re.sub(r'(?i)and\s+and', 'AND', sql)
        sql = re.sub(r'(?i)WHERE\s+and', 'WHERE', sql)
        sql = re.sub(r'(?i)WHERE\s+;', ';', sql)
    return sql

st.title('SQL Buddy')
col1, col2 = st.columns(2, gap='medium')
with st.sidebar:
    in_to_inner = st.checkbox("Convert in to inner joins")
    snowflake = st.checkbox("Convert to Snowflake")

with col1:
	#st.header('Insert SQL Script Here')
	txt = st.text_area('SQL to refactor', '''SELECT * 
		FROM ...
    ''')
sql = 'SELECT * FROM ...'
if in_to_inner:
	sql = format_sql(split_sql(txt, "in"))
	sql = re.sub(r';\s+', ';\n', sql)
elif snowflake:
	#sql = format_sql(split_sql(txt, "snowflake"))
	#sql = re.sub(r';\s+', ';\n', sql)
	st.text('Sorry, Snowflake is still under construction')
else:
	st.text('Please choose an option from the sidebar')
with col2:
	#st.header('SQL Output')
	#txt = st.text_area('SQL Output', '''''')
	st.code(sql)

