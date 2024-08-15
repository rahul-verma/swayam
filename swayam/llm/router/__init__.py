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

class Router:
    
    def __init__(self):
        from swayam.llm.conversation.context import PromptContext
        self.__context = PromptContext()
        self._run_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    def execute(self, executable, display=False, reset_context=True, report_html=True, show_in_browser=True):
        """
        Executes a compatible object.
        
        The Router can execute any of the following types of objects:
        - A Conversation object: Not supported yet
        - A Task object: Not supported yet
        - A Plan object: Not supported yet
        
        Args:
            executable: The object to execute.
        """
        if reset_context:
            print("Resetting context...")
            self.__context.reset()
            self._run_id = datetime.now().strftime("%Y%m%d%H%M%S")
            
        from swayam import Conversation
        if isinstance(executable, Conversation):
            from swayam.llm.agent.conversation import ConversationAgent
            agent = ConversationAgent(display=display, report_html=report_html, show_in_browser=show_in_browser)
            agent.execute(executable, _run_id=self._run_id, context=self.__context)
        else:
            raise TypeError(f"Cannot execute object of type {type(executable)}. It must be an instance of Conversation, Task, or Plan.")