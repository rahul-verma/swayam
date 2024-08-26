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

from swayam.inject.error import *

_NAME = "Parser"

class ParserCallError(InjectableObjectError): 
    
    def __init__(self, name, error):
        super().__init__(_NAME, name, message=f"An error occurred while calling the parser. Error: {error}")

class ParserNotFoundError(InjectedNameNotFoundError):
    
    def __init__(self, name):
        super().__init__(_NAME, name)
        
class ParserImportError(InjectedNameImportError):
    
    def __init__(self, name, *, import_error_message):
        super().__init__(_NAME, name, import_error_message=import_error_message)
        
class ParserArgIsNotCallableError(InjectedObjectCallableArgError):
    
    def __init__(self, name, kallable):
        super().__init__(_NAME, name, kallable=kallable)
        
class ParserInputStructureInvalidError(InjectableObjectError):
    
    def __init__(self, name, tool):
        super().__init__(_NAME, name, message=f"Input structure is invalid for the tool '{tool.name}' for creating a parser. Found >>{tool.input_structure.__class__.__name__}<<. Expected: TextContent or JsonContent.")