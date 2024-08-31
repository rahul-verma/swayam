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
        
    def execute_messages(self, *, messages, output_structure=None, tools=None):
        from pprint import pprint
        import openai
        if tools:
            tools =[tool.definition for tool in tools]


        for attempt in range(5):  # Retry up to 5 times
            try:
                if output_structure is None:
                    return self._client.chat.completions.create(
                        model=self.model_name,
                        messages=messages,
                        tools=tools,
                        **self._model_kwargs
                    )
                else:
                    return self._client.beta.chat.completions.parse(
                        model=self.model_name,
                        messages=messages,
                        response_format=output_structure.data_model,
                        **self._model_kwargs
                    )
                break  # Exit the loop if the prompt was successful
            
            except openai.APIConnectionError as e:
                print(f"APIConnectionError: {e}. Retrying in 2 seconds...")
                print(e.__cause__)  # an underlying Exception, likely raised within httpx.
                time.sleep(2)
            except openai.RateLimitError as e:
                print("A 429 status code was received; we should back off a bit as we have hit a rate limit.")
                print("Sleeping for 60 seconds...")
                time.sleep(60)
            except openai.APIStatusError as e:
                print("A non-200-range status code was received. Retrying in 2 seconds...")
                print(e.status_code)
                print(e.response)
                time.sleep(2)
                
