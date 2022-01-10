import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv ("C:\\tmp\\P65.csv")
print( df.head() )
print( df.corr(method ='kendall') )
