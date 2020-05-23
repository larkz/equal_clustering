filename=$1
k=$2
samp_size=$3

python3 sub_sampling.py $filename

mkdir elki_output/$filename/$filename-k$k-samp$samp_size
java -jar elki/elki-bundle-0.7.6-SNAPSHOT.jar KDDCLIApplication -dbc.in datasets/LL/$filename-$samp_size-ll.csv -algorithm tutorial.clustering.SameSizeKMeansAlgorithm -kmeans.k $k > elki_output/$filename/$filename-k$k-samp$samp_size/full-elki.txt

grep -E '# Cluster Mean: ' elki_output/$filename/$filename-k$k-samp$samp_size/full-elki.txt > elki_output/$filename/$filename-k$k-samp$samp_size/elki-clusters.txt
sed -i -e 's/# Cluster Mean: //g' elki_output/$filename/$filename-k$k-samp$samp_size/elki-clusters.txt; rm elki_output/$filename/$filename-k$k-samp$samp_size/elki-clusters.txt-e

python3 mip_ass_sol_exact.py $k $filename $samp_size