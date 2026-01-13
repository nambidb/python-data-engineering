import pandas as pd

#def valid_emails(users: pd.DataFrame) -> pd.DataFrame:





users = pd.DataFrame({
    'user_id': [1, 2, 3, 4, 5, 6, 7],
    'name': ['Winston', 'Jonathan', 'Annabelle', 'Sally', 'Marwan', 'David', 'Shapiro'],
    'mail': [
        'winston@leetcode.com',
        'jonathanisgreat',
        'bella-@leetcode.com',
        'sally.come@leetcode.com',
        'quarz#2020@leetcode.com',
        'david69@gmail.com',
        '.shapo@leetcode.com'
    ]
})

domain_ok = users['mail'].str.endswith('@leetcode.com')
print(domain_ok)
print(type(domain_ok))


prefix = users['mail'].str.split('@').str[0]
print(prefix)
print(type(prefix))

starts_letter = prefix.str[0].str.isalpha()
print(starts_letter)

allowed_chars = prefix.str.match(r'^[A-Za-z][A-Za-z0-9._-]*$')
print(allowed_chars)

mask = (domain_ok & allowed_chars & starts_letter)
print(mask)

users = users.loc[mask].reset_index(drop=True)

print(users)
#print(valid_emails(users))


