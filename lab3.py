import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("This is Lab 3")

# Fetch the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

# Set up the session state to hold chatbot messages and track if more info is requested
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
if "awaiting_more_info" not in st.session_state:
    st.session_state["awaiting_more_info"] = False  # Initialize awaiting_more_info

# Display the chatbot conversation
st.write("## Chatbot Interaction")
for msg in st.session_state.messages:
    chat_msg = st.chat_message(msg["role"])
    chat_msg.write(msg["content"])

# Get user input for the chatbot
if prompt := st.chat_input("Ask the chatbot a question or interact:"):
    # Append user input to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display the user input in the chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if the bot is awaiting a 'yes' or 'no' response for more information
    if st.session_state["awaiting_more_info"]:
        if prompt.lower() == "yes":
            # If user wants more info, provide additional details
            more_info_response = "Here’s some more information: [Detailed but simple explanation for a 10-year-old]. Do you want more info?"
            st.session_state.messages.append({"role": "assistant", "content": more_info_response})
            with st.chat_message("assistant"):
                st.write(more_info_response)

        elif prompt.lower() == "no":
            # If the user says no, ask what else the bot can help with
            no_more_info_response = "Okay! What else can I help you with?"
            st.session_state.messages.append({"role": "assistant", "content": no_more_info_response})
            st.session_state["awaiting_more_info"] = False  # Reset awaiting status
            with st.chat_message("assistant"):
                st.write(no_more_info_response)

        else:
            # If the response is not 'yes' or 'no', re-ask the question
            clarification_response = "Please answer 'yes' or 'no'. Do you want more info?"
            st.session_state.messages.append({"role": "assistant", "content": clarification_response})
            with st.chat_message("assistant"):
                st.write(clarification_response)

    else:
        # If not awaiting more info, generate response to the user's question
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages  # Send conversation history
        )

        # Extract the assistant's response correctly by accessing the 'content' attribute
        assistant_response = response.choices[0].message.content

        # Ensure the answer is simple enough for a 10-year-old
        simplified_response = f"Here’s the answer in a simple way: {assistant_response}. Do you want more info?"
        
        # Display the assistant's response and ask if more info is needed
        st.session_state.messages.append({"role": "assistant", "content": simplified_response})
        st.session_state["awaiting_more_info"] = True  # Set flag to expect 'yes' or 'no'
        with st.chat_message("assistant"):
            st.write(simplified_response)