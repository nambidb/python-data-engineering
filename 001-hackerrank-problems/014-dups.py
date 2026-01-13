import pandas as pd

person = pd.DataFrame({'id':[1,2,3],'email':['bob@example.com','john@example.com','bob@example.com']})

ded = person.sort_values(by='id').drop_duplicates(subset=['email'], keep='first')
#print(type(ded))

#print(person)
#print(ded)

#print(len(person))

person.drop(person.index, inplace=True)
#print(len(person))
for index,row in ded.iterrows():
    person.loc[len(person)] = row
    #print(index)
    #print(row)

print(person)

#print(person)
#print(type(person))
#person.update(ded)
#person.loc[:] = ded.values

#person.index = range(len(ded))
#print(person)