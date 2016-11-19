import sys
sys.path.append("./generator")

import npscript
import ConfigParser

Import("env")

def nps_gen():
    """
    Generate C++ code from NPS
    """

    script = None
    result = None

    try:

        cp = ConfigParser.ConfigParser()
        cp.read("npscript.ini")

        try:
            lang = cp.get("compiler", "lang")
            npscript.LANG = lang
        except:
            pass

        try:
            script = cp.get("compiler", "input")
        except:
            pass

        try:
            result = cp.get("compiler", "output")
        except:
            pass

    except:
        pass

    if script is None:
        script = "effects_%s.nps" % npscript.LANG

    if result is None:
        result = "src/nps.cpp"

    print("Compiling NeoPixel script: %s" % script)
    npsc = npscript.NpScript()

    with open(script, "r") as f:
        src = f.read()

    res = npsc.compile(src)

    with open(result, "w") as f:
        f.write(res)

nps_gen()
