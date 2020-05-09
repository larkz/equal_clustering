import pickle as pkl
import numpy as np
from equal_clustering_prep_elki import *
from get_mse import *
import sys

n_clus = 5
elki_result_obj = elki_cluster_obj(int(n_clus))

k = elki_result_obj.k
n_eq = elki_result_obj.n_eq
coords = elki_result_obj.coords

########### MSE Pre MIP - ELKI only

raw_ass = elki_result_obj.raw_data[:, 3][0:int(n_clus * k) ]

# uni_raw_ass = np.linspace(0, n_clus-1, num=n_clus).astype(int)
uni_raw_ass = np.unique(raw_ass)

clus_dic_elki = {}
for c in uni_raw_ass:
    inds = np.argwhere(raw_ass == c).reshape(-1)
    filt = coords[inds]
    clus_dic_elki[c] = np.mean(filt[:, 0:2], 0 )

num_wp = coords.shape[0]
depot_pts = np.zeros([num_wp, 2])

for i in range(0, num_wp):
    depot_pts[i, :] = clus_dic_elki[raw_ass[i]]

valid_coords = ass_arr_v3[:, 0:2]
pows = np.power(depot_pts - coords, 2)
se = pows[:,0] + pows[:,1]

mse = np.mean(se)
print(mse)


############# MIP post ELKI


ass = pkl.load(open("or_tools_output/ass_mip_elki_" + str(int(n_clus)) + ".pkl", "rb" ))
ass_arr = np.array(ass)

ass_arr_v2 = np.zeros([coords.shape[0], 3])

for i in range(ass_arr.shape[0]):
    index = int(ass_arr[i, 1])
    ass = int(ass_arr[i, 0])
    ass_arr_v2[index, 0] = coords[index, 0]
    ass_arr_v2[index, 1] = coords[index, 1]
    ass_arr_v2[index, 2] = ass

# ass_arr_v3 = ass_arr_v2[ass_arr_v2[:, 0] != 0 ]
ass_arr_v3 = ass_arr_v2

num_wp = ass_arr_v3.shape[0]
depot_pts = np.zeros([num_wp, 2])

n_clus = np.unique(ass_arr_v3[:, 2])

clus_dic = {}

for c in range(len(n_clus)):
    filt = ass_arr_v3[ass_arr_v3[:, 2] == c]
    clus_dic[c] = np.mean(filt[:, 0:2], 0 )

for i in range(0, num_wp):
    depot_pts[i, :] = clus_dic[ int(ass_arr_v3[i,2])] 

valid_coords = ass_arr_v3[:, 0:2]
pows = np.power(depot_pts - valid_coords, 2)
se = pows[:,0] + pows[:,1]

mse = np.mean(se)
print(mse)

##########

import numpy as np
import matplotlib.pyplot as plt

elki_cents = np.array([i for i in clus_dic_elki.values()])
mip_cents = np.array([i for i in clus_dic.values()])

plt.scatter(coords[:, 0], coords[:, 1], marker='^')
plt.scatter(elki_cents[:, 0], elki_cents[:, 1], marker='o')
plt.scatter(mip_cents[:, 0], mip_cents[:, 1], marker='x')


plt.show()









### 

# Fixing random state for reproducibility
np.random.seed(19680801)

N = 100
r0 = 0.6
x = 0.9 * np.random.rand(N)
y = 0.9 * np.random.rand(N)
area = (20 * np.random.rand(N))**2  # 0 to 10 point radii
c = np.sqrt(area)
r = np.sqrt(x ** 2 + y ** 2)
area1 = np.ma.masked_where(r < r0, area)
area2 = np.ma.masked_where(r >= r0, area)
plt.scatter(x, y, s=area1, marker='^', c=c)
plt.scatter(x, y, s=area2, marker='o', c=c)
# Show the boundary between the regions:
theta = np.arange(0, np.pi / 2, 0.01)
plt.plot(r0 * np.cos(theta), r0 * np.sin(theta))

