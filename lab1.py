import streamlit as st
import os 
from openai import OpenAI


# Show title and description.
st.title("Ankit's Gpt Version 1")
st.write("Add Your Open AI Key")



openai_api_key = st.text_input("OpenAI API Key", type="password")

#openai_api_key = st.secrets["OPEN_API_KEY"]


if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via ⁠ st.file_uploader ⁠.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via ⁠ st.text_area ⁠.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using ⁠ st.write_stream ⁠.
        st.write_stream(stream)

