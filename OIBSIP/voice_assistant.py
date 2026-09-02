import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("you said:",text)
        return text
    except sr.UnknownValueError:
        print("sorry,I did't understand")
    except sr.RequestError as e:
        print("Sorry,there was an error in retrieving the audio:",str(e))
    return ""
def speak(text):
    engine.say(text)
    engine.runAndWait()
    print("Assistant said:",text)

speak("Hello! How may i help you?")

while True:
    command = listen()
    if "hello" in command.lower():
        speak("Hello! How may i help you?")
    elif "what's your name" in command.lower():
        speak("My name is Voice Assistant.")
    elif "what is ai" in command.lower():
        speak("AI is Artificial Information.")
    elif "time" in command.lower():
        current_time = datetime.datetime.now().strftime("%I : %M %p")
        speak("The current time is"+current_time)
    elif "date" in command.lower():
        current_date = datetime.datetime.now().strftime("%d: %B %Y")
        speak("Today's date is:"+current_date)
    elif "search" in command.lower():
        speak("what do you want to search for?")
        query = listen()
        if query:
            speak("Searching for:"+query)
            webbrowser.open("https://www.google.com/search?q="+query.replace(" ","+"))
    elif "stop" in command.lower():
        speak("Goodbye!")
        break     
    else:
        speak("Sorry, I don't Know how to respond.")