import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
from ortools.graph import pywrapgraph
import pickle as pkl

# df_raw = pd.read_csv('iris.txt', header = None).rename(columns={0: "sl", 1: "sw", 2: "X", 3: "Y", 4: "class" })

df_raw = pd.read_csv('datasets/sb_locs.csv', header = 0)[['Longitude','Latitude']].dropna() # .head(1600)

k = 3200
n_eq = (len(df_raw) - (len(df_raw) % k))/k
df = df_raw.head(len(df_raw) - (len(df_raw) % k))

# Take a dividible number

kmeans = KMeans(n_clusters=len(df)//k)
coords = df_raw[['Longitude','Latitude']].dropna().values
kmeans.fit(coords)
cluster_centers = kmeans.cluster_centers_
dist_mat = euclidean_distances(coords, cluster_centers)
cost = np.tile(dist_mat, (1, k)) # the repetition here is inefficient

wp_len = len(cost)
batch_len = len(cost[0])
assignment = pywrapgraph.LinearSumAssignment()
for wp in range(wp_len):
    for batch in range(batch_len):
        if cost[wp][batch]:
            assignment.AddArcWithCost(wp, batch, int(cost[wp][batch]))

solve_status = assignment.Solve()

batch_ids = np.zeros(wp_len)

if solve_status == assignment.OPTIMAL:
    for i in range(0, assignment.NumNodes()):
        batch_ids[i] = assignment.RightMate(i)%(batch_len//k) + 1

print(batch_ids)

with open('or_tools_output/batch_ids.pkl', 'wb') as file_io:
    pkl.dump(batch_ids, file_io)



'''
elif solve_status == assignment.INFEASIBLE:
    print('No assignment is possible.')
    return False
elif solve_status == assignment.POSSIBLE_OVERFLOW:
    print('Some input costs are too large and may cause an integer overflow.')
    return False
'''


