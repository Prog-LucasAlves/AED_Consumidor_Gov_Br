"""
Dashboard Dados De Reclamações Consumidor Gov.br
"""

# Bibliotecas utilizadas
import streamlit as st
from PIL import Image

# Diretório dos Dados
# Caminho do arquivo parquet com os dados
PATH_PARQUET = "./data/Data_for_clear/dfGov.gzip"


def PypiConfigPage():
    """
    Função para configurar a página.
    """
    img = Image.open("./image/download.png")

    st.set_page_config(
        page_title="Em Construção",
        page_icon=img,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://www.extremelycoolapp.com/help",
            "Report a bug": "https://www.extremelycoolapp.com/bug",
            "About": "# This is a header. This is an *extremely* cool app!",
        },
    )


def PypiTitle():
    """
    Função para exibir o título do dashboard.
    """

    TITLE = """
<p style="
    color: Black;
    font-size: 30px;
    font-weight: bolder;"
> 🔍 Dashboard dos Dados das Reclamções Consumidor Gov.br </p>
"""
    st.markdown(TITLE, unsafe_allow_html=True)
