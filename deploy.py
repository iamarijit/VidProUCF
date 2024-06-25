import streamlit as st
import os

from utils.meta import add_spaces_before_uppercase
from utils.db import get_table, fetch_data

@st.experimental_dialog("Playing Video", width="large")
def show_video(path, gender, location, action, duration):
    sections = st.columns(2)
    sections[0].write(f'Activity : {action}')
    sections[1].write(f'Duration : {duration}s')
    sections[0].write(f'Gender : {gender}')
    sections[1].write(f'Location : {location}')
    st.video(path, autoplay=True)

root = os.path.join(os.getcwd(), "UCF-101")
conn, table = get_table()
actions = [each_action for each_action in os.listdir(root) if os.path.isdir(os.path.join(root, each_action))]
actions = map(add_spaces_before_uppercase, actions)

st.markdown("<h1 style='text-align: center;'>Video Search Tool (UCF101)</h1>", unsafe_allow_html=True)

location_filter = st.selectbox("Location", ("Indoor", "Outdoor"), index=None, placeholder="Choose Location")
gender_filter = st.selectbox("Gender", ("Male", "Female"), index=None, placeholder="Choose Gender")
action_filter =  st.selectbox("Action", actions, index=None, placeholder="Choose Action")

st.write('')
st.write('')

results = fetch_data(conn, table, location_filter, gender_filter, action_filter)[:5]
if len(results) > 0:
    st.write('### Videos Found')
    st.write('')
    sections = st.columns(2)

    for key, data in enumerate(results):
        path = data['file_name']
        action = data['action']
        gender = data['gender'].replace(',', '/')
        location = data['location']
        duration = data['duration']
        label = path.split('/')[-1]

        with sections[key % 2]:
            if st.button(label, key=key):
                show_video(path, gender, location, action, duration)
else:
    st.write('### No Videos Found')
