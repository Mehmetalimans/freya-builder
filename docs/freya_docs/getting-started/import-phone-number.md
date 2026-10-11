> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Import a Phone Number

> Learn how to import phone numbers from Twilio and other providers into Freya

## Overview

Before you can start making and receiving calls, you need to import phone numbers into Freya. Freya supports importing phone numbers from various providers, with Twilio being the primary supported provider.

## Prerequisites

Before importing a phone number, you need:

1. **A Twilio Account** - Sign up at [twilio.com](https://www.twilio.com) if you don't have one
2. **Twilio Phone Number** - Purchase or have a phone number in your Twilio account
3. **Twilio Integration Connected** - Connect your Twilio account in Freya's integrations page

## Connecting Twilio Integration

Before you can import phone numbers, you must connect your Twilio account:

### Step 1: Navigate to Integrations

1. Click on **"Integrations"** in the sidebar navigation
2. Find the **Twilio** integration card

### Step 2: Connect Twilio

1. Click **"Connect"** on the Twilio integration
2. Enter your Twilio credentials:
   * **Account SID** - Found in your Twilio console
   * **Auth Token** - Found in your Twilio console
3. Click **"Save"** to connect

<Warning>
  Keep your Twilio credentials secure. Never share them publicly.
</Warning>

## Importing a Phone Number

### Step 1: Navigate to Phone Numbers

1. Click on **"Phone Numbers"** in the sidebar navigation
2. You'll see a list of all imported phone numbers

### Step 2: Start Import Process

1. Click the **"Import"** button in the top right
2. A modal will open showing available providers

### Step 3: Select Provider

If Twilio is connected, you'll see:

* **Twilio** - Available (if connected)
* Other providers - May show as "Not Connected"

Click on **Twilio** to proceed.

### Step 4: Enter Phone Number

1. Enter the phone number you want to import
2. Use the phone input field with country code selection
3. Or use raw input mode for custom formats
4. Click **"Import"**

### Step 5: Verify Import

After clicking import:

1. Freya will fetch the phone number details from Twilio
2. The number will be added to your workspace
3. You'll see a success notification
4. The phone number will appear in your phone numbers list

## Imported Phone Number Details

After importing, the phone number will have:

* **Phone Number** - The actual number (e.g., +1234567890)
* **Friendly Name** - A display name for the number
* **Capabilities** - Voice, SMS, MMS, etc.
* **Status** - Active, pending, etc.
* **Provider** - Twilio or other provider

## Phone Number Configuration

After importing, you'll need to:

1. **Configure the number** - Set up inbound and outbound routing
2. **Connect to agents/workflows** - Link the number to your AI agents or workflows
3. **Set capabilities** - Enable voice, SMS, etc.

<Card title="Connect a Phone Number" icon="link" href="/basic-operations/connect-phone-number">
  Learn how to connect your imported phone number to agents or workflows.
</Card>

## Troubleshooting

### Twilio Not Connected

If you see "Twilio Not Connected":

1. Navigate to **Integrations**
2. Connect your Twilio account
3. Verify your credentials are correct
4. Try importing again

### Phone Number Not Found

If the import fails with "Phone number not found":

1. Verify the number exists in your Twilio account
2. Check that you're using the correct format (with country code)
3. Ensure the number is active in Twilio
4. Try using raw input mode with the exact Twilio format

### Import Errors

If you encounter errors:

1. Check your Twilio account has sufficient credits
2. Verify your Twilio credentials are still valid
3. Check that the phone number hasn't been deleted in Twilio
4. Contact support if issues persist

## Best Practices

<Tip>
  Import all phone numbers you plan to use before configuring them. This makes setup easier.
</Tip>

<Tip>
  Use descriptive friendly names for phone numbers to easily identify their purpose.
</Tip>

<Warning>
  Imported phone numbers are linked to your Twilio account. If you disconnect Twilio, you may lose access to these numbers.
</Warning>

## Next Steps

<Card title="Connect a Phone Number" icon="link" href="/basic-operations/connect-phone-number">
  After importing, learn how to connect your phone number to agents or workflows.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.