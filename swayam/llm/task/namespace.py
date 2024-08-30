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

class TaskDir:
    
    def __init__(self, *, role):
        self._role = role
        
    @classmethod
    def get_path_for_task(cls, *, name):
        from tarkash import Tarkash, YamlFile
        from swayam.core.constant import SwayamOption
        return os.path.join(Tarkash.get_option_value(SwayamOption.TASK_DIR), f"{name}.yaml")
    @classmethod
    def _create_purpose_from_file_name(cls, name):
        return name.replace("_", " ").lower().title()
    
    @classmethod
    def create_task_from_content(cls, name, content, **fmt_kwargs):
        from swayam import Task, Action, Request
        from swayam.llm.request.namespace import RequestDir
        from swayam.llm.request.format import RequestFormatter
        from swayam.llm.action.namespace import ActionDir
        from swayam.llm.action.format import ActionFormatter
        
        def load_system_request_from_direct_content(request):
            return RequestDir.create_request_from_content("system", f"{name}_system_request", request)
        
        def load_system_request_from_definition(definition):                
            if fmt_kwargs:
                request_file = getattr(getattr(Request.file, "system"), definition.strip())
                system_formatter = RequestFormatter(role="system", **fmt_kwargs)
                return getattr(system_formatter, request_file.file_name)
            else:
                return getattr(getattr(Request, "system"), definition.strip())
        
        def load_actions_from_direct_content(actions):
            from swayam import Generator
            
            action_objects = []
            for index, action in enumerate(actions):
                if type(action) in (dict,):
                    action_objects.append(ActionDir.create_action_from_content(f"{name}_action{index+1}", action))
                else:
                    raise ValueError(f"Invalid format of action in task file: {name}. Expected a string or a dictionary. Found: {type(action)}")
            
            return Task.actions(*action_objects, **task_kwargs)
        
        def load_actions_from_definitions(definitions):
            
            for index, definition in enumerate(definitions):
                if type(definition) not in (str, dict):
                    raise ValueError(f"Invalid format of action definition in task file: {name}. Expected a string or a dictionary. Found: {type(definition)}")
                
            action_files_or_objects = []
            for index, definition in enumerate(definitions):
                if type(definition) is str:
                    if fmt_kwargs:
                        # Load Raw Files
                        action_files_or_objects.append(getattr(Action.file, definition.strip()))
                    else:
                        # Load as Objects
                        action_files_or_objects.append(getattr(Action, definition.strip()))
                elif type(definition) is dict:
                    if "repeat" in definition:
                        from swayam import Generator
                        gdict = {"generator":None, "args":{}}
                        gdict.update(definition["repeat"])
                        generator_name = definition["repeat"].get("generator", None)
                        generator = getattr(Generator, generator_name)(**gdict["args"])
                        dynamic_file = (getattr(Action.repeater(generator=generator), definition["name"].strip()))
                        action_files_or_objects.append(dynamic_file)

            if fmt_kwargs:
                return Task.formatter(**fmt_kwargs).action_files(*action_files_or_objects, **task_kwargs)
            else:
                return Task.actions(*action_files_or_objects, **task_kwargs) 
            
        task_kwargs ={
            "purpose": content.get("purpose", cls._create_purpose_from_file_name(name)),
            "system_request": content.get("system_request", None),
            "image": content.get("image", None),
            "output_structure": content.get("output_structure", None),
            "tools": content.get("tools", None)
        }
        
        if type(content) is not dict:
            raise TypeError(f"Invalid format of task file: {name}. Expected a YAML dictionary with the allowed keys: [system_request, system_request_def, actions, action_defs, purpose, image, output_structure, tools]")  
        
        if "actions" in content and "action_defs" in content:
            raise ValueError(f"A task file cannot contain both 'actions' and 'action_defs' keys. Choose one.")
        
        if "system_request" in content and "system_request_def" in content:
            raise ValueError(f"A task file cannot contain both 'system_request' and 'system_request_def' keys. Choose one.")
        
        if "system_request" in content:
            if type(content["system_request"]) is not str:
                raise ValueError(f"The system_request key in a action file must be a string. Found: {type(content['system_request'])}") 
            task_kwargs["system_request"] = load_system_request_from_direct_content(content["system_request"])
        elif "system_request_def" in content:
            if type(content["system_request_def"]) is not str:
                raise ValueError(f"The system_request_def key in a action file must be a string. Found: {type(content['system_request_def'])}") 
            task_kwargs["system_request"]  = load_system_request_from_definition(content["system_request_def"])

        for key, allowed_type in [("purpose", str), ("image", str), ("output_structure",str), ("tools", list)]:
            if key in content:
                if type(content[key]) is not allowed_type:
                    raise ValueError(f"Invalid format of '{key}' key in action file: {name}. Expected a {allowed_type}. Found: {type(content[key])}")
        
        if "actions" in content:
            if type(content["actions"]) is not list:
                raise ValueError(f"The actions key in a task file must contain a list. Found: {type(content['actions'])}") 
            return load_actions_from_direct_content(content["actions"])
        elif "action_defs" in content:
            if type(content["action_defs"]) is not list:
                raise ValueError(f"The action_defs key in a task file must contain a list. Found: {type(content['action_defs'])}") 
            return load_actions_from_definitions(content["action_defs"])
        else:
            raise ValueError(f"A task file must contain either a 'actions' or 'action_defs' key.") 

    @classmethod    
    def load_task_from_file(cls, name):
        from tarkash import YamlFile        
        file = YamlFile(cls.get_path_for_task(name=name))
        return cls.create_task_from_content(name, file.content)