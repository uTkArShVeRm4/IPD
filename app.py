import streamlit as st
import openai
import langchain
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
import os
from io import StringIO
import PyPDF2

os.environ["OPENAI_API_KEY"] = "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"

st.title("Study help bot")

document = st.file_uploader("Upload Document Here",type='pdf')

if 'text' not in st.session_state:
	st.session_state.text = None

if st.button('Load PDF'):
    # Read the PDF file using PyPDF2
    pdf_reader = PyPDF2.PdfReader(document)
    st.session_state.text = ''
    # Loop through each page and print its contents
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        st.session_state.text+=page.extract_text()   
    st.write(len(st.session_state.text))


if st.session_state.text:

	question = st.text_input('Ask anything')

	if st.button('Ask question'):
		with st.spinner('Asking'):

			text_splitter = CharacterTextSplitter(        
					    separator = ".",
					    chunk_size = 1000,
					    chunk_overlap  = 200,
					    length_function = len,
					)


			texts = text_splitter.split_text(st.session_state.text)
			embeddings = OpenAIEmbeddings()
			docsearch = FAISS.from_texts(texts, embeddings)
			chain = load_qa_chain(OpenAI(), chain_type="stuff")
			docs = docsearch.similarity_search(question)

		st.write(chain.run(input_documents=docs, question=question))






