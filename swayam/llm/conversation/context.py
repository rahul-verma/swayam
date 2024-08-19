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

class PromptContext:
    
    def __init__(self, messages=None):
        self.__messages = messages if messages else []
        self.__reportable_messages = []
        self.__expected_output_structure = None
        
    def reset(self):
        self.__messages = []
        self.__reportable_messages = []
        
    @property
    def expected_output_structure(self):
        if not self.__expected_output_structure:
            return None
        return json.loads(self.__expected_output_structure.schema_json())
    
    @expected_output_structure.setter
    def expected_output_structure(self, value):
        self.__expected_output_structure = value
        
    @property
    def messages(self):
        return self.__messages
    
    def __len__(self):
        return len(self.__messages)
    
    @property
    def reportable_messages(self):
        return self.__reportable_messages
        
    def append_prompt(self, prompt):
        self.__messages.append(prompt.message)
        self.__reportable_messages.append(prompt.message)
        
    def append_assistant_response(self, *messages):
        for message in messages:
            if "tool_calls" in message and not message["tool_calls"]:
                del message["tool_calls"]
            self.__messages.append(message)
            self.__reportable_messages.append(message)
            
    def append_tool_response(self, response):
        message = {
            "role": "tool",
            "content": json.dumps(response.content),
            "tool_call_id": response.tool_id
        }
        self.__messages.append(message)
        self.__reportable_messages.append(message)