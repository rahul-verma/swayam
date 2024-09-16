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

from swayam.llm.phase.prompt import Prompt
from swayam.llm.phase.expression.conversation import Conversation
from swayam.llm.phase.prompt.response import LLMResponse
from swayam.llm.record import Reporter

class HtmlRecorder(Reporter):
    
    def __init__(self, config):
        super().__init__()
        self.__recorder_config = config
        
        from tarkash import Tarkash, TarkashOption
        from swayam import Swayam
        from swayam.core.constant import SwayamOption
        
        # For JSON Data
        
        # Don't vault the narration, always get it from config.
        record_dir = Tarkash.get_option_value(SwayamOption.FOLIO_NARRATION_DIR)
        self.__base_path = os.path.join(record_dir, str(self.__recorder_config.narration))
        os.makedirs(self.__base_path, exist_ok=True)
        self.__json_path = self.__base_path + "/json/data.json"
        self.__json_messages_path = self.__base_path + "/json"
        os.makedirs(self.__base_path +"/json", exist_ok=True)
        
        # For HTML Report
        self.__html_record_path = self.__base_path + "/narration.html"
        log_debug("Report Path:", self.__html_record_path)
        template_path = Swayam._get_swayam_res_path("llm_narration_template.html")
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
        
        # So far the report has only one plan node with one thought node.

    def __get_story_children_node(self):
        return self.__json_data[-1]["children"]
    
    def __get_thought_children_node(self):
        return self.__get_story_children_node()[-1]["children"]
    
    def __get_expression_node(self):
        return self.__get_thought_children_node()[-1]
    
    def __get_expression_children_node(self):
        return self.__get_expression_node()["children"]

    def __get_prompt_content_node(self):
        return self.__get_expression_children_node()[-1]["data"]["content"]
    
    def increment_expression_node(self):
        self.__current_expression_node_index += 1
            
    def __update_report(self):
        json_str = json.dumps(self.__json_data, indent=4)
        with open(self.__json_path, 'w') as f:
            f.write(json_str)
        
        with open(self.__html_record_path, 'w') as f:
            html = self.__template.replace("$$SWAYAM_JSON_DATA$$", json_str)
            f.write(html)
            
    def record_begin_story(self, story) -> None:
        """
        Broadcasts the story details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        if self.__json_data == []:
            # Add Story Node
            self.__json_data.append({
                                    "id": "story_node_" + uuid4().hex,
                                    "text": story.purpose,
                                    "children": []   
                                })
        self.__update_report()
            
    def record_begin_thought(self, thought) -> None:
        """
        Broadcasts the system prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        if self.__json_data == []:
            # Add Story Node
            self.__json_data.append({
                                    "id": "story_node_" + uuid4().hex,
                                    "text": "Story",
                                    "children": []   
                                })
            
        # The Thought node
        self.__get_story_children_node().append({
                                    "id": "thought_node_" + uuid4().hex,
                                    "text": f"{thought.purpose}",
                                    "children": []
                                })
        self.__update_report()
            
    def record_begin_expression(self, expression=None) -> None:
        """
        Broadcasts the system prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        
        if self.__json_data == []:
            # Add Story Node
            self.__json_data.append({
                                    "id": "story_node_" + uuid4().hex,
                                    "text": "Story",
                                    "children": []   
                                })
            
            # The Thought node
            self.__get_story_children_node().append({
                                        "id": "thought_node_" + uuid4().hex,
                                        "text": "Thought",
                                        "children": []
                                    })

        if not expression:
            expression_purpose = "Expression"
        else:
            expression_purpose = expression.purpose
        expression_id = "expression_" + uuid4().hex
        self.__get_thought_children_node().append({
                                    "id": expression_id,
                                    "text": f"{expression_purpose}",
                                    "data": {
                                        "content": []
                                    },
                                    "children": []
                                })

        if expression.directive:
            self.__get_expression_node()["data"]["content"].append({
                "heading": "Directive Text",
                "content": expression.directive
            })
        self.__update_report()
        log_debug("Finished: Reporting  Directive.")
        self.__update_report()

    def record_prompt(self, prompt:Prompt, conversation, role="User") -> None:
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        log_debug("Begin: Reporting Prompt.")
        prompt_id = "prompt_" + uuid4().hex
        prompt_node = {
                "id": prompt_id,
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
            
        self.__get_expression_children_node().append(prompt_node)
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
        
        expected_out_template = prompt.out_template
        if expected_out_template is not None:
            prompt_content_node.append({
                        "heading": "Data Template",
                        "content": expected_out_template.definition
                    })
        
        provided_actions = prompt.action_dict
        if provided_actions:
            action_content_for_main_page = {
                "heading": "Provided Actions",
                "content": {}
            }
            for action in provided_actions.values():
                action_content_for_main_page["content"][action.name] = action.definition
                
            prompt_content_node.append(action_content_for_main_page)
            
        debug = os.environ.get("SWAYAM_DEBUG", "false")
        if debug.lower() != "true":
            messages = conversation.reportable_messages[3:]
        else:
            messages = conversation.reportable_messages
        
        log_debug("Begin: Reporting Narrative.")
        conversation_file_path = self.__json_messages_path + "/" + prompt_id + "_conversation.json"
        conversation_json = json.dumps(messages, indent=4)
        with open(conversation_file_path, 'w') as f:
            f.write(conversation_json)
        
        conversation_html = action_content_for_main_page = {
                "heading": "Conversation",
                "content": [f"{conversation_file_path}"] + messages
            }
        prompt_content_node.append(conversation_html)
        self.__update_report()
        log_debug("Finished: Reporting Prompt.")
        
    def record_response(self, prompt, response:LLMResponse) -> None:
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

        # print("Response:", response)
        # if response["refusal"] is not None:
        #     self.__get_prompt_content_node().append({
        #                 "heading": "Response Meta-Data",
        #                 "content": response
        #         })
        
        if content:
            self.__get_prompt_content_node().append({
                            "heading": "Response Content",
                            "content": content
                        })
            
        # Appending non-LLM expression requirements
        if "tool_calls" in response and response["tool_calls"]:
            action_response_for_main_page = {
                "heading": "Action Calls Suggested by LLM",
                "content": {}
            }
 
            for action in response["tool_calls"]:
                action_response_for_main_page["content"][action["id"]] = {
                    "name": action["function"]["name"],
                    "arguments": json.loads(action["function"]["arguments"])
                }
                
            self.__get_prompt_content_node().append(action_response_for_main_page)           
    
        self.__update_report()
        log_debug("Finished: Reporting Response.")
        

    def record_action_response(self, response) -> None:
        """
        Reports the action response.

        Args:
            message (dict): ActionResponse object
        """
        log_debug("Begin: Action Response.")
        
        self.__get_prompt_content_node().append(
                {
                    "heading": f"Action Response:  {response.action_name}",
                    "content": {
                                    "action_id": response.action_id,
                                    "response": response.content
                                }
                }
            )     
        self.__update_report()
        log_debug("Finished: Reporting Action Response.")

    def finish(self) -> None:
        """
        Finishes report creation.
        """
        pass
    
    def reset(self) -> None:
        """
        Resets the report.
        """
        self.__json_data = []
        self.__update_report()


