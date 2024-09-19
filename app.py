"""
Dashboard Dados De Reclamações Consumidor Gov.br
"""

# Bibliotecas utilizadas
import streamlit as st
from PIL import Image
import duckdb

# Diretório dos Dados
# Caminho do arquivo parquet com os dados
PATH_PARQUET = "./Data/Data_for_clear/GOLD_data_transformed.parquet"


def PypiConfigPage():
    """
    Função para configurar a página.
    """

    img = Image.open("./Image/page.png")

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


def PypiAttData():
    """
    Função para exibir os dados de Atualização.
    """

    DATA = duckdb.query(
        f"""SELECT Mes_Finalizacao, Mes_Nome_Finalizacao, Ano
        FROM '{PATH_PARQUET}'
        GROUP BY Mes_Finalizacao, Mes_Nome_Finalizacao, Ano
        ORDER BY Ano DESC , Mes_Finalizacao DESC"""
    ).to_df()

    DATAATTMES = DATA.iloc[0, 1]
    DATAATTANO = DATA.iloc[0, 2]

    ATT = f"""
    <p style="color:DimGrey; font-size: 14px; font-weight: bolder;"
    > Atualização: {DATAATTMES} | {DATAATTANO} </p>
    """
    st.markdown(ATT, unsafe_allow_html=True)

    st.divider()

    return DATAATTMES, DATAATTANO


def PypiEsttAnual():
    """
    Função para exibir os dados Estatísticos Anuais.
    """

    st.subheader("Estatísticas Anuais")

    # Colunas do Selectbox
    col1, col2 = st.columns((1, 2))

    DATAANO = duckdb.query(
        f"""SELECT DISTINCT(Ano)
        FROM '{PATH_PARQUET}'
        ORDER BY Ano ASC
        """
    ).to_df()

    ANO = col1.selectbox("Selecione o Ano", DATAANO)

    DATANOMEFANTASIA = duckdb.query(
        f"""SELECT DISTINCT(Nome_Fantasia)
        FROM '{PATH_PARQUET}'
        ORDER BY Nome_Fantasia ASC
        """
    ).to_df()

    NOMEFANTASIA = col2.selectbox("Selecione a Empresa", DATANOMEFANTASIA)

    TOTALRECLAMACOES = duckdb.query(
        f"""SELECT COUNT(*) AS TOTAL
        FROM '{PATH_PARQUET}'
        WHERE Ano = {ANO}
        AND Nome_Fantasia = '{NOMEFANTASIA}'
        """
    ).to_df()

    TOTALRECLAMACOES = f"""
    <p style="color:Black; font-size: 16px; font-weight: bolder;"
    > Total de Reclamações: {TOTALRECLAMACOES.iloc[0, 0]} </p>
    """

    st.markdown(TOTALRECLAMACOES, unsafe_allow_html=True)

    return ANO, NOMEFANTASIA


if __name__ == "__main__":
    PypiConfigPage()
    PypiTitle()
    PypiAttData()
    PypiEsttAnual()
