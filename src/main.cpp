#include <Arduino.h>
#include "nps.h"

void setup()
{
  Serial.begin(9600);
  Serial.println("*** NeoPixelScipt Runtime ***");
}

void loop()
{
  nps_main();
}
