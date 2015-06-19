import curses
import RPi.GPIO as GPIO

PWM_FREQ = 100

SERVO_PIN = 18

#left motor
ENA_PIN = 17
IN1_PIN = 27
IN2_PIN = 22

#right motor
ENB_PIN = 18
IN3_PIN = 23
IN4_PIN = 24

MOTOR_STAY = 0
MOTOR_FORWARD = 1
MOTOR_BACKWARD = 2

class Controller:
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(SERVO_PIN, GPIO.OUT)
		GPIO.setup(ENA_PIN, GPIO.OUT)
		GPIO.setup(IN1_PIN, GPIO.OUT)
		GPIO.setup(IN2_PIN, GPIO.OUT)
		GPIO.setup(ENB_PIN, GPIO.OUT)
		GPIO.setup(IN3_PIN, GPIO.OUT)
		GPIO.setup(IN4_PIN, GPIO.OUT)
		
		self.servo_pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ)
		self.servo_pwm.start(0) #init duty cycle

	def __del__(self):
		GPIO.cleanup()
		self.servo_pwm.stop()

	def setServo(self,angle):
		duty = float(angle) / 10.0 + 2.5
		pwm.servo_pwm.ChangeDutyCycle(duty)

	def setMotors(self, motion1, motion2):
		if motion1 == MOTOR_STAY:
			GPIO.output(ENA_PIN, GPIO.LOW)
		elif motion1 == MOTOR_FORWARD:
			GPIO.output(ENA_PIN, GPIO.HIGH)
			GPIO.output(IN1_PIN, GPIO.HIGH)
			GPIO.output(IN2_PIN, GPIO.LOW)
		else:
			GPIO.output(ENA_PIN, GPIO.HIGH)
			GPIO.output(IN1_PIN, GPIO.LOW)
			GPIO.output(IN2_PIN, GPIO.HIGH)

		if motion2 == MOTOR_STAY:
			GPIO.output(ENB_PIN, GPIO.LOW)
		elif motion2 == MOTOR_FORWARD:
			GPIO.output(ENB_PIN, GPIO.HIGH)
			GPIO.output(IN3_PIN, GPIO.HIGH)
			GPIO.output(IN4_PIN, GPIO.LOW)
		else:
			GPIO.output(ENB_PIN, GPIO.HIGH)
			GPIO.output(IN3_PIN, GPIO.LOW)
			GPIO.output(IN4_PIN, GPIO.HIGH)

	def stay(self):
		self.setMotors( MOTOR_STAY, MOTOR_STAY)

	def goForward(self):
		self.setMotors( MOTOR_FORWARD, MOTOR_FORWARD)

	def goBack(self):	
		self.setMotors( MOTOR_BACKWARD, MOTOR_BACKWARD)

	def goLeft(self):
		self.setMotors( MOTOR_BACKWARD, MOTOR_FORWARD)

	def goRigth(self):
		self.setMotors( MOTOR_FORWARD, MOTOR_BACKWARD)

if __name__=="__main__":
	screen = curses.initscr()
	curses.cbreak()
	curses.noecho()
	screen.keypad(True)
	
	con = Controller()
	try:
		while True:
			key = screen.getch()
			if key == ord('q'):
				screen.addstr(0, 0, 'quit ')
				break

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
				con.goRigth()			
			else:
				screen.addstr(0, 0, 'err  ')

	finally:
		curses.nocbreak(); screen.keypad(0); curses.echo()
		curses.endwin()