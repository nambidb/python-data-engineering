import pandas as pd
import numpy as np

df = pd.DataFrame({
    'order_id': [1, 2, 3, 4, 5],
    'date': ['2025-11-19', '2025-11-19', '2025-11-19', '2025-11-20', '2025-11-20'],
    'category': ['Retail', 'E-commerce', 'Retail', 'Retail', 'E-commerce'],
    'amount': [500, 1500, 800, 300, 2000]
})

df_daily = df.groupby(['date','category']).agg(
    revenue=('amount','sum'),
    orders= ('order_id','count')
).reset_index()

print(df_daily)