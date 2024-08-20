# Scale System setup guide
## 1. Overview
The Scale System is a setup designed to monitor the weight of multipe, freely-behaving birds directly while in their cage (possibly while recording the birds' songs, monitoring their movement or recording neural data directly from their brain), in order to detect weight loss as a marker for their health condition.

The weighing is conducted by placing a load-cell-based weighing device (scale) in the bird's cage. This device is connected to an ADC breakout board (NAU7802) which helps convert and amplify the signal from the load cell to an I2C signal, readable with a microcontroller from which we can extract the weight in grams. The data collection is controlled by a script that runs continuously on the minicomputer, receives weighing data from the microcontroller, and stores it in '.csv' files.

Each Scale System is capable of connecting up to 8 weighing devices per microcontroller with the help of another breakout board (MUX), which enables communication with multiple I2C devices simultaneously.

## 2. Part list
The Scale System consists of the following items:
  1. Raspberry Pi (or similar) minicomputer
  2. Arduino UNO microcontroller
  3. Control box
      1. Sparkfun Qwiic MUX breakout board
      2. Sparkfun Qwiic Scale NAU7802 breakout board (multiple)
      3. Flexible Qwiic cables 
      4. Docking points (4-PIN JSM-ST Pigtail connector - male, multiple)
  4. Self-built weighing devices (multiple)
     1. Mini load cell 500g
     2. 3D printed perch, customized to be screwed onto the load cell
     3. Cylindrical steel weight, also customized to screw the load cell onto it
     4. 4-pin connector, to easily connect and disconnect the scale to/from the control system (for example - [Circuit Picoblade Male-to-Female plug 425mm (multiple)](link))
  5. Communication cables
     1. 4-PIN JSM-ST Pigtail connector (female)
     2. Circuit Picoblade Male-to-Female plug 425mm

see [general part list](link) for full list of parts and where to get them.

### Scale System setup schematic overview

<img src = "https://github.com/user-attachments/assets/6afa6e9a-1b17-4121-80c2-9fbb5fe0f42a" width = "1180" height = "800"> <br>

### Assembly
See [Scale System assembly guide](link) for assembly instructions for each part.

## 3. Wiring the Scale System 


Before operating the Scale System setup, follow these instructions to connect all the pieces together:
1. Open the control box, and connect as many docking points (NAU7802 board + Pigtail connector male) to the MUX as you plan to use (When adding/removig scales at any point, it will be neccesary to stop the main script, open the box and re-wire the docking points. NAU7802 boards that are connected to the MUX but not to a scale can cause issues with the code). Write down under each docking point to which channel on the MUX board it is connected to.
2. Place scales in the corner of the cages of the birds you wish to weigh with their connector sticking out.
3. Connect the communication cable to the scale inside the acoustic box and spread the cable through the hole in the side of the acoustic box all the way to the control center (Repeat for all scales you wish to connect)
4. Connect the communication cable's other side to a docking point on the control box. IMPORTANT! make sure that you know which bird is connected to which channel on the control box (and MUX accordingly)
5. Connect the Qwiic MUX to the Arduino microcontroller through the hole in the control box lid, using a Flexible Qwiic breadboard cable (connector on one side and 4 separate pins on the other):
  * Black pin (ground) - to any 'gnd'
  * Red pin (voltage) - to 3.3V channel
  * Yellow pin (signal) - to 'SCL' channel
  * Blue pin (signal) - to 'SDA' channel

<img src = "https://github.com/user-attachments/assets/87bd1f43-7030-40bb-8998-025d49eb796a" width = "925" height = "650"> <br>


6. Connect the Arduino microcontroller to the minicomputer.
7. Connect the minicomputer to the power source, screen, keyboard and mouse. Continue to the next step to operate the system on the minicomputer.

## 4. Operating the system
Once the system is up and connected, wait for the minicomputer to start up and follow the instructions:

### 1. Calibrating the scales
1. Exit the automaticly-started control script.
2. Load Arduino with [arduino_code_2](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/scale_system_add/arduino_codes/arduino_code_2/arduino_code_2.ino) (see instructions [here](https://docs.arduino.cc/learn/starting-guide/the-arduino-software-ide)).
3. Open the Serial Monitor: <br>
On the Arduino IDE, click `Tools` -> `Serial Monitor` or click on the top right Serial Monitor logo. ![Screenshot 2024-07-22 at 11 08 46](https://github.com/user-attachments/assets/3e3f0b35-7ee0-4f2b-8f74-7176461e129b) 
When the serial monitor opens, it should immediately start communicating with the MUX system and notify the user with the satatus of every connected scale and instructions on how to calibrate. Be prepared with a calibrating item with known exact weight (preferably within a range of a few grams).

* In general, output on the serial monitor will show detected scales and their calibration values (zero-offset and calibration factor) in the setup phase.
* A scale is detected on channel X if a docking port (NAU7802 board) is connected to that channel on the MUX board.
* After the setup phase, a new line of data from all 8 channels is given every second in the format `c0: 0.00` for channel 0, `ch1: 2.14` for channel 2 and so on.
* Some disconnected channels give numbers that are not 0 or none because the Arduino already has information about previous scales that were connected to those channels stored in its memory. Just ignore them and only look for the relevant channels.
* At Initial setup of a new Arduino, scales should not have calibration values, and you will have to follow the on-screen instructions in the serial monitor and calibrate each connected scale.
* For every change - relocation, addition ,cleaning of a scale etc. - **re-calibration of the scale is neccesary.**

4. Wait for the setup phase to complete, click on the Message panel to pass input to the Arduino, write `c` and press enter. Calibration process will now begin and indicative prompts will appear.
  * At initial setup, the Arduino will not detect calibration values for any scale and calibration proces will start automatically!

5. Follow instructions on screen to complete the calibration process for the desired scales (for more information see [arduino code guide](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/9a08e14dcccb3a1217388fe7d782128831e4b6a5/arduino_codes/Arduino%20code%20guide.md)).

#### Example 1: Calibrating in and already-used setup, but with new scale wiring
<img src="https://github.com/user-attachments/assets/0ef7554e-a696-4800-8037-2b2d359d2b2f" width="1150" height="500">

In this example, the first lines show that docking ports 0 and 6 are "active" (meaning that they are connected to the MUX board). Other ports / channels are not detected because they are not connected to the MUX board. The output will include the zero offset and calibration factor that are saved on the Arduino memory for these ports. 
After the setup phase in which the Arduino passed information about channels 0 and 6, it moves on to the next phase. 
Now every second a new line of data is given. We can see that it is a used setup because weighing data is given for disconnected scales. We will focus on data given from channels 0 and 6.

#### Calibration process for scale 0 looks like this:

![Arduino IDE calibration example 1_2](https://github.com/user-attachments/assets/152b89ef-84ee-4ad6-ab60-cbb147fc3d35)

1. After entering `c` in the message panel, the calibration began and the first prompt was given.
2. User input was 0 - to calibrate scale on port 0.
3. Next prompt instructed to clear the scale from any weight and press any key to continue - in this case the user input was `k` (could be any key).
4. Next prompt indicated the new zero offset saved to the Arduino memory.
5. Next prompt instructed to put known weight on the scale and press any key. In this case user put a known weight of 2.14 grams on the scale, wrote `k` in the message panel and pressed enter.
6. Next prompt instructed to enter the known weight in grams in the message pael and press enter. no apostrophe needed! User entered `2.14`
7. Next prompt indicated the new calibration factor saved to the Arduino memory, followed by new scale reading after calibration.
8. Calibration is complete and the Serial monitor keeps showing new lines of data.
9. In order to calibrate the scale on port 6, enter `c` in the message panel again and choose port 6.


### 2. Edit config file
Open the `Acoustic Chambers Environment Control` folder. Click on the `config_files` folder and open the relevant config file for editing (If not familiar, read [how to use the config file](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/46e9405cdcb7c96c5ceae5696ab63bdf03effe7b/config_files/How%20to%20use%20the%20config%20file.md) for more information).

Here, you will need to enter the names of the birds that have weighing devices in their cage in the `Channels` section.
Each docking point (channel) is connected to one scale. Write the name of the bird that connected to each channel with apostrophes.
You also need to make sure the the `scaleDataReadingAndSaving` has the input of **1**, and that the `scaleOutputBasePath` is correct.
At last, enter the time of day you wish to get the daily weight reports sent to the lab's `monitor_alerts` channel. 

For example - `channel1: 'lr17'`, send reports daily at 12:05PM

![Example 1](https://github.com/user-attachments/assets/35ef96ff-7ee1-4e23-ad93-af856b1b6240)

### 3. Re-run the main control script
After calibrating the scales and updating the config file, the system is ready to go.
In order to run the main control script, simply reboot the minicomputer. The script should run automatically at startup.

* It is recommended to test the system to see that it works properly before leaving it to run. You can run the script by opening the `Acoustic Chambers Environment Control` folder, and double clicking the `startup_script.sh` script and choose to execute it (not in terminal) when prompted.
* You can also open the terminal and run the following comand (Change paths accordingly):
```
python /path/to/script/main_control.py --config=/path/to/config/file
```


