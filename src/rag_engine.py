import os
import getpass
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_classic.chains import RetrievalQA

class FMCSAAssistant:
    def __init__(self, db_path="./data/chroma_db"):
        """
        Initialize the RAG system.
        :param db_path: Path to the ChromaDB folder.
        """
        self.db_path = db_path
        self._load_environment()
        self.vector_store = self._connect_to_db()
        self.qa_chain = self._build_chain()

    def _load_environment(self):
        """Securely load API keys."""
        load_dotenv()
        if "GOOGLE_API_KEY" not in os.environ:
            # If running in a script/app, we might not want interactive prompts,
            # but for now, we keep it as a fallback.
            print("⚠️ No .env found. Requesting key interactively...")
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter Google API Key: ")

    def _connect_to_db(self):
        """Load the existing ChromaDB."""
        print(f"📂 Loading database from {self.db_path}...")
        embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        return Chroma(
            collection_name="fmcsa_regulations",
            embedding_function=embedding_model,
            persist_directory=self.db_path
        )

    def _build_chain(self):
        """Initialize LLM and Retrieval Chain."""
        print("🧠 Connecting to Gemini 2.5 Flash...")
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )

    def ask(self, query):
        """
        Public method to ask a question.
        Returns a dictionary with 'answer' and 'sources'.
        """
        print(f"❓ Query: {query}")
        try:
            response = self.qa_chain.invoke({"query": query})
            
            # Format the output cleanly
            result = {
                "answer": response["result"],
                "sources": []
            }
            
            seen_refs = set()
            for doc in response["source_documents"]:
                source = doc.metadata.get('source', 'Unknown').split('/')[-1]
                # Fix the "Off-by-One" page error
                raw_page = doc.metadata.get('page', -1)
                human_page = raw_page + 1
                
                ref = f"{source} (Page {human_page})"
                if ref not in seen_refs:
                    result["sources"].append(ref)
                    seen_refs.add(ref)
            
            return result
            
        except Exception as e:
            return {"answer": f"Error: {str(e)}", "sources": []}