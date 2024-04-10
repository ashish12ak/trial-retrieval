

import streamlit as st
import json
import time
import pandas as pd
import json
from pyserini.search import LuceneSearcher
from pyserini.search import FaissSearcher



with st.sidebar:
    st.title("Retrieval of Clinical Trials")
    choice = st.radio("Navigation", ["Sparse Retrieval", "Dense Retrieval"], index=0)
    st.markdown("This application allows you to retrieve most relevant clinical trials based on your query", unsafe_allow_html=True)


# page_bg_img = """
# <style>
# [data-testid="stSidebar"] > div:first-child {
#     background-color: #FFD038;
#     color: #000000;

# }
# </style>
# """

# st.markdown(page_bg_img, unsafe_allow_html=True)


# background_image = """
# <style>
# [data-testid="stAppViewContainer"] > .main {
#   background-image: url("https://images.unsplash.com/photo-1604147706283-d7119b5b822c?q=80&w=2959&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
#   background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
#   background-position: center;  
#   background-repeat: no-repeat;
# }
# </style>
# """
# st.markdown(background_image, unsafe_allow_html=True)

@st.cache_resource()
def load_data():
    with open("/workspaces/trial-retrieval/extracted-data/extracted_data.json",'r') as f : 
            data = json.load(f)
    return data

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

def typewriter(text, speed):
    container = st.empty()
    for i in range(len(text)):
        container.text(text[:i+1])
        time.sleep(speed/100)

def dataframe_to_html_with_border(df):
    # Creatign the link
    link = f"https://clinicaltrials.gov/study/{df['nct_id'].values[0]}"

    # Replacing '\n' with '<br/>' in the 'brief_summary' and 'eligibility' columns
    df['brief_summary'] = df['brief_summary'].apply(lambda x: x.replace('\n', '<br/>'))
    df['Eligibility Criteria'] = df['Eligibility Criteria'].apply(lambda x: x.replace('\n', '<br/>')) # replace 'eligibility' with the actual column name

    # Converting DataFrame to HTML and add a border, width, and bottom margin
    df_html = df.to_html(index=False, escape=False).replace('<table', '<table style="border:2px solid black; width:100%; margin-bottom:20px;"')

    # Wrapping 'brief_summary' and 'eligibility' data in a scrollable div
    df_html = df_html.replace('<td>', '<td><div style="width: 150px;height : 150px; overflow-x: auto;">')
    df_html = df_html.replace('</td>', '</div></td>')

    # Adding the link to the DataFrame HTML
    df_html += f"<p><a href=\"{link}\" target=\"_blank\">Go to clinicaltrials.gov website for {df['nct_id'].values[0]} </a></p>"

    return df_html





if 'typewriter_text' not in st.session_state:
    st.session_state['typewriter_text'] = ''

