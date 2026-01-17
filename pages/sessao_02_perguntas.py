import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.utils import load_forestfires, agregar_por_mes, agregar_por_grid, MONTH_MAP, MONTH_ORDER

st.set_page_config(
    page_title="Sessão 02 - Perguntas",
    page_icon="❓",
    layout="wide"
)

st.title("❓ Sessão 02: Respondendo as Perguntas sobre Incêndios")
st.markdown("---")

# Carregar dados
df = load_forestfires()

# Criar abas para as 3 perguntas
tab1, tab2, tab3 = st.tabs([
    "📍 Onde ocorrem?",
    "🔥 Regiões Críticas?",
    "📅 Quais Meses?"
])

# ========== PERGUNTA 1: ONDE OCORREM OS INCÊNDIOS? ==========
with tab1:
    st.header("📍 Pergunta 1: Onde ocorrem mais incêndios?")
    
    st.write("""
    Analisamos a **distribuição geográfica dos incêndios** no Parque Montesinho 
    usando as coordenadas X e Y para identificar **hotspots** (áreas de concentração).
    """)
    
    # Mapa de calor principal
    st.subheader("Mapa de Calor: Concentração de Incêndios")
    
    # Preparar dados para heatmap
    heatmap_data = df.groupby(['x', 'y'])['area'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot_table(index='y', columns='x', values='area', fill_value=0)
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale='Reds',
        colorbar=dict(title="Área<br>Queimada (ha)"),
        hovertemplate="X: %{x}<br>Y: %{y}<br>Área: %{z:.2f} ha<extra></extra>"
    ))
    
    fig_heatmap.update_layout(
        title="Concentração de Área Queimada por Coordenadas (X, Y)",
        xaxis_title="Coordenada X",
        yaxis_title="Coordenada Y",
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Análise textual
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Insights Principais:**")
        
        # Top 3 coordenadas com mais incêndios
        top_coords_freq = df.groupby(['x', 'y']).size().reset_index(name='count').sort_values('count', ascending=False).head(3)
        st.write("**Top 3 Coordenadas por Frequência:**")
        for idx, row in top_coords_freq.iterrows():
            st.write(f"- ({row['x']}, {row['y']}): {row['count']} incêndios")
        
        # Top 3 coordenadas com mais área
        top_coords_area = df.groupby(['x', 'y'])['area'].sum().reset_index().sort_values('area', ascending=False).head(3)
        st.write("\n**Top 3 Coordenadas por Área Queimada:**")
        for idx, row in top_coords_area.iterrows():
            st.write(f"- ({row['x']}, {row['y']}): {row['area']:.2f} ha")
    
    with col2:
        st.write("**Padrão Espacial:**")
        st.info("""
        Os incêndios não estão uniformemente distribuídos. Existem:
        - **Clusters visíveis** no mapa de calor
        - **Regiões com alta frequência** mas baixa severidade
        - **Regiões com severidade extrema** (poucos incêndios, muita área)
        - **Padrão pode estar ligado a topografia, vegetação ou proximidade a habitações**
        """)
    
    # Scatter plot alternativo
    st.subheader("Visualização Alternativa: Scatter Plot")
    
    fig_scatter = px.scatter(
        df,
        x='x',
        y='y',
        size='area',
        color='area',
        hover_data=['month', 'temp', 'rh', 'ffmc', 'area'],
        color_continuous_scale='Reds',
        title="Localização de Incêndios (tamanho = área queimada)",
        labels={'x': 'Coordenada X', 'y': 'Coordenada Y', 'area': 'Área (ha)'}
    )
    
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

# ========== PERGUNTA 2: REGIÕES CRÍTICAS ==========
with tab2:
    st.header("🔥 Pergunta 2: Existem regiões mais críticas?")
    
    st.write("""
    Identificamos as **regiões (células de grid) mais críticas** usando dois critérios:
    1. **Frequência:** Quantos incêndios ocorreram
    2. **Severidade:** Quantidade total de área queimada
    """)
    
    # Agregar por grid
    grid_data = df.groupby(['x', 'y']).agg({
        'area': ['sum', 'mean', 'count', 'max'],
        'temp': 'mean',
        'rh': 'mean',
        'ffmc': 'mean',
        'dmc': 'mean',
        'dc': 'mean',
        'isi': 'mean'
    }).round(2)
    
    grid_data.columns = ['Área Total (ha)', 'Área Média (ha)', 'Frequência', 'Área Máxima (ha)',
                         'Temp Média', 'Umidade Média', 'FFMC Médio', 'DMC Médio', 'DC Médio', 'ISI Médio']
    grid_data = grid_data.sort_values('Área Total (ha)', ascending=False).reset_index()
    
    # Seletor de critério
    criterio = st.radio(
        "Ordenar regiões por:",
        ["Área Total Queimada", "Frequência de Incêndios", "Área Máxima em um Incêndio"],
        horizontal=True
    )
    
    if criterio == "Área Total Queimada":
        grid_sorted = grid_data.sort_values('Área Total (ha)', ascending=False)
        col_ordenacao = 'Área Total (ha)'
    elif criterio == "Frequência de Incêndios":
        grid_sorted = grid_data.sort_values('Frequência', ascending=False)
        col_ordenacao = 'Frequência'
    else:
        grid_sorted = grid_data.sort_values('Área Máxima (ha)', ascending=False)
        col_ordenacao = 'Área Máxima (ha)'
    
    st.subheader(f"🏆 Top 10 Regiões Críticas (por {criterio})")
    
    # Tabela formatada
    top_10 = grid_sorted.head(10)
    
    # Colorir a coluna de ordenação
    def color_row(row):
        colors = ['background-color: #E63946'] * len(row)
        return colors
    
    st.dataframe(
        top_10.style.format({
            'Área Total (ha)': '{:.2f}',
            'Área Média (ha)': '{:.2f}',
            'Frequência': '{:.0f}',
            'Área Máxima (ha)': '{:.2f}',
            'Temp Média': '{:.1f}',
            'Umidade Média': '{:.0f}',
            'FFMC Médio': '{:.1f}',
            'DMC Médio': '{:.1f}',
            'DC Médio': '{:.1f}',
            'ISI Médio': '{:.1f}'
        }),
        use_container_width=True
    )
    
    # Gráfico de ranking
    st.subheader("Visualização: Ranking de Regiões")
    
    top_15 = grid_sorted.head(15).copy()
    top_15['Coordenada'] = '(' + top_15['x'].astype(str) + ', ' + top_15['y'].astype(str) + ')'
    
    if criterio == "Área Total Queimada":
        y_col = 'Área Total (ha)'
    elif criterio == "Frequência de Incêndios":
        y_col = 'Frequência'
    else:
        y_col = 'Área Máxima (ha)'
    
    fig_ranking = px.bar(
        top_15,
        x=y_col,
        y='Coordenada',
        orientation='h',
        title=f"Top 15 Regiões Críticas - {criterio}",
        color=y_col,
        color_continuous_scale='Reds',
        labels={'Coordenada': 'Coordenadas (X, Y)'},
        text=y_col
    )
    
    fig_ranking.update_traces(texttemplate='%{x:.0f}', textposition='outside')
    fig_ranking.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_ranking, use_container_width=True)
    
    # Análise por características
    st.subheader("📊 Características Meteorológicas das Regiões Críticas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Regiões Críticas - Perfil Meteorológico:**")
        top_3_coords = top_10[['x', 'y']].head(3)
        for _, row in top_3_coords.iterrows():
            coord = f"({row['x']}, {row['y']})"
            data_coord = top_10[top_10['x'] == row['x']]
            data_coord = data_coord[data_coord['y'] == row['y']].iloc[0]
            st.write(f"""
            **{coord}**
            - Temp: {data_coord['Temp Média']:.1f}°C
            - Umidade: {data_coord['Umidade Média']:.0f}%
            - FFMC: {data_coord['FFMC Médio']:.1f}
            - ISI: {data_coord['ISI Médio']:.1f}
            """)
    
    with col2:
        st.write("**Comparação com Média Geral:**")
        media_geral = {
            'Temp': df['temp'].mean(),
            'Umidade': df['rh'].mean(),
            'FFMC': df['ffmc'].mean(),
            'ISI': df['isi'].mean()
        }
        st.write(f"""
        **Média do Parque:**
        - Temp: {media_geral['Temp']:.1f}°C
        - Umidade: {media_geral['Umidade']:.0f}%
        - FFMC: {media_geral['FFMC']:.1f}
        - ISI: {media_geral['ISI']:.1f}
        """)

