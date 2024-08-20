import datetime
import sys
import os
import time
import yaml 
from zoneinfo import ZoneInfo
from argparse import ArgumentParser
import glob
import astral
from astral.sun import sun
import serial
import serial.tools.list_ports
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

WEIZMANN_LAT = 31.905111
WEIZMANN_LONG = 34.808349

SERIAL_PORT_DATA_RATE = 9600
SLACK_CHANNEL_ID = "C04SXKM8K7V" # The Slack channel id for the `monitor_alerts` channel

SLACK_TOKEN = "xoxb" # insert the slack API (bot) token here. 

POSSIBLE_DEVICE_PATHS = [
    "/dev/ttyACM0", 
    "/dev/ttyACM1", 
    # Debugging on local macOS machine - 
    "/dev/cu.usbmodem1101",
    "/dev/tty.usbmodem11101",
    "/dev/cu.usbmodem2401",
    "/dev/cu.usbmodem2301",
    # Debugging on a PC - 
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5" 
] 

# On/Off tokens will be sent to the Arduino device to turn the lights on/off.
# The data is sent as bytes, and on the Ardunio we treat it as an int. 
# The threshold is the number 100. Since `a` is 97 (int.from_bytes(b"a", "big") == 97)
# and `f` is 102, they turn the light on / off respectively.
# This is the method that was previously used by Yarden, so I'm keeping the same logic.
ON_TOKEN = b'f'
OFF_TOKEN = b'a'

LAST_LIGHT_SWITCH_STATE = None

# These are the names of the CSV columns.
# NOTE - The last column must be dateTime, since we're counting the rest of the fields to verify
# the data vailidity!
CSV_FIELD_NAMES = ['humidity(%)','temprature(deg celsius)','photoresistor(milivolt)','Scale Reading (grams)', 'dateTime']

TIMEZONE_NAME = "Asia/Jerusalem"

strf_format = '%Y-%m-%d %H:%M' # This is the format for extracting datetime object from the 'Time' column string
scale_report_strf_time_format = '%Y-%m-%d %H:%M:%S' # This is the time format to be saved in the weight reports

def get_serial_device():
    """
    Get the device object for our serial port.
    """   
    for path in POSSIBLE_DEVICE_PATHS:
        try:
            ser = serial.Serial(path, SERIAL_PORT_DATA_RATE, timeout=1)
            print(f"\tSuccessfully opened serial port {path}")
            return ser
        except serial.SerialException:
            pass

    raise Exception(f"No valid serial port could be found! Tried the following - {POSSIBLE_DEVICE_PATHS}")


def get_astral_default_location_object():
    """
    Returns a default LocationInfo object for Israel, which is "Jerusalem".
    """
    db = astral.geocoder.database()
    location_object = astral.geocoder.lookup("Jerusalem", db)
    return location_object


def get_weizmann_location_object():
    """
    Return the LocationInfo object for the Weizmann Institute, which is determined by coordinates.
    """
    location_object = astral.LocationInfo('Rehovot', 'Israel', TIMEZONE_NAME, WEIZMANN_LAT, WEIZMANN_LONG)
    return location_object


def get_sun_times_by_offset(city: astral.LocationInfo, days_offset: int = 0,Hours_offset: int =0):
    """
    Receive a city (LocationInfo object) and return the sunrise & sunset times, for the current date.

    In addition, we receive a `days_offset` value (default = 0), which indicates whether we want a delay
    in our date calculation
    """

    date = datetime.date.today() + datetime.timedelta(days=days_offset) 

    sun_info = sun(city.observer, date=date, tzinfo=ZoneInfo(TIMEZONE_NAME))
    sunrise_time = sun_info["sunrise"]
    sunset_time = sun_info["sunset"]

    return (sunrise_time, sunset_time)


