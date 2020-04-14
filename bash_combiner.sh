cd elki_output/ny-wifi/ny-wifi-k6
for i in {0..5}
do
    cat cluster_$i* | sed '/^#/ d' | sed 's/$/ cluster_'$i'/' > clusterize_$i.csv
done

cat clusterize* > clusterized.csv
cd ..