# ========== PERGUNTA 3: SAZONALIDADE MENSAL ==========
with tab3:
    st.header("📅 Pergunta 3: Em quais meses ocorrem mais incêndios?")
    
    st.write("""
    Analisamos a **distribuição temporal** dos incêndios, identificando períodos 
    de alto risco e padrões sazonais ao longo do ano.
    """)
    
    # Agregar por mês
    monthly_data = df.groupby('month').agg({
        'area': ['sum', 'mean', 'count', 'max', 'std'],
        'temp': 'mean',
        'rh': 'mean',
        'ffmc': 'mean',
        'dmc': 'mean',
        'dc': 'mean',
        'isi': 'mean'
    }).round(2)
    
    monthly_data.columns = ['Área Total', 'Área Média', 'Frequência', 'Área Máxima', 'Desvio Área',
                           'Temp Média', 'Umidade Média', 'FFMC Médio', 'DMC Médio', 'DC Médio', 'ISI Médio']
    
    # Ordenar por ordem de meses
    monthly_data = monthly_data.reindex([m for m in MONTH_ORDER if m in monthly_data.index])
    monthly_data['Mês'] = monthly_data.index.map(MONTH_MAP)
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Frequência de Incêndios por Mês")
        fig_freq = px.bar(
            monthly_data.reset_index(),
            x='Mês',
            y='Frequência',
            title="Quantidade de Incêndios por Mês",
            color='Frequência',
            color_continuous_scale='Reds',
            text='Frequência'
        )
        fig_freq.update_traces(textposition='outside')
        fig_freq.update_layout(height=400, showlegend=False)
        fig_freq.update_xaxes(tickangle=45)
        st.plotly_chart(fig_freq, use_container_width=True)
    
    with col2:
        st.subheader("Área Total Queimada por Mês")
        fig_area = px.bar(
            monthly_data.reset_index(),
            x='Mês',
            y='Área Total',
            title="Área Queimada Total por Mês",
            color='Área Total',
            color_continuous_scale='Reds',
            text='Área Total'
        )
        fig_area.update_traces(texttemplate='%{y:.0f}', textposition='outside')
        fig_area.update_layout(height=400, showlegend=False)
        fig_area.update_xaxes(tickangle=45)
        st.plotly_chart(fig_area, use_container_width=True)
    
    # Análise combinada
    st.subheader("📊 Série Temporal: Evolução ao Longo do Ano")
    
    fig_combined = go.Figure()
    
    # Eixo Y primário: Frequência
    fig_combined.add_trace(go.Scatter(
        x=monthly_data['Mês'],
        y=monthly_data['Frequência'],
        name='Frequência',
        mode='lines+markers',
        yaxis='y1',
        line=dict(color='#E63946', width=3),
        marker=dict(size=10)
    ))
    
    # Eixo Y secundário: Temperatura média
    fig_combined.add_trace(go.Scatter(
        x=monthly_data['Mês'],
        y=monthly_data['Temp Média'],
        name='Temperatura Média',
        mode='lines+markers',
        yaxis='y2',
        line=dict(color='#F77F00', width=2, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig_combined.update_layout(
        title="Relação entre Frequência de Incêndios e Temperatura",
        xaxis=dict(title='Mês'),
        yaxis=dict(
            title=dict(text='Frequência de Incêndios', font=dict(color='#E63946')),
            tickfont=dict(color='#E63946')
        ),
        yaxis2=dict(
            title=dict(text='Temperatura Média (°C)', font=dict(color='#F77F00')),
            tickfont=dict(color='#F77F00'),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        height=450,
        hovermode='x unified',
        legend=dict(x=0.02, y=0.98)
    )
    
    st.plotly_chart(fig_combined, use_container_width=True)
    
    # Box plot: Distribuição de área por mês
    st.subheader("📦 Distribuição de Áreas Queimadas por Mês")
    
    df_plot = df.copy()
    df_plot['Mês'] = df_plot['month'].map(MONTH_MAP)
    df_plot = df_plot.sort_values('Mês', key=lambda x: x.map({v: k for k, v in MONTH_MAP.items()}).map(lambda y: MONTH_ORDER.index(y)))
    
    fig_box = px.box(
        df_plot,
        x='Mês',
        y='area',
        title="Box Plot: Variação de Área Queimada por Mês",
        color='Mês',
        color_discrete_sequence=px.colors.sequential.Reds,
        labels={'area': 'Área Queimada (ha)', 'Mês': 'Mês'}
    )
    
    fig_box.update_layout(height=400, showlegend=False)
    fig_box.update_xaxes(tickangle=45)
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Tabela resumida
    st.subheader("📋 Resumo Mensal Detalhado")
    
    monthly_display = monthly_data[['Mês', 'Frequência', 'Área Total', 'Área Média', 'Área Máxima',
                                     'Temp Média', 'Umidade Média', 'FFMC Médio', 'ISI Médio']].reset_index(drop=True)
    
    st.dataframe(
        monthly_display.style.format({
            'Frequência': '{:.0f}',
            'Área Total': '{:.2f}',
            'Área Média': '{:.2f}',
            'Área Máxima': '{:.2f}',
            'Temp Média': '{:.1f}',
            'Umidade Média': '{:.0f}',
            'FFMC Médio': '{:.1f}',
            'ISI Médio': '{:.1f}'
        }),
        use_container_width=True
    )
    
    # Insights finais
    st.subheader("💡 Insights Principais sobre Sazonalidade")
    
    col1, col2, col3 = st.columns(3)
    
    # Mês com mais incêndios
    mes_max_freq = monthly_data['Frequência'].idxmax()
    freq_max = monthly_data.loc[mes_max_freq, 'Frequência']
    
    # Mês com mais área
    mes_max_area = monthly_data['Área Total'].idxmax()
    area_max = monthly_data.loc[mes_max_area, 'Área Total']
    
    # Mês mais quente
    mes_quente = monthly_data['Temp Média'].idxmax()
    temp_max = monthly_data.loc[mes_quente, 'Temp Média']
    
    with col1:
        st.warning(f"""
        🔥 **Mês com Mais Frequência**
        
        {MONTH_MAP[mes_max_freq]}
        
        {freq_max:.0f} incêndios registrados
        """)
    
    with col2:
        st.error(f"""
        🌳 **Mês com Mais Área Queimada**
        
        {MONTH_MAP[mes_max_area]}
        
        {area_max:.0f} hectares
        """)
    
    with col3:
        st.info(f"""
        🌡️ **Mês Mais Quente**
        
        {MONTH_MAP[mes_quente]}
        
        {temp_max:.1f}°C em média
        """)

st.markdown("---")
st.success("✅ Sessão 02 concluída! Você explorou os padrões espaciais, críticos e temporais dos incêndios do Parque Montesinho.")
