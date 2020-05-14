

cat datasets/sample_table.csv | cut -d "," -f 2- | cut -d "," -f -2 > car-sharing-ll.csv

head 100 datasets/car-sharing-ll.csv > datasets/car-sharing-ll-100.csv

