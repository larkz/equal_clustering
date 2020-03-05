cd elki_output/starbucks/starbucks-k4
for i in {0..3}
do
    cat cluster_$i* | sed '/^#/ d' | sed 's/$/ cluster_'$i'/' > clusterize_$i.csv
done

cat clusterize* > clusterized.csv
cd ..
