# python3.6

import rospy, rospkg
from std_msgs.msg import String

import hashlib
import os

from ibm_watson.text_to_speech_v1 import Voice
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

tts = "" # objeto do servico do Watson
pub_audio_node_speak = ""

def input_callback(data):
  # criar um tipo de mensagem que contenha:
  # o tipo de voz (timbre)
  # a string com o texto a ser falado
  rospy.loginfo("tts_ibm_node/input funcionado")
  
  # Assume the default UTF-8 (Gera o hashing do arquivo de audio)
  # Also, uses the voice tone attribute in file hashing
  texto = data.data
  timbre_da_voz = "pt-BR_IsabelaV3Voice" # depois precisa ser definido externamente
  hash_object = hashlib.md5(texto.encode())
  rospy.loginfo("hashing: " + hash_object.hexdigest())

  # Eva tts-ibm function
  audio_speech_path = os.path.join(rospkg.RosPack().get_path("eva-robot-ros"), "scripts/speech_audio_files_cache/")
  speech_file_name = "IBM-"  + timbre_da_voz + "-" + hash_object.hexdigest()
  audio_file_type = ".mp3"

  # verifica se o audio da fala já existe na pasta
  if not (os.path.isfile(audio_speech_path + speech_file_name + audio_file_type)): # se nao existe chama o watson
    rospy.loginfo("O texto não se encontra na cache e será enviado para a nuvem...")
    with open(audio_speech_path + speech_file_name + audio_file_type, 'wb') as audio_file:
      try:
        # talvez o timbre de voz possa ser um parametro global em paramserver
        res = tts.synthesize(data.data, accept = "audio/mp3", voice = timbre_da_voz).get_result()
        audio_file.write(res.content)
        pub_audio_node_speak.publish(speech_file_name) # o path e o tipo do arquivo são inseridos no node audio_node
        rospy.loginfo("Arquivo: " + speech_file_name + audio_file_type + " , criado em " + audio_speech_path)
      except:
        rospy.loginfo("Voice exception")
        exit(1)
  else:
    rospy.loginfo("O texto já se encontra na cache e será falado imediatamente!")
    rospy.loginfo("Falando o texto: " + texto)
    pub_audio_node_speak.publish(speech_file_name) # o path e o tipo do arquivo são inseridos no node audio_node


def node_init():

  global pub_audio_node_speak

  rospy.init_node('tts_ibm_node', anonymous=False)
  
  pub_audio_node_speak = rospy.Publisher('audio_node/speak', String, queue_size=10)

  rospy.Subscriber('tts_ibm_node/input', String, input_callback)
  
  # watson config api key
  rospy.loginfo("Configurando o serviço do IBM Watson...")
	
  ibm_credentials_path = os.path.join(rospkg.RosPack().get_path("eva-robot-ros"), "scripts/ibm_cred.txt")
  with open(ibm_credentials_path, "r") as ibm_cred:
    ibm_config = ibm_cred.read().splitlines()
  
  apikey = ibm_config[0]
  url = ibm_config[1]
  
  # setup watson service
  authenticator = IAMAuthenticator(apikey)
  
  global tts # para poder ser acessada dentro da funcao callback
  # tts service
  tts = TextToSpeechV1(authenticator = authenticator)
  tts.set_service_url(url)
  rospy.loginfo("Serviço do Watson funcionando!")

  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()

if __name__ == '__main__':
  node_init()
