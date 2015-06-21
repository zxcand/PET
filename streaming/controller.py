import curses
import RPi.GPIO as GPIO

PWM_FREQ = 100

SERVO_PIN  = 18
MOTOR_PIN1 = 27 #IN1 on L298
MOTOR_PIN2 = 22 #IN2 on L298
MOTOR_PIN3 = 23 #IN3 on L298
MOTOR_PIN4 = 24 #IN4 on L298

MOTOR_STAY = 0
MOTOR_FORWARD = 1
MOTOR_BACKWARD = 2

class Controller:
	servo_angle = 0

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(SERVO_PIN, GPIO.OUT)
		
		GPIO.setup(MOTOR_PIN1, GPIO.OUT)
		GPIO.setup(MOTOR_PIN2, GPIO.OUT)
	
		GPIO.setup(MOTOR_PIN3, GPIO.OUT)
		GPIO.setup(MOTOR_PIN4, GPIO.OUT)
		
		self.servo_pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ)
		self.servo_pwm.start(0) #init duty cycle

	def __del__(self):
		GPIO.cleanup()
		self.servo_pwm.stop()

	def setServo(self,angle):
		duty = float(angle) / 10.0 + 2.5
		pwm.servo_pwm.ChangeDutyCycle(duty)

	def lookUpper(self):
		self.servo_angle = self.servo_angle + 5
		self.setServo(self.servo_angle)

	def lookLower(self):
		self.servo_angle = self.servo_angle - 5
		self.setServo(self.servo_angle)

	def setMotors(self, motion1, motion2):
		if motion1 == MOTOR_STAY:
			GPIO.output(MOTOR_PIN1, GPIO.LOW)
			GPIO.output(MOTOR_PIN2, GPIO.LOW)
		elif motion1 == MOTOR_FORWARD:
			GPIO.output(MOTOR_PIN1, GPIO.HIGH)
			GPIO.output(MOTOR_PIN2, GPIO.LOW)
		else:
			GPIO.output(MOTOR_PIN1, GPIO.LOW)
			GPIO.output(MOTOR_PIN2, GPIO.HIGH)

		if motion2 == MOTOR_STAY:
			GPIO.output(MOTOR_PIN3, GPIO.LOW)
			GPIO.output(MOTOR_PIN4, GPIO.LOW)
		elif motion2 == MOTOR_FORWARD:
			GPIO.output(MOTOR_PIN3, GPIO.HIGH)
			GPIO.output(MOTOR_PIN4, GPIO.LOW)
		else:
			GPIO.output(MOTOR_PIN3, GPIO.LOW)
			GPIO.output(MOTOR_PIN4, GPIO.HIGH)

	def goStay(self):
		self.setMotors( MOTOR_STAY, MOTOR_STAY)

	def goForward(self):
		self.setMotors( MOTOR_FORWARD, MOTOR_FORWARD)

	def goBack(self):	
		self.setMotors( MOTOR_BACKWARD, MOTOR_BACKWARD)

	def goLeft(self):
		self.setMotors( MOTOR_BACKWARD, MOTOR_FORWARD)

	def goRight(self):
		self.setMotors( MOTOR_FORWARD, MOTOR_BACKWARD)

if __name__=="__main__":
	con = Controller()

	screen = curses.initscr()
	curses.cbreak()
	curses.noecho()
	screen.keypad(True)
	
	try:
		while True:
			key = screen.getch()
			if key == ord('q'):
				screen.addstr(0, 0, 'quit ')
				break
			elif key == ord('1'):

				setServo()
			elif key == ord('2'):
			
			elif key == ord('s'):
				screen.addstr(0, 0, 'stay ')
				con.goStay()
			elif key == curses.KEY_UP: #Up arrow
				screen.addstr(0, 0, 'up   ')
				con.goForward()
			elif key == curses.KEY_DOWN: #Down arrow
				screen.addstr(0, 0, 'down ')
				con.goBack()
			elif key == curses.KEY_LEFT: #Left arrow
				screen.addstr(0, 0, 'left ')
				con.goLeft()
			elif key == curses.KEY_RIGHT: #Right arrow
				screen.addstr(0, 0, 'right')
				con.goRight()			
			else:
				screen.addstr(0, 0, 'err  ')

	finally:
		curses.nocbreak(); screen.keypad(0); curses.echo()
		curses.endwin()