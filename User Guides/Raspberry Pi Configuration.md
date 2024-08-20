# Setting up the Raspberry Pi
The Raspberry Pi is a minicomputer, on which we can run scripts that control our environmental system while also gathering important data. 
In order to use the Raspberry Pi for our purposes, we need to adjust some of its settings, install some files and libraries, and implement scripts that will run automatically when we want them to.

## Table of contents
1. [Installing the Raspberry Pi Operating system](#install-the-raspberry-pi-operating-system)
2. [Adding the Raspberry Pi to the WIS network](#adding-the-raspberry-pi-to-the-wis-network)
3. [Synchronizing the Raspberry Pi clock](#synchronizing-the-raspberry-pi-clock)
4. [Installing updates](#installing-updates)
5. [Mounting StorWis onto the Raspberry Pi](#mounting-storwis-onto-the-raspberry-pi)
6. [Acquiring neccesary files and libraries](#acquiring-neccesary-files-and-libraries)
7. [Manually running the script](#manually-running-the-script)
8. [Setting the script to run automatically when Raspberry Pi is turned on](#setting-the-script-to-run-automatically-when-raspberry-pi-is-turned-on)
9. [Copying data to the remote disk](#copying-data-to-the-remote-disk)

## Install the Raspberry Pi Operating system 
  Use [Raspberry Pi imager](https://www.raspberrypi.com/software/) to install the Rasraspberry pi OS (Legacy, 32 bit) operating system onto a compatible SD card.
  Set the user name to cohenlab and the password to the current lab user password.
  Now you can assemble the Raspberry Pi:  - insert the SD card in it's place, connect a keyboard, screen, mouse, ethernet, and power.

## Adding the Raspberry Pi to the WIS network
to connect to the Wis network and use storWis, we need to extract its MAC address and contact [Arthur Kalntarov](artur.kalantarov@weizmann.ac.il) to do that .
In terminal type:
```
ifconfig
```
Locate the MAC address in the first part of the text that opens (eth0). It is written after the word "ether" and has 6 pairs of characters separated by a colon(:).
Send it to Arthur and ask him to add it.
Once the Raspberry pi has been added, you will see on the top right corner of the screen next to the clock - two blue arrows pointing up and down, and it will display "eth0: configured".
Until this step is completed, you can continue with the following steps by connecting to the Wi-Fi, but you will not be able to connect to STORWIS, and the clock will not show the correct time (it's still OK to complete the steps in the sync clock procedure, but the clock might not show the exact time until you are connected to the network)

## Synchronizing the Raspberry Pi clock
  The Raspberry Pi clock uses the network to synchronize its clock. This is done by connecting to a server. The default server does not work properly. 
  So in this step, we will change the default server source. 
  Without a synchronized clock, we won't be able to install important updates and libraries which are essential.
  
Set the raspberry source as follows:
1. in the Raspberry Pi terminal type 
```
sudo nano /etc/apt/sources.list
```
2.  uncomment the bottom line 
3. In the file: change the mirror URL to a desired one (a list  of URLs is attached [here] (https://www.raspbian.org/RaspbianMirrors))
a mirror link has several components. Change only the existing  mirror URL (not the distribution or components)! 
```
deb http://<mirror-url>/ <distribution> <components>
```
for example:
```
deb http://raspbian.mirror.garr.it/mirrors/raspbian/raspbian/ bullseye main contrib non-free rpi

```
- mirror-URL: The URL of the mirror you want to use.
- distribution: The name of the distribution (e.g., stretch, buster, etc.).
- components: The software components you want to include (e.g., main, contrib, non-free, etc.).

4. Save and exit

## Installing updates 
Note that the last command in the code block below is the installation of the samba client which will allow us to connect to storWIS, and not a general update.
  Now run the following commands in the terminal.
  ```
  sudo apt-get update
  sudo apt-get upgrade 
  sudo apt-get install samba-common smbclient samba-common-bin smbclient  cifs-utils
  ```

## Mounting storWis onto the Raspberry Pi.
storWis is used to back up all the files which contain the environment monitoring data.
we can also access storWis relatively easily from different computers such that we have access to the data from any computer that is connected to the institute network.
 Create a credentials file, for instance, at the /home directory.
 Here, we will call it cred
The credential file is a text file containing the following format:
```
username=USERNAME(the desired username) 
password=PASWORD(its password) 
domain=wismain
```
Type in terminal:
```
sudo nano /etc/fstab
```
At the bottom of the file add the following line:
```
//isi.storwis.weizmann.ac.il/labs/cohen /mnt/path/to/mount/point cifs noauto,users,credentials=/PATH/to/cred,dir_mode=0777,file_mode=0777,noserverino,x-systemd.automount 0 0
```
Change the path to the mount point and to the credentials file. 

Save and exit

In terminal type
```
sudo mount -a
```
Now you should have Storwis folders in your directory, in the above example - /mnt. 

To check that the mounting was succesfull, you can type in the terminal either of the follwing commands:
```
df -h
```
In this example, look through the output to find your remote disk '//isi.storwis...' . It will be listed along with its mount point, which is the directory where it is mounted.

OR
```
ls /path/to/mount/point
```
In this example, the output should show all of the folders in the 'storwis' drive (see picture).

![check_mounted_to_storwis](https://github.com/user-attachments/assets/79eb34b4-3d16-4386-8634-bbac05511fb7)


IMPORTANT: Storwis should be mounted only when the Raspberry Pi is connected to the internet!
If there is no internet connection and the script is trying to access / save files in the STORWIS directory, errors might occur. In order to avoid that, you can type the following command in the terminal:
```
sudo umount /mnt/path/to/mount/point 
```
The path to mount point should match the location you defined STORWIS to mount on in the previous step (in the example - /mnt)

## Acquiring neccesary files and libraries

* Download the [acoustic_chamber_environment_control](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/tree/main)  repository as by clicking on `Code > Download zip.` extract the zip file onto the dashboard.
  now you should have a folder by the same name containing all the repository content.

* Install all Python dependencies (by running `pip install -r path/to/requirements.txt`, or by installing all the libraries manually)
  Numpy should already be installed in the Raspberry Pi, but sometimes when installing pandas it messes up something with numpy and it has to be reinstalled. To do so run:
  ```
  sudo pip3 uninstall numpy
  ```
  And then when the process is complete, reinstall by running:
  ```
  sudo pip3 install numpy
  ```
  Using sudo will ensure that numpy will be available system-wide.
  
  If the problem presists (later, when you try to run the `control_main` script), you can also try fixing this problem by directly installing 'libopenblas':
  ```
   sudo apt install libopenblas-dev
  ```

  
* Install Arduino IDE: In terminal type `sudo apt-get install Arduino`.
* (OPTIONAL)Install visual studio code: In terminal type `sudo apt-get install code`.
* Install all Arduino dependencies: You can do so by looking them up in the libraries section of the Arduino IDE:
  1. DHT sensor library
  2. DHTlib
  3. SparkFun Qwiic Scale NAU7802 Arduino Library
  4. SparkFun I2C MUX Arduino Library
     
  OR - you can download the libraries directly from github as a .zip file and follow these instructions:  
    * In Arduino IDE go to `Sketch > Include Library > Add .ZIP Library` and choose the library file 

    * Scale libraries can be downloaded from [here](https://github.com/sparkfun/SparkFun_Qwiic_Scale_NAU7802_Arduino_Library) and [here](https://github.com/sparkfun/SparkFun_I2C_Mux_Arduino_Library). Temperature and humidity sensor library can be downloaded from [here](https://github.com/CainZ/DHT)  


## Setting the script to run automatically when Raspberry Pi is turned on
The script should be launched automatically when Raspberry Pi is turned on.

This is done using the following tools - 
1. We have a bash script, called `startup_script.sh` which is an infinite loop that keep relaunching the script and waits for it to finish. If it crashes, it's supposed to run again.
2. When Raspberry Pi turns on, we automatically run the `startup_script.sh` script.

To automatically run the script when the machine turns on - <br>
*remember to change the '/path/to/startup_script.sh' part with the actual path to the startup script where needed*
1. Modify the bash script permission. in Terminal type : `chmod +x path/to/script/startup_script.sh`. 
2. In terminal Type `sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`
3. Add the following command to the end of the file - 
`@lxterminal -e /path/to/script/startup_script.sh`
  save and exit terminal.
4. Create a folder that will store the sensor data, and a folder that will store scale data. Update the path to those folders in the neccesary places according to the next step.
5. Update correct paths: Inside the acoustic_chamber_environment_control folder, there are several scripts, which use default paths that are not neccesarily compatible with the machine you are working on.
Update the paths in the following files:
 * in `startup_script.sh` -  update the path to config file.
 * in your [config file](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/config_files/cage_1_config.yaml), `dataOutputBasePath` and `scaleOutputBasePath` are the `base_path`'s to the folders you've created in the above step 4.

STILL IN WORK: AUTOMATICLLY SAVING THE DATA TO STORWIS
 * in [server_copy_script.sh](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/main/server_copy_script.sh) update the `base_path` to the folder you've created in step 4.
Update the `base_server_path` to the path where you want to copy the data to (storWis path).

6. Reboot the machine to verify that it's working

## Copying data to the remote disk
**NOTE: This section is still in the making**
The script `server_copy_script.sh` is used to copy the output files that are created by our code to a remote disk.

For this to work, the disk must be mounted to the Raspberry Pi.

Once it's mounted, the copy job can be scheduled via crontab.

Generally speaking, we can work with crontab as follows -
1. Type `crontab -e`
2. Add a new line at the end of the file, following the crontab syntax (a very nice explanation is commented out in the file itself).
3. For example, we may add - `0 6 * * * /path/to/server_copy_script.sh` to run every day at 06:00


In our case, we need to add the following two lines to crontab - 
```
59 5 * * * chmod a+x /path/to/server_copy_script.sh
0 6 * * * /path/to/server_copy_script.sh
```

The first command will run at 05:59 and will verify that we have permission to execute the script.

The second command will run a minute later, 06:00, and perform the actual copy.

## Summary.
After you've completed all of the steps, you should have a fully functioning Raspberry Pi that, on start-up, launches a Python script that controls the Arduino microcontroller and reads data from it.
You also should have access to storWis, where .csv files will be copied automatically.
Follow the next steps to prepare the arduino and operate the setup according to your preferances.

# Check that the system was configures properly
After the Rasperry Pi waas configured by following all of the steps above, we can check that it works properly by first running the script manually:

## Manually running the script
1. Make sure you have updated the config file. You can use the first example [here](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/f3f0723a57ecb227c9b016319a1390bf857777fb/config_files/How%20to%20use%20the%20config%20file.md)
2. Make sure you have a folder for output data files (according to what you specified in the config files, for the `dataOutputBasePath` and `scaleOutputBasePath` keys)
3. Open terminal and run `python /path/to/script/arduino_main.py --config=/path/to/config.yaml` (change path to script and config file accordingly)
4. The terminal should look like this:
   ![Terminal when running the script](https://github.com/user-attachments/assets/a34e9813-8287-4d5e-9a02-e30466f52d5f)

*Replace photo with a similar one after making adjustments in the control_main.py script.
