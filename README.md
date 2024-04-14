# 📄 Paper Summary Generator App

## 🌟 Features
- **Upload PDFs**: Allows users to upload research papers in PDF format.
- **Generate Summaries**: Automatically extracts and lists the key points from the paper.
- **Question-based Insights**: Users can ask specific questions to get detailed insights about the content.
- **Streamlit UI**: Easy-to-use interface built with Streamlit.
- **AI Powered**: Utilizes OpenAI's models to process and summarize papers.

## 🔧 Installation
To run the app, you need to install the required Python libraries:
```bash
pip install streamlit langchain-openai langchain-community
```

## 🚀 How to Use
1. **Start the App**:
   ```bash
   streamlit run app.py
   ```
2. **Upload a Paper**: Click on the upload area to add your PDF file.
3. **Enter OpenAI API Key**: Provide your API key in the sidebar to enable processing.
4. **Select Key Points**: Choose how many key points you want from the dropdown.
5. **Ask a Question**: Type a specific question to get targeted insights from the paper.

## ⚙️ Code Overview
- **PDF Processing**: Uses `PyPDFLoader` to read PDF files.
- **Text Summarization**: Employs `OpenAIEmbeddings` and `FAISS` for text analysis and summarization.
- **Interactive UI**: Built with Streamlit, featuring expanders and input boxes for a clean user experience.

## 📋 Example Output
The app provides a structured summary in a numbered list, pinpointing the locations of key points within the document.