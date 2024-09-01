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

from swayam.llm.prompt import Prompt
from swayam.llm.prompt.types import Directive
from swayam.llm.expression.narrative import ExpressionNarrative

class Recorder:
    
    def __init__(self, recorder_config):
        self.__reporters = []
        
        from .console import ConsoleRecorder
        from .html import HtmlRecorder
        if recorder_config.display:
            self.__reporters.append(ConsoleRecorder())
            
        if recorder_config.record_html:
            self.__reporters.append(HtmlRecorder(config=recorder_config))
            
    def record_begin_expression(self, expression) -> None:
        """
        Broadcasts the system prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        for reporter in self.__reporters:
            reporter.record_begin_expression(expression)
            
    def record_directive(self, prompt:Directive) -> None:
        """
        Broadcasts the system prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        for reporter in self.__reporters:
            reporter.record_directive(prompt)

    def record_prompt(self, prompt:Prompt) -> None:
        """
        Broadcasts the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        for reporter in self.__reporters:
            reporter.record_prompt(prompt)
    
    def record_narrative(self, narrative:ExpressionNarrative) -> None:
        """
        Broadcasts the narrative details.

        Args:
            narrative (ExpressionNarrative): Narrative object with all input messages.
        """
        for reporter in self.__reporters:
            reporter.record_narrative(narrative)
 
    def record_response(self, prompt, message:dict) -> None:
        """
        Broadcasts the output message.

        Args:
            message (dict): Response dict from LLM.
        """
        for reporter in self.__reporters:
            reporter.record_response(prompt, message)
            
    def record_tool_response(self, response) -> None:
        """
        Broadcasts the tool response.

        Args:
            message (dict): ToolResponse object
        """
        for reporter in self.__reporters:
            reporter.record_tool_response(response)
            
    def finish(self) -> None:
        """
        Broadcasts finish signal.
        """
        for reporter in self.__reporters:
            reporter.finish()