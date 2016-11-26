#include "ledfx.h"

#ifdef NP_FONT_HL2
  #include "font_hl2.h"
#else
  #include "font_ibm.h"
#endif

LedFX::LedFX()
{
  FastLED.addLeds<NEOPIXEL, NP_DATA_PIN>(leds, num_leds);
  FastLED.setBrightness(10);
}

void LedFX::setPixel(CRGB::HTMLColorCode color)
{
  for(uint16_t i = 0; i < num_leds; i++) {
    leds[i] = color;
  }
}

void LedFX::setPixel(uint16_t ledId, CRGB::HTMLColorCode color)
{
  if(ledId < num_leds) {
    leds[ledId] = color;
  }
}

void LedFX::setPixel(uint8_t row, uint8_t col, CRGB::HTMLColorCode color)
{
  if(row < rows && col < cols) {
    if(row % 2) {
      leds[rows * row + col] = color;
    }
    else {
      leds[rows * row + (cols - col - 1)] = color;
    }
  }
}

void LedFX::setPixel(unsigned char matrix[num_leds], CRGB::HTMLColorCode *colors)
{
  for(uint8_t row = 0; row < rows; row++) {
    for(uint8_t col = 0; col < cols; col++) {
      setPixel(row, col, colors[matrix[row * rows + col]]);
    }
  }
}

void LedFX::setPixel(unsigned char matrix[num_leds], CRGB::HTMLColorCode fgColor,
  CRGB::HTMLColorCode bgColor)
{
  CRGB::HTMLColorCode colors[] = {bgColor, fgColor};

  setPixel(matrix, colors);
}

void LedFX::setBrightness(uint8_t brightness)
{
  FastLED.setBrightness(brightness);
}

void LedFX::putChar(char c, CRGB::HTMLColorCode fgColor,
  CRGB::HTMLColorCode bgColor)
{
  unsigned char matrix[num_leds];

  if(fontCharToMatrix(c, matrix, true)) {
    setPixel(matrix, fgColor, bgColor);
  }
}

void LedFX::putString(const char *s, CRGB::HTMLColorCode fgColor,
  CRGB::HTMLColorCode bgColor, unsigned long pause)
{
  char *p = (char *)s;

  unsigned char matrix1[num_leds];
  unsigned char matrix2[num_leds];

  memset(matrix1, 0, num_leds);
  memset(matrix2, 0, num_leds);

  while(*p) {

#ifdef NP_FONT_HL2
    bool center = (*p < 32);

    uint8_t w = fontCharToMatrix(*p++, matrix2, center);
    uint8_t start = cols - w - 1;

    if(center || start < 0) {
      start = 0;
    }
#else
    fontCharToMatrix(*p++, matrix2);
    uint8_t start = 0;
#endif

    for(uint8_t i = start; i < cols; i++) {
      for(uint8_t col = 0; col < cols; col++) {
        for(uint8_t row = 0; row < rows; row++) {
          if(row == rows - 1) {
            matrix1[col * cols + row] = matrix2[col * cols + i];
          }
          else {
            matrix1[col * cols + row] = matrix1[col * cols + row + 1];
          }
        }
      }

      setPixel(matrix1, fgColor, bgColor);
      show(pause);
    }
  }
}

void LedFX::animate(const char *s, CRGB::HTMLColorCode fgColor,
  CRGB::HTMLColorCode bgColor, int loops, unsigned long pause)
{
  for(int i = 0; i < loops; i++) {
    const char *p = s;

    while(*p) {
      putChar(*p++, fgColor, bgColor);
      show(pause);
    }
  }
}

void LedFX::animate(unsigned char matrixList[][num_leds], uint8_t size,
  CRGB::HTMLColorCode fgColor, CRGB::HTMLColorCode bgColor,
  int loops, unsigned long pause)
{
  for(int i = 0; i < loops; i++) {
    for(uint8_t j = 0; j < size; j++) {
      setPixel(matrixList[j], fgColor, bgColor);
      show(pause);
    }
  }
}

void LedFX::animate(unsigned char matrixList[][num_leds], uint8_t size,
  CRGB::HTMLColorCode *colors, int loops, unsigned long pause)
{
  for(int i = 0; i < loops; i++) {
    for(uint8_t j = 0; j < size; j++) {
      setPixel(matrixList[j], colors);
      show(pause);
    }
  }
}

void LedFX::blend(uint8_t from, uint8_t to)
{
  if(from < to) {
    for(uint8_t i = from; i < to; i++) {
      setBrightness(i);
      show(20);
    }
  }
  else {
    for(uint8_t i = from; i > to; i--) {
      setBrightness(i);
      show(20);
    }
  }
}

void LedFX::shiftLeft(uint16_t amount, CRGB::HTMLColorCode color)
{
  if(amount < num_leds) {
    for(uint16_t i = 0; i < num_leds - amount; i++) {
      leds[i] = leds[i+amount];
    }
    for(uint16_t i = num_leds - amount; i < num_leds; i++) {
      leds[i] = color;
    }
  }
}

void LedFX::shiftRight(uint16_t amount, CRGB::HTMLColorCode color)
{
  if(amount < num_leds) {
    for(uint16_t i = num_leds - 1; i >= amount; i--) {
      leds[i] = leds[i-amount];
    }
    for(uint16_t i = 0; i < amount; i++) {
      leds[i] = color;
    }
  }
}

void LedFX::show(unsigned long pause)
{
  FastLED.show();

  if(pause) {
    delay(pause);
  }
}

uint8_t LedFX::fontCharToMatrix(char c, unsigned char matrix[num_leds],
  bool center)
{
  memset(matrix, 0, num_leds);

#ifdef NP_FONT_HL2
  uint8_t width = font[(unsigned char)c][0];
  uint8_t col = 1;
  uint8_t row = center ? (rows - width) / 2 : rows - width;

  if(c < 0 || c > 127) {
      return 0;
  }

  for(uint16_t i = 0; i < num_leds; i += 8) {
    if(i < width * 8) {
      for(uint16_t j = 0; j < 8; j++) {
        matrix[rows * j + row] = (font[(unsigned char)c][col] >> j) & 1;
      }
      col++;
      row++;
    }
  }
  return width;
#else
  if(c > 0x20 && c < 0x80) {
    for(uint16_t row = 0; row < rows; row++) {
        for(uint16_t col = 0; col < cols; col++) {
            matrix[row * 8 + col] = (font[(unsigned char)c - 0x21][row] >> col) & 1;
        }
    }
    return 8;
  }
  return 0;
#endif
}
