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
import json
from abc import ABC, abstractmethod
from pprint import pprint

from .prompt.request import Prompt
from .prompt.context import PromptContext
from .prompt.response import LLMResponse

class Reporter(ABC):
    
    def __init__(self, **kwargs):
        pass
    
    @abstractmethod
    def report_prompt(self, prompt:Prompt) -> None:
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        pass
        
    @abstractmethod
    def report_context(self, context:PromptContext) -> None:
        """
        Reports the context details.

        Args:
            context (PromptContext): Context object with all input messages.
        """
        pass

        
    def report_response(self, message:LLMResponse) -> None:
        """
        Reports the output message.

        Args:
            message (LLMResponse): Response message from LLM.
        """
        pass
    
    @abstractmethod
    def finish(self) -> None:
        """
        Finishes report creation.
        """
        pass
        
    
class ConsoleReporter(Reporter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    @property
    def enabled(self):
        return self.__enabled

    def report_prompt(self, prompt:Prompt) -> None:
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        print("-" * 80)
        print("Prompt:", f"(Role: {prompt.role})")
        print(prompt.content)
        print("-" * 80)

    def report_context(self, context:PromptContext) -> None:
        """
        Reports the context details.

        Args:
            context (PromptContext): Context object with all input messages.
        """
        print ("Total Context Length:", len(context.messages), "#Previous Request-Response Pairs:", int((len(context.messages)-1)/2))
        # if not context.messages:
        #     print("Context Messages: None")
        # else:
        #     print("Context Messages:")
        #     pprint(context.messages)
        print("-" * 80)

        
    def report_response(self, response:LLMResponse) -> None:
        """
        Reports the output message.

        Args:
            response (LLMResponse): Response message from LLM.
        """
        print("Response:")
        print(response.content)
        
    def finish(self) -> None:
        """
        Finishes report creation.
        """
        print("-"* 80) 

class HtmlReporter(Reporter):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def report_prompt(self, prompt:Prompt) -> None:
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        pass

    def report_context(self, context:PromptContext) -> None:
        """
        Reports the context details.

        Args:
            context (PromptContext): Context object with all input messages.
        """
        pass

        
    def report_response(self, response:LLMResponse) -> None:
        """
        Reports the output message.

        Args:
            response (LLMResponse): Response message from LLM.
        """
        pass

    def finish(self) -> None:
        """
        Finishes report creation.
        """
        if self._show_in_browser:
            self.show_in_browser()

class PromptSessionHtmlReporter:
    """
    Reports the prompt session details to a file.
    """
    
    def __init__(self, name, **kwargs):
        """
        Initializes the PromptSessionReporter with the provided name.
        """
        from swayam import Swayam
        from swayam.core.constant import SwayamOption
        
        # For JSON Data
        self.__base_path = os.path.join(Swayam.get_option_value(SwayamOption.REPORT_ROOT_DIR), name)
        os.makedirs(self.__base_path, exist_ok=True)
        self.__json_path = self.__base_path + "/json/data.json"
        os.makedirs(self.__base_path +"/json", exist_ok=True)
        
        # For HTML Report
        self.__html_report_path = self.__base_path + "/report.html"
        template_path = Swayam._get_swayam_res_path("report_template.html")
        self.__template = ""
        with open(template_path, 'r') as f:
            self.__template = f.read()
        self.__res_path = os.path.join(os.path.realpath(__file__), "..")
        self.__json_data = [
                                {
                                    "id": "node_1",
                                    "text": "Default Prompt Executor",
                                    "children": []
                                }
        ]
        self.__counter = -1
        self.__context_counter = -1
        self.__response_counter = -1
        self.__update_report()
        
    def __get_executor_node(self):
        return self.__json_data[0]["children"]
            
    def __update_report(self):
        json_str = json.dumps(self.__json_data, indent=4)
        with open(self.__json_path, 'w') as f:
            f.write(json_str)
        
        with open(self.__html_report_path, 'w') as f:
            html = self.__template.replace("$$SWAYAM_JSON_DATA$$", json_str)
            f.write(html)
        
    def report_prompt(self, prompt):
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        self.__counter += 1
        self.__get_executor_node().append(
        {
                "id": "prompt_" + str(self.__counter),
                "text": "Prompt::" + str(self.__counter + 1),
                "data": {
                            "content": prompt
                        },
                "children": [
                    {
                        "id": "prompt_text_" + str(self.__counter),
                        "text": "Prompt",
                        "icon": "jstree-file",
                        "data": {"content": prompt}
                    }
                ]
        })
        self.__update_report()
        
    def report_context(self, messages):
        self.__context_counter += 1
        children = []
        self.__chat_context_counter = 0
        output = []
        for message in messages:
            self.__chat_context_counter += 1
            child = {
                        "id": "chat_context_msg_" + str(self.__chat_context_counter),
                        "text": "Message:: " + str(self.__chat_context_counter),
                        "icon": "jstree-file",
                        "data": {"content": message}
                    }
            output.append(child)
            
            
        children.append({
                        "id": "chat_context_" + str(self.__context_counter),
                        "text": "Chat Context",
                        "icon": "jstree-file",
                        "data": {
                            "content": "This is the sequences of messages sent to the LLM for context management."
                        },
                        "children": output
                    })
        self.__get_executor_node()[-1]["children"].extend(children)        
        self.__update_report()
        
    def report_response(self, message):
        self.__response_counter += 1
        children = []
        children.append({
                        "id": "message_" + str(self.__response_counter),
                        "text": "Response Message",
                        "icon": "jstree-file",
                        "data": {
                            "content": message.to_dict()
                        }
                    })
        
        children.append({
                        "id": "content_" + str(self.__response_counter),
                        "text": "Response Content",
                        "icon": "jstree-file",
                        "data": {
                            "content": message.content
                        }
                    })
        self.__get_executor_node()[-1]["children"].extend(children)       
        self.__update_report()
        
        
    def show_in_browser(self):
        """
        Opens the report in the default browser.
        """
        import webbrowser
        webbrowser.open("file://" + self.__html_report_path)

