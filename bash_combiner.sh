k=$1;
filename=$2

cd elki_output/$filename/$filename-k$k
echo elki_output/$filename/$filename-k$k
for ((i=0; i < k; i++ )); 
do
    cat cluster_$i* | sed '/^#/ d' | sed 's/$/ cluster_'$i'/' > clusterize_$i.csv;
    echo cluster_$i;
done

cat clusterize* > clusterized.csv

cd ..
