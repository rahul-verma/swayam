

Swayam employs the STEPs model of problem solving using LLMs by Rahul Verma. It has the following high level components:

A large problem is called an Epic which can be broken down into STEPs:

Story: Captures the broad, overarching narrative or goal. It gives a sense of direction and purpose. This largely involves human intellect with some usage of tooling.

Thought: Represents the conceptual phase where ideas and themes are developed from the Story. Still a human-focused phase with some assistance from tooling.

Expression: Bridges the abstract with the concrete, focusing on how Thoughts will be articulated or represented. A phase in the achievement of a thought becoming a reality. This is a proxy layer between what the thought is about and who is solving the part of the problem this phase demands.

Prompt: The most actionable part, where the specific thoughts or commands are generated. A granular interaction with an entity who is supposed to solve a specific part of the problem. In the narrative of automation, this represents a problem unit/piece which can be automated with high level of confidence, with no human intervention, once the solution is implemented.

All building blocks of STEP are only expressed as definitions, with the only exception being a Prompt, which for an extremely simple situation does not need to be defined in a file.

## Narrative
Narrative is passed from narrator to the enactor and the primary object remains same throughout the narration. It has three primary provisions:
1. Directives from Story and Thought
2. A multi-layered, cascading look-up Store: A phase can store key-value pairs in its own layer or in its parent layer. When accessing, a cascading lookup takes place.
3. Current Conversation

## Prompt

- Prompt can be a simple text string.
- For more involved prompting, one has to create a Prompt Definition.
- A Prompt is a part of an Expression and continues the current Conversation in the Narrative.
- Currently a Prompt Def supports defining image, purpose, output structure and tools. In addition, it supports resources, before and after constructs.

### Expression

An Expression can contain multiple prompts.

Each expression starts a new Conversation within the Narrative.

Expression definitions are packages defined as directories.

The directive in an expression is clubbed with directives from Story and Thought.

### Thought

A Thought can contain multiple Expressions. 

Thought definitions are packages defined as directories.

### Story

A Story can contain multiple Thoughts.

Thought definitions are packages defined as directories.

## Fixtures

There are three types of fixtures that can be included in Phase definitions:
1. Resources: (Resource injectable)
    - These are injectables that are automatically called twice in the flow at appropriate point in time.
2. Before: (Parser, Condition, Tool injectables)
    - Once: These are injectables that are called for the current phase, before the phase starts.
    - Every: These are injectables that are called before every child phase.
2. Before: (Parser, Condition, Tool injectables)
    - Once: These are injectables that are called after the current phase, after the phase ends.
    - Every: These are injectables that are called after every child phase completes.

## Repeater
Expression and Thought Definitions have the provision to use a repeater.

In Expression a repeater can be associated with one or more prompts.

In Thought, a repeater can be associated with one or more expressions.

## Injectables and Injection Protocol

Swayam supports the concept of dependency injection using Injectables.

An Injectable is:
- a named object that has a well defined purpose in a sequence of steps.
- dicoverable using <InjectableType>.<InjectableName> syntax. For definition file based injectable it is <InjectableType>.file.<InjectableName>.
- has an input-output structure protocol. A part of the protocol could be pre-defined by Swayam for certain injectables.
- The callables encapsulated with injectables need to take only keyword arguments as determined by the input structure. In addition, they take a "invoker" argument. This caller object is passed from Swayam's execution flow. WIP.
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
- JsonParser created using Parser.json: the callable gets loaded Python object from a JSON string. Default input_structure is Structure.JsonContent. Allowed structures should inherit from its data model. Allow none is false by default. Has an additional provision for validating the input content using content_structure attribute.

Note that JPathExtractor uses the approach of partial functions, because at the time of creating an object of this, content_structure or output_structure is an unknown. 

### Resource

Resource is based on 2-yield statement based callable (or a custom callable which will be called twice) - once for setup and once for teardown. 

Takes the input structure as an argument based on a resource basis. 

Output structure for both the calls needs to be a Structure.Result object.


### Model /llm

TO Do

Here are the ideas:
- model/< type > folders will contain model configs. E.g. model/llm for LLM Model configs. The options will be as provided by corresponding models apart from generic options like temperature. Needs to be investigated.
- for the time being, till the provision for 2 models in single story is implemented, this feature is parked. Once in, this will allow to choose a different model even for prompts within a single model. The narrative management part has to be thought about.


### Model /embed
- other models: model/embed for dealing with embeddings.
- The compatibility of embedding models with llm models needs to be properly understood before architecting this in Swayam.


### VectorDB

To Do

This should follow the implementation of Model / embed injectable.

Most likely this would also mean that a concept fo Dynamic snippets would need to be developed to enable search results being made part of a prompt. 

The role of Tool or a specific injectable for the purpose needs to be explored as well.
All of this will be explored when RAG support needs to be integrated into Swayam.