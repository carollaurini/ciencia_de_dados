import pandas as pd
import sklearn 
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
from sklearn import feature_selection
import seaborn as sns
import openpyxl

def function_dataprep(janela,book_name):
    df = pd.read_csv("P:\\ciencia_de_dados\\Correlacao_de_fundos\\LaminaProducao\\bases\\bases_extraidas\\"+ book_name + "_" + janela +".csv",delimiter=',',decimal='.',parse_dates=True)
    df = df.dropna().drop_duplicates().rename(columns={'Unnamed: 0':'data'})
    
    df = df.melt(id_vars='data', value_vars=list(df.columns[1:]), value_name="FinancialPrice",var_name='Product')

    #Calculo das colunas temporais
    df['data']=pd.to_datetime(df['data'],format = '%Y-%m-%d')
    df['MesAno'] = df['data'].dt.strftime('%m-%Y')
    df['Mes_nomial']=df['data'].dt.strftime('%b')
    df['Mes']=df['data'].dt.strftime('%m').astype(int)
    df['Ano']=df['data'].dt.strftime('%Y').astype(int)

    if janela == 'diaria':
        df = df.groupby(['Product','MesAno']).agg(['max'])
        df.columns = df.columns.droplevel(1)
        df = df1.reset_index()
        df.head()

    df.sort_values(by=["Product",'data'],ascending=False,inplace=True)


    #Cria a coluna retorno e seta NaN na primeira linha de cada fundo
    df['FinancialPrice']=pd.to_numeric(df["FinancialPrice"], downcast="float")
    df["Retorno_1"] = (df.FinancialPrice.shift())/(df.FinancialPrice)
    df.loc[df.drop_duplicates('Product').index.values,'Retorno_1'] = np.NaN
    df['Retorno'] = df.Retorno_1.shift(periods=-1)
    df['Retorno'] = (df["Retorno_1"]-1)

    df.to_csv('P:\\ciencia_de_dados\\Correlacao_de_fundos\\LaminaProducao\\bases\\bases_tratadas\\retornos_'+ book_name + janela + '.csv',sep =';',decimal=',')
    return df