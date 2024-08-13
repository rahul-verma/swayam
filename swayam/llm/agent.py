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

from typing import List

from tarkash import TarkashObject, log_info, log_debug
from .config import *
from tarkash.type.descriptor import DString, DNumber, DBoolean
from pydantic import BaseModel

class Agent(TarkashObject):
    _name = DString()
    _temperature = DNumber()
    _model = DString()
    _content_only = DBoolean()
    _display = DBoolean()
    _report_html = DBoolean()
    _show_in_browser = DBoolean()
    
    """
    Swayam Agent to talk with LLMs.
    """
    def __init__(self, name:str = "Swayam Agent", provider:str = None, model:str = None, temperature=0, display=False, report_html=True, show_in_browser=True, **kwargs):
        self.__model_config = ModelConfig(provider=provider, model=model)
        self.__prompt_config = PromptConfig(temperature=temperature, **kwargs)
        
        tobj_kwargs = dict()
        tobj_kwargs["provider"] = self.__model_config.provider
        tobj_kwargs["model"] = self.__model_config.model
        tobj_kwargs["temperature"] = self.__prompt_config.temperature
        tobj_kwargs["report_html"] = report_html
        tobj_kwargs["show_in_browser"] = show_in_browser
        tobj_kwargs.update(kwargs)
        super().__init__(**kwargs)
        self._temperature = temperature
        self._provider = self.model_config.provider
        self._model = self.model_config.model
        self._display = display
        self._report_html = report_html
        self._show_in_browser = show_in_browser
        self._model_kwargs = kwargs
        
    @property
    def model_config(self):
        return self.__model_config
    
    @property
    def prompt_config(self):
        return self.__prompt_config
    
    @property
    def reporter_config(self):
        return self.__reporter_config
        
        
    def __normalise_nodes(self, *nodes):
        from .node import AgentNode
        node_objects = []
        nodes = list(nodes)
        log_debug(f"Normalising {len(nodes)} nodes", self)
        for i, node in enumerate(nodes):
            log_debug(f"Node:: {i+1}", self)
            AgentNode.append_node(node, node_objects) 
            log_debug(f"Finished:: Current Nodes: {node_objects}", self) 
        log_debug(f"Finished Normalisation:: Nodes: {node_objects}", self) 
        return node_objects

    def execute(self, *nodes:List[object], same_context:bool=True, response_format:BaseModel=None):
        """
        A simple facade to default LLM Model, resulting in one or more prompts being executed.
        
        The goal is to provide an equivalent of a simple web interface like ChatGPT in API-level experience.
        
        The default LLM Model is picked up from configuration.
        
        This method is meant for simple usage where a user wants to execute one or more prompts.
        
        The call supports multiple prompts and other objects to be provided in any sequence. Following are the supported object types:
        1. Prompt as a string.
        2. Prompt as a dictionary with role and content keys.
        3. Prompt as a File. The file names (Text/INI) (or file paths relative to the <ROOT>Prompt directory) can be provided. 
        
        Args:
            *prompts_or_objects (str, List, Dict): The prompts to be executed
            same_context (bool, optional): If True, the same context is used for all prompts. Defaults to True.
            response_format (BaseModel, optional): The Pydantic response format to be used. Defaults to None.

        Returns:
            (str, List): Returns a string or a list of strings as the output of the LLM.
        """
                
        nodes = self.__normalise_nodes(*nodes)
        
        from .prompt.context import PromptContext
        context = PromptContext()
        log_debug("Context Length: ", len(context.messages))
        
        from .listener import AgentListener
        listener = AgentListener(display=self._display, report_html=self._report_html, show_in_browser=self._show_in_browser)

        log_debug(f"Executing {len(nodes)} LLM node(s) (same_context={same_context})")        
        output_list = []
        for node in nodes:
            if not same_context:
                input_messages = []
            from .node import PromptNode
            if isinstance(node, PromptNode):
                prompt_sequence = node.wrapped_object
                log_debug(f"Found PromptSequence Node (children = {len(prompt_sequence)})")
                #print(node.wrapped_object.describe())
                if not same_context:
                    context.reset()
                from .executor import PromptExecutor
                executor = PromptExecutor(model_config=self.__model_config, prompt_config=self.__prompt_config, listener=listener)
                output = executor.execute(prompt_sequence=node.wrapped_object, context=context, response_format=response_format)
                output_list.extend(output)
                log_debug(f"Finished PromptNode")
                
        listener.finish()
        
        content = [m.content for m in output_list]
        if len(content) == 1:
            return content[0]
        else:
            return content
                
        
                