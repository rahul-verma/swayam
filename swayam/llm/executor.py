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

import os
from pprint import pprint
from pydantic import BaseModel
from tarkash import TarkashObject, log_info, log_debug
from .prompt.response import LLMResponse

class ConversationExecutor(TarkashObject):    
    """
    Executes the prompt and returns the result.
    """
    
    def __init__(self, *, model_config, prompt_config, listener):
        tobj_kwargs = dict()
        tobj_kwargs["model_config"] = model_config
        tobj_kwargs["prompt_config"] = prompt_config
        super().__init__(**tobj_kwargs)
        self.__model_config = model_config
        self.__prompt_config = prompt_config
        self.__listener = listener
        self.__client = None
        self.__load()
        
    @property
    def model_config(self):
        return self.__model_config
    
    @property
    def prompt_config(self):
        return self.__prompt_config
    
    @property
    def listener(self):
        return self.__listener
        
    def __load(self):
        from .model import Model
        self.__client = Model.create_client(config=self.model_config, prompt_config=self.prompt_config)
    
    def execute(self, *, conversation, response_format:BaseModel=None, functions=None):
        '''
            Runs the prompt text and returns the result.
        '''

        output_messages = []
        for prompt in conversation:
            log_debug("Executing prompt...")
            prompt.process_for_report()
            print("Is system prompt", prompt.is_system_prompt, prompt.content)
            if prompt.is_system_prompt:
                self.listener.report_system_prompt(prompt)
                conversation.context.append_prompt(prompt)
            else:
                self.listener.report_context(conversation.context)
                conversation.context.append_prompt(prompt)
                self.listener.report_prompt(prompt)

            response = self.__client.execute_messages(conversation.context.messages, response_format=response_format, functions=functions)
            output_message = response.choices[0].message
            output_messages.append(output_message)
            response_message = LLMResponse.create_response_object(output_message)
            self.listener.report_response(prompt, response_message)

            conversation.context.append_assistant_response(response_message.as_dict())

        return output_messages