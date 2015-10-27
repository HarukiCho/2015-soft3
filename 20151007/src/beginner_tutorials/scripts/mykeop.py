import roslib
import rospy
import sys
from std_msgs.msg import String
from geometry_msgs.msg import Twist

import termios
import sys,select
import time
import os
 
TERMIOS=termios
 
def getkey():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
        new[6][TERMIOS.VMIN] = 0
        new[6][TERMIOS.VTIME] = 1
        termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
        c = None
        try:
            c = os.read(fd, 1)
        finally:
            termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
        return c

class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def mykeyop():
    pub = rospy.Publisher('mobile_base/commands/velocity', Twist)
    rospy.init_node('mykeyop')
    cmd = Twist();
    cmd.linear.x = 0.0;
    cmd.linear.y = 0.0;
    cmd.linear.z = 0.0;
    cmd.angular.x = 0.0;
    cmd.angular.y = 0.0;
    cmd.angular.z = 0.0;
    while not rospy.is_shutdown():
        #getch = _Getch()
        #x = getch()
        x = getkey()

        if(x == 'k'):
            cmd.linear.x = cmd.linear.x + 0.1
        elif(x == 'j'):
            cmd.linear.x = cmd.linear.x - 0.1
        elif(x == 'h'):
            cmd.angular.z = cmd.angular.z + 0.1
        elif(x == 'l'):
            cmd.angular.z = cmd.angular.z - 0.1
        elif(x == 'q'):
            sys.exit()
        #print x
        print cmd.linear.x
        print cmd.angular.z
        pub.publish(cmd)

if __name__ == '__main__':
    try:
        mykeyop()
    except rospy.ROSInterruptException: pass
