# 1. Self-built weighing device (scale)
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

# 2. Control box
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

# 3. Communication cables
In order to easily manage connecting the scales to the control system, it is best to make custom communication cables with the neccesary length to connect between the location of the bird cage and the control box using simple 4-core network/telephone cables. These cables connect to the scale on one side (directly, or using the same connector used for the load cell), and to the NAU7802 breakout board on the other side. These cables allow easy setup and removal of the scale in and out of the birdcage, inside the acoustic box.

![IMG_20240811_171613](https://github.com/user-attachments/assets/f68ef31e-59ea-4ea2-9fc1-382087803f95)

ADD SCHEMATIC DIAGRAM - with JSM Pigtail connector, cable, and Picoblade connector.


# 4. Overview
