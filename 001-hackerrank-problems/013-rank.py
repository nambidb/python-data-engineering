import pandas as pd

# Create Scores DataFrame
df_scores = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6],
    'score': [3.50, 3.65, 4.00, 3.85, 4.00, 3.65]
})

#print(df_scores)

df_scores['rank'] = df_scores['score'].rank(method='dense', ascending=False).astype(int)
print(df_scores)
df_scores = df_scores.sort_values(by='rank').reset_index(drop=True)
print(df_scores)
df_scores = df_scores[['score','rank']]
print(df_scores)
