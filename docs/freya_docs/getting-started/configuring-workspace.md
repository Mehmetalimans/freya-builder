> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuring Your Workspace

> Learn how to configure workspace settings, team members, and preferences

## Overview

After creating a workspace, you'll want to configure it to match your needs. This includes setting up workspace preferences, inviting team members, managing integrations, and configuring billing.

## Accessing Workspace Settings

To access workspace settings:

1. Click on the **Settings** icon in the top navigation bar
2. Or navigate to `/workspace/settings` in your browser

## Workspace Configuration Options

### Basic Information

Update your workspace's basic information:

* **Workspace Name** - Change the name of your workspace
* **Logo URL** - Update the workspace logo that appears in the header
* **Integration Version** - Choose between v1 and v2 integration versions

### Workspace Settings

Configure workspace-level preferences:

<ParamField body="language" type="string">
  Default language for the workspace. Options: English (en), Czech (cs), Spanish (es)
</ParamField>

<ParamField body="outboundEnabled" type="boolean">
  Enable or disable outbound calling capabilities for this workspace
</ParamField>

<ParamField body="creditsMonthlyAllowance" type="number">
  Monthly credit allowance for the workspace
</ParamField>

<ParamField body="resetDayOfMonth" type="number">
  Day of the month when credits reset (1-31)
</ParamField>

### Team Members

Manage who has access to your workspace:

#### Inviting Members

1. Click **"Invite Member"** in the Members section
2. Enter the email address of the person you want to invite
3. Select their role:
   * **Admin** - Full access to all workspace features
   * **Member** - Can create and manage resources but can't modify workspace settings
4. Click **"Send Invitation"**

The invited user will receive an email with an invitation link. Once they accept, they'll have access to the workspace.

#### Managing Members

* **View Members** - See all current workspace members and their roles
* **Remove Members** - Remove team members from the workspace
* **View Invitations** - See pending invitations and their status

### Assistant IDs

Configure assistant IDs for workspace integrations. These are used to connect your workspace with external systems.

## Saving Changes

After making any changes to workspace settings:

1. Click the **"Save"** button at the top of the settings page
2. Changes will be applied immediately
3. You'll see a success notification confirming the update

## Workspace Billing

Access billing settings to:

* View credit balance
* Manage subscription plans
* View usage history
* Configure payment methods

Navigate to **Workspace > Billing** to access billing settings.

## Best Practices

<Warning>
  Always save your changes after modifying workspace settings. Unsaved changes will be lost if you navigate away.
</Warning>

<Tip>
  Use descriptive workspace names to easily identify different projects or environments.
</Tip>

<Tip>
  Regularly review team member access to ensure only authorized users have access to your workspace.
</Tip>

## Next Steps

<Card title="Create Your First Agent" icon="robot" href="/basic-operations/creating-agent">
  Now that your workspace is configured, learn how to create your first AI agent.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.