from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.config import Config
import client
import server
import message
from time import *

client = client.Client()
HOST_ADDRESS = "localhost"
PORT = 8003
aux = 1

class Login(Screen):
    # Configurando tamonha da tela de login
    Config.set('graphics', 'resizable', '0')
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '600')

    def sucess(self,loginTxt):
        app = App.get_running_app()
        app.username = loginTxt
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
        if aux < 9 :
            current_user = "User"+str(aux)
            self.ids[current_user].text = loginTxt
            self.ids[current_user].background_color = 1.0,1.0,1.0,1.0
            global aux
            aux += 1

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetScreen()

    def send(self):
        message = self.ids['message'].text
        global client
        client.send_message(['joao'], message)
        self.ids['message'].text = ""
        sleep(1)
        global client
        self.ids['log'].text = client.rcv_list[0]

class ZipZop(App):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        return manager

ZipZop().run()
