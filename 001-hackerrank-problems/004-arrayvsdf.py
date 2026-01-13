import numpy as np
import pandas as pd
amounts = np.array([50.5,100,200])
print (amounts)
print(type(amounts))

risk_flag = np.where(amounts > 100, 'HIGH', 'LOW')
print(risk_flag)

df_f = pd.DataFrame({
                    'id':['1','2','3'],
                    'amount':amounts,
                    'risk_flag':risk_flag
})
print(df_f)