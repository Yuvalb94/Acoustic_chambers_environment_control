#!/bin/bash
 
echo "Hello! this is the Bash startup script for our Arduino controller"
 
# Get the path we're currently at 
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
 
# Build the full path name of our file
py_script_name="$parent_path/control_main.py --config=/home/cohenlab/acoustic_chamber_environment_control/config_files/config_1.yaml"
echo $py_script_name
 
while true; do
	echo "Launching the Python script"
	lxterminal -e "python $py_script_name" # Launch a new terminal with our script
 
	echo "Waiting for the Python script to finish before launching a new one"
	sleep 2 # Wait a bit so we're sure the process was launched 
 
	PID=$(pgrep -f control_main.py) # Find the process name
	echo "Waiting for process $PID"
	while [ -d /proc/$PID ]; do
		sleep 1
	done
done
