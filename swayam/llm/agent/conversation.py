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

from typing import Union

from tarkash import log_debug

from swayam.llm.prompt.types import SystemPrompt
from .base import BaseLLMAgent

class ConversationAgent(BaseLLMAgent):

    def __init__(self, *, report_config, name:str = "Conversation Agent", provider:str = None, model:str = None, temperature=0, system_prompt: Union[str,SystemPrompt]=None, **kwargs):
        super().__init__(name=name, provider=provider, model=model, temperature=temperature, report_config=report_config, **kwargs)
        
        self.__default_agent_system_prompt = "You are a helpful assistant who deliberates and provides useful answers to my queries."
        if system_prompt is None:
            self.__system_prompt = SystemPrompt(text=self.__default_agent_system_prompt)
        elif isinstance(system_prompt, str):
            self.__system_prompt = SystemPrompt(text=system_prompt) 
        elif isinstance(system_prompt, SystemPrompt):
            self.__system_prompt = system_prompt
        else:
            TypeError(f"Invalid type for system_prompt: {type(system_prompt)}. Can be either str or SystemPrompt.")
            
        log_debug(f"Conversation Agent {name} created")
        
    @property
    def system_prompt(self):
        return self.__system_prompt
        
    def execute(self, conversation):
        from swayam.llm.report.listener import AgentListener
        from swayam.llm.prompt import Prompt
        log_debug(f"Creating Listener")
        listener = AgentListener(self.report_config)

        print(f"Executing Conversation with {len(conversation)} step(s)")
        from .mediator import Mediator
        mediator = Mediator(model_config=self.model_config, prompt_config=self.prompt_config, listener=listener)
        output = mediator.execute(conversation=conversation)
        log_debug(f"Finished Conversation")        
        listener.finish()
        return output
                