def get_sun_times_by_day(city: astral.LocationInfo, date: datetime.datetime.now()):
    """
    Receive a city (LocationInfo object) and return the sunrise & sunset times, for a desierd date.
    it's default is today's date
    """

    sun_info = sun(city.observer, date=date, tzinfo=ZoneInfo(TIMEZONE_NAME))
    sunrise_time = sun_info["sunrise"]
    sunset_time = sun_info["sunset"]

    return (sunrise_time, sunset_time)
    

def send_to_slack(slack_client, is_on, time):
    """
    Send a message to 'monitor_alerts' channel in slack when the light is turned on and off in every environmental system.
    The channel is defined by the 'SLACK_CHANNEL_ID' variable and the bot sending the file is defined by 'slack_client' variable which contains the bot's "token" ('SLACK_TOKEN').
    """
    env_system=config_data.get('env_system',0)
    if is_on:
        msg = f"Light was turned ON at {time}, in enviromental system {env_system}"
    else:
        msg = f"Light was turned OFF at {time}, in enviromental system {env_system}"

    try:
        result = slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=msg)
        if result.status_code != 200:
            raise Exception(f"Failed sending Slack message, response code = {result.status_code}")
    except Exception as err:
        print(f"Failed sending Slack message - {msg}")


def send_file_to_slack(slack_client, file_path):
    """
    This function sends *Files* such as .csv / .png to the slack channel.
    The function receives a slack client and a full path to the file and sends that file to slack.
    The channel is defined by the 'SLACK_CHANNEL_ID' variable and the bot sending the file is defined by 'slack_client' variable which contains the bot's "token" ('SLACK_TOKEN').
    """
    try:
        # Check if the file exists
        if os.path.isfile(file_path):
            # Read the file content
            with open(file_path, "rb") as file_content:
            # Upload the file
                result = slack_client.files_upload_v2(
                    file=file_content,
                    channel=SLACK_CHANNEL_ID,
                    filename=os.path.basename(file_path),
                    )
                print(f"File uploaded to Slack, result = {result['file']['id']}")
        else:
            print(f"File does not exist: {file_path}")
    except SlackApiError as e:
        # Handle errors
        print(f"Failed to upload file to Slack: {e.response['error']}")
        
def read_config(path):
    """
    Reads a YAML config file from a given path, and returns its content as a dict.
    """
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            return data
    except Exception as err:
        raise Exception(f"Failed reading file `{path}` - {err}")    


def data_aggregation(list_of_data_points):
    """
    Receive a list of data points, where each datapoint is a dictionary, e.g. - 
        {"humidity": 6, "temp": 1.3, "photoresistor": 800}
    
    and return an aggregated dictionary, with the minimum, maximum and median values for each category - 
    {"min_humidity": ___..., "max_humidity": ___... , "median_humidity": ___ , ...} and so on for all values of the original dictionary
    """
    df = pd.DataFrame(list_of_data_points)

    aggregated_data = {}
    try:
        for field in CSV_FIELD_NAMES:
            if (field != "dateTime") and (field != 'Scale Reading (grams)'): 
                aggregated_data[f"{field}_min"] = str(df[field].min())
                aggregated_data[f"{field}_max"] = str(df[field].max())
                aggregated_data[f"{field}_median"] = str(df[field].median())
    except Exception as err:
        print(f"Failed aggregating data - ")
        print(list_of_data_points)
        print("#####")
        print("ERROR -")
        print(err)

    current_time = datetime.datetime.now().strftime(strf_format)
    aggregated_data["dateTime"] = current_time

    return aggregated_data

