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

import json
from json import JSONDecodeError
from enum import Enum
from typing import *

from pydantic import BaseModel, create_model, Field
from swayam.inject.structure.structure import IOStructureObject, IOStructureObjectList
from swayam.inject.structure.error import StructureValidationError
from swayam.inject.structure.builtin import JsonContent, JsonContentList

from .error import *

class StructuredParser:
    
    def __init__(self, name, *, kallable, input_structure, content_structure, output_structure):
        self.__name = name
        self.__kallable = kallable
        self.__input_structure = input_structure
        self.__content_structure = content_structure
        self.__output_structure = output_structure
        
    @property
    def name(self):
        return self.__name
    
    @property
    def kallable(self):
        return self.__kallable
    
    @property
    def input_structure(self):
        return self.__input_structure
    
    @property
    def content_structure(self):
        return self.__content_structure
    
    @property
    def output_structure(self):
        return self.__output_structure

    def __call__(self, content, **kwargs):
        # Check call structure adherence
        kwargs["content"] = content
        kwargs = self.input_structure(**kwargs).as_dict()

        # Trigger any pre-processing before call is made to the kallable
        kwargs = self.modify_kwargs_before_call_to_callable(**kwargs)
        
        ## Add self reference to kwargs
        kwargs["parser"] = self
        
        # Actual call
        output = self.__kallable(**kwargs)
        
        if isinstance(output, IOStructureObject):
            output = output.as_dict()
        elif isinstance(output, IOStructureObjectList):
            output = output.as_list()
            if self.__output_structure.is_atomic():
                output = output[0]
        else:
            if self.__output_structure.is_atomic():
                if isinstance(output, dict):
                    output = self.__output_structure(**output).as_dict()
                else:
                    output = self.__output_structure(**output[0]).as_dict()
            else:
                output = self.__output_structure(*output).as_list()

        output = self.modify_output_before_return(output)
        return output
    
    def modify_kwargs_before_call_to_callable(self, **kwargs):
        return kwargs
    
    def modify_output_before_return(self, output):
        return output

class TextContentParser(StructuredParser):
    
    def __init__(self, name, *, kallable, input_structure=None, output_structure=None):
        from swayam.inject.structure.builtin import TextContent
        if input_structure is None:
            input_structure = TextContent
        super().__init__(name, kallable=kallable, input_structure=input_structure, output_structure=output_structure, content_structure=None)

class JsonContentParser(StructuredParser):
    
    def __init__(self, name, *, kallable, content_structure=None, output_structure=None, input_structure=None):
        from swayam.inject.structure.builtin import JsonContent, JsonContentList
        if input_structure is None:
            input_structure = JsonContent
        first_level_output_structure = JsonContentList
        if output_structure is not None:
            if output_structure.is_atomic():
                first_level_output_structure = JsonContent
        super().__init__(name, 
                         kallable=kallable, 
                         input_structure=input_structure,output_structure=first_level_output_structure,
                         content_structure=content_structure)
        self.__content_structure = content_structure
        self.__output_structure = output_structure

    def __call__(self, *, content, **kwargs):
        from swayam.inject.structure.builtin import JsonContent
        if not isinstance(content, str):
            content = json.dumps(content)
        try:
            json_str = JsonContent(content=content).as_dict()["content"]
        except ValueError as e:
            raise ParserCallError(self.name, error=f'Invalid json_text content. Expected valid Json: {e}')
        else:
            kwargs["content"] = json_str
            return super().__call__(**kwargs)

        
    def modify_kwargs_before_call_to_callable(self, **kwargs):
        json_str = kwargs["content"]
        if self.__content_structure is None:
            json_object = json.loads(json_str)
            kwargs["content"] = json_object
        else:
            def get_content_validated_json(in_json_str):
                if self.__content_structure in (JsonContent, JsonContentList):
                    return in_json_str
                else:
                    return self.__content_structure(**json.loads(kwargs["content"])).as_dict()
            if self.__content_structure.is_atomic():
                kwargs["content"] = get_content_validated_json(kwargs["content"])
            else:
                validated_list = [get_content_validated_json(item) for item in json.loads(kwargs["content"])]
                kwargs["content"] = validated_list
        return kwargs
    
    def modify_output_before_return(self, output):
        if self.__output_structure is None:
            if isinstance(output, str):
                return json.loads(output)
            elif isinstance(output, dict):
                output["content"] = json.loads(output["content"])
                return output
            elif isinstance(output, list):
                final = []
                for item in output:
                    item["content"] = json.loads(item["content"])
                    final.append(item)
                return final
            else:
                raise ParserCallError(self.name, error="Output structure not defined and the structure of the provided content does not match the parsing requirement.")

        if self.__output_structure.is_atomic():
            if not isinstance(output, dict):
                raise ParserCallError("Parser", error=f"Expected a dictionary for creating {self.__output_structure.name} structure.")
            output["content"] = self.__output_structure(**json.loads(output["content"])).as_dict()
            return output
        else:
            final_output = []
            if not isinstance(output, list):
                output = [output]
            for item in output:
                if not isinstance(item, dict):
                    raise ParserCallError("Parser", error=f"Expected a dictionary for creating {self.__output_structure.name} structure.")
                elif "content" not in item:
                    raise ParserCallError("Parser", error=f"Expected a dictionary with 'content' key for creating {self.__output_structure.name} structure.")
                
                try:
                    json.loads(item["content"])
                except JSONDecodeError as e:
                    raise ParserCallError("Parser", error=f"Invalid Json content. Expected valid Json for content key. Found: >>{item['content']}<<.")

                item["content"] = self.__output_structure(**json.loads(output["content"])).as_dict()
                final_output.append(item) 

            return output
    

