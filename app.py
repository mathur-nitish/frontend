import streamlit as st
import requests
import json

def post_data(json_data):
  try:
    response = requests.post("https://ra2111026030216.azurewebsites.net/bfhl", json=json_data)
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    st.error(f"An error occurred: {e}")
    return None

# GET
def get_data():
  try:
    response = requests.get("https://ra2111026030216.azurewebsites.net/bfhl")
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    st.error(f"An error occurred: {e}")
    return None

st.title("Bajaj Finserv API Assigment")

if 'response_data' not in st.session_state:
  st.session_state['response_data'] = None
if 'selected_sections' not in st.session_state:
  st.session_state['selected_sections'] = []

st.subheader("POST Request")
json_input = st.text_area("Enter JSON data:", '{"data": []}')
try:
  data = json.loads(json_input)
except json.JSONDecodeError:
  st.error("Invalid JSON format.")
  data = None

if st.button("Submit POST Request (use filters to get see response)"):
  if data:
    with st.spinner('Sending POST request...'):
      response = post_data(data)
      if response:
        st.session_state['response_data'] = response
    
        st.session_state['selected_sections'] = []

def handle_section_selection(selected_sections):
  st.session_state['selected_sections'] = selected_sections


# Multiselect
section_options = ["Alphabets", "Numbers", "Highest Alphabet"]
selected_sections = st.multiselect("Select sections to display:", section_options, key="section_selection")

handle_section_selection(selected_sections)

if st.session_state['response_data']:
  response = st.session_state['response_data']

  if st.session_state['selected_sections']:
    for section in st.session_state['selected_sections']:
      section_data = response.get(section.lower(), []) 
      st.write(f"{section}:")
      st.write(section_data)

# Section for GET request
st.subheader("GET Request")
if st.button("Fetch Operation Code"):
  with st.spinner('Sending GET request...'):
    response = get_data()
    if response:
      st.write("Response from API:")
      st.json(response)
