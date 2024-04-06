# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import time



    



with st.sidebar:
    st.title("Retrieval of Clinical Trials")
    choice = st.radio("Navigation", ["Sparse Retrieval", "Dense Retrieval"], index=0)
    st.info("This application allows you to retrieve most relevant clinical trials based on your query")

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
  background-image: url("https://images.unsplash.com/photo-1614850523011-8f49ffc73908?q=80&w=2970&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
  background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
  background-position: center;  
  background-repeat: no-repeat;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')
  

if choice == 'Sparse Retrieval' : 


    page_bg_img = '''
    <style>
    body {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: cover;
    }
    </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)
    

    text = "Welcome to the interface for Sparse Retrieval !"
    speed = 10
    typewriter(text=text, speed=speed)

    text_1 = "Type your query in the box and you can see the most relevant clinical trials in the sidebar."

    speed_1 = 10
    typewriter(text=text_1, speed=speed_1)

    







    


