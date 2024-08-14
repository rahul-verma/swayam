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

from .prompt.prompt import Prompt, SystemPrompt
from .prompt.context import PromptContext

class AgentListener:
    
    def __init__(self, display:bool=True, report_html=False, show_in_browser=True, **kwargs):
        self.__reporters = []
        
        from .report import ConsoleReporter, HtmlReporter
        if display:
            self.__reporters.append(ConsoleReporter(enabled=display))
            
        if report_html:
            self.__reporters.append(HtmlReporter(show_in_browser=show_in_browser))
            
    def report_system_prompt(self, prompt:SystemPrompt) -> None:
        """
        Broadcasts the system prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        for reporter in self.__reporters:
            reporter.report_system_prompt(prompt)

    def report_prompt(self, prompt:Prompt) -> None:
        """
        Broadcasts the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        for reporter in self.__reporters:
            reporter.report_prompt(prompt)
    
    def report_context(self, context:PromptContext) -> None:
        """
        Broadcasts the context details.

        Args:
            context (PromptContext): Context object with all input messages.
        """
        for reporter in self.__reporters:
            reporter.report_context(context)
 
    def report_response(self, prompt, message:dict) -> None:
        """
        Broadcasts the output message.

        Args:
            message (dict): Response dict from LLM.
        """
        for reporter in self.__reporters:
            reporter.report_response(prompt, message)
            
    def finish(self) -> None:
        """
        Broadcasts finish signal.
        """
        for reporter in self.__reporters:
            reporter.finish()