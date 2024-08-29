

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


## Injectables and Injection Protocol

Swayam supports the concept of dependency injection using Injectables.

An Injectable is:
- a named object that has a well defined purpose in a sequence of steps.
- dicoverable using <InjectableType>.<InjectableName> syntax. For definition file based injectable it is <InjectableType>.file.<InjectableName>.
- has an input-output structure protocol. A part of the protocol could be pre-defined by Swayam for certain injectables.
- The callables encapsulated with injectables need to take only keyword arguments as determined by the input structure. In addition, they take a "caller" argument. This caller object is passed from Swayam's execution flow. WIP.
- The input to the callable as well as the output from the called is always as simple Python objects rather than the Structure objects themselves. Think of them as Validation pass-throughs.


### Structure

- Used to define the input-output protocol in Injectables.
- Various built-in structures are available.
- Can be defined in a project in /lib/inject/structure.py (or a structure package)

### Tool
- Used to define the Tools to be used as an input to an LLM that supports tool calling.
- always define input/output structure on a tool basis.
- allow_none_output tweaks the default where the encapsulated callable is allowed to return None.

### Generator

Exists

### Condition

- Basic condition
- Condition callable has access to Condition object, for which a Store can be set.

### Snippet

- You can define a snippet as a definition file (text or dict) directly under /snippet or any sub-directory. **Snippet.file[.path.to.snippet].<Name>**.
- You can also define as a Python callable and use **Snippet.build**. Rules for callable:
    - Takes one kwarg: **caller** and no other arg.
    - The return type must be **Structure.Snippet** 

### Parser
- Two types of parsers: Text and Json
- Parser.text: the callable gets text input
- Parser.json: the callable gets loaded Python object from a JSON string.

Note: Pydantic behaves funny with unpacking of keyword args when the values are themselves dictionaries. So, I had to remove the notion of a generic JsonContent Model. in future, might handle this within the Structure hierarchy.

### Setter

To Do

### Cleaner

To Do