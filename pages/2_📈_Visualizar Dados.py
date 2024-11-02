import pandas as pd
from pathlib import Path
import streamlit as st
import plotly_express as px

st.set_page_config('Dados | Rener', '📈', 'wide')


# Header
st.markdown('# Propriedade Rener')
st.markdown('## Aqui você verá mais dados sobre a safra.')
st.markdown('')

# Carregando os dados para a sessão
df_colheita = st.session_state['df_colheita']
df_insumo = st.session_state['df_insumo']
df_mq_solo = st.session_state['df_mq_solo']
df_mq_plantio = st.session_state['df_mq_plantio']
df_mq_manutencao = st.session_state['df_mq_manutencao']
df_investimento = st.session_state['df_investimento']
df_transp_armaz = st.session_state['df_transp_armaz']
df_custo = st.session_state['df_custo']


st.markdown(f"### Insumos - Custo Total(ha): R$ {df_insumo['Preço total (R$/ha)'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
st.dataframe(df_insumo, hide_index=True)
st.divider()

st.markdown(f'### Máquinas - Custo Total(ha): R$ {(df_mq_manutencao['Preço total (R$/ha)'].sum() + df_mq_solo['Preço total (R$/ha)'].sum() + df_mq_plantio['Preço total (R$/ha)'].sum()):,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
st.write('Preparo de solo')
st.dataframe(df_mq_solo, hide_index=True)
st.write('Plantio e Tratos Culturais')
st.dataframe(df_mq_plantio, hide_index=True)
st.write('PManutenção das Maquinas')
st.dataframe(df_mq_manutencao, hide_index=True)
st.divider()

st.markdown(f"### Investimentos - Custo Total(ha): R$ {df_investimento['Custo (R$/ha)'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
st.dataframe(df_investimento, hide_index=True)
st.divider()

st.markdown(f"### Custos de Operação - Custo Total(ha): R$ {(df_transp_armaz['Preço total (R$/ha)'].sum() + df_colheita['Preço total (R$/ha)'].sum()):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
st.write('Colheita')
st.dataframe(df_colheita, hide_index=True)
st.write('Transporte e Armazenamento')
st.dataframe(df_transp_armaz, hide_index=True)
st.divider()