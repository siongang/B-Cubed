import pyttsx3


# import speech_recognition as sr

# rec = sr.Recognizer()


# with sr.Microphone() as mic:
#     print('you can start talking now')
#     audio = rec.listen(mic,timeout=1)
#     print('Time is over')

# try:
#     print('Text:' + rec.recognize_google(audio,key='AIzaSyDJPjSk1d4yixAf-yosxQYYnXCSFjBAfy0'))
# except:
#     print('It just exploded!')



def tts(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


