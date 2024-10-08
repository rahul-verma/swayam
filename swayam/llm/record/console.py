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

from swayam.llm.phase.prompt import Prompt
from swayam.llm.phase.expression.conversation import Conversation
from swayam.llm.phase.prompt.response import LLMResponse
from swayam.llm.record import Reporter
    
class ConsoleRecorder(Reporter):
    def __init__(self):
        super().__init__()
        
    @property
    def enabled(self):
        return self.__enabled
    
    def record_begin_thought(self, thought) -> None:
        pass
    
    def record_begin_story(self, story) -> None:
       pass

    def record_begin_expression(self, expression) -> None:
        """
        Broadcasts the system prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        pass

    def record_prompt(self, prompt:Prompt, conversation) -> None:
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        print("-" * 80)
        print("Prompt:", f"(Role: {prompt.role})")
        
        ## Should not print image
        content = prompt.content
        if type(content) == list:
            print(prompt.reportable_text)
            print("=" * 100)
            for item in prompt.reportable_content:
                if item["type"] == "image_url":
                    print(item["local_path"])
        else:
            print(prompt.content)
        print("-" * 80)
        
    def record_response(self, prompt, response:LLMResponse) -> None:
        """
        Reports the LLM response.

        Args:
            response (LLMResponse): Response message from LLM.
        """
        print("Response:")
        print(response.content)
        
    def record_action_response(self, response) -> None:
        """
        Reports the action response.

        Args:
            message (dict): ActionResponse object
        """
        pass
        
    def finish(self) -> None:
        """
        Finishes report creation.
        """
        print("-"* 80) 
        
    def reset(self) -> None:
        pass
