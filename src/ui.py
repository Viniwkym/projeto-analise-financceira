"""
Módulo de interface gráfica com Streamlit e visualizações com Plotly.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import pandas as pd

from src.diagnostics import FinancialProblem, SeverityLevel


def configure_page():
    """Configura a página do Streamlit."""
    st.set_page_config(
        page_title="Análise de Saúde Financeira",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def render_header():
    """Renderiza o cabeçalho da aplicação."""
    st.title("📊 Análise de Saúde Financeira Empresarial")
    st.markdown("""
    Esta ferramenta analisa automaticamente o Balanço Patrimonial e DRE da sua empresa,
    calculando indicadores financeiros fundamentais e gerando diagnóstico com recomendações práticas.
    """)


def render_file_upload() -> Optional[bytes]:
    """
    Renderiza componente de upload de arquivo.
    
    Returns:
        Conteúdo do arquivo ou None
    """
    st.subheader("1. Upload dos Dados Financeiros")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Faça upload do arquivo CSV com Balanço Patrimonial e DRE",
            type=['csv'],
            help="O arquivo deve conter dados históricos de 3 a 5 anos"
        )
    
    with col2:
        st.markdown("### 📥 Modelo de Exemplo")
        with open('sample_data/modelo_balanco_dre.csv', 'rb') as f:
            st.download_button(
                label="Baixar Modelo CSV",
                data=f,
                file_name="modelo_balanco_dre.csv",
                mime="text/csv"
            )
    
    if uploaded_file is not None:
        return uploaded_file.getvalue()
    
    return None


def render_context_form() -> Dict[str, Optional[str]]:
    """
    Renderiza formulário com dados contextuais opcionais.
    
    Returns:
        Dicionário com dados do contexto
    """
    with st.expander("2. Informações Adicionais da Empresa (Opcional)"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            setor = st.selectbox(
                "Setor de Atuação",
                options=[
                    "Não informado",
                    "Indústria",
                    "Comércio",
                    "Serviços",
                    "Tecnologia",
                    "Agronegócio",
                    "Construção Civil",
                    "Saúde",
                    "Educação",
                    "Alimentação",
                    "Outro"
                ]
            )
        
        with col2:
            faturamento = st.number_input(
                "Faturamento Anual (R$)",
                min_value=0.0,
                value=0.0,
                step=100000.0,
                format="%.2f"
            )
        
        with col3:
            funcionarios = st.number_input(
                "Número de Funcionários",
                min_value=0,
                value=0,
                step=1
            )
    
    return {
        'setor': setor if setor != "Não informado" else None,
        'faturamento': faturamento if faturamento > 0 else None,
        'funcionarios': funcionarios if funcionarios > 0 else None
    }


def render_kpi_cards(latest_metrics: Dict[str, Optional[float]], latest_year: str):
    """
    Renderiza cartões KPI com os indicadores do último ano.
    
    Args:
        latest_metrics: Indicadores do último ano
        latest_year: Ano mais recente
    """
    st.subheader(f"📈 Indicadores Financeiros - {latest_year}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_display = [
        ('Liquidez Corrente', latest_metrics.get('Liquidez Corrente'), ''),
        ('Liquidez Seca', latest_metrics.get('Liquidez Seca'), ''),
        ('Endividamento', latest_metrics.get('Endividamento Geral (%)'), '%'),
        ('Dív. Líq./EBITDA', latest_metrics.get('Dívida Líquida/EBITDA'), 'x'),
        ('Margem EBITDA', latest_metrics.get('Margem EBITDA (%)'), '%'),
        ('Margem Líquida', latest_metrics.get('Margem Líquida (%)'), '%'),
        ('ROE', latest_metrics.get('ROE (%)'), '%'),
        ('FCO/Dívida', latest_metrics.get('FCO/Dívida Total'), '')
    ]
    
    cols = [col1, col2, col3, col4, col1, col2, col3, col4]
    
    for idx, (label, value, suffix) in enumerate(metrics_display):
        with cols[idx]:
            if value is not None:
                formatted_value = f"{value:.2f}{suffix}"
                st.metric(label=label, value=formatted_value)
            else:
                st.metric(label=label, value="N/A")


def create_metric_chart(all_metrics: Dict[str, Dict[str, Optional[float]]], 
                       metric_name: str, 
                       years: List[str]) -> go.Figure:
    """
    Cria gráfico de evolução temporal de um indicador.
    
    Args:
        all_metrics: Todos os indicadores de todos os anos
        metric_name: Nome do indicador a plotar
        years: Lista de anos
        
    Returns:
        Figura do Plotly
    """
    values = [all_metrics[year].get(metric_name) for year in years]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=values,
        mode='lines+markers',
        name=metric_name,
        line=dict(width=3),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title=metric_name,
        xaxis_title="Ano",
        yaxis_title="Valor",
        hovermode='x unified',
        height=300
    )
    
    return fig


def render_evolution_charts(all_metrics: Dict[str, Dict[str, Optional[float]]], 
                           years: List[str]):
    """
    Renderiza gráficos de evolução temporal dos indicadores.
    
    Args:
        all_metrics: Todos os indicadores de todos os anos
        years: Lista de anos
    """
    st.subheader("📊 Evolução Histórica dos Indicadores")
    
    metric_names = list(all_metrics[years[0]].keys())
    
    col1, col2 = st.columns(2)
    
    for idx, metric_name in enumerate(metric_names):
        with col1 if idx % 2 == 0 else col2:
            fig = create_metric_chart(all_metrics, metric_name, years)
            st.plotly_chart(fig, use_container_width=True)


def render_diagnostic_section(problems: List[FinancialProblem]):
    """
    Renderiza seção de diagnóstico e recomendações.
    
    Args:
        problems: Lista de problemas identificados
    """
    st.subheader("🔍 Diagnóstico e Plano de Ação")
    
    if not problems:
        st.success("✅ Parabéns! Todos os indicadores estão dentro dos parâmetros recomendados.")
        return
    
    criticos = [p for p in problems if p.severity == SeverityLevel.CRITICO]
    alertas = [p for p in problems if p.severity == SeverityLevel.ALERTA]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Problemas Críticos", len(criticos))
    with col2:
        st.metric("Alertas", len(alertas))
    with col3:
        st.metric("Total de Pontos de Atenção", len(problems))
    
    if criticos:
        st.markdown("### 🚨 Problemas Críticos")
        for problem in criticos:
            with st.container():
                st.error(f"**{problem.indicator}**")
                st.write(problem.message)
                st.markdown("**Soluções Recomendadas:**")
                for idx, solution in enumerate(problem.solutions, 1):
                    st.markdown(f"{idx}. {solution}")
                st.markdown("---")
    
    if alertas:
        st.markdown("### ⚠️ Alertas")
        for problem in alertas:
            with st.container():
                st.warning(f"**{problem.indicator}**")
                st.write(problem.message)
                st.markdown("**Soluções Recomendadas:**")
                for idx, solution in enumerate(problem.solutions, 1):
                    st.markdown(f"{idx}. {solution}")
                st.markdown("---")


def render_context_info(context: Dict[str, Optional[str]]):
    """
    Renderiza informações de contexto da empresa se fornecidas.
    
    Args:
        context: Dados contextuais da empresa
    """
    if any(context.values()):
        with st.expander("ℹ️ Informações da Empresa"):
            if context['setor']:
                st.write(f"**Setor:** {context['setor']}")
            if context['faturamento']:
                st.write(f"**Faturamento Anual:** R$ {context['faturamento']:,.2f}")
            if context['funcionarios']:
                st.write(f"**Número de Funcionários:** {context['funcionarios']}")


def show_error(message: str):
    """
    Exibe mensagem de erro.
    
    Args:
        message: Mensagem de erro
    """
    st.error(f"❌ {message}")


def show_success(message: str):
    """
    Exibe mensagem de sucesso.
    
    Args:
        message: Mensagem de sucesso
    """
    st.success(f"✅ {message}")
