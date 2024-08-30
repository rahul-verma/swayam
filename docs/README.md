

Swayam employs the STAR model of problem solving by Rahul Verma. It has the following high level components:

Strategy: A very high level view of the problem that you want to solve and a break-down into tasks. This largely involves human intellect with some usage of tooling.
Task: Each task has a pertinent expected outcome to implement the strategy. This is where one would want to largely automate. Humans-in-the-loop is still recommended especially in the review of the task outcomes.
Action: A step/stage in the achievement of a task. Also, acts as a proxy layer between what the task demands and who is solving the part of the problem this step/stage demands.
Request: A granular interaction with an entity who is supposed to solve a specific part of the problem. In the context of automation, this represents a problem unit/piece which can be automated with high level of confidence, with no human intervention, once the solution is implemented.

As of now, Swayam focuses on Requests handled by an LLM. Other forms of AI as well as supporting systems will be explored later.

All building blocks of STAR are only expressed as definitions, with the only exception being a Request, which for an extremely simple situation does not need to be defined.

## Request

To Do

## Action

To Do
- Action as a package
- Request Loop with Generator
- Loop with a Condition based Generator
- Conditional Request
- Standalone PRequestrompt: Possibly to another instance of same Model or a different one.
- Dynamic Requests. Requests added on the fly.

## Task

To Do
- Task as a package


## Strategy

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

- Used to define a specific kind of injectable which when iterated over produces structures of the same kind.
- Typical usage: Looping.
- always define input/output structure on a generator basis.
- allow_none_output tweaks the default where the encapsulated callable is allowed to return None.
- Input structure can be empty.

### Condition

- Used to define a specific kind of injectable which always returns a **Structure.BoolValue**.
- Typical usage: Checking a condition for decision making.
- always define input structure on a generator basis.
- Input structure can be empty.

### Snippet

- You can define a snippet as a definition file (text or dict) directly under /snippet or any sub-directory. **Snippet.file[.path.to.snippet].<Name>**.

### Parser
- Two types of parsers: Text and Json
- TextParser created using Parser.text: the callable gets text input. Default input_structure is Structure.TextContent. Allowed structures should inherit from its data model. Default output structure is Structure.StringValues. Allow none is false by default
- JsonParser created using Parser.json: the callable gets loaded Python object from a JSON string. Default input_structure is Structure.JsonContent. Allowed structures should inherit from its data model. Allow none is false by default. Has an additional provision for validating the input content using schema_validator attribute.

### Resource

a single callable with yield (pytest) style. to do.