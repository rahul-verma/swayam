import openai

class _OpenAIModel:
    
    def __init__(self, model, temperature):
        self.__model = model
        self.__client = openai.OpenAI()
        self.__temperature = temperature
        self.__messages = []
        
    def send(self, prompt):
        self.__messages.append({"role": "user", "content": prompt.text})
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=self.__messages,
            temperature=self.__temperature
        )
        return response.choices[0].message.content
    
    def clear_context(self):
        self.__messages = []
        
class LLM:
    
    @classmethod
    def openai(cls, model="gpt-4o-mini", temperature=0):
        return _OpenAIModel(model=model, temperature=temperature)
        

