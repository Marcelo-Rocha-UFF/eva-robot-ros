# python3.6

import rospy, rospkg
from std_msgs.msg import String

import hashlib
import os

from gtts import gTTS


# Language in which you want to convert
language = 'pt'
tld_brasil="com.br"

def input_callback(data):
  # criar um tipo de mensagem que contenha:
  # o tipo de voz (timbre)
  # a string com o texto a ser falado
  rospy.loginfo("tts_google_node/input funcionado")
  
  # Assume the default UTF-8 (Gera o hashing do arquivo de audio)
  # Also, uses the voice tone attribute in file hashing
  texto = data.data

  hash_object = hashlib.md5(texto.encode())
  rospy.loginfo("hashing: " + hash_object.hexdigest())

  # Eva tts-ibm function
  audio_speech_path = os.path.join(rospkg.RosPack().get_path("eva-robot-ros"), "scripts/speech_audio_files_cache/")
  speech_file_name = "Google-" + language + "-" + hash_object.hexdigest()
  audio_file_type = ".mp3"

  # verifica se o audio da fala já existe na pasta
  if not (os.path.isfile(audio_speech_path + speech_file_name + audio_file_type)): # se nao existe chama o watson
    rospy.loginfo("O texto não se encontra na cache e será enviado para a nuvem...")
    tts_audio = gTTS(text=texto, lang=language, tld=tld_brasil, slow=False)
    tts_audio.save(audio_speech_path + speech_file_name + audio_file_type)
    pub_audio_node_speak.publish(speech_file_name) # o path e o tipo do arquivo são inseridos no node audio_node
    rospy.loginfo("Arquivo: " + speech_file_name + audio_file_type + " , criado em " + audio_speech_path)
  else:
    rospy.loginfo("O texto já se encontra na cache e será falado imediatamente!")
    rospy.loginfo("Falando o texto: " + texto)
    pub_audio_node_speak.publish(speech_file_name) # o path e o tipo do arquivo são inseridos no node audio_node


def node_init():

  global pub_audio_node_speak

  rospy.init_node('tts_google_node', anonymous=False)
  
  pub_audio_node_speak = rospy.Publisher('audio_node/speak', String, queue_size=10)

  rospy.Subscriber('tts_google_node/input', String, input_callback)

  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()

if __name__ == '__main__':
  node_init()
