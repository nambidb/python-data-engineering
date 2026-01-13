import pandas as pd
from numpy.ma.extras import vstack

salesperson = pd.DataFrame([
    [1, "John", 100000, 6, "4/1/2006"],
    [2, "Amy", 12000, 5, "5/1/2010"],
    [3, "Mark", 65000, 12, "12/25/2008"],
    [4, "Pam", 25000, 25, "1/1/2005"],
    [5, "Alex", 5000, 10, "2/3/2007"]
], columns=["sales_id", "name", "salary", "commission_rate", "hire_date"])
salesperson['hire_date'] = pd.to_datetime(salesperson['hire_date'])
#print(salesperson)
company = pd.DataFrame([
    [1, "RED", "Boston"],
    [2, "ORANGE", "New York"],
    [3, "YELLOW", "Boston"],
    [4, "GREEN", "Austin"]
], columns=["com_id", "name", "city"])
#print(company)
orders = pd.DataFrame([
    [1, "1/1/2014", 3, 4, 10000],
    [2, "2/1/2014", 4, 5, 5000],
    [3, "3/1/2014", 1, 1, 50000],
    [4, "4/1/2014", 1, 4, 25000]
], columns=["order_id", "order_date", "com_id", "sales_id", "amount"])
orders['order_date'] = pd.to_datetime(orders['order_date'])
#print(orders)

#orders = orders[orders['com_id'] != 1]
#print(orders)

red_com_id = company.loc[company['name'] == 'RED', 'com_id'].iloc[0]
sales_to_red = orders.loc[orders['com_id'] == red_com_id, 'sales_id']
result = salesperson.loc[~salesperson['sales_id'].isin(sales_to_red), ['name']]

vs

com_red = company.loc[company['name'] == 'RED', 'com_id'].iloc(0)
sales_red = orders.loc[orders['com_id'] == com_red, 'sales_id']
sales_person_1 = sales_person.loc[~sales_person['sales_id'].isin(sales_red), ['name']]
return sales_person_1

print(result)
