import pandas as pd

# Input tables
customers = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['Joe', 'Henry', 'Sam', 'Max']
})

orders = pd.DataFrame({
    'id': [1, 2],
    'customerId': [3, 1]
})

import pandas as pd


def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    nev_ord = customers[~customers['id'].isin(orders['customerId'])]
    nev_ord = nev_ord[['name']].rename(columns={'name': 'Customers'})
    return nev_ord

fr = find_customers(customers,orders)
print(fr)


