> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Phone Numbers

> Connect phone numbers to your agents for inbound and outbound calls — with SIP configuration, agent assignment, and regional endpoints

## What are Phone Numbers?

Phone numbers are the bridge between your AI agents and the real telephone network. Each number you add to Freya can receive inbound calls, make outbound calls, or both — depending on how you configure it.

When a call comes in on a number, Freya routes it to the agent you've assigned. When a campaign or API call dials out, it uses the outbound agent and SIP configuration you've set up on the number.

## The Phone Numbers Page

The phone numbers table shows all numbers in your workspace with the following columns:

| Column | What it shows |
| - | - |
| **Number** | The phone number in international format |
| **Friendly Name** | A human-readable label you assign (e.g., "Main Support Line") |
| **Agents** | Icons showing which agents are assigned for inbound and outbound |
| **Capabilities** | Visual indicators for what the number supports — inbound SIP (blue), outbound SIP (green), SMS (purple) |
| **Active Configuration** | Which endpoints are currently live (voice, messaging, or both) |

## Adding a Phone Number

Click **Create** to open the phone number form. The form is split into two columns: inbound configuration on the left, outbound on the right.

### General Settings

* **Phone Number** — enter the number in international format (e.g., +14155551234). A country picker helps with formatting. This field is required.
* **Friendly Name** — a descriptive label like "Sales Hotline" or "Support - US East". Required, and shown everywhere in the dashboard instead of the raw number.

### Inbound SIP Configuration

To receive calls on this number, configure the inbound SIP settings:

**Origination URI** — select the Freya SIP endpoint closest to your telephony provider. This is the address your provider sends calls to:

| Region | Endpoint |
| - | - |
| United States | `sip.us1.freyavoice.ai:5080` |
| Europe | `sip.eu1.freyavoice.ai:5080` |
| Turkey | `sip.tr.freyavoice.ai:5060` |

Choose the region that matches where your phone numbers are registered for the lowest latency and best call quality.

**Inbound Agent** — select which agent handles incoming calls on this number. When a call arrives, Freya connects the caller to this agent immediately.

### Outbound SIP Configuration

To make calls from this number (used by campaigns and the API), configure outbound SIP:

**Endpoint and Port** — the SIP server address and port of your telephony provider (e.g., `sip.provider.com:5060`). This is where Freya sends outbound call requests.

**Username and Password** — optional SIP authentication credentials if your provider requires them.

**From Domain** — an optional field that sets the domain in the SIP `From` header. Expand the collapsible section to configure this if your provider requires a specific domain for caller ID or routing.

**Outbound Agent** — select which agent handles outbound calls. This agent is used when campaigns dial out through this number, and is also auto-selected when you choose this number in the campaign creation form.

<Tip>
  A phone number needs both outbound SIP configuration **and** an outbound agent assigned before it appears in the campaign phone number dropdown. If your number is missing from campaigns, check these settings.
</Tip>

## Importing from Twilio

If you have phone numbers in a Twilio account, you can import them directly instead of configuring SIP manually:

1. Go to **Integrations** and connect your Twilio account
2. Return to the **Phone Numbers** page
3. Click **Import from Twilio**
4. Select the numbers you want to import

Imported numbers inherit their capabilities from Twilio and can be configured with agents immediately.

## Managing Phone Numbers

### Editing

Click any phone number row to open the edit form. You can change the friendly name, swap agents, or update SIP configuration at any time. Changes take effect immediately for the next call.

### Deleting

Delete a phone number from the actions menu. A confirmation dialog warns that the number will no longer receive calls. You can also select multiple numbers using checkboxes for bulk deletion.

<Note>
  Deleting a phone number from Freya does not release it from your telephony provider. You still own the number — it just won't be connected to Freya anymore.
</Note>

## Best Practices

* **Use descriptive friendly names.** When you have many numbers, names like "Support - US", "Sales - UK", and "Appointments - EU" are far easier to manage than remembering raw phone numbers.
* **Match the origination URI to your number's region.** A US number routed through the EU endpoint adds unnecessary latency to every call. Always pick the closest region.
* **Assign different agents for inbound vs. outbound.** An agent optimized for answering support calls isn't necessarily the best for making outbound campaign calls. Tailor each agent to its purpose.
* **Verify outbound configuration before launching campaigns.** Test an outbound call manually (using One-Click Call or a test campaign with one number) to confirm SIP credentials and agent behavior before dialing a full customer list.
* **Review unused numbers periodically.** Numbers with no recent calls may be costing you monthly fees from your provider without providing value. Either repurpose them or remove them.

## Next Steps

<CardGroup cols={2}>
  <Card title="Campaigns" icon="megaphone" href="/guides/features/campaigns">
    Use your configured phone numbers to launch outbound calling campaigns.
  </Card>

  <Card title="Integrations" icon="puzzle-piece" href="/guides/fundamentals/integrations">
    Connect your Twilio account to import phone numbers and enable outbound calling.
  </Card>
</CardGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.