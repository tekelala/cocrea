
import streamlit as st
import requests
import json
import re
from docx import Document
from io import BytesIO
import pandas as pd

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
        "model": "claude-2.0",
        "max_tokens_to_sample": 10000,
        "temperature": 0.6,
        "stop_sequences": ["

Human:"]
    }

    # Make a POST request to the Claude API
    try {
        response = requests.post(api_url, headers=headers, data=json.dumps(body))
        response.raise_for_status()
    } catch requests.exceptions.HTTPError as errh {
        st.error(f"HTTP Error: {errh}")
    } catch requests.exceptions.ConnectionError as errc {
        st.error(f"Error Connecting: {errc}")
    } catch requests.exceptions.Timeout as errt {
        st.error(f"Timeout Error: {errt}")
    } catch requests.exceptions.RequestException as err {
        st.error(f"Something went wrong: {err}")
    } catch Exception as e {
        st.error(f"Unexpected error: {e}")
    }

    # Extract Claude's response from the JSON response
    result = response.json()

    # Return Claude's response as a dictionary
    return result

# Streamlit App

st.title('Formulador de proyectos')

# Initialization
if "project_details" not in st.session_state:
    st.session_state["project_details"] = {}
if "answers" not in st.session_state:
    st.session_state["answers"] = {}
if "step" not in st.session_state:
    st.session_state["step"] = 0

# Define project details
project_details = {
    "nombre_proyecto": "Nombre del Proyecto",
    "nombre_titular_proyecto": "Nombre del Titular del proyecto",
    "contexto_proyecto": "Contexto del Proyecto",
    "objetivo_proyecto": "Objetivo del Proyecto",
    "metricas_exito": "Metricas de Exito",
    "experiencia_titular": "Experiencia Titular",
    "eje_proyecto": "Eje del Proyecto",
    "beneficiarios_proyectos": "Beneficiarios del Proyecto",
    "numero_beneficiarios": "Número de Beneficiarios",
    "inversion_proyecto": "Inversión del Proyecto",
}

# Collect project details from user
for detail, prompt in project_details.items():
    if detail not in st.session_state["project_details"]:
        st.session_state["project_details"][detail] = st.text_input(prompt)

