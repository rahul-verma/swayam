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
        
class ParserNoMatchError(InjectableObjectError):
    
    def __init__(self, injectable, *, error):
        super().__init__(injectable, error=f"Parser did not find any match. {error}")
        
class ParserIncompatibleInputStructureError(InjectableObjectError):
        
    def __init__(self, injectable, *, in_template):
        super().__init__(injectable, error=f"Parser input structure must be either Template.{in_template} or a structure based on a Pydantic class DataModel that inherits from Template.{in_template}.model.")
            
class TextParserIncompatibleInputStructureError(ParserIncompatibleInputStructureError):
    
    def __init__(self, injectable):
        super().__init__(injectable, in_template="TextContent")
        
class JsonParserIncompatibleInputStructureError(ParserIncompatibleInputStructureError):
    
    def __init__(self, injectable):
        super().__init__(injectable, in_template="JsonContent")