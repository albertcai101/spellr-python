import serial
import threading
import pyaudio
import wave
import speech_recognition as sr
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime

# Setup serial connection - adjust this to your Arduino's serial port
# need to forget the device to properly connect
ser = serial.Serial('/dev/tty.usbmodem145460101', 9600, timeout=1)
# ser = serial.Serial('/dev/tty.HC-05', 9600, timeout=1)

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
audio_interface = pyaudio.PyAudio()
audio_frames = []
recording = False

# Initialize Firebase Admin
cred = credentials.Certificate('spellr-60636-firebase-adminsdk-drjkq-bde7cd0f27.json')
firebase_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://spellr-60636-default-rtdb.firebaseio.com/',
    'storageBucket': 'gs://spellr-60636.appspot.com'  # Found in your Firebase Console under Storage section
})

def record_audio():
    """Function to handle audio recording in a separate thread."""
    global recording
    stream = audio_interface.open(format=FORMAT, channels=CHANNELS,
                                  rate=RATE, input=True,
                                  frames_per_buffer=CHUNK)
    print("Recording started...")
    while recording:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_frames.append(data)
    stream.stop_stream()
    stream.close()
    print("Recording stopped.")

def save_audio(filename="recording.wav"):
    """Function to save the recorded audio to a file."""
    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio_interface.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(audio_frames))
    wave_file.close()

def recognize_speech_from_audio(filename="recording.wav"):
    """Function to recognize speech from the recorded audio file."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        print("Recognizing speech...")
        try:
            text = recognizer.recognize_google(audio_data)
            print("Recognized text:", text)
            response = f"RES: {text.upper()}\n"  # Ensure to include newline character to signify end of message
            ser.write(response.encode('utf-8'))  # Encode the string to bytes
            upload_to_firebase(filename, text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

def listen_for_commands():
    """Main function to listen for serial commands and manage recording."""
    global recording, audio_frames
    while True:
        if ser.in_waiting > 0:
            command = ser.readline().decode('utf-8').strip()
            if command == "GO" and not recording:
                audio_frames = []  # Clear previous recording
                recording = True
                threading.Thread(target=record_audio).start()
            elif command == "STOP" and recording:
                recording = False
                save_audio()
                recognize_speech_from_audio()

def upload_to_firebase(filename, text):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Create a reference to the database
    ref = db.reference('recordings')
    
    # Generate a unique key for the new recording entry
    new_recording_ref = ref.push()
    
    # Set the data for the new recording
    new_recording_ref.set({
        'filename': filename,
        'text': text,
        'timestamp': timestamp,
    })

if __name__ == "__main__":
    try:
        listen_for_commands()
    finally:
        ser.close()
        audio_interface.terminate()
