import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from googlesearch import search
import sys, time, random
import souptest
import python_weather

typing_speed = 50  # wpm
client = python_weather.Client(format=python_weather.IMPERIAL)


async def fetch_weather():
    weather = await client.find("Tel Aviv")
    return weather.current.temperature


def slow_type(t):
    for letter in t:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(random.random() * 10.0 / typing_speed)
    print('')


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command(message_to_user="i am listening"):
    command = ""
    try:
        with sr.Microphone() as source:
            print(message_to_user)
            talk(message_to_user)
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
    except:
        talk("I couldn't catch that. Please repeat.")
    return command


def run_alexa():
    cmd = take_command()
    words = cmd.split(" ")
    command, parameters = words[0], words[1:]
    joined_parameters = " ".join(parameters)
    if command == "search":
        talk("These are the top 10 results from google")
        links = search(joined_parameters, 10, "en")
        for link in links:
            print(link)
    elif cmd.startswith("who is"):
        cmd.replace("who is", "")
        summary = wikipedia.summary(cmd, sentences=10)
        sentences = summary.split(".")
        talk(sentences[0])
        talk(sentences[1])
        answer = take_command(f"Do you want to hear more about {cmd} ?")
        if answer == "yes":
            for sentence in sentences:
                print(sentence)
                talk(sentence)

    elif command == "create":
        if "text file" in joined_parameters:
            name = take_command("Specify the text file's name:")
            content = take_command("Enter content to be written to the file.")
            with open(f"{name}.txt", "w") as new_file:
                new_file.write(content)
    elif command == "calculate":
        solution = eval(joined_parameters)
        print(solution)
        talk(solution)
    elif command == 'solve':
        pass
        # Not Implemented Yet
    elif cmd.startswith("what is"):
        print("got here !")
        cmd = cmd.replace("what is", "").strip()
        if cmd.startswith("a"):
            pass
        elif cmd.startswith("the"):
            if parameters[len(parameters) - 1] == "weather":
                talk(fetch_weather())


def main():
    """ the main function """
    talk("Welcome")
    running = True
    while running:
        run_alexa()


if __name__ == '__main__':
    main()
