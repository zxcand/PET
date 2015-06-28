import curses
import RPi.GPIO as GPIO
from numpy import interp

PWM_FREQ = 50 #100
PWM_dt = 1000 / PWM_FREQ
DUTY_MAX_dt = 2.0
DUTY_MIN_dt = 0.5
DUTY_MAX = 100 * DUTY_MAX_dt / PWM_dt
DUTY_MIN = 100 * DUTY_MIN_dt / PWM_dt
ANGLE_MAX = 180
ANGLE_MIN = 0

SERVO_PIN  = 18 #p12 
MOTOR_PIN1 = 27 #p13  IN1 on L298
MOTOR_PIN2 = 22 #p15  IN2 on L298
MOTOR_PIN3 = 23 #p16  IN3 on L298
MOTOR_PIN4 = 24 #p18  IN4 on L298

MOTOR_STAY = 0
MOTOR_FORWARD = 1
MOTOR_BACKWARD = 2

class Controller:
	servo_angle = 90

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(SERVO_PIN, GPIO.OUT)
		
		GPIO.setup(MOTOR_PIN1, GPIO.OUT)
		GPIO.setup(MOTOR_PIN2, GPIO.OUT)
	
		GPIO.setup(MOTOR_PIN3, GPIO.OUT)
		GPIO.setup(MOTOR_PIN4, GPIO.OUT)
		
		self.servo_pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ) 
		self.servo_pwm.start((DUTY_MAX + DUTY_MIN)/2) #init duty cycle
		self.goStay() 
	def __del__(self):
		GPIO.cleanup()
		self.servo_pwm.stop()

	def setServo(self):
		print self.servo_angle
		duty = interp(self.servo_angle,[ANGLE_MIN,ANGLE_MAX],[DUTY_MIN,DUTY_MAX])
		self.servo_pwm.ChangeDutyCycle(duty)

	def lookUpper(self,angle):
		self.servo_angle = min(ANGLE_MAX, self.servo_angle + angle)
		self.setServo()

	def lookLower(self,angle):
		self.servo_angle = max(ANGLE_MIN, self.servo_angle - angle)
		self.setServo()

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

	def goForward(self, degree):
		self.setMotors( MOTOR_FORWARD, MOTOR_FORWARD)

	def goBack(self,degree):	
		self.setMotors( MOTOR_BACKWARD, MOTOR_BACKWARD)

	def goLeft(self,degree):
		self.setMotors( MOTOR_BACKWARD, MOTOR_FORWARD)

	def goRight(self,degree):
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
			elif key == ord('z'):
				con.lookUpper(10)
				screen.addstr(0, 0, 'upper')
			elif key == ord('x'):
				con.lookLower(10)
				screen.addstr(0, 0, 'lower')
			elif key == ord('s'):
				screen.addstr(0, 0, 'stay ')
				con.goStay()
			elif key == curses.KEY_UP: #Up arrow
				screen.addstr(0, 0, 'up   ')
				con.goForward(0)
			elif key == curses.KEY_DOWN: #Down arrow
				screen.addstr(0, 0, 'down ')
				con.goBack(0)
			elif key == curses.KEY_LEFT: #Left arrow
				screen.addstr(0, 0, 'left ')
				con.goLeft(0)
			elif key == curses.KEY_RIGHT: #Right arrow
				screen.addstr(0, 0, 'right')
				con.goRight(0)			
			else:
				screen.addstr(0, 0, 'err  ')

	finally:
		curses.nocbreak(); screen.keypad(0); curses.echo()
		curses.endwin()
		GPIO.cleanup()
