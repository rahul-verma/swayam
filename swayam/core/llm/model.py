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
    
    def run_messages(self, messages, retain_context=True, temperature=None, functions=None, function_call="auto", return_content=True):
        if retain_context:
            self.__messages.extend(messages)
            messages = self.__messages
        if temperature is None:
            temperature = self.__temperature
            
        response = None
        if functions:
            response = self.__client.chat.completions.create(
                model=self.__model,
                messages=messages,
                temperature=temperature,
                functions=functions,
                function_call=function_call
            )
        else:
            response = self.__client.chat.completions.create(
                model=self.__model,
                messages=messages,
                temperature=temperature,
            )
    
        if return_content:
            return response.choices[0].message.content
        else:
            return response.choices[0].message 
        
    def run_prompt(self, prompt, temperature=None, functions=None, function_call="auto"):
        return self.run_messages([{"role": "user", "content": prompt.text}], temperature=temperature, functions=functions, function_call=function_call)
    
    def clear_context(self):
        self.__messages = []
        
class LLM:
    
    @classmethod
    def openai(cls, model="gpt-4o-mini", temperature=0):
        return _OpenAIModel(model=model, temperature=temperature)
        

