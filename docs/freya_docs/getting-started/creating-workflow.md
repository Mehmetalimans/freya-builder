> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Creating Your First Workflow

> Learn how to create and configure workflows in Freya

## Overview

Workflows allow you to create complex call routing and processing logic by combining multiple agents, conditions, and integrations. Workflows are perfect for handling multi-step processes, conditional routing, and complex business logic.

## Creating a Workflow

### Step 1: Navigate to Workflows

1. Click on **"Workflows"** in the sidebar navigation
2. You'll see a list of all your workflows (or an empty state if you don't have any)

### Step 2: Create a New Workflow

Click the **"Create Workflow"** button. You can also:

* Click **"Create from Template"** to start from a pre-built template
* Click **"Create Blank Workflow"** to start from scratch

### Step 3: Configure Your Workflow

When you create a new workflow, you'll be taken to the workflow editor. Here you can:

#### Basic Information

* **Workflow Name** - A descriptive name for your workflow
* **Description** - Optional description of what the workflow does
* **Tags** - Add tags to organize your workflows

#### Workflow Structure

Workflows are built using nodes:

* **Initial Node** - The starting point of your workflow
* **Agent Nodes** - Connect to AI agents to handle conversations
* **Function Nodes** - Execute custom functions or API calls
* **Condition Nodes** - Route calls based on conditions
* **Transfer Nodes** - Transfer to human agents or other systems

#### Adding Nodes

1. Click **"Add Node"** in the workflow editor
2. Select the type of node you want to add
3. Configure the node's settings
4. Connect nodes by dragging from one node's output to another's input

#### Configuring Nodes

Each node type has different configuration options:

**Agent Node:**

* Select which agent to use
* Configure agent-specific settings
* Set response behavior

**Function Node:**

* Define the function to call
* Set input parameters
* Configure error handling

**Condition Node:**

* Define the condition to check
* Set routing logic for true/false outcomes

### Step 4: Save Your Workflow

1. Click **"Save"** to save your workflow
2. Your workflow is now ready to be connected to phone numbers

## Workflow Templates

Freya provides pre-built workflow templates to help you get started:

* **Simple Agent** - Single agent workflow
* **Agent with Transfer** - Agent that can transfer to humans
* **Multi-Agent Routing** - Route calls to different agents based on conditions
* **Function Integration** - Workflow with custom function calls

## Testing Workflows

Before connecting your workflow to a phone number:

1. Use the workflow simulation feature
2. Test different scenarios and conditions
3. Verify that routing logic works as expected
4. Check that all integrations function properly

## Workflow Best Practices

<Tip>
  Start simple with a single agent node, then gradually add complexity as needed.
</Tip>

<Tip>
  Use descriptive names for nodes to make your workflow easy to understand.
</Tip>

<Tip>
  Test all conditional branches to ensure proper routing.
</Tip>

<Warning>
  Complex workflows can be difficult to debug. Start simple and add complexity incrementally.
</Warning>

## Copying Workflows

You can copy existing workflows to:

* Create variations of successful workflows
* Use as templates for new workflows
* Experiment without modifying the original

1. Click the **"Copy"** icon on any workflow card
2. The workflow will be duplicated with a new name
3. Edit the copy as needed

## Next Steps

<Card title="Import a Phone Number" icon="phone" href="/basic-operations/import-phone-number">
  Learn how to import phone numbers from Twilio and other providers.
</Card>

<Card title="Connect a Phone Number" icon="link" href="/basic-operations/connect-phone-number">
  Learn how to connect your phone numbers to agents or workflows.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.