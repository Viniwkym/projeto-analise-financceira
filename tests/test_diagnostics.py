"""
Testes unitários para o módulo de diagnóstico financeiro.
"""

import pytest
from src.diagnostics import FinancialDiagnostics, SeverityLevel, FinancialProblem


class TestFinancialDiagnostics:
    """Testes para a classe FinancialDiagnostics."""
    
    @pytest.fixture
    def healthy_metrics(self):
        """Fixture com métricas saudáveis."""
        return {
            'Liquidez Corrente': 2.0,
            'Liquidez Seca': 1.5,
            'Endividamento Geral (%)': 40.0,
            'Dívida Líquida/EBITDA': 2.0,
            'Margem EBITDA (%)': 20.0,
            'Margem Líquida (%)': 10.0,
            'ROE (%)': 15.0,
            'FCO/Dívida Total': 0.3
        }
    
    @pytest.fixture
    def critical_metrics(self):
        """Fixture com métricas críticas."""
        return {
            'Liquidez Corrente': 0.8,
            'Liquidez Seca': 0.5,
            'Endividamento Geral (%)': 75.0,
            'Dívida Líquida/EBITDA': 5.0,
            'Margem EBITDA (%)': 8.0,
            'Margem Líquida (%)': -2.0,
            'ROE (%)': -5.0,
            'FCO/Dívida Total': 0.05
        }
    
    @pytest.fixture
    def alert_metrics(self):
        """Fixture com métricas em alerta."""
        return {
            'Liquidez Corrente': 1.2,
            'Liquidez Seca': 0.9,
            'Endividamento Geral (%)': 60.0,
            'Dívida Líquida/EBITDA': 3.5,
            'Margem EBITDA (%)': 12.0,
            'Margem Líquida (%)': 3.0,
            'ROE (%)': 8.0,
            'FCO/Dívida Total': 0.15
        }
    
    def test_healthy_metrics_no_problems(self, healthy_metrics):
        """Testa que métricas saudáveis não geram problemas."""
        diagnostics = FinancialDiagnostics(healthy_metrics)
        problems = diagnostics.analyze()
        assert len(problems) == 0
    
    def test_critical_liquidez_corrente(self):
        """Testa detecção de Liquidez Corrente crítica."""
        metrics = {'Liquidez Corrente': 0.8}
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        assert len(problems) == 1
        assert problems[0].indicator == 'Liquidez Corrente'
        assert problems[0].severity == SeverityLevel.CRITICO
        assert len(problems[0].solutions) > 0
    
    def test_alert_liquidez_corrente(self):
        """Testa detecção de Liquidez Corrente em alerta."""
        metrics = {'Liquidez Corrente': 1.2}
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        assert len(problems) == 1
        assert problems[0].indicator == 'Liquidez Corrente'
        assert problems[0].severity == SeverityLevel.ALERTA
    
    def test_critical_endividamento(self):
        """Testa detecção de Endividamento Geral crítico."""
        metrics = {'Endividamento Geral (%)': 75.0}
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        assert len(problems) == 1
        assert problems[0].indicator == 'Endividamento Geral (%)'
        assert problems[0].severity == SeverityLevel.CRITICO
    
    def test_alert_endividamento(self):
        """Testa detecção de Endividamento Geral em alerta."""
        metrics = {'Endividamento Geral (%)': 60.0}
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        assert len(problems) == 1
        assert problems[0].severity == SeverityLevel.ALERTA
    
    def test_negative_margem_liquida(self):
        """Testa detecção de Margem Líquida negativa."""
        metrics = {'Margem Líquida (%)': -5.0}
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        assert len(problems) == 1
        assert problems[0].indicator == 'Margem Líquida (%)'
        assert problems[0].severity == SeverityLevel.CRITICO
    
    def test_critical_divida_ebitda(self):
        """Testa detecção de Dívida Líquida/EBITDA crítica."""
        metrics = {'Dívida Líquida/EBITDA': 5.0}
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        assert len(problems) == 1
        assert problems[0].indicator == 'Dívida Líquida/EBITDA'
        assert problems[0].severity == SeverityLevel.CRITICO
    
    def test_multiple_problems(self, critical_metrics):
        """Testa detecção de múltiplos problemas."""
        diagnostics = FinancialDiagnostics(critical_metrics)
        problems = diagnostics.analyze()
        
        assert len(problems) == 8
        critical_problems = [p for p in problems if p.severity == SeverityLevel.CRITICO]
        assert len(critical_problems) == 8
    
    def test_problems_sorted_by_severity(self, alert_metrics):
        """Testa que problemas críticos vêm antes de alertas."""
        alert_metrics['Liquidez Corrente'] = 0.8
        alert_metrics['Margem EBITDA (%)'] = 12.0
        
        diagnostics = FinancialDiagnostics(alert_metrics)
        problems = diagnostics.analyze()
        
        critical_indices = [i for i, p in enumerate(problems) if p.severity == SeverityLevel.CRITICO]
        alert_indices = [i for i, p in enumerate(problems) if p.severity == SeverityLevel.ALERTA]
        
        if critical_indices and alert_indices:
            assert max(critical_indices) < min(alert_indices)
    
    def test_get_summary(self, critical_metrics):
        """Testa geração de resumo da análise."""
        diagnostics = FinancialDiagnostics(critical_metrics)
        diagnostics.analyze()
        summary = diagnostics.get_summary()
        
        assert 'criticos' in summary
        assert 'alertas' in summary
        assert 'total' in summary
        assert summary['total'] == summary['criticos'] + summary['alertas']
    
    def test_none_values_ignored(self):
        """Testa que valores None são ignorados na análise."""
        metrics = {
            'Liquidez Corrente': None,
            'Endividamento Geral (%)': 40.0
        }
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        assert all(p.indicator != 'Liquidez Corrente' for p in problems)
    
    def test_problem_has_message(self):
        """Testa que problemas possuem mensagens descritivas."""
        metrics = {'Liquidez Corrente': 0.8}
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        assert len(problems[0].message) > 0
        assert 'Liquidez Corrente' in problems[0].message
    
    def test_problem_has_solutions(self):
        """Testa que problemas possuem soluções."""
        metrics = {'Liquidez Corrente': 0.8}
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        assert len(problems[0].solutions) > 0
        assert all(isinstance(sol, str) for sol in problems[0].solutions)
    
    def test_critical_roe(self):
        """Testa detecção de ROE crítico."""
        metrics = {'ROE (%)': -5.0}
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        assert len(problems) == 1
        assert problems[0].indicator == 'ROE (%)'
        assert problems[0].severity == SeverityLevel.CRITICO
    
    def test_alert_fco_divida(self):
        """Testa detecção de FCO/Dívida em alerta."""
        metrics = {'FCO/Dívida Total': 0.15}
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        assert len(problems) == 1
        assert problems[0].indicator == 'FCO/Dívida Total'
        assert problems[0].severity == SeverityLevel.ALERTA
    
    def test_boundary_values(self):
        """Testa valores exatamente nos limites."""
        metrics = {
            'Liquidez Corrente': 1.0,
            'Endividamento Geral (%)': 70.0
        }
        diagnostics = FinancialDiagnostics(metrics)
        problems = diagnostics.analyze()
        
        liquidez_problems = [p for p in problems if p.indicator == 'Liquidez Corrente']
        endiv_problems = [p for p in problems if p.indicator == 'Endividamento Geral (%)']
        
        assert len(liquidez_problems) > 0
        assert len(endiv_problems) > 0
