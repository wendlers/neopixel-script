'''
TODO
'''

import sys
import argparse

from genpars import *

LANG = "en"

_T = {
    "de": {
        # keyword translations
        "pixel":        "pixel",
        "brightness":   "helligkeit",
        "sleep":        "warte",
        "write":        "schreibe",
        "play":         "spiele",
        "array":        "feld",
        "symbol":       "symbol",
        "blend":        "blenden",
        "repeat":       "wiederhole",
        "times":        "mal",
        "end":          "ende",
        "scene":        "szene",
        "all":          "alle",
        "sec":          "sek",
        "msec":         "msek",
        "animate":      "animiere",
        "shift":        "schiebe",
        "left":         "links",
        "right":        "rechts",
        "in":           "in",
        "with":         "mit",

        # color translations
        "black":            "schwarz",
        "blue":             "blau",
        "brown":            "braun",
        "cyan":             "zyan",
        "darkblue":         "dunkelblau",
        "darkcyan":         "dunkelzyan",
        "darkgrey":         "dunkelgrau",
        "darkgreen":        "dunkelgruen",
        "darkmagenta":      "dunkelmagenta",
        "darkorange":       "dunkelorange",
        "darkred":          "dunkelrot",
        "darkturquoise":    "dunkeltuerkis",
        "darkviolet":       "dunkelviolet",
        "deeppink":         "dunkelpink",
        "gold":             "gold",
        "grey":             "grau",
        "green":            "gruen",
        "lightblue":        "hellblau",
        "lightcyan":        "hellzyan",
        "lightgreen":       "hellgruen",
        "lightgrey":        "hellgrau",
        "lightpink":        "hellpink",
        "lightyellow":      "hellgelb",
        "magenta":          "magenta",
        "orange":           "orange",
        "pink":             "pink",
        "purple":           "lila",
        "red":              "rot",
        "silver":           "silber",
        "turquoise":        "tuerkis",
        "violet":           "violet",
        "white":            "weiss",
        "yellow":           "gelb",
    }
}


def _t(s):

    global _T
    global LANG

    if LANG in _T and s in _T[LANG]:
        return _T[LANG][s]

    return s


