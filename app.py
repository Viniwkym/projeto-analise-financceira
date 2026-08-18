"""
Aplicação principal Streamlit para análise de saúde financeira empresarial.
"""

import streamlit as st
import tempfile
import os

from src.ui import (
    configure_page, render_header, render_file_upload, 
    render_context_form, render_kpi_cards, render_evolution_charts,
    render_diagnostic_section, render_context_info, show_error, show_success
)
from src.data_parser import parse_csv, get_years, DataParserError
from src.metrics import calculate_metrics_for_all_years
from src.diagnostics import FinancialDiagnostics


def main():
    """Função principal da aplicação."""
    configure_page()
    render_header()
    
    file_content = render_file_upload()
    context = render_context_form()
    
    if file_content is None:
        st.info("👆 Faça o upload do arquivo CSV para começar a análise.")
        st.markdown("### Como usar:")
        st.markdown("""
        1. Baixe o modelo de exemplo CSV
        2. Preencha com os dados financeiros da sua empresa (3 a 5 anos)
        3. Faça o upload do arquivo preenchido
        4. Opcionalmente, preencha as informações adicionais
        5. Clique em 'Analisar Dados Financeiros'
        """)
        return
    
    if st.button("🚀 Analisar Dados Financeiros", type="primary"):
        with st.spinner("Processando dados financeiros..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='wb') as tmp_file:
                    tmp_file.write(file_content)
                    tmp_path = tmp_file.name
                
                try:
                    df = parse_csv(tmp_path)
                    show_success("Arquivo CSV carregado com sucesso!")
                    
                    years = get_years(df)
                    st.info(f"📅 Períodos analisados: {', '.join(years)}")
                    
                    all_metrics = calculate_metrics_for_all_years(df, years)
                    
                    latest_year = years[-1]
                    latest_metrics = all_metrics[latest_year]
                    
                    st.markdown("---")
                    render_kpi_cards(latest_metrics, latest_year)
                    
                    st.markdown("---")
                    render_evolution_charts(all_metrics, years)
                    
                    st.markdown("---")
                    diagnostics = FinancialDiagnostics(latest_metrics)
                    problems = diagnostics.analyze()
                    render_diagnostic_section(problems)
                    
                    st.markdown("---")
                    render_context_info(context)
                    
                except DataParserError as e:
                    show_error(str(e))
                except Exception as e:
                    show_error(f"Erro ao processar os dados: {str(e)}")
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                    
            except Exception as e:
                show_error(f"Erro ao processar o arquivo: {str(e)}")


if __name__ == "__main__":
    main()
