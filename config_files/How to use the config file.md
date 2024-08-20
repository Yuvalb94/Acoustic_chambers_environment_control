# Config file user manual
The [arduino_main.py](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/main/arduino_main.py) code is used to control the acoustic chambers light cycle, and read data from the Arduino and write the date onto a '.csv' file. <br>
In order to easily manipulate between different operating options, we use a config file which helps define several parameters inside the script without having to visit the script itself and change it every time. <br>
The config file is saved in `.yaml` format, so that the paremeters inside are structured as `Key : Value`pairs seperated by a colon. See example [here](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/main/config_files/cage_1_config.yaml) keys are on the left, values on the right.

There are a few things that we can manipulate by changing parameters in the config file:
1. Control the light cycle (when the lighs will be on/off)
2. Decide how to save data to the disk (sensor data / scale data / both, storage location)
3. Provide information about the scale system (what bird is monitored and in which channel)

## Controlling light cycle. 
By default, the system sets the light on/off times according to real-world sunrise and sunset times in our location (Weizmann), taken from `astral` library. Meaning that it will turn on the lights at the time of sunrise today in Weizmann, according to `astral`, and it will turn the lights off in sunset.

There are several ways to manipulate the acoustic chamber light cycle based on our research needs:
 1. **Set sunset time and sunrise time manually** - you decide by yourself when the light will be switched on/off.
 2. **According to a stable date** - set a fixed date for which sunrise and sunset times will be calculated and won't change.
 3. **According to day offset** - sunrise and sunset times will be calculated according to the number of days drift from today. For instance, if today is 16.07.2024 and you've passed `-10 days`, then sunrise and sunset times will be calculated according to 06.07.2024. The next day, sunrise and sunset  will be calculated according to the 07.07.2024. If you pass 0 in the days offset option, sunrise and sunset times will be calculated according to today's times, without any drift. If you want to control the light according to a future date, for instance, plus 10 days from 16.07.2024, then just pass `10` in the days offset key in the config file.

NOTE! It is important to write the hours / dates in a specific format (examples given below).

   ### Hirerchy of light cycle control options
The main script running on the Raspberry Pi is programmed to determine the light cycly times according to the first given input (manual -> fixed date -> days offset). Meaning that if a manual sunrise and sunset times are given, it will set the cycle based on those times and ignore the other values (fixed date, days offset). If the user does not write anything in the `sunrise` and `sunset` keys, the script will go on to the next level of `fixed date`, and if it is empty as well, it will go next to `days/hours offset`. If `days offset` and `hour offset` are both 0, the script will use the default values. <br>

**NOTE! if the user chooses not to manipulate the sunrise and sunset times, The `days offset` and `hours_offset` keys must get the value 0, or the script will collapse!**

## Config file format
The Python script expects a specific value format. Thus, it is essential to be consistent and precise when updating values to prevent the script from crashing. You don't need to change the critical format.
Example YAML file

```yaml
room_name: BigRecRoom 
env_system: 1
sunrise:  #time format should be as follows 'h:m' for instance 5:45:21 or 21:6 (which will give you 21:06:00) never put a zero before a number as in 05:06, just write 5:6 note, don't enter seconds!
sunset:  
stable_date:  # the date should be in the following format : 'yyyy/mm/dd', i.e. '2022/01/02' 
days_offset: 0
Hours_offset: 0
dataOutputBasePath: /Users/cohenlab/Desktop/scale_test_control/arduinoData
sensorDataReadingAndSaving: 1
scaleOutputBasePath: /Users/cohenlab/Desktop/scale_test_control/scaleData
scaleDataReadingAndSaving: 1
sendWeightReportToSlackTime: '12:05'
# CHANNELS 1-8: enter the name of the bird connected to each MUX channel. This will be used to create a folder for each bird and store its weight report. Leave non-connected channels empty.
channel0: 'testy'
channel1: 
channel2: 
channel3: 
channel4: 
channel5: 
channel6: 
channel7:

``` 
* `room_name`  - The room in which this environmental system is in (Big/Small_RecRoom)
* `env_system` - The ID of the environmental system (single control setup connected to up to 8 boxes)
* `sunrise` and `sunset` - These are the manual options to set the light cycle. Note: time format should be as follows 'h:m' for instance, 5:45:21 or 21:6 (which will give you 21:06:00). Do not put a zero before a single digit hour/minute time marker, as in 05:06. Just write 5:6. 
* `stable date` - The date according to which the light cycle times will be calculated. The date should be in the following format: 'yyyymmdd', i.e. '20220102'. This is the second of January 2022, 2.1.2022. Remember to pass the data as a string
* `days_offset` - The number of days offset from today. Enter a negative or positive number to manipulate, or 0 to stay in default mode. Note! if other paraeters are not defined, this key cannot stay empty - for default mode user nust enter 0 or the script will crash!
* `hours_offset` - Similar to days offset but for hours.
* `dataOutputBasePath` - The path to the folder where **sensor** data will be stored.
* `sensorDataReadingAndSaving` - Decide if you want to record and save **sensor** data or not. choose 1 for yes, and 0 for no.
* `scaleOutputBasePath` - The path to the folder where **scale** data will be stored.
* `scaleDataReadingAndSaving` - Decide if you want to record and save **scale** data or not. choose 1 for yes, and 0 for no.
* `sendWeightReportToSlackTime` - Define the time of day ('HH:MM') you want the daily weight report for each monitored bird to be sent to slack, if you chose to record and save scale data.
* `channels 1-8` - For every channel of the MUX scale system, write the name of the bird that is monitored as a string. Leave non-connected channels empty / null.
 
