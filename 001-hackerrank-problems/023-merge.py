import pandas as pd
from pandas import Int64Dtype

employees = pd.DataFrame([
    [1, "Alice"],
    [7, "Bob"],
    [11, "Meir"],
    [90, "Winston"],
    [3, "Jonathan"]
], columns=["id", "name"])

print(employees)


employee_uni = pd.DataFrame([
    [3, 1],
    [11, 2],
    [90, 3]
], columns=["id", "unique_id"])

print(employee_uni)


df_f = employees.merge(employee_uni, on="id",how='left')[['unique_id','name']]
df_f['unique_id'] = df_f[['unique_id']].astype("Int64")
print(df_f)
