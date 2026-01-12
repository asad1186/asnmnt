from app.rag import search

def retrieve_docs(query: str):
    results = search(query)

    return results