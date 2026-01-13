import pandas as pd

# Create the DataFrame
df = pd.DataFrame({
    "teacher_id": [1, 1, 1, 2, 2, 2, 2],
    "subject_id": [2, 2, 3, 1, 2, 3, 4],
    "dept_id":    [3, 4, 3, 1, 1, 1, 1]
})



df= df[['teacher_id','subject_id']]
print(df)
df = df.drop_duplicates(['teacher_id','subject_id'])
print(df)
df = df.groupby(["teacher_id"]).agg(total_sub=('subject_id','count')).reset_index()
#df = df.groupby(["teacher_id"])['subject_id'].transform('count').reset_index()
print(df)