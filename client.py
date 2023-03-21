import openai


class ChatClient:
    def __init__(self, prefix: str = None):
        self.prefix = prefix or "You are a helpful assistant. You are also curious."
        self.messages = [{"role": "system", "content": self.prefix}]

    def get_chat_response(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages)
        return response['choices'][0]['message']['content']
