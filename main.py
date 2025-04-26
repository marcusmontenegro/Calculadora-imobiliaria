from st_on_hover_tabs import on_hover_tabs
from calculadora import calculadora_page
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.header("ABC Imóveis")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


with st.sidebar:
    tabs = on_hover_tabs(tabName=['Calculadora', 'Imóveis', 'Clientes'], 
                         iconName=['calculate', 'location_city', 'person_search'], default_choice=0)

if tabs =='Calculadora':
    calculadora_page()

elif tabs == 'Imóveis':
    st.title("Imóveis")
    st.write('Name of option is {}'.format(tabs))

elif tabs == 'Clientes':
    st.title("Clientes")
    st.write('Name of option is {}'.format(tabs))
    