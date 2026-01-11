import os
import faiss
import pickle
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-3-small"
INDEX_PATH = "embeddings/faiss.index"
DOCS_PATH = "embeddings/docs.pkl"

def load_documents(folder_path="data/documents"):
    docs = []
    for file in os.listdir(folder_path):
        with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
            docs.append({
                "text": f.read(),
                "source": file
            })
    return docs


def create_faiss_index():
    docs = load_documents()
    texts = [d["text"] for d in docs]

    embeddings = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    ).data

    vectors = [e.embedding for e in embeddings]
    dimension = len(vectors[0])

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors).astype("float32"))

    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(DOCS_PATH, "wb") as f:
        pickle.dump(docs, f)


def search(query, k=2):
    index = faiss.read_index(INDEX_PATH)

    with open(DOCS_PATH, "rb") as f:
        docs = pickle.load(f)

    query_embedding = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[query]
    ).data[0].embedding

    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"), k
    )

    results = []
    for i in indices[0]:
        results.append(docs[i])

    return results
