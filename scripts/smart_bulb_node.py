# python3.6

import socket
import rospy
from std_msgs.msg import String

HOST = "192.168.1.105"  # IP da XIAOMI
PORT = 55443  # Port used by the server


def state_callback(data): # controla o estado da lampada
  rospy.loginfo(rospy.get_caller_id() + ' I heard %s', data.data)
  if data.data == "on":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      s.sendall(b'{"id":1, "method":"set_power","params":["on", "smooth", 10]}\r\n')
  else:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      s.sendall(b'{"id":1, "method":"set_power","params":["off", "smooth", 10]}\r\n')
      
def color_callback(data): # controla a cor da lampada
  rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
  if data.data == "on":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      s.sendall(b'{"id":1, "method":"set_power","params":["on", "smooth", 10]}\r\n')
  else:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      s.sendall(b'{"id":1, "method":"set_power","params":["off", "smooth", 10]}\r\n')

def node_init():

  rospy.init_node('smart_bulb_node', anonymous=False)

  rospy.Subscriber('smart_bulb_node/state', String, state_callback)
  rospy.Subscriber('smart_bulb_node/color', String, color_callback)

  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()

if __name__ == '__main__':
  node_init()
