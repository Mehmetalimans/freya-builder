> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Start Initiating Outbound Calls

> Learn how to start making outbound calls and running campaigns in Freya

## Overview

Freya allows you to initiate outbound calls using your configured phone numbers and agents/workflows. This guide covers setting up outbound calling, creating campaigns, and managing outbound call operations.

## Prerequisites

Before initiating outbound calls, ensure:

1. ✅ **Phone number configured** - Phone number is imported and has outbound routing set
2. ✅ **Outbound agent/workflow** - An agent or workflow is configured for outbound calls
3. ✅ **Outbound enabled** - Outbound calling is enabled in workspace settings
4. ✅ **Sufficient credits** - Your workspace has enough credits for outbound calls
5. ✅ **Twilio integration** - Twilio is connected and properly configured

## Enabling Outbound Calls

### Step 1: Check Workspace Settings

1. Navigate to **Workspace > Settings**
2. Find the **Workspace Settings** section
3. Ensure **"Outbound Enabled"** is checked
4. Save if you made changes

### Step 2: Configure Phone Number

1. Navigate to **Phone Numbers**
2. Edit your phone number
3. Set **"Outbound Agent"** or **"Outbound Workflow"**
4. Save the configuration

## Making Outbound Calls

### Method 1: One-Click Call

Freya provides a one-click call feature for quick outbound calls:

1. Navigate to **One-Click Call** in the sidebar
2. Enter the phone number you want to call
3. Click **"Call"**
4. The call will be initiated using your configured outbound agent/workflow

### Method 2: Campaigns

For larger-scale outbound calling, use campaigns:

1. Navigate to **Campaign** in the sidebar
2. Click **"Create Campaign"**
3. Configure campaign settings:
   * **Name** - Campaign name
   * **Phone Numbers** - List of numbers to call
   * **Agent/Workflow** - Which agent/workflow to use
   * **Schedule** - When to start calling
4. Launch the campaign

### Method 3: API

You can also initiate calls programmatically using Freya's API:

```bash theme={null}
POST /api/v2/call
{
  "phoneNumber": "+1234567890",
  "customerPhoneNumber": "+0987654321",
  "agentId": "agent_123",
  "workspaceId": "workspace_456"
}
```

## Campaign Management

### Creating a Campaign

1. **Navigate to Campaigns**
   * Click **"Campaign"** in the sidebar
   * Click **"Create Campaign"**

2. **Configure Campaign**
   * **Name** - Descriptive campaign name
   * **Description** - Optional campaign description
   * **Phone Number** - Your outbound phone number
   * **Agent/Workflow** - Select the outbound agent or workflow
   * **Contact List** - Upload or enter phone numbers to call

3. **Set Campaign Parameters**
   * **Start Time** - When to begin calling
   * **Call Rate** - How many calls per hour
   * **Retry Logic** - How to handle failed calls
   * **Call Timeout** - Maximum call duration

4. **Launch Campaign**
   * Review configuration
   * Click **"Launch Campaign"**
   * Monitor progress in real-time

### Monitoring Campaigns

Track campaign performance:

1. **Campaign Dashboard**
   * View active campaigns
   * See call statistics
   * Monitor success rates

2. **Call Logs**
   * View individual calls
   * Review call recordings
   * Analyze transcripts

3. **Analytics**
   * Campaign performance metrics
   * Success rates
   * Cost analysis

## Outbound Call Configuration

### Phone Number Settings

When configuring outbound routing:

<ParamField body="outboundAgentId" type="string">
  The agent ID to use for outbound calls (if using Agents configuration)
</ParamField>

<ParamField body="outboundWorkflowId" type="string">
  The workflow ID to use for outbound calls (if using Workflows configuration)
</ParamField>

### Agent/Workflow Considerations

For outbound calls, consider:

* **Opening Message** - How the agent introduces itself
* **Call Purpose** - Why you're calling (sales, support, etc.)
* **Compliance** - Ensure compliance with calling regulations
* **Opt-out Handling** - How to handle opt-out requests

## Best Practices

<Tip>
  Always test outbound calls with a small batch before launching large campaigns.
</Tip>

<Tip>
  Ensure your agent's opening message clearly identifies who is calling and why.
</Tip>

<Tip>
  Monitor call success rates and adjust your approach based on real data.
</Tip>

<Warning>
  Ensure compliance with local calling regulations (TCPA, GDPR, etc.) before making outbound calls.
</Warning>

<Warning>
  Respect opt-out requests immediately and maintain a do-not-call list.
</Warning>

## Troubleshooting

### Calls Not Initiating

If outbound calls aren't starting:

1. **Check Workspace Settings**
   * Verify outbound is enabled
   * Check credit balance
   * Ensure workspace is active

2. **Verify Phone Number**
   * Confirm outbound routing is configured
   * Check phone number status
   * Verify Twilio integration

3. **Check Agent/Workflow**
   * Ensure outbound agent/workflow exists
   * Verify it's properly configured
   * Test it separately

### Low Success Rates

If calls aren't connecting:

1. **Phone Number Validation**
   * Verify numbers are in correct format
   * Check for invalid numbers
   * Remove duplicates

2. **Call Timing**
   * Avoid calling outside business hours
   * Consider time zones
   * Respect calling restrictions

3. **Agent Performance**
   * Review call recordings
   * Analyze conversation quality
   * Improve agent prompts

## Compliance and Regulations

When making outbound calls:

* **TCPA Compliance** (US) - Obtain consent before calling
* **GDPR Compliance** (EU) - Respect privacy regulations
* **Do Not Call Lists** - Maintain and respect DNC lists
* **Caller ID** - Use proper caller identification
* **Opt-out** - Provide clear opt-out mechanisms

## Next Steps

<Card title="View Analytics" icon="chart-bar" href="/analytics">
  Monitor your outbound call performance and campaign analytics.
</Card>

<Card title="Review Call Logs" icon="list" href="/calls">
  Review individual calls and analyze performance.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.