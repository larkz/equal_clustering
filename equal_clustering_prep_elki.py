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
from numpy.core.defchararray import find, lower


csv.field_size_limit(sys.maxsize)


# df_raw = pd.read_csv('datasets/sb_locs.csv', header = 0)[['Longitude','Latitude']].dropna()

class elki_cluster_obj:
    def __init__(self, num_clus, file_id):

        filename = 'elki_output/' + file_id + '/' + file_id + '-k' + str(num_clus) + '/clusterized.csv'
        reader = csv.reader(open(filename, "r"), delimiter=" ")
        x = list(reader)
        self.raw_data = np.array(x).astype(str)
        raw_data = self.raw_data
        self.num_clus = num_clus
        
        k = int(len(raw_data)/num_clus - (len(raw_data) % num_clus) )
        print(k)
        self.k = k
        
        self.n_eq = (len(raw_data) - (len(raw_data) % k))/k
        # self.df = raw_data.head(len(raw_data) - (len(raw_data) % k))
        # Take a dividible number
        self.coords = self.raw_data[:, 1:3].astype(float)[0:int(self.n_eq * k)]
        self.raw_coords = self.raw_data[:, 1:3].astype(float)
        
        self.cluster_centers = get_all_centroids(raw_data)
        self.dist_mat = euclidean_distances(self.coords, self.cluster_centers)

class elki_cluster_obj_samp:
    def __init__(self, num_clus, file_id, samp_size):

        filename = 'elki_output/' + file_id + '/' + file_id + '-k' + str(num_clus) + '-samp' + str(samp_size) + '/elki-clusters.txt'
        reader = csv.reader(open(filename, "r"), delimiter=",")
        x = list(reader)
        self.cluster_centers = np.array(x).astype(str)
        self.num_clus = num_clus
        
        filename_full = 'elki_output/' + file_id + '/' + file_id + '-k' + str(num_clus) + '/full-elki-nosamp.txt'
        print(filename_full)
        # self.full_data = np.array(list(csv.reader(open(filename_full, "r"), delimiter="\n"))).astype(str)

        raw_data_ingest = np.array(list(csv.reader(open(filename_full, "r"), delimiter="\n")))
        raw_data_str = raw_data_ingest[find(raw_data_ingest, 'ID') != -1]

        split_str = lambda x: x.split(" ")
        self.full_data = np.array(list(map(split_str, raw_data_str)))

        k = int(len(self.full_data)/num_clus - (len(self.full_data) % num_clus) )
        print(k)
        self.k = k
        self.n_eq = (len(self.full_data) - (len(self.full_data) % k))/k

        self.coords = self.full_data[:, 1:3].astype(float)[0:int(self.n_eq * k)]
        self.raw_coords = self.full_data[:, 1:3].astype(float)        
        
        self.dist_mat = euclidean_distances(self.coords, self.cluster_centers)
        

# https://stackoverflow.com/questions/17289032/solving-a-linear-program-in-case-of-an-equality-constraint
# adding an equality constraint





