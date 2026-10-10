> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Call outcome webhook

> Sent to the campaign's webhookUrl when a call completes or fails.

**Payload Types:**
- **WebhookCallOutcome**: Sent when a call completes (success or failure with ended_reason)
- **WebhookApiError**: Sent when call initiation fails before a call is created

**Failure Categories:**
- `no_answer`: Customer didn't answer
- `busy`: Line was busy
- `voicemail`: Reached voicemail
- `timeout`: Call timed out (infrastructure)
- `api_error`: API call failed before call started
- `llm_fail`: LLM evaluation failed (if successPrompt configured)
- `other`: Unknown failure

**Retry Behavior:**
- If `willRetry: true`, check `retryScheduledAt` for next attempt time
- Retries respect the campaign's schedule (activeDays, startTime, endTime, and daySchedules overrides)
- `retriesRemaining` shows how many retries are left



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json post /webhooks/campaign-call-outcome
openapi: 3.1.0
info:
  title: Freyavoice API
  version: 2.0.0
  description: >-
    Production API for managing calls and campaigns.


    **Authentication**: All endpoints require a bearer token issued by
    Freyavoice.


    **Response Format**: All responses are wrapped in a standard envelope:

    ```json

    {
      "success": true,
      "data": {
        "message": "Success",
        "result": { /* endpoint-specific data */ }
      }
    }

    ```


    Error responses follow the same format with `success: false`:

    ```json

    {
      "success": false,
      "data": {
        "message": "Error description",
        "result": null
      }
    }

    ```
  contact:
    name: Freyavoice Support
    email: support@freyavoice.com
servers:
  - url: https://app.freyavoice.ai/api/v2
    description: Production
security: []
tags:
  - name: Agents
    description: Manage AI agents
  - name: Analytics
    description: Call analytics and metrics
  - name: API Keys
    description: API key management
  - name: Audio
    description: Audio transcription and speech synthesis
  - name: Calls
    description: Call management and history
  - name: Call Recordings
    description: Call recording management
  - name: Call Tags
    description: Call tagging and categorization
  - name: Campaigns
    description: Campaign management
  - name: Chat
    description: Stateful text chat with agents and workflows
  - name: Custom
    description: Custom convenience endpoints
  - name: Export
    description: Data export
  - name: Insights
    description: Structured data field definitions
  - name: Agent Insights
    description: Agent-to-field assignments
  - name: Integrations
    description: Third-party integrations
  - name: Personas
    description: Simulation personas for agent testing
  - name: Phone Numbers
    description: Phone number management
  - name: Phone Aliases
    description: Workspace phone book (phone-number to label mappings)
  - name: Suppression List
    description: Workspace do-not-call (DNC) list; numbers blocked from outbound dialing
  - name: Feedbacks
    description: Feedback tracking
  - name: Feedback Assignees
    description: Feedback assignment
  - name: Feedback Comments
    description: Feedback comments
  - name: Feedback References
    description: Feedback cross-references to other entities
  - name: Feedback Status Config
    description: Feedback status configuration
  - name: Reviews
    description: Call reviews
  - name: Review Assignees
    description: Review assignment
  - name: Simulations
    description: Agent simulation testing
  - name: Simulation Iterations
    description: Simulation iteration history
  - name: Unit Tests
    description: Behavioural unit tests for agents and workflows
  - name: Branches
    description: Branches (proposed changes) of an agent or workflow version line
  - name: Webhooks
    description: Webhook configuration
  - name: Versions
    description: Version history and rollback for agents and workflows
  - name: Workflows
    description: Workflow management
  - name: Workspaces
    description: Workspace management
  - name: Workspace Credits
    description: Workspace credit balance
  - name: Workspace Invitations
    description: Workspace invitations
  - name: Workspace Logs
    description: Workspace activity logs
  - name: Workspace Members
    description: Workspace member management
  - name: Workspace Roles
    description: Custom roles and permissions per workspace
  - name: Permissions
    description: Permission catalog (used by role + API-key UIs)
paths:
  /webhooks/campaign-call-outcome:
    post:
      tags:
        - Webhooks
      summary: Call outcome webhook
      description: >-
        Sent to the campaign's webhookUrl when a call completes or fails.


        **Payload Types:**

        - **WebhookCallOutcome**: Sent when a call completes (success or failure
        with ended_reason)

        - **WebhookApiError**: Sent when call initiation fails before a call is
        created


        **Failure Categories:**

        - `no_answer`: Customer didn't answer

        - `busy`: Line was busy

        - `voicemail`: Reached voicemail

        - `timeout`: Call timed out (infrastructure)

        - `api_error`: API call failed before call started

        - `llm_fail`: LLM evaluation failed (if successPrompt configured)

        - `other`: Unknown failure


        **Retry Behavior:**

        - If `willRetry: true`, check `retryScheduledAt` for next attempt time

        - Retries respect the campaign's schedule (activeDays, startTime,
        endTime, and daySchedules overrides)

        - `retriesRemaining` shows how many retries are left
      operationId: campaignCallOutcomeWebhook
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WebhookCallOutcome'
      responses:
        '200':
          description: Webhook received successfully
components:
  schemas:
    WebhookCallOutcome:
      type: object
      properties:
        callId:
          type: string
        campaignId:
          type: string
        phoneNumber:
          type: string
        outcome:
          type: string
          enum:
            - success
            - failed
        failureCategory:
          type: string
          description: SipCodeCategory value or 'api_error' if outcome is 'failed'
        message:
          type: string
          description: >-
            Contextual message: ended_reason, timeout message, or LLM evaluation
            reason
        willRetry:
          type: boolean
          description: Whether the call will be retried
        retryScheduledAt:
          type: string
          format: date-time
          description: ISO8601 timestamp when retry is scheduled
        retriesRemaining:
          type: number
          description: Number of retries remaining
        attemptNumber:
          type: number
          description: Which attempt this outcome is for (1-indexed)
      required:
        - campaignId
        - phoneNumber
        - outcome

````

This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.