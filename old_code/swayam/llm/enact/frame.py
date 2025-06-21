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

import importlib
import swayam

from swayam.core.caller import get_caller_module_file_location

from swayam.inject.error import *
    
class Frame:
    def __init__(self, *, phase, prologue, epilogue):
        self.__phase = phase
        self.__prologue = prologue
        self.__epilogue = epilogue
        self.__props_in_place = []
        
    def __execute(self, injectables, park_prop):
        for injectable in injectables:
            if isinstance(injectable, str):
                try:
                    injectable_type, injectable_name = injectable.split('.')
                    injectable_args = {}
                except Exception as e:
                    raise ValueError("Invalid injectable type: {}. Expected an Injectable dictionary or a name as Prop.name, Cue.name etc".format(injectable))
            elif isinstance(injectable, dict):
                injectable_type = list(injectable.keys())[0]
                injectable_name = injectable[injectable_type]["name"]
                injectable_args = injectable[injectable_type]["args"]
                from swayam.inject import Injectable
                injectable_object = Injectable.load_from_module(injectable_type, injectable_name, caller_file= get_caller_module_file_location())   
            else:
                raise ValueError("Invalid injectable type: {}. Expected an Injectable dictionary".format(injectable))
            
            from swayam.inject import Injectable
            injectable_object = Injectable.load_from_module(injectable_type, injectable_name, caller_file= get_caller_module_file_location())
            
            # !!! It is critical that the vault is passed only at the calling stage. The vault should not be passed at the time of object creation as the Injectable can be used multiple times and the last value holds in such a case.
            if injectable_type == "Prop":
                iter_injectable_object = injectable_object(phase=self.__phase, **injectable_args)
                if park_prop:
                    self.__props_in_place.append(iter_injectable_object)
                next(iter_injectable_object)
            else:
                injectable_object(phase=self.__phase, **injectable_args)

    def prologue(self):
        self.__execute(self.__prologue, park_prop=True)
        
    def epilogue(self):
        self.__execute(self.__epilogue, park_prop=False)
        for prop in list(reversed(self.__props_in_place)):
            next(prop)
            
        # As the props are fully consumed, empty the list.
        # This is especially important for children level fixtures in a parent.
        self.__props_in_place = []