import speech_recognition as sr

def listen_and_save(filename="output.txt"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Adjusting for background noise... Please wait.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Listening... Speak now.")
    text_data = ""

    with mic as source:
        try:
            # Listen until a 5 second pause is detected
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
            speech_text = recognizer.recognize_google(audio)
            print(f"You said: {speech_text}")
            text_data += speech_text + " "
        except sr.WaitTimeoutError:
            print("No speech detected.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError:
            print("Speech recognition service error.")

    # Save to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text_data.strip())
    print(f"Saved to {filename}")

if __name__ == "__main__":
    listen_and_save()
