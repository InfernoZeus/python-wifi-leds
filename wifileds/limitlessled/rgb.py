import logging
import sys

class Command(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Colors(object):
    violet = Command("Violet", 0x00)
    royal_blue = Command("Royal Blue", 0x10)
    baby_blue = Command("Baby Blue", 0x20)
    aqua = Command("Aqua", 0x30)
    mint = Command("Mint", 0x40)
    seafoam_green = Command("Seafoam Green", 0x50)
    green = Command("Green", 0x60)
    lime_green = Command("Lime Green", 0x70)
    yellow = Command("Yellow", 0x80)
    yellow_orange = Command("Yellow Orange", 0x90)
    orange = Command("Orange", 0xA0)
    red = Command("Red", 0xB0)
    pink = Command("Pink", 0xC0)
    fusia = Command("Fusia", 0xD0)
    lilac = Command("Lilac", 0xE0)
    lavendar = Command("Lavendar", 0xF0)

class PartyModes(object):
    white = Command("static white color", 1)
    white_fade = Command("white color (gradual changes)", 2)
    all_colors = Command("all colors (gradual changes)", 3)
    rgb_fade = Command("red/green/blue (gradual changes)", 4)
    seven_color_jump = Command("7 colors (jump changes)", 5)
    three_color_jump = Command("3 colors (jump changes)", 6)
    rg_jump = Command("red/green (jump changes)", 7)
    rb_jump = Command("red/blue (jump changes)", 8)
    bg_jump = Command("blue/green (jump changes)", 9)
    white_blink = Command("white color (frequently blinks)", 10)
    white_glitter = Command("white color (glitters)", 11)
    red_blink = Command("red color (frequently blinks)", 12)
    red_glitter = Command("red color (glitters)", 13)
    green_blink = Command("green color (frequently blinks)", 14)
    green_glitter = Command("green color (glitters)", 15)
    blue_blink = Command("blue color (frequently blinks)", 16)
    blue_glitter = Command("blue color (glitters)", 17)
    yellow_blink = Command("yellow color (frequently blinks)", 18)
    yellow_glitter = Command("yellow color (glitters)", 19)
    circulation = Command("circulation mode", 20)

    def __init__(self):
        PartyModes.register_names()

    @classmethod
    def register_names(cls):
        if not hasattr(cls, 'names'):
            cls.names = {}
            for attr in vars(cls):
                attr_obj = getattr(cls, attr)
                if isinstance(attr_obj, Command):
                    cls.names[attr_obj.value] = attr_obj.name


class RGB:
    def effect(self, effect_name, args=[], effect_options={}):
        effect = sys.modules['wifileds.limitlessled.effects.%s' % effect_name]
        try:
            effect.run(self, *args, **effect_options)
        except AttributeError as e:
            logging.error('Effect "%s" failed due to missing lighting attribute: %s' % (effect_name, e))
            pass

    def __init__(self, parent):
        self.parent = parent
        self.long_pause = parent.long_pause
        self.short_pause = parent.short_pause
        self.logger = logging.getLogger(self.__class__.__name__)

        self.colors = Colors()
        self.party_modes = PartyModes()

    def all_on(self):
        self.parent.send_command(0x22)

    def all_off(self):
        self.parent.send_command(0x21)

    def brightness_up(self):
        self.parent.send_command(0x23)

    def brightness_down(self):
        self.parent.send_command(0x24)

    def mode_up(self):
        self.parent.send_command(0x27)
        self.logger.info("Set light to mode up")

    def mode_down(self):
        self.parent.send_command(0x28)

    def speed_up(self):
        self.parent.send_command(0x25)

    def speed_down(self):
        self.parent.send_command(0x26)

    def set_color(self, color):
        self.parent.send_command(0x20, color.value)
        self.logger.info("Set light to color " + color.name)

    def set_color_wheel(self, percentage):
        if percentage < 0 or percentage > 1:
            raise ValueError('Wheel percentage should be > 0 and < 1.')
        self.parent.send_command(0x20, chr(int(float(255) * percentage)))

    def max_brightness(self):
        for i in range(0, 9):
            self.brightness_up()

    def min_brightness(self):
        for i in range(0, 9):
            self.brightness_down()

    def max_speed(self):
        for i in range(0, 9):
            self.speed_up()

    def min_speed(self):
        for i in range(0, 9):
            self.speed_down()

    def white(self):
        for i in range(0, 20):
            self.mode_down()
        self.logger.info("Set light mode to " + PartyModes.names[1] + " (" + str(1) + ")")

    def set_mode(self, party_mode):
        self.white()
        for i in range(1, party_mode.value):
            self.mode_up()
            self.logger.info("Set light mode to " + PartyModes.names[i+1] + " (" + str(i+1) + ")")
