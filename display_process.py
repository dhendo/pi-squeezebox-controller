from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont
import time



def display_process(volumeSync, textSync, text2Sync, playingSync):
    try:
        device = ssd1306(port=1, address=0x3C)

        text = textSync.value
        lastText = text
        offset = 0
        text2offset = 0
        textHeight = 20
        font = ImageFont.truetype('bold_dot_digital-7.ttf', textHeight)

        while (1):
            text = textSync.value
            text2 = text2Sync.value.upper().strip()

            playing = playingSync.value
            volume = volumeSync.value

            bg = 0
            fg = 255

            if lastText != text:
                offset = 0

            textLength = font.getsize("%s " % text)[0]

            # Something nasty - with the font or PIL? Adds in extra gap at the end
            text2Length = font.getsize("%s " % text2)[0] - 16


            text2offset = int(round((device.width/2) - (text2Length/2)))




            if text:
                displayText = "%s %s" % (text, text)
            else:
                displayText = ""

            with canvas(device) as draw:




                # Draw some shapes.
                # First define some constants to allow easy resizing of shapes.
                padding = 2
                top = padding
                # Draw a rectangle of the same size of screen
                #draw.rectangle((0, 0, device.width-1, device.height-1), outline=255, fill=0)
                #draw.rectangle((15, 0, device.width-16, device.height-1), outline=255, fill=0)



                playGap = 14

                # Volume area
                draw.rectangle((0, 0, (device.width - 1) - playGap - padding, 15), outline=255, fill=0)
                volperc = round(((device.width - (playGap + 2 + padding)) * volume) / 100)
                draw.rectangle((0, 1, volperc, 15), outline=255, fill=255)


                # draw.rectangle((0, 16, device.width - 1, device.height - 1), outline=bg, fill=bg)

                x = padding
                # Write two lines of text.
                #draw.rectangle((text2offset, (top + 15 + (padding*2) + textHeight ), text2offset + text2Length, device.height-1), outline=255, fill=0)
                draw.text((x - offset, top + 18), displayText, font=font, fill=fg)
                draw.text((text2offset, top + 15 + (padding*5) + textHeight ), text2, font=font, fill=fg)


                # Play  / Paused

                startx = device.width + padding - playGap
                starty = 2

                if playing == 1:
                    playheight = 9
                    playwidth = 8

                    definition = [(startx, starty + playheight), (startx, starty),
                                  (startx + playwidth, (1 + starty + int(playheight / 2)))]
                    draw.polygon(definition, outline=255, fill=255)

                elif playing == 0:

                    barwidth = 3
                    barheight = 9
                    bargap = 3

                    draw.rectangle((startx, starty, startx + barwidth, starty + barheight), outline=255, fill=255)
                    draw.rectangle((startx + barwidth + bargap, starty, startx + barwidth + barwidth + bargap,
                                    starty + barheight), outline=255, fill=255)


                else:
                    # Off
                    draw.rectangle((0, 0, device.width-1, device.height-1), outline=0, fill=0)







            offset += 7
            if offset > textLength:
                offset = 0

            lastText = text
            time.sleep(0.25)
    except (KeyboardInterrupt, SystemExit):

        with canvas(device) as draw:
            draw.rectangle((0, 0, (device.width - 1), device.height - 1), outline=0, fill=0)
        print "Exiting Display Process"
