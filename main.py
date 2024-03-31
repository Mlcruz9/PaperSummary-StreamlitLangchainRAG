import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
# para convertir response que es un objeto a json
import json

from utils import extraer_secciones_del_texto
from openai import OpenAI
import tempfile
# import os
# import base64

st.markdown(
    '''
    <style>
    .streamlit-expanderHeader {
        background-color: #E0FFFF;
        color: black; # Adjust this for expander header color
    }
    .streamlit-expanderContent {
        background-color: #ADD8E6;
        color: black; # Expander content color
    }
    </style>
    ''',
    unsafe_allow_html=True
)

with st.sidebar:
    api_key_received = st.text_input("OpenAI API Key", key="gpt_api_key", type="password")
    client = OpenAI(api_key= api_key_received)

st.title("📝 Paper Summary Generator")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md", "pdf"))

# Coloca cuantos puntos clave quieras en la lista numerada en un drop-down
st.write("### Key Points")
key_points = st.selectbox(
    "Select the number of key points",
    [5, 10, 15, 20, 25, 50],
    index=1,
    format_func=lambda x: f"{x} points",
)

question = st.text_input(
    "Ask something about the article",
    placeholder="Aditional info of the paper.",
    disabled=not uploaded_file,
)


if uploaded_file and question and not api_key_received:
    st.info("Please add your OpenAI API key to continue.")

if uploaded_file and question:
    if uploaded_file.name.endswith(".pdf"):
        with st.spinner('Processing PDF...'):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                    tmpfile.write(uploaded_file.getvalue())
                    file_path = tmpfile.name

                loader = PyPDFLoader(file_path)
                pages = loader.load_and_split()
                
                # Opcional: Crear un índice FAISS con embeddings de OpenAI para búsquedas en el documento
                # faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings(openai_api_key = client.api_key))
                
                st.success('PDF processed successfully!')

                article = pages

                response = client.chat.completions.create(
                    model="gpt-4-turbo-preview", #gpt-4-turbo-preview,  # Asegúrate de que el nombre del modelo esté correctamente especificado aquí
                    messages=[
                    {"role":"system", "content": f"You are an expert making paper summaries. After reading an article, provide a summary by listing {key_points} of the key points. You will receive a question from the user, \
                                give a lot of importance to this question but always looking for the response in the paper. \
                                The summary should be concise and formatted as a numbered list. The answer is in spanish. Also give the user in the end of an\
                    item of the numerated list in which page the information was found, with the format of just the number of the page en the end of the item. Give just enumerated list, not intro or conclusion."},
                    {"role":"user", "content": f"Here's a paper:\n\n{article}\n\Question: {question}"}
                    ],
                    max_tokens=1000,  # Estos son los tokens de texto de salida máximos
                    stop= str(key_points + 1) + ".",  # Ajusta los delimitadores de parada según sea necesario
                    temperature=0.5,  # Ajusta la creatividad según sea necesario, mientras más alto más creativo
                    )
                
                # Extraer las secciones del texto
                secciones = extraer_secciones_del_texto(response.choices[0].message.content)

                #  # Aquí puedes permitir al usuario realizar búsquedas en el documento o simplemente procesar todo el texto.
                # query = st.text_input("Ask something about the article", placeholder="E.g., main findings of the paper.")
                # if query:
                #     docs = faiss_index.similarity_search(query, k=2)
                #     for doc in docs:
                #         st.write(f"Page {doc.metadata['page']}:", doc.page_content[:300])

                # Mostrar la respuesta
                st.write("### Answer")

                # Mostrar las secciones en un desplegable
                for numero, seccion in enumerate(secciones):
                    with st.expander(f"#{numero + 1}. {seccion['titulo']}"):
                        st.write(seccion['pagina'])
                    
            except Exception as e:
                st.error(f"Failed to process PDF: {e}")

    else:
        article = uploaded_file.getvalue().decode("utf-8")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Asegúrate de que el nombre del modelo esté correctamente especificado aquí
            messages=[
           {"role":"system", "content": f"You are an expert making paper summaries. After reading an article, provide a summary by listing {key_points} of the key points. You will receive a question from the user, \
                                give a lot of importance to this question but always looking for the response in the paper. \
                                The summary should be concise and formatted as a numbered list. The answer is in spanish. Also give the user in the end of an\
                    item of the numerated list in which page the information was found, with the format of just the number of the page en the end of the item. Give just enumerated list, not intro or conclusion."},
            {"role":"user", "content": f"Here's a paper:\n\n{article}\n\Aditional info: {question}"}
            ],
            max_tokens=1000,  # Estos son los tokens de texto de salida máximos
            stop= str(key_points + 1) + ".",  # Ajusta los delimitadores de parada según sea necesario
            temperature=0.5,  # Ajusta la creatividad según sea necesario
        )
        
        # Mostrar la respuesta
        st.write("### Answer")

        # Mostrar las secciones en un desplegable
        st.write(response.choices[0].message.content)