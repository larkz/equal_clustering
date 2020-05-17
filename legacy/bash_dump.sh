awk '
/^MeanModel/ {++count; file="file"count".txt"; print file}
file {print line > file}
{line=$0}
' full-elki-nosamp.txt