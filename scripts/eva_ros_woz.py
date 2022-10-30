import rospy
from std_msgs.msg import String
import threading

import time
from tkinter import *
from tkinter import messagebox
import tkinter
from  tkinter import ttk # usando tabelas
def gui_init():
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()

    # Create the Tkinter window
    window = Tk()
    window.title("EVA [ROS Version] - WoZ controller - UFF/MidiaCom")
    w = 600
    h = 280  # on linux use
    window.geometry(str(w) + "x" + str(h))

    # fonte tamanho 9 para botoes e textos em geral
    font1 = ('Arial', 9)

    #setting the default font for applicantion
    window.option_add( "*font", "Arial 9")
    #
    def eva_emotion_ctrl(emotion):
        print(emotion)
        pub_eyes_display_node_emotion.publish(emotion)

    def smartbulb_ctrl(color):
        print(color)
        if color == "off":
            pub_smart_bulb_node_state.publish("off")
        else:
            pub_smart_bulb_node_color_name.publish(color)
            pub_smart_bulb_node_state.publish("on")
            

    def tts_speak_ctrl(text_to_speak):
        print(text_to_speak.get())
        pub_tts_ibm_node_input.publish(text_to_speak.get())

    def play_sound(file_name):
        print(file_name)
        pub_audio_node_play.publish(file_name)

    # define o frame para a imagem do robô
    bt_padx = 5
    bt_pady = 10
    lf_expressions = ttk.Labelframe(window, text="Expressões do olhar")
    lf_expressions.grid(sticky="w", row=0, column=0, padx=10, pady=10)
    bt_exp_neutral = Button (lf_expressions, text = "Neutral", font = font1, command=lambda: eva_emotion_ctrl("neutral"))
    bt_exp_neutral.pack(side=tkinter.LEFT, padx=bt_padx, pady=bt_pady)
    bt_exp_happy = Button (lf_expressions, text = "Happy", font = font1, command=lambda: eva_emotion_ctrl("happy"))
    bt_exp_happy.pack(side=tkinter.LEFT, padx=bt_padx, pady=bt_pady)
    bt_exp_sad = Button (lf_expressions, text = "Sad", font = font1, command=lambda: eva_emotion_ctrl("sad"))
    bt_exp_sad.pack(side=tkinter.LEFT, padx=bt_padx, pady=bt_pady)
    bt_exp_angry = Button (lf_expressions, text = "Angry", font = font1, command=lambda: eva_emotion_ctrl("angry"))
    bt_exp_angry.pack(side=tkinter.LEFT, padx=bt_padx, pady=bt_pady)

    lf_smartbulb = ttk.Labelframe(window, text="Efeitos sensoriais de luz")
    lf_smartbulb.grid(row=1, column=0, padx=10, pady=10)
    bt_sb_off= Button (lf_smartbulb, text = "Off", font = font1, command=lambda: smartbulb_ctrl("off"))
    bt_sb_off.pack(side=tkinter.LEFT, padx=bt_padx, pady=bt_pady)
    bt_sb_white= Button (lf_smartbulb, text = "White", font = font1, command=lambda: smartbulb_ctrl("white"))
    bt_sb_white.pack(side=tkinter.LEFT, padx=bt_padx, pady=bt_pady)
    bt_sb_yellow= Button (lf_smartbulb, text = "Yellow", font = font1, command=lambda: smartbulb_ctrl("yellow"))
    bt_sb_yellow.pack(side=tkinter.LEFT, padx=bt_padx, pady=bt_pady)
    bt_sb_green= Button (lf_smartbulb, text = "Green", font = font1, command=lambda: smartbulb_ctrl("green"))
    bt_sb_green.pack(side=tkinter.LEFT, padx=bt_padx, pady=bt_pady)
    bt_sb_red= Button (lf_smartbulb, text = "Red", font = font1, command=lambda: smartbulb_ctrl("red"))
    bt_sb_red.pack(side=tkinter.LEFT, padx=bt_padx, pady=bt_pady)
    bt_sb_blue= Button (lf_smartbulb, text = "Blue", font = font1, command=lambda: smartbulb_ctrl("blue"))
    bt_sb_blue.pack(side=tkinter.LEFT, padx=bt_padx, pady=bt_pady)

    lf_tts = ttk.Labelframe(window, text="IBM-Watson Text To Speech (TTS) service")
    lf_tts.grid(row=2, column=0, padx=10, pady=10)
    tts_text_var = StringVar()
    bt_tts_send= Button (lf_tts, text = "Falar texto", font = font1, command=lambda: tts_speak_ctrl(tts_text_var))
    bt_tts_send.grid(row=0, column=0, padx=bt_padx, pady=bt_pady)
    text_to_speech=Entry(lf_tts, width=40, textvariable=tts_text_var)
    text_to_speech.grid(row=0, column=1, padx=bt_padx, pady=bt_pady)

    lf_audio_play = ttk.Labelframe(window, text="Tocar sons e músicas")
    lf_audio_play.grid(row=0, column=1, rowspan=3, pady=10, padx=5)
    Lb1 = Listbox(lf_audio_play)
    bt_play= Button (lf_audio_play, text = "    Play sound    ", font = font1, command=lambda: play_sound(Lb1.get(Lb1.curselection())))
    bt_play.grid(row=0, column=0, padx=bt_padx, pady=bt_pady)
    Lb1 = Listbox(lf_audio_play)
    Lb1.insert(1, "mario-end-01")
    Lb1.insert(2, "mario-start-01")
    Lb1.insert(3, "song-take-on-me")
    Lb1.insert(4, "song-weird-science")
    Lb1.insert(5, "thriller3")
    Lb1.insert(6, "thriller1")
    Lb1.insert(7, "song-vivaldi-spring")
    Lb1.insert(8, "song-the-imperial-march")
    Lb1.insert(9, "song-exodus")
    Lb1.grid(row=1, column=0, padx=bt_padx, pady=bt_pady)

    # define the closing app function
    window.protocol("WM_DELETE_WINDOW", on_closing)

    # does not show the min button
    window.resizable(0,0)

    window.mainloop() # thread da gui python

def node_init():
  rospy.init_node('eva_ros_woz_node', anonymous=False)

  global pub_smart_bulb_node_state, pub_smart_bulb_node_color_name, pub_smart_bulb_node_color_rgb
  # smart bulb
  pub_smart_bulb_node_state = rospy.Publisher('smart_bulb_node/state', String, queue_size=10)
  pub_smart_bulb_node_color_name = rospy.Publisher('smart_bulb_node/color_name', String, queue_size=10)
  pub_smart_bulb_node_color_rgb = rospy.Publisher('smart_bulb_node/color_rgb', String, queue_size=10)

  global pub_eyes_display_node_emotion
  # eyes display
  pub_eyes_display_node_emotion = rospy.Publisher('eyes_display_node/emotion', String, queue_size=10)

  global pub_tts_ibm_node_input
  # tts-IBM
  pub_tts_ibm_node_input = rospy.Publisher('tts_ibm_node/input', String, queue_size=10)

  global pub_audio_node_speak, pub_audio_node_play
  # audio control
  pub_audio_node_speak = rospy.Publisher('audio_node/speak', String, queue_size=10)
  pub_audio_node_play = rospy.Publisher('audio_node/play', String, queue_size=10)
  # spin() simply keeps python from exiting until this node is stopped

  threading.Thread(target=gui_init().start())


  rospy.spin()

if __name__ == '__main__':
  node_init()




