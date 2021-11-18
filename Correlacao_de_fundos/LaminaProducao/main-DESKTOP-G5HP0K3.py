#Libs criadas
from MWB_data import function_extracao
import lamina
import dataprep
import graficos

#Libs do sistema
import sys
import os
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

#sys.path.insert(0,'p:\ciencia_de_dados\Correlacao_de_fundos\LaminaProducao')
#os.system("p:\venv\scripts\activate.bat")

## Front End
df_array = []
ticker_names = []
while True:
    
        book_name,janela,ticker_array = function_extracao()
        df = dataprep.function_dataprep(janela,book_name)
        df_array.append(df)
        
        ticker_names = ticker_names + ticker_array #Somando arrays kkkk
        
        exite_var = input("Gostaria de extrair ativos em outra janela? (y/n)")
        if exite_var == 'y':
            continue
        if exite_var == 'n':
            break  
        else:
            print('Erro, tente novamente.')
            quit()
        
nome_benchmark = input("Digite o nome do benchmark: ")
print(nome_benchmark)

#Fundos sem o benchmark
col_fundos_input =  [x for x in ticker_names if x != nome_benchmark]


df = pd.concat(df_array)
tempo = 12 

##  Lamina univariada
#Marcação dos pontos positivos e negativos
df['Retorno_Positivo'] = np.where(df.Retorno >= 0, 1, 0)
df['Retorno_Negativo'] = np.where(df.Retorno < 0, 1, 0)

#Reshape dataframe para algumas funções
df_sub = df.pivot(index=["data","Ano","Mes"], columns="Product", values="Retorno_1")
df_sub = df_sub.reset_index()
df_sub = df_sub.dropna()

#Calculo do tracking error  
df_sub1 = df_sub.apply(lambda x: lamina.function_tracking_error(x,df_sub,nome_benchmark) if x.name in col_fundos_input else x)
df_concat = pd.concat([df_sub, df_sub1[col_fundos_input].add_suffix('_spread')], axis=1, join="inner")
col_fundos_spread = df_concat.columns[3:]

df.sort_values(by=["Product",'data'],ascending=False,inplace=True)
table = df.groupby('Product').agg({"Retorno": ['max','min','mean',lambda y: lamina.vol_anualizada(y,tempo)] ,"Retorno_Negativo":lamina.Meses_Negativos,"Retorno_Positivo": lamina.Meses_Positivos,"Retorno_1" : [lamina.retorno_total, lambda x: lamina.retorno_anualizado(x,tempo)]})

table.columns = table.columns.droplevel(0)
table.columns = ["Retorno Mensal Máximo","Retorno Mensal Minimo", "Média dos Retornos Mensais",'Volatilidade Anualizada','Meses Negativos','Meses Positivos','Retorno Total','Retorno Anualizado']
table["Sharpe"] = (table["Retorno Anualizado"] / table["Volatilidade Anualizada"])

#Criando o DrawDown
df.sort_values(by=["Product",'data'],ascending=True,inplace=True)
table2 = df.groupby('Product').agg({"FinancialPrice":lamina.MDD}).rename(columns={"FinancialPrice":"Maximo Drawdown"})

#Adiciona o DrawDown na tabela principal
x=pd.concat([table,table2],axis=1)
df_univar = x.T
df_univar.index.name=lamina.Periodo(df.data)


##  Bivariada  
#Regressao:
k=0
v = []
for i in col_fundos_input:
    v.append(lamina.regressao_linear(df,i,nome_benchmark))
df_bivar = pd.DataFrame(v,index=col_fundos_input).rename(columns = {0:'Beta',1:'Alpha'}).T

#Tracking Error:
v=[]
for i in col_fundos_input:
    v.append(np.std(df_sub1[i]))
df_bivar.loc['Tracking Error'] = [x for x in v]
df_bivar.index.name = ' '


##  Plotagem

#Porcentualizando os retornos para plotar os graficos
df_sub[ticker_names] = (df_sub[ticker_names] *100)-100

#Densidade
graficos.graf_densidade_retorno(df_sub[ticker_names],book_name)
#Matriz de Regressoes
df.reset_index()
graficos.graf_linear_reg(df,book_name)
#Matriz das correlacoes 

graficos.graf_correlacao(df_sub[ticker_names],book_name)

##  Escrevendo no Excel

