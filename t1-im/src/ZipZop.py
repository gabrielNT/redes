from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.config import Config

class Login(Screen):
    # Configurando tamonha da tela de login
    Config.set('graphics', 'resizable', '0')
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '600')

    def sucess(self,loginTxt):
        app = App.get_running_app()

        app.username = loginTxt

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

        app.config.read(app.get_application_config())
        app.config.write()

    def resetScreen(self):
        self.ids['login'].text = ""

class Connected(Screen):

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetScreen()

    def send(self):
        message = self.ids['message'].text
        self.ids['message'].text = ""

class ZipZop(App):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        return manager

ZipZop().run()
