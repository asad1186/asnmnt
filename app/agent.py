from app.prompts import AGENT_SYSTEM_PROMPT,decision_prompt

class AIAgent:
    def __init__(self, llm_client, tools, memory):
        self.llm = llm_client
        self.tools = tools
        self.memory = memory


    def decide_and_answer(self, query: str, session_id: str = None):

        decision_messages = [
            {"role": "system", "content": decision_prompt},
            {"role": "user", "content": query}
]
        decision = self.llm.chat(decision_messages).strip().lower()
        print('decision:',decision)
        # -------- 2️⃣ Prepare answer prompt --------
        history = self.memory.get(session_id) if session_id else []

        answer_messages = [
            {"role": "system", "content": AGENT_SYSTEM_PROMPT}
        ] + history

        sources = []
    
        if decision == "tool":
            tool_result = self.tools["retrieve_docs"](query)
            context = "\n".join(tool_result["context"])
            sources = tool_result["sources"]

            answer_messages.append({
                "role": "user",
                "content": (
                    "Use the following internal document context to answer the question.\n\n"
                    f"Context:\n{context}\n\n"
                    f"Question: {query}"
                )
            })
        else:
            answer_messages.append({
                "role": "user",
                "content": query
            })

        # -------- 4️⃣ Final answer --------
        final_answer = self.llm.chat(answer_messages)

        # -------- 5️⃣ Save memory --------
        if session_id:
            self.memory.add(session_id, "user", query)
            self.memory.add(session_id, "assistant", final_answer)

        return {
            "answer": final_answer,
            "sources": sources
        }
