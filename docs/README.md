

Swayam employs [The STEPs model of prompting by Rahul Verma](https://www.linkedin.com/pulse/swayam-steps-model-prompting-i-rahul-verma-iqjne). It has the following high level components:

Your Project is the Epic, which can be broken down into STEPs:

Story: Captures the broad, overarching narrative or goal. It gives a sense of direction and purpose. This largely involves human intellect with some usage of tooling.

Thought: Represents the conceptual phase where ideas and themes are developed from the Story. Still a human-focused phase with some assistance from tooling.

Expression: Bridges the abstract with the concrete, focusing on how Thoughts will be articulated or represented. A phase in the achievement of a thought becoming a reality. This is a proxy layer between what the thought is about and who is solving the part of the problem this phase demands.

Prompt: The most actionable part, where the specific thoughts or commands are generated. A granular interaction with an entity who is supposed to solve a specific part of the problem. In the narrative of automation, this represents a problem unit/piece which can be automated with high level of confidence, with no human intervention, once the solution is implemented.

All building blocks of STEPs are only expressed as definitions, with the only exception being a Prompt, which for an extremely simple situation does not need to be defined in a file.

## Narrative
Narrative is passed from narrator to the enactor and the primary vault remains same throughout the narration. What changes along the way is the current conversation that it holds at an expression level. It has three primary provisions:
1. Directives from Story and Thought. These get combined with the directive in an Expression and transformed as context by Swayam for the conversation in the Expression.
2. A multi-layered, cascading look-up Store: A phase can vault key-value pairs in its own layer or in its parent layer. When accessing, a cascading lookup takes place.
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

## Frames

There are 4 types of frames that can be included in Phase outlines (except Prompt in which only the first two are applicable). 
1. **prologue**: Before start of the phase whose outline contains it.
2. **epilogue**: After end of the phase whose outline contains it.
3. **prologue_node**: Before start of the every child node of current phase.
4. **epilogue_node**: After end of the every child node of current phase.

Prologue frames can include:
    - Prop
    - Cue - if evaluates to False, this phase is skipped.
    - Action

Epilogue frames can include:
    - Cue - if evaluates to False, a critical level exception is raised.
    - Action

Note: Props are tore down in the exact opposite order of their creation order.

## Repeater
Expression and Thought Outlines have the provision to use a repeater.

In Expression a repeater can be associated with one or more prompts.

In Thought, a repeater can be associated with one or more expressions.

## Injectables and Injection Protocol

Swayam supports the concept of dependency injection using Injectables.

An Injectable is:
- a named object that has a well defined purpose in a sequence of steps.
- discoverable using <InjectableType>.<InjectableName> syntax.
- has an input-output protocol based on templates. A part of the protocol could be pre-defined by Swayam for certain injectables.
- The callables encapsulated with injectables need to take only keyword arguments as determined by the input structure. In addition, they take a "invoker" argument. This caller object is passed from Swayam's execution flow. WIP.
- The input to the callable as well as the output from the called is always as simple Python objects rather than the Template objects themselves. Think of them as Validation pass-throughs.


### Template

- Used to define the input-output protocol in Injectables.
- Various built-in structures are available.
- Can be defined in a project in /lib/inject/template.py (or a template package)

### Action
- Used to define the Actions to be used as an input to an LLM that supports tool calling.
- always define input/output template on an action basis.
- allow_none_output tweaks the default where the encapsulated callable is allowed to return None.

### Driver

- Used to define a specific kind of injectable which when iterated over produces template objects of the same kind.
- Typical usage: Looping.
- always define input/output template on a driver basis.
- allow_none_output tweaks the default where the encapsulated callable is allowed to return None.
- Input template can be empty.

### Cue

- Used to define a specific kind of injectable which always returns a **Template.BoolValue**.
- Typical usage: Checking a condition for decision making.
- always define input template on a Cue basis.
- Input template can be empty.

### Snippet

- You can define a snippet as a YAML file (text or dict) directly under /snippet or any sub-directory. **Snippet.file[.path.to.snippet].<Name>**.

### Prop

Prop is based on 2-yield statement based callable (or a custom callable which will be called twice) - once for setup and once for teardown. 

Takes the input template as an argument based on a Prop basis. 

Output template for both the calls needs to be a Template.Result object.


### Model /llm

TO Do

Here are the ideas:
- model/< type > folders will contain model configs. E.g. model/llm for LLM Model configs. The options will be as provided by corresponding models apart from generic options like temperature. Needs to be investigated.
- for the time being, till the provision for 2 models in single story is implemented, this feature is parked. Once in, this will allow to choose a different model even for prompts within a single model. The narrative management part has to be thought about.

## Folio
is the vault of scripts and drafts

### Draft
An output from the prompt. Can be translated using a Translator. Can be structured or unstructured.

### Script
A draft or sourced from anywhere else with a translator. Can be structured or unstructured.

### Section
Each unit of information in a Structured Script.


### Model /embed
- other models: model/embed for dealing with embeddings.
- The compatibility of embedding models with llm models needs to be properly understood before architecting this in Swayam.


### VectorDB

To Do

This should follow the implementation of Model / embed injectable.

Most likely this would also mean that a concept fo Dynamic snippets would need to be developed to enable search results being made part of a prompt. 

The role of Tool or a specific injectable for the purpose needs to be explored as well.
All of this will be explored when RAG support needs to be integrated into Swayam.