import streamlit as st
import requests
import random
import time

# Define API URLs for the Mentor and Expert models
API_URL_MENTOR = "https://flowise-9kx9.onrender.com/api/v1/prediction/5daa37e1-3fdb-4eb4-986e-a835ac77ce6a"
API_URL_EXPERT = "https://flowise-9kx9.onrender.com/api/v1/prediction/cef2a608-65a9-4813-a3a7-171a153c40b3"

# List of randomized "thinking" messages
thinking_messages = [
    "Alex is Crunching the numbers…",
    "Running a DCF… please hold for a valuation.",
    "Checking with the M&A team… Alex will be right back.",
    "Consulting the deal book…",
    "Reviewing the pitch deck… insights coming soon.",
    "Adjusting the financial model…",
    "Running a few more Monte Carlo simulations… hang tight!",
    "Preparing a high-stakes IPO answer… patience pays dividends.",
    "Just a moment… Alex is cutting through red tape.",
    "The market's in flux… recalibrating!"
]

# Initialize session state for chat messages and context if not already set
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a default welcome message from the assistant
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I'm here to assist you with any finance recruiting questions you may have. How can I help you today?"
    })

# Selector for choosing between Mentor and Expert model
model_choice = st.selectbox("Choose AI Model", options=["Mentor", "Expert"])

# Function to send queries to the appropriate API based on model choice
def query(context, prompt, model):
    # Select the API URL based on model choice
    api_url = API_URL_MENTOR if model == "Mentor" else API_URL_EXPERT
    
    # Payload includes the refined question as a standalone prompt
    payload = {
        "question": f"{context}\n\nUser Question: {prompt}"
    }
    
    # Debugging output to check the payload before sending
    # st.write("Sending payload:", payload)

    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        return response.json().get("text")
    else:
        return f"Error: {response.status_code}"

# Main content: Chat interface
st.title("💬 Alex, Career Advisor in Finance")
st.markdown(
    """
    - I am AI Agent that answers your questions regarding Finance and Investment Banking Recruiting.
    - To provide accurate and high-performance answers, I was built using a multiple-agent framework. 
    - 🧠 This enables me to deliver valuable insights with sharper reasoning than ChatGPT.
    - 🎓 Mentor Mode: I serve as your personal tutor, encouraging thoughtful reflection and helping you develop skills for continuous improvement.
    - 💯 Expert Mode: I deliver advanced, high-precision insights to address complex questions with maximum accuracy. (I will think longer, please be patient!)
    """
)

# Display existing chat messages with profile pictures
for message in st.session_state.messages:
    role = message["role"]
    avatar_url = "https://github.com/Reese0301/GIS-AI-Agent/blob/main/4322991.png?raw=true" if role == "assistant" else "https://github.com/Reese0301/GIS-AI-Agent/blob/main/FoxUser.png?raw=true"
    with st.chat_message(role, avatar=avatar_url):
        st.markdown(message["content"])

# Chat input field for user to enter a message
if prompt := st.chat_input("Ask your question here..."):

    # Store and display the user's message with the user avatar
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="https://github.com/Reese0301/GIS-AI-Agent/blob/main/FoxUser.png?raw=true"):
        st.markdown(prompt)

    # Display a random "Alex is thinking..." message
    thinking_message = random.choice(thinking_messages)
    thinking_placeholder = st.empty()
    thinking_placeholder.markdown(f"💭 **{thinking_message}**")

    # Start the timer
    start_time = time.time()
    
    # Limit the conversation context to the last 5 messages
    CONTEXT_LIMIT = 5
    context = ""
    for msg in st.session_state.messages[-CONTEXT_LIMIT:]:  # Only take the last 5 messages
        if msg["role"] == "assistant":
            context += f"Assistant: {msg['content']}\n"
        elif msg["role"] == "user":
            context += f"User: {msg['content']}\n"
    
    # Send the refined standalone question to the selected model API
    response_content = query(context, prompt, model_choice)
    
    # End the timer
    end_time = time.time()
    response_time = end_time - start_time  # Calculate the response time in seconds

    # Clear the thinking message after receiving the response
    thinking_placeholder.empty()

    # Display the assistant's response with the assistant avatar
    with st.chat_message("assistant", avatar="https://github.com/Reese0301/GIS-AI-Agent/blob/main/4322991.png?raw=true"):
        # Show the response time only for Expert mode
        if model_choice == "Expert":
            st.markdown(f"💭 Thought for {response_time:.2f} seconds\n\n{response_content}")
        else:
            st.markdown(response_content)
    
    # Append the assistant's response to the session state chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})

# Sidebar for suggested prompts or custom messages
with st.sidebar:
    st.markdown(
        """
        <div style="background-color: #f0f0f5; padding: 20px; border-radius: 10px;">
            <h4>💡 Suggested Prompts</h4>
            <ul>
                <li>What are the key steps to develop a career in investment banking?</li>
                <li>Surprise me with one insight on Investment Banking Recruiting.</li>
                <li>What are the dos and donts of a superday interview?</li>
                <li>Can you suggest networking strategies for international students? </li>
            </ul>
            <div style="margin-top: 20px; border-top: 1px solid #ccc; padding-top: 10px; text-align: center;">
                <small>For Feedback or Concerns, contact: <a href="mailto:yizhuoyang@hotmail.com">yizhuoyang@hotmail.com</a></small>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
