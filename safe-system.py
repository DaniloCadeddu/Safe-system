import RPi.GPIO as GPIO # Iporting the gpio module for raspberry pi
import Keypad # Importing the module for controlling the keypad
import time
import random   
import math  
ROWS = 4        
COLS = 4        
keys =  [   '1','2','3','A',        # Defining the keypad chars
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [12,16,18,22]        # Every pin has a char associated with
colsPins = [19,15,13,11]       
pins = [29,31,32] # Pin associated with the rgb led
buzzerPin = 33 # Pin that controls the buzzer
password = '1234' # Put whatever you want as safe password
input_utente = '' # A string that contains every character the user press

# Standard setup of the gpio e and all the pins involved in the project
def setup():
	global pwmRed,pwmGreen,pwmBlue
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(buzzerPin, GPIO.OUT)
	GPIO.output(buzzerPin,GPIO.LOW)
	GPIO.setup(pins, GPIO.OUT)
	GPIO.output(pins, GPIO.HIGH)
	pwmRed = GPIO.PWM(pins[0], 2000)
	pwmGreen = GPIO.PWM(pins[1], 2000)
	pwmBlue = GPIO.PWM(pins[2], 2000)
	pwmRed.start(100)
	pwmGreen.start(100)
	pwmBlue.start(100)

# Setting the rgb color of the led
def setColor(r_val,g_val,b_val):
	pwmRed.ChangeDutyCycle(r_val)
	pwmGreen.ChangeDutyCycle(g_val)
	pwmBlue.ChangeDutyCycle(b_val)

# When the input password is wrong this function is called. The led start blinking red and the buzzer sound
def alert():
	i = 0
	while i < 3:
		r = 0
		g = 100
		b = 100
		setColor(r,g,b)
		GPIO.output(buzzerPin,GPIO.HIGH)
		time.sleep(0.6)
		r = 100
		g = 100
		b = 100
		setColor(r,g,b)
		GPIO.output(buzzerPin,GPIO.LOW)
		time.sleep(0.6)
		i += 1

# Main function of the program
def loop():
	global input_utente
	
	# Setting the keypad to be able to get the input
	keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)
	keypad.setDebounceTime(50)
	
	while(True):
		# Taking 4 chars as input 
		for i in range(4):
			key = keypad.getKey()
			if(key != keypad.NULL):
				input_utente += key
				print("*")

		# If the password has the right length 	
		if (len(input_utente) == 4):
			# Turn the led green if the password is right
			if(input_utente == password):
				r = 100
				g = 100
				b = 0
				setColor(r,g,b)
			else:
				alert()
			
			
if __name__ == '__main__':
    print ("Program is starting ... ")
    setup()
    try:
        loop()
    except KeyboardInterrupt: 
        GPIO.cleanup()

