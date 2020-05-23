filename=$1
k=$2

mkdir elki_output/$filename/$filename-k$k
start=$SECONDS
java -jar elki/elki-bundle-0.7.6-SNAPSHOT.jar KDDCLIApplication -dbc.in datasets/LL/$filename-ll.csv -algorithm tutorial.clustering.SameSizeKMeansAlgorithm -kmeans.k $k > elki_output/$filename/$filename-k$k/full-elki-nosamp.txt
end=$SECONDS

duration=$(( end - start ))

cd elki_output/$filename/$filename-k$k

csplit -k full-elki-nosamp.txt /MeanModel/ {1000}
rm xx00

for ((i=1; i <= k; i++ )); 
do
    d="$(($i-1))"
    n=$(printf %02d $i)
    echo cating file: $n
    mv xx$n clusterizer_$d.csv;
    cat clusterizer_$d.csv | sed '/^#/ d' | sed 's/$/ cluster_'$d'/' > clusterize_$d.csv;
    rm clusterizer_$d.csv
done

rm clusterized.csv
cat clusterize* >> clusterized.csv

echo Duration: $duration seconds
cd ../../..
echo $k,$(printf $duration%03d),all,elki >> runtimes/$filename.txt
