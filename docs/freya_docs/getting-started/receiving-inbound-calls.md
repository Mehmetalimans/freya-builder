> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Start Receiving Inbound Calls

> Learn how to test and start receiving inbound calls with your configured phone number

## Overview

Once you've imported a phone number and connected it to an agent or workflow, you're ready to start receiving inbound calls. This guide covers testing your setup and ensuring everything works correctly.

## Prerequisites

Before receiving inbound calls, make sure you have:

1. ✅ **Imported a phone number** - Phone number is imported from Twilio or another provider
2. ✅ **Connected the phone number** - Phone number is configured with an inbound agent or workflow
3. ✅ **Agent/Workflow is ready** - Your agent or workflow is properly configured and tested
4. ✅ **Twilio integration active** - Twilio webhooks are properly configured (if using Twilio)

## Testing Your Setup

Before going live, test your inbound call setup:

### Step 1: Verify Configuration

Check that your phone number is properly configured:

1. Navigate to **Phone Numbers**
2. Find your phone number
3. Verify it shows:
   * ✅ Type (Agents or Workflows)
   * ✅ Inbound agent/workflow is selected
   * ✅ Status is active

### Step 2: Test with Simulation

Use Freya's simulation feature to test:

1. Navigate to **Simulations**
2. Create a new simulation
3. Select your phone number
4. Make a test call
5. Verify the agent/workflow responds correctly

### Step 3: Make a Test Call

Call your phone number from another phone:

1. Dial the phone number you configured
2. The call should connect to your agent/workflow
3. Test a conversation to ensure everything works
4. Check the call logs to verify the call was recorded

## Monitoring Inbound Calls

### Viewing Call Logs

Track all inbound calls:

1. Navigate to **Calls** in the sidebar
2. View the list of all calls
3. Filter by:
   * Phone number
   * Date range
   * Call status
   * Agent/workflow used

### Call Details

Click on any call to see:

* **Call Recording** - Listen to the full conversation
* **Transcript** - Read the conversation transcript
* **Agent Performance** - See how your agent handled the call
* **Metadata** - Call duration, timestamps, etc.

## Troubleshooting

### Calls Not Connecting

If calls aren't connecting:

1. **Check Twilio Configuration**
   * Verify webhooks are set correctly in Twilio
   * Ensure Twilio integration is still connected
   * Check Twilio account status

2. **Verify Phone Number Status**
   * Confirm the number is active in Freya
   * Check that inbound routing is configured
   * Ensure agent/workflow exists and is active

3. **Check Call Logs**
   * Look for error messages in call logs
   * Check if calls are being received but failing
   * Review any error notifications

### Agent Not Responding

If the agent doesn't respond:

1. **Check Agent Configuration**
   * Verify the agent is properly configured
   * Ensure the system prompt is set
   * Check that the model is selected

2. **Test Agent Separately**
   * Use simulations to test the agent
   * Verify the agent works outside of phone calls
   * Check for configuration errors

3. **Review Call Transcripts**
   * See what the agent heard
   * Check if there were any errors
   * Verify the conversation flow

### Poor Call Quality

If call quality is poor:

1. **Check Network Connection**
   * Ensure stable internet connection
   * Verify Twilio connection quality
   * Check for network issues

2. **Review Voice Settings**
   * Adjust voice provider settings
   * Try different voice options
   * Check voice speed and stability

3. **Monitor Call Metrics**
   * Check call duration
   * Review drop rates
   * Analyze quality metrics

## Best Practices

<Tip>
  Always test your setup with simulations before going live with real calls.
</Tip>

<Tip>
  Monitor call logs regularly to identify issues early and improve agent performance.
</Tip>

<Tip>
  Start with simple agent configurations and gradually add complexity as you gain experience.
</Tip>

<Warning>
  Make sure your agent is properly configured before connecting it to a production phone number. Test thoroughly first.
</Warning>

## Going Live

Once you've tested and verified everything works:

1. **Monitor First Calls** - Watch the first few real calls closely
2. **Review Performance** - Check how your agent handles real conversations
3. **Iterate Quickly** - Make adjustments based on real call data
4. **Scale Gradually** - Start with one number and expand as you gain confidence

## Next Steps

<Card title="Start Initiating Outbound Calls" icon="phone-outgoing" href="/basic-operations/initiating-outbound-calls">
  Learn how to start making outbound calls and running campaigns.
</Card>

<Card title="View Analytics" icon="chart-bar" href="/analytics">
  Monitor your call performance and agent analytics.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.