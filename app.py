import streamlit as st
import requests
import json
import pprint
from docx import Document
from io import BytesIO

# Function to read the jsons
def read_json(json_file_name):
    # Open the JSON file
    with open(json_file_name, 'r') as file:
        # Load the data from the file
        data = json.load(file)
        
    # Extract values from the JSON data
    # The keys used here are placeholders, replace them with the actual keys from your JSON data
    text_json = data.get('text', '')
    
    return text_json

# Loading the jsons
text_convocatoria = read_json('jsons/convocatoria.json')
text_derechosculturales = read_json('jsons/derechosculturales.json')
text_plandesarrollo = read_json('jsons/plandesarrollo.json')

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

st.title('Formulador de proyectos')

 # Step 1
nombre_proyecto = st.text_input('Nombre del Proyecto')
nombre_titular_proyecto = st.text_input('Nombre del Titular del proyecto')
contexto_proyecto = st.text_area('Contexto del Proyecto')
objetivo_proyecto = st.text_area('Objetivo del Proyecto')
metricas_exito = st.text_area('Metricas de Exito')
experiencia_titular = st.text_area('Experiencia Titular')

# Step 2
eje_proyecto_options = [
    "Eje 1 Cultura de Paz: Participación ciudadana y construcción de la paz en territorios de posconflicto",
    "Eje 1 Cultura de Paz: Memoria y legado de la verdad en el país",
    "Eje 2 Culturas, artes para la vida: Formación, educación y aprendizaje para la construcción de ciudadanías libres y sensibles",
    "Eje 2 Culturas, artes para la vida: Espacios culturales para la vida",
    "Eje 2 Culturas, artes para la vida: Ecosistemas vivos de las culturas, las artes y los saberes",
    "Eje 3 Memoria viva y saberes: Gestión integral y territorial de los patrimonios para la vida y la paz",
    "Eje 3 Memoria viva y saberes: Memorias, saberes y oficios hacia una construcción diversa de nación",
    "Eje 4 Colombia en el mundo: las culturas, las artes y los saberes para la reconciliación del ser humano con el planeta",
    "Eje 4 Colombia en el mundo: Diálogo intercultural con el mundo",
    "Eje 5 Colombia sociedad de conocimiento: Propiedad intelectual para la riqueza social",
    "Eje 5 Colombia sociedad de conocimiento: Creatividad al servicio del ser humano",
    "Eje 6: Ciudadanos del Río"
]
eje_proyecto = st.selectbox('Eje del Proyecto', eje_proyecto_options)

# Step 3
beneficiarios_proyectos_options = [
    "Mujeres",
    "Sectores LGBTIQ+",
    "Víctimas",
    "Niñas, niños y adolescentes",
    "Pueblos y comunidades étnicas",
    "Jóvenes (población entre los 14 y 28 años)",
    "Personas con discapacidad",
    "Personas mayores",
    "Migrantes",
    "Campesinos",
    "Personas que viven en la pobreza"
]
beneficiarios_proyectos = st.multiselect('Beneficiarios del Proyecto', beneficiarios_proyectos_options)

# Step 4
numero_beneficiarios = st.number_input('Número de Beneficiarios', min_value=1, format="%i")

# Step 5
inversion_proyecto = st.number_input('Inversión del Proyecto', min_value=0.0, format="%f")

if st.button('Formular proyecto'):
    with st.spinner('Formulando...'):
    # Create the prompt
        prompt = f'''Role: You are an AI assistant trained in the formulation of creative and cultural economy projects using the logical framework methodology. 
                    Please follow these steps:
                    1. Write a 500 summary of the following text {text_plandesarrollo}. Please surround this text in <raw-content> tags.
                    2. Extract from the text the main points related with culture. Please surround this version of the content with <tagged-content> tags.'''

        
                    
                    

        # Call the function
        result = create_text(prompt)

        # Print the result
        st.write(result)

       