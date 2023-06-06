import streamlit as st
import requests
import json
import pprint
from docx import Document
from io import BytesIO


# Function to read .txt file
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Loading the .txt files
text_convocatoria = read_txt_file('txts/convocatoria_cocrea.txt')
text_derechosculturales = read_txt_file('txts/derechosculturales.txt')
text_plandesarrollo = read_txt_file('txts/plandesarrollo.txt')

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
        "temperature": 0.6,
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
    "General",
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
        prompt_ml = f'''Role: You are an AI assistant trained in the formulation of creative and cultural economy projects using the logical framework methodology. 
                    Your answers should always be in Spanish. Always write the number of the task before you answer. 
                    For example: 
                    Task 7: ...
                    Task 8: ...
                    Do the following taks:
                    
                    Task 1: Read the following documents {text_convocatoria} and {contexto_proyecto} to understand the context of the project. 
                    Do not write anything after performing this task. 
                    
                    Task 2: Analyze the following objectives {objetivo_proyecto} to understand the objectives of the project.
                    Do not write anything after performing this task.

                    Task 3: Analize the goals of the project that are {metricas_exito}.
                    Do not write anything after performing this task.

                    Task 4: Analyze the budget assign for the project {inversion_proyecto} in Colombian Pesos.
                    Do not write anything after performing this task.

                    Task 5: Take into account that {numero_beneficiarios} people will be positively impacted by the project.
                    Do not write anything after performing this task.

                    Task 6: The project is aligned with the following axis of the call {eje_proyecto}.
                    Do not write anything after performing this task.

                    Task 7: Write the detailed logical framework matrix as a plain text document for the project 
                    called {nombre_proyecto} that will benefit the population of {beneficiarios_proyectos}. 

                    Task 8: Read {text_derechosculturales} choose one of the rights according to the task 7. 
                    Write the right you choose and the explanation of how the project is related with this right and how it have a positive benefit.
                    
                    Task 9: write a paragraph describing the antecedents and justification of the project

                    Task 10: Write a list of the cross functional activities of the project

                    Task 11: Write a detailed description of the project and its impact in less than 2000 characters

                    Task 12: Estimate how many people will be employed in the project taking into account the budget and objectives. 
                    And create a table with 2 columns: Column 1 Number of People, Column 2 Profile of the person

                    Task 13: Write a description of the beneficiaries of the project
                    
                    '''               
                    

        # Call the function
        marco_logico = create_text(prompt_ml)

        # Print the result
        st.write(marco_logico)

       