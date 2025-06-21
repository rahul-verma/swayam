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
        
    DEFINITION_SNIPPET_DIR = auto()
    '''Root Directory for Snippet Files'''
        
    DEFINITION_PROMPT_DIR = auto()
    '''Root Directory for Prompt Files'''
    
    DEFINITION_EXPRESSION_DIR = auto()
    '''Root Directory for Expression Files'''
    
    DEFINITION_THOUGHT_DIR = auto()
    '''Root Directory for Thought Files'''
    
    DEFINITION_STORY_DIR = auto()
    '''Root Directory for Plan Files'''
    
    DEFINITION_ENTITY_DIR = auto()
    '''Root Directory for Entity Definition Files'''
    
    FOLIO_DIR = auto()
    '''Root Directory for Folio Files'''
    
    FOLIO_AGGREGATE_DIR = auto()
    '''Root Directory for Drafts in Folio.'''
    
    FOLIO_BLUEPRINT_DIR = auto()
    '''Root Directory for Blueprint Files in Folio'''
    
    FOLIO_OUTPUT_DIR = auto()
    '''Root Directory for Output in Folio'''
    
    FOLIO_NARRATION_DIR = auto()
    '''Root Directory for Narration Files in Folio'''
    
    LLM_PROVIDER = auto()
    '''Default LLM Provider name.'''
    
    LLM_MODEL = auto()
    '''Default LLM Model name.'''
    
    # Updating the Tarkash option
    LOG_DIR = auto()
    '''Root Directory for Logs'''