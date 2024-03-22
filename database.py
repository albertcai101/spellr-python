import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime

# Initialize Firebase Admin
cred = credentials.Certificate('spellr-60636-firebase-adminsdk-drjkq-bde7cd0f27.json')
firebase_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://spellr-60636-default-rtdb.firebaseio.com/',
    'storageBucket': 'gs://spellr-60636.appspot.com'  # Found in your Firebase Console under Storage section
})

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

# Replace this with your actual recognition and file handling logic
def main():
    # Example filename and text
    filename = "recording.wav"
    recognized_text = "Hello, world!"
    
    # Upload the example data to Firebase
    upload_to_firebase(filename, recognized_text)

if __name__ == "__main__":
    main()