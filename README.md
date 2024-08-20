# Acoustic chamber environment control setup
In our experiments we house birds in acoustic chambers. These chambers include wide spectrum LEDs to mimmick sun light and a fan system to circulate fresh air in the chamber. Seasonal birds, like the canaries we study, are sensitive to the daily cycle of light and dark, the photoperiod, and to its changes as days grow longer in spring and grow shorter in autumn. To mimmick this in the acoustic chambers, we created the environment control and monitoring setup described in this repository. This setup, called *environmental system* and sketched in figure 1, controls the light switch in up to 8 acoustic chambers, monitors the light level, humidity, and temperature in a sentinel chamber, and monitors the weight of up to 8 birds using [in-house built scales](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_yc_version/scale_system_documentation/scale_design.md).
## System overview
Figure 2 shows the *environmental system*'s functional overview. The system is controlled by a python script running on a Raspberry Pi computer. [This script](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/main/arduino_main.py) communicates with an Arduino microcontroller, which controls light switches, reads sensor data, and sends information back to the Raspberri Pi. 

The Raspberry Pi script:
 * Determines when lights should be turned on/off according to user-defined photoperiod regimes (detailed in [Operations](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_yc_version/README.md#operations)) and sends on/off commands to the Arduino.
 * Receives a sentinel chamber's temprature, humidity, and light sensor data from the Arduino and stores it and in .csv files.
 * Receives weight data of birds that are being monitored from the arduino and stores it (also in .csv files).
 * Store data locally and on the [storWIS drive](https://github.com/NeuralSyntaxLab/lab-handbook/wiki/Lab-Operations-and-Procedures#storwis) and/or send the data to the experimenter via Slack or Email.

Our environmental system allows flexibility in determining the photoperiod and its changes across days. Each  *environmental system* is given its unique ID. This allowes running experiments in different light cycles, or experiments on more than 8 acoustic chambers .

<figure>
<img src = "https://github.com/user-attachments/assets/3f617a45-ea5e-4f6d-8036-1d348ed8e47e" width = "1000" height = "850"> <br>
<figcaption> Figure 1: The environmental system setup </figcaption>
</figure>

---

## Table of contents
* **Part list** 
* **Preperations**
  1. [Setting up the Raspberri Pi](#setting-up-the-raspberry-pi)
  2. [Preparing hardware and connecting to Arduino](#preparing-hardware)
  3. [Setting up Arduino](#setting-up-arduino)
* **Operations**
  1. [Light control mode](#light-control-mode)
  2. [Light control & data acquisition mode](#light-control--data-acquisition-mode)

<br>

## Part list
[This table](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_yc_version/parts%20list.xlsx) contains the part list required to constructing one *environmental system*. The list reflects our current choice of microcontroller models, wiring, and connections. Many of these can be switched for the convenience of the user and their specific needs.

## Preperations
This section is a general overview of how to construct the *environmental system*. It contains links to separate manuals for manufacturing system components and describes how to connect them. This section also contains instructions about how to upload the Arduino code and how to calibrate the scale system. The next section, Opertaions, describes how to use the system once it's constructed and calibrated. 

### System hardware components
The following hardware components are constructed separately and wired after their installation in the acoustic chambers or in the experiment room's main instrumentation rack:
1. A Raspberry Pi minicomputer.
2. An Arduino Uno microcontroller.
3. Light control system - consists of 1 control box which connects to relay swiches on a maximum of 8 acoustic chambers.
4. Sensor box - consists of a humidity & temprature sensor (DHT) and a photoresistor (light sensor). Up to 1 box per setup.
5. Scale system - consists of 1 control box, capable of connecting up to 8 scales. Up to 1 system per setup.

To demonstrate the functional operation of the system, Figure 2 shows a simplified schematic that illustrates how sensors and actuators are connected to the Arduino microcontroller.
<figure>
  <img src = "https://github.com/user-attachments/assets/2519467c-20a3-4ffc-a414-5b14d84704b4">
  <br>
  <figcaption>Figure 2: Schematic diagram of the system components and their connections</figcaption>
</figure>

<br>
<br>
The following sequence of steps should be taken to construct the hardware components and to calibrate the system:

### 1. Set up the Raspberry Pi
When using a new Raspberry Pi, it has to undergo several steps, described in the [configuration guide](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/cf7c2d09ca352680ac4c0b2b953d89da0c118fb5/User%20Guides/Raspberry%20Pi%20Configuration.md), before using it to operate the environmental system. 

If you are using an already used Raspberry Pi, move on to preparing the hardware.
Return to the [configuration guide](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/cf7c2d09ca352680ac4c0b2b953d89da0c118fb5/User%20Guides/Raspberry%20Pi%20Configuration.md) if issues arise when running the `control_main.py` script.

### 2. Manufacture and prepare the light switches and sensor box 
This [assembly guide](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/cf7c2d09ca352680ac4c0b2b953d89da0c118fb5/User%20Guides/Hardware%20Assembly%20Guide.md) contains a step-by-step manual explaining how to build each device.

* #### 2.1 The light control system
Figure 3a illustrates the light control system. The system contains relay switches to control the light in each acoustic chamber and a control hub-box (3b) that transmitts the Arduino command to all the individual switches. The hub-box contains two output ports on the short edge that are used to connect to the Arduino microcontroller and a 5V external power source. On the long edge on both sides are 8 output ports that can connect to the relay switches on the acoustic boxes. To connect each relay switch to the hub, construct the cable shown in Figure 3c.

<figure>
  <div style="display: flex; justify-content: space-around; align-items: center;">
    <div>
      <img src="https://github.com/user-attachments/assets/bcb21ff7-fa91-4084-98cf-b2441daeda79">
      <figcaption style="text-align: center;">3a; Light control system diagram</figcaption>
    </div>
    <div>
      <br><img src="https://github.com/user-attachments/assets/6f29b7a1-29c8-45d0-aa78-bca54e76514b">
      <br><figcaption style="text-align: center;">3b; Light control hub-box.<br>The Arduino port connects the signal circuit, which transmits the signal from the Arduino to all relay switches, along with a 'GND' connection. The 5V port connects to an external 5V power source that helps send voltage to the relay switches without overloading the Arduino microcontroller.</figcaption>
    </div>
    <div>
    <br><img src="https://github.com/user-attachments/assets/938264f4-8b87-480a-a99c-6dd016027c1b">
    <br><figcaption style="text-align: center;">3c; Light control communication cable.<br>The cable is a simple 4-core cable with a 3-PIN Pigtail connector for easily connecting to the hub-box on one end, and a 3-pos connector to fit on the relay module on the other. In order to connect the relay switches on each acoustic box to the control hub, connect the relay-module end of the cable to the switch (as shown in the figure), spread the cable conveniently to the instrumentation rack and connect to one port of the hub-box.</figcaption>
    </div>
  </div>
</figure>


* #### 2.2 The sensor box
The sensor box should look like this: <br>
<figure>
  <img src = "https://github.com/user-attachments/assets/cd4a81d1-e175-4800-9989-cbe03c928424" width = "600" height = "600"> <br>
  <figcaption>Figure 4: The sensor box</figcaption>
</figure>
<br>

The box contains:

* DHT sensor (for detecting humidity, temprature)
* Photoresistor (for detecting light intensity)
* A connector for the communication cable (for receiving voltage - red and black wires, and sending data - green for DHT, white for photoresistor)

In order to connect the sensor box to the setup, construct the communication cable, shown in Figure 5 (guide for making the cable [here](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/cf7c2d09ca352680ac4c0b2b953d89da0c118fb5/User%20Guides/Hardware%20Assembly%20Guide.md)).

<figure>
  <img src = "https://github.com/user-attachments/assets/d995c5bd-1337-4e95-a3b7-6ce7065a55e3" width = "400" height = "500"><br>
  <figcaption>Figure 5: The cable for connecting the sensor box to the Arduino</figcaption>
</figure>

### 3. Manufacture and calibrate the scale system
The scale system allows to measure the weight of 8 birds simultaneously. This [Scale System setup guide](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/7b98ca46d210fc865f576b8630c2cdef0f82fe2f/User%20Guides/Scaling%20System%20Setup%20Guide.md) explains how to build the system and how to calibrate the scales for getting precise measurements. **Note:** Calibrating the scale system requires connecting it the Arduino and running the Arduino code [described below](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_yc_version/README.md#5-set-up-the-arduino). 

Figure 6 illustrates the whole scale system. Similar to the light control system, it contains a control hub-box, which contains special breakout boards (Qwiic Scale NAU7802, Qwiic MUX) that helps transmit, amplify and convert the signal from up to 8 scales simultaneously. The Qwiic MUX board inside the hub-box connects to the Arduino microcontroller on one end, and the NAU7802 board connects to the eight input ports to which we can connect the scales with long communication cables.

<figure>
  <div style="display: flex; justify-content: space-around; align-items: center;">
    <div>
      <img src="https://github.com/user-attachments/assets/27675ef7-392a-42d1-a9bc-e638e0a40e11">
      <figcaption style="text-align: center;">6a; Scale system illustration.</figcaption>
    </div>
    <div>
      <br><img src="https://github.com/user-attachments/assets/8d0e6fa8-13e1-4cde-aa0a-8de9ecc689a9">
      <br><figcaption style="text-align: center;">6b; Scale system control hub-box.<br>The box contains the breakout boards that are connected to the Arduino and the docking ports. On the side of the box, channel numbers are marked for each port, so that it fits the channel on the Qwiic MUX that it is connected to.</figcaption>
    </div>
    <div>
    <br><img src="https://github.com/user-attachments/assets/b8a0815a-6c03-449c-b1c5-0dd54ad85b15">
    <br><figcaption style="text-align: center;">6c; Scale system control communication cable.<br>The cable is a simple 4-core cable with a 4-PIN Pigtail connector for easily connecting to the hub-box on one end, and a 4-pos connector to connect to the scale on the other. In order to connect the scales to the control hub, connect the scale end of the cable to the scale, spread the cable conveniently to the instrumentation rack and connect to one port of the hub-box.</figcaption>
    </div>
    <div>
    <br><img src="https://github.com/user-attachments/assets/9e4fa71d-e9e0-483e-8ced-23121a80ec30">
    <br><figcaption style="text-align: center;">6d; The scale.</figcaption>
    </div>
  </div>
</figure>


### 4. Connect all the hardware to the Arduino
In order for the Arduino microcontroller to receive the data smoothely and without failtures, the devices must be connected properly. Figure 7 schematize the wiring diagram:
<figure>
  <img src = "https://github.com/user-attachments/assets/63127fc2-eab4-4d5c-8b07-724631dcf009" width = "1000" height = "650">
  <figcaption>Figure 7: The systems's wiring diagram</figcaption>
</figure>
<br>

#### Wiring list 
The colors of the lines in Figure 7 refer to different lines in the cables connecting the devices to the Arduino according to the following wiring list. Each entry in the list is formatted as "Device wire ID (function in the device) - pin on Arduino":
1. To connect the light control system (2 wires):
   * Black (ground) - to any 'gnd'
   * White (signal) - to digital channel 13

2. To connect the sensor box (4 wires):
   * Black (ground) - to any 'gnd'
   * Red (voltage) - to 5V channel
   * White (photoresistor) - to analog channel A0
   * Green (DHT) - to digital channel 8

3. To connect the Scale System (4 wires):
   * Black (ground) - to any 'gnd'
   * Red (voltage) - to 3.3V channel
   * Yellow (signal) - to 'SCL' channel
   * Blue (signal) - to 'SDA' channel

### 5. Set up the Arduino
Before running the main script on the Raspberry Pi, make sure to load the appropriate code for the operation that you want on the Arduino.

1. Connect the Arduino to the Raspberri Pi with a USB-A to USB-B cable.
2. Open the relevant arduino code:
   * [arduino_code_0](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_0/arduino_code_0.ino) - For light control only mode.
   * [arduino_code_1](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_1/arduino_code_1.ino) - For light control & data analysis mode.
   * [arduino_code_2](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_2/arduino_code_2.ino) - For initial set up and calibration of the Scale System.
3. Load the relevant code onto the Arduino using the IDE. (see instructions [here](https://docs.arduino.cc/learn/starting-guide/the-arduino-software-ide)).
4. Once all the hardware components are connected to the Arduino, open 'Serial Monitor' to check that the arduino operates smoothely, acquiring the neccesary data in every mode.


## Operations

$${\color{red}\text{Begin comment ********}}$$

*This section is organized in a difficult way. Specifically, the definition of operation modes and the definition of how to configure things are intermingled and this is too confusing. I suggest a different structure below*

$${\color{red}\text{End comment ********}}$$

### Operation overview
The *environmental system* can be used in two distinct *operation modes*:
1. Light cycle only - The system controls the light switches and does not read sensors. In this mode the system **TBD: Does it save data? Does it send data to the user?**
2. Light and sensors - The system controls the lights and also reads sensors.

The user chooses the operation mode by loading different codes to the Arduino and by manupulating a single configuration file on the Raspberri Pi. This section instructs how to run the system in example cases of the two operation modes. For the full information about how to use the configuration file see [this manual](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/config_files/How%20to%20use%20the%20config%20file.md).

### To start running the system

After creating the configuration file, the user needs to edit the `startup_script.sh` shell script and point to the full path of the configuration file by changing this line: <br>
`
py_script_name="$parent_path/control_main.py --config=/path/to/repo/acoustic_chamber_environment_control/config_files/config_file_name.yaml"
` 
<br> 

Editing the `startup_script.sh` shell script is needed since the system is set to execute it automatically on start-up. This prevents light cycle failues if the system accidently boots (e.g. after a power fluctuation) to ensure minimal disruption for the animals.

Then, to start running the *environmental system* the user can:

* Boot the Raspberri Pi.
* Alternatively,
  * Open a terminal on the Raspberri Pi.
  * Change the directory to the root directory of this repository.
  * Execute the shell script `startup_script.sh`

### Day to day operations
#### 1. Changing the light cycle
#### 2. Configuring the system's reports
#### 3. Housing a new bird
#### 4. Removing a bird



### Operation modes
### *The "Light cycle only" operation mode*
This is a minimalistic operation mode that allows using the setup only for controlling the light cycle. In this mode **TBD: what will be controlled? What sensors are registered? What data is saved and sent to user?**
To work in this mode:
1. Load the Arduino microcontroller with [arduino_code_0](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_0/arduino_code_0.ino)
2. Edit the [config file](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/config_files/config_1.yaml): 
   * Write values in one of `sunrise` & `sunset`, `stable_date` or `days_offset` & `hours_offset` according to the [config file user manual](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/config_files/How%20to%20use%20the%20config%20file.md) in order to achieve the desired result.
   * Make sure that both `dataReadingAndSaving` values are 0.
3. Run the script.
4. See that it operates properly. The lights in the acoustc chambers should be turned on/off based on your parameter settings.<br>
The terminal should look like this:
$${\color{red}insert picture}$$


### The *Light and sensors* mode
In order to use the setup for data acquisition (sensor, weight), follow these instructions:
1. Load the Arduino microcontroller with [arduino_code_1](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_1/arduino_code_1.ino).
2. Edit the [config file](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/config_files/config_1.yaml):
  * Edit light cycle parameters based on your needs.
  * For sensor data acquisition:
    * Set `sensorOutputBasePath` with the path to the output folder that will contain the sensor data, and make sure that the folder exists.
    * Set `sensorDataReadingAndSaving` to 1 
  * For weight data acquisition 
    * Set `scaleOutputBasePath` with the path to the output folder that will contain the scale data, and make sure that the folder exists.
    * Set `scaleDataReadingAndSaving` to 1
    * Determine the time when you want the daily weight report to be sent to slack in `sendWeightReportToSlackTime`
    * **IMPORTANT!** Enter the names of the birds that are being weighed in the channel number which their scale is connected to. The script will generate a folder for each bird in the scale output folder, in which their continuously accumulating weight report will be stored.
    * **MOST IMPORTANT!** Calibrate the scales:
      1. Exit the startup script and the running main control script. If there are birds in the chambers, make sure to temporary keep the lights in the acoustic boxes controlled by this setup in the correct on/off configuration manually, until the calibration proccess is over.
      2. Load Arduino with [arduino_code_2](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_2/arduino_code_2.ino)
      3. On the Arduino IDE, click `Tools` -> `Serial Monitor` or click on the top right Serial Monitor logo. ![Screenshot 2024-07-22 at 11 08 46](https://github.com/user-attachments/assets/3e3f0b35-7ee0-4f2b-8f74-7176461e129b) 
         When the serial monitor opens, it should immediately start communicating with the MUX system and notify the user with the status of every connected scale and instructions on how to calibrate. Be prepared with a calibrating item with known exact weight (preferably within a range of a few grams).
      4. Follow instructions on screen to calibrate the connected scales (see full calibration guide in the [Scale System setup guide](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/cf7c2d09ca352680ac4c0b2b953d89da0c118fb5/User%20Guides/Scaling%20System%20Setup%20Guide.md).
      5. Once calibration is done, make sure to reload the [arduino_code_1](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_1/arduino_code_1.ino) to the Arduino and then boot the system.
