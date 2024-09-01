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

class ThoughtDir:
    
    def __init__(self, *, role):
        self._role = role
        
    @classmethod
    def get_path_for_thought(cls, *, name):
        from tarkash import Tarkash, YamlFile
        from swayam.core.constant import SwayamOption
        return os.path.join(Tarkash.get_option_value(SwayamOption.THOUGHT_DIR), f"{name}.yaml")
    @classmethod
    def _create_purpose_from_file_name(cls, name):
        return name.replace("_", " ").lower().title()
    
    @classmethod
    def create_thought_from_content(cls, name, content, **fmt_kwargs):
        from swayam import Thought, Expression, Prompt
        from swayam.llm.prompt.namespace import PromptDir
        from swayam.llm.prompt.format import PromptFormatter
        from swayam.llm.expression.namespace import ExpressionDir
        from swayam.llm.expression.format import ExpressionFormatter
        
        def load_system_prompt_from_direct_content(prompt):
            return PromptDir.create_prompt_from_content("system", f"{name}_system_prompt", prompt)
        
        def load_system_prompt_from_definition(definition):                
            if fmt_kwargs:
                prompt_file = getattr(getattr(Prompt.file, "system"), definition.strip())
                system_formatter = PromptFormatter(role="system", **fmt_kwargs)
                return getattr(system_formatter, prompt_file.file_name)
            else:
                return getattr(getattr(Prompt, "system"), definition.strip())
        
        def load_expressions_from_direct_content(expressions):
            from swayam import Generator
            
            expression_objects = []
            for index, expression in enumerate(expressions):
                if type(expression) in (dict,):
                    expression_objects.append(ExpressionDir.create_expression_from_content(f"{name}_expression{index+1}", expression))
                else:
                    raise ValueError(f"Invalid format of expression in thought file: {name}. Expected a string or a dictionary. Found: {type(expression)}")
            
            return Thought.expressions(*expression_objects, **thought_kwargs)
        
        def load_expressions_from_definitions(definitions):
            
            for index, definition in enumerate(definitions):
                if type(definition) not in (str, dict):
                    raise ValueError(f"Invalid format of expression definition in thought file: {name}. Expected a string or a dictionary. Found: {type(definition)}")
                
            expression_files_or_objects = []
            for index, definition in enumerate(definitions):
                if type(definition) is str:
                    if fmt_kwargs:
                        # Load Raw Files
                        expression_files_or_objects.append(getattr(Expression.file, definition.strip()))
                    else:
                        # Load as Objects
                        expression_files_or_objects.append(getattr(Expression, definition.strip()))
                elif type(definition) is dict:
                    if "repeat" in definition:
                        from swayam import Generator
                        gdict = {"generator":None, "args":{}}
                        gdict.update(definition["repeat"])
                        generator_name = definition["repeat"].get("generator", None)
                        generator = getattr(Generator, generator_name)(**gdict["args"])
                        dynamic_file = (getattr(Expression.repeater(generator=generator), definition["name"].strip()))
                        expression_files_or_objects.append(dynamic_file)

            if fmt_kwargs:
                return Thought.formatter(**fmt_kwargs).expression_files(*expression_files_or_objects, **thought_kwargs)
            else:
                return Thought.expressions(*expression_files_or_objects, **thought_kwargs) 
            
        thought_kwargs ={
            "purpose": content.get("purpose", cls._create_purpose_from_file_name(name)),
            "system_prompt": content.get("system_prompt", None),
            "image": content.get("image", None),
            "output_structure": content.get("output_structure", None),
            "tools": content.get("tools", None)
        }
        
        if type(content) is not dict:
            raise TypeError(f"Invalid format of thought file: {name}. Expected a YAML dictionary with the allowed keys: [system_prompt, system_prompt_def, expressions, expression_defs, purpose, image, output_structure, tools]")  
        
        if "expressions" in content and "expression_defs" in content:
            raise ValueError(f"A thought file cannot contain both 'expressions' and 'expression_defs' keys. Choose one.")
        
        if "system_prompt" in content and "system_prompt_def" in content:
            raise ValueError(f"A thought file cannot contain both 'system_prompt' and 'system_prompt_def' keys. Choose one.")
        
        if "system_prompt" in content:
            if type(content["system_prompt"]) is not str:
                raise ValueError(f"The system_prompt key in a expression file must be a string. Found: {type(content['system_prompt'])}") 
            thought_kwargs["system_prompt"] = load_system_prompt_from_direct_content(content["system_prompt"])
        elif "system_prompt_def" in content:
            if type(content["system_prompt_def"]) is not str:
                raise ValueError(f"The system_prompt_def key in a expression file must be a string. Found: {type(content['system_prompt_def'])}") 
            thought_kwargs["system_prompt"]  = load_system_prompt_from_definition(content["system_prompt_def"])

        for key, allowed_type in [("purpose", str), ("image", str), ("output_structure",str), ("tools", list)]:
            if key in content:
                if type(content[key]) is not allowed_type:
                    raise ValueError(f"Invalid format of '{key}' key in expression file: {name}. Expected a {allowed_type}. Found: {type(content[key])}")
        
        if "expressions" in content:
            if type(content["expressions"]) is not list:
                raise ValueError(f"The expressions key in a thought file must contain a list. Found: {type(content['expressions'])}") 
            return load_expressions_from_direct_content(content["expressions"])
        elif "expression_defs" in content:
            if type(content["expression_defs"]) is not list:
                raise ValueError(f"The expression_defs key in a thought file must contain a list. Found: {type(content['expression_defs'])}") 
            return load_expressions_from_definitions(content["expression_defs"])
        else:
            raise ValueError(f"A thought file must contain either a 'expressions' or 'expression_defs' key.") 

    @classmethod    
    def load_thought_from_file(cls, name):
        from tarkash import YamlFile        
        file = YamlFile(cls.get_path_for_thought(name=name))
        return cls.create_thought_from_content(name, file.content)