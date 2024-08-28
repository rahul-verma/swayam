

## Prompt

Done
- A prompt can be as simple as string.
- Can be a complex object, with provisions for response format, tool calling, image attachment.
- Should be definable in a YAML format.

To Do

- Reporting for all steps.

## Conversation
Done

To Do
- Conversation as a package
- Prompt Loop with Generator
- Loop with a Condition based Generator
- Conditional Prompt
- Standalone Prompt: Possibly to another instance of same Model or a different one.
- Dynamic Prompts. Prompts added on the fly.

## Task

To Do
- Task as a package


## Directive

To Do

## Plan

To Do


## Injectables


### Structure

Exists

### Tool

Exists

### Generator

Exists

### Parser
- Two types of parsers: Text and Json
- Parser.text: the callable gets text input
- Parser.json: the callable gets loaded Python object from a JSON string.

Note: Pydantic behaves funny with unpacking of keyword args when the values are themselves dictionaries. So, I had to remove the notion of a generic JsonContent Model. in future, might handle this within the Structure hierarchy.

### Condition

- Basic condition
- Condition callable has access to Condition object, for which a Store can be set.

### Snippet

- You can define a snippet as a definition file (text or dict) directly under /snippet or any sub-directory. **Snippet.file[.path.to.snippet].<Name>**.
- You can also define as a Python callable and use **Snippet.build**. Rules for callable:
    - Takes one kwarg: **caller** and no other arg.
    - The return type must be **Structure.Snippet** 

### Setter

To Do

### Cleaner

To Do