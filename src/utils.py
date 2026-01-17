"""
Módulo utilitário com funções reutilizáveis para a aplicação Streamlit
"""

import pandas as pd
import numpy as np
from typing import Tuple


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