class NpScript:
    """
    TODO
    """

    TYPE = "TYPE"
    HEX = "HEX"
    DEC = "DEC"
    REF = "REF"
    KEY = "KEY"
    STR = "STR"
    ASSIGN = "ASSIGN"
    DELIM = "DELIM"
    RANGE = "RANGE"
    COMMA = "COMMA"

    def __init__(self):

        self.color_map = {
            _t("black"): "CRGB::Black",
            _t("blue"): "CRGB::Blue",
            _t("brown"): "CRGB::Brown",
            _t("cyan"): "CRGB::Cyan",
            _t("darkblue"): "CRGB::DarkBlue",
            _t("darkcyan"): "CRGB::DarkCyan",
            _t("darkgray"): "CRGB::DarkGray",
            _t("darkgrey"): "CRGB::DarkGrey",
            _t("darkgreen"): "CRGB::DarkGreen",
            _t("darkmagenta"): "CRGB::DarkMagenta",
            _t("darkorange"): "CRGB::DarkOrange",
            _t("darkred"): "CRGB::DarkRed",
            _t("darkturquoise"): "CRGB::DarkTurquoise",
            _t("darkviolet"): "CRGB::DarkViolet",
            _t("deeppink"): "CRGB::DeepPink",
            _t("gold"): "CRGB::Gold",
            _t("gray"): "CRGB::Gray",
            _t("grey"): "CRGB::Grey",
            _t("green"): "CRGB::Green",
            _t("lightblue"): "CRGB::LightBlue",
            _t("lightcyan"): "CRGB::LightCyan",
            _t("lightgreen"): "CRGB::LightGreen",
            _t("lightgray"): "CRGB::LightGrey",
            _t("lightgrey"): "CRGB::LightGrey",
            _t("lightpink"): "CRGB::LightPink",
            _t("lightyellow"): "CRGB::LightYellow",
            _t("magenta"): "CRGB::Magenta",
            _t("orange"): "CRGB::Orange",
            _t("pink"): "CRGB::Pink",
            _t("purple"): "CRGB::Purple",
            _t("red"): "CRGB::Red",
            _t("silver"): "CRGB::Silver",
            _t("turquoise"): "CRGB::Turquoise",
            _t("violet"): "CRGB::Violet",
            _t("white"): "CRGB::White",
            _t("yellow"): "CRGB::Yellow",
        }

        self.result = {"main": ""}
        self.scene = "main"
        self.indent = 0
        self.main_indent = 0
        self.repeat_index = 0
        self.field_index = 0

        tokenizer = Tokenizer()

        tokenizer.append((r"0x[-10-9A-Fa-f]+", lambda scanner, token: Tok(self.HEX, int(token, 16))))
        tokenizer.append((r"[-10-9]+", lambda scanner, token: Tok(self.DEC, int(token))))
        tokenizer.append((r"\$[A-Za-z][A-Za-z0-9_]*", lambda scanner, token: Tok(self.REF, str(token[1:]))))
        tokenizer.append((r"[A-Za-z][A-Za-z0-9_]*", lambda scanner, token: Tok(self.KEY, str(token))))
        tokenizer.append((r'".*?"', lambda scanner, token: Tok(self.STR, token)))
        tokenizer.append((r':', lambda scanner, token: Tok(self.DELIM, token)))
        tokenizer.append((r'\.\.', lambda scanner, token: Tok(self.RANGE, token)))
        tokenizer.append((r'=', lambda scanner, token: Tok(self.ASSIGN, token)))
        tokenizer.append((r',', lambda scanner, token: Tok(self.COMMA, token)))
        tokenizer.append((r'//.*?$', lambda scanner, token: None))
        tokenizer.append((r'[ \n\r\t]', lambda scanner, token: None))

        grammar = Grammar()

        number = OR(Tok(self.DEC), Tok(self.HEX))
        string = Tok(self.STR)
        color = OR(AND(Tok(self.KEY, _t('in')),
                       Tok(self.KEY, self.color_map.keys())), Tok(self.KEY, self.color_map.keys()))
        number_or_ref = OR(Tok(self.DEC), Tok(self.HEX), Tok(self.REF))
        ledid = OR(AND(AND(number_or_ref, Tok(self.DELIM), number_or_ref)),
                   AND(AND(number_or_ref, Tok(self.RANGE), number_or_ref)),
                   number_or_ref, Tok(self.KEY, _t('all')))
        ledid_list = MULT(OR(ledid, AND(Tok(self.COMMA), ledid)))

        """
        pixel <n> <color>
        pixel <x>:<y> <color>
        """
        pixel = AND(
            Tok(self.KEY, _t('pixel')),
            AND(
                ledid_list,
                color,
                action=self._pixel)
        )

        """
        brightness <value>
        """
        brightness = AND(
            Tok(self.KEY, _t('brightness')),
            number,
            action=self._brightness
        )

        """
        sleep <value> sec|msec
        """
        wait = AND(
            Tok(self.KEY, _t('sleep')),
            AND(number, OR(Tok(self.KEY, _t('sec')), Tok(self.KEY, _t('msec')))),
            action=self._wait
        )

        """
        write <string> <color>
        """
        write = AND(
            Tok(self.KEY, _t('write')),
            AND(string, color, action=self._write)
        )

        """
        play <scene>
        """
        play = AND(
            Tok(self.KEY, _t('play')),
            Tok(self.KEY),
            action=self._play
        )

        """
        array <values> <color>
        """
        field = AND(
            AND(Tok(self.KEY, _t('array')), MULT(number)),
            color, action=self._field
        )

        """
        symbol <char> <color>
        """
        symbol = AND(
            Tok(self.KEY, _t('symbol')),
            AND(string, color),
            action=self._symbol
        )

        """
        blend <to>
        blend <from>:<to>
        """
        blend = AND(
            Tok(self.KEY, _t('blend')),
            OR(
                AND(AND(number_or_ref, Tok(self.RANGE), number_or_ref)),
                number_or_ref), action=self._blend
        )

        """
        animate <string> <color>
        """
        animate = AND(
            Tok(self.KEY, _t('animate')),
            AND(string, color, action=self._animate)
        )

        """
        shift left|right <amount> <color>
        """
        shift = AND(
            Tok(self.KEY, _t('shift')),
            AND(
                AND(
                    number,
                    OR(
                        Tok(self.KEY, _t('left')), Tok(self.KEY, _t('right'))
                        )
                ),
                color
            ), action=self._shift
        )

        commands = OR(pixel, brightness, write, wait, play, field, symbol,
                      blend, animate, shift)

        """
        repeat <num> times
            <body>
        end
        """
        repeat = AND(
            Tok(self.KEY, _t('repeat')),
            AND(
                AND(
                    AND(number,
                        OR(
                            AND(Tok(self.KEY, _t('times')), AND(Tok(self.KEY, _t('with')), Tok(self.REF))),
                            Tok(self.KEY, _t('times'))
                        ), action=self._repeat_head),
                    MULT(commands)
                ),
                Tok(self.KEY, _t('end')), action=self._repeat_tail
            )
        )

        # repeat is recursive ...
        commands.items.insert(0, repeat)

        """
        scene <name>
            <body>
        end
        """
        scene = AND(
            AND(Tok(self.KEY, _t('scene')), Tok(self.KEY), action=self._scene_head),
            AND(
                MULT(commands),
                Tok(self.KEY, _t('end'))
            ), action=self._scene_tail
        )

        grammar.append(Rule(OR(commands, scene)))

        self.parser = Parser(tokenizer, grammar)

    def _pixel(self, tokens):

        # print("pixel", tokens)

        ledids = [None, None]
        ledrefs = ["", ""]
        idx = 0
        rng = False

        for t in tokens:
            if t.kind in [self.DEC, self.HEX, self.REF]:
                ledids[idx] = t.value
                if t.kind == self.REF:
                    ledrefs[idx] = "nps_"
                else:
                    ledrefs[idx] = ""
                idx = 0
            elif t.kind == self.DELIM:
                idx += 1
            elif t.kind == self.RANGE:
                idx += 1
                rng = True
            elif t.kind == self.KEY and t.value == _t('all'):
                self.result[self.scene] += ' ' * self.indent + 'fx.setPixel(%s);\n' % self.color_map[tokens[-1].value]
            elif t.kind in [self.COMMA, self.KEY] and ledids[0] is not None:
                if not rng:
                    if ledids[1] is not None:
                        self.result[
                            self.scene] += ' ' * self.indent + 'fx.setPixel((uint8_t)%s%s, (uint8_t)%s%s, %s);\n' % (
                                ledrefs[0], ledids[0], ledrefs[1], ledids[1],
                                self.color_map[tokens[-1].value])
                    else:
                        self.result[self.scene] += ' ' * self.indent + 'fx.setPixel((uint16_t)%s%s, %s);\n' % (
                            ledrefs[0], ledids[0],
                            self.color_map[tokens[-1].value])
                else:
                    for i in range(ledids[0], ledids[1] + 1):
                        self.result[self.scene] += ' ' * self.indent + 'fx.setPixel((uint16_t)%s, %s);\n' % (
                            i,
                            self.color_map[
                                tokens[
                                    -1].value])

                ledids = [None, None]

                rng = False

    def _brightness(self, tokens):

        # print("helligkeit", tokens)

        self.result[self.scene] += ' ' * self.indent + 'fx.setBrightness(%d);\n' % tokens[1].value

    def _write(self, tokens):

        # print("write", tokens)

        self.result[self.scene] += ' ' * self.indent + 'fx.putString(%s, %s);\n' % (
        tokens[0].value, self.color_map[tokens[-1].value])

    def _wait(self, tokens):

        # print("wait", tokens)

        mult = 1

        if tokens[2].value == "sek":
            mult = 1000

        self.result[self.scene] += ' ' * self.indent + 'fx.show(%d);\n' % (tokens[1].value * mult)

    def _repeat_head(self, tokens):

        # print("repeat_head", tokens)

        counter_var = "nps_i%d" % self.repeat_index

        if len(tokens) > 2:
            counter_var = "nps_%s" % tokens[3].value

        self.result[self.scene] += '\n' + (' ' * self.indent) + 'for(int %s = 0; %s < %d; %s++) {\n' % \
                                                                (counter_var, counter_var, tokens[0].value,
                                                                 counter_var)
        self.indent += 2
        self.repeat_index += 1

    def _repeat_tail(self, tokens):

        # print("repeat_tail", tokens)

        self.indent -= 2
        self.repeat_index -= 1
        self.result[self.scene] += ' ' * self.indent + '}\n\n'

    def _scene_head(self, tokens):

        # print("scene_head", tokens)

        self.scene = tokens[1].value
        self.result[self.scene] = ""
        self.main_indent = self.indent
        self.indent = 2
        self.result[self.scene] += "void nps_scene_%s(void) {\n" % tokens[1].value

    def _scene_tail(self, tokens):

        # print("scene_tail", tokens)

        self.indent -= 2
        self.result[self.scene] += ' ' * self.indent + '}\n'
        self.scene = "main"
        self.indent = self.main_indent

    def _play(self, tokens):

        # print("play", tokens)

        self.result[self.scene] += ' ' * self.indent + 'nps_scene_%s();\n' % tokens[1].value

    def _field(self, tokens):

        # print("field", tokens)

        self.result[self.scene] += ' ' * self.indent + "unsigned char f%d[LedFX::num_leds] = {" % self.field_index

        for i, t in enumerate(tokens[1:]):

            if t.kind == self.KEY:
                break

            if i % 8 == 0:
                self.result[self.scene] += "\n"
                self.result[self.scene] += ' ' * (self.indent + 2)

            self.result[self.scene] += "%d, " % t.value

        self.result[self.scene] += "};\n"
        self.result[self.scene] += ' ' * self.indent + "fx.setPixel(f%d, %s);\n" % (
            self.field_index, self.color_map[tokens[-1].value])
        self.field_index += 1

    def _symbol(self, tokens):

        # print("symbol", tokens)

        self.result[self.scene] += ' ' * self.indent + "fx.putChar('%s', %s);\n" % (
            tokens[1].value[1:-1], self.color_map[tokens[-1].value])

    def _blend(self, tokens):

        # print("blend", tokens)

        vals = [0, 100]
        refs = ["", ""]
        i = 0

        for t in tokens[1:]:
            if t.kind in [self.REF, self.DEC, self.HEX]:
                if t.kind == self.REF:
                    refs[i] = "i"
                vals[i] = t.value
                i += 1

        self.result[self.scene] += ' ' * self.indent + "fx.blend(%s%d, %s%d);\n" % (
            refs[0], vals[0], refs[1], vals[1])

    def _animate(self, tokens):

        # print("animate", tokens)

        self.result[self.scene] += ' ' * self.indent + "fx.animate(%s, %s);\n" % (
            tokens[0].value, self.color_map[tokens[-1].value])

    def _shift(self, tokens):

        print("shift", tokens)

        if tokens[2].value == _t('left'):
            dir = "Left"
        else:
            dir = "Right"

        self.result[self.scene] += ' ' * self.indent + "fx.shift%s(%d, %s);\n" % (
            dir, tokens[1].value, self.color_map[tokens[-1].value])

    def compile(self, inp):

        self.indent = 2
        self.repeat_index = 0

        s, r = self.parser.parse(inp)

        if not s:
            raise SyntaxError("%s" % r)

        result = "/* DO NOT EDIT BY HAND - autogenerated */\n\n"
        result += "#include \"nps.h\"\n"
        result += "#include \"ledfx.h\"\n\n"
        result += "LedFX fx = LedFX();\n\n"

        for scene in self.result.keys():
            if scene == "main":
                continue
            result += "void nps_scene_%s(void);\n" % scene

        result += "\n"

        for scene, code in self.result.items():
            if scene == "main":
                continue
            result += code + "\n"

        result += "void nps_main(void)\n{\n"
        result += self.result["main"]
        result += "\n  fx.show();\n"
        result += "}"

        return result


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='NPS - NeoPixelScript to C++ Compiler')

    parser.add_argument("-c", "--compile", default=None, metavar="FILE",
                        help="Script file to compile")

    parser.add_argument("-o", "--output", default=None, metavar="FILE",
                        help="Write C++ code to file")

    parser.add_argument("-l", "--lang", default="en", metavar="LANG",
                        help="Language used for NPS (de or en)")

    args = parser.parse_args()

    if args.compile is None:
        sys.stderr.write("Input file missing (need -c)\n")
        exit(1)

    try:
        LANG = args.lang
        npsc = NpScript()

        with open(args.compile, "r") as f:
            src = f.read()

        res = npsc.compile(src)

        if args.output is not None:
            with open(args.output, "wb") as f:
                f.write(res)
        else:
            print(res)
    except IOError as e:
        sys.stderr.write("%s\n" % e)
        exit(1)
    except SyntaxError as e:
        sys.stderr.write("Compile error: %s\n" % e)
        exit(2)
