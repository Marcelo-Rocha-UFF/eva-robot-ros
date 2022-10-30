import rospy
from std_msgs.msg import String

import time
from tkinter import *
import threading



def gui_init():
  global window, canvas, display_img
  window = Tk()
  window.title("EVA - Display")
  window.geometry("456x256")
  canvas = Canvas (window, width=456, height=243 )
  display_img = PhotoImage(file = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/eyes_images/eyes_neutral.png")
  canvas.create_image(228, 128, image=display_img)
  canvas.pack()
  window.mainloop()
   

def emotion_callback(data):
  global display_img
  if data.data.lower() == "neutral":
    rospy.loginfo(data.data)
    display_img = PhotoImage(file = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/eyes_images/eyes_neutral.png")
    canvas.create_image(228, 128, image=display_img)

  elif data.data.lower() == "angry":
    rospy.loginfo(data.data)
    display_img = PhotoImage(file = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/eyes_images/eyes_angry.png")
    canvas.create_image(228, 128, image=display_img)

  elif data.data.lower() == "happy":
    rospy.loginfo(data.data)
    display_img = PhotoImage(file = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/eyes_images/eyes_happy.png")
    canvas.create_image(228, 128, image=display_img)

  elif data.data.lower() == "sad":
    rospy.loginfo(data.data)
    display_img = PhotoImage(file = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/eyes_images/eyes_sad.png")
    canvas.create_image(228, 128, image=display_img)

def image_callback(data):
  global display_img
  rospy.loginfo(data.data)
  display_img = PhotoImage(file = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/images/" + data.data)
  canvas.create_image(228, 128, image=display_img)


def node_init():
  rospy.init_node('display_node', anonymous=False)
  rospy.Subscriber('display_node/emotion', String, emotion_callback)
  rospy.Subscriber('display_node/image', String, image_callback)



  threading.Thread(target=gui_init().start())
  # spin() simply keeps python from exiting until this node is stopped

  rospy.spin()



if __name__ == '__main__':
  node_init()
