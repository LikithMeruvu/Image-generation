from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import streamlit as st

@st.cache_data
def Dall_e2(token,prompt):
    client = OpenAI(api_key=token)
    response = client.images.generate(
     model = "dall-e-2",
     prompt = prompt,
     size = "512x512",
     quality = "hd",
     n=1,
   )
    image_url = response.data[0].url
    return image_url



def display_Dall_e3(token):
    st.markdown("<h1 style='text-align:center;'>OpenAI DALL-E 2.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>You can download the image with right click > save image</p>", unsafe_allow_html=True)

    with st.sidebar:

        st.subheader("Usage Manual (Must Read!)")
        st.markdown("""<ul>
                        <li>DALL-E 2.0</li>
                        <li>It converts your text prompts into images</li>
                        <li>Ensure your prompts do not contain hateful or malicious text as it may result in errors or blank images</li>
                        <li>If you encounter errors with legitimate prompts, try altering the prompt slightly or clearing cache data from above settings</li>
                        <li>Only 8000 characters are allowed in a single prompt, so write wisely</li>
                        <li>If your chat history is long, it might cause the page to be stuck or take more time to render (will be fixed in the future). If you encounter this, start another session by refreshing the page</li>
                        </ul>
                    """, unsafe_allow_html=True)
        st.success("You are good to go!")

    if "messages_dall_e3" not in st.session_state:
        st.session_state["messages_dall_e3"] = [
            {"role": "assistant", "content": "What kind of image do you need me to generate? (example: a cat riding a bicycle)"}
        ]

    # Display previous prompts and results
    for message in st.session_state.messages_dall_e3:
        st.chat_message(message["role"]).write(message["content"])
        if "image" in message:
            st.chat_message("assistant").image(message["image"], caption=message["prompt"], use_column_width=True)

    # Prompt Logic
    prompt = st.chat_input("Enter your prompt:")

    if prompt:
        # Input prompt
        st.session_state.messages_dall_e3.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        try:
            # Call the Dall_e3 function with updated parameters
            image_url = str(Dall_e2(token, prompt))

            # Fetch the image from the URL
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))

            # Show the result
            st.session_state.messages_dall_e3.append({"role": "assistant", "content": f'Here is your image related to "{prompt}"', "prompt": prompt, "image": img})
            st.chat_message("assistant").write(f'Here is your image related to "{prompt}"')
            st.chat_message("assistant").image(img, caption=prompt, use_column_width=True)

        except Exception as e:
            st.chat_message("assistant").write("Our server is at max capacity. Please try using a different model.")
