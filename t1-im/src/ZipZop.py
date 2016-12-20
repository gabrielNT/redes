from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.config import Config
from kivy.clock import Clock
from functools import partial
from time import *
import sys
import client
import os

client = client.Client()
HOST_ADDRESS = "104.196.39.110"
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
    notification_list = []

    def newConnection(self,loginTxt):
        Clock.schedule_interval(self.rcv_msg,0.5)
        Clock.schedule_interval(self.update_text, 0.4)

    def update_text(self, dt):
        global receiver
        try:
            if receiver != '':
                if sys.platform.startswith('win32'):
                    filename = os.path.dirname(os.path.realpath(__file__)) + "\\logs\\" + username + ";" + receiver
                elif sys.platform.startswith('linux'):
                    filename = dir_path + "/logs/" + username + ";" + receiver
                log = open(filename, 'r')
                text = log.read()
                self.ids['log'].text = ""
                self.ids['log'].text = text
        except:
            self.ids['log'].text = "Envie sua mensagem!"


    def rcv_msg(self, dt):
        aux = 1
        while aux < 9:
            current_user = "User" + str(aux)
            self.ids[current_user].text = ""
            self.ids[current_user].background_color = 0.0, 0.0, 0.0, 0.0
            aux += 1
        aux = 1
        for j in client.user_list:
            counter = 0
            if j != "" and j != username:
                current_user = "User" + str(aux)
                self.ids[current_user].text = j
                while len(self.notification_list) > counter:
                    if j == self.notification_list[counter]:
                        self.ids[current_user].background_color = 1.0, 0.0, 0.0, 1.0
                    counter += 1

                if j == receiver:
                    try:
                        self.notification_list.remove(j)
                    except:
                        pass
                    self.ids[current_user].background_color = 1.0, 1.0, 1.0, 1.0
                aux += 1

        global client
        if len(client.rcv_list):
            while len(client.rcv_list):
                i = client.rcv_list[0]
                i += "\n"
                dir_path = os.getcwd()
                global username
                if sys.platform.startswith('win32'):
                    filename = os.path.dirname(os.path.realpath(__file__)) + "\\logs\\" + username + ";"
                elif sys.platform.startswith('linux'):
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
                global receiver
                if target != receiver and target not in self.notification_list:
                    self.notification_list.append(target)
                    print target + str(len(self.notification_list))
                client.rcv_list.pop(0)

    def disconnect(self):
        sys.exit()

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
        if sys.platform.startswith('win32'):
            dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\logs\\"
        elif sys.platform.startswith('linux'):
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
