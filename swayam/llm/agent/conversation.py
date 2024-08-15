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


from swayam.llm.prompt.types import SystemPrompt
from .base import BaseLLMAgent
from tarkash import log_debug

class ConversationAgent(BaseLLMAgent):

    def __init__(self, name:str = "Conversation Agent", provider:str = None, model:str = None, temperature=0, display=False, report_html=True, show_in_browser=True, **kwargs):
        super().__init__(name=name, provider=provider, model=model, temperature=temperature, display=display, report_html=report_html, show_in_browser=show_in_browser, **kwargs) 
        self.__default_system_prompt = SystemPrompt(text="You are a helpful assistant. You are here to help me with my queries.") 
        
    def execute(self, conversation, *, context, _run_id=True):
        from swayam.llm.report.listener import AgentListener
        from swayam.llm.prompt import Prompt
        self.report_config._run_id = _run_id
        listener = AgentListener(self.report_config)

        # If a non-empty context is provided, then the system prompt is already set in it. (Till we reach a multi-agent router)
        if len(context) == 0 and not conversation.has_system_prompt():
            conversation.set_system_prompt(self.__default_system_prompt)

        print(f"Executing Conversation with {len(conversation)} step(s)")
        from .mediator import Mediator
        mediator = Mediator(model_config=self.model_config, prompt_config=self.prompt_config, listener=listener)
        conversation.context = context
        output = mediator.execute(conversation=conversation)
        log_debug(f"Finished Conversation")        
        listener.finish()

        if output.tool_calls:
            print(output.tool_calls)
        return output
                