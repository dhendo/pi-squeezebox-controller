# coding=utf-8

import time
from ctypes import c_char
from multiprocessing import Process, Value, Manager, Array
import argparse

if __name__ == '__main__':
    volume = Value('i', 0)
    playing = Value('i', 1)
    text = Array(c_char, "*" * 1000)
    text2 = Array(c_char, "*" * 100)
    text.value = ""
    text2.value = ""

    parser = argparse.ArgumentParser(description='Control a local squeezebox')
    parser.add_argument('--mac', dest='mac', action='store',
                        default=None,
                        help='MAC Address of the player to control')

    parser.add_argument('--port', dest='port', action='store',
                        default=9090,
                        help='port number of the LMS Server')

    parser.add_argument('--host', dest='host', action='store',
                        default="127.0.0.1",
                        help='hostname or IP of the LMS Server')

    parser.add_argument('--a', dest='channel_a', action='store',
                        default=27,
                        help='Rotary Encoder Channel A BCM PIN')

    parser.add_argument('--b', dest='channel_b', action='store',
                        default=4,
                        help='Rotary Encoder Channel B BCM PIN')

    parser.add_argument('--sw', dest='channel_sw', action='store',
                        default=22,
                        help='Switch BCM PIN')

    args = parser.parse_args()

    if args.mac:
        print "here"
        MAC = args.mac
    else:
        MAC = open('/sys/class/net/eth0/address').read().strip()

    host = args.host
    port = args.port

    from volume_process import volume_process

    p = Process(target=volume_process, args=(volume, playing, args.channel_a, args.channel_b, args.channel_sw), name="Volume Process")
    p.start()

    from display_process import display_process

    p2 = Process(target=display_process, args=(volume, text, text2, playing), name="Display Process")
    p2.start()

    from local_change_process import local_change_process

    p3 = Process(target=local_change_process, args=(text, text2, volume, playing, MAC, host, port),
                 name="Player Process")
    p3.start()

    from player_change_process import player_change_process

    p4 = Process(target=player_change_process, args=(text, volume, playing, MAC, host, port), name="Player Process")
    p4.start()

    import signal
    import sys


    def signal_handler(signal, frame):
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)


    # p.join()
