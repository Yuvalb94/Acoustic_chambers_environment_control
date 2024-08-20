Since we are responsible for the well-being of the labs, we aim to monitor and control different aspects of the bird environment. Controlling light cycles can directly affect the bird's singing.
As part of monitoring and controlling the acoustic chamber environment, we use several components connected to an Arduino microcontroller controlled by a Raspberry Pi unit. 
We monitor temperature, humidity, light intensity, and bird's weight and control light cycles within the acoustic chamber.

To monitor the chamber environment and control its light cycle,  Several components are connected to the Arduino: 

 * [DHT22 Temperature and humidity sensor](https://il.farnell.com/dfrobot/sen0137/dht22-temp-humidity-sensor-arduino/dp/3517874) - a digital component outputs a digital signal. 
 * [A light-dependent resistor](https://il.farnell.com/advanced-photonix/norps-12/light-dependent-resistor-1mohm/dp/327700?st=327700) -  an analog component connected in series with a resistor. Outputs an analog signal. 
 * [A 5V trigger relay module](https://il.farnell.com/mcm/83-17990/5v-trigger-relay-module-for-arduinoraspberry/dp/2801412?st=2801412) - receives a digital input turning on /off the light inside the acoustic chamber. 
 * A [Qwiic scale amplifier](https://www.sparkfun.com/products/15242) and a [500g mini load cell straight bar](https://www.digikey.co.il/en/products/detail/sparkfun-electronics/SEN-14728/9555602?s=N4IgTCBcDaILIEkByCAEAZA8gQQCKoGEBRddVAVgAZKBxVAZQBUAlbBGgCUdQCFtmQAXQC%252525252BQA) - this components serve as a scale to measure birds weight.

Every acoustic chamber has a relay module controlling the chamber's light cycle.
Except for the trigger relay module, the rest of the sensors are assembled in a box placed inside the acoustic chamber and connected to the Arduino via a [9-pin D-Sub](https://www.digikey.co.il/he/products/detail/mikroelektronika/MIKROE-2092/5804553?s=N4IgTCBcDaILIEkDSAlA8gUQLRgAwE4IBdAXyA) cable and a [connector](https://www.digikey.co.il/he/products/detail/assmann-wsw-components/A-DF-09-LL-Z/5051922).

# Sensor box

## Components and tools for sensor box assembly:
 * DHT22 temperature and humidity sensor.
 * Light-dependent resistor (LDR).
 * 10 kilo-ohm resistor. 
 * A plastic box ([this for example](https://www.digikey.co.il/he/products/detail/bud-industries/CU-1943/439229))
 * Qwiic scale amplifier
 * 500g mini load cell straight bar
 * 9 pin D-Sub cable
 * 9 pin D-Sub connector and compatible nuts and bolts(usually 3m size is sufficient)
 * Jumper wires
 * Holdering station
 * Hot glue gun
 * A tool to make holes in the plastic box (I used a soldering pencil, not from the soldering station!)
 * A multimeter
 * An electrical type (such as isolierband)

## Sensor box assembly
  * Make a small hole for the light-dependent resistor cable in the box lid.
  * Make a circular hole for the light-dependent resistor.
  * Make a small hole for the mini-load cell cables. 

Glued sensors onto the box with:
<img src="https://github.com/NeuralSyntaxLab/lab-handbook/assets/111876216/85f5a481-1bac-4484-97f3-9f1f4df31efc" width="200" height="400">

* Glue  the temperature and humidity sensor and the light-dependent resistor onto the box lid (as in the picture above)

* Make a hole for the D-Sub connector on the side of the box.

D-Sub connector connections:
<img src = "https://github.com/NeuralSyntaxLab/lab-handbook/assets/111876216/55b9be4e-38b1-48cc-af0b-07846da60cd7" width="300" height="200">


* If you have a male D-Sub connector, cut the male side of your D-Sub cable and expose its wires, or vice versa if you have a female D-Sub connector.

* Connect the D-Sub connector to the compatible side of the cable. At the connector back (the side that is not connected to the cable), there are 9 
  numbered soldering cups. 
  Using the multimeter, identify which soldering cup is connected to which exposed cable. 
  For example, touch the red wire with one end of the multimeter and the soldering cup with the other. If the multimeter made a bip sound, this means they 
  are connected.  

* Identify the soldering cup that is connected to the red D-Sub wire. This will be connected to the 5V input.
* Identify the soldering cup that is connected to the Black D-Sub wire. This will be connected to the ground input.


* Solder one leg of the LDR to one leg of the 10kohm resistor. This will be the output leg. Solder the other leg of the LDR to 5V input and the other leg of the 10 Kohm resistor to ground. As in the picture below
<img width="400" alt="image" src="https://github.com/NeuralSyntaxLab/lab-handbook/assets/111876216/12172c92-33e1-450e-b885-49c7b61af875">

 *  Using the multimeter, identify a soldering cup and its corresponding D-Sub wire (for example, green wire to cup number 2). Solder the output leg to an individual cup. This will be connected to Arduino pin A0 via the D-Sub cable.
 * The [DHT22 sensor](https://il.farnell.com/dfrobot/sen0137/dht22-temp-humidity-sensor-arduino/dp/3517874), has a connector of itself, and it comes with 
  a specific cable with red (5V input), black (ground input) and green (digital output) wires.As in the picture below :
<img width="300" alt="image" src="https://github.com/NeuralSyntaxLab/lab-handbook/assets/111876216/9496dd76-77f1-4c3d-a0f5-1931c2456bb7">

 * Solder the DHT22 red  wire to the 5V input, solder the DHT22 black wire to the ground input, and solder the green wire to a desired soldering cup (Note! identify which is the corresponding D-Sub wire). This digital input for the temperature and humidity sensor will connect to Arduino pin 8.
   
 * Preparing the Qwiic scale amplifier: Solder Four 90-degree legs to each of the four following inputs: 1.GND 2.3V3 3.SDA 4.SCL  (can also be done with soldering of jumper wires directly to the amplifier). Glue the amplifier to the bottom of the box.
<img width="600" alt="image" src="https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/assets/111876216/7c73d9d4-f4a0-4439-b584-d85cc4466705">

  * Solder the GND amplifier input to ground.
  * Solder the 3v3 input to an individual solder cup (Note! Identify which is the corresponding D-Sub wire).
  * Solder the SDA  output to an individual solder cup (Note! Identify which is the corresponding D-Sub wire).
  * Solder the SCL  output to an individual solder cup (Note! Identify which is the corresponding D-Sub wire).

* Pass the mini-load cell cables through the hole you made earlier and connect them to the Qwiic scale amplifier using the green, built-in clips on the amplifier. As in the picture below
 
   <img width="400" alt="image" src="https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/assets/111876216/5ad10c56-29b8-4ede-a90c-5b7c2ba79334"> 

* After you've finished soldering, make sure to cover every conducting part with electrical type.
* Push the D-Sub connector into its hole in the box (the one that you passed wired through, as in the picture).
  <img width="400" alt="image" src="https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/assets/111876216/ebfd8951-83d1-40f6-ab44-5be5dc9398c5">

* To each identified wire(wires which you know soldered to their corresponding solder cups), solder jumper wire that will fit the Arduino pins. similar to the picture below (Note, the wires are not fully assembled in that picture)

   <img width="668" alt="image" src="https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/assets/111876216/aaa3d665-5aae-4de2-b287-1294b94375d8">

* Place the sensor box inside the acoustic chamber and pass the D-Sub cable through the hole in the left side of the chamber.

  # 5V trigger relay module (light switch)

  ## Components and tools for 5V trigger relay module:
   * 5V trigger relay module.
   * Screwdrivers (regular and small for electronics).
   * Hot glue gun.
   * An electrical type (such as isolierband).
   * 20cm power cable (with two exposed sides).
   * Wire stripper.
   * Permanent marker.
   * Power drill.
   * Terminal connector  : <img width="200" alt="image" src="https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/assets/111876216/ee5fff8e-f836-4085-b57d-30b5ff6c3a7d">
   * Cutter.

   ### Light switch assembly
  * Power connection and switches are at the right side of the acoustic chamber(if you are standing in front of its door). Check that ventilation (top switch indicated with blue LED) and light (bottom switch indicated with red LED) work properly.
  * Disconnect the power cord from the acoustic box, and disassemble the switch panel on the right of the acoustic chamber by unscrewing the top and bottom screws.
    <img width="1271" alt="image" src="https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/assets/111876216/e9ae1528-8ed9-4252-8ad5-bf8582f16d98">
  * Mark the bottom white wire(in the picture, it is marked  with red, and it's the rightmost wire). As in the picture above, there are 6 cables: 2 blue, 3 white(the rightmost wire is white but colored with red), and 1 red cable. The ventilation switch is connected with blue, red, and white wires. The light switch is connected with 1 blue and 2 white wires.
  * Cut both light switch white wires(the one you have marked and the one adjacent to it)
  * Expose all of the white ends, two of  which have legs and are connected to the switch and two of which are coming out of the box.
  * Cut one of the 3 wires in the exposed power cord on both sides and expose the two  remaining wires such that you'll have conductive wire exposed.
  * Connect each of the  two exposed white wires from the box to the terminal connector.On the other side of the terminal connector, connect one leged white cable with one of the exposed power cord wires and do the same with the remaining power cord and legged white wire, as in the pictures below:

       <img width="527" alt="image" src="https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/assets/111876216/49038266-f747-45f8-8d9d-e3ef64d4a621">
       
       white cable marked red is connected together with the blue power cord wire at one end of the terminal connector. The other side is connected to the box. The other white-legged wire is connected together with the brown power cord cable.

* Connect the two power cord exposed wires to the ON inputs in the power resistor. one wire in the middle and the other at the top  left side (according to the picture below).
  
    <img width="385" alt="image" src="https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/assets/111876216/e0f45642-bb96-4c59-9d73-0797a3ae801c">

* Secure the power cord and its connected switch on top of the acoustic chamber using a type 
* Connect the three legs on the right side (according to the picture above) to the Arduino, to their signs: plus sign to 5V, minus sign to ground, and S - signs signal; this should be connected to Arduino pin 13.

# Arduino pinout 
This will describe to which pin each component should be connected, according to [This Code](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/blob/main/arduino_code/arduino_code.ino).

 * Light-dependent resistor - Arduino pin A0. Should also be connected to 5V and ground
 * Temperature and humidity sensor Arduino pin 8. Should also be connected to 5V and ground
 * Relay trigger module - Arduino pin 13. Should also be connected to 5V and ground
 * Qwiic scale amplifier  - Arduino pins SDA and SCL (according to markings on the amplifier). Should also be connected to 3V3 and ground.


# Scale System
## 1. Self-built weighing device (scale)
The self-build scale consists of the following items:
* Mini load cell 500g
* 3D printed perch, customized to be screwed onto the load cell
* Cylindrical steel weight, also customized to screw the load cell onto it
* 4-pin connector, to easily connect and disconnect the scale to/from the control system (for example - [Circuit Picoblade Male-to-Female plug 425mm (multiple)](link))

see [scale design](https://github.com/NeuralSyntaxLab/acoustic_chamber_environment_control/tree/0fc50bf446f8784b286c2851cd4cca4fbe7e9609/scale_system_documentation) for further information and specifics.

To asemble the scale:
1. Solder the wires of the load cell to a 4-pin connector
2. Screw the load cell to the 3D printed perch on one side and to the steel weight on the other side, making sure that:
   * The side with the wires is screwed to the weight, enabling the wires to go in the gap under the weight.
   * The load cell's arrow indicating its direction is pointing down.

![image](https://github.com/user-attachments/assets/321154e2-6062-4a48-aa21-518dfa5117a5) <br>

![image](https://github.com/user-attachments/assets/e881e2ac-d0b9-48a4-a9e2-338105f54037)

## 2. Control box
When weighing several birds in one setup, it is highly recommended to use a central control system, so that the microcontroller and minicomputer are located in a central, organized location, and the scales are connected through a contro box located next to them. This control box contains the breakout boards (MUX, NAU7802) with customized connectors to easily modify the connections with the scales scattered around the room inside the birdcages. 

**Part list:**
1. Plastic box
2. SparkFun Qwiic MUX breakout
3. SparkFun QwiicScale NAU7802 (multiple)
4. JST-SM Pigtail connector (4-PIN) (multiple)
5. Flexible Qwiic cables (multiple)
6. Flexible Qwiic breadboard cable

It should look like this: <br>

<img src = "https://github.com/user-attachments/assets/196ff288-d76b-417b-a72e-e28f238e9f77" width = "500" height = "1100"> <br>

## 3. Communication cables
In order to easily manage connecting the scales to the control system, it is best to make custom communication cables with the neccesary length to connect between the location of the bird cage and the control box using simple 4-core network/telephone cables. These cables connect to the scale on one side (directly, or using the same connector used for the load cell), and to the NAU7802 breakout board on the other side. These cables allow easy setup and removal of the scale in and out of the birdcage, inside the acoustic box.

![IMG_20240811_171613](https://github.com/user-attachments/assets/f68ef31e-59ea-4ea2-9fc1-382087803f95)

ADD SCHEMATIC DIAGRAM - with JSM Pigtail connector, cable, and Picoblade connector.


##s 4. Overview
