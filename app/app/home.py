import streamlit as st
import pandas as pd
import numpy as np
import scipy as sp
import plotly.express as px

st.title('Mineração de Notas Fiscais')

produto = st.selectbox(
    'Produto',
     ['Alcool Gel 500', 'Alcool 70', 'Vinagre']
     )

preco = st.number_input('preço')
quantidade = st.number_input('quantidade')

if st.button('Calcular'):

    notas = pd.read_csv(f'./data/alcool.csv', sep=';', header=0)
    notas.Produto = notas.Produto.str.upper()
    if produto == 'Alcool Gel 500':
        notas = notas.loc[(notas.Produto.str.find(r'GEL') != -1)&(notas.Produto.str.find(r'500') != -1)&(notas['Unid. Medida'].str.find(r'UN') != -1)]

    st.header('Intervalo')
    stats = notas['Valor Unitário'].describe()
    st.write(stats[['count','25%','mean','75%']].T)
    fig = px.scatter(
    notas,
    x="Valor Unitário",
    y="Quantidade",
    # size='quantidade',
    # color='descricaoProdutoServico',
    # hover_data=['nomeFornecedor', 'descricaoProdutoServico'],
    )
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, theme="streamlit")
    
    st.subheader('Intervalo de confiança:')
    ic = sp.stats.norm.interval(0.95, loc=stats['mean'], scale=stats['std'])
    st.write('Limite Inferior (LI):','{:.2f}'.format(ic[0]))
    st.write( 'Limite Superior (LS): ','{:.2f}'.format(ic[1]))
    st.write( 'Preço (P): ', str(preco), ' P > LS: ', str(preco > ic[1]) )
   
    st.header('Sobrepreço')
    if preco > ic[1]:
        st.caption('Preço R$ {:.2f}'.format((preco - notas['Valor Unitário'].mean())))
        st.caption('Valor R$ {:,.2f}'.format((preco - notas['Valor Unitário'].mean()).round(2) * quantidade))
    else:
        st.subheader('Não há evidência de sobrepreço.')