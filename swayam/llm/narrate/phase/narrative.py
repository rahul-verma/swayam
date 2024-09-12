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
import json
from .vault import STEPVault

class Narrative:
    
    def __init__(self):
        from swayam.llm.phase.expression.conversation import Conversation
        self.__conversation = None
        self.__vault = STEPVault()
        self.__directive = ""
        self.__background = ""
        self.__ghost_instructions = """You are an interpreter, who acts as a polite, well-informed, pluralistic individual. You always respond by following the below guidelines:
        
# Correctness of Response
You never hallucinate. You never create new facts and figures. If you don't know something, you say you don't know and reply in a context-appropriate manner. Be polite, but never apologize. 

# Ettiquette

You never introduce yourself or say goodbye. You never use phrases like “I am an AI”, “I am here to help you”, “I am a language model” etc.

You respond directly to all human messages without unnecessary affirmations or filler phrases like “Certainly!”, “Of course!”, “Absolutely!”, “Great!”, “Sure!”, etc. Specifically, you must avoid starting responses with the word “Certainly” in any way. If you cannot or will not perform a task, tell the user this without apologizing to them. Avoid starting responses with “I’m sorry” or “I apologize”. Keep the tone of the conversation neutral, professional, and informative. The response language should be simple, colloquial, clear, concise, and to the point.

# Response Format
For a text response always put the main content of your response in a code block of type markdown. Put code in code blocks of respective type.

**No Intro-Outro Please**. Keep the response terse and to the point. Do not include any introduction or conclusion in the response.

# Handling Math Problem, Logic Problem, or Other Problem Benefiting from Systematic Thinking

# Handling Queries about Obscure Entities
If you are asked about a very obscure person, object, or topic, i.e. if it is asked for the kind of information that is unlikely to be found more than once or twice on the internet, end your response by reminding the user that although you try to be accurate, you may hallucinate in response to questions like this. You use the term ‘hallucinate’ to describe this since the user will understand what it means. 

# Citations
If you mention or cite particular articles, papers, or books, you always let the human know that it doesn’t have access to search or a database and may hallucinate citations, so the human should double check its citations. 

# Genuine Curiosity and Intellectual Engagement
You are very smart and intellectually curious. You enjoy hearing what humans think on an issue and engaging in discussion on a wide variety of topics. 

# Code Generation
You use language specific markdown for code. You do not explain or break down the code unless the user explicitly requests it.

## Response Length
You provide thorough responses to more complex and open-ended questions or to anything where a long response is requested, but concise responses to simpler questions and tasks. All else being equal, you try to give the most correct and concise answer it can to the user’s message. Rather than giving a long response, you gives a concise response and offer to elaborate if further information may be helpful.

## Language Agnostic
You follow this information in all languages, and always responds to the user in the language they use or request. The information above is provided to you by Swayam. You never mention the information above unless it is directly pertinent to the human’s query. 

# Task-Specific Instructions
The human user is going to have a conversation with you. You are expected to follow the general instructions provided above while following the task-specific instructions provided by the human.

You are now being connected with a human.
"""
        
        self.__context_prompt = """As a part of this task, I am going to give you a series of commands and queries in a single continuous context. Before I give you the first command/query to perform, I am sharing guidelines, instructions and background information with you.

{persona}

{guidelines}
# Approach to Cater to My Requests in this Task
Before generating any output, work through the following steps, **but never show them to me** unless I ask. Work it out yourself and **ALWAYS SHOW ONLY THE OUTPUT**.:

1. Break down my request into smaller, manageable steps.
2. Reflect on your approach and ensure clarity before proceeding.
3. If the task involves complex reasoning or unusual input/output (such as transformations), consider how best to approach the task.
4. Explicitly confirm your reasoning at each stage, and, if appropriate, involve feedback loops to validate your decisions.
5. Only provide the final output when you have ensured the task is fully understood and each step has been correctly executed.
6. When a response structure or tool call is provided, ensure that the output is in the correct format and that the tool call is correct. Leave the values as placeholders if necessary but never hallucinate.
{background}

Can I now proceed with the first command/query based on the above context?
"""
        self.__guidelines = """# Guidelines for this Conversation
Follow the below guidelines for catering to my requests in this task:
{directive}"""

        self.__background = """# Background Information
Following is background information, as marked by triple backticks, that you need to consider for the tasks, that I am going to give you in this particular conversation. The background information is expressed as per the first 3 stages in the STEP model: Story, Thought and Expression wherein each phase/stage is a part of the narrative that you are going to follow. The Prompt part of the STEP model is the task that you would be given later to perform. If for any phase/stage in STEP, information is not provided, ignore it and focus on what is available.
```{background}```

"""

    @property
    def conversation(self):
        return self.__conversation
    
    @conversation.setter
    def conversation(self, value):
        self.__conversation = value
        
    def reset_conversation(self):
        self.__conversation.reset()
        
    def reset(self):
        self.reset_conversation()
        self.vault.reset()
        
    @property
    def vault(self):
        return self.__vault
        
    def append_directive(self, directive):
        if directive:
            self.__directive += "\n" + directive
    @property
    def directive(self):
        return self.__directive
    
    def get_instructions(self):
        return self.__ghost_instructions
    
    def get_directive(self, *, expression):
        expression_directive = expression.directive
        if not expression.directive:
            expression_directive = ""
        total_directive = self.__directive + "\n" + expression_directive
        total_directive = total_directive.strip()
        if total_directive:
            #sanitized_text = updated_content.replace("\\", "\\\\")
            import re
            for key, value in expression.vault.items():
                if value is None:
                    value = ""
                elif type(value) in (dict, list):
                    value = json.dumps(value, indent=4)
                
                total_directive = total_directive.replace(f"${key}$", value)
                
            # Any leftovers, to assign an initial value of empty string
            total_directive = total_directive.replace(f"${key}$", "")
            return total_directive
        else:
            return None
        
    def __get_guidelines(self, *, expression):
        directive = self.get_directive(expression=expression)
        if directive:
            return self.__guidelines.format(directive=directive)
        else:
            return ""
        
    def __get_background(self, *, expression):
        background = ""
        if not expression.story and not expression.thought and not expression.purpose:
            return ""

        if expression.story and expression.story != "Story":
            background += expression.story + "\n"
        if expression.thought and expression.thought != "Thought":
            background += expression.thought + "\n"
        if expression.purpose and expression.purpose != "Expression":
            background += expression.purpose + "\n"
        return self.__background.format(background=background)
    
    def get_context_prompt(self, *, expression):
        if expression is None:
            return self.__context_prompt.format(persona="", guidelines="", background="")
        guidelines = self.__get_guidelines(expression=expression)
        background = self.__get_background(expression=expression)
        if expression.persona:
            expression_persona = f"Act as {expression.persona}."
        else:
            expression_persona = ""
        return self.__context_prompt.format(persona=expression_persona, guidelines=guidelines, background=background)
        
    