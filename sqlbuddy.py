import streamlit as st
import re
from sql_formatter.core import format_sql

def split_sql(sql, mode, db):
	try:
		queries = sql.split(';')
		new_sql = []
		for query in queries:
			query = re.sub(r"[ \t]", r" ", query)
			if mode == 'in':
				new_sql.append(in_to_inner_join(query))
			if mode == 'snowflake':
				new_sql.append(snowSQL(query, db))
		return ''.join(new_sql)
	except:
		return ''

def snowSQL(text, db = 'MHP_FWA_DW'):    

	isnull = r"(?i)ISNULL *\(([\w.@()']+) *[, ()'.]+([\w@.()']+) *\)"
	text = re.sub(isnull, r"COALESCE(\1,\2)", text)

	tryconv = r"(?i)TRY_CONVERT *\(([\w.@]+) *[, ]+([\w@.]+) *[\w@., ]*\)"
	text = re.sub(tryconv, r"TRY_CAST(\2 AS \1) ", text)

	tables = r"(?i)(?:[\w]*\.)*(PHI.)((\w)*)"
	text = re.sub(tables, r"{}.\1\2 ".format(db), text)
    
	curr_db = r"(?i)(?:^|\W)DB_NAME()"
	text = re.sub(curr_db, r" CURRENT_DATABASE() ", text)

	outer = r"(?i)OUTER *APPLY"
	text = re.sub(outer, r" LEFT OUTER JOIN ", text)

	prt = r"(?i)(?:^|\W)PRINT *'(.*?)'"
	text = re.sub(prt, r"", text)
    
	eq_w_paran = r"(?i)([\w.]+) *= *((?:(?:[\w ]*[(]+)+(?:[\w. ']*)[\w. ',]*[ )',]+)+)(\s*,|\s*FROM)"
	text = re.sub(eq_w_paran, r"\2 as \1\3", text)
	
	#eq = r"([\w.]+) *= *(?:(?:(?:[\w ]*[(]+)+([\w. ']*)[\w. ',]*[ )',]+)+|([\w. ]*))(,|\s*FROM)"
	eq = r"(?i)([\w.]+) *= *([\w. ]*)(\s*,|\s*FROM)"
	text = re.sub(eq, r"\2 as \1\3", text)
    
	case = r"([\w. ]+) *= *(CASE *WHEN *[\w. ()',=]+ *END *),"
	text = re.sub(case, r"\2 as \1,", text)

	drop = r"(?i)DROP *TABLE *( *IF *EXISTS *) *\#(.*)(?:$|\W)"
	text = re.sub(drop, r"CREATE OR REPLACE TEMPORARY TABLE \2 AS \n", text)
	
	droptmp = r"(?i)DROP *TABLE *( *IF *EXISTS *) *(tmp.)(.*)(?:$|\W)"
	text = re.sub(droptmp, r"CREATE OR REPLACE TEMPORARY TABLE \3 AS \n", text)
	
	remove = r"(?i)INTO *\#(.*)|\#|(?:^|\W)GO(?:$|\W)|USE *([\w]*)|\[|\]|INTO *(tmp.)(.*)"
	text = re.sub(remove, r"", text)
    
	return text

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

st.header('SQL Buddy : Edit Full Queries')
st.subheader('Please copy and paste your SQL Query in the box to the left and choose what actions you would like to perform')
col1, col2 = st.columns(2, gap='medium')
with st.sidebar:
    in_to_inner = st.checkbox("Convert in to inner joins")
    snowflake = st.checkbox("Convert to Snowflake")

with col1:
	#st.header('Insert SQL Script Here')
	txt = st.text_area('SQL to refactor', '''USE MHP_FWA_DW;
GO;
SELECT PAID = ISNULL(FCL.PAID_AMT, 0) 
, ALLOWED = ALLOWED_AMT
FROM PHI.FACT_CLAIM_LINE FCL
LEFT JOIN PHI.CPT4 CPT on CPT.CPT_SID = FCL.CPT_SID
WHERE CODE in ('99215', '99216', '99217', '99218');
   
   
   ''', label_visibility="collapsed", height=200)
sql = 'SELECT * FROM ...'
#find database name
res = re.search(r"(?i)USE *([\w]*)", txt)
try:
	db = res.group(1)
except:
	db = 'MHP_FWA_DW' #default to MHP_FWA_DW if not found


if in_to_inner:
	txt = format_sql(split_sql(txt, "in", db))
	txt = re.sub(r';\s+', ';\n', txt)
if snowflake:
	txt = format_sql(split_sql(txt, "snowflake", db))
	txt = re.sub(r';\s+', ';\n', txt)
	#st.text('Sorry, Snowflake is still under construction')
if not snowflake and not in_to_inner:
	st.warning('Please choose an option from the sidebar')
with col2:
	#st.header('SQL Output')
	#txt = st.text_area('SQL Output', '''''')
	st.code(txt, language="sql")

