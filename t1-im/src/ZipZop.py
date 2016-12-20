from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.config import Config
from kivy.clock import Clock
from functools import partial
from time import *
import client
import os

client = client.Client()
HOST_ADDRESS = "localhost"
PORT = 8003
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
        Clock.schedule_interval(self.rcv_msg,0.5)
        Clock.schedule_interval(self.update_text, 0.4)

    def update_text(self, dt):
        global receiver
        if receiver != '':
            filename = os.getcwd() + "/logs/" + username + ";" + receiver
            log = open(filename, 'r')
            text = log.read()
            self.ids['log'].text = text


    def rcv_msg(self, dt):
        aux = 1
        while aux < 9:
            current_user = "User" + str(aux)
            self.ids[current_user].text = ""
            self.ids[current_user].background_color = 0.0, 0.0, 0.0, 0.0
            aux += 1
        aux = 1
        for j in client.user_list:
            if j != "" and j != username:
                current_user = "User" + str(aux)
                self.ids[current_user].text = j
                if j == receiver:
                    self.ids[current_user].background_color = 1.0, 1.0, 1.0, 1.0
                aux += 1

        global client
        if len(client.rcv_list):
            while len(client.rcv_list):
                i = client.rcv_list[0]
                i += "\n"
                dir_path = os.getcwd()
                global username
                filename = dir_path + "/logs/" + username + ";"
                target = i[1]
                counter = 2
                while i[counter] != "]":
                    target += i[counter]
                    counter += 1
                filename += target
                log = open(filename,'a')
                log.write(i)
                log.close()
                client.rcv_list.pop(0)

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetScreen()

    def send(self):
        global username
        message = self.ids['message'].text
        log_message = "[" + username + "]" + message + "\n"
        global receiver
        global client
        client.send_message([receiver], message)
        self.ids['message'].text = ""
        #sleep(1)
        #TODO: Windows version
        dir_path = os.getcwd() + "/logs/"
        filename = dir_path+username+";"+receiver
        log = open(filename,'a')
        log.write(log_message)
        log.close()
        global client
        #self.ids['log'].text = client.rcv_list[0][1]

    def button_pressed(self, label):
        if self.ids[label].text:
            global receiver
            receiver = self.ids[label].text

class ZipZop(App):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        return manager

ZipZop().run()
