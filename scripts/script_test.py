import rospy
import time
from std_msgs.msg import String

pub_bulb_state = ""
pub_tts_ibm = ""
pub_audio = ""

def node_init():
    
    global pub_audio, pub_bulb_state, pub_tts_ibm
    rospy.loginfo("Assinando os tópicos...")
    rospy.init_node('script_test', anonymous=True)
    pub_bulb_state = rospy.Publisher('smart_bulb_node/state', String, queue_size=10)
    time.sleep(2)
    pub_tts_ibm = rospy.Publisher('tts_ibm_node/input', String, queue_size=10)
    time.sleep(2)
    pub_audio = rospy.Publisher('audio_node/play_sound', String, queue_size=10)
    time.sleep(2)

    rospy.loginfo("Tópicos assinados!")
    time.sleep(5)
    rate = rospy.Rate(.1) # 1/3hz
    while not rospy.is_shutdown():
        pub_bulb_state.publish("off")
        time.sleep(3)
        pub_bulb_state.publish("on")
        time.sleep(3)
        pub_tts_ibm.publish("Testando o serviço da IBM")
        time.sleep(10)
        pub_audio.publish("mario-end-02")
        time.sleep(10)
        global state
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        node_init()
    except rospy.ROSInterruptException:
        pass