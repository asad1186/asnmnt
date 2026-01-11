from app.rag import search

def retrieve_docs(query: str):
    results = search(query)

    return {
        "chunks": [r["text"] for r in results],
        "sources": [r["source"] for r in results]
    }
