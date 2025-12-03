import RPi.GPIO as GPIO
import time
import sys
import termios
import tty

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# ---- Pins (matches your wiring) ----
ENA = 18
IN1 = 17
IN2 = 27

IN3 = 22
IN4 = 23
ENB = 19

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

pwm_left = GPIO.PWM(ENA, 1000)
pwm_right = GPIO.PWM(ENB, 1000)

pwm_left.start(100)
pwm_right.start(100)

# ----- MOVEMENT FUNCTIONS -----
def stop():
    GPIO.output(IN1,0)
    GPIO.output(IN2,0)
    GPIO.output(IN3,0)
    GPIO.output(IN4,0)

def forward():
    # reversed to fix direction
    GPIO.output(IN1,0)
    GPIO.output(IN2,1)
    GPIO.output(IN3,0)
    GPIO.output(IN4,1)

def backward():
    # reversed to fix direction
    GPIO.output(IN1,1)
    GPIO.output(IN2,0)
    GPIO.output(IN3,1)
    GPIO.output(IN4,0)

def left():
    GPIO.output(IN1,0)
    GPIO.output(IN2,1)
    GPIO.output(IN3,1)
    GPIO.output(IN4,0)

def right():
    GPIO.output(IN1,1)
    GPIO.output(IN2,0)
    GPIO.output(IN3,0)
    GPIO.output(IN4,1)

# ---- READ SINGLE CHARACTER ----
def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch1 = sys.stdin.read(1)
        if ch1 == '\x1b':  # arrow keys start
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            return ch1+ch2+ch3
        return ch1
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

print("Controls:")
print("↑ forward | ↓ backward | ← left | → right | SPACE brake | q quit")

try:
    while True:
        key = getch()

        if key == '\x1b[A':      # UP
            forward()

        elif key == '\x1b[B':    # DOWN
            backward()

        elif key == '\x1b[D':    # LEFT
            left()

        elif key == '\x1b[C':    # RIGHT
            right()

        elif key == ' ':         # SPACEBAR = brake
            stop()

        elif key == 'q':
            break

        else:
            stop()

finally:
    stop()
    pwm_left.stop()
    pwm_right.stop()
    GPIO.cleanup()