if choice == 'Sparse Retrieval' : 

    if 'query' not in st.session_state:
        st.session_state['query'] = 'Cholera'

    if 'num_results' not in st.session_state:
        st.session_state['num_results'] = 5

    if 'typewriter_run' not in st.session_state:
        st.session_state['typewriter_run'] = False
    
    if 'retrieval_model' not in st.session_state:
        st.session_state['retrieval_model'] = 'BM25'

    page_bg_img = '''
    <style>
    body {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: cover;
    }
    </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)

    if not st.session_state['typewriter_run']:
        text = "Welcome to the interface for Sparse Retrieval !"
        speed = 5
        typewriter(text=text, speed=speed)
        st.session_state['typewriter_text'] += text + ' '

        text_1 = "Type your query in the box and you can see the most relevant clinical trials."
        speed_1 = 5
        typewriter(text=text_1, speed=speed_1)
        st.session_state['typewriter_text'] += text_1 + ' '

        text_2 = "Please wait for few seconds till the data loads in the memory."
        speed_2 = 5
        typewriter(text=text_2, speed=speed_2)



        st.session_state['typewriter_run'] = True

    query = st.text_input('Enter your query for Sparse Retrieval', value=st.session_state['query'], key='query_sparse')
    num_results = st.slider('Number of results', 1, 100, st.session_state['num_results'])
    retrieval_model = st.radio('Choose a retrieval method', ['BM25', 'Query Likelihood'], index=0)


    data = load_data()


    def top_ten_trials(query, retrieval_model ,k = num_results) : 
        
        if retrieval_model == 'Query Likelihood':
            searcher = LuceneSearcher('/workspaces/trial-retrieval/correct-anserini-dense-index/sparse_index')
            searcher.set_qld()
            hits = searcher.search(query,k = num_results+1)
            relevant_trials = [hits[i].docid for i in range(num_results+1)]
            relevant_dicts = []
        else: # Default to BM25
            searcher = LuceneSearcher('/workspaces/trial-retrieval/correct-anserini-dense-index/sparse_index')
            searcher.set_bm25()
            hits = searcher.search(query,k = num_results+1)
            relevant_trials = [hits[i].docid for i in range(num_results+1)]
            relevant_dicts = []

        
        
        count = 0
        for dictionary in data:
            num = 0
            if dictionary['nct_id'] in relevant_trials:
                
                # for key, value in dictionary.items():
                #     num+=1
                #     print(f">>> {key}: {value}\n")
                #     if num == 3 :
                #         break
                count += 1
                if count == num_results+1:
                    break
                relevant_dicts.append(dictionary)

        if count == 0:
            st.info("No relevant trials found.")
        
        if st.button('Get Results'):
            # Get the results
            results = relevant_dicts

            # Display the results in rectangular boxes
            for i, result in enumerate(results, start=0):
                keys_of_interest = ['nct_id', 'brief_title', 'brief_summary', 'Eligibility Criteria', 'Status']

                # Create a new dictionary with only the keys of interest
                filtered_result = {key: result[key] for key in keys_of_interest}

                # Convert the filtered dictionary to a DataFrame
                df = pd.DataFrame([filtered_result])
                df_html = dataframe_to_html_with_border(df)
                st.write(df_html, unsafe_allow_html=True)

            del relevant_dicts, searcher, hits, relevant_trials
        


        
    top_ten_trials(query, retrieval_model)




if choice == 'Dense Retrieval' : 

    if 'query' not in st.session_state:
        st.session_state['query'] = 'cholera'

    if 'num_results' not in st.session_state:
        st.session_state['num_results'] = 5


    query_dense = st.text_input('Enter your query for Dense Retrieval', value=st.session_state['query'], key='query_dense')
    num_results_2 = st.slider('Number of results', 1, 100, st.session_state['num_results'])

 
    data = load_data()

    @st.cache_resource()
    def get_searcher():
        return  FaissSearcher( '/workspaces/trial-retrieval/hnsw-index', 'facebook/dpr-question_encoder-multiset-base' )
    


    def top_ten_trials(query_dense, k=num_results_2):
        searcher = get_searcher()
        hits = searcher.search(query_dense, k=num_results_2+1)

        relevant_trials = [hit.docid for hit in hits]

        relevant_dicts = []
        count = 0
        for dictionary in data:
            num = 0
            if dictionary['nct_id'] in relevant_trials:
                count += 1
                if count == num_results_2+1:
                    break
                relevant_dicts.append(dictionary)

        if count == 0:
            st.info("No relevant trials found.")
        
        if st.button('Get Results'):
            # Get the results
            results = relevant_dicts

            # Display the results in rectangular boxes
            for i, result in enumerate(results, start=0):
                keys_of_interest = ['nct_id', 'brief_title', 'brief_summary', 'Eligibility Criteria', 'Status']

                # Create a new dictionary with only the keys of interest
                filtered_result = {key: result[key] for key in keys_of_interest}

                # Convert the filtered dictionary to a DataFrame
                df = pd.DataFrame([filtered_result])
                df_html = dataframe_to_html_with_border(df)
                st.write(df_html, unsafe_allow_html=True)

    top_ten_trials(query_dense)


    





