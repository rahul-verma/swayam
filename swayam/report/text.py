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

class PromptSessionTextReporter:
    """
    Reports the prompt session details to console.
    """
    
    def __init__(self, name, **kwargs):
        """
        Initializes the PromptSessionReporter with the provided name.
        """
        pass
        
    def report_prompt(self, prompt):
        """
        Reports the prompt details.
        
        Args:
            prompt (Prompt): The prompt to report.
        """
        self.__counter += 1
        self.__json_list.append({
                "id": "prompt_" + str(self.__counter),
                "text": "Prompt::" + str(self.__counter),
                "data": {
                            "content": prompt
                        }
                "children": [
                    {
                        "id": "prompt_text_" + str(self.__counter),
                        "text": "Prompt",
                        "icon": "jstree-file",
                        "data": {
                            "content": prompt
                    }
                ]
        })
        with open(self.__json_path, 'w') as f:
            f.write(str(self.__json_list))
        
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
            f.write(str(self.__json_list))
        
