import pandas as pd

# Create Orders DataFrame
df_orders = pd.DataFrame({
    'order_number': [1, 2, 3, 4],
    'customer_number': [1, 2, 3, 3]
})

#print(df_orders)

df_orders = df_orders.groupby('customer_number')['order_number'].count().reset_index(name='tot_ord')
print(df_orders)

max_orders = df_orders['tot_ord'].max()
#print(max_orders)
top_customer = df_orders[df_orders['tot_ord'] == max_orders]
print(top_customer)


