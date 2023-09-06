
import pandas as pd
import numpy as np
df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6],[8,9,10]]))

# Sử dụng thuộc tính `shape`
print(df.shape)

# Hoặc sử dụng hàm `len()` với thuộc tính `index`
print(len(df))