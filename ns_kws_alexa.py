"""
Hands-free Voice Assistant with Snowboy and Alexa Voice Service. The wake-up keyword is "alexa"

Requirement:
    sudo apt-get install python-numpy
    pip install webrtc-audio-processing voice-engine avs
"""

import signal
import time
import logging
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.ns import NS
from avs.alexa import Alexa


def main():
    logging.basicConfig(level=logging.DEBUG)

    src = Source(rate=16000)
    ns = NS(rate=16000, channels=1)
    kws = KWS(model='alexa')
    alexa = Alexa()

    src.pipeline(ns, kws, alexa)

    def on_detected(keyword):
        logging.info('detected {}'.format(keyword))
        alexa.listen()

    kws.set_callback(on_detected)

    is_quit = []
    def signal_handler(signal, frame):
        is_quit.append(True)
        print('Quit')
    signal.signal(signal.SIGINT, signal_handler)

    src.pipeline_start()
    while not is_quit:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    src.pipeline_stop()


if __name__ == '__main__':
    main()
