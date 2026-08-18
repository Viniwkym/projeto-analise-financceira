"""
Módulo para diagnóstico de saúde financeira e geração de recomendações.
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum


class SeverityLevel(Enum):
    """Níveis de severidade dos problemas identificados."""
    CRITICO = "Crítico"
    ALERTA = "Alerta"
    BOM = "Bom"


class FinancialProblem:
    """Representa um problema financeiro identificado."""
    
    def __init__(self, indicator: str, severity: SeverityLevel, 
                 current_value: float, message: str, solutions: List[str]):
        """
        Inicializa um problema financeiro.
        
        Args:
            indicator: Nome do indicador
            severity: Nível de severidade
            current_value: Valor atual do indicador
            message: Descrição do problema
            solutions: Lista de soluções recomendadas
        """
        self.indicator = indicator
        self.severity = severity
        self.current_value = current_value
        self.message = message
        self.solutions = solutions


class FinancialDiagnostics:
    """Motor de diagnóstico financeiro baseado em regras."""
    
    BENCHMARKS = {
        'Liquidez Corrente': {
            'critico': 1.0,
            'alerta': 1.5,
            'direction': 'above'
        },
        'Liquidez Seca': {
            'critico': 0.8,
            'alerta': 1.0,
            'direction': 'above'
        },
        'Endividamento Geral (%)': {
            'critico': 70.0,
            'alerta': 50.0,
            'direction': 'below'
        },
        'Dívida Líquida/EBITDA': {
            'critico': 4.0,
            'alerta': 3.0,
            'direction': 'below'
        },
        'Margem EBITDA (%)': {
            'critico': 10.0,
            'alerta': 15.0,
            'direction': 'above'
        },
        'Margem Líquida (%)': {
            'critico': 0.0,
            'alerta': 5.0,
            'direction': 'above'
        },
        'ROE (%)': {
            'critico': 0.0,
            'alerta': 10.0,
            'direction': 'above'
        },
        'FCO/Dívida Total': {
            'critico': 0.1,
            'alerta': 0.2,
            'direction': 'above'
        }
    }
    
    SOLUTIONS = {
        'Liquidez Corrente': {
            SeverityLevel.CRITICO: [
                "Renegociar prazos com fornecedores para alongar o prazo de pagamento",
                "Buscar rolagem de dívidas de curto prazo para longo prazo",
                "Avaliar venda de ativos não essenciais para gerar caixa imediato",
                "Reduzir drasticamente despesas operacionais não críticas"
            ],
            SeverityLevel.ALERTA: [
                "Melhorar a gestão de recebíveis (cobrar clientes inadimplentes)",
                "Renegociar condições de pagamento com fornecedores",
                "Reduzir níveis de estoque para liberar capital de giro"
            ]
        },
        'Liquidez Seca': {
            SeverityLevel.CRITICO: [
                "Reduzir drasticamente os níveis de estoque",
                "Negociar prazo maior com fornecedores",
                "Buscar linhas de crédito de curto prazo emergenciais",
                "Acelerar conversão de recebíveis em caixa"
            ],
            SeverityLevel.ALERTA: [
                "Revisar política de estoques e implementar just-in-time",
                "Melhorar ciclo de conversão de caixa",
                "Negociar melhores condições de pagamento"
            ]
        },
        'Endividamento Geral (%)': {
            SeverityLevel.CRITICO: [
                "Suspender novos endividamentos imediatamente",
                "Buscar aporte de capital próprio (sócios/investidores)",
                "Vender ativos não essenciais para reduzir dívidas",
                "Renegociar dívidas com credores (alongamento, carência)"
            ],
            SeverityLevel.ALERTA: [
                "Priorizar amortização de dívidas com recursos de caixa",
                "Evitar novos financiamentos no curto prazo",
                "Aumentar geração de caixa operacional"
            ]
        },
        'Dívida Líquida/EBITDA': {
            SeverityLevel.CRITICO: [
                "Priorizar amortização acelerada da dívida",
                "Reduzir custos operacionais para aumentar EBITDA",
                "Buscar reestruturação da dívida com credores",
                "Avaliar venda de ativos ou unidades de negócio"
            ],
            SeverityLevel.ALERTA: [
                "Acelerar geração de caixa operacional",
                "Aumentar EBITDA através de eficiência operacional",
                "Priorizar pagamento de dívidas sobre novos investimentos"
            ]
        },
        'Margem EBITDA (%)': {
            SeverityLevel.CRITICO: [
                "Revisar estrutura de custos fixos e variáveis urgentemente",
                "Implementar programa de redução de despesas operacionais",
                "Renegociar contratos com principais fornecedores",
                "Avaliar reajuste de preços de produtos/serviços"
            ],
            SeverityLevel.ALERTA: [
                "Aumentar eficiência operacional (produtividade)",
                "Reduzir despesas administrativas e comerciais",
                "Buscar ganhos de escala ou melhor mix de produtos"
            ]
        },
        'Margem Líquida (%)': {
            SeverityLevel.CRITICO: [
                "Identificar e eliminar produtos/serviços não lucrativos",
                "Reduzir custos fixos e despesas financeiras",
                "Renegociar dívidas para reduzir juros",
                "Implementar corte emergencial de despesas"
            ],
            SeverityLevel.ALERTA: [
                "Melhorar mix de produtos de maior margem",
                "Reduzir despesas financeiras e tributárias",
                "Aumentar preços ou reduzir descontos comerciais"
            ]
        },
        'ROE (%)': {
            SeverityLevel.CRITICO: [
                "Aumentar rentabilidade através de redução de custos",
                "Avaliar reestruturação do modelo de negócio",
                "Focar em produtos/serviços de maior margem",
                "Reduzir ativos improdutivos ou inativos"
            ],
            SeverityLevel.ALERTA: [
                "Melhorar eficiência na utilização de ativos",
                "Aumentar margem líquida através de redução de custos",
                "Otimizar estrutura de capital"
            ]
        },
        'FCO/Dívida Total': {
            SeverityLevel.CRITICO: [
                "Melhorar gestão de capital de giro urgentemente",
                "Acelerar recebimentos e postergar pagamentos",
                "Reduzir investimentos em estoque",
                "Buscar renegociação de dívidas para aliviar pressão de caixa"
            ],
            SeverityLevel.ALERTA: [
                "Melhorar ciclo de conversão de caixa",
                "Otimizar gestão de recebíveis e estoques",
                "Aumentar geração operacional de caixa"
            ]
        }
    }
    
    def __init__(self, metrics: Dict[str, Optional[float]]):
        """
        Inicializa o motor de diagnóstico.
        
        Args:
            metrics: Dicionário com os indicadores calculados
        """
        self.metrics = metrics
        self.problems: List[FinancialProblem] = []
    
    def _evaluate_metric(self, metric_name: str, value: Optional[float]) -> Optional[SeverityLevel]:
        """
        Avalia um indicador específico contra os benchmarks.
        
        Args:
            metric_name: Nome do indicador
            value: Valor do indicador
            
        Returns:
            Nível de severidade ou None se estiver bom
        """
        if value is None or metric_name not in self.BENCHMARKS:
            return None
        
        benchmark = self.BENCHMARKS[metric_name]
        direction = benchmark['direction']
        critico = benchmark['critico']
        alerta = benchmark['alerta']
        
        if direction == 'above':
            if value < critico:
                return SeverityLevel.CRITICO
            elif value < alerta:
                return SeverityLevel.ALERTA
        else:
            if value > critico:
                return SeverityLevel.CRITICO
            elif value > alerta:
                return SeverityLevel.ALERTA
        
        return None
    
    def _generate_message(self, metric_name: str, value: float, severity: SeverityLevel) -> str:
        """
        Gera mensagem descritiva sobre o problema.
        
        Args:
            metric_name: Nome do indicador
            value: Valor atual
            severity: Nível de severidade
            
        Returns:
            Mensagem descritiva
        """
        if '%' in metric_name:
            value_str = f"{value:.2f}%"
        else:
            value_str = f"{value:.2f}"
        
        benchmark = self.BENCHMARKS[metric_name]
        
        if severity == SeverityLevel.CRITICO:
            threshold = benchmark['critico']
        else:
            threshold = benchmark['alerta']
        
        direction = benchmark['direction']
        
        if '%' in metric_name:
            threshold_str = f"{threshold:.2f}%"
        else:
            threshold_str = f"{threshold:.2f}"
        
        if direction == 'above':
            comparison = f"abaixo do limite {'crítico' if severity == SeverityLevel.CRITICO else 'de alerta'} de {threshold_str}"
        else:
            comparison = f"acima do limite {'crítico' if severity == SeverityLevel.CRITICO else 'de alerta'} de {threshold_str}"
        
        return f"{metric_name} está em {value_str}, {comparison}."
    
    def analyze(self) -> List[FinancialProblem]:
        """
        Analisa todos os indicadores e identifica problemas.
        
        Returns:
            Lista de problemas financeiros identificados
        """
        self.problems = []
        
        for metric_name, value in self.metrics.items():
            if value is None:
                continue
            
            severity = self._evaluate_metric(metric_name, value)
            
            if severity and severity != SeverityLevel.BOM:
                message = self._generate_message(metric_name, value, severity)
                solutions = self.SOLUTIONS.get(metric_name, {}).get(severity, [])
                
                problem = FinancialProblem(
                    indicator=metric_name,
                    severity=severity,
                    current_value=value,
                    message=message,
                    solutions=solutions
                )
                
                self.problems.append(problem)
        
        self.problems.sort(key=lambda p: (
            0 if p.severity == SeverityLevel.CRITICO else 1,
            p.indicator
        ))
        
        return self.problems
    
    def get_summary(self) -> Dict[str, int]:
        """
        Retorna resumo da análise.
        
        Returns:
            Dicionário com contagem por severidade
        """
        return {
            'criticos': len([p for p in self.problems if p.severity == SeverityLevel.CRITICO]),
            'alertas': len([p for p in self.problems if p.severity == SeverityLevel.ALERTA]),
            'total': len(self.problems)
        }
