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

import json
from typing import Union

from tarkash import log_debug

from swayam.llm.prompt.types import Perspective
from swayam.llm.prompt.response import LLMResponse
from .base import BaseLLMEnactor

class ExpressionEnactor(BaseLLMEnactor):

    def __init__(self, *, listener:str, model:str = None, name:str = "Expression Enactor", provider:str = None, temperature=0, perspective: Union[str,Perspective]=None, **kwargs):
        super().__init__(listener=listener, name=name, provider=provider, model=model, temperature=temperature, **kwargs)            
        log_debug(f"Expression Enactor {name} created")

    def load(self):
        from swayam.llm.model import Model
        self.__client = Model.create_client(config=self.model_config, prompt_config=self.prompt_config)
    
    def enact(self, expression):
        '''
        Runs the expression and returns the result.
        '''        
        # For an extended expression, the system prompt is already executed in one of the previous expressions.
        
        expression_narrative = expression.narrative.expression_narrative
        
        log_debug(f"Executing Expression with {len(expression)} prompt(s).")
        if not expression.extends_previous_expression:
            self.listener.record_begin_expression(expression)
            if expression.is_new():
                if expression.has_perspective():
                    # For dynamic variables in Narrator store
                    expression.narrative.format_prompt(expression.perspective)
                    expression.perspective.process_for_report()
                    self.listener.record_perspective(expression.perspective)
                    
                    expression_narrative.append_prompt(expression.perspective)
                    self.listener.record_narrative(expression_narrative)
        log_debug("Finished processing system prompt.")
        
        for prompt in expression:
            log_debug("Processing prompt...")
            # For dynamic variables in Narrator store
            expression.narrative.format_prompt(prompt)
            prompt.process_for_report()
            
            self.listener.record_narrative(expression_narrative)
            
            # Appending happens via the Narrator Narrative so that dynamic variables can be considered.
            expression_narrative.append_prompt(prompt)
            self.listener.record_narrative(expression_narrative)
            
            self.listener.record_prompt(prompt)
            log_debug("Finished processing prompt...")

            log_debug("Executing prompt...")
            response = self.__client.execute_messages(messages=expression_narrative.messages, output_structure=prompt.output_structure, tools=prompt.tools)
            log_debug("Handling Response.")
            output_message = response.choices[0].message
            llm_response = LLMResponse(output_message)
            
            expression_narrative.append_assistant_response(llm_response.as_dict())
            self.listener.record_narrative(expression_narrative)
            
            self.listener.record_response(prompt, llm_response)

            
            log_debug("Updated Narrative with Response message.")

            if output_message.tool_calls:
                response_messages = []
                for tool in output_message.tool_calls:
                    tool_response = prompt.call_tool(tool.id, tool.function.name, **json.loads(tool.function.arguments))
                    self.listener.record_tool_response(tool_response)
                    response_messages.append(tool_response)
                    expression_narrative.append_tool_response(tool_response)
                    self.listener.record_narrative(expression_narrative)
            else: 
                response_messages = output_message
                
        if expression.should_store_response:
            stored_message = response_messages
            if type(response_messages) is list:
                stored_message = response_messages[-1]
            from swayam.inject.tool.response import ToolResponse
            if isinstance(stored_message, ToolResponse):
                stored_message = stored_message.content
            else:
                stored_message = stored_message.to_dict()
            if "content" in stored_message and stored_message["content"]:
                expression.narrative.store[expression.response_storage_name] = stored_message["content"]

        log_debug(f"Finished Expression") 
        return response_messages