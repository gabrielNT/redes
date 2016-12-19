from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.config import Config
import client
import kivy.clock
from time import *
import os
client = client.Client()
HOST_ADDRESS = "localhost"
PORT = 8003
aux = 1
username = ""
receiver = ""

class Login(Screen):
    # Configuring login screen size
    Config.set('graphics', 'resizable', '0')
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '600')

    def sucess(self,loginTxt):
        app = App.get_running_app()
        app.username = loginTxt
        global username
        username = loginTxt
        global client
        client.start(HOST_ADDRESS, PORT, loginTxt)

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'
        self.manager.current_screen.newConnection(loginTxt)

        app.config.read(app.get_application_config())
        app.config.write()

    def resetScreen(self):
        self.ids['login'].text = ""

class Connected(Screen):
    global aux
    def newConnection(self,loginTxt):
        clock.schedule_interval(rcv_msg,0.5)
        if aux < 9 :
            current_user = "User"+str(aux)
            self.ids[current_user].text = loginTxt
            self.ids[current_user].background_color = 1.0,1.0,1.0,1.0
            global aux
            aux += 1

    def rcv_msg(self):
        global client
        if len(client.recv_list):
            for i in client.recv_list:
                i += "\n"
                dir_path = os.getcwd()
                global username
                filename = dir_path+username+";"
                target = i[1]
                counter = 2
                while i[counter] != "]":
                    target += i[counter]
                    counter += 1
                filename += target
                log = open(filename,'a')
                log.write(i)
                log.close()
                #  printa na tela

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetScreen()

    def send(self):
        message = self.ids['message'].text
        global receiver
        receiver
        global client
        client.send_message([receiver], message)
        self.ids['message'].text = ""
        sleep(1)
        dir_path = os.getcwd()
        filename = dir_path+username+";"+receiver
        log = open(filename,'a')
        message += "\n"
        log.write(message)
        log.close()
        global client
        #self.ids['log'].text = client.rcv_list[0][1]

class ZipZop(App):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        return manager

ZipZop().run()
