# This file is a part of Tarkash
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

"""
[
            {
                "id": "task",
                "text": "Task: What is the difference between LangChain and LangSmith",
                "children": false
            },
            {
                "id": "plan",
                "text": "Plan",
                "children": [
                    {
                        "id": "plan_0",
                        "text": "Introduction",
                        "icon": "jstree-file",
                        "data": {
                            "content": "LangChain and LangSmith are tools used in AI language processing. This document compares and contrasts their features."
                        }
                    },
                    {
                        "id": "plan_1",
                        "text": "Overview of LangChain",
                        "icon": "jstree-file",
                        "data": {
                            "content": "LangChain is a tool designed for chaining multiple language models and processing tasks."
                        }
                    },
                    {
                        "id": "plan_2",
                        "text": "Overview of LangSmith",
                        "icon": "jstree-file",
                        "data": {
                            "content": "LangSmith, on the other hand, is focused on integrating and orchestrating language tasks with more customizable options."
                        }
                    },
                    {
                        "id": "plan_3",
                        "text": "Comparison",
                        "icon": "jstree-file",
                        "data": {
                            "content": "While both tools aim to facilitate language processing, LangChain is more general-purpose, whereas LangSmith provides more granular control."
                        }
                    }
                ]
            }
        ]
"""

import json
class PromptSessionHtmlReporter:
    """
    Reports the prompt session details to a file.
    """
    
    def __init__(self, name, **kwargs):
        """
        Initializes the PromptSessionReporter with the provided name.
        """
        from tarkash import Tarkash
        from swayam.type.constant import SwayamOption
        self.__base_path = os.path.join(Tarkash.get_option_value(SwayamOption.REPORT_ROOT_DIR), name)
        self.__json_path = self.__base_path + "/json/data.json"
        print(self.__json_path)
        self.__json_list = [
            
        ]
        self.__counter = -1
        with open(self.__json_path, 'w') as f:
            s = json.dumps(self.__json_list)
            f.write(s)
        
    def report_prompt(self, prompt):
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        self.__counter += 1
        self.__json_list.append(
        {
                "id": "prompt_" + str(self.__counter),
                "text": "Prompt::" + str(self.__counter),
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
        with open(self.__json_path, 'w') as f:
            s = json.dumps(self.__json_list)
            f.write(s)
        
    def report_output(self, message):
        children = []
        children.append({
                        "id": "message",
                        "text": "Response Message",
                        "icon": "jstree-file",
                        "data": {
                            "content": message.to_dict()
                        }
                    })
        
        children.append({
                        "id": "content",
                        "text": "Response Content",
                        "icon": "jstree-file",
                        "data": {
                            "content": message.content
                        }
                    })
        self.__json_list[-1]["children"].append(children)
        with open(self.__json_path, 'w') as f:
            s = json.dumps(self.__json_list)
            f.write(s)
        
