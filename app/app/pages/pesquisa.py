import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Pesquisa de Preços')

orgaos = pd.read_csv('../data/lista-de-orgaos-do-siafiLista-de-Orgaos-SIAFI.csv', encoding='utf-16', sep=',', on_bad_lines='skip', header=0)


orgao = st.selectbox(
    'Orgão',
     orgaos['Órgão UGE Nome'],
     index=128
     )
try:
    notas = pd.read_csv(f'../data/{orgao}.csv', header=0, decimal=',', thousands='.', parse_dates=True, infer_datetime_format=True)

    if orgao:
        produto = st.selectbox(
            'Produto',
            notas['ncmSh'].unique()
        )
except:
    st.write("Não há dados. Selecione outro órgão.")

if st.button('Detalhar produto'):
    
    st.header('Preços')

    notas_produto = notas.loc[notas['ncmSh'] == produto]
    tab1, tab2 = st.tabs(["Dispersão", "Boxplot"])

    with tab1:
        fig = px.scatter(
        notas_produto,
        x="dataEmissao",
        y="valorUnitario",
        size='quantidade',
        color='descricaoProdutoServico',
        hover_data=['nomeFornecedor', 'descricaoProdutoServico'],
        )
        fig.update_layout(showlegend=False)

        st.plotly_chart(fig, theme="streamlit")

    with tab2:
        fig2 = px.box(
        notas_produto,
        y="valorUnitario"
        )
        st.plotly_chart(fig2, theme="streamlit")
        st.write(notas_produto["valorUnitario"].describe().T)



    st.header('Notas')
    st.write(notas_produto[['orgaoDestinatario','nomeFornecedor', 'dataEmissao','descricaoProdutoServico', 'quantidade', 'valorUnitario']])
    # st.write(notas_produto)