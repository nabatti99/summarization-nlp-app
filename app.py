import streamlit as st
import time
import datetime

from summarization import summarize
from ocr import ocr

st.title('CV Summarization Chatbot')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if uploaded_file:= st.file_uploader("Upload a file", type=["jpg", "png"]):
    # Clear chat history
    st.session_state.messages.clear()
    
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"CV/{date}.png"
    with open(filename, "wb") as f:
        buffer = uploaded_file.getbuffer()
        f.write(buffer)

    # Display assistant message in chat message container
    with st.chat_message("assistant"):
        st.markdown("Recognizing...")

    texts = ocr(filename)

    # Display assistant message in chat message container
    with st.chat_message("assistant"):
        st.markdown("Summarizing...")

    for text in texts:
        summarized_text = summarize(text)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            full_response = ""
            # Simulate stream of response with milliseconds delay
            for chunk in summarized_text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": text})

# React to user input
if prompt := st.chat_input("Request here..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    assistant_response = summarize(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        full_response = ""
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