def get_arduino_data(serial_device):
    """
    Read & parse sensor data from the arduino device (via the serial port).
    We return a dict with the parsed data from the sensors.
    """
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y_%m_%d_%H_%M_%S.%f")

    try:
        arduino_raw_data = serial_device.readline()
    except Exception as err:
        print(f"Failed reading data from Arduino! {err}")
        return None
    
    data_packet = parse_arduino_data(arduino_raw_data)

    # Verify that the data was read properly. 
    # If our data dict has less than the expected CSV field name count (minus 1 for the datetime field
    # which we manually add), then there's been an error with reading the data 
    if (data_packet is None) or (len(data_packet) != (len(CSV_FIELD_NAMES) - 1)):
        print(f"Failed parsing data. Ignoring this record! (raw data was - {arduino_raw_data})")
        return None

    data_packet.append(formatted_time)

    tuples = [(key, value) for i, (key, value) in enumerate(zip(CSV_FIELD_NAMES, data_packet))]

    return dict(tuples)


def parse_arduino_data(arduino_raw_data):
    """
    this function accepts raw data from the serial port arduino it is connected to and edit it such that we will get numbers, with no space between lines.

    ###ARGS###
    arduino_raw_data - a one line with semicolon as delimeter between values for example : 50;300;14.6;

    In data acquisition modes (sensor, weight):
    'arduino_raw_data' comes as a line with an additional 8 values for 8 possible scales. Total 11 values, eg. 50;300;14.6;0.00;20.1;19.6;0.00;0.00;2.22;0.00;0.00;
    In this case the formed list of data values is initially split into two: 'weight_packet' to take the weight measurements, and 'data'packet' to take the sensor measirements.
    Then, the weight data is added in the end of the sensor data as a list of 8 values, which will later be handled separately from the sensor data.
    The joint list of data values is returned (eg. [50, 300, 14.6, [0, 20.1, 19.6, 0, 0, 2.22, 0, 0]])
    """
    try:
        raw_data = str(arduino_raw_data,'utf-8')
        # raw_data = arduino_raw_data.decode('utf-8')
        data_packet = raw_data
        data_packet = data_packet.strip('\r\n')
        data_packet = data_packet.split(";")

        ## single or no scale version (Tom's old version):
        # data_packet = [float(x) for x in data_packet]

        # Yuval's new Mux multiscale version - 8 scale readings are parsed seperately and re-attached to the data_packet as one item (list).
        weight_packet = [float(x) for x in data_packet[3:-1]]
        data_packet = [float(x) for x in data_packet[0:3]]
    except Exception as err:
        print(f"Failed parsing a row - {raw_data}. Error - {err}")
        return None
    data_packet.append(weight_packet)
    return data_packet


def parse_stable_date(stable_date):
    """
    parse a stable date, to make it a datetime object, for sun location
    
    """
    try:
        data_packet=str(stable_date)
        data_packet = data_packet.split("/")
        stable_date_obj=datetime.date(int(data_packet[0]),int(data_packet[1]),int(data_packet[2]))
    except Exception as err:
        print(f"Failed parsing the date - {stable_date}. Error - {err}")
        return None
    return stable_date_obj

def parse_sunrise_sunset(set_time):
    """
    parse sunrise and sunset times, to make it a time object, for turning on and of light
    
    """
    try:
        data_packet=str(set_time)
        data_packet = data_packet.split(":")
        set_time_obj=[int(data_packet[0]),int(data_packet[1])]
    except Exception as err:
        print(f"Failed parsing the date - {set_time}. Error - {err}")
        return None
    return set_time_obj

