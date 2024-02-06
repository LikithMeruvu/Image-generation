import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
import os

from Models.SDF import display_SDF
from Models.RunwayML_SDF import display_RunwayML_SDF
# # from Models.kosmos2 import Display_Kosmos2
# from Models.Palm2 import Display_Palm2
# from Models.Mistral import Display_Mistral_7B
# from Models.Llama2 import Display_Llama2

load_dotenv()
HUGGINGFACE_API_KEY = api_key = os.getenv("HUGGINGFACE_API_KEY")

st.set_page_config(
        page_title="Generative LLMs",
)

# Define the sidebar
with st.sidebar:
    # Create the options menu
    selected = option_menu(menu_title="Media-Gen Models",
                           options=["Stable Diffusion 1.0", "Stable Diffusion 1.5","Model3","Model4","Model5"],
                           icons=["box", "box", "box","box","box"],
                           menu_icon="boxes",
                           default_index=0
                           )
    
if selected == "Stable Diffusion 1.0":
    display_SDF(HUGGINGFACE_API_KEY)
elif selected == "Stable Diffusion 1.5":
    display_RunwayML_SDF(HUGGINGFACE_API_KEY)
# # elif selected == "Kosmos2":
# #     Display_Kosmos2()
# elif selected == "Palm-2":
#     Display_Palm2()
# elif selected == "Mistral 8x7B":
#     Display_Mistral_7B()
# elif selected == "Llama-2 70B":
#     Display_Llama2()