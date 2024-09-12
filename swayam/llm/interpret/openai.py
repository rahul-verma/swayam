# This file is a part of Swayam
# Copyright 2015-2024 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, time
from .base import LLMClient

class OpenAIClient(LLMClient):
    def __init__(self, model, *, temperature:float=0, **kwargs):
        super().__init__(provider="openai", model=model, temperature=temperature, **kwargs)
        
    def _create_client(self):
        from openai import OpenAI
        self._client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
    def execute_messages(self, *, messages, out_template=None, tools=None):
        from pprint import pprint
        from swayam.llm.phase.prompt.response import LLMResponse
        import openai
        if tools:
            tools =[tool.definition for tool in tools]

        error_content = ""
        for attempt in range(5):  # Retry up to 5 times
            
            try:
                response = None
                if out_template is None:
                    response = self._client.chat.completions.create(
                        model=self.model_name,
                        messages=messages,
                        tools=tools,
                        **self._model_kwargs
                    )
                else:
                    response = self._client.beta.chat.completions.parse(
                        model=self.model_name,
                        messages=messages,
                        response_format=out_template.model,
                        **self._model_kwargs
                    )
                    
                return LLMResponse(response.choices[0].message)
                # Exit the loop if the prompt was successful
            
            except openai.APIConnectionError as e:
                error_content += f"\nAPIConnectionError: {e}. Retrying in 2 seconds..\n."
                error_content += str(e.__cause__)  # an underlying Exception, likely raised within httpx.
                time.sleep(2)
            except openai.RateLimitError as e:
                error_content += "\nA 429 status code was received; we should back off a bit as we have hit a rate limit.\n"
                print("\nSleeping for 15 seconds...\n")
                time.sleep(15)
            except openai.APIStatusError as e:
                error_content += "\nA non-200-range status code was received. Retrying in 2 seconds...\n"
                error_content += f"{e.status_code}\n"
                error_content += f"{e.response}\n"
                time.sleep(2)
                
        from swayam import Template
        
        error_dict = {
            "content": error_content,
            "role": "user"
        }
        return LLMResponse(error_dict, error=True)