## Example config files
* First example: sunrise and sunset times will be calculated according to stable_date and data won't be read and saved.
```yaml
room_name: BigRecRoom 
env_system: 1
sunrise:  #time format should be as follows 'h:m' for instance 5:45:21 or 21:6 (which will give you 21:06:00) never put a zero before a number as in 05:06, just write 5:6 note, don't enter seconds!
sunset:  
stable_date: '2024/06/21' # the date should be in the following format : 'yyyy/mm/dd', i.e. '2022/01/02' 
days_offset: 0
Hours_offset: 0
sensorOutputBasePath: 
sensorDataReadingAndSaving: 0
scaleOutputBasePath: 
scaleDataReadingAndSaving: 0
sendWeightReportToSlackTime: 
# CHANNELS 1-8: enter the name of the bird connected to each MUX channel. This will be used to create a folder for each bird and store its weight report. Leave non-connected channels empty.
channel0: 
channel1: 
channel2: 
channel3: 
channel4: 
channel5: 
channel6: 
channel7:

``` 

* second example: Light cycle times will be calculated according to 25 days and 2 hours drift from today, sensor data will be saved at `/home/desktopArduinoData`, scale data will not be saved, therefore it does not matter what the user writes in `sendWeightReportToSlackTime` and `channels 1-8`.
```yaml
room_name: BigRecRoom 
env_system: 1
sunrise:  #time format should be as follows 'h:m' for instance 5:45:21 or 21:6 (which will give you 21:06:00) never put a zero before a number as in 05:06, just write 5:6 note, don't enter seconds!
sunset:  
stable_date:  # the date should be in the following format : 'yyyy/mm/dd', i.e. '2022/01/02' 
days_offset: 25
Hours_offset: 2
sensorOutputBasePath: `/home/desktop/ArduinoData`
sensorDataReadingAndSaving: 1
scaleOutputBasePath: 
scaleDataReadingAndSaving: 0
sendWeightReportToSlackTime: '30:89'
# CHANNELS 1-8: enter the name of the bird connected to each MUX channel. This will be used to create a folder for each bird and store its weight report. Leave non-connected channels empty.
channel0: 'jokesonyou'
channel1: 
channel2: 
channel3: 
channel4: 
channel5: 
channel6: 'doNotReplyRb17'
channel7:

``` 

* third example: Light cycle times will be calculated by manual setting to turn on at 7:25AM and turn off at 18:30PM, although `stable_date` and `days_offset` are holding valid values (Hierarchy). In addition, sensor data will be saved at `/home/desktop/ArduinoData/SensorData`, and scale data for birds 'lbrb43', 'rb100', 'lpnkrg1' will be recorded and saved at `/home/desktop/ArduinoData/ScaleData`. Once a day in 10:00 AM a daily report containing all data recorded for each bird so far, will be sent to `monitor alerts` group in slack as a .csv file.
```yaml
room_name: BigRecRoom 
env_system: 1
sunrise: '7:25' #time format should be as follows 'h:m' for instance 5:45:21 or 21:6 (which will give you 21:06:00) never put a zero before a number as in 05:06, just write 5:6 note, don't enter seconds!
sunset: '18:30'
stable_date:  # the date should be in the following format : 'yyyy/mm/dd', i.e. '2022/01/02' 
days_offset: 25
Hours_offset: 0
sensorOutputBasePath: `/home/desktop/ArduinoData/SensorData`
sensorDataReadingAndSaving: 1
scaleOutputBasePath: `/home/desktop/ArduinoData/ScaleData`
scaleDataReadingAndSaving: 1
sendWeightReportToSlackTime: '10:00'
# CHANNELS 1-8: enter the name of the bird connected to each MUX channel. This will be used to create a folder for each bird and store its weight report. Leave non-connected channels empty.
channel0: 'lbrb43'
channel1: 'rb100'
channel2: 
channel3: 
channel4: 'lpnkrg1'
channel5: 
channel6: 
channel7:

``` 
