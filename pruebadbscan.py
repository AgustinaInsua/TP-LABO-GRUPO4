from numpy import unique
from numpy import where
from matplotlib import pyplot
from sklearn.datasets import make_classification
from sklearn.cluster import DBSCAN
import pandas as pd
from sklearn.preprocessing import StandardScaler

# inicializar el conjunto de datos con el que trabajaremos
dataframe = pd.read_csv(r"info2018.csv")
x = dataframe.iloc[:,[0,5,7,9]]
scaler=StandardScaler()
x_scaled=scaler.fit_transform(x)


# definir el modelo
dbscan_model = DBSCAN(eps=0.25, min_samples=9)

# entrenar el modelo
dbscan_model.fit(x_scaled)

# asignar cada punto de datos a un grupo
dbscan_result = dbscan_model.fit_predict(x_scaled)

# obtener todos los grupos únicos
dbscan_clusters = unique(dbscan_result)

# graficar el DBSCAN de grupos
for dbscan_cluster in dbscan_clusters:
    # obtener todos los puntos de datos que caen en este grupo
    index = where(dbscan_result == dbscan_cluster)
    # hacer el gráfico
    # pyplot.scatter(x_scaled['provincia_id'], x_scaled['cantidad_casos'], cmap='rainbow')
    pyplot.scatter(x_scaled[index, 3], x_scaled[index, 0], cmap='rainbow')

# mostrar el gráfico DBSCAN
pyplot.show()