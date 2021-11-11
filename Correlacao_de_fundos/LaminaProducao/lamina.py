import pandas as pd
import sklearn 
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
from sklearn import feature_selection
import seaborn as sns
import scipy.stats
from matplotlib import pyplot as plt
import math
import openpyxl
from  matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import xlsxwriter
from sklearn import feature_selection
import datetime

#Cria a df_sub1 para calculo do tracking error 
def function_tracking_error(x):
    print(x.name)
    return (x.div(df_sub[nome_benchmark]))#divisao entre o o retorno do fundo com o do benchmark

#Retorno Mensal
def function_retorno(df,i,const,col_fundos):

    pivot_table = pd.pivot_table(df,index=['Ano'],values=[col_fundos[i]],fill_value=1,aggfunc='prod',columns=['Mes'])#,margins=True,margins_name="Year")
    pivot_table=pivot_table.rename(columns={1: 'Jan', 2:"Feb",3:"Mar", 4:"Apr", 5:"May", 6:"Jun",7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"})
    
    ITD_Matrix = [df[df.Ano <= i_ano][col_fundos[i]].prod() for i_ano in df.Ano.unique()]
    YTD_Matrix = [df[df.Ano == i_ano][col_fundos[i]].prod() for i_ano in df.Ano.unique()]
    
    ITD_df=pd.DataFrame(ITD_Matrix, columns = [col_fundos[i]] ,index=df_concat.Ano.unique())
    YTD_df=pd.DataFrame(YTD_Matrix, columns = [col_fundos[i]] ,index=df_concat.Ano.unique())
    
    ITD_df.columns = pd.MultiIndex.from_product([ITD_df.columns, ['Retorno LTD']])
    YTD_df.columns = pd.MultiIndex.from_product([YTD_df.columns, ['Retorno YTD']])
    
    pivot_table = pd.concat([pivot_table,YTD_df,ITD_df],axis=1)
    pivot_table = pivot_table-1
    
    # backgroung color mapping
    my_cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256)
    pivot_table.index.name="Retorno Mensal"
  
    return pivot_table

def vol_anualizada(x,tempo):
    z = x.std() * (tempo**(1/2))
    return z

def retorno_anualizado(x,tempo):
    return (x.product()**(tempo/float(x.count())) - 1)

def MDD(x):
    return min(((x/x.cummax()) - 1))

def retorno_total(x):
    return (x.prod() - 1)

def Meses_Positivos(x): #Gambiarra para nomear sum
    return x.sum()

def Meses_Negativos(x):
    return x.sum()

def Periodo(x):
    return datetime.datetime.strptime(min(x), '%Y-%m-%d').strftime('%b-%Y')+' a ' + datetime.datetime.strptime(max(x), '%Y-%m-%d').strftime('%b-%Y')

def regressao_linear(df,nome_do_fundo,nome_benchmark): 
    df['Retorno100'] = df['Retorno']*100
    df_fundo = df.loc[df.Product == nome_do_fundo,['data','Retorno100']]
    df_bench = df.loc[df.Product == nome_benchmark,['data','Retorno100']]

    df_fundo.index = df_fundo['data']
    df_bench.index = df_bench['data']
    df_join =pd.merge(df_bench, df_fundo,how='inner',left_index=True, right_index=True).dropna()[['Retorno100_x','Retorno100_y']]

    #Regressao Linear total
    x = (df_join['Retorno100_x']).values.reshape((-1, 1))
    y= (df_join['Retorno100_y']).values.reshape((-1, 1))
    
    regr = sklearn.linear_model.LinearRegression()
    regr.fit(x, y)
    return regr.coef_[0][0],regr.intercept_[0]
