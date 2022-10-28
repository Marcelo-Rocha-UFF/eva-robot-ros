# python3.6

import rospy
from std_msgs.msg import String

import hashlib

from ibm_watson.text_to_speech_v1 import Voice
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

tts = "" # objeto do servico do Watson
pub = ""

def input_callback(data):
  # criar um tipo de mensagem que contenha:
  # o tipo de voz (timbre)
  # a string com o texto a ser falado
  rospy.loginfo("tts_ibm_node/input funcionado")
  
  # Assume the default UTF-8 (Gera o hashing do arquivo de audio)
  # Also, uses the voice tone attribute in file hashing
  
  #hash_object = hashlib.md5(texto[ind_random].encode())
  #file_name = "_audio_"  + root.find("settings")[0].attrib["tone"] + hash_object.hexdigest()

  # verifica se o audio da fala já existe na pasta
  #if not (os.path.isfile("audio_cache_files/" + file_name + ".mp3")): # se nao existe chama o watson
  # Eva tts functions
  audio_file_path = "src/beginner_tutorials/scripts/speak_audio_files_cache/"
  audio_file_name = data.data
  audio_file_type = ".mp3"
  audio_file_path_name = "src/beginner_tutorials/scripts/speak_audio_files_cache/" + data.data
  with open(audio_file_path + audio_file_name + audio_file_type, 'wb') as audio_file:
    rospy.loginfo("Aqui")
    try:
      # talvez o timbre de voz possa ser um parametro global em paramserver
      res = tts.synthesize(data.data, accept = "audio/mp3", voice = "pt-BR_IsabelaV3Voice").get_result()
      audio_file.write(res.content)
      rospy.loginfo("Arquivo de audio gerado na pasta src/beginner_tutorials/scripts/speak_audio_files_cache/")
    except:
      rospy.loginfo("Voice exception")
      #exit(1)

  rospy.loginfo("Publicando " + audio_file_name)
  pub.publish(audio_file_name) # o path e o tipo do arquivo são inseridos no node audio_node


def node_init():

  global pub
  
  pub = rospy.Publisher('audio_node/play_voice', String, queue_size=10)
  
  rospy.init_node('tts_ibm_node', anonymous=False)

  rospy.Subscriber('tts_ibm_node/input', String, input_callback)
  
  # watson config api key
  rospy.loginfo("Configurando o serviço do IBM Watson...")
	
  with open("src/beginner_tutorials/scripts/ibm_cred.txt", "r") as ibm_cred:
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
