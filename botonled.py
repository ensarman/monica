from gpiozero import Button, PWMLED
from signal import pause

led = PWMLED(17)
button = Button(3)

#button.when_pressed = led.on
#button.when_released = led.off

led.off()
	
def pulsar():	
	led.pulse(0.2,0.2,6)
	#led.blink(on_time=1, off_time=1, fade_in_time=0, fade_out_time=0, n=None, background=True)
	
button.when_pressed = pulsar

pause()
