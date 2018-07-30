import machine
import sdcard
import os

sd = sdcard.SDCard(machine.SPI(1), machine.Pin(19))
