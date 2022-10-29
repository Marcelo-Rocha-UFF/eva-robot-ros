# python3.6

import socket
import rospy
from std_msgs.msg import String

HOST = "192.168.1.105"  # IP da XIAOMI
PORT = 55443  # Port used by the server

def state_callback(data): # controla o estado da lampada
  if data.data == "on":
    rospy.loginfo("Ligando a lâmpada.")
    s.sendall(b'{"id":1, "method":"set_power","params":["on", "smooth", 100]}\r\n')
  else:
    rospy.loginfo("Desligando a lâmpada.")
    s.sendall(b'{"id":1, "method":"set_power","params":["off", "smooth", 100]}\r\n')
      
def color_name_callback(data): # controla a cor da lampada (pelo nome da cor)
  color_map = {"WHITE":"16777215", "BLACK":"0", "RED":"16711680", "PINK":"15073406", "GREEN":"65280", "YELLOW":"16776960", "BLUE":"255"}
  color_number = color_map.get(data.data.upper()) # data.data é convertido para maiuscula para evitar incompatibilidade
  st_json = '{"id":1,"method":"set_rgb","params":[' + color_number + ', "smooth", 100]}\r\n'
  s.sendall(st_json.encode())

def color_rgb_callback(data): # controla a cor da lampada (pelo valor em RGB, pode ter # ou não)
  color_number = int(data.data.replace('#', ''), base=16)
  st_json = '{"id":1,"method":"set_rgb","params":[' + str(color_number) + ', "smooth", 100]}\r\n'
  s.sendall(st_json.encode())

def node_init():
  # configurando o nó
  rospy.init_node('smart_bulb_node', anonymous=False)
  rospy.Subscriber('smart_bulb_node/state', String, state_callback)
  rospy.Subscriber('smart_bulb_node/color_name', String, color_name_callback)
  rospy.Subscriber('smart_bulb_node/color_rgb', String, color_rgb_callback)

  #conectando à lâmpada
  try:
    global s # socket de conexão com a lâmpada
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
  except socket.error as err:
    print ("socket creation failed with error %s" %(err))
  # connecting to the server
  # colocar um try aqui
  s.connect((HOST, PORT))

  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()

if __name__ == '__main__':
  node_init()
