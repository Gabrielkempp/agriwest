import pandas as pd
from pathlib import Path
import streamlit as st
import plotly_express as px

st.set_page_config('Agriwest | Rener', '🌱', 'wide')

# Carregando arquivo
cur_dir = Path(__file__).parent
arquivo = pd.ExcelFile(cur_dir / 'custos.xlsx')

# Chaves que você deseja verificar no session_state
keys = ['df_insumo', 'df_mq_solo', 'df_mq_plantio', 'df_mq_manutencao', 'df_investimento', 'df_colheita', 'df_transp_armaz']

if any(key not in st.session_state for key in keys):
    # Carrega cada Planilha do arquivo em um dataframe eliminando valores nulos
    df_insumo = arquivo.parse('insumos').fillna(0)
    df_mq_solo = arquivo.parse('maq_prep_solo').fillna(0)
    df_mq_plantio = arquivo.parse('maq_plant').fillna(0)
    df_mq_manutencao = arquivo.parse('maq_manutencao').fillna(0)
    df_investimento = arquivo.parse('investimento').fillna(0)
    df_colheita = arquivo.parse('colheita').fillna(0)
    df_transp_armaz = arquivo.parse('transp_armaz').fillna(0)

    # Criando Dataframe custo
    df_custo = pd.DataFrame({
        'Categoria': ['Insumos', 'Máquinas', 'Investimentos', 'Colheita tercerizada', 'Transporte e armazenamento'],
        'R$/ha': [
            df_insumo['Preço total (R$/ha)'].sum(),
            df_mq_solo['Preço total (R$/ha)'].sum() + df_mq_plantio['Preço total (R$/ha)'].sum() + df_mq_manutencao['Preço total (R$/ha)'].sum(),
            df_investimento['Custo (R$/ha)'].sum(),
            df_colheita['Preço total (R$/ha)'].sum(),
            df_transp_armaz['Preço total (R$/ha)'].sum()
        ]
    })

    # Criando porcentagem
    df_custo['Partc. Custo'] = round((df_custo['R$/ha'] / df_custo['R$/ha'].sum()) * 100, 2)


    # Carregando os dados para a sessão
    for key, value in zip(keys, [df_insumo, df_mq_solo, df_mq_plantio, df_mq_manutencao, df_investimento, df_colheita, df_transp_armaz]):
        st.session_state[key] = value

    st.session_state['df_custo'] = df_custo

# Carregando os dados para a sessão
df_colheita = st.session_state['df_colheita']
df_insumo = st.session_state['df_insumo']
df_mq_solo = st.session_state['df_mq_solo']
df_mq_plantio = st.session_state['df_mq_plantio']
df_mq_manutencao = st.session_state['df_mq_manutencao']
df_investimento = st.session_state['df_investimento']
df_transp_armaz = st.session_state['df_transp_armaz']
df_custo = st.session_state['df_custo']

# Header
st.markdown('# Propriedade Rener')
st.markdown('## Análise Agriwest - Gestão Agroempresarial 📈🌱')
st.markdown('')

# Selecione a quantidade de hectares 
st.sidebar.write("**Cálculo do custo da safra**")
st.sidebar.write(' ')
hec = st.sidebar.number_input('Insira a quantidade de Hectares',min_value=1, value=20)
hec = float(hec) 



# Calculo do custo
custo_por_hectare = df_custo['R$/ha'].sum()
custo_total = hec * custo_por_hectare

# Criando uma cópia para formatação
df_exibicao = df_custo.copy()

# Formatando colunas apenas para exibição
df_exibicao['R$/ha'] = df_exibicao['R$/ha'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
df_exibicao['Partc. Custo'] = df_exibicao['Partc. Custo'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + '%')

# Exibindo informacoes
st.divider()
col1, col2 = st.columns([0.5, 0.5])
col1.dataframe(df_exibicao.rename(columns={'R$/ha': 'Custo total por Hectare', 'Partc. Custo': 'Fatia do Gasto'}),width=600, hide_index=True)
col2.write()
col2.metric(label='Custo Total por Hectare', value=f'R$ {custo_por_hectare:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric(label='Custo Total da Safra', value=f'R$ {custo_total:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."), delta='-12% Comparado a ultima safra', delta_color='inverse')
st.divider()
# Grafico pie
fig = px.pie(df_custo,label='Divisão de custos por categoria' , names=df_custo['Categoria'],values=df_custo['Partc. Custo'])
st.plotly_chart(fig)
st.divider()