import speech_recognition as sr  # Speech-to-text converter
import datetime
import wikipedia
import webbrowser
import requests
from AppKit import NSSpeechSynthesizer  # Speak provided text using NSSpeechSynthesizer
import os
import sys

# Initialize NSSpeechSynthesizer for Mac
synthesizer = NSSpeechSynthesizer.alloc().init()
available_voices = ["com.apple.speech.synthesis.voice.Alex", "com.apple.speech.synthesis.voice.samantha"]
synthesizer.setVoice_(available_voices[1])  # Set default voice to Alex
synthesizer.setRate_(180)  # Adjust the speaking rate

# API keys (Replace with your actual API keys)
WEATHER_API_KEY = "9afd9ba701880f76f84b7e0b95d9afef"
NEWS_API_KEY = "bd9ceea0c7db4cd4abde789ed3a8daf5"

# Function to convert text to speech
def speak(text):
    """Speak the provided text using NSSpeechSynthesizer."""
    print(f"Speaking: {text}")
    synthesizer.startSpeakingString_(text)
    
    # Wait until the speech finishes before proceeding
    while synthesizer.isSpeaking():
        pass  # Keep checking if it's speaking, and wait if it is


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


# Function to greet the user
def wish_me():
    """Greet the user based on the current time."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning! How can I assist you today?")
    elif hour < 18:
        speak("Good afternoon! How can I assist you today?")
    else:
        speak("Good evening! How can I assist you today?")

# Function to get the weather of multiple cities
def get_weather_for_multiple_cities():
    """Fetch temperature data for multiple cities."""
    speak("Please tell me the names of the cities you want to know the temperature for.")
    city_input = takeCommand()

    if city_input == "None" or not city_input.strip():
        speak("I didn't get any city names. Please try again.")
        return

    # Remove unnecessary prompt text from the recognized input
    city_input = city_input.replace("please tell me the names of the cities you want to know the temperature for", "").strip()

    # Now split the remaining input by commas or treat it as a single city
    cities = [city.strip() for city in city_input.split(",")]

    if len(cities) == 0:
        speak("No cities provided. Please try again.")
        return

    print(f"Cities to check: {cities}")  # Debug print to ensure correct input

    for city in cities:
        # Get weather data for each city
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        try:
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            # Check if the city is valid and the API call was successful
            if weather_response.status_code == 200:
                temp = weather_data["main"]["temp"]
                weather_report = f"The current temperature in {city} is {temp}°C."
                speak(weather_report)
                print(weather_report)
            else:
                # Handle case where city is not found or invalid
                speak(f"Could not fetch weather data for {city}. Please check the city name.")
                print(f"Could not fetch weather data for {city}. Status code: {weather_response.status_code}")
        except requests.RequestException as e:
            speak("Error fetching weather data.")
            print(f"Weather fetch error: {e}")




# Function to fetch and announce the latest news
def get_news():
    """Fetch the latest headlines and read them aloud."""
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        news_data = response.json()

        if news_data["status"] == "ok":
            articles = news_data["articles"][:5]
            for i, article in enumerate(articles, 1):
                title = article["title"]
                speak(f"News {i}: {title}")
                print(f"News {i}: {title}")
        else:
            speak("Sorry, I couldn't fetch the news at the moment.")
    except Exception as e:
        speak("There was an error fetching the news.")
        print(f"News fetch error: {e}")



# Main function that processes voice commands
# Main function that processes voice commands
if __name__ == "__main__":
    wish_me()

    while True:  # Run indefinitely
        query = takeCommand()
        
        if query == "None":
            continue

        # Respond to "wish me"
        if "wish me" in query:
            wish_me()

        # Respond to greetings
        elif "good morning" in query:
            speak("Good morning! How can I assist you?")
        elif "good afternoon" in query:
            speak("Good afternoon! How can I assist you?")
        elif "good evening" in query:
            speak("Good evening! How can I assist you?")

        # Wikipedia search
        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception:
                speak("Sorry, I couldn't find anything on Wikipedia.")

        # Open websites
        elif "youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "github" in query:
            speak("Opening GitHub")
            webbrowser.open("https://www.github.com")
        elif "twitter" in query:
            speak("Opening Twitter")
            webbrowser.open("https://x.com")

        # Open applications
        elif "music" in query:
            speak("Opening the Music app")
            os.system("open -a Music")
        elif "code" in query:
            speak("Opening Visual Studio Code")
            os.system("open -a 'Visual Studio Code'")

        # Time command
        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        # Weather and temperature updates
        elif "weather" in query or "temperature" in query:
            get_weather_for_multiple_cities()  # Correct function call

        # News updates
        elif "news" in query or "headlines" in query:
            get_news()

        # Exit command
        elif "stop" in query or "exit" in query or "goodbye" in query or "bye" in query or "thankyou" in query:
            speak("Goodbye! Have a great day.")
            sys.exit()

        # Unknown commands
        else:
            speak("Sorry, I didn't understand that. Please try again.")
        

