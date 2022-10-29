# python3.6

from playsound import playsound
import os, rospkg

import rospy
from std_msgs.msg import String


def speak_callback(data):

  # preciso detectar o tipo de audio (audio em geral ou fala na pasta de tts)
  # preciso definir uma mensagem com:
  # tipo (audio ou fala)
  # nome do arquivo sem a extensão
  # parametro block (true ou false)
  
  audio_speech_path = os.path.join(rospkg.RosPack().get_path("eva-robot-ros"), "scripts/speech_audio_files_cache/")
  speech_file_name = data.data
  audio_file_type = ".mp3"
  playsound(audio_speech_path + speech_file_name + audio_file_type, block = True)
  
def play_callback(data):
  # preciso definir uma mensagem com:
  # nome do arquivo sem a extensão
  # parametro block (true ou false)
  audio_file_path = os.path.join(rospkg.RosPack().get_path("eva-robot-ros"), "scripts/audio_files/")
  audio_file_name = data.data
  audio_file_type = ".wav"
  playsound(audio_file_path + audio_file_name + audio_file_type, block = True)
 
  

def node_init():

  rospy.init_node('audio_node', anonymous=False)

  rospy.Subscriber('audio_node/play', String, play_callback)
  rospy.Subscriber('audio_node/speak', String, speak_callback)

  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()
  

if __name__ == '__main__':
  node_init()
