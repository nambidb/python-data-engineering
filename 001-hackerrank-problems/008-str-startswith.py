import pandas as pd

# Create Employees DataFrame
employees = pd.DataFrame({
    'employee_id': [2, 3, 7, 8, 9],
    'name': ['Meir', 'Michael', 'Addilyn', 'Juan', 'Kannon'],
    'salary': [3000, 3800, 7400, 6100, 7700]
})


employees['bonus'] = employees.apply(lambda row: row['salary'] if (row['employee_id'] % 2 == 1 and not row['name'].startswith('M')) else 0, axis=1)
print(type(employees))
employees = employees[['employee_id','bonus']].sort_values(by='employee_id', ascending=True)
print(type(employees))


