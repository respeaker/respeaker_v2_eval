"""
Search keyword "alexa" and estimate the direction of arrival

Requirement:
    sudo apt-get install python-numpy
    pip install webrtc-audio-processing
"""


import time
import logging
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.ns import NS
from voice_engine.kws import KWS
from doa_respeaker_v2_6mic_array import DOA
from pixels import pixels


def main():
    logging.basicConfig(level=logging.DEBUG)

    src = Source(rate=16000, channels=8)
    ch1 = ChannelPicker(channels=8, pick=1)
    ns = NS(rate=16000, channels=1)
    kws = KWS(model='alexa')
    doa = DOA(rate=16000)

    src.link(ch1)
    ch1.link(ns)
    ns.link(kws)

    src.link(doa)

    def on_detected(keyword):
        direction = doa.get_direction()
        logging.info('detected {} at direction {}'.format(keyword, direction))
        pixels.wakeup(direction)

    kws.on_detected = on_detected

    src.recursive_start()

    while True:
        try:
            time.sleep(0.05)
            #direction = doa.get_direction()
            #logging.info('direction {}'.format(direction))
            #pixels.wakeup(direction)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
