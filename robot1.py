import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

STBY = 7

AIN1 = 11
PWMA = 12
AIN2 = 13

BIN1 = 15
BIN2 = 16
PWMB = 33

#pins = [AIN1, AIN2, PWMA, STBY, BIN1, BIN2, PWMB]
#for pin in pins:
GPIO.setup(STBY, GPIO.OUT)
GPIO.output(STBY, GPIO.HIGH)
#GPIO.output(BIN1, GPIO.LOW)
#GPIO.output(AIN1, GPIO.LOW)
#pa = GPIO.PWM(PWMA, 100)
#pb = GPIO.PWM(PWMB, 100)
#pa.start(0)
#pb.start(0)

class motorClass:
    def __init__(self, IN1, IN2, PWM):
        self.IN1 = IN1
        self.IN2 = IN2
        self.PWM = PWM
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(PWM, GPIO.OUT)

        self.p = GPIO.PWM(PWM, 100)
        self.p.start(0)

    def setPower(self, power):
        IN1 = self.IN1
        IN2 = self.IN2
        
        if power < 0:
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            self.p.ChangeDutyCycle(abs(power))
            
        elif power > 0:
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            self.p.ChangeDutyCycle(abs(power))
        else:
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            self.p.ChangeDutyCycle(abs(power))

motorA = motorClass(AIN1, AIN2, PWMA)
motorB = motorClass(AIN1, AIN2, PWMB)

def goTime(seconds, powerA=50, powerB=50):
    motorA.setPower(powerA)
    motorB.setPower(powerB)
    time.sleep(seconds)
    motorA.setPower(0)
    motorB.setPower(0)

def setDir(direction=None):
    if direction == "forward":
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)

        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
        
    elif direction == "left":
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)

        GPIO.output(BIN2, GPIO.LOW)
        GPIO.output(BIN1, GPIO.HIGH)

    elif direction == "right":
        GPIO.output(AIN2, GPIO.HIGH)
        GPIO.output(AIN1, GPIO.LOW)

        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
        
    else:
        
        GPIO.output(AIN2, GPIO.HIGH)
        GPIO.output(AIN1, GPIO.LOW)

        GPIO.output(BIN2, GPIO.LOW)
        GPIO.output(BIN1, GPIO.HIGH)

def setSpeed(power):
    pa.ChangeDutyCycle(power)
    pb.ChangeDutyCycle(power)
