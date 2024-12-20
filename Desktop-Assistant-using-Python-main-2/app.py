import streamlit as st
from src.helper import voice_input, text_to_speech, llm_model_object
import os

def main():
    st.title("Naughty AI Assistant 🧠🎤")

    # Informative message for the user
    st.write("Jankari ke liye button press kre!")

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

                # Step 3: Generate AI response
                response = llm_model_object(text)

                # Step 4: Check if AI generated valid output
                if response and response.strip():
                    st.write("🤖 **AI Response:**")
                    st.text_area("Response", response, height=250)

                    # Convert AI response to speech
                    audio_file_path = text_to_speech(response)

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
