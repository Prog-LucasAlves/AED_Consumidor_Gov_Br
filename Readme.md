# ![The San Juan Mountains are beautiful!](./Image/download.png "San Juan Mountains") Análise de Dados das reclamações feitas no site Consumidor.gov.br

## ![Tecnologias utilizadas](https://cdn-icons-png.flaticon.com/24/5460/5460163.png) Tecnologias utilizadas

1. Python

- Dados extraidos nesse *[link](https://www.consumidor.gov.br/pages/dadosabertos/externo/)*

- Dados ate o mês 11/2022 - Atualizado dia 02/12/2022

## 💬 Sobre o Serviço

- O **Consumidor.gov.br** é um serviço público que permite a interlocução direta entre consumidores e empresas para solução de conflitos de consumo pela internet. *[Consumidor.gov.br](https://www.consumidor.gov.br/pages/principal/?1662172782421)*

## ![Etapas de Limpeza realizadas](https://cdn-icons-png.flaticon.com/24/6104/6104865.png) Etapas de Limpeza realizadas

**Considerações:**

- Após a união do arquivos CSVs, o DataFrame ficou com 1188519 registros e 19 colunas.
- Foi verificado que o DataFrame havia 2.73% de valores ausentes(Em 3 colunas do DataFrame).

| Coluna | Valores Ausentes | % de Valores Ausentes |
| ------ | ---------------- | --------------------- |
| Nota do Consumidor | 591305 | 49.75 |
| Tempo Resposta | 24924 | 2.10 |
| Sexo | 89 | 0.01 |

**Etapas:**

1. Imputação dos valores ausentes

    1. Coluna 'Nota do Consumidor' -> Será imputado valores utilizando o método de preenchimento progressivo (forward fill) para os valores NaN.
    2. Coluna 'Tempo Resposta' -> será imputado o valor 0(Zero) para os valores NaN - Pois são reclamações que não foram respondidas.
    3. Coluna 'Sexo' -> será imputado o valor 'O'(Outros) para os valores NaN.

2. linhas Duplicadas

    1. Foram eliminadas do Dataframe as linhas duplicadas.

- Após as transformações realizadas o DataSet ficou com 1184928 registros e 19 colunas.

## ![Perguntas a serem respondidas](https://cdn-icons-png.flaticon.com/24/4501/4501315.png) Perguntas a serem respondidas

1. **As reclamações estão aumentando ou diminuindo**
2. **Quais Segmentos de Mercado com menor indice(%) de respostas por reclamações.**

## ![Deploy dos dados](https://cdn-icons-png.flaticon.com/24/1508/1508878.png) Deploy dos dados

[Site](https://bit.ly/3AVnEFo)

## ![Planejamento](https://cdn-icons-png.flaticon.com/24/5341/5341024.png) Planejamento

- [x] Coleta dos dados
- [x] Limpeza e Transformação dos dados
- [ ] Deploy Streamlit

## ![CI](https://cdn-icons-png.flaticon.com/24/6577/6577286.png) CI

[![Linter](https://github.com/Prog-LucasAlves/AED_Consumidor_Gov_Br/actions/workflows/Linter.yml/badge.svg)](https://github.com/Prog-LucasAlves/AED_Consumidor_Gov_Br/actions/workflows/Linter.yml)
[![Linter](https://github.com/Prog-LucasAlves/AED_Consumidor_Gov_Br/actions/workflows/Linter.yml/badge.svg)](https://github.com/Prog-LucasAlves/AED_Consumidor_Gov_Br/actions/workflows/Linter.yml)
[![Data Clear](https://github.com/Prog-LucasAlves/AED_Consumidor_Gov_Br/actions/workflows/Data_Clear.yml/badge.svg)](https://github.com/Prog-LucasAlves/AED_Consumidor_Gov_Br/actions/workflows/Data_Clear.yml)

## ![P](https://cdn-icons-png.flaticon.com/24/8422/8422251.png) Pacotes Python utilizados

[![Pandas](https://badge.fury.io/py/pandas.svg)](https://badge.fury.io/py/pandas)
