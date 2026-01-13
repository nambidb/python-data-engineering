import pandas as pd

# Create Employee dataframe
employees = pd.DataFrame([
    [101, "John", "A", None],
    [102, "Dan", "A", 101],
    [103, "James", "A", 101],
    [104, "Amy", "A", 101],
    [105, "Anne", "A", 101],
    [106, "Ron", "B", 101]
], columns=["id", "name", "department", "managerId"])

#print(employees)

direct_reports = employees.groupby('managerId').size().reset_index(name='num_reports')
print(direct_reports)
managers = direct_reports[direct_reports['num_reports'] >= 5]
print(managers)
result = managers.merge(employees, left_on="managerId", right_on="id")[["name"]]
print(result)