#include <Arduino.h>
#include "nps.h"

void setup()
{
  Serial.begin(9600);

  Serial.println("*** NeoPixelScipt Runtime ***");
  Serial.print("- version is ");
  Serial.println(NP_VERSION);
  Serial.print("- data pin is ");
  Serial.println(NP_DATA_PIN);
  Serial.print("- driving ");
  Serial.print(NP_COLS * NP_ROWS);
  Serial.println(" LEDs");
  Serial.print("- ");
  Serial.print(NP_ROWS);
  Serial.println(" row(s)");
  Serial.print("- ");
  Serial.print(NP_COLS);
  Serial.println(" col(s)");

#ifdef NP_ORDER_SWAP
  Serial.println("- swapping LED order");
#endif
  Serial.print("- using font ");
#ifdef NP_FONT_IBM
  Serial.println("IBM");
#else
  Serial.println("HL2");
#endif
}

void loop()
{
  nps_main();
}
