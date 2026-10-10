> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Connect a Phone Number

> Learn how to connect phone numbers to agents or workflows in Freya

## Overview

After importing a phone number, you need to connect it to agents or workflows to start handling calls. This guide shows you how to configure phone number routing for both inbound and outbound calls.

## Accessing Phone Number Configuration

### Step 1: Navigate to Phone Numbers

1. Click on **"Phone Numbers"** in the sidebar navigation
2. Find the phone number you want to configure
3. Click the **"Edit"** button (three dots menu) on the phone number row

### Step 2: Open Configuration Dialog

Clicking **"Edit"** opens the phone number configuration dialog where you can:

* Set basic information (number, friendly name)
* Choose configuration type (Agents or Workflows)
* Configure inbound routing
* Configure outbound routing

## Configuration Types

Freya supports two configuration types for phone numbers:

### Agents Configuration

Connect your phone number directly to AI agents:

* **Inbound Agent** - Agent that handles incoming calls
* **Outbound Agent** - Agent used for outbound calls

### Workflows Configuration

Connect your phone number to workflows:

* **Inbound Workflow** - Workflow that processes incoming calls
* **Outbound Workflow** - Workflow used for outbound calls

## Configuring a Phone Number

### Step 1: Basic Information

Fill in the basic details:

<ParamField body="phoneNumber" type="string" required>
  The phone number (usually pre-filled from import)
</ParamField>

<ParamField body="friendlyName" type="string" required>
  A descriptive name for this phone number (e.g., "Main Business Line", "Support Line")
</ParamField>

### Step 2: Choose Configuration Type

Select how you want to configure this number:

**Agents:**

* Best for simple setups
* Direct connection to a single agent
* Easier to manage

**Workflows:**

* Best for complex routing
* Multiple agents and logic
* More flexible

### Step 3: Configure Inbound Routing

Set up how incoming calls are handled:

#### For Agents Configuration:

1. Select **"Inbound Agent"** dropdown
2. Choose an agent from the list
3. Or select "No agent selected" to disable inbound calls

#### For Workflows Configuration:

1. Select **"Inbound Workflow"** dropdown
2. Choose a workflow from the list
3. Or select "No workflow selected" to disable inbound calls

### Step 4: Configure Outbound Routing

Set up how outbound calls are handled:

#### For Agents Configuration:

1. Select **"Outbound Agent"** dropdown
2. Choose an agent from the list
3. Or select "No agent selected" to disable outbound calls

#### For Workflows Configuration:

1. Select **"Outbound Workflow"** dropdown
2. Choose a workflow from the list
3. Or select "No workflow selected" to disable outbound calls

### Step 5: Save Configuration

1. Review your configuration
2. Click **"Create Phone Number"** or **"Update Phone Number"**
3. Your phone number is now configured and ready to use

## Phone Number Display

After configuration, your phone number will show:

* **Type** - Whether it's configured with Agents or Workflows
* **Inbound Configuration** - Which agent/workflow handles inbound calls
* **Outbound Configuration** - Which agent/workflow handles outbound calls
* **Capabilities** - Voice, SMS icons indicating enabled features

## Configuration Examples

### Example 1: Simple Agent Setup

```
Phone Number: +1234567890
Friendly Name: Customer Support Line
Configuration Type: Agents
Inbound Agent: Customer Support Agent
Outbound Agent: (None)
```

This setup handles all inbound calls with a single agent and doesn't allow outbound calls.

### Example 2: Workflow with Transfer

```
Phone Number: +1234567890
Friendly Name: Sales Line
Configuration Type: Workflows
Inbound Workflow: Sales Workflow (with agent and transfer logic)
Outbound Workflow: Sales Outbound Campaign
```

This setup uses a workflow for both inbound and outbound calls, allowing for complex routing.

## Switching Configuration Types

You can switch between Agents and Workflows:

1. Open the phone number configuration
2. Change the **"Configuration Type"** dropdown
3. Select new agents/workflows for inbound and outbound
4. Save the changes

<Warning>
  Switching configuration types will clear your previous agent/workflow selections. Make sure to select new ones before saving.
</Warning>

## Best Practices

<Tip>
  Use descriptive friendly names that indicate the phone number's purpose (e.g., "Support Line", "Sales Hotline").
</Tip>

<Tip>
  Start with Agents configuration for simplicity, then upgrade to Workflows when you need more complex routing.
</Tip>

<Tip>
  You can use different agents/workflows for inbound and outbound calls to optimize for each use case.
</Tip>

<Warning>
  Make sure your selected agents or workflows exist and are properly configured before connecting them to phone numbers.
</Warning>

## Troubleshooting

### Agent/Workflow Not Available

If an agent or workflow doesn't appear in the dropdown:

1. Verify it exists in your workspace
2. Check that it's not deleted or archived
3. Refresh the page and try again
4. Create the agent/workflow if it doesn't exist

### Configuration Not Saving

If your configuration won't save:

1. Ensure all required fields are filled
2. Verify the phone number format is correct
3. Check that selected agents/workflows are valid
4. Try refreshing and reconfiguring

## Next Steps

<Card title="Start Receiving Inbound Calls" icon="phone-incoming" href="/basic-operations/receiving-inbound-calls">
  Learn how to test and start receiving inbound calls with your configured phone number.
</Card>

<Card title="Start Initiating Outbound Calls" icon="phone-outgoing" href="/basic-operations/initiating-outbound-calls">
  Learn how to start making outbound calls using your configured phone number.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.