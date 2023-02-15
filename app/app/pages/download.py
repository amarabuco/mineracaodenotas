import streamlit as st
import pandas as pd
import numpy as np
import requests

st.title('Download Notas Fiscais')

# df = pd.read_csv('../data/nfe_nota_2021_destinatario05.07-17hs.csv')

# st.write(df.iloc[0]['CHAVE_ACESSO'])

# ch = df.iloc[0]['CHAVE_ACESSO']

# chave = st.text_input('chave API')
chave = st.text_input('chave API','4f309cc82a298c317d97a452238c5a64', help='https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email')

headers = {
    'chave-api-dados': chave,
    
}

# body2 = {
#     'chave-api-dados': '4f309cc82a298c317d97a452238c5a64',
#     'chaveUnicaNotaFiscal': ''
# }

orgaos = pd.read_csv('../data/lista-de-orgaos-do-siafiLista-de-Orgaos-SIAFI.csv', encoding='utf-16', sep=',', on_bad_lines='skip', header=0)


orgao = st.selectbox(
    'Orgão',
     orgaos['Órgão UGE Nome'],
     index=23
     )

orgao_id = orgaos.loc[orgaos['Órgão UGE Nome'] == orgao].iloc[0]['Órgão UGE Código']

pags = st.slider(
    'Páginas',
     0,
     100, 
     10
     )

# st.write(orgaos.loc[orgaos['Órgão UGE Nome'] == orgao])
# st.write(orgaos.loc[orgaos['Órgão UGE Nome'] == orgao].iloc[0]['Órgão UGE Código'])


if st.button('Baixar notas'):

    # st.write(orgao_id)
    # st.write(pags)

    df = pd.DataFrame()
    for n in range(1,pags):
        print(n)
        print(f'https://api.portaldatransparencia.gov.br/api-de-dados/notas-fiscais?codigoOrgao={orgao_id}&pagina={n}')
        r1 = requests.get(f'https://api.portaldatransparencia.gov.br/api-de-dados/notas-fiscais?codigoOrgao={orgao_id}&pagina={n}', headers=headers)
        
        if len(r1.json()) == 0:
            st.write('Não há dados.')
            break 

        for nota in r1.json():
            key = nota['chaveNotaFiscal']
            print(key)

            r2 = requests.get(f'https://api.portaldatransparencia.gov.br/api-de-dados/notas-fiscais-por-chave?chaveUnicaNotaFiscal={key}', headers=headers)
            # # r = requests.post('https://www.nfe.fazenda.gov.br/portal/consulta.aspx?tipoConsulta=resumo&tipoConteudo=7PhJ+gAVw2g=', params=body)

            # st.write(r2.json())
            nf = r2.json()
            base = pd.DataFrame.from_dict(nf['notaFiscalDTO'], orient='index')
            
            for i in nf['itensNotaFiscal']:
                # print(i)
                # st.write(i)
                tmp = pd.DataFrame.from_dict(i, orient='index')
                row = pd.concat([base,tmp], axis=0)
                df = pd.concat([df,row.T], axis=0)
            st.write(df)

    if len(df) > 0:
        df.to_csv(f'../data/{orgao}.csv')