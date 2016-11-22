NeoPixel Script - A DSL to drive NeoPixels
==========================================

This project tries to implement a simple DSL (domain specific language)
which easily allows to program effects for a NeoPixel based 8x8 matrix.
One of the main goals of this language is to be simple, easy to learn
and understand especially by children. Thus, the language is offered in
different languages (currently German and English).

A simple script which will produce a colorful effect on the whole 8x8
matrix would look like this:

In German

    wiederhole 8 mal
      // "schiebt" 2 grüne Pixel von der linken Seite ein
      schiebe 2 links in gruen
      warte 100 msek
      schiebe 2 links in rot
      warte 100 msek
      schiebe 2 links in lila
      warte 100 msek
      schiebe 2 links in weiss
      warte 100 msek
    ende

And in English

    repeat 8 times
      // "shifts" in 2 green pixels from the left side
      shift 2 left in green
      sleep 100 msec
      shift 2 left in red
      sleep 100 msec
      shift 2 left in magenta
      sleep 100 msec
      shift 2 left in white
      sleep 100 msec
    end

For more examples see the "examples" directory.

How it works
------------

LED effects are written in NPS (NeoPixel Sript). Then the NPS is "compiled"
into C++ code (by a Python tool). The C++ code is linked with some Arduino
libraries (especially FastLED) into a native executable for the Arduino,
and then is uploaded.

By using PlatformIO IDE, the steps described above are as easy as editing
"effects_de.nps" if using the German implementation of NPS or "effects_en.nps"
if using the English implementation. Then the only thing left to do is hit
the "Upload" button on the left tool-bar of the IDE, and after a few seconds,
the Arduino will run your script.

Usage
-----

You need PlatformIO IDE (CLI will also do but is more complex to install) to
use the code from this project.

To install PlatformIO IDE, follow the [steps described on their web-side](
  http://docs.platformio.org/en/stable/installation.html).

Then open the IDE by starting "Atom" select "Open Project" and point it to
the "neopixel-script" directory.

Check the file "npscript.ini". You need to specify the language of NPS, and
the name of your script file (default language is "en", and default script is
"effects_en.nps"). Also "npscript.ini" it the place where you would point the
compiler to one of the examples.

The data input of the NeoPixel matrix needs to be connected to PIN3. The
default MCU is "pro16MHzatmega328". If you use a different PIN or a
different MCU, have a look at "platformio.ini" where you could change this
parameters too.
