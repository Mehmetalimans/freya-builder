> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Creating Your First Agent

> Learn how to create and configure an AI voice agent in Freya

## Overview

AI agents are the core of Freya. They are intelligent voice assistants that can handle phone conversations, understand natural language, and execute functions. This guide will walk you through creating your first agent.

## Creating an Agent

### Step 1: Navigate to Agents

1. Click on **"Agents"** in the sidebar navigation
2. If you don't have any agents yet, you'll see an empty state with a **"Create Agent"** button

### Step 2: Create a New Agent

Click the **"Create Agent"** button. This will:

1. Create a new agent with default settings
2. Automatically redirect you to the agent configuration page
3. Open the agent editor where you can customize your agent

### Step 3: Configure Your Agent

The agent configuration page allows you to customize:

#### Basic Information

* **Agent Name** - A descriptive name for your agent
* **Description** - Optional description of what the agent does

#### System Prompt

The system prompt is the most important part of your agent. It defines:

* The agent's personality and tone
* What the agent can and cannot do
* How the agent should respond to different situations
* Instructions for handling edge cases

<Warning>
  The system prompt directly affects your agent's behavior. Take time to craft a clear, detailed prompt.
</Warning>

#### Model Configuration

Choose the AI model your agent will use:

* **Model Provider** - Select from available providers (OpenAI, Anthropic, etc.)
* **Model** - Choose the specific model (GPT-4, Claude, etc.)
* **Temperature** - Control the randomness of responses (0-1)
* **Max Tokens** - Maximum response length

#### Voice Settings

Configure how your agent sounds:

* **Voice Provider** - Select a voice provider
* **Voice** - Choose a specific voice
* **Voice Speed** - Adjust speaking speed
* **Voice Stability** - Control voice consistency

#### Functions

Add functions that your agent can call:

* **Function Name** - Unique identifier for the function
* **Description** - What the function does
* **Parameters** - Input parameters the function accepts
* **Endpoint** - API endpoint to call

#### Advanced Settings

* **First Message** - Optional greeting message
* **Response Delay** - Delay before responding
* **Max Duration** - Maximum call duration
* **Language** - Agent's primary language

### Step 4: Save Your Agent

1. Click **"Save"** to save your agent configuration
2. Your agent is now ready to use
3. You can test it using the simulation feature

## Testing Your Agent

Before connecting your agent to a phone number:

1. Navigate to the **Simulations** page
2. Create a test simulation
3. Make a test call to see how your agent performs
4. Iterate on the prompt and settings based on the results

## Agent Best Practices

<Tip>
  Start with a clear, specific system prompt. Be explicit about what the agent should and shouldn't do.
</Tip>

<Tip>
  Test your agent thoroughly before deploying it to production phone numbers.
</Tip>

<Tip>
  Use the AI Studio to iteratively improve your agent's prompt based on real conversations.
</Tip>

## Next Steps

<Card title="Iterate Your Agents" icon="wand-magic-sparkles" href="/basic-operations/iterating-agents">
  Learn how to use AI Studio to improve your agent's prompts and performance.
</Card>

<Card title="Create Your First Workflow" icon="diagram-project" href="/basic-operations/creating-workflow">
  Learn how to create workflows that combine multiple agents and logic.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.