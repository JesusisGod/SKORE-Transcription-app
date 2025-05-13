#  Web Speech API (with partial/interim transcript)
#  streamlit_python_Javascript4.py
# INSTALLATION:
# C:\Users\IniOluwa\AppData\Local\Microsoft\WindowsApps\python3.10.exe -m venv venv
# .\venv\Scripts\Activate.ps1
# C:\Users\IniOluwa\StreamlitPythonJava\venv\Scripts\python.exe -m pip install streamlit bokeh==2.4.3 streamlit_bokeh_events
# C:\Users\IniOluwa\StreamlitPythonJava\venv\Scripts\python.exe -m pip install --upgrade pip
# C:\Users\IniOluwa\StreamlitPythonJava\venv\Scripts\python.exe -m pip uninstall numpy
# C:\Users\IniOluwa\StreamlitPythonJava\venv\Scripts\python.exe -m pip install numpy==1.23.5

# RUN with C:\Users\Ogunbo\StreamlitPythonJavaScript\venv\Scripts\python.exe  C:\Users\Ogunbo\StreamlitPythonJavaScript\venv\Scripts\streamlit.exe run .\streamlit_python_Javascript4.py
# DEBUG with C:\Users\Ogunbo\StreamlitPythonJavaScript\venv\Scripts\python.exe  C:\Users\Ogunbo\StreamlitPythonJavaScript\venv\Scripts\streamlit.exe run .\streamlit_python_Javascript4.py --logger.level=debug

# https://discuss.streamlit.io/t/speech-to-text-on-client-side-using-html5-and-streamlit-bokeh-events/7888
# https://discuss.streamlit.io/t/bokeh-plots-no-longer-showing/28762
# https://stackoverflow.com/questions/48839314/how-to-add-punctuation-to-web-speech-api

import streamlit as st
import bokeh
#from bokeh.models.widgets import Button #pip install bokeh
from bokeh.models import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events # pip install streamlit-bokeh-events
from translate import Translator
#from_lang='en'; to_lang ='ko'
from_lang='ko'; to_lang ='en'

#// recognition.lang = 'en-US';
#//recognition.lang = from_lang;
# AttributeError: module 'numpy' has no attribute 'bool8' solved by:
# C:\Users\Ogunbo\streamlit_mic_recorder\venv\Scripts\python.exe -m pip uninstall numpy
# C:\Users\Ogunbo\streamlit_mic_recorder\venv\Scripts\python.exe -m pip install numpy==1.23.5

def text_translation(text,from_lang,to_lang): # from c:/Users/Ogunbo/gradio-groq-basics-main/calorie-tracker/gradio_Elevenlabs.py
    translation = Translator(from_lang=from_lang,to_lang=to_lang)
    translation_text =translation.translate(text)
    ccc="""
    translator_es = Translator(from_lang="en", to_lang="es")
    es_text = translator_es.translate(text)

    translator_ar = Translator(from_lang="en", to_lang="ar")
    ar_text = translator_ar.translate(text)

    translator_ja = Translator(from_lang="en", to_lang="ja")
    ja_text = translator_ja.translate(text)

    return es_text, ar_text, ja_text
    """
    return translation_text


#print(bokeh.__version__)
stt_button = Button(label="Speak", width=100)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "ko-KR"
    
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            } else {
                value += e.results[i][0].transcript; //interim Transcript                        
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        transcription = result.get("GET_TEXT")
        #st.write(f"#{result.get("GET_TEXT")}") # Latex, single # sign gives the biggest fontsize with bold face
        #st.write(f"#{transcription}")
        trF=transcription.find(".")
        trQ=transcription.find("?")
        translation = text_translation(transcription,from_lang,to_lang)
        st.write(f"{translation}")
        print(translation)
        if(trF > -1 or trQ >-1):
            translation = text_translation(transcription,from_lang,to_lang)
            print(translation)
            st.write(f"{translation}")
