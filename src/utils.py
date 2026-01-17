"""
Módulo utilitário com funções reutilizáveis para a aplicação Streamlit
Análise de Incêndios Florestais - Parque Montesinho, Portugal
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict
import streamlit as st
from pathlib import Path


def gerar_dados_exemplo(n_dias: int = 100) -> pd.DataFrame:
    """
    Gera dados de exemplo para análise
    
    Args:
        n_dias: Número de dias de dados a gerar
        
    Returns:
        DataFrame com dados de vendas, visitantes e conversão
    """
    dates = pd.date_range(start='2024-01-01', periods=n_dias)
    data = {
        'Data': dates,
        'Vendas': np.random.randint(100, 500, n_dias),
        'Visitantes': np.random.randint(1000, 5000, n_dias),
        'Conversão': np.random.uniform(0.01, 0.1, n_dias)
    }
    return pd.DataFrame(data)


def calcular_kpis(df: pd.DataFrame) -> dict:
    """
    Calcula KPIs principais dos dados
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        Dicionário com KPIs calculados
    """
    return {
        'total_vendas': df['Vendas'].sum(),
        'media_vendas': df['Vendas'].mean(),
        'total_visitantes': df['Visitantes'].sum(),
        'media_visitantes': df['Visitantes'].mean(),
        'taxa_conversao_media': df['Conversão'].mean(),
        'desvio_conversao': df['Conversão'].std()
    }


def formatar_moeda(valor: float) -> str:
    """
    Formata valor como moeda brasileira
    
    Args:
        valor: Valor a formatar
        
    Returns:
        String formatada como R$ XX,XX
    """
    return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')


def formatar_percentual(valor: float, casas: int = 2) -> str:
    """
    Formata valor como percentual
    
    Args:
        valor: Valor entre 0 e 1
        casas: Casas decimais
        
    Returns:
        String formatada como XX,XX%
    """
    return f"{valor*100:.{casas}f}%"


# ========== FUNÇÕES PARA ANÁLISE DE INCÊNDIOS FLORESTAIS ==========

@st.cache_data
def load_forestfires() -> pd.DataFrame:
    """
    Carrega e processa dados de incêndios florestais do Parque Montesinho
    
    Returns:
        DataFrame com dados de incêndios
    """
    csv_path = Path(__file__).parent.parent / "data" / "forestfires.csv"
    df = pd.read_csv(csv_path)
    
    # Padronizar nomes de colunas
    df.columns = df.columns.str.lower().str.strip()
    
    return df


# Dicionário explicativo dos componentes FWI
FWI_DESCRIPTIONS = {
    "FFMC": {
        "nome": "Fine Fuel Moisture Code",
        "profundidade": "0-2 cm",
        "descricao": "Umidade dos combustíveis finos superficiais (agulhas, folhas secas)",
        "interpretacao": "Indica facilidade de ignição de novo fogo",
        "range": "18.7 - 96.2"
    },
    "DMC": {
        "nome": "Duff Moisture Code",
        "profundidade": "2-7 cm",
        "descricao": "Umidade da matéria orgânica levemente compactada (palha, detritos)",
        "interpretacao": "Afeta profundidade de penetração e duração do incêndio",
        "range": "1.1 - 291.3"
    },
    "DC": {
        "nome": "Drought Code",
        "profundidade": "8-18 cm",
        "descricao": "Déficit hídrico de longo prazo em camadas profundas",
        "interpretacao": "Reflete secas prolongadas, afeta combustível profundo",
        "range": "7.9 - 860.6"
    },
    "ISI": {
        "nome": "Initial Spread Index",
        "profundidade": "Taxa de propagação",
        "descricao": "Taxa esperada de propagação baseada em vento e FFMC",
        "interpretacao": "Prediz velocidade de propagação do incêndio",
        "range": "0 - 56.1"
    }
}

# Descrições de variáveis meteorológicas
WEATHER_DESCRIPTIONS = {
    "temp": {
        "nome": "Temperatura",
        "unidade": "°C",
        "interpretacao": "Relação direta com risco de incêndio (maior temp = maior risco)"
    },
    "RH": {
        "nome": "Umidade Relativa",
        "unidade": "%",
        "interpretacao": "Relação inversa com risco (menor umidade = maior risco)"
    },
    "wind": {
        "nome": "Velocidade do Vento",
        "unidade": "km/h",
        "interpretacao": "Afeta propagação (maior vento = propagação mais rápida)"
    },
    "rain": {
        "nome": "Precipitação",
        "unidade": "mm",
        "interpretacao": "Reduz risco de incêndio, afeta todos os códigos de umidade"
    }
}

# Mapeamento de meses
MONTH_MAP = {
    "jan": "Janeiro", "feb": "Fevereiro", "mar": "Março", "apr": "Abril",
    "may": "Maio", "jun": "Junho", "jul": "Julho", "aug": "Agosto",
    "sep": "Setembro", "oct": "Outubro", "nov": "Novembro", "dec": "Dezembro"
}

MONTH_ORDER = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def calcular_kpis_incendios(df: pd.DataFrame) -> Dict:
    """
    Calcula KPIs principais para análise de incêndios
    
    Args:
        df: DataFrame com dados de incêndios
        
    Returns:
        Dicionário com KPIs calculados
    """
    total_incendios = len(df)
    area_total = df['area'].sum()
    area_media = df['area'].mean()
    area_max = df['area'].max()
    
    # Mês crítico
    mes_mais_incendios = df['month'].value_counts().idxmax()
    mes_critico_nome = MONTH_MAP.get(mes_mais_incendios, mes_mais_incendios)
    
    # Região crítica (coordenadas com mais área queimada)
    regiao_critica = df.groupby(['x', 'y'])['area'].sum().idxmax()
    area_regiao_critica = df.groupby(['x', 'y'])['area'].sum().max()
    
    return {
        'total_incendios': total_incendios,
        'area_total': area_total,
        'area_media': area_media,
        'area_max': area_max,
        'mes_critico': mes_mais_incendios,
        'mes_critico_nome': mes_critico_nome,
        'regiao_critica': regiao_critica,
        'area_regiao_critica': area_regiao_critica
    }


def agregar_por_grid(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega dados por coordenadas de grid (X, Y)
    
    Args:
        df: DataFrame com dados de incêndios
        
    Returns:
        DataFrame agregado por grid
    """
    return df.groupby(['x', 'y']).agg({
        'area': ['sum', 'mean', 'count'],
        'temp': 'mean',
        'rh': 'mean',
        'wind': 'mean',
        'ffmc': 'mean',
        'dmc': 'mean',
        'dc': 'mean',
        'isi': 'mean'
    }).reset_index()


def agregar_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega dados por mês
    
    Args:
        df: DataFrame com dados de incêndios
        
    Returns:
        DataFrame agregado por mês
    """
    agg_data = df.groupby('month').agg({
        'area': ['sum', 'mean', 'count'],
        'temp': 'mean',
        'rh': 'mean',
        'wind': 'mean',
        'ffmc': 'mean',
        'dmc': 'mean',
        'dc': 'mean',
        'isi': 'mean'
    }).reset_index()
    
    # Converter order de mês para numérico para ordenação
    agg_data['month_order'] = agg_data['month'].apply(lambda x: MONTH_ORDER.index(x))
    agg_data = agg_data.sort_values('month_order').drop('month_order', axis=1)
    
    return agg_data
