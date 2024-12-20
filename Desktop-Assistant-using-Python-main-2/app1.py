import streamlit as st
from src.helper import voice_input, text_to_speech, llm_model_object
import os
import re
import requests




# Weather API Key
WEATHER_API_KEY = "9afd9ba701880f76f84b7e0b95d9afef"  # OpenWeatherMap API key

def get_weather(city_name):
    """
    Fetch weather information for a given city using OpenWeatherMap API.
    """
    try:
        # OpenWeatherMap API endpoint
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        # Check if the API call was successful
        if data.get("cod") != 200:
            return f"Sorry, I couldn't fetch weather data for {city_name}. Please check the city name."

        # Extract weather details
        weather_desc = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]

        # Format the weather response
        weather_info = (
            f"Weather in {city_name}:\n"
            f"- Description: {weather_desc.capitalize()}\n"
            f"- Temperature: {temperature}°C\n"
            f"- Feels Like: {feels_like}°C\n"
            f"- Humidity: {humidity}%"
        )
        return weather_info
    except Exception as e:
        return f"An error occurred while fetching weather data: {e}"
    
    
    
    
def clean_output(text):
    """
    Function to remove all '*' symbols from the text.
    """
    cleaned_text = text.replace('*', '')
    return cleaned_text

def main():
    st.title("Friendly AI Assistant 🧠🎤")

    # Informative message for the user
    st.write("Press the button below and ask me anything!")

    # Streamlit Button to trigger voice input
    if st.button("Kuch bhi pucho Bhai! 🎙️"):
        with st.spinner("Sun raha hu bhai... 🕒"):
            try:
                # Step 1: Capture voice input
                text = voice_input()

                # Step 2: Check if voice was captured successfully
                if not text or text.strip() == "":
                    st.error("Kuch sunayi nahi diya! Please try again.")
                    return
                
                st.success(f"User said: {text}")
                
                
                 # Step 3: Check if the query relates to weather
                if "weather" in text.lower() or "temperature" in text.lower():
                    city_name = text.split()[-1]  # Assume the city name is the last word
                    weather_response = get_weather(city_name)
                    st.write("🌦️ **Weather Information:**")
                    st.text_area("Weather Details", weather_response, height=200)

                    # Convert weather response to speech
                    audio_file_path = text_to_speech(weather_response)
                    if audio_file_path:
                        with open(audio_file_path, "rb") as audio_file:
                            audio_bytes = audio_file.read()

                        st.audio(audio_bytes, format="audio/mp3")
                        st.download_button(label="Download Weather Info",
                                           data=audio_bytes,
                                           file_name="weather_info.mp3",
                                           mime="audio/mp3")
                    return

                # Step 3: Generate AI response
                response = llm_model_object(text)

                # Step 4: Check if AI generated valid output
                if response and response.strip():
                    # Clean any '*' from the AI response
                    cleaned_response = clean_output(response)

                    st.write("🤖 **AI Response:**")
                    st.text_area("Response", cleaned_response, height=250)

                    # Convert cleaned AI response to speech
                    audio_file_path = text_to_speech(cleaned_response)

                    if audio_file_path:
                        # Play audio response
                        with open(audio_file_path, "rb") as audio_file:
                            audio_bytes = audio_file.read()

                        st.audio(audio_bytes, format="audio/mp3")
                        st.download_button(label="Download Speech",
                                           data=audio_bytes,
                                           file_name="response.mp3",
                                           mime="audio/mp3")
                    else:
                        st.error("Speech generation failed. Please try again.")

                else:
                    st.error("AI did not return any valid response.")

            except Exception as e:
                st.error(f"Error: {e}")
                st.write("Something went wrong. Please try again!")

if __name__ == "__main__":
    main()
