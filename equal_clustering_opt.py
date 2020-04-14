import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
from ortools.graph import pywrapgraph

# df_raw = pd.read_csv('iris.txt', header = None).rename(columns={0: "sl", 1: "sw", 2: "X", 3: "Y", 4: "class" })

df_raw = pd.read_csv('datasets/sb_locs.csv', header = 0)[['Longitude','Latitude']].dropna().head(1600)

k = 7
n_eq = (len(df_raw) - (len(df_raw) % k))/k
df = df_raw.head(len(df_raw) - (len(df_raw) % k))

# Take a dividible number

kmeans = KMeans(n_clusters=len(df)//k)
coords = df_raw[['Longitude','Latitude']].dropna().values
kmeans.fit(coords)
cluster_centers = kmeans.cluster_centers_
dist_mat = euclidean_distances(coords, cluster_centers)

# https://stackoverflow.com/questions/17289032/solving-a-linear-program-in-case-of-an-equality-constraint
# adding an equality constraint