from pylms.server import Server
from pylms.client import Client
from pylms.player import Player
from unicodedata import normalize
import time


class RClient(Client):
    def __init__(self,
                 hostname="localhost",
                 port=9090,
                 username="",
                 password="",
                 charset="utf8", mac_filter=None, volumeSync=None, playingSync=None, textSync=None):

        self.mac_filter = mac_filter
        self.volumeSync = volumeSync
        self.playingSync = playingSync
        self.textSync = textSync

        self.hplayer = None

        super(Client, self).__init__(hostname=hostname, port=port, username=username, password=password,
                                     charset=charset)

    def update(self, data):
        if self.mac_filter and data[0] == self.mac_filter:

            print "*** %s" % data
            player = self.hplayer
            if data[1] == "playlist":
                if data[2] == "newsong":
                    trackname = unicode(data[3])
                    artist = player.get_track_artist().strip()
                    self.setText(artist, trackname)
                    self.playingSync.value = 1
                if data[2] == "jump":
                    time.sleep(1)
                    trackname = unicode(player.get_track_title())
                    artist = unicode(player.get_track_artist().strip())
                    self.setText(artist, trackname)
                    self.playingSync.value = 1

                if data[2] == "index":
                    trackname = unicode(player.get_track_title())
                    artist = unicode(player.get_track_artist())

                    self.setText(artist, trackname)
                    self.playingSync.value = 1

            if data[1] == "mode":
                if data[2] == "stop":
                    self.playingSync.value = -1  # off
            if data[1] == "power":
                if data[2] == "0":
                    self.playingSync.value = -1  # off

            elif data[1] == "prefset":
                if data[2] == "server" and data[3] == "volume":
                    self.volumeSync.value = int(round(float(data[4])))
            elif data[1] == "pause":
                if data[2] == "1" or not data[2]:
                    self.playingSync.value = 0
                else:
                    self.playingSync.value = 1
            elif data[1] == "play":
                self.playingSync.value = 1
            elif data[1] == "stop":
                self.playingSync.value = -1
            else:
                pass
                print data

    def setText(self, artist, trackname):
        displayText = ""

        # print "T:"
        # print trackname
        # print "a:"
        # print artist

        if trackname:
            trackname = trackname.replace("_", " ")
            if artist and not "http:" in artist and not "https:" in artist:
                displayText = "%s - %s" % (artist, trackname)
            else:
                displayText = "%s" % trackname
        elif artist:
            if artist and not "http:" in artist and not "https:" in artist:
                displayText = artist

        if not displayText:
            displayText = "[Unknown]"

        displayText = unicode(displayText).strip()
        displayText = normalize('NFD', displayText).encode('ascii', 'ignore')
        self.textSync.value = displayText[:1000]


def player_change_process(textSync, volumeSync, playingSync, mac, host, port):
    try:

        # Http version
        sv = Server(hostname=host, port=port)
        sv.connect(update=False)

        # Telnet
        sc = RClient(hostname=host, port=port, mac_filter=mac, textSync=textSync, playingSync=playingSync,
                     volumeSync=volumeSync)
        sc.connect(update=False)

        print "Logged in: %s" % sv.logged_in
        print "Version: %s" % sv.get_version()

        sc.hplayer = sv.get_player(mac)
        trackname = sc.hplayer.get_track_title().strip()
        artist = sc.hplayer.get_track_artist().strip()

        sc.setText(artist, trackname)

        sc.start()
    except (KeyboardInterrupt, SystemExit):
        print "Exiting LMS Telnet Process"
