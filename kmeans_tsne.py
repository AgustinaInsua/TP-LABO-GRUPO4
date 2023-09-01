import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from scipy.spatial import ConvexHull
from scipy.spatial import QhullError
from sklearn.preprocessing import StandardScaler

urls = [
    'https://github.com/AgustinaInsua/TP-LABO-GRUPO4/raw/main/info2018.csv'
]

# Cargar y procesar los datos de los tres años
data_frames = []
nrows_to_read = 10000  #  filas a cargar
for url in urls:
    data = pd.read_csv(url, nrows=nrows_to_read)
    data_frames.append(data)

# Combinar los DataFrames en uno solo
combined_data = pd.concat(data_frames, ignore_index=True)
combined_data

# Borramos las rows de los grupo_edad_id que sean igual a 17
index = combined_data[combined_data['grupo_edad_id'] == 17].index
combined_data.drop(index , inplace=True)

# Limpia valores de las columnas antes de asignar
string_columns = ['evento_nombre', 'provincia_nombre', 'grupo_edad_desc']
for column in string_columns:
    combined_data[column] = combined_data[column].str.strip('"')  # Elimina comillas
    combined_data[column] = combined_data[column].str.strip()     # Elimina espacios en blanco

# Organizamos los grupos de edad y provincias asignando un nuevo id. Ademas, asignamos id a columnas no númericas

assignment_mapping = {
    'evento_nombre': {
        'Bronquiolitis en menores de 2 anos': 2,
        'Bronquiolitis en menores de 2 años': 2,
        'Bronquiolitis en menores de 2 años (sin especificar)': 2,
        'Enfermedad tipo influenza (ETI)': 3,
        'Neumonia': 1,
        'Neumonía': 1,
        'Neumonía (sin especificar)': 1
    },

    'provincia_id': {
        6: 1,
        2: 2,
        10: 3,
        22: 4,
        26: 5,
        14: 6,
        18: 7,
        30: 8,
        34: 9,
        38: 10,
        42: 11,
        46: 12,
        50: 13,
        54: 14,
        58: 15,
        62: 16,
        66: 17,
        70: 18,
        74: 19,
        78: 20,
        82: 21,
        86: 22,
        94: 23,
        90: 24
    }
}


# Aplica las asignaciones
for column, mapping in assignment_mapping.items():
    combined_data[column] = combined_data[column].map(mapping)

combined_data.fillna(0, inplace=True)

#Sumamos todos los casos que cumplan: misma provincia, año, grupo de edad, tipo de enfermedad, semanas epidemiologicas

for index, row in combined_data.iterrows():
    resultSum = combined_data.loc[(combined_data['provincia_id'] == row['provincia_id'])  & (combined_data['grupo_edad_id'] == row['grupo_edad_id']) & (combined_data['año'] == row['año'])
                   & (combined_data['semanas_epidemiologicas'] == row['semanas_epidemiologicas']) & (combined_data['evento_nombre'] == row['evento_nombre']), 'cantidad_casos'].sum()
    combined_data.at[index,'cantidad_casos'] = resultSum

combined_data.drop_duplicates(subset=['provincia_id', 'año', 'semanas_epidemiologicas', 'evento_nombre', 'grupo_edad_id'], keep='first', inplace=True)

#Eliminamos las columnas que no se van a utilizar
columns_to_drop = ['departamento_id', 'departamento_nombre', 'provincia_nombre', 'semanas_epidemiologicas', 'departamento_nombre', 'grupo_edad_desc']
combined_data = combined_data.drop(columns=columns_to_drop)
combined_data

#Calculos para ver la cantidad optima de clusters

wcss=[]
for i in range(2,10):
  kmeans = KMeans(i, n_init=100)
  kmeans.fit(combined_data)
  wcss_iter = kmeans.inertia_
  wcss.append(wcss_iter)

number_clusters = range(2,10)
plt.plot(number_clusters, wcss, marker='*', markersize=10, color='green')
plt.title('Número optimo de clusters')
plt.xlabel('Número de clusters')
plt.ylabel('WCSS')

