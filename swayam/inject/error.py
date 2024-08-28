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

class InjectableObjectError(Exception):
    
    def __init__(self, type, name, message):
        super().__init__(f"{type} >>{name}<<: {message}")

class InjectedNameNotFoundError(InjectableObjectError):
    
    def __init__(self, type, name):
        super().__init__(type, name, "Neither defined in the project, nor defined by Swayam.")
        
class InjectedNameImportError(InjectableObjectError):
    
    def __init__(self, type, name, *, import_error_message):
        super().__init__(type, name, f"Object was found, but could not be imported. Error: {import_error_message}. Check definition for {type} >>{name}<< for spelling/casing errors, else check your project hook lib.")
        
class InjectedObjectCallableArgError(InjectableObjectError):
    
    def __init__(self, type, name, *, kallable):
        super().__init__(type, name, kallable, f"Got object >>{kallable} of type >>{type(kallable)}<<. Expected callable.")
        
class InjectableObjectCallableOutputError(InjectableObjectError):
    
    def __init__(self, type, name, *, kallable, expected_type, actual_object):
        super().__init__(_NAME, name, kallable, f"Expected callable >>{kallable}<< to return object of type >>{expected_type}<<. Got >>{actual_object}<< of type >>{type(actual_object)} instead.")