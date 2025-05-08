"""
Dashboard Dados De Reclamações Consumidor Gov.br
"""

# Bibliotecas utilizadas
import streamlit as st
import duckdb
import plotly.express as px

# Diretório dos Dados
PATH_PARQUET = "./Data/Data_for_clear/GOLDEN_dfGov.parquet"

st.set_page_config(
    page_title="Dashboard Reclamações",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# Dashboard de Reclamações - Gov.br",
    },
)

st.title("Dashboard Dados De Reclamações Consumidor Gov.br")


# ==== FUNÇÕES ====
def PypiAttData():
    DATA = duckdb.query(
        f"""SELECT Mes_Finalizacao, Mes_Nome_Finalizacao, Ano
        FROM '{PATH_PARQUET}'
        GROUP BY Mes_Finalizacao, Mes_Nome_Finalizacao, Ano
        ORDER BY Ano DESC , Mes_Finalizacao DESC"""
    ).to_df()

    DATAATTMES = DATA.iloc[0, 1]
    DATAATTANO = DATA.iloc[0, 2]

    ATT = f"""
    <p style="color:DimGrey; font-size: 14px; font-weight: bolder;">
    Atualização: {DATAATTMES} | {DATAATTANO}</p>
    """
    st.markdown(ATT, unsafe_allow_html=True)
    st.divider()

    return DATAATTMES, DATAATTANO


def PypiEstGeral():
    TOTALRECLAMACOESGERAL = duckdb.query(
        f"""SELECT COUNT(*) AS TOTAL
        FROM '{PATH_PARQUET}'"""
    ).to_df()

    TOTALRECLAMACOESGERALFORMAT = f"{TOTALRECLAMACOESGERAL.iloc[0, 0]:,}".replace(
        ",", "."
    )

    st.markdown(
        f"""<p style="color:Black; font-size: 16px; font-weight: bolder;">
        Total de Reclamações: {TOTALRECLAMACOESGERALFORMAT}</p>""",
        unsafe_allow_html=True,
    )


def PypiEstEmGeral():
    st.subheader("Estatísticas Gerais")

    SELECTNOMEFANTASIAGERAL = duckdb.query(
        f"""SELECT DISTINCT(Nome_Fantasia)
        FROM '{PATH_PARQUET}'
        ORDER BY Nome_Fantasia ASC"""
    ).to_df()

    NOMEFANTASIAGERAL = st.selectbox(
        "Selecione a Empresa",
        SELECTNOMEFANTASIAGERAL["Nome_Fantasia"].tolist(),
        key="geral_empresa",
    )

    TOTALRECLAMACOESGERAL = duckdb.query(
        f"""SELECT COUNT(*) AS TOTAL
        FROM '{PATH_PARQUET}'
        WHERE Nome_Fantasia = '{NOMEFANTASIAGERAL}'"""
    ).to_df()

    st.markdown(
        f"""<p style="color:Black; font-size: 16px; font-weight: bolder;">
        Total de Reclamações: {TOTALRECLAMACOESGERAL.iloc[0, 0]}</p>""",
        unsafe_allow_html=True,
    )

    return NOMEFANTASIAGERAL


def PypiEstEmAnual():
    st.subheader("Estatísticas Anuais")
    col1, col2 = st.columns((2, 2))

    SELECTANO = duckdb.query(
        f"""SELECT DISTINCT(Ano)
        FROM '{PATH_PARQUET}'
        ORDER BY Ano ASC"""
    ).to_df()
    ANO = col1.selectbox("Selecione o Ano", SELECTANO["Ano"].tolist(), key="anual_ano")

    SELECTNOMEFANTASIAANUAL = duckdb.query(
        f"""SELECT DISTINCT(Nome_Fantasia)
        FROM '{PATH_PARQUET}'
        ORDER BY Nome_Fantasia ASC"""
    ).to_df()
    NOMEFANTASIAANUAL = col2.selectbox(
        "Selecione a Empresa",
        SELECTNOMEFANTASIAANUAL["Nome_Fantasia"].tolist(),
        key="anual_empresa",
    )

    TOTALRECLAMACOES = duckdb.query(
        f"""SELECT COUNT(*) AS TOTAL
        FROM '{PATH_PARQUET}'
        WHERE Ano = {ANO}
        AND Nome_Fantasia = '{NOMEFANTASIAANUAL}'"""
    ).to_df()

    st.markdown(
        f"""<p style="color:Black; font-size: 16px; font-weight: bolder;">
        Total de Reclamações: {TOTALRECLAMACOES.iloc[0, 0]}</p>""",
        unsafe_allow_html=True,
    )

    return ANO, NOMEFANTASIAANUAL


