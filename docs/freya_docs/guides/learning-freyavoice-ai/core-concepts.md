> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Core Concepts

> Understanding the fundamental building blocks of Freyavoice AI

## Introduction

Freyavoice AI is built on several core concepts that work together to create powerful voice AI applications. Understanding these concepts is essential for building effective solutions.

## Agents

**Agents** are the heart of Freyavoice AI. They are intelligent voice assistants powered by advanced AI models that can understand natural language, maintain context, and execute actions.

### What Makes an Agent

An agent consists of several key components:

**System Prompt**: The agent's instructions and personality. This defines how the agent behaves, what it can do, and how it should respond to different situations. A well-crafted system prompt is crucial for agent performance.

**Model Configuration**: The AI model that powers the agent (GPT-4, Claude, etc.). Different models have different strengths - some are better at reasoning, others at speed or cost efficiency.

**Voice Settings**: How the agent sounds. This includes the voice provider, specific voice selection, speaking speed, and voice stability. The right voice can significantly impact user experience.

**Functions**: Actions the agent can take. Functions allow agents to interact with external systems, query databases, make API calls, and perform other operations beyond just conversation.

**Context Management**: How the agent maintains conversation history and context. This includes conversation length limits, context window management, and memory strategies.

### Agent Lifecycle

When a call comes in, the agent goes through several stages:

1. **Initialization**: The agent loads its configuration, system prompt, and any required functions
2. **Context Loading**: Previous conversation history is loaded if available
3. **Listening**: The agent receives and processes audio input
4. **Understanding**: Speech is converted to text and analyzed
5. **Reasoning**: The AI model processes the input and generates a response
6. **Action Execution**: Any required functions are called
7. **Response Generation**: The response is converted to speech and delivered
8. **Context Update**: The conversation is saved for future reference

## Workflows

**Workflows** are visual, node-based systems that allow you to create complex call routing and processing logic. They enable you to build sophisticated applications that go beyond what a single agent can do.

### Workflow Components

**Nodes**: The building blocks of workflows. Each node represents a specific action or decision point:

* **Agent Nodes**: Connect to AI agents to handle conversations
* **Function Nodes**: Execute custom functions or API calls
* **Condition Nodes**: Route calls based on conditions (time of day, caller ID, etc.)
* **Transfer Nodes**: Transfer to human agents or other systems
* **Wait Nodes**: Pause execution for a specified duration
* **Loop Nodes**: Repeat actions based on conditions

**Connections**: The lines between nodes that define the flow of execution. Connections can be conditional, allowing different paths based on node outputs.

**Variables**: Data that flows between nodes. Variables can store user input, function results, or any other data needed during call processing.

### Workflow Execution

When a workflow is triggered:

1. **Entry Point**: Execution starts at the initial node
2. **Node Processing**: Each node executes its logic
3. **Data Flow**: Variables are passed between nodes
4. **Conditional Routing**: Conditions determine which path to take
5. **Parallel Execution**: Some nodes can execute simultaneously
6. **Completion**: The workflow completes when reaching an end node or transfer

### When to Use Workflows vs Agents

Use a **single agent** when:

* Your use case is straightforward
* You need a simple conversation flow
* You want to get started quickly
* The agent can handle everything independently

Use **workflows** when:

* You need complex routing logic
* Multiple agents need to work together
* You require conditional branching
* You need to integrate with multiple systems
* You want to add human-in-the-loop capabilities

## Telephony Layer

The **telephony layer** connects your agents and workflows to the real world through phone numbers and call handling infrastructure.

### Phone Numbers

Phone numbers are your connection point to the telephony network. They can be:

* **Imported**: Brought in from providers like Twilio
* **Purchased**: Acquired through Freya's marketplace (if available)
* **Configured**: Set up with specific capabilities (voice, SMS, etc.)

### Call Routing

When a call comes in, Freya routes it through several stages:

1. **Inbound Reception**: The call is received at the phone number
2. **Number Resolution**: Freya identifies which agent or workflow to use
3. **Session Creation**: A call session is created with unique identifiers
4. **Agent/Workflow Invocation**: The configured agent or workflow is activated
5. **Call Processing**: The agent/workflow handles the conversation
6. **Call Completion**: The call ends and data is saved

### Outbound Calling

For outbound calls, the process is similar but initiated by your application:

1. **Call Request**: Your application requests an outbound call
2. **Number Selection**: Freya selects the appropriate phone number
3. **Call Initiation**: The call is placed to the destination
4. **Connection**: Once connected, the agent/workflow takes over
5. **Processing**: Same as inbound calls from this point

## Integration Points

Freyavoice AI integrates with various external systems:

**Telephony Providers**: Twilio, and other SIP providers for call handling
**AI Models**: OpenAI, Anthropic, and other LLM providers for agent intelligence
**External APIs**: Webhooks and function calls to integrate with your systems
**Storage**: Conversation history, call recordings, and analytics data

## Data Flow

Understanding how data flows through Freyavoice AI helps you build better applications:

1. **Audio Input**: Phone call audio is received
2. **Speech-to-Text**: Audio is converted to text
3. **Agent Processing**: The agent analyzes the text and generates a response
4. **Function Execution**: Any required functions are called
5. **Text-to-Speech**: The response is converted back to audio
6. **Audio Output**: The audio is sent back to the caller
7. **Data Storage**: All interactions are logged for analytics and improvement

## Next Steps

<Card title="Architecture Deep Dive" icon="sitemap" href="/guides/learning-freyavoice-ai/architecture">
  Learn how these core concepts come together in Freyavoice AI's architecture.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.