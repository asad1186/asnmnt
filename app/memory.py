class SessionMemory:
    def __init__(self):
        self.sessions = {}

    def get(self, session_id: str):
        return self.sessions.get(session_id, [])

    def add(self, session_id: str, role: str, content: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append({
            "role": role,
            "content": content
        })
