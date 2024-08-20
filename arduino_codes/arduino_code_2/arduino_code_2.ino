/***************************************************************************
* THIS IS THE MAIN ARDUINO CODE FOR CALIBRATING THE SCALE SYSTEM

* It can be used to calibrate new scales or re-calibrate existing scales.

* In order to use it:
* 1. Stop the main code running on the Raspi
* 2. Upload this version of the arduino code on the arduino UNO.
* 3. If needed, connect / disconnect new scales to the system
* 4. Follow the instructions on the Serial monitor

NOTE: PLEASE MAKE SURE THAT THE FOLLOWING LIBRARY IS INSTALLED IN ARDUINO IDE:
SparkFun I2C Mux Arduino Library

Software explanations and information:

EEPROM main functions:  (for more information visit https://docs.arduino.cc/learn/built-in-libraries/eeprom/)
EEPROM is a sort of internal storage of the arduino (non-volatile memory - NVM).
It has 1024 bytes (in UNO) for storage and can endure up to 100,000 write/erase instances.
For the calibration of the scale we use this storage, in order to store the calibration factor and zero offset of each scale.
here are some modules and their meaning:
LOCATION_CALIBRATION_FACTOR(port) - used to define the location of each port's calibration factor
LOCATION_ZERO_OFFSET(port) - used to define the location of each port's zero offset
   The locations are based on the storage requirements of the data with extra space taken for future alterations, total 20 bytes:
     - Each port takes the first 20 spots after the 20*portNumber
     - First 4 bytes for float (calibration factor)
     - 4 bytes extra space
     - 4 bytes for long (zero offset)
     - 8 bytes extra space
EEPROM.get(adress, variable) - receives the data stored in (adress) to (variabe)
EEPROM.put(adress, data) - sets a new value (data) to the defined adress (adress)

NAU7802 main functions: (for more information visit the SparkFun_Qwiic_Scale_NAU7802_Arduino_Library - src folder )
myScale.calculateCalibrationFactor() - Sets the calibration factor based on the weight on scale and zero offset.
myScale.calculateZeroOffset() - Also called taring. Call this with nothing on the scale
myScale.getCalibrationFactor() - Ask library for this value. Useful for storing value into NVM.
myScale.getZeroOffset() - Ask library for this value. Useful for storing value into NVM.
myScale.setCalibrationFactor() - ass a known calibration factor into library. Helpful if users is loading settings from NVM.
myScale.setZeroOffset() - Sets the internal variable. Useful for users who are loading values from NVM.\
***************************************************************************/


#include <EEPROM.h> //Needed to record user settings
#include <SparkFun_I2C_Mux_Arduino_Library.h>
#include "SparkFun_Qwiic_Scale_NAU7802_Arduino_Library.h"

QWIICMUX myMux;
NAU7802 myScale;


//EEPROM locations to store 20-byte variables
#define LOCATION_CALIBRATION_FACTOR(port) (port * 20) // Float, requires 4 bytes, plus extra space.
#define LOCATION_ZERO_OFFSET(port) (LOCATION_CALIBRATION_FACTOR(port) + 8) // //Must be more than 4 away from previous spot. Long, requires 4 bytes of EEPROM
bool settingsDetected = false; //Used to prompt user to calibrate their scale

const int numScales = 8; // Number of Qwiic Scale ports available

int incomingByte = 0; // Variable that will contain user input

unsigned long seconds = 1000L;
unsigned long minutes = seconds * 1;
unsigned long DelayRate = minutes;

void setup() {

  Wire.begin();

  Serial.begin(9600);

  //myScale setup and scale parameters acquisition / calibration
  if (!myMux.begin()) {
  Serial.println("Mux not detected. Freezing...");
  while (1);
  }
  Serial.println("Mux detected");

  for (int i = 0; i < numScales; ++i) {
    myMux.enablePort(i);
    myScale.begin();
    delay(1);

    if (!myScale.begin()) {
      Serial.println("No scale detected on port " + String(i));
    } 
    else {
      Serial.println("Scale detected on port " + String(i));
      
      myScale.setSampleRate(NAU7802_SPS_320); //Increase to max sample rate
      myScale.calibrateAFE(); //Re-cal analog front end when we change gain, sample rate, or channel 

      readSystemSettings(i); //Load zeroOffset and calibrationFactor from EEPROM
      if(settingsDetected == false) {
        Serial.print("\tScale " + String(i));
        //Serial.print(i);
        Serial.println(" not calibrated. Follow calibration instructions.");
        // Serial.print(" not calibrated. Calibrating scale:");

        // calibrateScale();
      } 
      else {
        Serial.print("Zero offset: ");
        Serial.println(myScale.getZeroOffset());
        Serial.print("Calibration factor: ");
        Serial.println(myScale.getCalibrationFactor());
      }
    }
    myMux.disablePort(i);
  } 
}

void loop() {

  for (int i = 0; i < numScales; ++i) {

    myMux.setPort(i); // Activate communication with active scale #[i], disable all other ports
    Serial.print(" c"); 
    Serial.print(i);
    Serial.print(": "); // indicate channel number before each value
    
    // for every port, check if there is a new scale reading and print it. If no input from the scale print 0.
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


  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte == 't') //Tare the scale
    {
      tareScale();
    }
    else if (incomingByte == 'c') //Calibrate
    {
      calibrateScale();
    }
    else if (incomingByte == 's') // Show system settings of connected scales
    {
      showScaleSettings();
    }
  }
  delay(DelayRate);
}