# Create a Pandas Excel writer using XlsxWriter as the engine.


writer = pd.ExcelWriter('.\Laminas\Lamina_' + book_name + '.xlsx', engine='xlsxwriter')
workbook = writer.book
worksheet = workbook.add_worksheet('Sumario')
options = {
    'width': 256,
    'height': 100,
    'x_offset': 10,
    'y_offset': 10,

    'font': {'color': 'white',
             'size': 20},
    'align': {'vertical': 'middle',
              'horizontal': 'center'
              },
    'gradient': {'colors': ['#3E9EBC',
                            '#2F778D',
                            ]},
}
options2 = {
    'width': 200,
    'height': 20,
    'x_offset': 10,
    'y_offset': 10,

    'font': {'color': 'white',
             'size': 15},
    'align': {'vertical': 'middle',
              'horizontal': 'center'
              },
    'gradient': {'colors': ['#800000',
                            '#800000',
                            ]},
}
options3 = {
    'width': 200,
    'height': 20,
    'x_offset': 10,
    'y_offset': 10,

    'font': {'color': 'white',
             'size': 10},
    'align': {'vertical': 'middle',
              'horizontal': 'center'
              },
    'gradient': {'colors': ['#3E9EBC',
                            '#2F778D',
                            ]},
}

worksheet.insert_textbox('B2', 'Lâmina',options)
writer.sheets['Sumario'] = worksheet
spread_names = [s for s in df_concat.columns[3:] if 'spread' in s]
#Tabela de retornos coloridos
worksheet.insert_textbox('B8', 'Retorno do fundo - Retorno do benchmarck',options2)
table_size = len(df.Ano.unique()) + 4

const = 12

for i in range(len(col_fundos_spread)):
    lamina.function_retorno(df_concat,i,const,col_fundos_spread).to_excel(writer,sheet_name = 'Sumario',startrow=(8 + table_size*i), startcol=0,index_label='Retorno')
    if col_fundos_spread[i] in spread_names:
        worksheet.insert_textbox('B'+ str((8 + table_size*i)), 'Spread do Retorno',options2)
    else:    
        worksheet.insert_textbox('B'+ str((8 + table_size*i)), 'Retorno',options3)
    
#Graficos

worksheet.insert_image('R'+ str((8+ len(df_univar)+10)),'.\Graficos\PairplotRegressaoLin.'+book_name+'.png')
worksheet.insert_image('W'+ str((8+ len(df_univar)+10)),'.\Graficos\Retorno_density_distribution'+book_name+'.png')
worksheet.insert_image('AA'+ str((8+ len(df_univar)+10)) ,'.\Graficos\CorrelationMatrix'+book_name+'.png')#,{'x_scale': 2, 'y_scale': 2})    

#Tabelas com os resultados
df_univar = df_univar.reindex(sorted(df_univar.columns), axis=1)
first_column = df_univar.pop(nome_benchmark)
df_univar.insert(len(df_univar.columns), nome_benchmark, first_column)
df_bivar = df_bivar.reindex(sorted(df_bivar.columns), axis=1)
df_univar.to_excel(writer, sheet_name='Sumario',startrow=8,startcol = 17)
df_bivar.to_excel(writer, sheet_name='Sumario',startcol=17,startrow = (8+ len(df_univar)+2))


#Formatacao
format_dict={"number": writer.book.add_format({'num_format': '0.0','align':'center', 'valign':'vcenter'}),
            "percentage_one_decimal" : writer.book.add_format({'num_format': '0.0%','align':'center', 'valign':'vcenter'})}

writer.sheets['Sumario'].set_column(17, 30, 30)
writer.sheets['Sumario'].set_column(0, 0, 15)
writer.sheets['Sumario'].set_column(13, 14, 15)


for i in [9,10,11,12,15,16,18,23]:
    writer.sheets['Sumario'].set_row(i, None,format_dict["percentage_one_decimal"] )
for i in [13,14,17,21,22]:
    writer.sheets['Sumario'].set_row(i, None,format_dict["number"] )
    
writer.sheets['Sumario'].set_column(1,14,10,format_dict["percentage_one_decimal"])
    
    
df_sub.to_excel(writer,sheet_name = 'UnstackRetornosPercentuais')
df.to_excel(writer, sheet_name='StackRetornos1')

writer.save()
