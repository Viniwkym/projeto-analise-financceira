"""
Módulo para leitura, limpeza e validação de arquivos CSV com dados financeiros.
"""

import pandas as pd
from typing import Dict, List, Optional


class DataParserError(Exception):
    """Exceção customizada para erros de parsing de dados."""
    pass


def clean_numeric_value(value: str) -> float:
    """
    Limpa e converte valores numéricos de strings para float.
    
    Remove símbolos de moeda, espaços e converte vírgulas em pontos.
    
    Args:
        value: String contendo o valor numérico
        
    Returns:
        Valor convertido para float
        
    Raises:
        ValueError: Se o valor não puder ser convertido
    """
    if pd.isna(value):
        return 0.0
    
    if isinstance(value, (int, float)):
        return float(value)
    
    cleaned = str(value).strip()
    cleaned = cleaned.replace('R$', '').replace('$', '')
    cleaned = cleaned.replace('.', '').replace(',', '.')
    cleaned = cleaned.strip()
    
    if not cleaned or cleaned == '-':
        return 0.0
    
    return float(cleaned)


def validate_csv_structure(df: pd.DataFrame) -> None:
    """
    Valida se o DataFrame possui a estrutura esperada.
    
    Args:
        df: DataFrame a ser validado
        
    Raises:
        DataParserError: Se a estrutura não for válida
    """
    required_accounts = [
        'Receita Líquida',
        'EBITDA',
        'Lucro Líquido',
        'Ativo Circulante',
        'Ativo Total',
        'Estoque',
        'Passivo Circulante',
        'Passivo Exigível Total',
        'Dívida Bruta',
        'Caixa e Equivalentes',
        'Patrimônio Líquido',
        'Fluxo de Caixa Operacional'
    ]
    
    if 'Conta' not in df.columns:
        raise DataParserError("A coluna 'Conta' não foi encontrada no CSV.")
    
    accounts_in_file = df['Conta'].str.strip().tolist()
    missing_accounts = [acc for acc in required_accounts if acc not in accounts_in_file]
    
    if missing_accounts:
        raise DataParserError(
            f"Contas obrigatórias faltando no CSV: {', '.join(missing_accounts)}"
        )
    
    year_columns = [col for col in df.columns if col != 'Conta']
    if len(year_columns) < 3:
        raise DataParserError(
            "O arquivo deve conter pelo menos 3 anos de dados históricos."
        )


def parse_csv(file_path: str) -> pd.DataFrame:
    """
    Lê e processa arquivo CSV com dados financeiros.
    
    Args:
        file_path: Caminho para o arquivo CSV
        
    Returns:
        DataFrame limpo e validado com dados financeiros
        
    Raises:
        DataParserError: Se houver erro na leitura ou validação
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file_path, encoding='latin-1')
        except Exception as e:
            raise DataParserError(f"Erro ao ler o arquivo CSV: {str(e)}")
    except Exception as e:
        raise DataParserError(f"Erro ao ler o arquivo CSV: {str(e)}")
    
    df.columns = df.columns.str.strip()
    df['Conta'] = df['Conta'].str.strip()
    
    validate_csv_structure(df)
    
    year_columns = [col for col in df.columns if col != 'Conta']
    
    for col in year_columns:
        df[col] = df[col].apply(clean_numeric_value)
    
    return df


def get_years(df: pd.DataFrame) -> List[str]:
    """
    Extrai a lista de anos disponíveis no DataFrame.
    
    Args:
        df: DataFrame com dados financeiros
        
    Returns:
        Lista de anos (colunas) ordenados
    """
    return [col for col in df.columns if col != 'Conta']


def get_account_value(df: pd.DataFrame, account_name: str, year: str) -> float:
    """
    Busca o valor de uma conta específica em um ano específico.
    
    Args:
        df: DataFrame com dados financeiros
        account_name: Nome da conta contábil
        year: Ano desejado
        
    Returns:
        Valor da conta no ano especificado (0.0 se não encontrado)
    """
    try:
        row = df[df['Conta'] == account_name]
        if row.empty:
            return 0.0
        return float(row[year].iloc[0])
    except (KeyError, IndexError):
        return 0.0


def get_all_data_for_year(df: pd.DataFrame, year: str) -> Dict[str, float]:
    """
    Retorna todos os dados financeiros de um ano específico.
    
    Args:
        df: DataFrame com dados financeiros
        year: Ano desejado
        
    Returns:
        Dicionário com todas as contas e seus valores
    """
    data = {}
    for _, row in df.iterrows():
        account = row['Conta']
        value = row[year]
        data[account] = float(value)
    return data
