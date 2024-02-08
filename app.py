import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
import os

from Models.SDF import display_SDF
from Models.RunwayML_SDF import display_RunwayML_SDF
from Models.SDFv2 import display_SDFv2
from Models.DreamShaperv7 import display_DreamShaper_v7
from Models.Anime_DF import display_Anime_df


load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_API_KEY1 = os.getenv("HUGGINGFACE_API_KEY1")

st.set_page_config(
        page_title="Generative Media",
)

# Define the sidebar
with st.sidebar:
    # Create the options menu
    selected = option_menu(menu_title="Media-Gen Models",
                           options=["Stable Diffusion 1.0", "Stable Diffusion 1.5","Stable Diffusion 2.1","DreamShaper v7","Anime Diffusion"],
                           icons=["box", "box", "box","box","box"],
                           menu_icon="boxes",
                           default_index=0
                           )
    
if selected == "Stable Diffusion 1.0":
    display_SDF(HUGGINGFACE_API_KEY)
elif selected == "Stable Diffusion 1.5":
    display_RunwayML_SDF(HUGGINGFACE_API_KEY)
elif selected == "Stable Diffusion 2.1":
    display_SDFv2(HUGGINGFACE_API_KEY)
elif selected == "DreamShaper v7":
    display_DreamShaper_v7(HUGGINGFACE_API_KEY1)
elif selected == "Anime Diffusion":
    display_Anime_df(HUGGINGFACE_API_KEY1)