//Weight sensor Calibration and EEPROM(non-vlatile memory of arduino) stuff

//Gives user the ability to set a known weight on the scale and calculate a calibration factor
void calibrateScale()
{
  int selectedPort = -1; // Initialize selectedPort with an invalid value

  while (selectedPort < 0 || selectedPort >= numScales) {
    Serial.println("Enter scale port number to calibrate (0-7): ");
    while (Serial.available()) Serial.read(); //Clear anything in RX buffer
    while (Serial.available() == 0) delay(10); //Wait for user to press key
    selectedPort = Serial.parseInt();
    
    // Check if the input is within the valid range and corresponds to an active scale
    if (selectedPort < 0 || selectedPort >= numScales) {
      Serial.println("Invalid scale port number. Please enter a number between 0 and 7 for an active scale.");
    }
  }

  // at this point, selectedPort is a valid port number. Proceeding with calibration process
  myMux.setPort(selectedPort);
  Serial.println();
  Serial.println("Starting calibration for scale on port " + String(selectedPort));
  

  Serial.println(F("Setup scale with no weight on it. Press a key when ready."));
  while (Serial.available()) Serial.read(); //Clear anything in RX buffer
  while (Serial.available() == 0) delay(10); //Wait for user to press key

  myScale.calculateZeroOffset(64); //Zero or Tare the scale. Average over 64 readings. This command also sets the new zero offset temporarily in myScale object until arduino is shut down or new value is acquired.
  Serial.print(F("New zero offset: "));
  Serial.println(myScale.getZeroOffset());

  Serial.println(F("Place known weight on scale. Press a key when weight is in place and stable."));
  while (Serial.available()) Serial.read(); //Clear anything in RX buffer
  while (Serial.available() == 0) delay(10); //Wait for user to press key

  Serial.print(F("Please enter the weight, without units, currently sitting on the scale (for example '4.25'): "));
  while (Serial.available()) Serial.read(); //Clear anything in RX buffer
  while (Serial.available() == 0) delay(10); //Wait for user to press key

  //Read user input
  float weightOnScale = Serial.parseFloat();
  Serial.println();

  myScale.calculateCalibrationFactor(weightOnScale, 64); //Tell the library how much weight is currently on it and will also set the new calibration factor temporarily in myScale object.
  Serial.print("Scale " + selectedPort);
  Serial.print(" Calibrated. New cal factor: ");
  Serial.println(myScale.getCalibrationFactor(), 2);

  Serial.print(F("New Scale Reading: "));
  Serial.println(myScale.getWeight(), 2);

  recordSystemSettings(selectedPort); //Commit these values to EEPROM 
  myMux.disablePort(selectedPort);
}

void tareScale() 
{
  int selectedPort = -1; // Initialize selectedPort with an invalid value

  while (selectedPort < 0 || selectedPort >= numScales) {
    Serial.println("Enter scale port number to tare (0-7): ");
    while (Serial.available()) Serial.read(); //Clear anything in RX buffer
    while (Serial.available() == 0) delay(10); //Wait for user to press key
    selectedPort = Serial.parseInt();
    
    // Check if the input is within the valid range and corresponds to an active scale
    if (selectedPort < 0 || selectedPort >= numScales) {
      Serial.println("Invalid scale port number. Please enter a number between 0 and 7 for an active scale.");
    }
  }

  // at this point, selectedPort is a valid port number. Proceeding with calibration process
  myMux.enablePort(selectedPort);
  Serial.println();
  Serial.println("Taring scale on port " + String(selectedPort));
  myScale.calculateZeroOffset();

  recordZeroOffset(selectedPort); //Commit these values to EEPROM 

  myMux.disablePort(selectedPort);
}

//Record the current system settings to EEPROM
void recordSystemSettings(int scalePort)
{
  //Get existing calibration values from libraty (myScale object) and commit them to the arduino's NVM
  EEPROM.put(LOCATION_CALIBRATION_FACTOR(scalePort), myScale.getCalibrationFactor());
  EEPROM.put(LOCATION_ZERO_OFFSET(scalePort), myScale.getZeroOffset());
}

//Record the new zero offset after taring to EEPROM
void recordZeroOffset(int scalePort)
{
  //Get existing calibration values from libraty (myScale object) and commit them to the arduino's NVM
  EEPROM.put(LOCATION_ZERO_OFFSET(scalePort), myScale.getZeroOffset());
}

//show current settings for each scale. 
void showScaleSettings(){
  for (int i = 0; i < numScales; ++i) {
    myMux.enablePort(i);
    myScale.begin();

    if (!myScale.begin()) {
      Serial.println("No scale on port " + String(i));
    } 
    else {
      Serial.print("Scale " + String(i));
      Serial.println(" system settings:");
      readSystemSettings(i); //Load zeroOffset and calibrationFactor from EEPROM

      Serial.print("Zero offset: ");
      Serial.println(myScale.getZeroOffset());
      Serial.print("Calibration factor: ");
      Serial.println(myScale.getCalibrationFactor());
    }
    myMux.disablePort(i);
  }
  delay(10000);
}
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