> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Workspaces

> Understanding workspaces and how to effectively organize your Freyavoice AI resources

## What Are Workspaces?

Workspaces are the foundational organizational unit in Freyavoice AI. They serve as containers that isolate and organize all your resources including agents, workflows, phone numbers, team members, settings, and integrations.

## Workspace Structure

Each workspace is a self-contained environment with:

**Resources**: All agents, workflows, and phone numbers belong to a specific workspace. This isolation ensures that resources from different projects or clients don't interfere with each other.

**Team Members**: Workspaces have their own team with different roles (admin, member). Team members can be invited, assigned roles, and managed independently per workspace.

**Settings**: Each workspace has its own configuration including language preferences, credit allowances, outbound calling settings, and integration versions.

**Integrations**: Workspace-level integrations allow you to connect external services like Twilio, HubSpot, or custom APIs that are specific to that workspace.

**Billing**: Workspaces can have independent billing and credit management, making it easy to track costs per project or client.

## When to Use Multiple Workspaces

### Project-Based Organization

Create separate workspaces for different projects. This keeps resources organized and makes it easy to manage multiple client projects or internal initiatives independently.

**Example**: You might have workspaces for "Client A Support", "Client B Sales", and "Internal Testing".

### Environment Separation

Use different workspaces for development, staging, and production environments. This prevents accidental changes to production resources and allows safe testing.

**Example**: "Production", "Staging", and "Development" workspaces with appropriate access controls.

### Team or Department Organization

Organize workspaces by team or department. Each team can manage their own resources without interfering with others.

**Example**: "Sales Team", "Support Team", and "Marketing Team" workspaces.

### Client Isolation

For agencies or service providers, create separate workspaces for each client. This ensures complete data isolation and makes client management easier.

**Example**: Each client gets their own workspace with their branding, settings, and resources.

## Workspace Management

### Creating Workspaces

When creating a new workspace, consider:

**Naming**: Use descriptive names that clearly indicate the workspace's purpose. Good names make it easy to identify workspaces at a glance.

**Initial Settings**: Configure default language, credit allowances, and other settings during creation. You can always change these later, but setting them up front saves time.

**Logo and Branding**: Add workspace logos and branding elements to make the dashboard feel customized for each workspace.

### Workspace Settings

Key settings to configure:

**Language**: Set the default language for the workspace. This affects agent behavior, UI language, and default voice settings.

**Outbound Enabled**: Control whether outbound calling is allowed in this workspace. Disable for workspaces that should only handle inbound calls.

**Credit Management**: Configure monthly credit allowances and reset schedules. This helps control costs and manage budgets per workspace.

**Integration Version**: Choose between v1 and v2 integration versions based on your needs and compatibility requirements.

### Team Management

**Inviting Members**: Invite team members by email. They'll receive an invitation link to join the workspace.

**Role Assignment**: Assign appropriate roles:

* **Admin**: Full access to all workspace features including settings and billing
* **Member**: Can create and manage resources but cannot modify workspace settings

**Member Management**: View all members, their roles, and when they joined. Remove members when they no longer need access.

**Display Names**: Each member can have a display name that appears throughout the workspace. This personalizes the experience.

## Workspace Best Practices

### Organization Strategy

**Consistent Naming**: Use a consistent naming convention across workspaces. This makes it easier to find and manage workspaces as your organization grows.

**Documentation**: Document the purpose of each workspace, what resources it contains, and who has access. This helps team members understand the workspace structure.

**Regular Cleanup**: Periodically review and archive or delete unused workspaces to keep your workspace list manageable.

### Security Considerations

**Access Control**: Only invite team members who need access. Regularly review member lists and remove access when no longer needed.

**Role Management**: Use the principle of least privilege. Give members only the permissions they need, not admin access by default.

**Workspace Isolation**: Remember that workspaces are isolated. Resources in one workspace cannot access resources in another without explicit sharing mechanisms.

### Cost Management

**Credit Allocation**: Set appropriate credit allowances per workspace based on expected usage. Monitor usage to adjust as needed.

**Usage Tracking**: Use workspace-level analytics to track usage and costs. This helps identify which workspaces are consuming the most resources.

**Budget Planning**: Plan credit allocations based on workspace needs. Production workspaces may need higher allowances than development workspaces.

## Workspace Analytics

Each workspace provides analytics including:

**Call Volume**: Track calls per workspace to understand usage patterns.

**Resource Usage**: See how many agents, workflows, and phone numbers are in use.

**Team Activity**: Monitor team member activity and contributions.

**Cost Tracking**: Track credits consumed and costs per workspace.

## Next Steps

<Card title="Agents" icon="robot" href="/guides/fundamentals/agents">
  Learn about creating and managing AI agents in your workspace.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.