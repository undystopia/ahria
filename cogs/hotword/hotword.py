import snowboydecoder
import speech_recognition as sr


def listen_forever(text_callback):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        # listen for 5 seconds and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=5)

        print("Done.")

        detector = snowboydecoder.HotwordDetector(
            "resources/Ahria.pmdl", sensitivity=0.75)

        assistant = None

        def callback():
            detector.terminate()
            audio = r.listen(source)
            try:
                text_callback(r.recognize_sphinx(audio))
            except sr.UnknownValueError:
                print("Sphinx could not understand audio")
            except sr.RequestError as e:
                print("Sphinx error; {0}".format(e))
            detector.start(detected_callback=callback, sleep_time=0.03)

        detector.start(detected_callback=callback, sleep_time=0.03)
        # blocks?
        detector.terminate()