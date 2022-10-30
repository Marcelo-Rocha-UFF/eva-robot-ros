import rospy
from std_msgs.msg import String

import time
from tkinter import *
import threading



def gui_init():
  global root, canvas, eye_img
  root = Tk()
  root.geometry("456x243")
  canvas = Canvas (root, width=456, height=243 )
  eye_img = PhotoImage(file = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/eyes_images/eyes_neutral.png")
  canvas.create_image(228, 120, image=eye_img)
  canvas.pack()
  root.mainloop()
   

def eyes_node_callback(data):
  global eye_img
  if data.data.lower() == "neutral":
    rospy.loginfo(data.data)
    eye_img = PhotoImage(file = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/eyes_images/eyes_neutral.png")
    canvas.create_image(228, 120, image=eye_img)

  elif data.data.lower() == "angry":
    rospy.loginfo(data.data)
    eye_img = PhotoImage(file = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/eyes_images/eyes_angry.png")
    canvas.create_image(228, 120, image=eye_img)

  elif data.data.lower() == "happy":
    rospy.loginfo(data.data)
    eye_img = PhotoImage(file = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/eyes_images/eyes_happy.png")
    canvas.create_image(228, 120, image=eye_img)

  elif data.data.lower() == "sad":
    rospy.loginfo(data.data)
    eye_img = PhotoImage(file = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/eyes_images/eyes_sad.png")
    canvas.create_image(228, 120, image=eye_img)



def node_init():
  rospy.init_node('eyes_display_node', anonymous=False)
  rospy.Subscriber('eyes_display_node/emotion', String, eyes_node_callback)



  threading.Thread(target=gui_init().start())
  # spin() simply keeps python from exiting until this node is stopped

  rospy.spin()



if __name__ == '__main__':
  node_init()
