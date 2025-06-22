import openai

class Chat:
    # Build logic here to start a new chat.
    # A new chat starts with a blank context. system prompt should be decided about.
    pass

class _OpenAIModel:
    
    def __init__(self, model, temperature):
        self.__model = model
        self.__client = openai.OpenAI()
        self.__temperature = temperature
        self.__messages = []
        
    def run_prompt(self, prompt, temperature=None):
        if temperature is None:
            temperature = self.__temperature
        self.__messages.append({"role": "user", "content": prompt.text})
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=self.__messages,
            temperature=self.__temperature
        )
        return response.choices[0].message.content
    
    def run_messages(self, messages, retain_context=True, temperature=None):
        if retain_context:
            self.__messages.extend(messages)
            messages = self.__messages
        if temperature is None:
            temperature = self.__temperature
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            temperature=self.__temperature
        )
        return response.choices[0].message.content       
    
    def clear_context(self):
        self.__messages = []
        
class LLM:
    
    @classmethod
    def openai(cls, model="gpt-4o-mini", temperature=0):
        return _OpenAIModel(model=model, temperature=temperature)
        

