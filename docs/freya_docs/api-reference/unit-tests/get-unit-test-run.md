> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get unit-test run

> Returns a single unit-test run, including its verdict and metrics.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json get /unit-tests/runs/{runId}
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
  /unit-tests/runs/{runId}:
    get:
      tags:
        - Unit Tests
      summary: Get unit-test run
      description: Returns a single unit-test run, including its verdict and metrics.
      operationId: getUnitTestRun
      parameters:
        - schema:
            type: string
            format: uuid
          required: true
          name: runId
          in: path
      responses:
        '200':
          description: Unit-test run details
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
                          id:
                            type: string
                            format: uuid
                          workspaceId:
                            type: string
                            format: uuid
                          unitTestId:
                            type: string
                            format: uuid
                          entityVersionId:
                            type: string
                            format: uuid
                          unitTestJobId:
                            type:
                              - string
                              - 'null'
                            format: uuid
                          outcome:
                            type: string
                            enum:
                              - queued
                              - running
                              - pass
                              - fail
                              - error
                          verdictReason:
                            type:
                              - string
                              - 'null'
                          agentResponse:
                            type:
                              - string
                              - 'null'
                          agentResponseMessageId:
                            type:
                              - string
                              - 'null'
                          latencyMs:
                            type:
                              - integer
                              - 'null'
                          judgeLatencyMs:
                            type:
                              - integer
                              - 'null'
                          judgeModel:
                            type:
                              - string
                              - 'null'
                          messages:
                            type:
                              - array
                              - 'null'
                            items:
                              type: object
                              additionalProperties: {}
                          assertionResults:
                            type:
                              - array
                              - 'null'
                            items:
                              type: object
                              properties:
                                index:
                                  type: integer
                                  minimum: 0
                                type:
                                  type: string
                                passed:
                                  type: boolean
                                detail:
                                  type:
                                    - string
                                    - 'null'
                                observed: {}
                              required:
                                - index
                                - type
                                - passed
                          metadata:
                            type: object
                            additionalProperties: {}
                          isStale:
                            type: boolean
                          startedAt:
                            type:
                              - string
                              - 'null'
                          completedAt:
                            type:
                              - string
                              - 'null'
                          createdAt:
                            type: string
                          updatedAt:
                            type: string
                        required:
                          - id
                          - workspaceId
                          - unitTestId
                          - entityVersionId
                          - unitTestJobId
                          - outcome
                          - verdictReason
                          - agentResponse
                          - agentResponseMessageId
                          - latencyMs
                          - judgeLatencyMs
                          - judgeModel
                          - messages
                          - assertionResults
                          - metadata
                          - isStale
                          - startedAt
                          - completedAt
                          - createdAt
                          - updatedAt
                    required:
                      - message
                      - result
                required:
                  - success
                  - data
        '400':
          description: Validation error
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
          description: Run not found
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