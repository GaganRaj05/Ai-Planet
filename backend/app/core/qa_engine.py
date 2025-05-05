#qa engine to answer the questions from the ask-questions route
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from app.core.config import GROQAI_API_KEY

#split the document data into smaller chunk discarding characters like \n \n\n
splitter = RecursiveCharacterTextSplitter(  
    chunk_size=500,  #Maximum characters per chunk
    chunk_overlap=100, #characters overlapping between chunks
    separators=["\n\n", "\n", " ", ""] #splitting separators
)    
#huggingfaceembeddings class used to generate text embeddings using hugging face model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", encode_kwargs={'normalize_embeddings':True})
#llm config for user interaction
llm = ChatGroq(
        api_key=GROQAI_API_KEY,
        temperature=0.5,
        model_name="llama3-8b-8192", 
    )

#helper function to interact with the model
async def answer_question(pdf_text: str, question: str):
    #create small chunks of pdf text 
    docs = splitter.create_documents([pdf_text])
    #convert text chunk into embeddings
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever()

    #combines retrieval and generation
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, 
        retriever=retriever, #faiss retriever
        return_source_documents=True
    )
    #return the result given by the model
    result = qa_chain({"query": question})
    return result["result"]