def handle_lights(serial_device, config_data, wis_location_info, slack_client):
    """
    Receive the serial device object, and use it to turn the lights on/off.
    The logic behind this is documented at the beginning of the code.
    """
    light_switch_status = LAST_LIGHT_SWITCH_STATE
    current_time = datetime.datetime.now()


    days_offset = config_data.get("days_offset", 0)
    hours_offset = config_data.get("Hours_offset", 0)
    stable_date=config_data.get("stable_date", 0)
    sunrise = config_data.get("sunrise",0)
    sunset =config_data.get("sunset",0)
    
    if (sunrise is not None) & (sunset is not None):
        sunrise_time=parse_sunrise_sunset(sunrise)
        sunset_time=parse_sunrise_sunset(sunset)
        sunrise_time=datetime.time(sunrise_time[0],sunrise_time[1])
        sunset_time=datetime.time(sunset_time[0],sunset_time[1]) 
        
        print(f"\tSunrise and Sunset were calculated were set manually. sunrise `{sunrise_time}`, sunset: '{sunset_time}'")
    elif stable_date is not None:
        stable_date_obj=parse_stable_date(stable_date)
        print(f"\tSunrise and Sunset were calculated according to a fixed date: `{stable_date_obj}`")
        
        sunrise_time, sunset_time = get_sun_times_by_day(wis_location_info, stable_date_obj)
        
        sunrise_time=sunrise_time.time()
        sunset_time=sunset_time.time()
        
    elif type(days_offset) == type(1):
        print(f"\tCalculating sun times with a delay of `{days_offset}` ")
        sunrise_time, sunset_time = get_sun_times_by_offset(wis_location_info, days_offset, )
        sunrise_time=sunrise_time.time()
        sunset_time=sunset_time.time()
    elif not ((sunrise is not None) & (sunset is not None)):
        sunrise_time=sunrise_time.time()
        sunset_time=sunset_time.time()
            
    #handeling sunset sun rise hours offset
    
    sunrise_datetime  = datetime.datetime.combine(current_time.date(), sunrise_time)
    sunset_datetime = datetime.datetime.combine(current_time.date(), sunset_time)
    
    sunrise_time =sunrise_datetime + datetime.timedelta(hours=hours_offset)
    sunset_time = sunset_datetime + datetime.timedelta(hours=hours_offset)
   
    sunrise_time = sunrise_time.time()
    sunset_time =sunset_time.time()
    
    print(f"Surise time = {sunrise_time}")
    print(f"Sunset time = {sunset_time}")

    if current_time.time() > sunrise_time and current_time.time() < sunset_time: ## the new sunrise_time is a time object so it doesnot havea ".time() option. Should be fixed 
        print(f"Time to turn the lights on!")
        serial_device.write(ON_TOKEN)
        print(f"Light turned on!")

        if light_switch_status == "OFF" or light_switch_status is None:
            send_to_slack(slack_client, is_on=True, time=current_time)
            light_switch_status = "ON"
    else:
        print("Lights stay off!")
        serial_device.write(OFF_TOKEN)
        
        if light_switch_status == "ON" or light_switch_status is None:
            send_to_slack(slack_client, is_on=False, time=current_time)
            light_switch_status = "OFF"
    
    return light_switch_status


def create_filename_for_data_report(config_data, time_format="%Y_%m_%d"):
    ''' 

    Create the file name of the saved report based on the given parameters and time format

    '''
    curr_time = datetime.datetime.now().strftime(time_format)
    days_offset = config_data.get("days_offset", 0)
    stable_date=config_data.get("stable_date", 0)
    if stable_date is not None:
        stable_date=stable_date.replace("/","") # In order to save the file we need to get rid of the slashes in the date
    sunrise = config_data.get("sunrise",0)
    sunset =config_data.get("sunset",0)

    if (sunrise is not None) & (sunset is not None):
        file_name = f"{config_data['room_name']}_env_system_{str(config_data['env_system'])}_{curr_time}_manually_set.csv"
    elif stable_date is not None:
        file_name = f"{config_data['room_name']}_env_system_{str(config_data['env_system'])}_{curr_time}_stable_date_{str(stable_date)}.csv"
    elif type(days_offset) == type(1):
        file_name = f"{config_data['room_name']}_env_system_{str(config_data['env_system'])}_{curr_time}_Days_offset_{str(days_offset)}.csv"

    return file_name


