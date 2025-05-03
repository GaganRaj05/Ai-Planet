from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from app.core.config import GROQAI_API_KEY

splitter = RecursiveCharacterTextSplitter(  
    chunk_size=500, 
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""] 
)    
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", encode_kwargs={'normalize_embeddings':True})
llm = ChatGroq(
        api_key=GROQAI_API_KEY,
        temperature=0.5,
        model_name="llama3-8b-8192", 
    )

async def answer_question(pdf_text: str, question: str):
    docs = splitter.create_documents([pdf_text])

    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever()


    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    result = qa_chain({"query": question})
    return result["result"]
