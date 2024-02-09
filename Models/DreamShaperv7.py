import streamlit as st
import requests
import io
from PIL import Image


@st.cache_data
def DreamShaper_v7(token,inputs, guide_scale, inference_steps,Negative):
    API_URL = "https://api-inference.huggingface.co/models/SimianLuo/LCM_Dreamshaper_v7"
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "inputs": inputs,
        "guidence_scale": guide_scale,
        "num_inference_steps": inference_steps,
        "negative_prompt":Negative
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    image_bytes = response.content

    return image_bytes


def display_DreamShaper_v7(token):
    st.markdown("<h1 style='text-align:center;'>DreamShaper v7</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>You can download the image with right click > save image</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.title("Parameters Tuning")
        st.session_state.GS_val2 = st.slider("Select Guidencescale", key="slider1", min_value=0.1, max_value=10.0, value=9.0, step=0.1, help="how much your prompt effect your image")
        if st.session_state.GS_val2 > 9.9:
            st.session_state.GS_val2 = 10
        st.write('Guidence scale:', st.session_state.GS_val2)

        st.session_state.inference_steps_val2 = st.slider("Select Inference Steps", key="slider2", min_value=50, max_value=200, value=100, step=1, help="Number of inference steps for image generation")
        st.write('Inference Steps:', st.session_state.inference_steps_val2)

        st.session_state.Negative3 = st.text_input("enter Negative prompt",help="Things you dont want to see in image")

        st.subheader("Usage Manual (must Read !)")
        st.markdown("""<ul>
                        <li>DreamShaper v7</l1>
                        <li>It convert your text prompts into image</l1>
                        <li>When your prompts contains any hateful or malicious text it wont give you image, instead it might give you error or a blank image so dont do it !</l1>
                        <li>Sometimes it migth give you error even when you give legit prompt in that case try changing prompt a little or clear cache data from above settings</l1>
                        <li>There is only 8000 char input allowed in a single prompt so write wisely</li>
                        <li>when your chat history is long it might get Stuck or takes more time to render page (will fix in future), If you encounter this start another session by refreshing page</li>
                        </ul>
                    
                    """,unsafe_allow_html=True)
        st.success("You are Good to go !")

    if "messages_Dream" not in st.session_state:
        st.session_state["messages_Dream"] = [
            {"role": "assistant", "content": "What kind of image do you need me to generate? (example: entire universe in glass jar)"}]

    # Display previous prompts and results
    for message in st.session_state.messages_Dream:
        st.chat_message(message["role"]).write(message["content"])
        if "image" in message:
            st.chat_message("assistant").image(message["image"], caption=message["prompt"], use_column_width=True)

    # Prompt Logic
    prompt = st.chat_input("Enter your prompt:")

    if prompt:
    # Input prompt
        st.session_state.messages_Dream.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        try:
        # Call the SDF_Runway_ML function with updated parameters
            image_bytes = DreamShaper_v7(token, prompt, st.session_state.GS_val2, st.session_state.inference_steps_val2,st.session_state.Negative3)

        # Open the image using PIL
            image = Image.open(io.BytesIO(image_bytes))
            msg = f'Here is your image related to "{prompt}"'

        # Show the result
            st.session_state.messages_Dream.append({"role": "assistant", "content": msg, "prompt": prompt, "image": image})
            st.chat_message("assistant").write(msg)
            st.chat_message("assistant").image(image, caption=prompt, use_column_width=True)
    
        except Exception as e:
            st.chat_message("assistant").write("Our Server is at Max Capacity Try using Different Model !")
