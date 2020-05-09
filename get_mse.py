import numpy as np
import csv

filename = 'elki_output/starbucks/starbucks-k7/clusterized.csv'
reader = csv.reader(open(filename, "r"), delimiter=" ")
x = list(reader)
raw_data = np.array(x).astype(str)

# Requires ingesting the stuff the clusterized file, and re-computing the mse, erroneous right now

def get_avg_mse_all_grp(raw_data):
    clus = np.unique(raw_data[:, 3])
    nc = len(clus)
    mse = np.zeros(nc)
    for c in range(nc):
        clus_data = raw_data[raw_data[:, 3] == clus[c]][:,1:3].astype(float)
        mse[c] = get_mse(clus_data)
    return np.sum(mse)/nc

def get_avg_mse_all_grp_goog(raw_data):
    clus = np.unique(raw_data[:, 2])
    nc = len(clus)
    mse = np.zeros(nc)
    for c in range(nc):
        clus_data = raw_data[raw_data[:, 2] == clus[c]][:,0:2].astype(float)
        mse[c] = get_mse(clus_data)
    return np.sum(mse)/nc

def get_mse(clus_data):
    cent = np.mean(clus_data, 0)
    pows = np.power(clus_data - cent, 2)
    sqerr = pows[:,0] + pows[:,1]
    mse = np.mean(sqerr)
    return mse

def get_all_centroids(raw_data):
    clus = np.unique(raw_data[:, 3])
    nc = len(clus)
    cents = np.zeros([nc, 2])
    for c in range(nc):
        clus_data = raw_data[raw_data[:, 3] == clus[c]][:,1:3].astype(float)
        cents[c] = np.mean(clus_data)
    return cents

def get_centroids(clus_data):
    cent = np.mean(clus_data, 0)
    pows = np.power(clus_data - cent, 2)
    sqerr = pows[:,0] + pows[:,1]
    mse = np.mean(sqerr)
    return mse

if __name__ == "__main__":
    print(raw_data)
    print(get_avg_mse_all_grp(raw_data))