from sklearn.metrics import silhouette_samples, silhouette_score

silhouette_scores = []

for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, n_init=100, random_state=0)
    cluster_labels = kmeans.fit_predict(combined_data)

    silhouette_avg = silhouette_score(combined_data, cluster_labels)
    silhouette_scores.append(silhouette_avg)


    # Calcular las puntuaciones de silueta para cada muestra
    sample_silhouette_values = silhouette_samples(combined_data, cluster_labels)

plt.figure(figsize=(8, 6))
plt.plot(range(2, 10), silhouette_scores,  marker='*', markersize=10, color='green')
plt.xlabel('Número de Clusters')
plt.ylabel('Puntuación de Silueta Promedio')
plt.title('Análisis de Siluetas')
plt.grid(True)
plt.show()

# Aplicamos K-Means para clasificar las regiones en grupos
kmeans = KMeans(n_clusters=3, n_init=100, random_state=0).fit(combined_data)

# Asigna un color a cada región en base a los clusters
combined_data['Cluster'] = kmeans.predict(combined_data)

# Reducción de dimensionalidad con t-SNE
tsne = TSNE(n_components=2, random_state=0, perplexity=30)
tsne_coordinates = tsne.fit_transform(combined_data)
combined_data['tsne_x'] = tsne_coordinates[:, 0]
combined_data['tsne_y'] = tsne_coordinates[:, 1]

# Generación de colores para los clusters
cluster_colors = plt.cm.tab10.colors
plt.figure(figsize=(12, 8))
unique_clusters = np.unique(kmeans.labels_)
for cluster in unique_clusters:
    cluster_data = combined_data[combined_data['Cluster'] == cluster]
    plt.scatter(cluster_data['tsne_x'], cluster_data['tsne_y'],
                label=f'Cluster {cluster}', alpha=0.7, s=50)

legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor=f'C{cluster}', markersize=10, label=f'Cluster {cluster}') for cluster in unique_clusters]

# Coloca la leyenda al costado del gráfico
plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.05, 1))

plt.title('Clustering con K-Means (' + str(kmeans.n_clusters) +' clústers) y t-SNE ( '+ str(tsne.perplexity) + ' de perplejidad) de Regiones y provincias')
plt.xlabel('t-SNE x')
plt.ylabel('t-SNE y')
plt.show()


# Crea un gráfico de distribución de provincias para cada cluster
unique_clusters = np.unique(kmeans.labels_)
for cluster in unique_clusters:
    # Filtramos la tabla por cada cluster
    cluster_data = combined_data[combined_data['Cluster'] == cluster]
    # Obtenemos un array con la cantidad de veces que se tiene esa provincia en el cluster
    province_counts = cluster_data['provincia_id'].value_counts()

    # Recorremos las filas de la tabla filtrada por clusters
    for index, row in cluster_data.iterrows():
      # Sumamos el resultado de la cantidad de casos, de cada provincia
      resultSum = cluster_data.loc[(cluster_data['provincia_id'] == row['provincia_id']), 'cantidad_casos'].sum()
      # Reemplazamos la cantidad de casos de la row actual, con la sumatoria de todos los casos
      cluster_data.at[index,'cantidad_casos'] = resultSum

    # Borramos todos las filas que tienen provincia repetida y dejamos la primera que tiene la sumatoria correcta
    cluster_data.drop_duplicates(subset=['provincia_id'], keep='first', inplace=True)

    # Hacemos que nuestro id sea la provincia_id
    cluster_data.set_index('provincia_id', inplace=True)
    # Creamos un array la cantidad de casos y (con lo anterior dejamos la provincia_id como el id)
    cluster_data_filter = cluster_data['cantidad_casos']

    plt.figure(figsize=(10, 6))
    cluster_data_filter.plot(kind='bar', color='blue', alpha=0.7)

    plt.title(f'Distribución de provincias en Cluster {cluster}')
    plt.xlabel('Provincia')
    plt.ylabel('Cantidad de casos')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)

    plt.show()