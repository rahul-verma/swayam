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
import webbrowser
from abc import ABC, abstractmethod
from pprint import pprint
import copy

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
        Reports the LLM response.

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
        
        ## Should not print image
        content = prompt.content
        if type(content) == list:
            print(prompt.reportable_text)
            for item in prompt.reportable_content:
                if item["type"] == "image_url":
                    print(item["local_path"])
        else:
            print(prompt.content)
        print("-" * 80)

    def report_context(self, context:PromptContext) -> None:
        """
        Reports the context details.

        Args:
            context (PromptContext): Context object with all input messages.
        """
        if len(context.messages) == 1:
            return
        print ("Total Context Length (Previous Request-Response Pairs):", int((len(context.messages)-1)/2))
        # if not context.messages:
        #     print("Context Messages: None")
        # else:
        #     print("Context Messages:")
        #     pprint(context.messages)
        print("-" * 80)

        
    def report_response(self, response:LLMResponse) -> None:
        """
        Reports the LLM response.

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
    
    def __init__(self, show_in_browser=True, **kwargs):
        super().__init__(**kwargs)
        self.__show_in_browser = show_in_browser
        
        from tarkash import Tarkash
        from swayam import Swayam
        from swayam.core.constant import SwayamOption
        
        # For JSON Data
        self.__base_path = os.path.join(Tarkash.get_option_value(SwayamOption.REPORT_ROOT_DIR), "session")
        os.makedirs(self.__base_path, exist_ok=True)
        self.__json_path = self.__base_path + "/json/data.json"
        os.makedirs(self.__base_path +"/json", exist_ok=True)
        
        # For HTML Report
        self.__html_report_path = self.__base_path + "/report.html"
        template_path = Swayam._get_swayam_res_path("llm_report_template.html")
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

    def report_prompt(self, prompt:Prompt) -> None:
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        self.__counter += 1
        prompt_node = {
                "id": "prompt_" + str(self.__counter),
                "text": "Prompt::" + str(self.__counter + 1),
                "data": {
                            "content": prompt.reportable_text
                        },
                "children": []
        }
        
        reportable_content = prompt.reportable_content
        if type(prompt.reportable_content)  != list:
            reportable_content = [reportable_content]
        
        def append_text_child(text, sub_counter):
            prompt_node["children"].append({
                        "id": "prompt_part_" + str(self.__counter) + "_" + str(sub_counter),
                        "text": "Prompt",
                        "icon": "jstree-file",
                        "data": {"content": text}
            })
            
        sub_counter = 0
        for item in reportable_content:
            sub_counter += 1
            if type(item) is str:
                append_text_child(item, sub_counter)
            elif item["type"] == "image_url":
                prompt_node["children"].append({
                        "id": "prompt_part_" + str(self.__counter) + "_" + str(sub_counter),
                        "text": "Image Upload",
                        "icon": "jstree-file",
                        "data": {"content": item["local_path"]}
            })
            else:
                append_text_child(item["text"], sub_counter)
                        
        self.__get_executor_node().append(prompt_node)
        self.__update_report()
        
    def report_context(self, context:PromptContext) -> None:
        """
        Reports the context details.

        Args:
            context (PromptContext): Context object with all input messages.
        """
        self.__context_counter += 1
        children = []
        self.__chat_context_counter = 0
        output = []
        for message in context.reportable_messages:
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
        
    def report_response(self, response:LLMResponse) -> None:
        """
        Reports the LLM response.

        Args:
            response (LLMResponse): Response message from LLM.
        """
        self.__response_counter += 1
        children = []
        children.append({
                        "id": "message_" + str(self.__response_counter),
                        "text": "Response Message",
                        "icon": "jstree-file",
                        "data": {
                            "content": response.as_dict()
                        }
                    })
        
        children.append({
                        "id": "content_" + str(self.__response_counter),
                        "text": "Response Content",
                        "icon": "jstree-file",
                        "data": {
                            "content": response.content
                        }
                    })
        self.__get_executor_node()[-1]["children"].extend(children)       
        self.__update_report()

    def finish(self) -> None:
        """
        Finishes report creation.
        """
        if self.__show_in_browser:        
            webbrowser.open("file://" + self.__html_report_path)


        


