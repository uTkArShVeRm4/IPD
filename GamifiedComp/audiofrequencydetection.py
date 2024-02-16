import streamlit as st
from IPython.display import YouTubeVideo
import youtube_dl
from pydub import AudioSegment
from pydub.playback import play
import os
import random
import librosa
import numpy as np

def modify_audio_frequency(audio_data, srs, variables):
    
    audio_data = audio_data.astype(np.float32)
    # Randomly select three variables within the specified range
    random_factors = [random.uniform(variables[0], variables[1]),
                      random.uniform(variables[2], variables[3]),
                      random.uniform(variables[4], variables[5])]

    # Apply the selected variables to modify the frequency
    modified_audios = []
    for factor in random_factors:
        modified_audio = librosa.effects.pitch_shift(audio_data, sr = srs, n_steps=factor)
        modified_audios.append(modified_audio)
    print("completed\n\n")
    return modified_audios


def download_audio_from_youtube(url, output_dir="."):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s')
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def page1():
    st.title("YouTube Video Player")

    # Input field for YouTube URL
    youtube_url = st.text_input("Enter YouTube URL:", "")

    if youtube_url:
        st.text("Loading video...")
        try:
            video_id = youtube_url.split("v=")[1]
            video_url = f"https://www.youtube.com/embed/{video_id}"
            video_player = f'<iframe width="560" height="315" src="{video_url}" frameborder="0" allowfullscreen id="ytplayer"></iframe>'
            st.markdown(video_player, unsafe_allow_html=True)
            # Play audio
            st.text("Click the button when you can hear the sound:")
            play_button = st.button("I can hear it!")
            if play_button:
                st.write('<script>document.getElementById("ytplayer").contentWindow.postMessage({"event":"command","func":"pauseVideo","args":""}, "*");</script>', unsafe_allow_html=True)

            
        except Exception as e:
            st.error(f"Error: {e}")

def page2():
    st.title("Custome Audio file")
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])

    if audio_file is not None:
        st.audio(audio_file, format='audio/wav')

        # Load the audio file
        audio_data, sr = librosa.load(audio_file, sr=None, duration=4)
        print(sr)
        # Check if audio file is longer than 4 seconds, if so, trim it
        if len(audio_data) > sr * 10:
            audio_data = audio_data[:sr * 10]

        # Specify the range for the three variables
        variables_range = (-3.0, 3.0, -2.0, 2.0, -1.0, 1.0)

        # Modify the frequency of the audio using the selected variables
        modified_audios = modify_audio_frequency(audio_data, sr, variables_range)

        # Randomly shuffle the modified audios
        random.shuffle(modified_audios)

        # Play the modified audios in sequence
        st.text("Playing modified audios...")
        for modified_audio in modified_audios:
            st.audio(modified_audio, format='audio/wav')
    
def page3():
    st.title("Page 3")
    st.write("This is Page 3")
    
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Page 1", "Page 2", "Page 3"])

    if page == "Page 1":
        page1()
    elif page == "Page 2":
        page2()
    elif page == "Page 3":
        page3()

        

if __name__ == "__main__":
    main()