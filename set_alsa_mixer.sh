#!/bin/sh

amixer sset  'ADC1 PGA gain' 100%
amixer sset  'ADC2 PGA gain' 100%
amixer sset  'ADC3 PGA gain' 100%
amixer sset  'ADC4 PGA gain' 100%
amixer sset  'ADC5 PGA gain' 100%
amixer sset  'ADC6 PGA gain' 100%
amixer sset  'ADC7 PGA gain' 100%
amixer sset  'ADC8 PGA gain' 100%

amixer sset  'CH1 volume' 64%
amixer sset  'CH2 volume' 64%
amixer sset  'CH3 volume' 64%
amixer sset  'CH4 volume' 64%
amixer sset  'CH5 volume' 64%
amixer sset  'CH6 volume' 64%
amixer sset  'CH7 volume' 64%
amixer sset  'CH8 volume' 64%

amixer cset numid=17 80%

