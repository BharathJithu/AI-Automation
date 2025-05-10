from ipaddress import ip_address

import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
from decouple import config
from datetime import datetime

from pyexpat.errors import messages

from conv import random_text
from random import choice
from online import find_my_ip, search_on_google, search_on_youtube, search_on_wikipedia, send_email

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 225)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

USER = config('USER')
HOSTNAME = config('BOT')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_me():
    hour = datetime.now().hour
    if (hour >= 5) and (hour < 12):
        speak(f"Good morning {USER}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good Afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USER}")
    speak(f"i am {HOSTNAME}. How may i assist you? {USER}")

listening = False

def start_listening():
    global listening
    listening = True
    print('started listening....')

def pause_listening():
    global listening
    listening = False
    print('stopped listening..')

keyboard.add_hotkey('ctrl+alt+k',start_listening)
keyboard.add_hotkey('ctrl+alt+p',pause_listening)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing.....")
        queri = r.recognize_google(audio,language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if (hour >=21) and (hour < 6):
                speak(f"Good night sir")
            else:
                speak(f"have a good day sir")
            exit()

    except Exception:
        speak("Sorry i couldn't understand, can you please repeat that ")
        queri = 'None'
    return  queri


if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak(("i'm absolutely fine sir, what about you"))

            elif "open command prompt" in query:
                speak("opening command prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("opening camera sir")
                sp.run('start microsoft.windows.camera:',shell=True)

            elif "open notepad" in query:
                speak("opening notepad for you sir")
                notepad_path = "C:\\Windows\\notepad.exe"
                os.startfile(notepad_path)

            elif "open Assassin's creed" in query:
                speak("opening Assassin creed for you sir")
                assassin_creed_path = "C:\\Program Files (x86)\\Assassins Creed III\\AC3SP.exe"
                os.startfile(assassin_creed_path)

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(f"your ip address is {ip_address}")
                print(f"your ip address is {ip_address}")

            elif "open youtube" in query:
                speak(f"what do yo want to play on youtube sir?")
                video = take_command().lower()
                search_on_youtube(video)

            elif "open google" in query:
                speak(f"what do yo want to search in google sir?")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak(f"what do you want to search in wikipedia sir?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia {results}")
                speak(f"iam printing in on terminal")
                print(results)

            elif "send an email" in query:
                speak(f"On what email address do you want to send sir?. Please enter in the terminal")
                receiver_add = input("Email Address:")
                speak(f"what should be the subject sir?")
                subject = take_command().capitalize()
                speak(f"what is the message")
                message = take_command().capitalize()
                if send_email(receiver_add,subject,message):
                    speak(f"i have send the email sir")
                    print(f"i have send the email sir")
                else:
                    speak(f"something went wrong please check the error")
