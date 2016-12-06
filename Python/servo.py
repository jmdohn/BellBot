#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from flask import request
from flask_api import FlaskAPI


app = FlaskAPI(__name__)

# When going to the flask server, display the url for requesting to ring the bell
@app.route('/', methods=['GET'])
def api_root():
	return {
		"ring_url" : request.url + "ring/(FAST | MEDIUM | SLOW)/times",
                "ring_url_POST": {"speed" : "(FAST | MEDIUM | SLOW)", "times": "[0-9]*"}
		}

# Function to ring the bell
# Param: Speed - how fast or slow to ring the bell
# Param: Times - how many times to ring the bell
@app.route('/ring/<speed>/<times>', methods=["GET","POST"])
def main(speed, times):
        if request.method == "POST":
		print "Setup start"

		# Setup the pin as number 12
		pin = 12
                
                GPIO.setmode(GPIO.BOARD)

                # Setup the pin
                GPIO.setup(pin,GPIO.OUT)

                # Set PWM for pin 12
                p = GPIO.PWM(pin, 50)

                # Start the pin at 180 degrees
		p.start(12.5)

		# Print the speed to the terminal
		speed = request.data.get("speed")
		print speed

                # Print the times to ring to the terminal
		times = int(request.data.get("times"))
		print times

                ring(speed, times, p)

                # Cleanup the pins after finished
                GPIO.cleanup()
		print "Setup end"       
        return {"speed": speed, "times": times}

# Ring the bell by amount of speed and number of times
def ring(speed, times, pwm):
	print "Ring Start"
	if speed == "FAST":
		frequency(0.5,0.25, times, pwm)
	elif speed == "MEDIUM":
		frequency(1, 0.25, times, pwm)
	elif speed == "SLOW":
		frequency(1, 1, times, pwm)
	print "Ring end"

# Ring the bell as fast as specified in sleep1 and sleep2
# Times is the amount of times to ring the bell
def frequency(sleep1, sleep2, times, pwm):
        for x in range(0, times):
		print "On ring " + str(x)
                pwm.ChangeDutyCycle(12.5)
                time.sleep(sleep1)
	
                pwm.ChangeDutyCycle(10)
                time.sleep(sleep2)

if __name__ == "__main__":
    app.run()
