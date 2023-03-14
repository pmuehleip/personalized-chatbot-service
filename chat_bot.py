import openai

MODEL = "gpt-3.5-turbo-0301"

class ChatBot:
    def __init__(self, role="", greeting=""):
        self.role = role
        self.messages = []
        if self.role:
            self.messages.append({"role": "system", "content": role})
        if greeting:
            self.messages.append({"role": "assistant", "content": greeting})
    
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self):
        completion = openai.ChatCompletion.create(model=MODEL, messages=self.messages)
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        # print(completion.usage)
        print(completion)
        return completion.choices[0].message.content