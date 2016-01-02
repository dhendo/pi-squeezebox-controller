from pylms.server import Server
from pylms.client import Client
import time

def local_change_process(textSync, text2Sync, volumeSync, playingSync, MAC, host, port):

    try:
        sc = Server(hostname=host, port=port)
        sc.connect(update=False)

        print "Logged in: %s" % sc.logged_in
        print "Version: %s" % sc.get_version()


        localVolume = volumeSync.value
        localPlaying = playingSync.value

        player = sc.get_player(unicode(MAC))


        if player:
            localVolume = player.get_volume()
            text2Sync.value = player.get_name()
            volumeSync.value = localVolume
            print player.get_mode()

            mode = player.get_mode()

            if mode == "play":
                localPlaying = 1
            elif mode == "stop":
                localPlaying = -1
            else:
                localPlaying = 0

            playingSync.value = localPlaying
            print "Controlling player: %s (%s)" % (player.get_name(), MAC)
        else:
            print "No Player found"



        while (1):
            if player:
                if localVolume != volumeSync.value:
                    # Volume Changed by hardware
                    localVolume = volumeSync.value
                    player.set_volume(localVolume)


                if localPlaying != playingSync.value:
                    # State Changed by hardware
                    localPlaying = playingSync.value
                    if localPlaying == 1:
                        player.unpause()
                    elif localPlaying == 0:
                        player.pause()
                    elif localPlaying == -1:
                        pass# stop
            time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        print "Exiting Player Update Process"