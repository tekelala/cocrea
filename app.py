import streamlit as st
import requests
import json
import pprint
from docx import Document
from io import BytesIO

# Define send message function
def create_text(prompt):
    api_url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": st.secrets["API_KEY"]  # Use the API key from Streamlit's secrets
    }

    # Prepare the prompt for Claude
    conversation = f"Human: {prompt}\n\nAssistant:"

    # Define the body of the request
    body = {
        "prompt": conversation,
        "model": "claude-v1.3-100k",
        "max_tokens_to_sample": 100000,
        "temperature": 0.7,
        "stop_sequences": ["\n\nHuman:"]
    }

    # Make a POST request to the Claude API
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(body))
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        st.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        st.error(f"Something went wrong: {err}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

    # Extract Claude's response from the JSON response
    result = response.json()

    # Return Claude's response as a dictionary
    return result

# Streamlit App

st.title('AI Summary App')

# Input fields
proyecto = st.text_area("Proyecto")
beneficiadas = st.number_input('Personas beneficiadas', value=0, format="%i")
inversion = st.number_input("Inversión")

if st.button('Escribiendo el proyecto'):
    # Create the prompt
    prompt = f'''Role: You are an AI assistant trained in legal expertise and your answers needs to be always in Spanish and just provide the text requested no need of titles or writting what you are doing

                Task: Create a summary of approximately 100 words for the following text {proyecto}'''

    # Call the function
    result = create_text(prompt)

    # Pretty print the result
    pp = pprint.PrettyPrinter(indent=4)
    st.write(pp.pformat(result))

    # Write to .docx
    doc = Document()
    doc.add_paragraph(pp.pformat(result))

    # Save to BytesIO object
    f = BytesIO()
    doc.save(f)
    f.seek(0)

    # Add download button
    st.download_button(
        label="Descargar",
        data=f,
        file_name="result.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
