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

from swayam.llm.expression.conversation import Conversation

class Recorder:
    
    def __init__(self, recorder_config):
        self.__recorders = []
        
        from .console import ConsoleRecorder
        from .html import HtmlRecorder
        if recorder_config.display:
            self.__recorders.append(ConsoleRecorder())
            
        if recorder_config.record_html:
            self.__recorders.append(HtmlRecorder(config=recorder_config))
            
    def record_begin_story(self, story) -> None:
        """
        Broadcasts the story details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        for recorder in self.__recorders:
            recorder.record_begin_story(story)

    def record_begin_thought(self, thought) -> None:
        """
        Broadcasts the thought details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        for recorder in self.__recorders:
            recorder.record_begin_thought(thought)
                        
    def record_begin_expression(self, expression) -> None:
        """
        Broadcasts the expression details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        for recorder in self.__recorders:
            recorder.record_begin_expression(expression)
            
    def record_directive(self, directive) -> None:
        """
        Broadcasts the directive details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        for recorder in self.__recorders:
            recorder.record_directive(directive)

    def record_prompt(self, prompt) -> None:
        """
        Broadcasts the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        for recorder in self.__recorders:
            recorder.record_prompt(prompt)
    
    def record_conversation(self, narrative:Conversation) -> None:
        """
        Broadcasts the narrative details.

        Args:
            narrative (Conversation): Narrative object with all input messages.
        """
        for recorder in self.__recorders:
            recorder.record_conversation(narrative)
 
    def record_response(self, prompt, message:dict) -> None:
        """
        Broadcasts the output message.

        Args:
            message (dict): Response dict from LLM.
        """
        for recorder in self.__recorders:
            recorder.record_response(prompt, message)
            
    def record_tool_response(self, response) -> None:
        """
        Broadcasts the tool response.

        Args:
            message (dict): ToolResponse object
        """
        for recorder in self.__recorders:
            recorder.record_tool_response(response)
            
    def finish(self) -> None:
        """
        Broadcasts finish signal.
        """
        for recorder in self.__recorders:
            recorder.finish()
            
    def reset(self) -> None:
        """
        Broadcasts reset signal.
        """
        for recorder in self.__recorders:
            recorder.reset()