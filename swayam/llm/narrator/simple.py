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

class SimpleNarrator:
    
    def __init__(self, display=False, record_html=True, run_id=None):
        self.__narrative = NarratorNarrative()
        from swayam.llm.config.report import RecorderConfig
        self.__recorder_config = RecorderConfig(display=display, record_html=record_html, show_in_browser=False)
        if not run_id:
            self.__recorder_config._run_id = datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            self.__recorder_config._run_id = str(run_id)
            
        from swayam.llm.record.recorder import Recorder
        log_debug(f"Creating Listener")
        self.__listener = Recorder(self.__recorder_config)
        log_debug("Narrator initialized.")
        
    def __prepare_for_execution(self, *, show_in_browser):
        log_debug(f"Setting show_in_browser to {show_in_browser}.")
        self.__recorder_config.show_in_browser = show_in_browser
        
        
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
        log_debug(f"Expression has an already assigned system prompt?", expression.has_perspective()) 
        if expression.is_new() and not expression.has_perspective():
            log_debug(f"Setting default system prompt from the Narrator.")
            expression.perspective = narrator.perspective
            
        log_debug("Validating expression.")
        if expression.is_new() and not expression.has_perspective():
            raise ValueError("It's a new expression, but no Perspective was found. Review.")
        
        if not expression.is_new() and expression.has_perspective():
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
    
    def enact(self, executable, show_in_browser=False):
        """
        Executes a part of or complete strategy.
        
        The Narrator can execute any of the following types of objects:
        - A User Prompt object
        - A Expression object
        - A Thought object: Not supported yet
        - A Story object: Not supported yet
        
        Args:
            executable: The object to execute.
            show_in_browser: If True, the HTML report will be displayed in the browser. Default is False.
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