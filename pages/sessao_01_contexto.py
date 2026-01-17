import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.utils import (
    load_forestfires, FWI_DESCRIPTIONS, WEATHER_DESCRIPTIONS, MONTH_MAP
)

st.set_page_config(
    page_title="Sessão 01 - Contexto",
    page_icon="📖",
    layout="wide"
)

# Esconder navegação padrão do Streamlit
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Barra lateral customizada
with st.sidebar:
    st.title("📚 Navegação")
    st.page_link("app.py", label="Resumo", icon="📊")
    st.page_link("pages/sessao_01_contexto.py", label="Contexto", icon="🌲")
    st.page_link("pages/sessao_02_perguntas.py", label="Perguntas", icon="❓")
    st.page_link("pages/sobre.py", label="Sobre", icon="ℹ️")

st.title("📖 Sessão 01: Entendimento do Problema e do Contexto")
st.markdown("---")

# Carregar dados
df = load_forestfires()

# ========== SEÇÃO 1: O QUE ESTÁ SENDO MEDIDO? ==========
st.header("❓ O que está sendo medido?")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 🔥 Incêndios Florestais do Parque Natural de Montesinho

    **Localização:** Nordeste de Portugal  
    **Período:** Dados históricos de incêndios florestais  
    **Total de Registros:** {0} incêndios registrados

    #### O Problema
    Incêndios florestais são uma ameaça significativa aos ecossistemas portugueses. 
    O Parque Natural de Montesinho, localizado na região nordeste, é uma área crítica 
    para conservação florestal.

    #### Objetivo da Análise
    Entender os **padrões espaciais e temporais** dos incêndios e sua correlação com 
    **condições meteorológicas e índices de perigo climático (FWI)** para:
    - Identificar regiões críticas
    - Prever períodos de alto risco
    - Orientar políticas de prevenção e combate

    #### Área de Estudo
    - **Grid de Coordenadas:** X (1-9) × Y (2-9)
    - **Cada célula representa uma zona do parque**
    - **Dados espaciais permitem mapear hotspots de incêndios**
    """.format(len(df)))

with col2:
    st.info("""
    ### 📊 Dataset
    - **Registros:** {0}
    - **Variáveis:** 13
    - **Período:** Múltiplos anos
    - **Fonte:** Dados históricos ICNF
    """.format(len(df)))

st.markdown("---")

# ========== SEÇÃO 2: QUAIS SÃO AS VARIÁVEIS? ==========
st.header("📋 Quais são as variáveis disponíveis?")

# Criar tabela de variáveis
variables_data = {
    "Variável": ["X", "Y", "month", "day", "FFMC", "DMC", "DC", "ISI", "temp", "RH", "wind", "rain", "area"],
    "Tipo": ["Inteiro", "Inteiro", "Texto", "Texto", "Float", "Float", "Float", "Float", "Float", "Float", "Float", "Float", "Float"],
    "Mínimo": [
        df['x'].min(), df['y'].min(), "-", "-",
        f"{df['ffmc'].min():.1f}", f"{df['dmc'].min():.1f}", f"{df['dc'].min():.1f}", f"{df['isi'].min():.1f}",
        f"{df['temp'].min():.1f}", f"{df['rh'].min():.0f}", f"{df['wind'].min():.1f}", f"{df['rain'].min():.1f}",
        f"{df['area'].min():.2f}"
    ],
    "Máximo": [
        df['x'].max(), df['y'].max(), "-", "-",
        f"{df['ffmc'].max():.1f}", f"{df['dmc'].max():.1f}", f"{df['dc'].max():.1f}", f"{df['isi'].max():.1f}",
        f"{df['temp'].max():.1f}", f"{df['rh'].max():.0f}", f"{df['wind'].max():.1f}", f"{df['rain'].max():.1f}",
        f"{df['area'].max():.2f}"
    ],
    "Média": [
        f"{df['x'].mean():.1f}", f"{df['y'].mean():.1f}", "-", "-",
        f"{df['ffmc'].mean():.1f}", f"{df['dmc'].mean():.1f}", f"{df['dc'].mean():.1f}", f"{df['isi'].mean():.1f}",
        f"{df['temp'].mean():.1f}", f"{df['rh'].mean():.0f}", f"{df['wind'].mean():.1f}", f"{df['rain'].mean():.1f}",
        f"{df['area'].mean():.2f}"
    ]
}

st.dataframe(pd.DataFrame(variables_data), use_container_width=True)

# ========== EXPLICAÇÕES DETALHADAS ==========
st.markdown("---")
st.header("🔍 Explicações Detalhadas das Variáveis")

# Abas para organizar as informações
tab1, tab2, tab3 = st.tabs(["📍 Localização", "🌡️ FWI - Índices de Perigo", "🌤️ Variáveis Meteorológicas"])

with tab1:
    st.subheader("Coordenadas Geográficas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**X - Coordenada Horizontal**")
        st.info(f"Intervalo: {df['x'].min()} a {df['x'].max()}")
        st.write("Posição no eixo horizontal do Parque Montesinho")
    
    with col2:
        st.write("**Y - Coordenada Vertical**")
        st.info(f"Intervalo: {df['y'].min()} a {df['y'].max()}")
        st.write("Posição no eixo vertical do Parque Montesinho")
    
    st.write("**month - Mês do Ano**")
    st.write("Abreviado em 3 letras (jan, feb, mar, ..., dec)")
    
    st.write("**day - Dia da Semana**")
    st.write("Abreviado em 3 letras (mon, tue, wed, thu, fri, sat, sun)")

with tab2:
    st.subheader("Índices de Perigo de Incêndio (FWI)")
    
    for code, info in FWI_DESCRIPTIONS.items():
        with st.expander(f"🔥 **{code}** - {info['nome']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Profundidade:** {info['profundidade']}")
                st.write(f"**Range:** {info['range']}")
                st.write(f"**Descrição:**")
                st.write(info['descricao'])
            
            with col2:
                st.write(f"**Interpretação:**")
                st.warning(info['interpretacao'])
                
                # Mostrar distribuição
                if code in df.columns:
                    st.write(f"**Estatísticas no Dataset:**")
                    st.write(f"- Mínimo: {df[code].min():.2f}")
                    st.write(f"- Máximo: {df[code].max():.2f}")
                    st.write(f"- Média: {df[code].mean():.2f}")

with tab3:
    st.subheader("Variáveis Meteorológicas e Resultado")
    
    for var, info in WEATHER_DESCRIPTIONS.items():
        col_name = var.lower()
        with st.expander(f"🌡️ **{var}** - {info['nome']} ({info['unidade']})", expanded=False):
            st.write(f"**Interpretação:** {info['interpretacao']}")
            st.write(f"**Estatísticas no Dataset:**")
            st.write(f"- Mínimo: {df[col_name].min():.2f} {info['unidade']}")
            st.write(f"- Máximo: {df[col_name].max():.2f} {info['unidade']}")
            st.write(f"- Média: {df[col_name].mean():.2f} {info['unidade']}")
    
    st.write("---")
    st.write("**area - Área Queimada (hectares)**")
    st.write("""
    Variável de resposta (target) - Quantidade de hectares queimados em cada incêndio.
    - Valores variam de 0 a 1090.84 hectares
    - Maioria dos incêndios são pequenos (perto de 0 ha)
    - Alguns incêndios significativos queimam áreas extensas
    """)

st.markdown("---")

# ========== DISTRIBUIÇÕES DOS COMPONENTES FWI ==========
st.header("📊 Distribuições dos Componentes FWI")

col1, col2, col3, col4 = st.columns(4)

fwi_components = ['ffmc', 'dmc', 'dc', 'isi']

for idx, col in enumerate([col1, col2, col3, col4]):
    with col:
        component = fwi_components[idx]
        fig = px.histogram(
            df,
            x=component,
            nbins=30,
            title=f"Distribuição {component}",
            color_discrete_sequence=['#E63946']
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ========== MATRIZ DE CORRELAÇÃO ==========
st.header("🔗 Correlação Entre Variáveis")

st.write("Matriz de correlação entre índices FWI, variáveis meteorológicas e área queimada:")

correlation_vars = ['ffmc', 'dmc', 'dc', 'isi', 'temp', 'rh', 'wind', 'rain', 'area']
corr_matrix = df[correlation_vars].corr()

fig_corr = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale='RdBu',
    zmid=0,
    text=corr_matrix.values.round(2),
    texttemplate='%{text}',
    textfont={"size": 10},
    colorbar=dict(title="Correlação")
))

fig_corr.update_layout(height=500, width=700)
st.plotly_chart(fig_corr, use_container_width=True)

st.info("""
💡 **Interpretação:**
- **Correlação positiva (+1 a 0):** Variáveis aumentam juntas
- **Correlação negativa (-1 a 0):** Uma aumenta enquanto a outra diminui
- **Próximo de 0:** Pouca ou nenhuma relação
""")

st.markdown("---")

# ========== RESUMO ESTATÍSTICO ==========
st.header("📈 Resumo Estatístico Completo")

with st.expander("Ver estatísticas descritivas detalhadas", expanded=False):
    st.dataframe(df.describe().round(2), use_container_width=True)
