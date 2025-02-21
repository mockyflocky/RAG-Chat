import streamlit as st
import os
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Ensure data directory exists
pdfs_directory = './data/'
os.makedirs(pdfs_directory, exist_ok=True)

# Streamlit UI
st.title("PDF Chat & AI Assistant")

# Model selection
available_models = [
    "mistral:latest",
    "nomic-embed-text:latest",
    "llama3.2:latest",
    "deepseek-r1:1.5B",
    "llama3.2:3b",
    "llama3:latest",
    "deepseek-r1:7b"
]
selected_model = st.selectbox("Pilih Model AI:", available_models)

# Initialize model and vector store
embeddings = OllamaEmbeddings(model=selected_model)
vector_store = InMemoryVectorStore(embeddings)
model = OllamaLLM(model=selected_model)

# Prompt template
template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

def upload_pdf(file):
    with open(os.path.join(pdfs_directory, file.name), "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    return loader.load()

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return text_splitter.split_documents(documents)

def index_docs(documents):
    vector_store.add_documents(documents)

def retrieve_docs(query):
    return vector_store.similarity_search(query)

def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": context})

def chat_with_ai(question):
    return model.invoke(question)

mode = st.radio("Pilih Mode:", ["Mode Baca PDF", "Mode Curhat"])

if mode == "Mode Baca PDF":
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    if uploaded_file:
        upload_pdf(uploaded_file)
        documents = load_pdf(os.path.join(pdfs_directory, uploaded_file.name))
        chunked_documents = split_text(documents)
        index_docs(chunked_documents)

        question = st.chat_input()
        if question:
            st.chat_message("user").write(question)
            related_documents = retrieve_docs(question)
            answer = answer_question(question, related_documents)
            st.chat_message("assistant").write(answer)

elif mode == "Mode Curhat":
    question = st.chat_input("Tanyakan apa saja!")
    if question:
        st.chat_message("user").write(question)
        answer = chat_with_ai(question)
        st.chat_message("assistant").write(answer)
