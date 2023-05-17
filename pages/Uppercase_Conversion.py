import streamlit as st

st.header('Uppercase Conversion')
st.subheader('Please paste the text you want to conver to uppercase in the textbox')

col1, col2 = st.columns(2, gap ='medium')

def upper_fmt(t):
    t = t.upper()
    t.replace('\N', '\n')
    return t

with col1:
    txt = st.text_area('Text to Convert', '')
with col2:
    st.code(upper_fmt(txt), language = "sql")
