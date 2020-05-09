from get_mse import *
import sys
import csv
from progress.bar import IncrementalBar

# set_name = "car-sharing-9999"
set_name = str(sys.argv[1])

if __name__ == "__main__":
    f = open('summary_output/' + set_name + '_summary.csv', 'w')
    writer = csv.writer(f)

    kmax = 7
    kstart = 2
    bar = IncrementalBar('Countdown', max = kmax - 1 )
    
    for k in range(kstart, kmax + 1):
        filename = 'elki_output/' + str(set_name) + '/' + str(set_name) + '-k' + str(k) + '/clusterized.csv'
        reader = csv.reader(open(filename, "r"), delimiter=" ")
        x = list(reader)
        raw_data = np.array(x).astype(str)
        kmse = get_avg_mse_all_grp(raw_data)    

        row = [k, kmse]
        writer.writerow(row)
        bar.next()

    bar.finish()
    
    f.close()

