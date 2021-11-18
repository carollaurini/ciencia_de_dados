import sys
sys.path.insert(0,'p:/Lib')
from MWB_Data_Reader import bd_per_year, BasketHistoricalData
from datetime import datetime


print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
"""
    basket_array is an array of dictionaries with the following fields
    {"Ticker" : ttt, "Source" : "Bloomberg"/"Databate"/"GoogleTrends",
      "Proxy ticker" : ttt, "Proxy source" : "Bloomberg"/"Databate"/"GoogleTrends"}
      Proxy ticker is optional
"""

basket_array = [{"Ticker": "TEAP",
                "Source": "Database"},
                {"Ticker": "FOCUS GENERATION-J",
                "Source": "Database"},
                ]
                #{"Ticker": "Vacina",
                #"Source": "GoogleTrends"}]

min_d = datetime.strptime("2018-12-31", "%Y-%m-%d")
max_d = datetime.strptime("2021-06-30", "%Y-%m-%d")


data = BasketHistoricalData("Nome", basket_array)
data.loadFromDatabase(min_d, max_d)
#data.loadFromGoogleTrends(min_d, max_d)
prices=data.getData(dropna=False, useproxies=True)
print(prices)
