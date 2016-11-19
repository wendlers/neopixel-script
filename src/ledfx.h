#ifndef LEDFX_H_
#define LEDFX_H_

#include "FastLED.h"

class LedFX {
public:

  static const uint8_t rows = 8;
  static const uint8_t cols = 8;
  static const uint16_t num_leds = rows * cols;

public:

  LedFX();

  void setPixel(CRGB::HTMLColorCode color);

  void setPixel(uint16_t ledId, CRGB::HTMLColorCode color);

  void setPixel(uint8_t row, uint8_t col, CRGB::HTMLColorCode color);

  void setPixel(unsigned char matrix[num_leds], CRGB::HTMLColorCode *colors);

  void setPixel(unsigned char matrix[num_leds], CRGB::HTMLColorCode fgColor,
    CRGB::HTMLColorCode bgColor = CRGB::Black);

  void setBrightness(uint8_t brightness);

  void putChar(char c, CRGB::HTMLColorCode fgColor,
    CRGB::HTMLColorCode bgColor = CRGB::Black);

  void putString(const char *s, CRGB::HTMLColorCode fgColor,
    CRGB::HTMLColorCode bgColor = CRGB::Black, unsigned long pause = 100);

  void animate(const char *s, CRGB::HTMLColorCode fgColor,
    CRGB::HTMLColorCode bgColor = CRGB::Black,
    int loops = 1, unsigned long pause = 250);

  void animate(unsigned char matrixList[][num_leds], uint8_t size,
    CRGB::HTMLColorCode fgColor,
    CRGB::HTMLColorCode bgColor = CRGB::Black,
    int loops = 1, unsigned long pause = 250);

    void animate(unsigned char matrixList[][num_leds], uint8_t size,
      CRGB::HTMLColorCode *colors,
      int loops = 1, unsigned long pause = 250);

  void blend(uint8_t from = 0, uint8_t to = 100);

  void shiftLeft(uint16_t amount, CRGB::HTMLColorCode color);

  void shiftRight(uint16_t amount, CRGB::HTMLColorCode color);

  void show(unsigned long pause = 0);

private:

  uint8_t fontCharToMatrix(char c, unsigned char matrix[num_leds],
    bool center = false);

private:

  CRGB leds[num_leds];
};

#endif