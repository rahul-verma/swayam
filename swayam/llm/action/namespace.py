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

class ActionDir:
    
    def __init__(self, *, role):
        self._role = role
        
    @classmethod
    def get_path_for_action(cls, *, name):
        from tarkash import Tarkash, YamlFile
        from swayam.core.constant import SwayamOption
        return os.path.join(Tarkash.get_option_value(SwayamOption.ACTION_DIR), f"{name}.yaml")
    @classmethod
    def _create_purpose_from_file_name(cls, name):
        return name.replace("_", " ").lower().title()
    
    @classmethod
    def create_action_from_content(cls, name, content, **fmt_kwargs):
        from swayam import Action , Request
        from swayam.llm.request.namespace import RequestDir
        from swayam.llm.request.format import RequestFormatter
        
        def load_requests_from_direct_content(role, requests):
            

            request_objects = []
            for index, request in enumerate(requests):
                counter = ""
                if role == "user":
                    counter = f"_{index+1}"
                if type(request) in (str, dict):
                    request_objects.append(RequestDir.create_request_from_content(role, f"{name}_{role}_request{counter}", request))
                else:
                    raise ValueError(f"Invalid format of user request in action file: {name}. Expected a string or a dictionary. Found: {type(request)}")
            if role == "user":
                return Action.requests(*request_objects, **action_kwargs)
            else:
                return request_objects[0]
        
        def load_requests_from_definitions(role, definitions):
            
            for index, definition in enumerate(definitions):
                if type(definition) is not str:
                    raise ValueError(f"Invalid format of request definition in action file: {name}. Expected a string. Found: {type(definition)}")
                
            if fmt_kwargs:
                request_files = []
                for index, definition in enumerate(definitions):
                    request_files.append(getattr(getattr(Request.file, role), definition.strip()))
                if role == "user":
                    return Action.formatter(**fmt_kwargs).request_files(*request_files, **action_kwargs)
                else:
                    system_formatter = RequestFormatter(role=role, **fmt_kwargs)
                    return getattr(system_formatter, request_files[0].file_name)
            else:
                request_objects = []
                for index, definition in enumerate(definitions):
                    request_objects.append(getattr(getattr(Request, role), definition.strip()))
                if role == "user":
                    return Action.requests(*request_objects, **action_kwargs) 
                else:
                    return request_objects[0]
            
        action_kwargs ={
            "purpose": content.get("purpose", cls._create_purpose_from_file_name(name)),
            "system_request": content.get("system_request", None),
            "image": content.get("image", None),
            "output_structure": content.get("output_structure", None),
            "tools": content.get("tools", None),
            "reset_context": content.get("reset_context", True),
            "standalone": content.get("standalone", False),
            "store_response_as": content.get("store_response_as", None),
        }
        
        if type(content) is not dict:
            raise TypeError(f"Invalid format of action file: {name}. Expected a YAML dictionary with the allowed keys: [system_request, requests, request_defs, purpose, image, output_structure, tools]")  
        
        if "requests" in content and "request_defs" in content:
            raise ValueError(f"A action file cannot contain both 'requests' and 'request_defs' keys. Choose one.")
        
        if "system_request" in content and "system_request_def" in content:
            raise ValueError(f"A action file cannot contain both 'system_request' and 'system_request_def' keys. Choose one.")
        
        # System Request
        if action_kwargs["system_request"] is not None and type(action_kwargs["system_request"]) is not str:
            raise ValueError(f"Invalid format of 'system_request' key in action file: {name}. Expected a string. Found: {type(action_kwargs['system_request'])}")
        
        if "system_request" in content:
            if type(content["system_request"]) is not str:
                raise ValueError(f"The system_request key in a action file must be a string. Found: {type(content['system_request'])}") 
            action_kwargs["system_request"] = load_requests_from_direct_content("system", [content["system_request"]])
        elif "system_request_def" in content:
            if type(content["system_request_def"]) is not str:
                raise ValueError(f"The system_request_def key in a action file must be a string. Found: {type(content['system_request_def'])}") 
            action_kwargs["system_request"]  = load_requests_from_definitions("system", [content["system_request_def"]])
                   
        """
        *requests:UserRequest, purpose:str=None, system_request:Union[str,SystemRequest]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None)
        """
        for key, allowed_type in [("purpose", str), ("image", str), ("output_structure",str), ("tools", list)]:
            if key in content:
                if type(content[key]) is not allowed_type:
                    raise ValueError(f"Invalid format of '{key}' key in action file: {name}. Expected a {allowed_type}. Found: {type(content[key])}")
        
        if "requests" in content:
            if type(content["requests"]) is not list:
                raise ValueError(f"The requests key in a action file must contain a list. Found: {type(content['requests'])}") 
            return load_requests_from_direct_content("user", content["requests"])
        elif "request_defs" in content:
            if type(content["request_defs"]) is not list:
                raise ValueError(f"The request_defs key in a action file must contain a list. Found: {type(content['request_defs'])}") 
            return load_requests_from_definitions("user", content["request_defs"])
        else:
            raise ValueError(f"A action file must contain either a 'requests' or 'request_defs' key.") 

    @classmethod    
    def load_action_from_file(cls, name):
        from tarkash import YamlFile        
        file = YamlFile(cls.get_path_for_action(name=name))
        return cls.create_action_from_content(name, file.content)