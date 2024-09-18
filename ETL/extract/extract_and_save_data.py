# Importando as bibliotecas necessárias
import pandas as pd
import glob


def extractandload():
    """
    Função para extrair e salvar os dados.
    Camada SILVER
    """
    # Local aonde será salvo os dados coletados
    path = "../../Data/Data_for_clear/"

    # Criando uma variável com a extensão do arquivo a ser lido
    extensao = "csv"

    # Agrupando/Concatenando os arqquivos, tudo em um único DataFrame
    arquivos_csv = [i for i in glob.glob(f"../../Data/Data_for_csv/*.{extensao}")]
    df_gov = pd.concat([pd.read_csv(f, sep=";") for f in arquivos_csv])
    df_gov.to_parquet(f"{path}SILVER_data.parquet", index=False)


if __name__ == "__main__":
    extractandload()
