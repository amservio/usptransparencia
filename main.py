import streamlit as st
import pandas as pd
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import json
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

st.set_page_config(layout="wide")

data_final = date(2024, 8, 1)
qtd_meses = 12

unidades = ["FFLCH", "IME", "IF", "FAU", "EACH"]
categorias = ["Celetista", "Doc Apos", "Func Apos", "Func Aut", "Docente"]
competencias = [data_final + relativedelta(months=-i) for i in range(0, qtd_meses)]

def get_transparency_portal_data():

  df = pd.DataFrame(columns=['Unid/Orgão', 'Depto/Setor', 'Jornada', 'Categoria',
        'Data Ingresso/Aposentadoria', 'Classe', 'Ref/MS', 'Função',
        'Função de Estrutura', 'Data designação', 'Tempo USP',
        'Parcelas Eventuais', 'Salário Mensal', 'Líquido', 'Competência'])
  for competencia in competencias:
    print(f"Buscando competência {competencia.strftime('%d/%m/%Y')}")
    for unidade in unidades:
      for categoria in categorias:
        url = f"https://uspdigital.usp.br/portaltransparencia/gerarArquivoTranspConsol?print=true&anompes=&nomundorg={unidade}&nomdepset=&tipcon={categoria}&tipcla=&nomabvfnc=&dtainictc={competencia.strftime('%d/%m/%Y')}&ctcatl=C&nomfncetr=&condicao=&reload=exportarArquivo"
        result = requests.get(url)
        df_competencia = pd.read_csv(StringIO(result.text), sep=";", decimal = ",", dayfirst = True, index_col=False)
        df_competencia['Competência'] = competencia
        df = pd.concat([df, df_competencia])

  df['Competência'] = pd.to_datetime(df['Competência'], dayfirst = True)
  df['Data Ingresso/Aposentadoria'] = pd.to_datetime(df['Data Ingresso/Aposentadoria'], dayfirst = True)
  df['Data designação'] = pd.to_datetime(df['Data designação'], dayfirst = True)

  return df


def get_transparency_portal_data2(unid, cat, mes):
    url = f"https://uspdigital.usp.br/portaltransparencia/gerarArquivoTranspConsol?print=true&anompes=&nomundorg={unid}&nomdepset=&tipcon={cat}&tipcla=&nomabvfnc=&dtainictc={mes.strftime('%d/%m/%Y')}&ctcatl=C&nomfncetr=&condicao=&reload=exportarArquivo"
    result = requests.get(url)
    df = pd.read_csv(StringIO(result.text), sep=";", decimal = ",", dayfirst = True, index_col=False)
    df['Competência'] = mes

    df['Competência'] = pd.to_datetime(df['Competência'], dayfirst = True)
    df['Data Ingresso/Aposentadoria'] = pd.to_datetime(df['Data Ingresso/Aposentadoria'], dayfirst = True)
    df['Data designação'] = pd.to_datetime(df['Data designação'], dayfirst = True)
    return df

col1, col2, col3 = st.columns(3)

unid = col1.selectbox('Unidade', unidades)
cat = col2.selectbox('Categoria', categorias)
mes = col3.selectbox('Competência', competencias)
df = get_transparency_portal_data2(unid, cat, mes)
st.dataframe(df, use_container_width=True, hide_index=True)
