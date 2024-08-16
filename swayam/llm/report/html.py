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
from pprint import pprint
import copy

from tarkash import log_debug

from swayam.llm.prompt import Prompt
from swayam.llm.conversation.context import PromptContext
from swayam.llm.prompt.response import LLMResponse
from swayam.llm.report import Reporter

class HtmlReporter(Reporter):
    
    def __init__(self, config):
        super().__init__()
        self.__report_config = config
        
        from tarkash import Tarkash
        from swayam import Swayam
        from swayam.core.constant import SwayamOption
        
        # For JSON Data
        
        # Don't store the run_id, always get it from config.
        self.__base_path = os.path.join(Tarkash.get_option_value(SwayamOption.REPORT_ROOT_DIR), str(self.__report_config.run_id))
        os.makedirs(self.__base_path, exist_ok=True)
        self.__json_path = self.__base_path + "/json/data.json"
        os.makedirs(self.__base_path +"/json", exist_ok=True)
        
        # For HTML Report
        self.__html_report_path = self.__base_path + "/report.html"
        log_debug("Report Path:", self.__html_report_path)
        template_path = Swayam._get_swayam_res_path("llm_report_template.html")
        self.__template = ""
        with open(template_path, 'r') as f:
            self.__template = f.read()
        self.__res_path = os.path.join(os.path.realpath(__file__), "..")
        self.__json_data = []
        if not os.path.exists(self.__json_path):
            log_debug("It's a new report.")
            self.__json_data = []
        else:
            log_debug("Found existing report.")
            with open(self.__json_path, 'r') as f:
                self.__json_data = json.load(f)
        self.__update_report()
        
        # So far the report has only one plan node with one task node.

    def __get_plan_children_node(self):
        return self.__json_data[-1]["children"]
    
    def __get_task_children_node(self):
        return self.__get_plan_children_node()[-1]["children"]
    
    def __get_conversation_children_node(self):
        return self.__get_task_children_node()[-1]["children"]
    
    def __get_prompt_children_node(self):
        return self.__get_conversation_children_node()[-1]["children"]
    
    def increment_conversation_node(self):
        self.__current_conversation_node_index += 1
            
    def __update_report(self):
        json_str = json.dumps(self.__json_data, indent=4)
        with open(self.__json_path, 'w') as f:
            f.write(json_str)
        
        with open(self.__html_report_path, 'w') as f:
            html = self.__template.replace("$$SWAYAM_JSON_DATA$$", json_str)
            f.write(html)
            
    def report_begin_conversation(self, conversation) -> None:
        """
        Broadcasts the system prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        
        if self.__json_data == []:
            # Add Plan Node
            self.__json_data.append({
                                    "id": "plan_node_" + uuid4().hex,
                                    "text": "Plan",
                                    "children": []   
                                })
            
            # The Task node
            self.__get_plan_children_node().append({
                                        "id": "task_node_" + uuid4().hex,
                                        "text": "Task",
                                        "children": []
                                    })
        
        if conversation.is_new():
            self.__get_task_children_node().append({
                                        "id": "conversation_node_" + uuid4().hex,
                                        "text": "Conversation",
                                        "children": []
                                    })
            
    def report_system_prompt(self, prompt:Prompt) -> None:
        """
        Reports the system prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        log_debug("Begin: Reporting System Prompt.")


        
        # The system prompt node it as index 0
        prompt_node = self.report_prompt(prompt, role="System")
        self.__update_report()
        log_debug("Finished: Reporting System Prompt.")
            
    def report_context(self, context:PromptContext) -> None:
        """
        Reports the context details.

        Args:
            context (PromptContext): Context object with all input messages.
        """
        log_debug("Begin: Reporting Context.")
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
        self.__get_conversation_children_node().append(context_node)        
        self.__update_report()
        log_debug("Finished: Reporting Context.")

    def report_prompt(self, prompt:Prompt, role="User") -> None:
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """

        log_debug("Begin: Reporting Prompt.")
        if role == "User":
            prompt_node = {
                    "id": "prompt_" + uuid4().hex,
                    "text": f"{role} Prompt",
                    "data": {
                                "content": prompt.reportable_text
                            },
                    "children": []
            }
        else:
             prompt_node = {
                    "id": "prompt_" + uuid4().hex,
                    "text": f"{role} Prompt",
                    "data": {
                                "content": prompt.reportable_text
                            }
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

        self.__get_conversation_children_node().append(prompt_node)
        self.__update_report()
        log_debug("Finished: Reporting Prompt.")
        
    def report_response(self, prompt, response:LLMResponse) -> None:
        """
        Reports the LLM response.

        Args:
            response (LLMResponse): Response message from LLM.
        """
        log_debug("Finished: Reporting Response.")
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
            
        
        self.__get_prompt_children_node().extend(children)       
        self.__update_report()
        log_debug("Finished: Reporting Response.")

    def finish(self) -> None:
        """
        Finishes report creation.
        """
        # !!!Should always be referred from reporting_config as it is a global object updated by Router from one execution to another.
        log_debug("Showing report in browser", self.__report_config.show_in_browser)
        if self.__report_config.show_in_browser:        
            webbrowser.open("file://" + self.__html_report_path)


        


