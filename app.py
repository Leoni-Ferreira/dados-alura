import pandas as pd
import streamlit as st
import plotly.express as px
import pycountry



# configurações da página
# definir o título da pagina

st.set_page_config(
  page_title="Dashboard de Salarios na Area de Dados",
  page_icon="📊",
  layout="wide",
)
# carregamento dos dados
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# Barra lateral
st.sidebar.header("🔍 Filtros")

# filtro de ano
anos_disponiveis = sorted(df["ano"].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# filtros de senioridade
senioridades_disponiveis = sorted(df["senioridade"].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# filtro por tipo de contrato
contratos_disponiveis = sorted(df["contrato"].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Filtor por tamanho da empresa
tamanhos_disponiveis = sorted(df["tamanho_empresa"].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# Filtragem do dataframe
# O datframe principal é filtrado com base nas seleçoes feitas na barra lateral
df_filtrado = df[
    (df["ano"].isin(anos_selecionados)) &
    (df["senioridade"].isin(senioridades_selecionadas)) &
    (df["contrato"].isin(contratos_selecionados)) &
    (df["tamanho_empresa"].isin(tamanhos_selecionados))
]

# conteudo principal
st.title("Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na area de dados nos ultimos anos. utilize os filtros a esquerda para refinar sua busca.")

# Metricas Principais
st.subheader("Métricas Gerais (Salario anual em USD)")

if not df_filtrado.empty:
  salario_medio = df_filtrado['usd'].mean()
  salario_maximo = df_filtrado['usd'].max()
  total_registros = df_filtrado.shape[0]
  cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
  salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, ""
  
col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio", f"${salario_medio:,.0f}")
col2.metric("Salário Máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de Registros", total_registros)
col4.metric("Cargo Mais Frequente", cargo_mais_frequente)

st.markdown("---")

# Analise visual com plotly
st.subheader("Graficos")

col_graf1, colgraf2 = st.columns(2)

with col_graf1:
  if not df_filtrado.empty:
    top_cargos = df_filtrado.groupby("cargo")["usd"].mean().nlargest(10).sort_values(ascending=True).reset_index()
    grafico_cargos =px.bar(
      top_cargos,
      x='usd',
      y='cargo',
      orientation='h',
      title="Top 10 Cargos por Salário Médio",
      labels={"usd": "Média Salarial anual (USD)", "cargo": ""}
      
      
    )
    grafico_cargos.update_layout(title_x=0.1, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(grafico_cargos, use_container_width=True)
    
  else:
    st.warning("Nenhum dado disponível no gráfico de cargos.")
    
with colgraf2:
  if not df_filtrado.empty:
    grafico_hist =px.histogram(
      df_filtrado,
      x='usd',
      nbins=30,
      title="Distribuição de Salários anuais",
      labels={"usd": "Faixa Salárial (USD)", "count": ""}  
    )
    
    grafico_hist.update_layout(title_x=0.1)
    st.plotly_chart(grafico_hist, use_container_width=True)
  else:
    st.warning("Nenhum dado disponível no gráfico de distribuição de salários.")

col_graf3 = st.columns(2)

with col_graf3[0]:
  if not df_filtrado.empty:
    remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
    remoto_contagem.columns = ['Tipo_trabalho', 'quantidade']
    grafico_remoto = px.pie(
      remoto_contagem,
      names='Tipo_trabalho',
      values='quantidade',
      title="Proporção dos tipos de trabalhos",
      hole=0.5,
    )
    grafico_remoto.update_traces(textinfo='percent+label')
    grafico_remoto.update_layout(title_x=0.1)
    st.plotly_chart(grafico_remoto, use_container_width=True)
  else:
    st.warning("Nenhum dado disponível no gráfico de trabalho remoto.")
    
    
    # Tabela de dados detalhados
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado) 
    