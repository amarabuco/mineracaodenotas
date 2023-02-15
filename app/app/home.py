import streamlit as st
import pandas as pd
import numpy as np

st.title('Mineração de Notas Fiscais')

orgaos = pd.read_csv('../data/lista-de-orgaos-do-siafiLista-de-Orgaos-SIAFI.csv', encoding='utf-16', sep=',', on_bad_lines='skip', header=0)


orgao = st.selectbox(
    'Orgão',
     orgaos['Órgão UGE Nome'],
     index=23
     )

if st.button('Ver notas'):

    notas = pd.read_csv(f'../data/{orgao}.csv', header=0)
    st.write(notas)
   