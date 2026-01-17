import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from src.utils import load_forestfires, calcular_kpis_incendios, agregar_por_mes, agregar_por_grid, MONTH_MAP

# Configuração da página
st.set_page_config(
    page_title="🔥 Incêndios - Parque Montesinho",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para tema florestal
st.markdown("""
<style>
    /* Paleta de cores florestal */
    :root {
        --color-fire: #E63946;
        --color-warning: #F77F00;
        --color-dark: #4A4E69;
        --color-light: #F1FAEE;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    h1, h2, h3 {
        color: #4A4E69;
    }
    
    [data-testid="metric-container"] {
        background-color: white;
        border-left: 4px solid #E63946;
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Título e descrição
st.title("🔥 Análise de Incêndios Florestais - Parque Montesinho")
st.markdown("---")

st.markdown("""
**Parque Natural de Montesinho** - Nordeste de Portugal  
Análise de incêndios florestais com dados de índices de perigo climático (FWI).
""")

# Carregar dados
df = load_forestfires()
kpis = calcular_kpis_incendios(df)

# ========== KPIs PRINCIPAIS ==========
st.header("📊 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🔥 Total de Incêndios",
        value=f"{kpis['total_incendios']}",
        delta="registrados"
    )

with col2:
    st.metric(
        label="🌳 Área Queimada Total",
        value=f"{kpis['area_total']:,.0f}",
        delta="hectares"
    )

with col3:
    st.metric(
        label="📅 Mês Crítico",
        value=kpis['mes_critico_nome'],
        delta=f"{len(df[df['month'] == kpis['mes_critico']])} incêndios"
    )

with col4:
    st.metric(
        label="📍 Região Crítica",
        value=f"({kpis['regiao_critica'][0]}, {kpis['regiao_critica'][1]})",
        delta=f"{kpis['area_regiao_critica']:,.0f} ha"
    )

st.markdown("---")

# ========== GRÁFICOS RESUMIDOS ==========
st.header("📈 Análise Resumida")

col1, col2 = st.columns(2)

# Gráfico 1: Área queimada por mês
with col1:
    monthly_data = agregar_por_mes(df)
    monthly_data['month_nome'] = monthly_data['month'].map(MONTH_MAP)
    # Flatten MultiIndex columns from aggregation
    monthly_data.columns = [
        '_'.join([c for c in col if c]).strip('_') if isinstance(col, tuple) else col
        for col in monthly_data.columns
    ]
    
    fig_monthly = px.line(
        monthly_data,
        x='month_nome',
        y='area_sum',
        markers=True,
        title="Área Queimada por Mês",
        labels={'month_nome': 'Mês', 'area_sum': 'Área (ha)'},
        color_discrete_sequence=['#E63946']
    )
    fig_monthly.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    fig_monthly.update_xaxes(tickangle=45)
    st.plotly_chart(fig_monthly, use_container_width=True)

# Gráfico 2: Frequência de incêndios por mês
with col2:
    fig_freq = px.bar(
        monthly_data,
        x='month_nome',
        y='area_count',
        title="Frequência de Incêndios por Mês",
        labels={'month_nome': 'Mês', 'area_count': 'Quantidade'},
        color_discrete_sequence=['#F77F00']
    )
    fig_freq.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    fig_freq.update_xaxes(tickangle=45)
    st.plotly_chart(fig_freq, use_container_width=True)

st.markdown("---")

# ========== DISTRIBUIÇÃO GEOGRÁFICA ==========
st.header("🗺️ Distribuição Geográfica")

grid_data = agregar_por_grid(df)

# Mapa de calor das coordenadas
heatmap_data = df.groupby(['x', 'y'])['area'].sum().reset_index()
heatmap_pivot = heatmap_data.pivot_table(index='y', columns='x', values='area', fill_value=0)

fig_heatmap = go.Figure(data=go.Heatmap(
    x=heatmap_pivot.columns,
    y=heatmap_pivot.index,
    z=heatmap_pivot.values,
    colorscale='Reds',
    colorbar=dict(title="Área (ha)")
))

fig_heatmap.update_layout(
    title="Mapa de Calor: Área Queimada por Coordenadas",
    xaxis_title="Coordenada X",
    yaxis_title="Coordenada Y",
    height=500
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")

# ========== ESTATÍSTICAS GERAIS ==========
st.header("📊 Estatísticas Descritivas")

stat_cols = st.columns(3)

with stat_cols[0]:
    st.write("**Área Queimada (hectares)**")
    st.write(f"- Mínima: {df['area'].min():.2f} ha")
    st.write(f"- Média: {df['area'].mean():.2f} ha")
    st.write(f"- Máxima: {df['area'].max():.2f} ha")
    st.write(f"- Mediana: {df['area'].median():.2f} ha")

with stat_cols[1]:
    st.write("**Temperatura (°C)**")
    st.write(f"- Mínima: {df['temp'].min():.1f}°C")
    st.write(f"- Média: {df['temp'].mean():.1f}°C")
    st.write(f"- Máxima: {df['temp'].max():.1f}°C")

with stat_cols[2]:
    st.write("**Umidade Relativa (%)**")
    st.write(f"- Mínima: {df['rh'].min():.0f}%")
    st.write(f"- Média: {df['rh'].mean():.0f}%")
    st.write(f"- Máxima: {df['rh'].max():.0f}%")

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
