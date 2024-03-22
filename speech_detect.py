import speech_recognition as sr
import threading

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.active_listening = False  # Tracks if we're currently listening
        self.recognized_speech = []  # List to store recognized speech

    def start_listening(self):
        if self.active_listening:
            print("Already listening")
            return

        self.recognized_speech.clear()  # Clear previous session data

        def listen():
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("You can start speaking now!")
                while self.active_listening:
                    try:
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        self.process_speech(audio)
                    except sr.WaitTimeoutError:
                        pass  # Timeout reached without user speech, loop back to continue listening

        self.active_listening = True
        threading.Thread(target=listen).start()

    def stop_listening(self):
        if not self.active_listening:
            print("Not currently listening")
            return
        
        self.active_listening = False
        print("Stopping speech recognition...")

        # Once stopped, print everything that was recognized
        print("Everything recognized between 'go' and 'stop':")
        for speech in self.recognized_speech:
            print(speech)

    def process_speech(self, audio):
        try:
            speech_text = self.recognizer.recognize_google(audio)
            self.recognized_speech.append(speech_text)  # Add recognized speech to the list
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")  # Catch-all for any other exceptions

def main():
    speech_recognizer = SpeechRecognizer()
    
    while True:
        command = input("Type 'go' to start recognition or 'stop' to stop it: ").strip().lower()
        
        if command == "go":
            speech_recognizer.start_listening()
        elif command == "stop":
            speech_recognizer.stop_listening()
        else:
            print("Invalid command. Type 'go' to start or 'stop' to stop.")

if __name__ == "__main__":
    main()

# now instead of the microphone as the source, I want the source to analog readings be sent by com port of a microphone