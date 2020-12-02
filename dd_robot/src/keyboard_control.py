#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import curses

rospy.init_node('keyboard_control', anonymous=True)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

move_vect = Twist()

# Movment Variables
movement_speed = 1.0
movement_increment = 0.1

# Curses Init
screen = curses.initscr()
curses.noecho()
curses.cbreak()

# Screen Text Information
screen.addstr(0, 0, "------------------------------------------------")
screen.addstr(1, 0, "--------- dd_robot keyboard controller ---------")
screen.addstr(2, 0, "------------------------------------------------")
screen.addstr(3, 0, "- Press w to move forward")
screen.addstr(4, 0, "- Press a to turn left")
screen.addstr(5, 0, "- Press s to move backwards")
screen.addstr(6, 0, "- Press d to turn right")
screen.addstr(7, 0, "- Press i to increase the movement speed")
screen.addstr(8, 0, "- Press k to decrease the movement speed")
screen.addstr(9, 0, "- Press q to quit the program")
screen.addstr(10, 0, "- Press any other key to stop")
screen.addstr(12, 0, "Moving State: idle")
screen.addstr(13, 0, "Current Speed: 1.0")
screen.addstr(14, 0, "Target Speed:  1.0")

def key2ros(x, y, msg):
    global screen

    move_vect.linear.x = x
    move_vect.linear.y = y
    pub.publish(move_vect)
    
    screen.addstr(12, 14, "                ")
    screen.addstr(12, 14, msg)
    screen.addstr(13, 15, str(float(movement_speed)))

# Keyboard Loop:
try:
    while True:
        char = screen.getch()

        if char == ord('q'):
            break
        elif char == ord('w'):
            key2ros(0, movement_speed, "Moving forward")
        elif char == ord('s'):
            key2ros(0, -movement_speed, "Moving backwards")
        elif char == ord('a'):
            key2ros(movement_speed, 0, "Turning left")
        elif char == ord('d'):
            key2ros(-movement_speed, 0, "Turning right")
        elif char == ord('i'):
            movement_speed += movement_increment
            if (movement_speed > 1):
                movement_speed = 1
            screen.addstr(14, 15, str(movement_speed))
        elif char == ord('k'):
            movement_speed -= movement_increment
            if (movement_speed < 0.1):
                movement_speed = 0.1
            screen.addstr(14, 15, str(movement_speed))
        else:
            key2ros(0, 0, "Stopping")

        screen.move(15, 0)
finally:
    curses.nocbreak()
    curses.echo()
    curses.endwin()