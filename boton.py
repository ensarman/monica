#!/usr/bin/python

from gpiozero import Button
from subprocess import check_call
from signal import pause

def shutdown():
    check_call(['sudo', 'poweroff'])

def decir_hola():
	print("presionado por 2 segundos")

shutdown_btn = Button(3, hold_time=2)
shutdown_btn.when_held = shutdown
#shutdown_btn.when_held = decir_hola

pause()
