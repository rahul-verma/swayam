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
    
class Fixture:
    def __init__(self, *, phase, before, after):
        print(before, after)
        self.__phase = phase
        self.__before = before
        self.__after = after
        self.__setup_resource_objects = []
        
    def __execute(self, injectables, store_resources):
        for injectable in injectables:
            if isinstance(injectable, str):
                try:
                    injectable_type, injectable_name = injectable.split('.')
                except Exception as e:
                    raise ValueError("Invalid injectable type: {}. Expected an Injectable dictionary or a name as Resource.name, Condition.name etc".format(injectable))
                from swayam.inject import Injectable
                injectable_object = Injectable.load_from_module(injectable_type, injectable_name, caller_file= get_caller_module_file_location())
                injectable_object.store = self.__phase.store
                if injectable_type == "Resource":
                    injectable_object = iter(injectable_object())
                    if store_resources:
                        self.__setup_resource_objects.append(injectable_object)
                    next(injectable_object)
                else:
                    injectable_object()
            elif isinstance(injectable, dict):
                injectable_type = list(injectable.keys())[0]
                injectable_name = injectable[injectable_type]["name"]
                injectable_args = injectable[injectable_type]["args"]
                from swayam.inject import Injectable
                injectable_object = Injectable.load_from_module(injectable_type, injectable_name, caller_file= get_caller_module_file_location())
                injectable_object.store = self.__phase.store
                if injectable_type == "Resource":
                    injectable_object = iter(injectable_object(**injectable_args))
                    if store_resources:
                        self.__setup_resource_objects.append(injectable_object)
                    next(injectable_object)
                else:
                    injectable_object(**injectable_args)
            else:
                raise ValueError("Invalid injectable type: {}. Expected an Injectable dictionary".format(injectable))

    def before(self):
        print("BEFORE")
        self.__execute(self.__before, store_resources=True)
        
    def after(self):
        print("AFTER")
        self.__execute(self.__after, store_resources=False)
        for resource in self.__setup_resource_objects[-1:]:
            next(resource)