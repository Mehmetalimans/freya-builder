> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Campaigns

> Launch outbound calling campaigns to reach customers at scale — with scheduling, retries, and real-time progress tracking

## What are Campaigns?

Campaigns let you make outbound calls to a list of customers automatically. You provide the phone numbers, choose which agent handles the conversation, set a schedule, and Freya works through the list — calling each customer, handling retries for failed attempts, and tracking progress in real time.

Common use cases include appointment reminders, payment follow-ups, customer surveys, sales outreach, and service notifications.

## Campaign Lifecycle

Every campaign moves through a series of statuses as it progresses:

| Status | Meaning |
| - | - |
| **Draft** | Campaign is created but hasn't started yet. You can still edit everything. |
| **Scheduled** | Campaign is configured with a future start date and waiting to begin. |
| **Active** | Campaign is currently making calls. |
| **Completed** | All customers have been called and all retries exhausted. |
| **Partially Completed** | Some calls failed and retries are exhausted, but not all customers were reached. You can retry these. |

## Creating a Campaign

### 1. Name and Description

Give your campaign a clear name so you can identify it later in the list. The name defaults to today's date, but you should use something descriptive — like "April Payment Reminders" or "Product Launch Outreach". The description is optional but helpful for team context.

### 2. Select a Phone Number

Choose which phone number Freya will call from. The dropdown only shows numbers that have **outbound SIP enabled** and an **agent or workflow configured** — if your number doesn't appear, check its configuration on the Phone Numbers page.

The phone number you pick determines which agent is pre-selected in the next step, based on the outbound agent configured for that number.

### 3. Choose an Agent

Select the agent that will handle conversations during the campaign. This is auto-populated from the phone number's outbound agent, but you can change it.

If your agent uses **variables** in its system prompt (like `{{customer_name}}` or `{{appointment_date}}`), those variables appear as columns in the customer table so you can provide personalized data for each call.

### 4. Add Customers

The customer table is where you enter the phone numbers to call. Each row represents one customer:

* **Phone number** (required) — the number to dial, in any common format
* **Custom properties** — additional columns appear automatically based on variables detected in your agent's prompt

Freya normalizes all phone numbers to **E.164 format** automatically. Use the country picker to set a default country code for numbers entered without one — for example, if you enter "555-1234" with the US country selected, it becomes "+15551234".

<Tip>
  The system validates for duplicates and empty numbers before you can start the campaign. If two rows have the same phone number, you'll be prompted to fix it.
</Tip>

### 5. Configure the Schedule

By default, campaigns start calling immediately. To schedule calls for later:

* **Start Date** — the first day calls will be made
* **Start Time / End Time** — the daily calling window (e.g., 9:00 AM to 6:00 PM)
* **Active Days** — which days of the week calls can happen (all seven enabled by default)
* **Timezone** — auto-detected from your browser, used for all schedule calculations

The summary at the bottom of the form shows exactly when calling will begin — either "Starting immediately" or "Starting on \[date] at \[time]".

### 6. Set Up Retries

If a call fails (busy signal, no answer, network error), Freya can automatically retry:

* **Call Retries** — number of retry attempts per customer (0–10, default 0)
* **Retry Delay** — seconds to wait between attempts (default 300 seconds / 5 minutes)
* **Retry Conditions** — which call outcomes trigger a retry (specific SIP codes and end reasons)

Retries respect the active days and calling window — they won't happen outside your configured schedule.

### 7. Webhook (Optional)

Under **Advanced Settings**, you can provide a webhook URL that receives a callback for each call as it completes. This is useful for updating external CRMs or triggering follow-up workflows in other systems.

### 8. Review and Start

The form shows a summary of your configuration — how many calls are queued, when they'll start, and the calling window. Click **Start Campaign** and confirm in the dialog to begin.

## Managing Campaigns

### The Campaign List

The campaigns page shows all your campaigns in a table with:

* **Campaign name** and description
* **Status** badge (Draft, Active, Scheduled, Completed, Partially Completed)
* **Phone Numbers** — the number of customers in the campaign
* **Created date**

Use the status filter buttons above the table to quickly narrow down to campaigns in a specific state.

### Campaign Actions

Right-click a campaign or use the actions menu to:

* **Duplicate** — create a copy of an existing campaign with the same configuration, useful for running similar campaigns with different customer lists
* **Retry** — available for Partially Completed campaigns, re-queues the customers that weren't successfully reached
* **Delete** — permanently remove a campaign (with confirmation)
* **Export to CSV** — download campaign data for reporting or external analysis

You can also select multiple campaigns using the checkboxes for **bulk delete** operations.

### Quick Campaign

For simple campaigns that don't need detailed scheduling, the **Quick Campaign** option opens a streamlined modal where you can set up and launch a campaign in seconds — just pick a number, add customers, and go.

## Best Practices

* **Name campaigns descriptively.** You'll accumulate campaigns over time. Names like "2026-04 Appointment Reminders - Dental" are much easier to find than "Campaign 47".
* **Test with a small list first.** Before launching a campaign to hundreds of customers, run it with 2–3 test numbers to verify the agent handles the conversation correctly and the variables are populated as expected.
* **Set reasonable calling windows.** Nobody wants a robot call at 7 AM. Configure start and end times that respect your customers' time zones and local regulations.
* **Use retries sparingly.** One or two retries with a 5-minute delay is usually enough. Excessive retries can annoy customers and waste resources.
* **Check your phone number configuration.** If a number doesn't appear in the dropdown, it's missing outbound SIP or an assigned agent. Fix it on the Phone Numbers page first.
* **Use the webhook for CRM integration.** If you track call outcomes in an external system, configure the webhook URL so each completed call automatically updates your records.

## Next Steps

<CardGroup cols={2}>
  <Card title="Phone Numbers" icon="phone" href="/guides/fundamentals/phone-numbers">
    Configure phone numbers with outbound SIP and agents so they're available for campaigns.
  </Card>

  <Card title="Analytics" icon="chart-line" href="/guides/features/analytics">
    Track campaign call performance, sentiment, and outcomes in the Analytics dashboard.
  </Card>
</CardGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.