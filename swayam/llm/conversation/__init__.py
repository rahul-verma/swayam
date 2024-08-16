
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

from typing import Any

from tarkash import log_debug
from swayam.llm.prompt.types import SystemPrompt, UserPrompt
from .conversation import LLMConversation

class Conversation:
    
    @classmethod
    def from_prompts(cls, *prompts:UserPrompt, system_prompt:SystemPrompt=None) -> LLMConversation:
        return LLMConversation(*prompts, system_prompt=system_prompt)