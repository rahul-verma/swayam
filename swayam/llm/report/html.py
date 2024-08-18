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
        self.__json_messages_path = self.__base_path + "/json"
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
    
    def __get_conversation_node(self):
        return self.__get_task_children_node()[-1]
    
    def __get_conversation_children_node(self):
        return self.__get_conversation_node()["children"]

    def __get_prompt_content_node(self):
        return self.__get_conversation_children_node()[-1]["data"]["content"]
    
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
            conversation_id = "conversation_" + uuid4().hex
            self.__get_task_children_node().append({
                                        "id": conversation_id,
                                        "text": f"{conversation.purpose}",
                                        "data": {
                                            "content": [{
                                                    "heading": "Conversation ID",
                                                    "content": conversation_id
                                                },
                                                {
                                                    "heading": "Message History",
                                                    "content": []
                                                }
                                        ]},
                                        "children": []
                                    })
            
    def report_system_prompt(self, prompt:Prompt) -> None:
        """
        Reports the system prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        log_debug("Begin: Reporting System Prompt.")

        prompt_node = {
                    "id": "prompt_" + uuid4().hex,
                    "text": f"{prompt.purpose}",
                    "icon": "jstree-file",
                    "data": {
                                "content": [{
                                                "heading": "Prompt Text",
                                                "content" : prompt.reportable_text
                                }]
                    }
        }
        self.__get_conversation_children_node().append(prompt_node)
        self.__update_report()
        log_debug("Finished: Reporting System Prompt.")
            
    def report_context(self, context:PromptContext) -> None:
        """
        Reports the context details.

        Args:
            context (PromptContext): Context object with all input messages.
        """
        log_debug("Begin: Reporting Context.")
        context_file_path = self.__json_messages_path + "/" + self.__get_conversation_node()["id"] + "_context.json"
        context_json = json.dumps(context.reportable_messages, indent=4)
        with open(context_file_path, 'w') as f:
            f.write(context_json)
        for_html = [
            {"heading": message["role"].title(), "content":message} for message in context.reportable_messages
        ]
        self.__get_conversation_node()["data"]["content"][1]["content"] = [f"{context_file_path}"] + context.reportable_messages
     
        self.__update_report()
        log_debug("Finished: Reporting Context.")

    def report_prompt(self, prompt:Prompt, role="User") -> None:
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        log_debug("Begin: Reporting Prompt.")
        prompt_node = {
                "id": "prompt_" + uuid4().hex,
                "text": f"{prompt.purpose}",
                "icon": "jstree-file",
                "data": {
                            "content": [{
                                            "heading": "Prompt Text",
                                            "content" : prompt.reportable_text
                                }]
                        },
                "children": []
        }
            
        self.__get_conversation_children_node().append(prompt_node)
        prompt_content_node = self.__get_prompt_content_node()
        
        reportable_content = prompt.reportable_content
        if type(prompt.reportable_content)  != list:
            reportable_content = [reportable_content]

        for item in reportable_content:
            # As the text part of prompt is already the tree node, we skip the text item type.
            if isinstance(item, str):
                pass
            elif item["type"] == "image_url":
                prompt_content_node.append({
                        "heading": "Image Upload",
                        "content": item["local_path"]
                })
        
        expected_response_format = prompt.response_format
        if expected_response_format is None:
            expected_response_format = "Not specified."
        else:
            expected_response_format = json.loads(expected_response_format.schema_json())

        prompt_content_node.append({
                    "heading": "Expected Response Format",
                    "content": expected_response_format
                })
        
        provided_tools = prompt.tool_dict
        if not provided_tools:
            prompt_content_node.append({
                    "heading": "Provided Tools",
                    "content": "No tool provided."
                })
        else:
            tool_content_for_main_page = {
                "heading": "Provided Tools",
                "content": {}
            }
            for tool in provided_tools.values():
                tool_content_for_main_page["content"][tool.name] = tool.definition
                
            prompt_content_node.append(tool_content_for_main_page)

        self.__update_report()
        log_debug("Finished: Reporting Prompt.")
        
    def report_response(self, prompt, response:LLMResponse) -> None:
        """
        Reports the LLM response.

        Args:
            response (LLMResponse): Response message from LLM.
        """
        log_debug("Begin: Reporting Response.")
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
        
        self.__get_prompt_content_node().append({
                    "heading": "Response Meta-Data",
                    "content": response
            })
        
        if content:
            self.__get_prompt_content_node().append({
                            "heading": "Response Content",
                            "content": content
                        })
        else:
            self.__get_prompt_content_node().append({
                    "heading": "Response Content",
                    "content": "No response content was returned by the LLM. Check the response meta-data for more details."
            })
            
        # Appending non-LLM action requirements
        if "tool_calls" in response and response["tool_calls"]:
            tool_response_for_main_page = {
                "heading": "Tool Calls Suggested by LLM",
                "content": {}
            }

            for tool in response["tool_calls"]:
                tool_response_for_main_page["content"][tool["id"]] = {
                    "name": tool["function"]["name"],
                    "arguments": json.loads(tool["function"]["arguments"])
                }
                
            self.__get_prompt_content_node().append(tool_response_for_main_page)           
            
        else:
            self.__get_prompt_content_node().append(
                {
                    "heading": "Tool Calls Suggested by LLM",
                    "content": "No suggestions."
                }
            )     
        self.__update_report()
        log_debug("Finished: Reporting Response.")
        

    def report_tool_response(self, response) -> None:
        """
        Reports the tool response.

        Args:
            message (dict): ToolResponse object
        """
        log_debug("Begin: Tool Response.")
 
        tool_response_node = {
                            "id": "tool_response_" + uuid4().hex,
                            "text": f"Tool Response: {response.tool_name}",
                            "icon": "jstree-file",
                            "data": {
                                "content": {
                                    "id": response.tool_id,
                                    "response": response.content
                                }
                            }
                        }
        
        self.__get_prompt_content_node().append(
                {
                    "heading": f"Tool Response:  {response.tool_name}",
                    "content": {
                                    "tool_id": response.tool_id,
                                    "response": response.content
                                }
                }
            )     
        self.__update_report()
        log_debug("Finished: Reporting Tool Response.")

    def finish(self) -> None:
        """
        Finishes report creation.
        """
        # !!!Should always be referred from reporting_config as it is a global object updated by Router from one execution to another.
        log_debug("Showing report in browser", self.__report_config.show_in_browser)
        if self.__report_config.show_in_browser:        
            webbrowser.open("file://" + self.__html_report_path)


        


