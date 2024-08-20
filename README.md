# Acoustic chamber environment control setup
To control light cycles and monitor acoustic chamber environment we operate a control setup, guided by a script that runs continuously on a Raspberry Pi computer. This script communicates with an Arduino microcontroller, which sends various information back to the Raspberri Pi every second. 

The Raspberry Pi script, that should automatically launch at start-up, has several responsibilities:
 * Determine and control whether the lights inside the acoustic boxes should be turned on/off according to user preference.
 * Read and store sensor data in .csv files (temprature, humidity, light)
 * Read and store weight data of birds that are being monitored.
 * Store data locally and on [storWIS drive](https://github.com/NeuralSyntaxLab/lab-handbook/wiki/Lab-Operations-and-Procedures#storwis).

It does so by accumulating sensor and weight data gathered by the Arduino, which is connected to several [hardware](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/cf7c2d09ca352680ac4c0b2b953d89da0c118fb5/User%20Guides/Hardware%20Assembly%20Guide.md) devices, and sending commands back to the light setup through the Arduino.

Each setup is capable of controlling and gathering data from up to 8 acoustic boxes. Therefore each setup, named *environmental system*, is given its unique environmental system ID. In our recording rooms we can maintain different environmental conditions and record data for each group of birds individually, by manipulating some parameters in the config file and loading different codes on the Arduino microcontroller.

## Setup schematic diagram

<img src = "https://github.com/user-attachments/assets/3f617a45-ea5e-4f6d-8036-1d348ed8e47e" width = "1000" height = "850"> <br>


## Table of contents
* **Components** 
* **Preperations**
  1. [Setting up the Raspberri Pi](#setting-up-the-raspberry-pi)
  2. [Preparing hardware and connecting to Arduino](#preparing-hardware)
  3. [Setting up Arduino](#setting-up-arduino)
* **Operations**
  1. [Light control mode](#light-control-mode)
  2. [Light control & data acquisition mode](#light-control--data-acquisition-mode)

<br>

## Components
1. **Raspberry Pi 4 model B minicomputer**
2. **Arduino Uno R3 microcontroller**
3. **Light control system** - consists of 1 control box which connects to relay modules on a maximum of 8 acoustic boxes per control setup. <br>
    1. Relay module 5Vdc 10A (multiple)
    2. 4-Core electric cable
    3. JST-SM Pigtail connector (3-PIN) male-to-female (multiple)
    4. Terminal block
    5. JST-SM Pigtail connector (2-PIN) male-to-female
    6. 5V, min.1A AC/DC power source
    7. Jumper wires
    8. Plastic box
4. **Sensor box** - consists of a DHT22 sensor and a light sensor. Up to 1 box per setup. <br>
      1. DHT22 humidity & temprature sensor + Analog sensor cable (should come with)
      2. Light dependant resistor
      3. 10 kOhm resistor
      4. JST-SM Pigtail connector (4-PIN) male-to-female
      5. 4-Core electric cable
      6. Jumper wires
      7. Plastic box
5. **Scale System** - consists of 1 control box capable of connecting up to 8 scales. Up to 1 system per setup. <br>
    1. Self built scale:
       * Mini Load cell 500g straight bar
       * for full description and part list of the self-built scale go [here](scale_system_documentation/scale_design.md)
    2. SparkFun QwiicScale NAU7802
    3. 4 Circuit Picoblade Male-to-Female plug 425mm (multiple)
    4. JST-SM Pigtail connector (4-PIN) male-to-female (multiple)
    5. SparkFun Qwiic MUX breakout
    6. Flexible Qwiic cables (multiple)
    7. Flexible Qwiic breadboard cable
    8. 4-Core electric cable
    9. Plastic box


# Preperations
## Setting up the Raspberry Pi
When using a new Raspberry Pi, it has to undergo several steps, described in the [configuration guide](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/cf7c2d09ca352680ac4c0b2b953d89da0c118fb5/User%20Guides/Raspberry%20Pi%20Configuration.md), before using it to operate the environmental system. 

If you are using an already used Raspberry Pi, move on to preparing the hardware.
Return to the [configuration guide](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/cf7c2d09ca352680ac4c0b2b953d89da0c118fb5/User%20Guides/Raspberry%20Pi%20Configuration.md) if issues arise when running the `control_main.py` script.

## Preparing hardware
### Components
The control setup contains several hardware devices:
1. A Raspberry Pi minicomputer.
2. An Arduino Uno microcontroller.
3. Light control system - consists of 1 control box which connects to relay swiches on a maximum of 8 acoustic boxes per control setup.
4. Sensor box - consists of a humidity & temprature sensor (DHT) and a photoresistor (light sensor). Up to 1 box per setup.
5. Scale system - consists of 1 control box with SparkFun QwiicScale MUX, capable of connecting up to 8 scales. Up to 1 system per setup.

### Schematic diagram
![Extended envSys setup Arduino pinout diagram 1](https://github.com/user-attachments/assets/2519467c-20a3-4ffc-a414-5b14d84704b4)

### Hardware Assembly and preperations
Check out the [assembly guide](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/cf7c2d09ca352680ac4c0b2b953d89da0c118fb5/User%20Guides/Hardware%20Assembly%20Guide.md) to see how to build each device.

* #### Preparing the light control system
*Add picture of light control box and explain how to connect to the relay boxes

* #### Preparing the sensor box
The sensor box should look like this: <br>
<img src = "https://github.com/user-attachments/assets/cd4a81d1-e175-4800-9989-cbe03c928424" width = "600" height = "600"> <br>

It contains:
* DHT sensor (for detecting humidity, temprature)
* Photoresistor (for detecting light intensity)
* A connector for the communication cable (for receiving voltage - red and black wires, and sending data - green for DHT, white for photoresistor)

In order to connect the sensor box to the setup, simply connect the communication cable (guide for making the cable [here](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/cf7c2d09ca352680ac4c0b2b953d89da0c118fb5/User%20Guides/Hardware%20Assembly%20Guide.md)) to the box on the connector side, and to the arduino on the breadboard side according to the [instructions](#connecting-the-hardware-to-the-arduino)

<img src = "https://github.com/user-attachments/assets/d995c5bd-1337-4e95-a3b7-6ce7065a55e3" width = "400" height = "500">



* #### Preparing the scale system
See [Scale System setup guide](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/7b98ca46d210fc865f576b8630c2cdef0f82fe2f/User%20Guides/Scaling%20System%20Setup%20Guide.md).


### Connecting the hardware to the Arduino
In order for the Arduino microcontroller to receive the data smoothely and without failtures, the devices must be connected properly as explained here:
<img src = "https://github.com/user-attachments/assets/63127fc2-eab4-4d5c-8b07-724631dcf009" width = "900" height = "750">


1. To connect the light control system (2 cables):
   * Black cable (ground) - to any 'gnd'
   * White cable (signal) - to digital channel 13

2. To connect the sensor box (4 cables):
   * Black (ground) - to any 'gnd'
   * Red (voltage) - to 5V channel
   * White (photoresistor) - to analog channel A0
   * Green (DHT) - to digital channel 8

3. To connect the Scale System (4 cables):
   * Black (ground) - to any 'gnd'
   * Red (voltage) - to 3.3V channel
   * Yellow (signal) - to 'SCL' channel
   * Blue (signal) - to 'SDA' channel

## Setting up Arduino
Before running the main script on the Raspberry Pi, make sure to load the appropriate code for the operation that you want on the Arduino.

1. Connect the Arduino to the Raspberri Pi with a USB-A to USB-B cable.
2. Open the relevant arduino code:
   * [arduino_code_0](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_0/arduino_code_0.ino) - For light control only mode.
   * [arduino_code_1](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_1/arduino_code_1.ino) - For light control & data analysis mode.
   * [arduino_code_2](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_2/arduino_code_2.ino) - For initial set up and calibration of the Scale System.
3. Load the relevant code onto the Arduino using the IDE. (see instructions [here](https://docs.arduino.cc/learn/starting-guide/the-arduino-software-ide)).
4. Open 'Serial Monitor' to check that the arduino operates smoothely, acquiring the neccesary data in every mode


# Operations
When operating the  `Acoustic chambers environment control` setup, there are a few things to look into:
1. Light cycle - determine when the lights should be turned on/off.
2. Data recording and saving:
   * From the sensor box (DHT, light)
   * From the Scale System

Each setup is capable of controlling and gathering data from up to 8 acoustic boxes. Therefore each setup, named *environmental system*, is given its unique environmental system ID. In our recording rooms we can maintain different environmental conditions and record data for each group of birds individually, by manipulating some parameters in the config file and loading different codes on the Arduino microcontroller.

** For more information about the parameters see [how to use config file](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/config_files/How%20to%20use%20the%20config%20file.md).

Once all of the prerequisites are fulfilled, we can go on and determine the operation mode.

## Light control mode
In order to use the setup only for manipulating the light cycle, follow these instructions:
1. Load the Arduino microcontroller with [arduino_code_0](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_0/arduino_code_0.ino)
2. Edit the [config file](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/config_files/config_1.yaml): 
   * Write values in one of `sunrise` & `sunset`, `stable_date` or `days_offset` & `hours_offset` according to the [config file user manual](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/config_files/How%20to%20use%20the%20config%20file.md) in order to achieve the desired result.
   * Make sure that both `dataReadingAndSaving` values are 0.
3. Run the script by executing the `startup_script_sh` in terminal, or by rebooting (the script should auto-start)
4. See that it operates properly. The lights in the acoustc boxes should be turned on/off based on your parameter settings.<br>
The terminal should look like this:
 insert picture...


## Light control & data acquisition mode
In order to use the setup for data acquisition (sensor, weight), follow these instructions:
1. Load the Arduino microcontroller with [arduino_code_1](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_1/arduino_code_1.ino).
2. Edit the [config file](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/config_files/config_1.yaml):
  * Edit light cycle parameters based on your needs.
### For sensor data acquisition
  * Set `sensorOutputBasePath` with the path to the output folder that will contain the sensor data, and make sure that the folder exists.
  * Set `sensorDataReadingAndSaving` to 1 
### For weight data acquisition 
  * Set `scaleOutputBasePath` with the path to the output folder that will contain the scale data, and make sure that the folder exists.
  * Set `scaleDataReadingAndSaving` to 1
  * Determine the time when you want the daily weight report to be sent to slack in `sendWeightReportToSlackTime`
  * IMPORTANT! Enter the names of the birds that are being weighed in the channel number which their scale is connected to. The script will generate a folder for each bird in the scale output folder, in which their continuously accumulating weight report will be stored.
  * MOST IMPORTANT! Calibrate the scales:
      1. Exit the startup script and the running main control script. Make sure to temporary keep the lights in the acoustic boxes controlled by this setup in the correct on/off configuration manually, until the calibration proccess is over.
      2. Load Arduino with [arduino_code_2](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_2/arduino_code_2.ino)
      3. On the Arduino IDE, click `Tools` -> `Serial Monitor` or click on the top right Serial Monitor logo. ![Screenshot 2024-07-22 at 11 08 46](https://github.com/user-attachments/assets/3e3f0b35-7ee0-4f2b-8f74-7176461e129b) 
         When the serial monitor opens, it should immediately start communicating with the MUX system and notify the user with the satatus of every connected scale and instructions on how to calibrate. Be prepared with a calibrating item with known exact weight (preferably within a range of a few grams).
      4. Follow instructions on screen to calibrate the connected scales (see full calibration guide in the [Scale System setup guide](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/cf7c2d09ca352680ac4c0b2b953d89da0c118fb5/User%20Guides/Scaling%20System%20Setup%20Guide.md).
