#!/usr/bin/python3

"""
    Program: ADC Basics (adc.py)
    Author:  M. Heidenreich, (c) 2020

    Description: This code is provided in support of the following YouTube tutorial:
                 https://youtu.be/BdmQcayG8Gg

    This tutorial demonstrates how to use Freenove ADC Chips PCF8591 and ADS7830
    with Raspberry Pi and Python to create a digital LED dimmer with a potentiometer.

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS
    ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
    IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
    OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,WHETHER IN AN ACTION OF CONTRACT,
    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from signal import signal, SIGTERM, SIGHUP, pause
from smbus import SMBus
from gpiozero import PWMLED
from time import sleep
from math import log10

bus = SMBus(1)
led = PWMLED(26)
steps = 255
fade_factor = (steps * log10(2))/(log10(steps))
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)


def safe_exit(signum, frame):
    exit(1)


def read_pcf8591(input):
    bus.write_byte(0x48, 0x40+input)
    return bus.read_byte(0x48)


def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)


def values(input):
    while True:
        value = read_ads7830(input)
        yield (pow(2, (value/fade_factor))-1)/steps


try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    led.source_delay = 0.05
    led.source = values(0)

    pause()

except KeyboardInterrupt:
    pass

finally:
    led.close()
