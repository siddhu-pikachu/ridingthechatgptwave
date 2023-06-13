import streamlit as st
import requests
from gtts import gTTS
import os

# Function to convert text to speech and save it as an audio file
# For this task, I am using the gTTS library

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en', tld='com.mx')
    tts.save(filename)

api_key = os.getenv('OPENAI_API_KEY')

# Set up the Streamlit app
st.title("Book Summary to Audio Converter")

# Create a form for the user to input the book name and the word size required
book_name = st.text_input("Enter the name of the book:")
word_size = st.slider("Select the word size required:", min_value=50, max_value=500, step=25)

# st.write(api_key)

# Create a button to generate the audio file
if st.button("Generate Audio"):
    if api_key:
        # Make a request to the ChatGPT API to get a summary of the book
        url = "https://api.openai.com/v1/engines/text-davinci-003/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
            # Get the API key from an environment variable ___this will be the part that you will have to change___
        }
        data = {
            "prompt": f"Summarize the book '{book_name}' in approximately {word_size} words. Start with the author name and the year the book was published as a sentence, and then continue to summarize the book in the writing style of the author.",
            "max_tokens": word_size,
            "temperature": 1,
        }
        response = requests.post(url, headers=headers, json=data)
        # st.write(response.json())
        summary = response.json()["choices"][0]["text"]

        summary = summary.replace('"', '')
        summary = summary.replace('\'', '')

        st.write(summary)
        # Convert the summary to an audio file
        output_filename = "audiobook.mp3"
        text_to_speech(summary, output_filename)

        # Make the audio file available for download
        st.audio(output_filename, format="audio/mp3")
        # Add a download button for the audio file
        with open(output_filename, 'rb') as file:
            st.download_button("Download Audio", file.read(), file_name='audiobook.mp3')
    else:
        st.error("API key not found. Please make sure to set the OPENAI_API_KEY environment variable.")
