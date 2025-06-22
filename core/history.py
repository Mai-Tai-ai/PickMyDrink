
class History:

    def __init__(self):
        self.messages = []

    def system(self, message):
        self.add("system", message)

    def assistant(self, message):
        self.add("assistant", message)

    def user(self, message):
        self.add("user", message)

    def add(self, role, message):
        self.messages.append({'role': role, "content": message})

    def count(self):
        return len(self.messages)
