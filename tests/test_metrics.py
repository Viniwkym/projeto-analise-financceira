"""
Testes unitários para o módulo de cálculo de métricas financeiras.
"""

import pytest
from src.metrics import FinancialMetrics


class TestFinancialMetrics:
    """Testes para a classe FinancialMetrics."""
    
    @pytest.fixture
    def sample_data(self):
        """Fixture com dados financeiros de exemplo."""
        return {
            'Receita Líquida': 1000000,
            'EBITDA': 200000,
            'Lucro Líquido': 80000,
            'Ativo Circulante': 500000,
            'Ativo Total': 1500000,
            'Estoque': 150000,
            'Passivo Circulante': 400000,
            'Passivo Exigível Total': 800000,
            'Dívida Bruta': 600000,
            'Caixa e Equivalentes': 100000,
            'Patrimônio Líquido': 700000,
            'Fluxo de Caixa Operacional': 180000
        }
    
    def test_liquidez_corrente(self, sample_data):
        """Testa cálculo da Liquidez Corrente."""
        metrics = FinancialMetrics(sample_data)
        result = metrics.liquidez_corrente()
        expected = 500000 / 400000
        assert result == pytest.approx(expected, rel=1e-6)
    
    def test_liquidez_corrente_zero_denominator(self):
        """Testa Liquidez Corrente com denominador zero."""
        data = {'Ativo Circulante': 500000, 'Passivo Circulante': 0}
        metrics = FinancialMetrics(data)
        result = metrics.liquidez_corrente()
        assert result is None
    
    def test_liquidez_seca(self, sample_data):
        """Testa cálculo da Liquidez Seca."""
        metrics = FinancialMetrics(sample_data)
        result = metrics.liquidez_seca()
        expected = (500000 - 150000) / 400000
        assert result == pytest.approx(expected, rel=1e-6)
    
    def test_liquidez_seca_zero_denominator(self):
        """Testa Liquidez Seca com denominador zero."""
        data = {
            'Ativo Circulante': 500000,
            'Estoque': 150000,
            'Passivo Circulante': 0
        }
        metrics = FinancialMetrics(data)
        result = metrics.liquidez_seca()
        assert result is None
    
    def test_endividamento_geral(self, sample_data):
        """Testa cálculo do Endividamento Geral."""
        metrics = FinancialMetrics(sample_data)
        result = metrics.endividamento_geral()
        expected = (800000 / 1500000) * 100
        assert result == pytest.approx(expected, rel=1e-6)
    
    def test_endividamento_geral_zero_denominator(self):
        """Testa Endividamento Geral com denominador zero."""
        data = {'Passivo Exigível Total': 800000, 'Ativo Total': 0}
        metrics = FinancialMetrics(data)
        result = metrics.endividamento_geral()
        assert result is None
    
    def test_divida_liquida_ebitda(self, sample_data):
        """Testa cálculo da Dívida Líquida / EBITDA."""
        metrics = FinancialMetrics(sample_data)
        result = metrics.divida_liquida_ebitda()
        expected = (600000 - 100000) / 200000
        assert result == pytest.approx(expected, rel=1e-6)
    
    def test_divida_liquida_ebitda_zero_ebitda(self):
        """Testa Dívida Líquida / EBITDA com EBITDA zero."""
        data = {
            'Dívida Bruta': 600000,
            'Caixa e Equivalentes': 100000,
            'EBITDA': 0
        }
        metrics = FinancialMetrics(data)
        result = metrics.divida_liquida_ebitda()
        assert result is None
    
    def test_margem_ebitda(self, sample_data):
        """Testa cálculo da Margem EBITDA."""
        metrics = FinancialMetrics(sample_data)
        result = metrics.margem_ebitda()
        expected = (200000 / 1000000) * 100
        assert result == pytest.approx(expected, rel=1e-6)
    
    def test_margem_ebitda_zero_receita(self):
        """Testa Margem EBITDA com receita zero."""
        data = {'EBITDA': 200000, 'Receita Líquida': 0}
        metrics = FinancialMetrics(data)
        result = metrics.margem_ebitda()
        assert result is None
    
    def test_margem_liquida(self, sample_data):
        """Testa cálculo da Margem Líquida."""
        metrics = FinancialMetrics(sample_data)
        result = metrics.margem_liquida()
        expected = (80000 / 1000000) * 100
        assert result == pytest.approx(expected, rel=1e-6)
    
    def test_margem_liquida_negativa(self):
        """Testa Margem Líquida com lucro negativo."""
        data = {'Lucro Líquido': -50000, 'Receita Líquida': 1000000}
        metrics = FinancialMetrics(data)
        result = metrics.margem_liquida()
        expected = (-50000 / 1000000) * 100
        assert result == pytest.approx(expected, rel=1e-6)
    
    def test_roe(self, sample_data):
        """Testa cálculo do ROE."""
        metrics = FinancialMetrics(sample_data)
        result = metrics.roe()
        expected = (80000 / 700000) * 100
        assert result == pytest.approx(expected, rel=1e-6)
    
    def test_roe_zero_patrimonio(self):
        """Testa ROE com patrimônio líquido zero."""
        data = {'Lucro Líquido': 80000, 'Patrimônio Líquido': 0}
        metrics = FinancialMetrics(data)
        result = metrics.roe()
        assert result is None
    
    def test_fco_divida_total(self, sample_data):
        """Testa cálculo do FCO / Dívida Total."""
        metrics = FinancialMetrics(sample_data)
        result = metrics.fco_divida_total()
        expected = 180000 / 800000
        assert result == pytest.approx(expected, rel=1e-6)
    
    def test_fco_divida_total_zero_divida(self):
        """Testa FCO / Dívida Total com dívida zero."""
        data = {
            'Fluxo de Caixa Operacional': 180000,
            'Passivo Exigível Total': 0
        }
        metrics = FinancialMetrics(data)
        result = metrics.fco_divida_total()
        assert result is None
    
    def test_calculate_all(self, sample_data):
        """Testa cálculo de todos os indicadores."""
        metrics = FinancialMetrics(sample_data)
        result = metrics.calculate_all()
        
        assert 'Liquidez Corrente' in result
        assert 'Liquidez Seca' in result
        assert 'Endividamento Geral (%)' in result
        assert 'Dívida Líquida/EBITDA' in result
        assert 'Margem EBITDA (%)' in result
        assert 'Margem Líquida (%)' in result
        assert 'ROE (%)' in result
        assert 'FCO/Dívida Total' in result
        
        assert result['Liquidez Corrente'] is not None
        assert result['Liquidez Seca'] is not None
        assert result['Endividamento Geral (%)'] is not None
    
    def test_missing_data_fields(self):
        """Testa comportamento com dados ausentes."""
        data = {'Receita Líquida': 1000000}
        metrics = FinancialMetrics(data)
        
        assert metrics.liquidez_corrente() is None
        result = metrics.margem_ebitda()
        assert result == 0.0 or result is None
