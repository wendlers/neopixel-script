/* DO NOT EDIT BY HAND - autogenerated */

#include "nps.h"
#include "ledfx.h"

LedFX fx = LedFX();


void nps_main(void)
{
  fx.setBrightness(150);
  fx.setPixel((uint16_t)0, CRGB::Red);
  fx.show(250);
  fx.setPixel((uint16_t)1, CRGB::Red);
  fx.setPixel((uint16_t)0, CRGB::Black);
  fx.show(250);
  fx.setPixel((uint16_t)2, CRGB::Red);
  fx.setPixel((uint16_t)1, CRGB::Black);
  fx.show(250);
  fx.setPixel((uint16_t)3, CRGB::Red);
  fx.setPixel((uint16_t)2, CRGB::Black);
  fx.show(250);
  fx.setPixel((uint16_t)4, CRGB::Red);
  fx.setPixel((uint16_t)3, CRGB::Black);
  fx.show(250);
  fx.setPixel((uint16_t)5, CRGB::Red);
  fx.setPixel((uint16_t)4, CRGB::Black);
  fx.show(250);
  fx.setPixel((uint16_t)5, CRGB::Black);

  fx.show();
}