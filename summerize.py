
# THIS APP IS MADE FROM REFERENCE OF NOTEBOOK LM from google

import streamlit as st
import validators
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
#search data loader using langchain

prompt_temp= """provide the summery of following content in 500 words:
content:{text}"""

from langchain_groq import ChatGroq
#llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9,api_key='')
llm = ChatGroq(model = "groq/compound-mini",api_key="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")

prompt=PromptTemplate(template=prompt_temp)
st.set_page_config(page_title="summerize text", page_icon=":guardsman:", layout="wide")
st.title("summerize text using langchain")

user_url = st.text_input('URL')
if st.button('click to summerize'):
    if not user_url.strip():
      st.error("Please enter valid URL.")
    elif not validators.url(user_url):
       st.error('provide correct format url')
    else:
        try:
            with st.spinner('in progress'):
                if 'youtube.com' in user_url:
                  loader = YoutubeLoader.from_youtube_url(user_url,add_video_info=True)
                else:
                  loader = UnstructuredURLLoader(urls = [user_url],ssl_verify = False)
                data = loader.load()
                chain = load_summarize_chain(llm,chain_type='stuff',prompt = prompt)
                output = chain.run(data)
                st.success(output)
        except Exception as e:
           st.exception(f'Exception : {e}')
           raise
       

