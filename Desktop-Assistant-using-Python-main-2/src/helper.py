import speech_recognition as sr
import google.generativeai as genai
import os
from gtts import gTTS

# Set the API key as an environment variable
GOOGLE_API_KEY = "AIzaSyDESru5KRYmOtwrJ-APxeM8ln34kJJ9pIo"
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Configure the Google Generative AI (Gemini)
genai.configure(api_key=GOOGLE_API_KEY)

def voice_input():
    """Capture voice input and convert it to text using Google Speech Recognition."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        # Use Google Speech Recognition to convert audio to text
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    return None

# Function to recognize user's voice input
# Function to recognize user's voice input
def takeCommand():
    """Listen to voice input and return recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")  # Debugging message
        r.pause_threshold = 1.0  # Allow slightly longer pauses
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            speak("Listening timed out. Please say that again.")
            return "None"

    try:
        print("Recognizing...")  # Debugging message
        query = r.recognize_google(audio, language='en-in')  # Use Indian English
        print(f"User said: {query}\n")  # Print recognized query for debugging
        
        # Shorten long inputs or split
        if len(query.split()) > 100:  # If the sentence is too long, we limit it
            speak("Sorry, I couldn't process that. Please try a shorter command.")
            return "None"

        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand. Could you repeat that?")
        return "None"
    except sr.RequestError:
        speak("Network issue. Please check your internet connection.")
        return "None"
    except Exception as e:
        print(f"Error recognizing speech: {e}")
        speak("An error occurred. Please try again.")
        return "None"

def text_to_speech(text):
    """Convert the given text to speech and save it as an MP3 file."""
    if not text or not text.strip():
        print("No text to convert to speech.")
        return None
    # Create a gTTS object for text-to-speech
    tts = gTTS(text=text, lang='en')
    audio_file = "speech.mp3"
    tts.save(audio_file)
    print(f"Speech saved as {audio_file}")
    return audio_file
def llm_model_object(user_text):
    """Generate content using Google Generative AI."""
    try:
        # Load the model (gemini-pro is commonly used)
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate content using the provided input text
        response = model.generate_content(user_text)
        
        # Extract the content from the response
        result = response.text  # Access the generated text
        print("AI Response:", result)
        return result
    except Exception as e:
        print(f"Error with Generative AI API: {e}")
        return None


# Main function to run the application
if __name__ == "__main__":
    print("Starting the application...")

    # Step 1: Capture voice input
    user_text = voice_input()

    if user_text:
        # Step 2: Generate AI response
        ai_response = llm_model_object(user_text)
        if ai_response:
            # Step 3: Convert AI response to speech
            audio_file = text_to_speech(ai_response)
            if audio_file:
                print(f"Audio output created: {audio_file}")
        else:
            print("Failed to get a valid response from the AI.")
    else:
        print("No valid user input received.")
