import streamlit as st
import requests
import io
from PIL import Image

@st.cache_data
def SDF_v2(token, inputs, guide_scale, inference_steps):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "inputs": inputs,
        "guide_scale": guide_scale,
        "inference_steps": inference_steps,
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    image_bytes = response.content

    return image_bytes

def display_SDFv2(token):
    st.markdown("<h1 style='text-align:center;'>Stable Diffusion v-2.1</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>You can download the image with right click > save image</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.title("Parameters Tuning")
        st.session_state.guide_scale_val3 = st.slider("Select Guidencescale", key="slider1", min_value=0.1, max_value=10.0, value=8.5, step=0.1, help="how much your prompt effect your image")
        if st.session_state.guide_scale_val3 > 9.9:
            st.session_state.guide_scale_val3 = 10
        st.write('Guidence scale:', st.session_state.guide_scale_val3)

        st.session_state.inference_steps_val = st.slider("Select Inference Steps", key="slider2", min_value=50, max_value=200, value=100, step=1, help="Number of inference steps for image generation")
        st.write('Inference Steps:', st.session_state.inference_steps_val)

        st.subheader("Usage Manual (must Read !)")
        st.markdown("""<ul>
                        <li>Stable diffusion v-2.1</l1>
                        <li>It convert your text prompts into image</l1>
                        <li>When your prompts contains any hateful or malicious text it wont give you image, instead it might give you error or a blank image so dont do it !</l1>
                        <li>Sometimes it migth give you error even when you give legit prompt in that case try changing prompt a little or clear cache data from above settings</l1>
                        <li>There is only 8000 char input allowed in a single prompt so write wisely</li>
                        <li>when your chat history is long it might get Stuck or takes more time to render page (will fix in future), If you encounter this start another session by refreshing page</li>
                        </ul>
                    
                    """,unsafe_allow_html=True)
        st.success("You are Good to go !")

    if "messages_sdfv2" not in st.session_state:
        st.session_state["messages_sdfv2"] = [
            {"role": "assistant", "content": "What kind of image do you need me to generate? (example: cool dog with a cute smile !)"}]

    # Display previous prompts and results
    for message in st.session_state.messages_sdfv2:
        st.chat_message(message["role"]).write(message["content"])
        if "image" in message:
            st.chat_message("assistant").image(message["image"], caption=message["prompt"], use_column_width=True)

    # Prompt Logic
    prompt = st.chat_input("Enter your prompt:")

    if prompt:
        # Input prompt
        st.session_state.messages_sdfv2.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        image_bytes = SDF_v2(token, prompt, st.session_state.guide_scale_val3, st.session_state.inference_steps_val)

        # Return Image
        image = Image.open(io.BytesIO(image_bytes))
        msg = f'Here is your image related to "{prompt}"'

        # Show Result
        st.session_state.messages_sdfv2.append({"role": "assistant", "content": msg, "prompt": prompt, "image": image})
        st.chat_message("assistant").write(msg)
        st.chat_message("assistant").image(image, caption=prompt, use_column_width=True)
