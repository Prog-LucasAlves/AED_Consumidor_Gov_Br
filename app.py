"""
Dashboard Dados De Reclamações Consumidor Gov.br
"""

# Bibliotecas utilizadas
import streamlit as st
from PIL import Image
import duckdb
import plotly.express as px

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


def PypGrafics(ano, nomefantasia):
    """
    Função para exibir os gráficos.
    """

    st.subheader("Gráficos")

    col1, col2, col3 = st.columns((2, 2, 2))

    DATA = duckdb.query(
        f"""SELECT Mes_Finalizacao AS M, Mes_Nome_Finalizacao AS Mês, COUNT(*) AS TOTAL
        FROM '{PATH_PARQUET}'
        WHERE Ano = {ano}
        AND Nome_Fantasia = '{nomefantasia}'
        GROUP BY Mes_Finalizacao, Mes_Nome_Finalizacao
        ORDER BY Mes_Finalizacao DESC
        """
    ).to_df()

    fig = px.bar(
        DATA,
        x="TOTAL",
        y="Mês",
        text_auto=True,
        title="Qtd. Reclamações por Mês",
        height=400,
        width=400,
    )
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    col1.plotly_chart(fig, use_container_width=True)

    # -----

    DATA1 = duckdb.query(
        f"""SELECT Regiao AS R, COUNT(*) AS TOTAL,
        CASE Regiao
            WHEN 'S ' THEN 'Região Sul'
            WHEN 'N ' THEN 'Região Norte'
            WHEN 'NE' THEN 'Região Nordeste'
            WHEN 'SE' THEN 'Região Sudeste'
            WHEN 'CO' THEN 'Região Centro-Oeste'
        END AS 'Região'
        FROM '{PATH_PARQUET}'
        WHERE Ano = {ano}
        AND Nome_Fantasia = '{nomefantasia}'
        GROUP BY Regiao
        """
    ).to_df()

    fig2 = px.pie(
        DATA1, values="TOTAL", names="Região", title="Qtd. Reclamações por Região"
    )
    col2.plotly_chart(fig2, use_container_width=True)

    # -----

    DATA2 = duckdb.query(
        f"""SELECT UF, COUNT(*) AS TOTAL
        FROM '{PATH_PARQUET}'
        WHERE Ano = {ano}
        AND Nome_Fantasia = '{nomefantasia}'
        GROUP BY UF
        ORDER BY TOTAL ASC
        """
    ).to_df()

    fig3 = px.bar(
        DATA2, x="TOTAL", y="UF", text_auto=True, title="Qtd. Reclamações por Estado"
    )
    fig3.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    col3.plotly_chart(fig3, use_container_width=True)

    st.divider()


if __name__ == "__main__":
    PypiConfigPage()
    PypiTitle()
    PypiAttData()
    ano, nomefantasia = PypiEsttAnual()
    PypGrafics(ano, nomefantasia)
