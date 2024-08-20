/***************************************************************************
* THIS IS THE MAIN ARDUINO CODE FOR ACOUSTIC CHAMBERS LIGHT CYCLE CONTROL, AS WELL AS SENSOR(DHT+LIGHT) & WEIGHT DATA ACQUISITION

* It has two functionalities -
*   1. Turn the lights on/off, based on an input from the serial port.
*       Data from the serial port arrives as an int, and so we set a
*       threshold to decide whether the light goes on or off.
*
*   2. Read data from temp. and humidity sensors, as well as light and weight
*     sensors, and print values to the serial port (via Serial.print()).
*     This data will later be read by our Raspberry Pi device, whenever
*     we're ready to consume the data.

NOTE: PLEASE MAKE SURE THAT THE FOLLOWING LIBRARY IS INSTALLED IN ARDUINO IDE:
SparkFun I2C Mux Arduino Library

***************************************************************************/

#include <dht.h>
#include <Wire.h>
#include <EEPROM.h> //Needed to record user settings
#include <SparkFun_I2C_Mux_Arduino_Library.h>
#include <SparkFun_Qwiic_Scale_NAU7802_Arduino_Library.h>

#define DHT22_PIN 8
QWIICMUX myMux;
NAU7802 myScale;
dht DHT;

//EEPROM locations to store 20-byte variables
#define LOCATION_CALIBRATION_FACTOR(port) (port * 20) // Float, requires 4 bytes, plus extra space.
#define LOCATION_ZERO_OFFSET(port) (LOCATION_CALIBRATION_FACTOR(port) + 8) // //Must be more than 4 away from previous spot. Long, requires 4 bytes of EEPROM
bool settingsDetected = false; //Used to prompt user to calibrate their scale

const int numScales = 8; // Number of Qwiic Scale ports available

int LIGHT_SWITCH_PIN = 13;
int BYTES_THRESHOLD = 100;
int incomingByte = 0; // Variable that will contain user input

int ldrPin = A0;
unsigned long seconds = 1000L;
unsigned long minutes = seconds * 1;
unsigned long DelayRate = minutes;

void setup() {
  pinMode(LIGHT_SWITCH_PIN, OUTPUT);
  pinMode(ldrPin, INPUT);
  Wire.begin();

  Serial.begin(9600);

  // myScale setup and scale parameters acquisition
  if (!myMux.begin()) {
  Serial.println("Mux not detected. Make sure scale system is connected properly and try again. Swich to arduino_code_0 to monitor DHT data alone, or to arduino_code_2 to test and calibrate scale.");
  delay(DelayRate);
  }
  else {
  Serial.println("Mux detected");
  
  for (int i = 0; i < numScales; ++i) {
    myMux.enablePort(i);
    myScale.begin();

    if (myScale.begin()) {

      myScale.setSampleRate(NAU7802_SPS_320); //Increase to max sample rate
      myScale.calibrateAFE(); //Re-cal analog front end when we change gain, sample rate, or channel 
    }
    myMux.disablePort(i);
  } 
  } 
}

void loop() {

  //This part is for DHT data acquisition and printing out of all the data
  int LDRinput = analogRead(ldrPin);
  int chk = DHT.read22(DHT22_PIN);

  switch (chk) {
    case DHTLIB_OK:
      break;
    case DHTLIB_ERROR_CHECKSUM:
      Serial.print(0);
      break;
    case DHTLIB_ERROR_TIMEOUT:
      Serial.print(0);
      break;
    default:
      Serial.print(0);
      break;
  }
  
  Serial.print(DHT.humidity);
  Serial.print(";");
  Serial.print(DHT.temperature);
  Serial.print(";");
  Serial.print(LDRinput);
  Serial.print(";");

  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte > BYTES_THRESHOLD) {
      digitalWrite(LIGHT_SWITCH_PIN, HIGH);
    } else {
      digitalWrite(LIGHT_SWITCH_PIN, LOW);
    }
  }
  // This part is for acquisition of data from all connected scales
  for (int i = 0; i < numScales; ++i) {
    myMux.setPort(i); // Activate communication with active scale #[i], disable all other ports
 
    if (myScale.available() == true) {
      readSystemSettings(i);
      float currentScaleReading = myScale.getWeight();
      if (!isnan(currentScaleReading)) {
        Serial.print(currentScaleReading, 2);
        Serial.print(";");   
      } else {
        Serial.print(0);
        Serial.print(";");
      } 
    } 
    else {
      Serial.print(0);
      Serial.print(";");
    }
  }
  Serial.println("");
  myMux.setPort(-1); // disable all ports

  delay(DelayRate); //wait 1 second until next data reading

}

//Scale functions for communicating with EEPROM(non-vlatile memory of arduino)

//Reads the current system settings from EEPROM
//If anything looks weird, reset setting to default value
void readSystemSettings(int scalePort) //REQUIRED to read an already-calibrated system settings (zero offset and calibration factor)
{
  float settingCalibrationFactor; //Value used to convert the load cell reading to lbs or kg
  long settingZeroOffset; //Zero value that is found when scale is tared

  //Look up the calibration factor
  EEPROM.get(LOCATION_CALIBRATION_FACTOR(scalePort), settingCalibrationFactor);
  if (settingCalibrationFactor == 0xFFFFFFFF)
  {
    settingCalibrationFactor = 0; //Default to 0
    EEPROM.put(LOCATION_CALIBRATION_FACTOR(scalePort), settingCalibrationFactor);
  }

  //Look up the zero tare point
  EEPROM.get(LOCATION_ZERO_OFFSET(scalePort), settingZeroOffset);
  if (settingZeroOffset == 0xFFFFFFFF)
  {
    settingZeroOffset = 1000L; //Default to 1000 so we don't get inf
    EEPROM.put(LOCATION_ZERO_OFFSET(scalePort), settingZeroOffset);
  }

  //Pass these values to the library
  myScale.setCalibrationFactor(settingCalibrationFactor);
  myScale.setZeroOffset(settingZeroOffset);

  settingsDetected = true; //Assume for the moment that there are good cal values
  if (settingCalibrationFactor < 0.1 || settingZeroOffset == 1000)
    settingsDetected = false; //Defaults detected. Prompt user to cal scale.
}