import streamlit as st
import requests
import io
from PIL import Image


@st.cache_data
def SDF_Runway_ML(token,inputs, guide_scale, inference_steps):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "inputs": inputs,
        "guide_scale": guide_scale,
        "inference_steps": inference_steps
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    image_bytes = response.content

    return image_bytes


def display_RunwayML_SDF(token):
    st.markdown("<h1 style='text-align:center;'>Stable Diffusion RunwayML v-1.5</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>You can download the image with right click > save image</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.title("Parameters Tuning (SDF)")
        st.session_state.GS_val = st.slider("Select Guidencescale", key="slider1", min_value=0.1, max_value=10.0, value=7.5, step=0.1, help="how much your prompt effect your image")
        if st.session_state.GS_val > 9.9:
            st.session_state.GS_val = 10
        st.write('Guidence scale:', st.session_state.GS_val)

        st.session_state.inference_steps_val = st.slider("Select Inference Steps", key="slider2", min_value=50, max_value=200, value=50, step=1, help="Number of inference steps for image generation")
        st.write('Inference Steps:', st.session_state.inference_steps_val)

    if "messages_run" not in st.session_state:
        st.session_state["messages_run"] = [
            {"role": "assistant", "content": "What kind of image do you need me to generate? (example: Sunrise moment)"}]

    # Display previous prompts and results
    for message in st.session_state.messages_run:
        st.chat_message(message["role"]).write(message["content"])
        if "image" in message:
            st.chat_message("assistant").image(message["image"], caption=message["prompt"], use_column_width=True)

    # Prompt Logic
    prompt = st.chat_input("Enter your prompt:")

    if prompt:
        # Input prompt
        st.session_state.messages_run.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Query Stable Diffusion
        headers = {"Authorization": f"Bearer {token}"}
        image_bytes = SDF_Runway_ML(token, prompt, st.session_state.GS_val, st.session_state.inference_steps_val)

        # Return Image
        image = Image.open(io.BytesIO(image_bytes))
        msg = f'Here is your image related to "{prompt}"'

        # Show Result
        st.session_state.messages_run.append({"role": "assistant", "content": msg, "prompt": prompt, "image": image})
        st.chat_message("assistant").write(msg)
        st.chat_message("assistant").image(image, caption=prompt, use_column_width=True)
