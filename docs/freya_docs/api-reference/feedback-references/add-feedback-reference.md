> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Add feedback reference

> Links a feedback to an entity in the same workspace. Returns the full list.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json post /feedbacks/{feedbackId}/references
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
  /feedbacks/{feedbackId}/references:
    post:
      tags:
        - Feedback References
      summary: Add feedback reference
      description: >-
        Links a feedback to an entity in the same workspace. Returns the full
        list.
      operationId: addFeedbackReference
      parameters:
        - schema:
            type: string
            format: uuid
            description: Feedback ID
          required: true
          description: Feedback ID
          name: feedbackId
          in: path
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                entityType:
                  type: string
                  enum:
                    - persona
                    - simulation
                    - call
                    - version
                    - agent
                    - workflow
                    - branch
                    - external
                  description: Referenced entity type
                entityId:
                  type: string
                  format: uuid
                  description: Referenced entity ID (internal types)
                url:
                  type: string
                  maxLength: 2048
                  format: uri
                  description: External tracker URL (ClickUp, GitHub, ...)
                label:
                  type: string
                  maxLength: 200
                  description: Display label for external references
                relation:
                  type: string
                  enum:
                    - concerns
                    - caused_by
                    - relates
                  description: Reference relation
              required:
                - entityType
      responses:
        '200':
          description: Reference added
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    enum:
                      - true
                  data:
                    type: object
                    properties:
                      message:
                        type: string
                      result:
                        type: object
                        properties:
                          success:
                            type: boolean
                          references:
                            type: array
                            items:
                              type: object
                              properties:
                                id:
                                  type: string
                                feedbackId:
                                  type: string
                                entityType:
                                  type: string
                                  enum:
                                    - persona
                                    - simulation
                                    - call
                                    - version
                                    - agent
                                    - workflow
                                    - branch
                                    - external
                                entityId:
                                  type:
                                    - string
                                    - 'null'
                                relation:
                                  type: string
                                  enum:
                                    - concerns
                                    - caused_by
                                    - relates
                                url:
                                  type:
                                    - string
                                    - 'null'
                                label:
                                  type:
                                    - string
                                    - 'null'
                                createdBy:
                                  type:
                                    - string
                                    - 'null'
                                createdAt:
                                  type: string
                              required:
                                - id
                                - feedbackId
                                - entityType
                                - entityId
                                - relation
                                - createdAt
                        required:
                          - success
                          - references
                    required:
                      - message
                      - result
                required:
                  - success
                  - data
        '400':
          description: Referenced entity not found in workspace
        '401':
          description: Missing or invalid token
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    enum:
                      - false
                  data:
                    type: object
                    properties:
                      message:
                        type: string
                      result: {}
                    required:
                      - message
                required:
                  - success
                  - data
        '403':
          description: Workspace ID mismatch or insufficient permissions
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    enum:
                      - false
                  data:
                    type: object
                    properties:
                      message:
                        type: string
                      result: {}
                    required:
                      - message
                required:
                  - success
                  - data
        '404':
          description: Feedback not found
        '500':
          description: Server error
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    enum:
                      - false
                  data:
                    type: object
                    properties:
                      message:
                        type: string
                      result: {}
                    required:
                      - message
                required:
                  - success
                  - data
      security:
        - bearerAuth: []
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer

````

This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.