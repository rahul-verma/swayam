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

from enum import Enum, auto

class SwayamOption(Enum):
    '''
        Represents all built-in configuration options for Swayam.
    '''

    EPIC_DIR = auto()
    '''Root directory of the Epic.'''
        
    SNIPPET_DIR = auto()
    '''Root Directory for Snippet Files'''
        
    PROMPT_DIR = auto()
    '''Root Directory for Prompt Files'''
    
    EXPRESSION_DIR = auto()
    '''Root Directory for Expression Files'''
    
    THOUGHT_DIR = auto()
    '''Root Directory for Thought Files'''
    
    STORY_DIR = auto()
    '''Root Directory for Plan Files'''
    
    FOLIO_DIR = auto()
    '''Root Directory for Folio Files'''
    
    NARRATION_DIR = auto()
    '''Root Directory for Narration Files'''
    
    LLM_PROVIDER = auto()
    '''Default LLM Provider name.'''
    
    LLM_MODEL = auto()
    '''Default LLM Model name.'''