import pandas as pd
import numpy as np

df = pd.DataFrame({'amount':[50,100,200,4300,545,45,232,557657,324]})
conditions = [df['amount'] > 1000,df['amount'] < 200]
print(conditions)
choice    = ['vip','regular']
df['segment'] = np.select(conditions,choice,default='small')
print(df)