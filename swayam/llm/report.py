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
from uuid import uuid4

import os
import json
import webbrowser
from abc import ABC, abstractmethod
from pprint import pprint
import copy

from .prompt.prompt import Prompt
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
    
    def report_system_prompt(self, prompt:Prompt) -> None:
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        print("-" * 80)
        print("Prompt:", f"(Role: {prompt.role})")
        
        self.report_prompt(prompt)

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
            print("=" * 100)
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

        
    def report_response(self, prompt, response:LLMResponse) -> None:
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
        self.__json_data = []
        self.__update_report()
        
    def __get_latest_conversation_node(self):
        first_agent_insertion_point = self.__json_data[0]["children"] # System prompt is at index 0
        first_task_insertion_point = first_agent_insertion_point[1]["children"]
        first_conversation_insertion_point = first_task_insertion_point[0]["children"]
        from pprint import pprint
        pprint(first_conversation_insertion_point)
        return first_conversation_insertion_point
            
    def __update_report(self):
        json_str = json.dumps(self.__json_data, indent=4)
        with open(self.__json_path, 'w') as f:
            f.write(json_str)
        
        with open(self.__html_report_path, 'w') as f:
            html = self.__template.replace("$$SWAYAM_JSON_DATA$$", json_str)
            f.write(html)
            
    def report_system_prompt(self, prompt:Prompt) -> None:
        """
        Reports the system prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        print("Reporting System Prompt")
        
        # Add Agent Node
        self.__json_data.append({
                                "id": "agent_node_" + uuid4().hex,
                                "text": "Agent",
                                "children": []   
                            })
        
        # The system prompt node it as index 0
        prompt_node = self.report_prompt(prompt, role="System", append=False)
        self.__json_data[0]["children"].append(prompt_node)
        
        # The Task node is index 1
        self.__json_data[0]["children"].append({
                                    "id": "task_node_" + uuid4().hex,
                                    "text": "Task",
                                    "children": []
                                })
        
        # This children in this node is the executor node for rest of the reporting.
        # self.__json_data[0]["children"][1]["children"][0["children"]
        self.__json_data[0]["children"][1]["children"] = [{
                                    "id": "conversation_node_" + uuid4().hex,
                                    "text": "Conversation",
                                    "children": []
                                }]
        self.__update_report()
            
    def report_context(self, context:PromptContext) -> None:
        """
        Reports the context details.

        Args:
            context (PromptContext): Context object with all input messages.
        """
        print("Reporting Context")
        context_messages = []
        
        title = {
            "system": "System",
            "user": "User",
            "assistant": "LLM",
        }

        for i, message in enumerate(context.reportable_messages):
            text = title[message["role"]]
            child = {
                        "id": "chat_context_msg_" + uuid4().hex,
                        "text": text,
                        "icon": "jstree-file",
                        "data": {"content": message}
                    }
            context_messages.append(child)

        if not context_messages:
            context_node = {
                        "id": "chat_context_" + uuid4().hex,
                        "text": "Chat Context",
                        "icon": "jstree-file",
                        "data": {
                            "content": "No context messages were sent along with the next prompt."
                        }
                    }
        else:            
            context_node = {
                            "id": "chat_context_" + uuid4().hex,
                            "text": "Chat Context",
                            "data": {
                                "content": "This is the sequences of messages sent to the LLM for context management."
                            },
                            "children": context_messages
                        }
        self.__get_latest_conversation_node().append(context_node)        
        self.__update_report()

    def report_prompt(self, prompt:Prompt, role="User", append=True) -> None:
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        print("Reporting Prompt")
        prompt_node = {
                "id": "prompt_" + uuid4().hex,
                "text": f"{role} Prompt",
                "data": {
                            "content": prompt.reportable_text
                        },
                "children": []
        }
        
        reportable_content = prompt.reportable_content
        if type(prompt.reportable_content)  != list:
            reportable_content = [reportable_content]
        
        # def append_text_child(text, sub_counter):
        #     prompt_node["children"].append({
        #                 "id": "prompt_part_" + str(self.__counter) + "_" + str(sub_counter),
        #                 "text": f"{role} Prompt",
        #                 "icon": "jstree-file",
        #                 "data": {"content": text}
        #     })

        for item in reportable_content:
            # As the text part of prompt is already the tree node, we skip the text item type.
            if isinstance(item, str):
                pass
            elif item["type"] == "image_url":
                prompt_node["children"].append({
                        "id": "prompt_part_" + uuid4().hex,
                        "text": "Image Upload",
                        "icon": "jstree-file",
                        "data": {"content": item["local_path"]}
            })
            # else:
            #     append_text_child(item["text"], sub_counter)

        if append:
            print("Appending prompt node")
            self.__get_latest_conversation_node().append(prompt_node)
            self.__update_report()
        else:
            return prompt_node
        
    def report_response(self, prompt, response:LLMResponse) -> None:
        """
        Reports the LLM response.

        Args:
            response (LLMResponse): Response message from LLM.
        """
        print("Reporting Prompt Response")
        children = []
        response = response.as_dict()
        content = response["content"]
        del response["content"]
        children.append({
                        "id": "message_" + uuid4().hex,
                        "text": "Response Meta-Data",
                        "icon": "jstree-file",
                        "data": {
                            "content": response
                        }
                    })
        
        if content:
            children.append({
                            "id": "content_" + uuid4().hex,
                            "text": "Response Content",
                            "icon": "jstree-file",
                            "data": {
                                "content": content
                            }
                        })
        else:
            children.append({
                            "id": "content_" + uuid4().hex,
                            "text": "Response Content",
                            "icon": "jstree-file",
                            "data": {
                                "content": "No response content was returned by the LLM."
                            }
                        })
            
        # Appending non-LLM action requirements
        if "function_call" in response:
            children.append({
                            "id": "action_" + uuid4().hex,
                            "text": "Needs Function Call",
                            "icon": "jstree-file",
                            "data": {
                                "content": f"A function call needs to be made:\n\nFunction Name: {response['function_call']['name']} \nArguments: {response['function_call']['arguments']}"
                            }
                        })
            
        
        if prompt.role == "system":
            self.__json_data[0]["children"][0]["children"].extend(children)
        else:
            self.__get_latest_conversation_node()[-1]["children"].extend(children)       
        self.__update_report()

    def finish(self) -> None:
        """
        Finishes report creation.
        """
        if self.__show_in_browser:        
            webbrowser.open("file://" + self.__html_report_path)


        


