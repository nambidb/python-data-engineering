import pandas as pd

data = {
    "id": [1, 2, 3],
    "salary": [100, 200, 300]
}

df = pd.DataFrame(data)

print(df)

df = df['salary'].drop_duplicates().sort_values(ascending=False).reset_index(drop=True)


print(df)

print(df.loc[2])
print(df.iloc[2])

print(type(df))
N = 3
#print(len(df))

if N <= len(df):
    result = df[N-1]
else:
    result = None

#print(result)


f_df = pd.DataFrame({'getnthhighestsalary({})'.format(N):[result]})

#print(f_df)






