import pandas as pd

# Create the dataframe
df_students = pd.DataFrame({
    'student': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'class': ['Math', 'English', 'Math', 'Biology', 'Math', 'Computer', 'Math', 'Math', 'Math']
})



df_students = df_students[['class']]

df_students = df_students.groupby('class').agg(tot_cnt=('class', 'count')).reset_index()

mask =(df_students['tot_cnt']>=5)
df_students = df_students[mask]
print(df_students)

