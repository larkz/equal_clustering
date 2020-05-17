filename=$1
k=$2
samp_size=$3

for ((i=2; i <= k; i++ )); 
do
    sh bash_pipeline.sh $filename $i $samp_size;
    echo cluster_$i;
done