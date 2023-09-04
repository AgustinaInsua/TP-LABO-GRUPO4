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
def consultar_riesgo_de_enfermarse(provincia_id_user, grupo_edad_id_user, evento_id_user, provincia_nombre_user, evento_nombre_user):
  data_for_this_user = combined_data.loc[(combined_data['provincia_id'] == provincia_id_user) & (combined_data['grupo_edad_id'] == grupo_edad_id_user) & (combined_data['evento_nombre'] == evento_id_user)]
  cant_casos_pais_con_evento_id_user = combined_data.loc[(combined_data['grupo_edad_id'] == grupo_edad_id_user) & (combined_data['evento_nombre'] == evento_id_user), 'cantidad_casos'].sum()

  string_return = ""
  if data_for_this_user.empty:
    string_return = "No hay información para los datos ingresados."
  else:
    for index, row in data_for_this_user.iterrows():
      if row.cluster == 0:
        string_return = "Prioridad baja. \n"
      else:
        string_return = "Prioridad alta. \n"
      porcentaje_enfermos = row['cantidad_casos'] * 100 // cant_casos_pais_con_evento_id_user
      string_return = string_return + "\n" + "Probabilidad de enfermarse de " + str(evento_nombre_user) + " en " + str(provincia_nombre_user) + ": " + str(porcentaje_enfermos) + "%"
      break
  return string_return

provincias_a_ids = {
    'Buenos Aires': 1,
    'CABA': 2,
    'Catamarca':3,
    'Chaco': 4,    
    'Chubut': 5,   
    'Córdoba': 6,
    'Corrientes': 7,
    'Entre Ríos':8,
    'Formosa': 9,
    'Jujuy': 10,
    'La Pampa': 11,
    'La Rioja': 12,
    'Mendoza': 13,
    'Misiones': 14,
    'Neuquén': 15,
    'Río Negro': 16,
    'Salta': 17,
    'San Juan': 18,
    'San Luis': 19,
    'Santa Cruz': 20,
    'Santa Fe': 21,
    'Santiago del Estero': 22,
    'Tierra del Fuego': 23,
    'Tucumán': 24
}

# Función para mapear el nombre de la provincia a su ID
def mapear_provincia_a_id(nombre_provincia):
    # Buscar el nombre de la provincia en el diccionario y retornar su ID ---- Si la provincia no está en el diccionario, se retorna -1
    return provincias_a_ids.get(nombre_provincia, -1)

enfermedades_a_ids = {
        'Bronquiolitis en menores de 2 años': 2,
        'Enfermedad tipo influenza (ETI)': 3,
        'Neumonía': 1,
    }

# Función para mapear el nombre de la enfermedad a su ID
def mapear_enfermedad_a_id(nombre_enfermedad):
    
    return enfermedades_a_ids.get(nombre_enfermedad, -1)

