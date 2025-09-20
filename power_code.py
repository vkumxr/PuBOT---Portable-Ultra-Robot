#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Pin definitions
IN1 = 11
IN2 = 13  
IN3 = 15
IN4 = 16
ENA = 12
ENB = 18

print("=== L298N DIAGNOSTIC TEST ===")
print("This will help identify power and connection issues")
print()

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)

def test_without_pwm():
    """Test motors at full speed without PWM"""
    print("Testing WITHOUT PWM (full power)...")
    
    # Enable motors at full power (HIGH = 100% speed)
    GPIO.output(ENA, GPIO.HIGH)  
    GPIO.output(ENB, GPIO.HIGH)
    
    print("Left motor forward (5 seconds)...")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(5)
    
    # Stop
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    print("Stopped. Did left wheels move? (buzzing = power issue)")
    input("Press Enter to continue...")
    
    print("Right motor forward (5 seconds)...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(5)
    
    # Stop
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    print("Stopped. Did right wheels move?")
    input("Press Enter to continue...")
    
    print("Left motor backward (5 seconds)...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(5)
    
    # Stop
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    print("Stopped. Did left wheels move backward?")
    input("Press Enter to continue...")
    
    print("Right motor backward (5 seconds)...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(5)
    
    # Stop
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    print("Stopped. Did right wheels move backward?")
    input("Press Enter to continue...")
    
    # Test both forward
    print("Both motors forward (5 seconds)...")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(5)
    
    # Stop
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    print("Stopped. Did both sides move forward?")
    input("Press Enter to continue...")
    
    # Test both backward
    print("Both motors backward (5 seconds)...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(5)
    
    # Final stop
    GPIO.output([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.LOW)
    print("Test complete!")

def main():
    try:
        print("IMPORTANT CHECKS FIRST:")
        print("1. Is L298N getting power? (LED should be on)")
        print("2. Are motors connected to OUT1,OUT2 and OUT3,OUT4?")
        print("3. Is external power connected if motors need >5V?")
        print()
        input("Press Enter when ready...")
        
        test_without_pwm()
        
    except KeyboardInterrupt:
        print("\nTest interrupted")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()