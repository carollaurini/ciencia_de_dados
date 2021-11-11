from MWB_data import function_extracao
import sys
import os
import lamina
import dataprep

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

df_array = []
while True:
    
        book_name,janela,ticker_array = function_extracao()
        df = dataprep.function_dataprep(janela,book_name)
        df_array.append(df)
        
        exite_var = input("Gostaria de extrair ativos em outra janela? (y/n)")
        if exite_var == 'y':
            continue
        if exite_var == 'n':
            break  
        else:
            print('Erro, tente novamente.')
            quit()
        

nome_benchmark = input("Digite o nome do benchmark: ")

df = pd.concat(df_array)

print(df.head())

