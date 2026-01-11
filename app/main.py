from fastapi import FastAPI
from app.schemas import AskRequest, AskResponse
from app.agent import AIAgent
from app.memory import SessionMemory
from app.tools import retrieve_docs
from app.llm_client import OpenAIClient

app = FastAPI(title="AI Agent with RAG")

# ---- Initialize core components ----
llm_client = OpenAIClient()
memory = SessionMemory()
tools = {
    "retrieve_docs": retrieve_docs
}

agent = AIAgent(
    llm_client=llm_client,
    tools=tools,
    memory=memory
)

# ---- API Endpoint ----
@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    result = agent.decide_and_answer(
        query=request.query,
        session_id=request.session_id
    )

    return AskResponse(
        answer=result["answer"],
        sources=result["sources"]
    )
