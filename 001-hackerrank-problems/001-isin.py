import pandas as pd
import numpy as np

#np.random.seed(42)
#transactions = np.random.uniform(low=10,high=100,size=1000)
transactions  = np.array([100,434,999,111,343.434,22,2000])
print(transactions)
print(type(transactions))
#blacklist = np.random.choice(transactions,size=1000,replace=False)
blacklist = np.array([111,999,666])
print(blacklist)
flags = (transactions > 1000) | np.isin(transactions,blacklist)
blockedtransactions = transactions[flags]
riskflag = np.where(flags,'high','low')
print(riskflag)
print(blockedtransactions)


df = pd.DataFrame({'transaction_id':[101,102,101,103]})
print(df)
unique_ids = np.unique(df['transaction_id'])
print(unique_ids)
df_unique = df[df['transaction_id'].isin(unique_ids)]
print(df_unique)
df_unique = df.drop_duplicates(subset=['transaction_id'])
print(df_unique)
