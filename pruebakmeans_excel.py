import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
 
dataframe = pd.read_excel("infosep2020_agosto2022.xls", engine='openpyxl')
dataframe.head()

sb.pairplot(dataframe.dropna(), hue='departamento_nombre',size=4,vars=["año","grupo_edad_id","cantidad_casos"],kind='scatter')
plt.show()