# pi-squeezebox-controller
Controller to run a squeezebox (Logitech Media Server - http://forums.slimdevices.com/) controller with rotary encoder and I2C OLED display on a raspberry pi.

The rotary encoder controls the volume. The switch toggles play / pause. The display shows volume, play / pause, artist / track, player name.

The controller uses the multiprocessing module to deal with the threading and avoid IO events being missed. 
- The rotary encoder is interrupt driven and sits in its own process
- The display refresh is in another process.
- A telnet connection to the LMS server is used to avoid polling repeatedly.
- A process keeps track of the local hardware changes and flushes when necessary to the LMS server.

## Requirements:

### Software
- TODO oled driver
- PY LMS (patched): sudo pip install git+https://github.com/readingtype/PyLMS.git
- RPIO (PR): sudo pip install git+https://github.com/tylerwowen/RPIO

### Hardware

![Proof of concept](/images/hardware.jpg?raw=true "Proof of Concept")


- Raspberry Pi (Tested on a 2 Model B)
- I2C OLED screen (driven by a SSD1306) e.g. http://search.ebay.co.uk/oled i2c
- Rotary Encoder  - 4 pin with switch e.g. http://search.ebay.co.uk/ky-040


## Wiring - See http://pinout.xyz/

- Connect the OLED to the I2C pins and 3v3 and GND http://pinout.xyz/pinout/i2c
- Connect the rotary encoder to BCM 4, BCM 27. Switch to BCM 22 (you can adjust this on the command line)


## Running

```sudo python pi-squeezebox-controller.py --host [LMS server]```

You can also specify the mac address to control (defaults to the local MAC).


```
usage: pi-squeezebox-controller.py [-h] [--mac MAC] [--port PORT]
                                   [--host HOST] [--a CHANNEL_A]
                                   [--b CHANNEL_B] [--sw CHANNEL_SW]

Control a local squeezebox

optional arguments:
  -h, --help       show this help message and exit
  --mac MAC        MAC Address of the player to control
  --port PORT      port number of the LMS Server
  --host HOST      hostname or IP of the LMS Server
  --a CHANNEL_A    Rotary Encoder Channel A BCM PIN
  --b CHANNEL_B    Rotary Encoder Channel B BCM PIN
  --sw CHANNEL_SW  Switch BCM PIN
```


## TODO

- Apply to a clean pi build to test dependencies
- Build a max2play (http://max2play.com) plugin for easy install
