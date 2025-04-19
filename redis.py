import uuid


class SimpleSessionManager:
    def __init__(self):
        self.sessions = {}  # Dictionnaire pour stocker les sessions

    def create_session(self, user_id, role):
        token = str(uuid.uuid4())
        self.sessions[token] = {"user_id": user_id, "role": role}
        return token

    def get_session(self, token):
        return self.sessions.get(token)

    def delete_session(self, token):
        if token in self.sessions:
            del self.sessions[token]