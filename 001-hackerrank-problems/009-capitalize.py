import pandas as pd

# Create Users DataFrame
users = pd.DataFrame({
    'user_id': [1, 2],
    'name': ['aLice', 'bOB']
})
users['name'] = users['name'].str.capitalize().to_frame().sort_values(by=['name'], ascending=True)
print(type(users))
print(users.info())
print(users)

