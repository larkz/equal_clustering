filename=$1
k=$2

python3 sub_sampling.py $filename

mkdir elki_output/$filename/$filename-k$k-samp1000
java -jar elki/elki-bundle-0.7.6-SNAPSHOT.jar KDDCLIApplication -dbc.in datasets/LL/$filename-1000-ll.csv -algorithm tutorial.clustering.SameSizeKMeansAlgorithm -kmeans.k $k > elki_output/$filename/$filename-k$k-samp1000/full-elki.txt