def plot_data(data, xaxisby='hours from start', date_fmt = '%Y-%m-%d %H:%M:%S.%f', title='Bird weight over time', save=False, fig_name_path=''):
    fig, ax = plt.subplots()

    # Extract the dates and times separately from the time column
    times = [datetime.datetime.strptime(time, f"{date_fmt}").strftime("%H:%M") for time in data["Time"]]
    dates = [datetime.datetime.strptime(time, f"{date_fmt}").strftime("%Y-%m-%d") for time in data["Time"]]
    # times = [time.strftime("%H:%M") for time in data["Time"]]
    # dates = [time.strftime("%Y-%m-%d") for time in data["Time"]]

    # Calculate the ticks of the date shifts
    unique_dates = np.unique(dates)
    date_shift_ticks  = []
    for date in unique_dates:
        date_shift_ticks.append(dates.index(date))

    # Plot the weight data
    ax.plot(data.index, data['Weight'], marker='.', linestyle='-')

    # Edit time axis
    if xaxisby == 'datetime': 
        ax.set_xticks(data.index[::3600], labels=times[::3600])
        ax.set_xlabel("time(H_M)")
        
        # Plot vertical lines in positions of date shifts
        for date in date_shift_ticks:
            ax.axvline(x=date, color='red', linestyle='--')
    
            # Add the value of the index next to the vertical line
            ax.text(date, np.mean(ax.get_ylim()), str(dates[date]), color='red', rotation=90, va='center', ha='right')

    else: # Plot x-axis as hours from start
        ax.set_xticks(data.index[::3600], labels=np.arange(0, len(data.index[::3600])))
        ax.set_xlabel("hours from start")

    plt.xticks(rotation=90)                  
    ax.set_ylabel("weight(g)")
    plt.title(f"{title}")
    # ax.legend()

    if save == True:
        plt.savefig(fig_name_path)
    
    return fig, ax


def extract_dates(path_to_file, birdname):
    filename = os.path.basename(path_to_file)
    start_date = filename[(len(birdname)+15):(len(birdname)+25)]
    if len(filename) > (len(birdname)+26):
        end_date = filename[(len(birdname)+27):(len(birdname)+37)]
    else:
        end_date = ''
    return [start_date, end_date]


def find_single_csv_file(path_to_dir, name_type='full'):
    files = glob.glob(path_to_dir + '/*.csv')
    if len(files) == 0:
        print(f"Error when trying to obtain csv file from {path_to_dir}. No files in directory.")
    elif len(files) > 1:
        print(f"Error when trying to obtain csv file from {path_to_dir}. More than one file in directory.")
    else:
        if name_type == 'full':
            return files[0]
        elif name_type == 'basename':
            return os.path.basename(files[0])


def concat_data_in_folder(path_to_dir):
    files = sorted(glob.glob(path_to_dir + '/*.csv')) # Gives the whole path to each file in the directory
    scale_data = pd.read_csv(files[0])
    for file in files[1:]:
        temp = pd.read_csv(file)
        scale_data = pd.concat([scale_data, temp], ignore_index=True)
    return scale_data


