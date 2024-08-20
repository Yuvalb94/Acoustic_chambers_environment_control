/***************************************************************************
* THIS IS THE MAIN ARDUINO CODE FOR CONTROLLING THE ACOUSTIC CHAMBERS LIGHT CYCLE

* Its main and only function is to turn the lights on/off, based on an input from the serial port.
* Data from the control script on the Raspberry Pi cones through the serial port as an int value of either 97 (sent as 'a' byte) or 102 (sent as 'f' byte).
* A threshold of 100 is set so that a value higher than 100 will turn the light on, and a value of 97 will turn the light off.
* The Arduino then sends a command to all relay switches through digital pin 13 to turn the lights on/off.


NOTE: remember to edit the config file according to the instructions in order to achieve the desired sunrise and sunset times!
***************************************************************************/

int LIGHT_SWITCH_PIN = 13;
int BYTES_THRESHOLD = 100;
int incomingByte = 0;

unsigned long seconds = 1000L;
unsigned long minutes = seconds * 1;
unsigned long DelayRate = minutes;

void setup() {
  pinMode(LIGHT_SWITCH_PIN, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  Serial.print("Hello"); //Script must print anything to initiate the proccess in the 'control_main.py' script

  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte > BYTES_THRESHOLD) {
      digitalWrite(LIGHT_SWITCH_PIN, HIGH);
    } else {
      digitalWrite(LIGHT_SWITCH_PIN, LOW);
    }
  }

  delay(DelayRate);
}
