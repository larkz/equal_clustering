import pickle as pkl
import numpy as np
from equal_clustering_prep_elki import *
from get_mse import *
import sys
# import geopandas
# import geoplot
from mpl_toolkits.basemap import Basemap


n_clus = sys.argv[1]
# fac = sys.argv[2]
file_id = sys.argv[2]
samp_size = sys.argv[3]
to_plot = sys.argv[4]

elki_result_obj = elki_cluster_obj(int(n_clus), file_id)

k = elki_result_obj.k
n_eq = elki_result_obj.n_eq
coords = elki_result_obj.coords
raw_coords = elki_result_obj.raw_coords

########### MSE Pre MIP - ELKI only

raw_ass = elki_result_obj.raw_data
raw_ass = raw_ass[0:(int(n_clus) * int(k)), 3]

print(elki_result_obj.raw_data[0:int(n_clus * k)].shape)
print(raw_ass.shape)
print(n_clus)
print(k)

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

pows = np.power(depot_pts - coords, 2)
se = pows[:,0] + pows[:,1]

elki_mse = np.mean(se)

print(elki_mse)

'''

############# MIP post ELKI

ass = pkl.load(open("or_tools_output/ass_mip_elki_" + str(n_clus) + "relax_" + str(fac) + ".pkl", "rb" ))
ass_arr = np.array(ass)[0:(int(n_clus) * int(k)) ]

max_ind = np.max(ass_arr[:, 1])
print(max_ind)
ass_arr_v2 = np.zeros([max_ind + 1, 3]) - 1
print(ass_arr_v2.shape)

for i in range(ass_arr.shape[0]):
    index = int(ass_arr[i, 1])
    ass = int(ass_arr[i, 0])
    ass_arr_v2[index, 0] = raw_coords[index, 0]
    ass_arr_v2[index, 1] = raw_coords[index, 1]
    ass_arr_v2[index, 2] = ass

print("num of unique wp: ")
print(len(np.unique(ass_arr[:, 1])))

# ass_arr_v3 = ass_arr_v2[ass_arr_v2[:, 0] != 0 ]
inds = np.argwhere(ass_arr_v2[:, 2] > -1).reshape(-1)
ass_arr_v3 = ass_arr_v2[inds]

num_wp = ass_arr_v3.shape[0]
depot_pts = np.zeros([num_wp, 2])

n_clus_arr = np.unique(ass_arr_v3[:, 2])

clus_dic = {}

for c in range(len(n_clus_arr)):
    filt = ass_arr_v3[ass_arr_v3[:, 2] == c]
    clus_dic[c] = np.mean(filt[:, 0:2], 0 )

for i in range(0, num_wp):
    depot_pts[i, :] = clus_dic[ int(ass_arr_v3[i,2])] 

valid_coords = ass_arr_v3[:, 0:2]
pows = np.power(depot_pts - valid_coords, 2)
se = pows[:,0] + pows[:,1]

mse = np.mean(se)
print(mse)
'''

########### MSE ELKI Sample

elki_result_obj = elki_cluster_obj_samp(int(n_clus), file_id, int(samp_size) )

k = elki_result_obj.k
n_eq = elki_result_obj.n_eq
coords = elki_result_obj.coords
raw_coords = elki_result_obj.raw_coords


########### MSE ELKI Sample Sol + MIP 

ass = pkl.load(open("or_tools_output/ass_mip_elki_" + str(n_clus) + ".pkl", "rb" ))
ass_arr = np.array(ass)[0:(int(n_clus) * int(k)) ]

max_ind = np.max(ass_arr[:, 1])
print(max_ind)
ass_arr_v2 = np.zeros([max_ind + 1, 3]) - 1
print(ass_arr_v2.shape)

for i in range(ass_arr.shape[0]):
    index = int(ass_arr[i, 1])
    ass = int(ass_arr[i, 0])
    ass_arr_v2[index, 0] = raw_coords[index, 0]
    ass_arr_v2[index, 1] = raw_coords[index, 1]
    ass_arr_v2[index, 2] = ass

print("num of unique wp: ")
print(len(np.unique(ass_arr[:, 1])))

# ass_arr_v3 = ass_arr_v2[ass_arr_v2[:, 0] != 0 ]
inds = np.argwhere(ass_arr_v2[:, 2] > -1).reshape(-1)
ass_arr_v3 = ass_arr_v2[inds]

num_wp = ass_arr_v3.shape[0]
depot_pts = np.zeros([num_wp, 2])

n_clus_arr = np.unique(ass_arr_v3[:, 2])

clus_dic_samp = {}

for c in range(len(n_clus_arr)):
    filt = ass_arr_v3[ass_arr_v3[:, 2] == c]
    clus_dic_samp[c] = np.mean(filt[:, 0:2], 0 )

for i in range(0, num_wp):
    depot_pts[i, :] = clus_dic_samp[ int(ass_arr_v3[i,2])] 

valid_coords = ass_arr_v3[:, 0:2]
pows = np.power(depot_pts - valid_coords, 2)
se = pows[:,0] + pows[:,1]

mse = np.mean(se)
print(mse)


##########

if int(to_plot):
    import matplotlib.pyplot as plt
    # plt.ion()

    elki_cents = np.array([i for i in clus_dic_elki.values()])
    # mip_cents = np.array([i for i in clus_dic.values()])
    mip_samp_cents = np.array([i for i in clus_dic_samp.values()])

    # m = Basemap(width=12000000,height=9000000,projection='lcc',
    #     resolution='c',lat_1=45.,lat_2=55,lon_0=-50,lat_0=60)
    m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
    m.drawcoastlines()

    sc_fac = 1
    coords_x, coords_y = m(coords[:, 0] * sc_fac, coords[:, 1] * sc_fac)
    ek_x, ek_y = m(elki_cents[:, 0] * sc_fac, elki_cents[:, 1] * sc_fac)

    m.scatter(coords_x, coords_y, marker='^')
    m.scatter(ek_x, ek_y, marker='o')
    # plt.scatter(mip_cents[:, 0], mip_cents[:, 1], marker='x')
    m.scatter(mip_samp_cents[:, 0], mip_samp_cents[:, 1], marker='+')
    plt.show()

    # Create assignment plot, for all points,

    m2 = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
    m2.drawcoastlines()

    print(ass_arr_v3)

    coords_x_ass, coords_y_ass = m2(ass_arr_v3[:, 0], ass_arr_v3[:, 1])
    m2.scatter(coords_x_ass, coords_y_ass, c=ass_arr_v3[:, 2], marker='^')
    plt.show()
    




with open( "error_metrics/" + str(file_id) + ".txt", "a") as f:
    f.write( str(n_clus) + "," + str(samp_size) + "," + str(elki_mse) + "," + str(mse) + "\n" )




