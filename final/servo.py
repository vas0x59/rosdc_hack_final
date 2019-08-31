import time
import os

def setup_gpio():
    os.system("sudo pigpiod")  # Launching GPIO library
    time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error
    import pigpio
    ESC = 17
    STEER = 18
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(ESC, 0)
    pi.set_servo_pulsewidth(STEER, 0)
    time.sleep(1)
    # pi.set_servo_pulsewidth(ESC, 1500)
    # time.sleep(1)

    return pi,ESC,STEER


def calibrate(pi,ESC):
    max_value = 2000
    min_value = 700
    pi.set_servo_pulsewidth(ESC, 0)
    print("Otkluchite pitanie i nazhmite Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Vkluchite pitanie. Vy dolzhny uslyshat 2 signala. Zatem nazhmite Enter")
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(ESC, min_value)
            print ("Zhdite ....")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print ("Ostanovite ESC ...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print ("Game over")
            # control() # You can change this to any other function you want
            pi.set_servo_pulsewidth(ESC, 1500)

def control(pi,ESC,speed,STEER,angle):
    pi.set_servo_pulsewidth(ESC, speed)
    pi.set_servo_pulsewidth(STEER,int(16.6666666*angle))

def stop(pi,ESC): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()