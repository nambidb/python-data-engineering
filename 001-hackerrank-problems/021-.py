import pandas as pd

# Create Activities DataFrame
df_activities = pd.DataFrame({
    'sell_date': [
        '2020-05-30', '2020-06-01', '2020-06-02',
        '2020-05-30', '2020-06-01', '2020-06-02',
        '2020-05-30'
    ],
    'product': [
        'Headphone', 'Pencil', 'Mask',
        'Basketball', 'Bible', 'Mask',
        'T-Shirt'
    ]
})

print(df_activities)

#df_activities = df_activities.groupby('sell_date')['product'].count().reset_index(name='num_sold')
#print(df_activities)
df_activities = df_activities.groupby('sell_date').agg(num_sold=('product','nunique'),products=('product',lambda x:','.join(sorted(set(x))))).reset_index()
print(df_activities)
