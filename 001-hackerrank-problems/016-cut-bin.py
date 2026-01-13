import numpy as np
import pandas as pd

# Create Accounts DataFrame
accounts = pd.DataFrame({
    "account_id": [3, 2, 8, 6],
    "income": [108939, 12747, 87709, 91796]
})

print(accounts)


accounts['category'] = pd.cut(accounts['income'], bins=[0,20000,50000,float("inf")],labels=['Low','Medium','High'])
print(accounts)

accounts = accounts.groupby(['category'])['account_id'].count().reset_index(name='accounts_count')

print(accounts)