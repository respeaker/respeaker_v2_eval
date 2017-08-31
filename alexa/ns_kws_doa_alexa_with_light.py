"""
Hands-free Voice Assistant with Snowboy and Alexa Voice Service. The wake-up keyword is "snowboy"

Requirement:
    sudo apt-get install python-numpy
    pip install webrtc-audio-processing
    pip install spidev
"""


import time
import logging
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.ns import NS
from voice_engine.doa_respeaker_6p1_mic_array import DOA
from avs.alexa import Alexa
from pixels import pixels


def main():
    logging.basicConfig(level=logging.DEBUG)

    src = Source(rate=16000, channels=8)
    ch1 = ChannelPicker(channels=8, pick=1)
    ns = NS(rate=16000, channels=1)
    kws = KWS()
    doa = DOA(rate=16000)
    alexa = Alexa()

    alexa.state_listener.on_listening = pixels.listen
    alexa.state_listener.on_thinking = pixels.think
    alexa.state_listener.on_speaking = pixels.speak
    alexa.state_listener.on_finished = pixels.off

    def on_detected(keyword):
        logging.info('detected {} at direction {}'.format(keyword, doa.get_direction()))
        alexa.listen()

    kws.on_detected = on_detected

    src.link(ch1)
    ch1.link(ns)
    ns.link(kws)
    kws.link(alexa)

    src.link(doa)

    src.recursive_start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
