import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()

DOCS_PATH = "data/documents"
EMBED_DIR = "embeddings"

EMBEDDING_MODEL = "text-embedding-3-large"



def build_faiss():
    print("🔧 Building FAISS index...")

    loader = DirectoryLoader(
        path=DOCS_PATH,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()
    print(f"📄 Loaded {len(documents)} pages")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    docs = text_splitter.split_documents(documents)
    print(f"✂️ Total chunks: {len(docs)}")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = FAISS.from_documents(docs, embeddings)

    os.makedirs(EMBED_DIR, exist_ok=True)
    vectorstore.save_local(EMBED_DIR)

    print("✅ FAISS built and saved successfully")


def load_or_build_faiss():
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    if os.path.exists(EMBED_DIR):
        print("📦 Loading existing FAISS index...")
        return FAISS.load_local(
            EMBED_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        build_faiss()
        return FAISS.load_local(
            EMBED_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )



def search(query, k=2):
    # ✅ Usage
    vectorstore = load_or_build_faiss()
    results = vectorstore.similarity_search(query, k=3)
    contexts = []
    sources = []

    for doc in results:
        contexts.append(doc.page_content)
        sources.append({
            "document": doc.metadata.get("source"),
            "page": doc.metadata.get("page") + 1  # human-readable
        })
    sources = list(
        set(
            os.path.basename(i["document"])
            for i in sources
            if i.get("document")
        )
    )

    return {'context':contexts,
            'sources':sources}