def PypGraficsGeral():
    st.subheader("Gráficos")
    col1, col2, col3 = st.columns((2, 2, 2))

    DATA = duckdb.query(
        f"""SELECT Respondida AS R, COUNT(*) AS TOTAL,
        CASE Respondida
            WHEN 'Sim' THEN 'Reclamação Respondida'
            WHEN 'Não' THEN 'Reclamação Não Respondida'
        END AS Status
        FROM '{PATH_PARQUET}'"""
    ).to_df()
    fig = px.bar(
        DATA,
        x="TOTAL",
        y="Status",
        text_auto=True,
        title="Qtd. Reclamações por Mês",
        height=400,
    )
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    col1.plotly_chart(fig, use_container_width=True, key="respondida")


def PypGraficsEmAnual(ano, nomefantasia):
    st.subheader("Gráficos")
    col1, col2, col3 = st.columns((2, 2, 2))

    DATA = duckdb.query(
        f"""SELECT Mes_Finalizacao AS M, Mes_Nome_Finalizacao AS Mês, COUNT(*) AS TOTAL
        FROM '{PATH_PARQUET}'
        WHERE Ano = {ano}
        AND Nome_Fantasia = '{nomefantasia}'
        GROUP BY Mes_Finalizacao, Mes_Nome_Finalizacao
        ORDER BY Mes_Finalizacao DESC"""
    ).to_df()
    fig = px.bar(
        DATA,
        x="TOTAL",
        y="Mês",
        text_auto=True,
        title="Qtd. Reclamações por Mês",
        height=400,
    )
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    col1.plotly_chart(fig, use_container_width=True, key="mes_em_anual")

    DATA1 = duckdb.query(
        f"""SELECT Regiao AS R, COUNT(*) AS TOTAL,
        CASE Regiao
            WHEN 'S ' THEN 'Região Sul'
            WHEN 'N ' THEN 'Região Norte'
            WHEN 'NE' THEN 'Região Nordeste'
            WHEN 'SE' THEN 'Região Sudeste'
            WHEN 'CO' THEN 'Região Centro-Oeste'
        END AS Região
        FROM '{PATH_PARQUET}'
        WHERE Ano = {ano}
        AND Nome_Fantasia = '{nomefantasia}'
        GROUP BY Regiao"""
    ).to_df()
    fig2 = px.pie(
        DATA1, values="TOTAL", names="Região", title="Qtd. Reclamações por Região"
    )
    col2.plotly_chart(fig2, use_container_width=True)

    DATA2 = duckdb.query(
        f"""SELECT UF, COUNT(*) AS TOTAL
        FROM '{PATH_PARQUET}'
        WHERE Ano = {ano}
        AND Nome_Fantasia = '{nomefantasia}'
        GROUP BY UF
        ORDER BY TOTAL ASC"""
    ).to_df()
    fig3 = px.bar(
        DATA2, x="TOTAL", y="UF", text_auto=True, title="Qtd. Reclamações por Estado"
    )
    fig3.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    col3.plotly_chart(fig3, use_container_width=True)

    DATA3 = duckdb.query(
        f"""SELECT Assunto, COUNT(*) AS TOTAL
        FROM '{PATH_PARQUET}'
        WHERE Ano = {ano}
        AND Nome_Fantasia = '{nomefantasia}'
        GROUP BY Assunto
        ORDER BY TOTAL DESC"""
    ).to_df()
    fig4 = px.bar(
        DATA3,
        x="TOTAL",
        y="Assunto",
        text_auto=True,
        title="Qtd. Reclamações por Assunto",
    )
    fig4.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    col1.plotly_chart(fig4, use_container_width=True)


def PypGraficsEmGeral(nomefantasia):
    st.subheader("Gráficos")
    col1, col2, col3 = st.columns((2, 2, 2))

    DATA = duckdb.query(
        f"""SELECT Mes_Finalizacao AS M, Mes_Nome_Finalizacao AS Mês, COUNT(*) AS TOTAL
        FROM '{PATH_PARQUET}'
        WHERE Nome_Fantasia = '{nomefantasia}'
        GROUP BY Mes_Finalizacao, Mes_Nome_Finalizacao
        ORDER BY Mes_Finalizacao DESC"""
    ).to_df()
    fig = px.bar(
        DATA,
        x="TOTAL",
        y="Mês",
        text_auto=True,
        title="Qtd. Reclamações por Mês",
        height=400,
    )
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    col1.plotly_chart(fig, use_container_width=True, key="mes_em_geral")


def main():
    aba1, aba2 = st.tabs(["📄 Dados Gerais", "📊 Dados por Empresa"])

    with aba1:
        st.header("Dados Gerais")
        PypiAttData()
        PypiEstGeral()
        PypGraficsGeral()

    with aba2:
        st.header("Dados por Empresa")
        PypiAttData()
        subaba1, subaba2 = st.tabs(["📊 Anuais", "📈 Gerais"])

        with subaba1:
            ano, nomefantasia = PypiEstEmAnual()
            PypGraficsEmAnual(ano, nomefantasia)

        with subaba2:
            nomefantasia = PypiEstEmGeral()


if __name__ == "__main__":
    main()
