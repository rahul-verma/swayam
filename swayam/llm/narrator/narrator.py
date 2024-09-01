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

from datetime import datetime
from tarkash import log_debug
from .narrative import NarratorNarrative

class Narrator:
    
    def __init__(self, display=False, record_html=True, narration=None):
        self.__narrative = NarratorNarrative()
        if not display and not record_html:
            raise ValueError("At least one of display or record_html must be True.")
        from swayam.llm.config.report import RecorderConfig
        self.__recorder_config = RecorderConfig(display=display, record_html=record_html, show_in_browser=False)
        if not narration:
            self.__recorder_config._narration = datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            self.__recorder_config._narration = str(narration)
            
        from swayam.llm.record.recorder import Recorder
        log_debug(f"Creating Recorder")
        self.__listener = Recorder(self.__recorder_config)
        log_debug("Narrator initialized.")
        
    def __execute_user_prompt(self, user_prompt):
        from swayam import Expression
        log_debug(f"Converting UserPrompt to Expression.")
        expression = Expression.prompts(user_prompt, reset_narrative=False)
        expression.extends_previous_expression = True
        return self.__execute_expression(expression)
    
    def __execute_expression(self, expression):
        from swayam.llm.expression.narrative import ExpressionNarrative
        from swayam.llm.enactor.expression import ExpressionEnactor

        if expression.reset_narrative:
            self.__narrative.reset_expression_narrative()

        # Set narrative of expression
        if not expression.standalone:
            expression.narrative = self.__narrative
        else:
            # Set empty narrative
            expression.narrative = NarratorNarrative()
        
        log_debug(f"Executing Expression with ExpressionNarrator.")
        narrator = ExpressionEnactor(listener=self.__listener)
        
        # If a the narrative is non-empty then the system prompt is already set in it.
        log_debug(f"New narrative-free expression?", expression.is_new())
        log_debug(f"Expression has an already assigned system prompt?", expression.has_directive()) 
        if expression.is_new() and not expression.has_directive():
            log_debug(f"Setting default system prompt from the Narrator.")
            expression.directive = narrator.directive
            
        log_debug("Validating expression.")
        if expression.is_new() and not expression.has_directive():
            raise ValueError("It's a new expression, but no Directive was found. Review.")
        
        if not expression.is_new() and expression.has_directive():
            raise ValueError("As it is continued expression, the system prompt is already set in the narrative. So, the narrative found in this expression is going to be ignored. Review.")

        log_debug(f"Executing Expression with ExpressionNarrator.")
        def process_output(in_data):
            if in_data.content:
                return in_data.content
            elif "tool_calls" in in_data and in_data["tool_calls"]:
                return f'Tool Call {in_data["tool_calls"]["function"]["name"]} suggested.'
                
        output = narrator.enact(expression)
        
        if type(output) is list:
            if len(output) == 1:
                return process_output(output[0])
            elif len(output) == 0:
                return None
            else:
                return [process_output(o) for o in output]
        else:
            return process_output(output)
        
    def __execute_thought(self, thought):
        output = None
        for expression in thought:
            output = self.__execute_expression(expression)
        return output
    
    def enact(self, phase):
        """
        Executes a part of or complete strategy.
        
        The Narrator can execute any of the following types of objects:
        - A Prompt object
        - An Expression object
        - A Thought object: Not supported yet
        - A Story object: Not supported yet
        
        Args:
            phase: The phase to enact.
        """
        
        log_debug(f"Executing Narrator executable object of type {type(executable)}.")
        self.__prepare_for_execution(show_in_browser=show_in_browser)
        
        from swayam.llm.prompt.types import UserPrompt
        from swayam.llm.expression.expression import LLMExpression
        from swayam.llm.thought.thought import LLMThought
        
        if not isinstance(executable, (str, UserPrompt, LLMExpression, LLMThought)):
            raise TypeError(f"Cannot execute object of type {type(executable)}. It must be an instance of str, UserPrompt, LLMExpression, LLMThought, or Story.")
        
        output = None
        if isinstance(executable, str):
            from swayam.llm.prompt import Prompt
            log_debug(f"Converting user prompt string to LLMExpression.")
            output = self.__execute_user_prompt(Prompt.text(executable))
        if isinstance(executable, UserPrompt):
            log_debug(f"Converting UserPrompt to LLMExpression.")
            output = self.__execute_user_prompt(executable)
        elif isinstance(executable, LLMExpression):
            output = self.__execute_expression(executable)
        elif isinstance(executable, LLMThought):
            output = self.__execute_thought(executable)
            
        self.__listener.finish()
        return output