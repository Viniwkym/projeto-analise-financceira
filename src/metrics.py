"""
Módulo para cálculo dos indicadores financeiros fundamentais.
"""

from typing import Dict, Optional


class FinancialMetrics:
    """Classe para cálculo de indicadores financeiros."""
    
    def __init__(self, financial_data: Dict[str, float]):
        """
        Inicializa a classe com os dados financeiros de um período.
        
        Args:
            financial_data: Dicionário com as contas contábeis e seus valores
        """
        self.data = financial_data
    
    def _safe_division(self, numerator: float, denominator: float) -> Optional[float]:
        """
        Realiza divisão segura, retornando None se denominador for zero.
        
        Args:
            numerator: Numerador da divisão
            denominator: Denominador da divisão
            
        Returns:
            Resultado da divisão ou None se denominador for zero
        """
        if denominator == 0 or denominator is None:
            return None
        return numerator / denominator
    
    def liquidez_corrente(self) -> Optional[float]:
        """
        Calcula a Liquidez Corrente.
        
        Fórmula: Ativo Circulante / Passivo Circulante
        
        Returns:
            Liquidez Corrente ou None se não puder calcular
        """
        ativo_circulante = self.data.get('Ativo Circulante', 0)
        passivo_circulante = self.data.get('Passivo Circulante', 0)
        return self._safe_division(ativo_circulante, passivo_circulante)
    
    def liquidez_seca(self) -> Optional[float]:
        """
        Calcula a Liquidez Seca.
        
        Fórmula: (Ativo Circulante - Estoque) / Passivo Circulante
        
        Returns:
            Liquidez Seca ou None se não puder calcular
        """
        ativo_circulante = self.data.get('Ativo Circulante', 0)
        estoque = self.data.get('Estoque', 0)
        passivo_circulante = self.data.get('Passivo Circulante', 0)
        return self._safe_division(ativo_circulante - estoque, passivo_circulante)
    
    def endividamento_geral(self) -> Optional[float]:
        """
        Calcula o Endividamento Geral (em percentual).
        
        Fórmula: (Passivo Exigível Total / Ativo Total) * 100
        
        Returns:
            Endividamento Geral em % ou None se não puder calcular
        """
        passivo_exigivel = self.data.get('Passivo Exigível Total', 0)
        ativo_total = self.data.get('Ativo Total', 0)
        result = self._safe_division(passivo_exigivel, ativo_total)
        return result * 100 if result is not None else None
    
    def divida_liquida_ebitda(self) -> Optional[float]:
        """
        Calcula a relação Dívida Líquida / EBITDA.
        
        Fórmula: (Dívida Bruta - Caixa e Equivalentes) / EBITDA
        
        Returns:
            Dívida Líquida / EBITDA ou None se não puder calcular
        """
        divida_bruta = self.data.get('Dívida Bruta', 0)
        caixa = self.data.get('Caixa e Equivalentes', 0)
        ebitda = self.data.get('EBITDA', 0)
        divida_liquida = divida_bruta - caixa
        return self._safe_division(divida_liquida, ebitda)
    
    def margem_ebitda(self) -> Optional[float]:
        """
        Calcula a Margem EBITDA (em percentual).
        
        Fórmula: (EBITDA / Receita Líquida) * 100
        
        Returns:
            Margem EBITDA em % ou None se não puder calcular
        """
        ebitda = self.data.get('EBITDA', 0)
        receita_liquida = self.data.get('Receita Líquida', 0)
        result = self._safe_division(ebitda, receita_liquida)
        return result * 100 if result is not None else None
    
    def margem_liquida(self) -> Optional[float]:
        """
        Calcula a Margem Líquida (em percentual).
        
        Fórmula: (Lucro Líquido / Receita Líquida) * 100
        
        Returns:
            Margem Líquida em % ou None se não puder calcular
        """
        lucro_liquido = self.data.get('Lucro Líquido', 0)
        receita_liquida = self.data.get('Receita Líquida', 0)
        result = self._safe_division(lucro_liquido, receita_liquida)
        return result * 100 if result is not None else None
    
    def roe(self) -> Optional[float]:
        """
        Calcula o ROE - Return on Equity (em percentual).
        
        Fórmula: (Lucro Líquido / Patrimônio Líquido) * 100
        
        Returns:
            ROE em % ou None se não puder calcular
        """
        lucro_liquido = self.data.get('Lucro Líquido', 0)
        patrimonio_liquido = self.data.get('Patrimônio Líquido', 0)
        result = self._safe_division(lucro_liquido, patrimonio_liquido)
        return result * 100 if result is not None else None
    
    def fco_divida_total(self) -> Optional[float]:
        """
        Calcula a relação Fluxo de Caixa Operacional / Dívida Total.
        
        Fórmula: FCO / Passivo Exigível Total
        
        Returns:
            FCO / Dívida Total ou None se não puder calcular
        """
        fco = self.data.get('Fluxo de Caixa Operacional', 0)
        passivo_exigivel = self.data.get('Passivo Exigível Total', 0)
        return self._safe_division(fco, passivo_exigivel)
    
    def calculate_all(self) -> Dict[str, Optional[float]]:
        """
        Calcula todos os indicadores financeiros.
        
        Returns:
            Dicionário com todos os indicadores calculados
        """
        return {
            'Liquidez Corrente': self.liquidez_corrente(),
            'Liquidez Seca': self.liquidez_seca(),
            'Endividamento Geral (%)': self.endividamento_geral(),
            'Dívida Líquida/EBITDA': self.divida_liquida_ebitda(),
            'Margem EBITDA (%)': self.margem_ebitda(),
            'Margem Líquida (%)': self.margem_liquida(),
            'ROE (%)': self.roe(),
            'FCO/Dívida Total': self.fco_divida_total()
        }


def calculate_metrics_for_all_years(df, years: list) -> Dict[str, Dict[str, Optional[float]]]:
    """
    Calcula os indicadores para todos os anos disponíveis.
    
    Args:
        df: DataFrame com dados financeiros
        years: Lista de anos para calcular
        
    Returns:
        Dicionário onde chave é o ano e valor é dicionário com os indicadores
    """
    from src.data_parser import get_all_data_for_year
    
    results = {}
    for year in years:
        financial_data = get_all_data_for_year(df, year)
        metrics = FinancialMetrics(financial_data)
        results[year] = metrics.calculate_all()
    
    return results
