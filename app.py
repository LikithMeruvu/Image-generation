import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
import os

from Models.SDF import display_SDF
from Models.Brea import display_Brea
from Models.DreamShaperv7 import display_DreamShaper_v7
from Models.Anime_DF import display_Anime_df
from Models.Dall_e3 import display_Dall_e3


load_dotenv()
HUGGINGFACE_API_KEY = st.secrets['HUGGINGFACE_API_KEY']
HUGGINGFACE_API_KEY1 = st.secrets['HUGGINGFACE_API_KEY1']
OPEN_AI_API = st.secrets['OPEN_AI_API']

st.set_page_config(
        page_title="Generative Image",
)

# Define the sidebar
with st.sidebar:
    # Create the options menu
    selected = option_menu(menu_title="Image-Gen Models",
                           options=["Stable Diffusion XL","Brea v2","DreamShaper v7","Dall-e2","Anime Diffusion"],
                           icons=["box", "box","box","box","box"],
                           menu_icon="boxes",
                           default_index=0
                           )
    
if selected == "Stable Diffusion XL":
    display_SDF(HUGGINGFACE_API_KEY)
elif selected == "Brea v2":
    display_Brea(HUGGINGFACE_API_KEY)
elif selected == "DreamShaper v7":
    display_DreamShaper_v7(HUGGINGFACE_API_KEY1)
elif selected == "Anime Diffusion":
    display_Anime_df(HUGGINGFACE_API_KEY1)
elif selected == "Dall-e2":
    display_Dall_e3(OPEN_AI_API)
