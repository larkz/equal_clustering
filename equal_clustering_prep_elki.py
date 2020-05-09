import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
from ortools.graph import pywrapgraph
from get_mse import *
import sys
import csv

# df_raw = pd.read_csv('datasets/sb_locs.csv', header = 0)[['Longitude','Latitude']].dropna()

class elki_cluster_obj:
    def __init__(self, num_clus):

        filename = 'elki_output/starbucks/starbucks-k' + str(num_clus) + '/clusterized.csv'
        reader = csv.reader(open(filename, "r"), delimiter=" ")
        x = list(reader)
        self.raw_data = np.array(x).astype(str)
        raw_data = self.raw_data
        self.num_clus = num_clus
        
        k = int(len(raw_data)/num_clus)
        print(k)
        self.k = k
        
        self.n_eq = (len(raw_data) - (len(raw_data) % k))/k
        # self.df = raw_data.head(len(raw_data) - (len(raw_data) % k))
        # Take a dividible number
        self.coords = self.raw_data[:, 1:3].astype(float)[0:int(self.n_eq * k)]
        
        self.cluster_centers = get_all_centroids(raw_data)
        self.dist_mat = euclidean_distances(self.coords, self.cluster_centers)


# https://stackoverflow.com/questions/17289032/solving-a-linear-program-in-case-of-an-equality-constraint
# adding an equality constraint





