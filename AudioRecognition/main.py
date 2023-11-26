import speech_recognition as sr

# create a recognizer instance
recognizer: sr.Recognizer = sr.Recognizer()

# use the microphone as the audio source
with sr.Microphone() as source:
    while True:
        print("Say something!")
        audio = recognizer.listen(source, phrase_time_limit=5)
        print("Got it! Now to recognize it...")

        # recognize speech using Google Speech Recognition
        try:
            print("You said: " +
                  recognizer.recognize_google(audio, language='en-US'))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}"
                .format(e))
