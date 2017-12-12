#!/bin/sh

echo 1066 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio1066/direction
echo 0 > /sys/class/gpio/gpio1066/value
