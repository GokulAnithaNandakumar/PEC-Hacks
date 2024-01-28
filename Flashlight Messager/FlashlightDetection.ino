#include <Arduino_APDS9960.h>

static int blinkCount = 0;
static int cnt = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!APDS.begin()) {
    Serial.println("Error initializing APDS-9960 sensor.");
  }
}

void loop() {

  int food=0, help=0, medicine=0, emergency=0;
  
  for (int i=0; i<3; i++) {
      unsigned long startTime = millis();
      unsigned long duration = 0;

      blinkCount = 0;
      cnt=0;

      while (duration < 10000) {  // Measure for 5 seconds (adjust as needed)
        // check if color reading is available
        while (!APDS.colorAvailable()) {
          delay(5);
        }
        int r, g, b;

        // read the color
        APDS.readColor(r, g, b);

        // Check for changes in light intensity
        if (r > 100 || g > 100 || b > 100) {
          // Serial.println("Flashlight detected");
          blinkCount++;
          cnt++;
          // delay(100);
        }
        else {
          // Serial.println("no");
          cnt++;
        }

        // wait a bit before reading again
        // delay(500);
        
        // Update duration
        duration = millis() - startTime;
      }
      if (blinkCount>=430 && blinkCount<=480)
        food += 1;
      else if (blinkCount>=400 && blinkCount<=425)
        help += 1;
      else if (blinkCount>=426 && blinkCount<=460)
        medicine += 1;
      else if (blinkCount>=300 && blinkCount<=340)
        emergency += 1;
  }
  
  if (food>=2)
    Serial.println("FOOD");
  else if (help>=2)
    Serial.println("HELP");
  else if (medicine>=2)
    Serial.println("MEDICINE");
  else if (emergency>=2)
    Serial.println("EMERGENCY");
  else
    Serial.println("Not sure...");
  delay(3000);
}