filename=$1
k=$2
samp_size=$3

for ((i=3; i <= k; i++ )); 
do
    # sh bash_pipeline.sh $filename $i $samp_size;
    # echo cluster_$i;
    python3 get_metrics.py  samp_size 0
done