# Once all details are collected, process them
if len(st.session_state["project_details"]) == len(project_details):
    if st.button('Formular proyecto'):
        with st.spinner('Formulando...'):
             # Create the prompt
            prompt_1 = f'''Role: You are an AI assistant trained in the formulation of creative and cultural economy projects using the logical framework methodology. Give your answers in Spanish.
                        Always write the number of the task before you answer. 
                        For example: 
                        Task 7: ...
                        Task 8: ...
                        Do the following taks:
                        
                        Task 1: Read the following documents {text_convocatoria} and {contexto_proyecto} to understand the context of the project. Do not write anything after performing this task. 
                        
                        Task 2: Analyze the following objectives {objetivo_proyecto} to understand the objectives of the project. Do not write anything after performing this task.
                        
                        Task 3: Analize the goals of the project that are {metricas_exito}. Do not write anything after performing this task.
                        
                        Task 4: Analyze the budget assign for the project {inversion_proyecto} in Colombian Pesos. Do not write anything after performing this task.
                        
                        Task 5: Take into account that {numero_beneficiarios} people will be positively impacted by the project. Do not write anything after performing this task.
                        
                        Task 6: The project is aligned with the following axis of the call {eje_proyecto}.Do not write anything after performing this task.
                        
                        Task 7: Write the detailed logical framework matrix as a plain text document for the project called {nombre_proyecto} that will benefit the population of {beneficiarios_proyectos}. The answer should have the following format: 
                                Task 7: 
                                1. The project's goal, purpose and outputs.
                                2. The key assumptions and risks that could influence the project's success.
                                3. The objectively verifiable indicators used to measure achievement of the goal, purpose and outputs.
                                4. The means of verification for monitoring and evaluating the indicators.
                                5. Narrative summary: Describes the project's goal, purpose, outputs and activities.
                                6. Indicators: Specifies the measures to assess whether the objective of each level of the project hierarchy is achieved.
                                7. Means of verification: Specifies how and from where data on the indicators will be obtained.
                                8. Assumptions: Lists key assumptions which must hold true for the project to succeed but are outside its control.
                        '''
            
            # Call the function for the first batch of tasks and extract the answers
            marco_logico = create_text(prompt_1)
            # extracted_marco_logico = marco_logico
            
            prompt_2 = f'''Role: You are an AI assistant trained in the formulation of creative and cultural economy projects using the logical framework methodology. Give your answers in Spanish.
                        Always write the number of the task before you answer. 
                        For example: 
                        Task 7: ...
                        Task 8: ...
                        Do the following taks:

                        Task 1: Read and analyze the followinw logical framework matrix {marco_logico}. Do not write anything after performing this task.
                        
                        Task 2: Write a paragraph describing the antecedents and justification of the project
                        
                        Task 3: Write a list of the cross functional activities of the project
                        
                        Task 4: Write a detailed description of the project and its impact in less than 2000 characters.
                        
                        Task 5: Estimate how many people will be employed in the project taking into account the budget and objectives. And create a table with 2 columns: Column 1 Number of People and Column 2 Profile of the person.
                        
                        Task 6: Write a description of the beneficiaries of the project.

                        Task 7: Read {text_derechosculturales} choose one of the rights according to the task 7. Write the right you choose and the explanation of how the project is related with this right and how it have a positive benefit.
                        
                        Task 8: Write "Tekelala".
                        '''             
                        

            # Call the function for the second batch of tasks and extract the answers
            info_proyecto = create_text(prompt_2)
            #extracted_info_proyecto = info_proyecto

            # Extract the tasks
            match = re.search(r"Task 7:(.*?)(Task 8:|$)", marco_logico["completion"], re.DOTALL)
            if match is not None:
                task_7 = match.group(1).strip()
            else:
                task_7 = "Task 7 not found in text"

            match = re.search(r"Task 2:(.*?)(Task 3:|$)", info_proyecto["completion"], re.DOTALL)
            if match is not None:
                task_1 = match.group(1).strip()
            else:
                task_1 = "Task 1 not found in text"

            match = re.search(r"Task 3:(.*?)(Task 4:|$)", info_proyecto["completion"], re.DOTALL)
            if match is not None:
                task_2 = match.group(1).strip()
            else:
                task_2 = "Task 2 not found in text"

            match = re.search(r"Task 4:(.*?)(Task 5:|$)", info_proyecto["completion"], re.DOTALL)
            if match is not None:
                task_3 = match.group(1).strip()
            else:
                task_3 = "Task 3 not found in text"

            match = re.search(r"Task 5:(.*?)(Task 6:|$)", info_proyecto["completion"], re.DOTALL)
            if match is not None:
                task_4 = match.group(1).strip()
            else:
                task_4 = "Task 4 not found in text"

            match = re.search(r"Task 6:(.*?)(Task 7:|$)", info_proyecto["completion"], re.DOTALL)
            if match is not None:
                task_5 = match.group(1).strip()
            else:
                task_5 = "Task 5 not found in text"

            match = re.search(r"Task 7:(.*?)(Task 8:|$)", info_proyecto["completion"], re.DOTALL)
            if match is not None:
                task_6 = match.group(1).strip()
            else:
                task_6 = "Task 6 not found in text"

            # Print the result
            #st.write(marco_logico)
            #st.write(info_proyecto)
            st.header("Proyecto estructurado con metodologia Marco Lógico")
            st.write(task_7)
            st.header("Antecedentes y justificación del proyecto")
            st.write(task_1)
            st.header("Actividades transversales del proyecto:")
            st.write(task_2)
            st.header("Descripción detallada e impacto del proyecto")
            st.write(task_3)
            st.header("Número de personas que trabajarán en el proyecto y sus cargos")
            st.write(task_4)
            st.header("Breve descripción de los beneficiarios")
            st.write(task_5)
            st.header("Explicación de cómo contribuye el proyecto al elemento o condición del derecho cultural que se seleccionó")
            st.write(task_6)
        

                # Call the function to get the answers and store them
            st.session_state["answers"] = create_text(prompt)
            st.session_state["step"] = 1

# Display the answers and allow user to ask for more information
if st.session_state["step"] == 1:
    st.header("Here are the answers to your questions:")
    st.write(st.session_state["answers"])

    user_prompt = st.text_input("Do you want to ask for more information about the answers?")

    if user_prompt:
        with st.spinner('Processing your request...'):
            # Call the function to get the answer to the new prompt and store it
            st.session_state["answers"] = create_text(user_prompt)
