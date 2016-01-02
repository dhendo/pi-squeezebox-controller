import RPIO
import time



class RotaryEncoder(object):
    lut = [0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0];

    def __init__(self, channel_a=27, channel_b=4, debounce_ms=50, channel_sw=22):
        self.last_val = 0
        self.last = None
        self.debounce = debounce_ms;
        self.click_count = 0

        self.callback = None
        self.click_callback = None

        self.channel_a = channel_a
        self.channel_b = channel_b
        self.channel_sw = channel_sw
        # change to BCM numbering schema
        RPIO.setmode(RPIO.BCM)

        RPIO.setup(channel_a, RPIO.IN)
        RPIO.set_pullupdn(channel_a, RPIO.PUD_UP)

        RPIO.setup(channel_b, RPIO.IN)
        RPIO.set_pullupdn(channel_b, RPIO.PUD_UP)

        RPIO.setup(22, RPIO.IN)
        RPIO.set_pullupdn(channel_sw, RPIO.PUD_UP)

        # GPIO interrupt callbacks
        RPIO.add_interrupt_callback(channel_a, self.__gpio_callback, edge="both")
        RPIO.add_interrupt_callback(channel_b, self.__gpio_callback, edge="both")
        RPIO.add_interrupt_callback(channel_sw, self.__click_callback, edge="both",  pull_up_down=RPIO.PUD_UP, debounce_timeout_ms=300)


    def step(self, delta):
        if self.callback:
            self.callback(delta)

    def add_step_callback(self, callback):
        self.callback = callback

    def add_click_callback(self, callback):
        self.click_callback = callback


    def run(self, threaded=False):
        RPIO.wait_for_interrupts(threaded=threaded)


    def __gpio_callback(self, gpio_id, val):

        a = RPIO.input(self.channel_a)
        b = RPIO.input(self.channel_b)

        current = (a << 1) + b

        val = ((self.last_val << 2) + current) & 0b1111

        delta = RotaryEncoder.lut[val]
        if delta:
            s_time = time.time()
            if not self.last:
                self.last = s_time
                self.step(delta)
            elif (s_time - self.last) * 1000 > self.debounce:
                # print "\nA: %d B: %d\tState: %s\t%s\tDelta: %d\t%5f" % (
                #     a, b, "{0:b}".format(val), val, delta, (s_time - self.last) * 1000)
                self.last = s_time
                self.step(delta)

        self.last_val = current

    def __click_callback(self, gpio_id, val):
        if self.click_callback:
            self.click_callback()

