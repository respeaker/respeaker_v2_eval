"""
Hands-free Voice Assistant with Snowboy and Alexa Voice Service. The wake-up keyword is "snowboy"

Requirement:
    pip install avs
    pip install spidev
"""


import time
import logging
from voice_engine.source import Source
from voice_engine.kws import KWS
from avs.alexa import Alexa
from pixels import pixels


def main():
    logging.basicConfig(level=logging.DEBUG)

    src = Source(rate=16000)
    kws = KWS(model='alexa')
    alexa = Alexa()

    alexa.state_listener.on_listening = pixels.listen
    alexa.state_listener.on_thinking = pixels.think
    alexa.state_listener.on_speaking = pixels.speak
    alexa.state_listener.on_finished = pixels.off

    def on_detected(keyword):
        logging.info('detected {}'.format(keyword))
        alexa.listen()

    kws.on_detected = on_detected

    src.link(kws)
    kws.link(alexa)

    src.recursive_start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
