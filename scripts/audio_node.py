# python3.6

from playsound import playsound
import rospy
from std_msgs.msg import String


def play_voice_callback(data):

  # preciso detectar o tipo de audio (audio em geral ou fala na pasta de tts)
  # preciso definir uma mensagem com:
  # tipo (audio ou fala)
  # nome do arquivo sem a extensão
  # parametro block (true ou false)
  audio_voice_path = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/speak_audio_files_cache/"
  audio_file = audio_voice_path + data.data + ".mp3"
  #rospy.loginfo(rospy.get_caller_id() + ' playing speak file: %s', audio_file)
  playsound(audio_file, block = True)
  
def play_sound_callback(data):

  # preciso detectar o tipo de audio (audio em geral ou fala na pasta de tts)
  # preciso definir uma mensagem com:
  # tipo (audio ou fala)
  # nome do arquivo sem a extensão
  # parametro block (true ou false)
  audio_file_path = "/home/pi/catkin_ws/src/eva-robot-ros/scripts/audio_files/"
  audio_file = audio_file_path + data.data + ".wav"
  #rospy.loginfo(rospy.get_caller_id() + ' playing audio file: %s', audio_file)
  playsound(audio_file, block = True)
 
  

def node_init():

  rospy.init_node('audio_node', anonymous=False)

  rospy.Subscriber('audio_node/play_voice', String, play_voice_callback)
  rospy.Subscriber('audio_node/play_sound', String, play_sound_callback)

  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()
  

if __name__ == '__main__':
  node_init()
