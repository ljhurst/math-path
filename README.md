# math-path

This is a demo repo showcasing an autonomous agent.
The agent takes a start number and an end number and then works to make the start number equal the end number by:

- Adding one
- Subtracting one
- Doubling
- Halving

This simple example shows how the agent can plan out its own route from start to finish, keep track of progress, and know when to stop.

## Set Up

We use `uv`. Install via instructions [here](https://docs.astral.sh/uv/getting-started/installation/)

Then install dependencies

```bash
uv sync
```

## Run

### Prerequisites

We expect the LLM powering the agent to be hosted on Databricks. Set the auth token

```bash
export DATABRICKS_TOKEN=<databricks-personal-access-token>
```

### Command

```bash
uv run python src/math_path/cli.py --start-number 1 --end-number 2
```

## Concepts

This is a [12 Factor Agents](https://github.com/humanlayer/12-factor-agents/) style agent.
It demonstrates a few of the factors:

- 01 - Natural Language to Tool Calls
  - The agent is able to turn a user request into tool calls
- 02 - Own Your Prompts
  - The only prompts sent to the LLM are from this repo
  - See all the prompts [here](./src/math_path/prompts/)
- 03 - Own Your Context Window
  - A single user message is sent each turn with a custom thread to prompt serialization
  - See the serialization [here](./src/math_path/prompts/from_thread.py)
- 04 - Tools are Structured Outputs
  - Tools are use to signify execution and also as a way for the LLM to communicate the next step in a structured way
  - See a tool that is only used for structured output [here](./src/math_path/tools/next_step.py)
- 05 - Unify Execution State
  - The only state is the `Thread`. All `Event`s are added to the `Thread` as they happen
- 08 - Own Your Control Flow
  - The agent makes decisions and are executed [here](./src/math_path/agent.py#L63)

One goal of this demo was to build an agent without frameworks to be able to demonstrate the steps under the hood. The agent works like this

1. Get a user request (start 1, end 2)
2. Start a `Thread` with the user request as the first `Event`
3. Loop until the task is finished or we run out of turns

    1. Serialize the entire `Thead` into a prompt
    2. Have the agent decide the next step
    3. Add the agent decision to the `Thread`

        1. Either we're done, signaled by calling the done tool (not executed, just used for structured output)
        2. Or we need to call another tool

            1. Add tool call to `Thread`
            2. Add tool result to `Thread`
