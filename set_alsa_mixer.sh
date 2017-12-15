#!/bin/sh

amixer -c 0 sset  'ADC1 PGA gain' 100%
amixer -c 0 sset  'ADC2 PGA gain' 100%
amixer -c 0 sset  'ADC3 PGA gain' 100%
amixer -c 0 sset  'ADC4 PGA gain' 100%
amixer -c 0 sset  'ADC5 PGA gain' 100%
amixer -c 0 sset  'ADC6 PGA gain' 100%
amixer -c 0 sset  'ADC7 PGA gain' 100%
amixer -c 0 sset  'ADC8 PGA gain' 100%

amixer -c 0 sset  'CH1 volume' 64%
amixer -c 0 sset  'CH2 volume' 64%
amixer -c 0 sset  'CH3 volume' 64%
amixer -c 0 sset  'CH4 volume' 64%
amixer -c 0 sset  'CH5 volume' 64%
amixer -c 0 sset  'CH6 volume' 64%
amixer -c 0 sset  'CH7 volume' 64%
amixer -c 0 sset  'CH8 volume' 64%

amixer -c 0 cset numid=17 80%

