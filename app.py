import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Dashboard Streamlit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e descrição
st.title("📊 Dashboard com Streamlit")
st.markdown("---")
st.write("Bem-vindo! Este é um exemplo de aplicação Streamlit com dados interativos.")

# Sidebar para controles
st.sidebar.header("⚙️ Configurações")

# Gerar dados de exemplo
@st.cache_data
def load_data():
    """Carrega dados de exemplo"""
    dates = pd.date_range(start='2024-01-01', periods=100)
    data = {
        'Data': dates,
        'Vendas': np.random.randint(100, 500, 100),
        'Visitantes': np.random.randint(1000, 5000, 100),
        'Conversão': np.random.uniform(0.01, 0.1, 100)
    }
    return pd.DataFrame(data)

df = load_data()

# Filtros
col1, col2, col3 = st.columns(3)

with col1:
    start_date = st.sidebar.date_input(
        "Data inicial",
        value=df['Data'].min().date()
    )

with col2:
    end_date = st.sidebar.date_input(
        "Data final",
        value=df['Data'].max().date()
    )

# Filtrar dados
mask = (df['Data'].dt.date >= start_date) & (df['Data'].dt.date <= end_date)
filtered_df = df.loc[mask]

# KPIs
st.header("📈 KPIs Principais")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="Total de Vendas",
        value=f"R$ {filtered_df['Vendas'].sum():,.0f}",
        delta=f"{filtered_df['Vendas'].mean():.0f} (média)"
    )

with kpi2:
    st.metric(
        label="Total de Visitantes",
        value=f"{filtered_df['Visitantes'].sum():,}",
        delta=f"{filtered_df['Visitantes'].mean():.0f} (média)"
    )

with kpi3:
    st.metric(
        label="Taxa de Conversão",
        value=f"{filtered_df['Conversão'].mean():.2%}",
        delta=f"{filtered_df['Conversão'].std():.4f} (desvio)"
    )

with kpi4:
    st.metric(
        label="Dias no Período",
        value=len(filtered_df),
        delta=f"de {len(df)} total"
    )

st.markdown("---")

# Gráficos
st.header("📊 Análise de Dados")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Vendas por Data")
    fig_vendas = px.line(
        filtered_df,
        x='Data',
        y='Vendas',
        markers=True,
        title="Evolução de Vendas",
        labels={'Vendas': 'Vendas (R$)', 'Data': 'Data'}
    )
    st.plotly_chart(fig_vendas, use_container_width=True)

with col2:
    st.subheader("Visitantes por Data")
    fig_visitantes = px.bar(
        filtered_df,
        x='Data',
        y='Visitantes',
        title="Visitantes por Dia",
        labels={'Visitantes': 'Número de Visitantes', 'Data': 'Data'}
    )
    st.plotly_chart(fig_visitantes, use_container_width=True)

# Tabela de dados
st.header("📋 Dados Brutos")
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# Estatísticas descritivas
st.header("📊 Estatísticas Descritivas")
st.write(filtered_df[['Vendas', 'Visitantes', 'Conversão']].describe())

# Download de dados
st.header("⬇️ Exportar Dados")
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Baixar CSV",
    data=csv,
    file_name=f"dados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

# Rodapé
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p style='color: gray; font-size: 12px;'>
            Desenvolvido com ❤️ usando Streamlit
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
