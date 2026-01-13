import pandas as pd
import numpy as np

# Create Products DataFrame
products = pd.DataFrame({
    "product_id": [0, 1],
    "store1": [95, 70],
    "store2": [100, np.nan],
    "store3": [105, 80]
})

print(products)


products = products.melt(id_vars=['product_id'], var_name='store', value_name='price')
products = products.dropna(subset=['price'])
print(products)