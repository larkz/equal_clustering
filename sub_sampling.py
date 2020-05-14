import csv
import sys
import pandas as pd 
import numpy as np

set_name = sys.argv[1]
# set_name = 'starbucks'

filename = 'datasets/LL/' + str(set_name) + '-ll.csv'
reader = csv.reader(open(filename, "r"), delimiter=",")

full_data = np.array(list(reader)).astype(float)

inds = np.arange(full_data.shape[0]-1)
inds_samp = np.random.choice(inds, 1000, replace = False)

samp_data = full_data[inds_samp]

filename_out = 'datasets/LL/' + str(set_name) + '-1000-ll.csv'

pd.DataFrame(samp_data).to_csv(filename_out, header=None, index=None)



