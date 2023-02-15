import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Notas Fiscais por Orgão')

orgaos = pd.read_csv('../data/lista-de-orgaos-do-siafiLista-de-Orgaos-SIAFI.csv', encoding='utf-16', sep=',', on_bad_lines='skip', header=0)


orgao = st.selectbox(
    'Orgão',
     orgaos['Órgão UGE Nome'],
     index=23
     )

if st.button('Ver notas'):

    notas = pd.read_csv(f'../data/{orgao}.csv', header=0, decimal=',', thousands='.', parse_dates=True, infer_datetime_format=True)
    
    st.write(notas)
    st.header('Fornecedor')

    fornecedor = {}

    # notas['valor'] = notas['valor'].apply(lambda x: x.replace('.','')).apply(lambda x: x.replace(',','.')).astype('float')
    fornecedor['valor'] = notas.groupby('nomeFornecedor')['valor'].sum().sort_values(ascending=False)

    st.write(fornecedor['valor'].head(10).reset_index())

    fig = px.bar(
    fornecedor['valor'].head(10).reset_index(),
    x="nomeFornecedor",
    y="valor")

    st.plotly_chart(fig, theme="streamlit")

    # st.bar_chart(fornecedor['valor'].head(10))
   
    st.header('Produtos')

    produtos = {}

    produtos['valor'] = notas.groupby('ncmSh')['valor'].agg(['sum','count']).sort_values(by='sum',ascending=False)

    st.write(produtos['valor'].head(10))

    fig2 = px.bar(
    produtos['valor'].head(10).reset_index(),
    x="ncmSh",
    y="sum")

    st.plotly_chart(fig2, theme="streamlit")

    # st.bar_chart(produtos['valor'].head(10))

    # notas_produto = notas.loc[notas['ncmSh'] == produto]
    
    # if st.button('Detalhar produto'):
    #     st.write(notas_produto)
