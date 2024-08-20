#!/bin/bash
base_path="/home/tom/Desktop/Cage1_singing_trials"
base_server_path="/mnt/STORWIS/cohenlab/test_copy_from_raspb"
 
# When we perform our daily copy, we'll do it for the day of `today - N`. This defines `N`.
n_days_back=15
# Calculate the day we want to perform the copy for -
copy_date=$(date --date="$n_days_back days ago" +"%Y%m%d")
 
files_for_copy_path=$base_path/cage_*_"$copy_date"_*.csv
echo "Copying files from $files_for_copy_path"
 
destination_dir_name=$base_server_path/data_from_$copy_date
mkdir -p $destination_dir_name
 
echo "Files will be copied to $destination_dir_name"
 
cp $files_for_copy_path $destination_dir_name
 
echo "Done copying!"