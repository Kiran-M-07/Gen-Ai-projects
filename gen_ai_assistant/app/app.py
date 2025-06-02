import streamlit as st
import pandas as pd 
import json
import re 
from rag_chat import chat

# @st.cache_resource
# def load_():
#     return chat()

# rag = load_()

chat_instance = chat()

# import data
df = pd.read_csv("/Users/kiranm/Desktop/gen_ai_assistant/app/data/insights_meta.csv")
ids = df["pubmed_id"].tolist()


# --- Layout with Two Columns ---

# print(f"search : {search_id}\n")
# print(f"id_list : {ids}")
# print(type(ids[1])," -- ", type(search_id)) 

# --- CSS for gradient box ---
custom_css = """
<style>
.gradient-box {
    border: 3px solid;
    border-image: linear-gradient(45deg, black, blue) 1;
    border-radius: 15px;
    padding: 20px;
    background-color: #f9f9f9;
    margin-top: 10px;
    word-wrap: break-word;
}
.gradient-title {
    border: 4px solid;
    border-image: linear-gradient(45deg, black, blue) 1;
    border-radius: 20px;
    padding: 20px;
    font-size: 30px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
    background-color: #f9f9f9;
    color: #000000;
}
.gradient-border {
    border: 3px solid;
    border-image: linear-gradient(45deg, black, blue) 1;
    border-radius: 15px;
    padding: 15px;
    margin-top: 10px;
    background-color: #f9f9f9;
    color: #000000;
}
textarea {
    border-radius: 10px !important;
}
input[type="text"] {
    border: 3px solid;
    border-image: linear-gradient(45deg, black, blue) 1;
    border-radius: 10px;
    padding: 10px;
}
</style>
"""

# --- Title ---
st.markdown('<div class="gradient-title"><h1>Biomedical Research Insights Explorer</h1></div>', unsafe_allow_html=True)


# --- Text Input ---
search_id = st.text_input("Enter PUBMED_ID", help="Search for a specific ID to view associated biomedical insights")

# --- Create columns with spacing for a divider ---
col1, col2 = st.columns([5,3])

    
if search_id:
    search_id = int(search_id)
    if search_id in df["pubmed_id"].values:
        record = df[df["pubmed_id"] == search_id].iloc[0]
        with col1:
            st.markdown(custom_css, unsafe_allow_html=True)
            content_html = f"""
            <div class="gradient-box">
                <h4>Title</h4>
                <p>{record['title']}</p>
                <h4>Abstract</h4>
                <p>{record['abstract']}</p>
                <h4>Summary</h4>
                <p>{record['summary']}</p>
            </div>
            """
            st.markdown(content_html, unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="gradient-border"><h4>Ask a Question</h4>', unsafe_allow_html=True)
            user_question = st.text_area("", placeholder="Type your question here...", height=200)
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("Submit Question"):
                if user_question.strip():
                 
                    response = chat_instance.answer_(question = user_question)  
                    st.write("Response:", response)
    else:
        with col1:
            st.warning(f"No data found for ID: {search_id}")