> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Creating a Workspace

> Learn how to create your first workspace in Freya

## Overview

A workspace is the foundation of your Freya setup. It organizes all your resources including agents, workflows, phone numbers, team members, and settings. When you first sign up for Freya, you'll need to create a workspace to get started.

## Creating Your First Workspace

When you first log into Freya, you'll see a screen prompting you to create your first workspace. Here's how to do it:

### Step 1: Access the Workspace Creation Dialog

If you don't have any workspaces yet, you'll automatically see the workspace creation screen. Otherwise, you can create a new workspace by:

1. Clicking on the workspace selector in the sidebar
2. Selecting "Create New Workspace" from the dropdown

### Step 2: Fill in Workspace Details

The workspace creation dialog requires the following information:

<ParamField body="name" type="string" required>
  The name of your workspace. This will be displayed throughout the dashboard.
</ParamField>

<ParamField body="displayName" type="string" required>
  Your display name - how you'd like to be addressed in this workspace.
</ParamField>

<ParamField body="logoPath" type="string">
  Optional URL to your workspace logo. This will be displayed in the header.
</ParamField>

<ParamField body="language" type="string">
  Default language for the workspace (English, Czech, or Spanish). Defaults to English.
</ParamField>

### Step 3: Create the Workspace

Once you've filled in the required fields:

1. Click the **"Create Workspace"** button
2. Your workspace will be created and you'll be automatically switched to it
3. You'll be redirected to the home page

## Workspace Features

After creating a workspace, you'll have access to:

* **Agents** - Create and manage AI voice agents
* **Workflows** - Build complex call routing workflows
* **Phone Numbers** - Import and configure phone numbers
* **Team Members** - Invite collaborators with different roles
* **Settings** - Configure workspace preferences
* **Billing** - Manage credits and subscriptions
* **Analytics** - View call analytics and insights

## Multiple Workspaces

You can create multiple workspaces to:

* Separate different projects or clients
* Organize by environment (development, staging, production)
* Manage different teams or departments
* Isolate resources for better organization

Each workspace maintains its own:

* Agents and workflows
* Phone numbers
* Team members and permissions
* Settings and configurations
* Credits and billing

## Next Steps

<Card title="Configure Your Workspace" icon="gear" href="/basic-operations/configuring-workspace">
  Learn how to configure workspace settings, invite team members, and customize your workspace.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.