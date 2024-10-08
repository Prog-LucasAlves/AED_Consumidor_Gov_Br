# Importando as bibliotecas necessárias
import pandas as pd
import sqlite3


def loaddata():
    """
    Função para carregar os dados salvos.
    """
    # Local onde estão os dados
    path = "../../Data/Data_for_clear/"

    # Lendo os dados salvos
    data = pd.read_parquet(f"{path}SILVER_data.parquet")
    return data


def transformdata():
    """
    Função para transformar os dados.
    """
    # Carregando os dados
    data = loaddata()

    # Ajustando o índice do DataFrame
    data.reset_index(inplace=True, drop=True)

    # Imputando na coluna 'Nota do Consumidor' valores utilizando o método (forward fill)
    data["Nota do Consumidor"] = data["Nota do Consumidor"].ffill()

    # Imputando na coluna 'Tempo Resposta' o valor 0(Zero) nos valores NaN
    data["Tempo Resposta"] = data["Tempo Resposta"].fillna(0)

    # Imputando na coluna 'Sexo' o Valor O(Outros) nos Valores NaN
    data["Sexo"] = data["Sexo"].fillna("O")

    # Eliminando valores ausentes na coluna 'Avaliação Reclamação'
    data.dropna(subset=["Avaliação Reclamação"], inplace=True)

    # Elimina/apaga as linhas duplicadas
    data.drop_duplicates(inplace=True)

    # Criando a variavel 'Solicitação' aonde cada linha vai receber o numero 1 como identificação
    data["Solicitação"] = 1

    # Transformando a coluna 'Data Finalização' de object para datetime
    data["Data Finalização"] = pd.to_datetime(data["Data Finalização"], format="mixed")

    # Criando a variável Mes(Número do mês)
    data["Mes Finalização"] = data["Data Finalização"].dt.month

    # Criando a variável Mes Nome(Com o nome do mês)
    data["Mes Nome Finalização"] = "NaN"

    data.loc[data["Mes Finalização"] == 1, "Mes Nome Finalização"] = "Janeiro"
    data.loc[data["Mes Finalização"] == 2, "Mes Nome Finalização"] = "Fevereiro"
    data.loc[data["Mes Finalização"] == 3, "Mes Nome Finalização"] = "Março"
    data.loc[data["Mes Finalização"] == 4, "Mes Nome Finalização"] = "Abril"
    data.loc[data["Mes Finalização"] == 5, "Mes Nome Finalização"] = "Maio"
    data.loc[data["Mes Finalização"] == 6, "Mes Nome Finalização"] = "Junho"
    data.loc[data["Mes Finalização"] == 7, "Mes Nome Finalização"] = "Julho"
    data.loc[data["Mes Finalização"] == 8, "Mes Nome Finalização"] = "Agosto"
    data.loc[data["Mes Finalização"] == 9, "Mes Nome Finalização"] = "Setembro"
    data.loc[data["Mes Finalização"] == 10, "Mes Nome Finalização"] = "Outubro"
    data.loc[data["Mes Finalização"] == 11, "Mes Nome Finalização"] = "Novembro"
    data.loc[data["Mes Finalização"] == 12, "Mes Nome Finalização"] = "Dezembro"

    # Criando a variável Dia da Semana(Número do Dia da Semana)
    data["Dia Semana Finalização"] = data["Data Finalização"].dt.weekday

    # Criando a variável Dia Semana Nome Finalização(Com o nome do dia da semana)
    data["Dia Semana Nome Finalização"] = "NaN"

    data.loc[data["Dia Semana Finalização"] == 0, "Dia Semana Nome Finalização"] = (
        "Segunda-Feira"
    )
    data.loc[data["Dia Semana Finalização"] == 1, "Dia Semana Nome Finalização"] = (
        "Terça-Feira"
    )
    data.loc[data["Dia Semana Finalização"] == 2, "Dia Semana Nome Finalização"] = (
        "Quarta-Feira"
    )
    data.loc[data["Dia Semana Finalização"] == 3, "Dia Semana Nome Finalização"] = (
        "Quinta-Feira"
    )
    data.loc[data["Dia Semana Finalização"] == 4, "Dia Semana Nome Finalização"] = (
        "Sexta-Feira"
    )
    data.loc[data["Dia Semana Finalização"] == 5, "Dia Semana Nome Finalização"] = (
        "Sábado"
    )
    data.loc[data["Dia Semana Finalização"] == 6, "Dia Semana Nome Finalização"] = (
        "Domingo"
    )

    # Criando a variável Ano
    data["Ano"] = data["Data Finalização"].dt.year

    # Renomeando algumas colunas
    data.rename(
        columns={
            "Região": "Regiao",
            "Faixa Etária": "Faixa_Etaria",
            "Data Finalização": "Data_Finalizacao",
            "Tempo Resposta": "Tempo_Resposta",
            "Nome Fantasia": "Nome_Fantasia",
            "Segmento de Mercado": "Segmento_de_Mercado",
            "Área": "Area",
            "Grupo Problema": "Grupo_Problema",
            "Como Comprou Contratou": "Como_Comprou_Contratou",
            "Procurou Empresa": "Procurou_Empresa",
            "Situação": "Situacao",
            "Avaliação Reclamação": "Avaliacao_Reclamacao",
            "Nota do Consumidor": "Nota_do_Consumidor",
            "Solicitação": "Solicitacao",
            "Mes Finalização": "Mes_Finalizacao",
            "Mes Nome Finalização": "Mes_Nome_Finalizacao",
            "Dia Semana Finalização": "Dia_Semana_Finalizacao",
            "Dia Semana Nome Finalização": "Dia_Semana_Nome_Finalizacao",
        },
        inplace=True,
    )

    # Local aonde os dados transformados serão salvos
    path = "../../Data/Data_for_clear/"
    data.to_parquet(f"{path}GOLD_data_transformed.parquet", index=False)

    # Conectando ao banco de dados SQLite
    conn = sqlite3.connect("../../Data/Data_for_clear/GOLD_data_transformed.db")
    data.to_sql("GOLD_data_transformed", conn, if_exists="replace", index=False)


if __name__ == "__main__":
    transformdata()
