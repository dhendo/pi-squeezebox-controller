from RotaryEncoder import RotaryEncoder


class VolumeIOManager(object):
    def __init__(self, volume, playing, channel_a, channel_b, channel_sw):
        self.volume = volume
        self.playing = playing
        self.encoder = RotaryEncoder(channel_a = channel_a, channel_b = channel_b, channel_sw = channel_sw)
        self.encoder.add_step_callback(self.onStep)
        self.encoder.add_click_callback(self.onClick)
        self.encoder.run()


    def onStep(self, delta):
        vol = self.volume.value
        vol = vol + delta
        if vol > 100:
            vol = 100
        if vol < 0:
            vol = 0
        self.volume.value = vol

    def onClick(self):
        if self.playing.value == 1:
            self.playing.value = 0
        else:
            self.playing.value = 1


def volume_process(volume, playing, channel_a, channel_b, channel_sw):
    try:
        VolumeIOManager(volume, playing, channel_a, channel_b, channel_sw)
    except (KeyboardInterrupt, SystemExit):
        print "Exiting Hardware IO Process"