if __name__ == "__main__":
    print("Hello! This is the Arduino controller script!\n")

    ## Part 1 - parse the config file
    parser = ArgumentParser()

    # `config` actually IS a required variable, but this way it'll be easier to raise a custom error when it isn't supplied
    parser.add_argument("--config", required=False, help="The path for the config file we're working with.")
    args = parser.parse_args()

    config_path = args.config
    config_path = r'/Users/cohenlab/Documents/GitHub_Yuval/acoustic_chamber_environment_control/config_files/config_1.yaml'
    if config_path is None:
        raise Exception("No config file was supplied! Please rerun and add `--config=/path/to/config` ")

    config_data = read_config(config_path)
    print(f"Working with config file `{config_path}`, which contains - ")
    print(yaml.dump(config_data)) # This is just a trick to print the YAML content in a nicer way

    ## Part 2 - Initialize Slack
    try:
        slack_client = WebClient(token=SLACK_TOKEN)
        print("\tSuccessfully initialized Slack client")
    except Exception as err:
        print(f"Failed initializing Slack client - `{err}`")
        sys.exit(1)
        
    ## Part 3 - Connect to the serial device
    try:
        serial_device = get_serial_device()
        print("\tSuccessfully connected to Serial device")
    except Exception as err:
        print(f"Failed connecting to the Serial device - `{err}`")
        sys.exit(1)
    
    ## Part 4 - Initialize a Weizmann location object for the Astral package
    try:
        wis_location_info = get_weizmann_location_object()
        print("\tSuccessfully initialized the location object for WIS")
    except Exception as err:
        print(f"Failed initializing the location object - `{err}`")
        sys.exit(1)
    
    print("\n")

    ## Part 5 - This is the main part of the code, which runs in a loop and reads data from sensors, and controls the light switch.

    scale_readings = [] # This array will hande temporary scale data and will be reset once the defined time is over
    
    temp_sensor_data = [] # This array will handle the temporary sensor data, and will be reset once the defined time is over
    daily_sensor_data = pd.DataFrame() # This array will handle daily sensor data and will be reset once a day is over

    temp_loop_start_time = datetime.datetime.now()
    day_loop_start_time = datetime.datetime.now()

    if config_data["sendWeightReportToSlackTime"] is not None:
        last_slacking_time = datetime.datetime.now() # This timestamp will help indicate if we need to send the weight report to slack
        # Read user settings for time to send daily weight report to slack in HH:MM
        target_hour = int(config_data["sendWeightReportToSlackTime"][0:2])  # Example: 14 for 2 PM
        target_minute = int(config_data["sendWeightReportToSlackTime"][3:])  # Example: 30 for 2:30 PM

    if config_data["scaleDataReadingAndSaving"]: # If user chose to collect scale data, print the bird catalog (which bird is connected to which channel).
        bird_catalog = dict()
        for i in range(8):
            bird_id = config_data.get(f"channel{i}", 0)
            bird_catalog[f"channel{i}"] = bird_id
            print(f"bird connected to channel{i}: {bird_id}")
        print("\n")
    
    while True: 
        while serial_device.in_waiting == 0: 
            pass 
        
        # Part 5.1 - Handle the lights! Turn the lights on/off, and update our state variable based on the action
        LAST_LIGHT_SWITCH_STATE = handle_lights(serial_device, config_data, wis_location_info, slack_client)

        # Part 5.2 - Read & aggregate data from the sensor
        current_time = datetime.datetime.now()
        print(f"Current UTC time is {current_time}\n")

        data_from_last_minute = []

        minute_loop_start_time = datetime.datetime.now()
        
       
        if config_data["sensorDataReadingAndSaving"] or config_data["scaleDataReadingAndSaving"]:
            '''
            If the user chose to collect data (either sensor or scale data), this part of the script will collect and store it in the following manner:

            Data collection loop should run for 1 minute, with a 1 second rest in between.
            Every second we get new data from the arduino, and store in an array.
            Then, sensor and scale data will each be concatenated to the appropriate data report and re-saved to the directories defined by the user.

            Sensor data:
            Sensor data (humidity, temprature and light) will be stored in a daily file, containing minimum, maximum and median values for every minute of data collection, together with the time&date for that recording.

            Scale date:
            Scale data for each monitored bird will be stored in a continuous weight report, containing time and weight(g) values from every second of data collection. Every minute newly acquired data will be added to the report.
            Once a day, in a time (HH:MM) defined by the user, the weight reports from all monitored birds will be sent to the lab slack channel - 'monitor_alerts', if the user chose to do so.
            '''
            #**********COLLECT DATA FOR 1 MINUTE**********
            while True:
                data = get_arduino_data(serial_device)
                # print("get arduino data: ", data)
                if data is None: # There was an error, moving on and ignoring this specific read
                    continue
                
                if config_data["scaleDataReadingAndSaving"]:
                    scale = data.get('Scale Reading (grams)')
                    scale_readings.append([datetime.datetime.now().strftime(scale_report_strf_time_format), scale])
                   
                # In the multiscale version, we need to separate the scale readings from the agg. data dict here because it is now a list of 8 values and cannot be used in data_aggregation
                data_for_agg = {key: data[key] for key in data.keys() & {'dateTime','humidity(%)','temprature(deg celsius)','photoresistor(milivolt)'}}
                # print("data for agg = ", data_for_agg)
                data_from_last_minute.append(data_for_agg) # changed data --> data_for_agg in multiscale version does not include scale data

                if (datetime.datetime.now() - minute_loop_start_time).seconds >= 60:
                    print("\tFinished collecting data for 1 minute")
                    break
                time.sleep(1)
            
            # After we recorded data for 1 minute, we aggregate it and store in the temporary array.
            aggregated_data = data_aggregation(data_from_last_minute)
            print("\tSuccessfully aggregated data\n")
            temp_sensor_data.append(aggregated_data) ## Maybe we don;t need that
			

            #**********UPDATE SENSOR DATA REPORT**********          
            if config_data["sensorDataReadingAndSaving"]: #User chose to save sensor data
                print(f"\tWriting sensor data to disk...")
                
                # Create the name of the saved report based on the current parameters
                file_name = create_filename_for_data_report(config_data, time_format="%Y_%m_%d")

                # Generate path and save the file (create temporary files folder if neccesary)
                sensor_data_base_path = os.path.join(config_data["sensorOutputBasePath"], "sensor_data")
                os.makedirs(sensor_data_base_path, exist_ok=True)
                
                sensor_data_filename = os.path.join(sensor_data_base_path, file_name)
                
                new_sensor_data_df = pd.DataFrame(temp_sensor_data)

                # Re-arrange columns so that the time will appear first
                columns_order = ['dateTime'] + [col for col in new_sensor_data_df.columns if col != 'dateTime']
                new_sensor_data_df = new_sensor_data_df[columns_order]

                try:
                    existing_sensor_data = pd.read_csv(sensor_data_filename)
                    joint_sensor_data = pd.concat([existing_sensor_data, new_sensor_data_df])
                    try:
                        joint_sensor_data.to_csv(sensor_data_filename, index=False)
                        print(f"\tSuccessfully added sensor data to file: {sensor_data_filename}.\n")
                    except Exception as e:
                        print(f"\t\tAn error occurred while saving the new sensor data report in: {sensor_data_filename}: {e}")
                except FileNotFoundError:
                    # If there is no existing weight report for this bird, use current data to form a new report.
                    new_sensor_data_df.to_csv(sensor_data_filename, index=False)
                    print(f"\tSuccessfully created a new sensor data report. It was saved to: {sensor_data_filename}.\n")

                # Reset temporary data array
                temp_sensor_data = [] 
            else:
                print('\tUser chose not to print and save aggregated sensor data.')


            #**********UPDATE WEIGHT REPORTS**********        
            # Add temporary scale data to existing reports from each bird:  
            if config_data["scaleDataReadingAndSaving"]: # User chose to save scale data
                print(f"\tWriting scale data to disk...")
                path_to_weight_reports = os.path.join(config_data["scaleOutputBasePath"], "weight_reports")

                # This dataframe will contain the current temporary time and weight data from all active scales
                scale_df = pd.DataFrame()
                # Create the time column once as it is similar for all
                scale_df['Time'] = [item[0] for item in scale_readings] 

                # Iterate through all birds, if they have an active scale, add the new collected data to the weight report
                for i in range(8):
                    if bird_catalog[f"channel{i}"] is None:
                        print(f"\t\tno birds in channel {i}, moving on...")
                        continue
                    else:
                        bird = bird_catalog[f"channel{i}"]
                        print(f"\t\tbird '{bird}' in channel {i}, writing it's temporary scale data...")
                        # Collect data for current bird into DataFrame.
                        scale_df[bird] = [item[1][i] for item in scale_readings]
                        new_bird_data = scale_df[["Time", f"{bird}"]]
                        # Build path to weight reports folder and create a folder for the current bird if it doesn't exist:
                        path_to_current_bird = os.path.join(path_to_weight_reports, bird)
                        os.makedirs(path_to_current_bird, exist_ok=True) 
                    
                        # date_today = datetime.datetime.now().strftime("%Y_%m_%d") # current date
                        weight_report_filename = os.path.join(path_to_current_bird, f"{bird}_weight_report.csv")
                        try:
                            existing_bird_data = pd.read_csv(weight_report_filename)
                            joint_bird_data = pd.concat([existing_bird_data, new_bird_data], ignore_index=True)
                            try:
                                joint_bird_data.to_csv(weight_report_filename, index=False)
                                print(f"\t\tSuccessfully added temporary scale data for bird: {bird}.")
                            except Exception as e:
                                print(f"\t\tAn error occurred while saving the new weight report for bird {bird}: {e}")
                        except FileNotFoundError:
                            # If there is no existing weight report for this bird, use current data to form a new report.
                            new_bird_data.to_csv(weight_report_filename, index=False)
                            print(f"\tSuccessfully created a new weight report for bird: {bird}. It was saved to: {weight_report_filename}.\n")
                    
                # Reset temporary scale data array
                scale_readings = []

            else:
                print('\tUser chose not to print and save scale data.')


            #**********SEND REPORTS TO SLACK**********
            # Once a day, weight reports from all monitored birds will be slacked according to user choice.
            # Check if user entered a time (HH:MM), If not - continue without slacking.
            if config_data["sendWeightReportToSlackTime"] is not None:
                now = datetime.datetime.now()
                time_from_last_slacking = (now - last_slacking_time).total_seconds() / 60
                # Check if it's time to send daily weight reports to slack:
                # 1. Check if current hours & minutes match target hours & minutes.
                # 2. Sometimes a specific minute can be missed or repeated (because the minute data acquisition loop cannot be accurate to the second). 
                #    The second condition is there to catch a missed minute marker (target_minute+1) as long as no slack report was sent in the last minute(time_from_last_slacking).
                #    If target_minute was missed because the last 'now' was 09:59:59 and the new 'now' is 10:01:01 (the time 10:00 was missed), and the desired slacking time is 10:00, the condition will also work for 10:01 as long as there was no report sent in 10:00.
                #    A report could have been sent in 10:00, whereas the new 'now' will be 10:01 the condition would have worked unintendedly without the addition of the last condition. 
                if now.hour == target_hour and ((now.minute == target_minute or now.minute == target_minute+1) and time_from_last_slacking > 1):
                    print(f"\t\tCurrent time is : {now.strftime('%H:%M')}, Slacking daily scale data...")
                    # Generate daily data file for each bird, save it and send it to slack
                    weight_report_output_path = os.path.join(config_data["scaleOutputBasePath"], "weight_reports")
                
                    # upload the current scale report for each bird and send it to slack:   
                    for key, birdname in bird_catalog.items():
                        if birdname is None:
                            continue
                        else:
                            path_to_current_bird = os.path.join(weight_report_output_path, birdname)
                            weight_report_filename = find_single_csv_file(path_to_current_bird, name_type='full')

                            # send daily csv report to slack
                            try:
                                send_file_to_slack(slack_client, weight_report_filename)
                                last_slacking_time = datetime.datetime.now()
                                print(f"\t\tSuccesfully slacked daily weight report for bird {birdname}!")
                            except Exception as e:
                                    print(f"\t\t\tAn error occurred while slacking daily weight report for bird {birdname}: {e}")
    
        else:
            print('User chose not to print and save data at all')
            time.sleep(60)
            
        

