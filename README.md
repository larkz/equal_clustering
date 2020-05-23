# equal_clustering

## Creating a sub sample
python3 sub_sampling.py starbucks

## Running ELKI via GUI
In the ELKI jar folder, run:
java -jar elki-bundle-0.7.6-SNAPSHOT.jar

# Running ELKI directly into output file

java -jar elki-bundle-0.7.6-SNAPSHOT.jar KDDCLIApplication -dbc.in {csv_path} -algorithm tutorial.clustering.SameSizeKMeansAlgorithm -kmeans.k {num_clus} > {output_file}

# Massage some ELKI output
ELKI will directly output some junky files using the above method. We need some *nix commands to clean it up.

grep -E '# Cluster Mean: ' {output_file} > {corrected_file}

sed -i -e 's/# Cluster Mean: //g' {corrected_file}; rm {corrected_file}-e

# Mixed integer solver



# Bash pipeline can run the entire pipeline

Running `bash_pipeline.sh` with the approprite arguments.



# Compute the errors, write the file, get the times


