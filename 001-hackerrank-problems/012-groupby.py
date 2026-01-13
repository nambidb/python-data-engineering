import pandas as pd
#Employee DataFrame
df_employee = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'name': ['Joe', 'Jim', 'Henry', 'Sam', 'Max'],
    'salary': [70000, 90000, 80000, 60000, 90000],
    'departmentId': [1, 1, 2, 2, 1]
})

# Department DataFrame
df_department = pd.DataFrame({
    'id': [1, 2],
    'name': ['IT', 'Sales']
})

#print(df_employee)
#print(df_department)

df_F = df_employee.merge(df_department, left_on='departmentId', right_on='id',how='left')
print(df_F)

#h_salary = df_F.loc[df_F.groupby('departmentId')['salary'].idxmax()].reset_index(drop=True)
#print(h_salary)

max_salary = df_F.groupby('departmentId')['salary'].transform('max')
m_t_salary = df_F.groupby('departmentId').agg(dep_total=('salary','max')).reset_index()
print(m_t_salary)
h = df_F[df_F['salary'] == max_salary].reset_index(drop=True)
#print(h)
final = h[['name_y','name_x','salary']].rename(columns={'name_y':'Department','name_x':'Employee','salary':'Salary'})
#print(final)
#print(type(final))