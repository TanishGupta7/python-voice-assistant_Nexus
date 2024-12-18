import speech_recognition as sr
import webbrowser as wb
import pyttsx3 as ttx
import os
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import PhotoImage
import random
import requests
import datetime
import difflib
import subprocess

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = ttx.init()

# Function to make the assistant speak
def speak(text):
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Function to create and display an image for specific gods
def create_god_image(god_name):
    width, height = 800, 400
    img = Image.new('RGB', (width, height), color=(255, 223, 186))
    draw = ImageDraw.Draw(img)
    for i in range(height):
        color = (255, 223 - i // 3, 186 - i // 3)
        draw.line([(0, i), (width, i)], fill=color, width=1)
    message = (
        f"🌸 Dear User, 🌸\n"
        f"You are being blessed by {god_name}.\n"
        f"May {god_name} guide your path! 🌟"
    )
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()
    text_bbox = draw.textbbox((0, 0), message, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.multiline_text((x, y), message, fill="black", font=font, align="center")
    image_path = f"{god_name}_message.png"
    img.save(image_path)
    def display_image_fullscreen():
        root = tk.Tk()
        root.title(f"{god_name} Message")
        root.attributes("-fullscreen", True)
        root.configure(bg="black")
        photo = PhotoImage(file=image_path)
        label = tk.Label(root, image=photo, bg="black")
        label.pack(expand=True)
        root.bind("<Escape>", lambda e: root.destroy())
        root.mainloop()
    display_image_fullscreen()

# difflib module for better command matching
def get_best_match(command, options):
    """
    Returns the closest match from options for the given command.
    """
    matches = difflib.get_close_matches(command, options, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Function to get current weather
def get_weather():
    try:
        api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
        city = "Your_City_Name"  # Replace with your city name
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        # Fetch weather data
        response = requests.get(url)
        data = response.json()
        
        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            speak(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
        else:
            error_message = data.get("message", "Unable to fetch weather details.")
            speak(f"Weather API error: {error_message}")
    except Exception as e:
        speak("There was an error getting the weather. Please try again later.")
        print(f"Weather error: {e}")

#Function to get the joke
def tell_joke():
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url)
        
        if response.status_code == 200:
            joke = response.json()
            setup = joke.get("setup", "")
            punchline = joke.get("punchline", "")
            speak(f"Here's a joke for you: {setup} ... {punchline}")
        else:
            speak("Unable to fetch a joke at the moment. Here's one: Why did the scarecrow win an award? He was outstanding in his field!")
    except Exception as e:
        speak("An error occurred while fetching a joke.")
        print(f"Joke API error: {e}")

# Function to process user commands
def processCommand(command):
    command = command.lower()
    
    if "open google" in command:
        speak("Opening Google.")
        print("Opening Google.")
        wb.open("https://www.google.com/")
    elif "open youtube" in command:
        speak("Opening YouTube.")
        print("Opening YouTube.")
        wb.open("https://www.youtube.com/")
    elif "open gmail" in command:
        speak("Opening Gmail.")
        print("Opening Gmail.")
        wb.open("https://mail.google.com/")
    elif "open github" in command:
        speak("Opening GitHub.")
        print("Opening GitHub.")
        wb.open("https://github.com/")
    elif "open linkedin" in command:
        speak("Opening LinkedIn.")
        print("Opening LinkedIn.")
        wb.open("https://linkedin.com/")
    elif "open bluetooth" in command:
        speak("Opening Bluetooth settings.")
        print("Opening Bluetooth settings.")
        os.system("start ms-settings:bluetooth")
    elif "open wi-fi" in command:
        speak("Opening wi-fi settings.")
        print("Opening wi-fi settings.")
        os.system("start ms-settings:network-wi-fi")
    elif "airplane mode" in command:
        speak("Opening Airplane mode settings.")
        print("Opening Airplane mode settings.")
        os.system("start ms-settings:network-airplanemode")
    elif "open chrome" in command:
        speak("Opening Google Chrome.")
        print("Opening Google Chrome.")
        subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif "open microsoft edge" in command:
        speak("Opening Microsoft Edge.")
        print("Opening Microsoft Edge.")
        subprocess.Popen("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe")
    elif "open vs code" in command or "open visual studio code" in command:
        speak("Opening Visual Studio Code.")
        print("Opening Visual Studio Code.")
        subprocess.Popen("C:\\Users\\<username>\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
    elif "turn on bluetooth" in command:
        speak("Enabling Bluetooth.")
        print("Enabling Bluetooth.")
        os.system("powershell -Command \"Start-Service bthserv\"")
    elif "turn off bluetooth" in command:
        speak("Disabling Bluetooth.")
        print("Disabling Bluetooth.")
        os.system("powershell -Command \"Stop-Service bthserv\"")
    elif "turn on wi-fi" in command:
        speak("Enabling wi-fi.")
        print("Enabling wi-fi.")
        os.system("powershell -Command \"(Get-NetAdapter -Name 'Wi-Fi').Enable()\"")
    elif "turn off wi-fi" in command:
        speak("Disabling wi-fi.")
        print("Disabling wi-fi.")
        os.system("powershell -Command \"(Get-NetAdapter -Name 'Wi-Fi').Disable()\"")
    elif "play music" in command:
        speak("Playing some music for you.")
        print("Playing some music for you.")
        os.system("start wmplayer")
    elif "shutdown" in command:
        speak("Shutting down the system. Goodbye!")
        print("Shutting down the system. Goodbye!")
        os.system("shutdown /s /t 1")
    elif "weather" in command:
        speak("Fetching the current weather.")
        print("Fetching the current weather.")
        get_weather()
    elif "joke" in command:
        tell_joke()
    elif any(god in command for god in ["shiv", "mata", "balaji", "shyam baba", "krishna"]):
        god_name = next(god.capitalize() for god in ["shiv", "mata", "balaji", "shyam baba", "krishna"] if god in command)
        speak(f"Taking you to the darbaar of {god_name}.")
        create_god_image(god_name)
    elif "inspire me" in command or "motivation" in command:
        response = requests.get("https://api.quotable.io/random", verify=False)
        if response.status_code == 200:
            quote = response.json().get("content", "Keep going, you're doing great!")
            speak(f"Here is your motivational quote: {quote}")
        else:
            speak("Unable to fetch a quote at the moment.")
    elif "exit" in command or "stop" in command:
        speak("Goodbye. Have a great day!")
        exit()
    else:
        speak("Sorry, I did not understand that command.")

    
# Main function
def main():
    assistant_name = "Nexus"
    speak(f"Initializing {assistant_name}. Say '{assistant_name}' to begin.")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print(f"Listening for the activation word '{assistant_name}'...")
                audio = recognizer.listen(source, timeout=5)
                activation_word = recognizer.recognize_google(audio).lower()
                print(f"Heard: {activation_word}")
                if assistant_name.lower() in activation_word:
                    speak("Yes, how can I assist you?")
                    while True:
                        try:
                            with sr.Microphone() as source:
                                recognizer.adjust_for_ambient_noise(source)
                                command_audio = recognizer.listen(source, timeout=5)
                                command = recognizer.recognize_google(command_audio)
                                print(command)
                                processCommand(command)
                        except sr.UnknownValueError:
                            speak("Sorry, I did not understand. Please repeat.")
                        except sr.WaitTimeoutError:
                            print("Listening timed out. Waiting for a command...")
                        except Exception as e:
                            speak("An error occurred.")
                            print(f"Error: {e}")
        except sr.WaitTimeoutError:
            print("No input detected. Listening again...")
        except Exception as e:
            speak("An error occurred.")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
