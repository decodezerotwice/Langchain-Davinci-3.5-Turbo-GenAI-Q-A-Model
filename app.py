import openai
import streamlit as st
import os
import base64

# Get the API key from Streamlit secrets
openai_api_key = st.secrets["general"]["OPENAI_API_KEY"]

# Check if the environment variable is loaded correctly
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not found. Please check your Streamlit secrets configuration.")
else:
    print(f"Loaded OPENAI_API_KEY: {openai_api_key}")

# Set the OpenAI API key globally
openai.api_key = openai_api_key

# Function to load OpenAI model and get response
def get_openai_response(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        max_tokens=100,
        temperature=0.5
    )
    return response['choices'][0]['message']['content'].strip()

# Set the page configuration
st.set_page_config(
    page_title="Q&A Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to encode image to Base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Path to the local background image

# Add custom CSS with animations and background image
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');

    @keyframes fadeIn {{
        0% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
    }}

    @keyframes slideIn {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(0); }}
    }}

    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
        100% {{ transform: scale(1); }}
    }}

    * {{
        font-family: 'Montserrat' !important;
    }}

    .sidebar .sidebar-content {{
        background-color: #1f1f2e;
        color: white;
        animation: slideIn 1s ease-in-out;
    }}
    .sidebar .sidebar-content h1 {{
        color: #f39c12;
        animation: pulse 2s infinite;
    }}
    .stButton button {{
        background-color: #f39c12;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s ease;
       
    }}
    .stButton button:hover {{
        background-color: #1fd655;
    }}
    .stTextInput > div > div > input {{
        background-color: #f0f2f6;
        color: #333;
        border: 1px solid #ccc;
        padding: 10px;
        font-size: 16px;
        border-radius: 5px;
        animation: fadeIn 2s ease-in-out;
    }}
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: white !important;
        animation: fadeIn 2s ease-in-out;
        
    }}
    .cool-text {{
        color: #f39c12;
        
        
    }}
    footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        text-align: center;
        padding: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content
st.sidebar.title("Langchain Davinci 3.5 GenAI Q&A Model")
st.sidebar.markdown("The Langchain Davinci 3.5 GenAI model is a cutting-edge AI system designed to understand and respond to natural language queries. Utilizing the latest advancements in machine learning and natural language processing, this model can comprehend complex questions and generate relevant, human-like responses. It's built on OpenAI's powerful GPT-3.5-turbo, which is known for its impressive ability to generate coherent and contextually appropriate text")
st.sidebar.markdown("### Settings")
temperature = st.sidebar.slider("More Accurate vs. More Creative:", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
max_tokens = st.sidebar.slider("Max Tokens:", min_value=50, max_value=500, value=100, step=10)

# Main content
st.markdown("### Ask me anything!")

input_text = st.text_input(label="", key="input")
submit = st.button("Fetch")

# If ask button is clicked
if submit:
    with st.spinner("Generating response..."):
        response = get_openai_response(input_text)
        st.subheader("The Response is:")
        st.markdown(f"<div class='cool-text'>{response}</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <footer>
        Created by <a href="https://joshuaebenezer.com" style="color: white; text-decoration: none;">Joshua Ebenezer</a>
    </footer>
    """,
    unsafe_allow_html=True
)
