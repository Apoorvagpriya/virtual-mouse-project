import speech_recognition as sr
import pyttsx3
import os
import datetime
recognizer = sr.Recognizer()
engine = pyttsx3.init()
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Sorry, speech service is down.")
            return ""
def open_app(command):
    try:
        if "chrome" in command:
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            speak("Opening Chrome")
        elif "excel" in command:
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
            speak("Opening Excel")
        elif "paint" in command:
            os.startfile("mspaint")
            speak("Opening Paint")
        elif "word" in command:
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
            speak("Opening Word")
        elif "spotify" in command:
            os.startfile("C:\\Users\\yuvas\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe")
            speak("Opening Spotify")
        elif "file" in command or "explorer" in command:
            os.startfile("explorer")
            speak("Opening File Explorer")
        elif "time" in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time}")
        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            exit()
        else:
            speak("Sorry, I don't know that command.")
    except Exception as e:
        speak("Failed to open the application.")
speak("Voice Assistant Started. Say 'hello' to begin.")

while True:
    cmd = listen()
    if "hello" in cmd:
        speak("Hi! How can I help you?")
        while True:
            command = listen()
            open_app(command)
