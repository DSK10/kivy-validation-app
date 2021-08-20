from os import path
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hover_logout.hoverable import HoverBehavior
Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, user, passw):
        with open("app/users.json") as file:
            users = json.load(file)

        if user in users and passw == users[user]['password']:
            self.manager.current = "login_screen_success"
        else:
            self.ids.fail.text = "Login Failed!"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def main_screen(self):
        self.manager.current = "login_screen"

    def add_user(self, uname, pword):
        with open("app/users.json") as file:
            users = json.load(file)
            
        users[uname] = {"username":uname, "password":pword,
             "created":datetime.now().strftime('%y-%m-%d') }

        with open("app/users.json", 'w') as file:
            json.dump(users, file)

        self.manager.current = "sign_up_success"
        

class SignUpSuccess(Screen):
    def main_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

    def enlight(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("app/qoutes/*txt")
        print(available_feelings)
        available_feelings = [Path(filename).stem for 
                                filename in available_feelings]
        if feel in available_feelings:
            with open(f"app/qoutes/{feel}.txt") as file:
                qoutes = file.readlines()
            self.ids.show.text = qoutes[random.randint(0,len(qoutes)-1)]
        else:
            self.ids.show.text = "Try another feeling"


        # if que == "happy":
        #     self.ids.show.text = "happy"
        # elif que == "sad":
        #     self.ids.show.text = "sad"

        # elif que  == "unloved":
        #     self.ids.show.text = "unloved"
        # else:
        #     self.ids.show.text = "wrong words!"



class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
