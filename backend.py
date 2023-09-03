import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.preprocessing import LabelEncoder
from scipy.spatial import ConvexHull
from scipy.spatial import QhullError

## Metodo para cargar los datos?
# Cargar y procesar los datos
combined_data = pd.read_csv('https://github.com/AgustinaInsua/TP-LABO-GRUPO4/raw/main/archivofiltrado.csv')

for index, row in combined_data.iterrows():
    resultSum = combined_data.loc[(combined_data['provincia_id'] == row['provincia_id'])  & (combined_data['grupo_edad_id'] == row['grupo_edad_id'])
                   & (combined_data['evento_nombre'] == row['evento_nombre']), 'cantidad_casos'].sum()
    combined_data.at[index,'cantidad_casos'] = resultSum

combined_data.drop_duplicates(subset=['provincia_id',  'evento_nombre', 'grupo_edad_id'], keep='first', inplace=True)

columns_to_drop = ['departamento_id', 'departamento_nombre', 'provincia_nombre', 'grupo_edad_desc','semanas_epidemiologicas']
combined_data = combined_data.drop(columns=columns_to_drop)


## Este lo borraria
"""wcss=[]
K = range(1, 10)
for num_clusters in K:
  kmeans = KMeans(n_clusters=num_clusters, n_init = 100)
  kmeans.fit(combined_data)
  wcss.append(kmeans.inertia_)

plt.plot(K, wcss, marker='*', markersize=10, color='green')
plt.title('Número optimo de clusters')
plt.xlabel('Número de clusters')
plt.ylabel('WCSS')
"""

##Metodo de calculo optimo de clusters
from sklearn.metrics import silhouette_samples, silhouette_score

silhouette_scores = []

for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, n_init=100, random_state=0)
    cluster_labels = kmeans.fit_predict(combined_data)

    silhouette_avg = silhouette_score(combined_data, cluster_labels)
    silhouette_scores.append(silhouette_avg)

# Obtenemos el maximo valor de la lista y con eso obtemos la cantidad de clusters que usaremos
max_value_silhouette_scores = max(silhouette_scores)
cant_clusters_to_use = silhouette_scores.index(max_value_silhouette_scores) + 2

## Metodo kmeanscontsne
# Aplicamos K-Means para clasificar las regiones en grupos
kmeans = KMeans(n_clusters=cant_clusters_to_use, n_init=100, random_state=0).fit(combined_data)
combined_data['cluster'] = kmeans.predict(combined_data)

# Reducción de dimensionalidad con t-SNE
tsne = TSNE(n_components=2, random_state=0, perplexity=50, n_iter = 5000)
tsne_coordinates = tsne.fit_transform(combined_data)
combined_data['tsne_x'] = tsne_coordinates[:, 0]
combined_data['tsne_y'] = tsne_coordinates[:, 1]


# Suponemos que el usuario ingreso provincia_id,  grupo_edad_id y evento
def consultar_riesgo_de_enfermarse(provincia_id_user, grupo_edad_id_user, evento_nombre_user):
  data_for_this_user = combined_data.loc[(combined_data['provincia_id'] == provincia_id_user) & (combined_data['grupo_edad_id'] == grupo_edad_id_user) & (combined_data['evento_nombre'] == evento_nombre_user)]
  cant_casos_pais_con_evento_nombre_user = combined_data.loc[(combined_data['grupo_edad_id'] == grupo_edad_id_user) & (combined_data['evento_nombre'] == evento_nombre_user), 'cantidad_casos'].sum()

  string_return = ""
  if data_for_this_user.empty:
    string_return = "No hay información para los datos ingresados."
  else:
    for index, row in data_for_this_user.iterrows():
      if row.cluster == 0:
        string_return = "El riesgo de enfermarse es bajo. \n"
      else:
        string_return = "El riesgo de enfermarse es alto. \n"
      porcentaje_enfermos = row['cantidad_casos'] * 100 // cant_casos_pais_con_evento_nombre_user
      string_return = string_return + "Porcentaje de enfermarse en la provincia: " + str(porcentaje_enfermos) + "%"
      break
  return string_return

