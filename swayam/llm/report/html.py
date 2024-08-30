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

from swayam.llm.request import Request
from swayam.llm.action.context import ActionContext
from swayam.llm.request.response import LLMResponse
from swayam.llm.report import Reporter

class HtmlReporter(Reporter):
    
    def __init__(self, config):
        super().__init__()
        self.__report_config = config
        
        from tarkash import Tarkash, TarkashOption
        from swayam import Swayam
        
        # For JSON Data
        
        # Don't store the run_id, always get it from config.
        report_dir = Tarkash.get_option_value(TarkashOption.REPORT_DIR)
        self.__base_path = os.path.join(report_dir, str(self.__report_config.run_id))
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
            with open(self.__json_path, 'w') as f:
                f.write("[]")
        else:
            log_debug("Found existing report.")
            with open(self.__json_path, 'r') as f:
                self.__json_data = json.load(f)
        self.__update_report()
        
        # So far the report has only one plan node with one task node.

    def __get_strategy_children_node(self):
        return self.__json_data[-1]["children"]
    
    def __get_task_children_node(self):
        return self.__get_strategy_children_node()[-1]["children"]
    
    def __get_action_node(self):
        return self.__get_task_children_node()[-1]
    
    def __get_action_children_node(self):
        return self.__get_action_node()["children"]

    def __get_request_content_node(self):
        return self.__get_action_children_node()[-1]["data"]["content"]
    
    def increment_action_node(self):
        self.__current_action_node_index += 1
            
    def __update_report(self):
        json_str = json.dumps(self.__json_data, indent=4)
        with open(self.__json_path, 'w') as f:
            f.write(json_str)
        
        with open(self.__html_report_path, 'w') as f:
            html = self.__template.replace("$$SWAYAM_JSON_DATA$$", json_str)
            f.write(html)
            
    def report_begin_action(self, action) -> None:
        """
        Broadcasts the system request details.
        
        Args:
            request (Request): The request to report.
        """
        
        if self.__json_data == []:
            # Add Strategy Node
            self.__json_data.append({
                                    "id": "strategy_node_" + uuid4().hex,
                                    "text": "Strategy",
                                    "children": []   
                                })
            
            # The Task node
            self.__get_strategy_children_node().append({
                                        "id": "task_node_" + uuid4().hex,
                                        "text": "Task",
                                        "children": []
                                    })

        action_id = "action_" + uuid4().hex
        self.__get_task_children_node().append({
                                    "id": action_id,
                                    "text": f"{action.purpose}",
                                    "data": {
                                        "content": [{
                                                "heading": "Action ID",
                                                "content": action_id
                                            },
                                            {
                                                "heading": "Message History",
                                                "content": []
                                            }
                                    ]},
                                    "children": []
                                })
            
    def report_system_request(self, request:Request) -> None:
        """
        Reports the system request details.
        
        Args:
            request (Request): The request to report.
        """
        log_debug("Begin: Reporting System Request.")

        request_node = {
                    "id": "request_" + uuid4().hex,
                    "text": f"{request.purpose}",
                    "icon": "jstree-file",
                    "data": {
                                "content": [{
                                                "heading": "Request Text",
                                                "content" : request.reportable_text
                                }]
                    }
        }
        self.__get_action_children_node().append(request_node)
        self.__update_report()
        log_debug("Finished: Reporting System Request.")
            
    def report_context(self, context:ActionContext) -> None:
        """
        Reports the context details.

        Args:
            context (ActionContext): Context object with all input messages.
        """
        
        if self.__json_data == []:
            from swayam import Action
            self.report_begin_action(Action.texts("Hi"))
        
        log_debug("Begin: Reporting Context.")
        context_file_path = self.__json_messages_path + "/" + self.__get_action_node()["id"] + "_context.json"
        context_json = json.dumps(context.reportable_messages, indent=4)
        with open(context_file_path, 'w') as f:
            f.write(context_json)
        for_html = [
            {"heading": message["role"].title(), "content":message} for message in context.reportable_messages
        ]
        self.__get_action_node()["data"]["content"][1]["content"] = [f"{context_file_path}"] + context.reportable_messages
     
        self.__update_report()
        log_debug("Finished: Reporting Context.")

    def report_request(self, request:Request, role="User") -> None:
        """
        Reports the request details.
        
        Args:
            request (Request): The request to report.
        """
        log_debug("Begin: Reporting Request.")
        request_node = {
                "id": "request_" + uuid4().hex,
                "text": f"{request.purpose}",
                "icon": "jstree-file",
                "data": {
                            "content": [{
                                            "heading": "Request Text",
                                            "content" : request.reportable_text
                                }]
                        },
                "children": []
        }
            
        self.__get_action_children_node().append(request_node)
        request_content_node = self.__get_request_content_node()
        
        reportable_content = request.reportable_content
        if type(request.reportable_content)  != list:
            reportable_content = [reportable_content]

        for item in reportable_content:
            # As the text part of request is already the tree node, we skip the text item type.
            if isinstance(item, str):
                pass
            elif item["type"] == "image_url":
                request_content_node.append({
                        "heading": "Image Upload",
                        "content": item["local_path"]
                })
        
        expected_output_structure = request.output_structure
        if expected_output_structure is None:
            expected_output_structure = "Not specified."
        else:
            expected_output_structure = expected_output_structure.data_model.model_json_schema()

        request_content_node.append({
                    "heading": "Expected Response Format",
                    "content": expected_output_structure
                })
        
        provided_tools = request.tool_dict
        if not provided_tools:
            request_content_node.append({
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
                
            request_content_node.append(tool_content_for_main_page)

        self.__update_report()
        log_debug("Finished: Reporting Request.")
        
    def report_response(self, request, response:LLMResponse) -> None:
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
        
        self.__get_request_content_node().append({
                    "heading": "Response Meta-Data",
                    "content": response
            })
        
        if content:
            self.__get_request_content_node().append({
                            "heading": "Response Content",
                            "content": content
                        })
        else:
            self.__get_request_content_node().append({
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
                
            self.__get_request_content_node().append(tool_response_for_main_page)           
            
        else:
            self.__get_request_content_node().append(
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
        
        self.__get_request_content_node().append(
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
        # !!!Should always be referred from reporting_config as it is a global object updated by Agent from one execution to another.
        log_debug("Showing report in browser", self.__report_config.show_in_browser)
        if self.__report_config.show_in_browser:        
            webbrowser.open("file://" + self.__html_report_path)


        


