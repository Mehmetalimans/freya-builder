> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Import calls from a raw ZIP export

> Accepts a multipart/form-data upload of a ZIP archive produced by /call/export-raw. Phase A inserts bundled workflows/agents/versions (ON CONFLICT DO NOTHING, flagged is_imported) so imported calls preserve their call → agent → workflow → version FK chain inside the target workspace. Phase B creates calls (flagged is_imported), uploads recordings to the target workspace S3 path, and inserts related tags/feedbacks/assertion results. Workspace-scoped; requires the `calls:import` permission.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json post /call/import
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
  /call/import:
    post:
      tags:
        - Calls
      summary: Import calls from a raw ZIP export
      description: >-
        Accepts a multipart/form-data upload of a ZIP archive produced by
        /call/export-raw. Phase A inserts bundled workflows/agents/versions (ON
        CONFLICT DO NOTHING, flagged is_imported) so imported calls preserve
        their call → agent → workflow → version FK chain inside the target
        workspace. Phase B creates calls (flagged is_imported), uploads
        recordings to the target workspace S3 path, and inserts related
        tags/feedbacks/assertion results. Workspace-scoped; requires the
        `calls:import` permission.
      operationId: importCalls
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              required:
                - workspaceId
                - file
              properties:
                workspaceId:
                  type: string
                  format: uuid
                file:
                  type: string
                  format: binary
                  description: ZIP archive
      responses:
        '200':
          description: Import summary
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
                          created:
                            type: number
                          skipped:
                            type: number
                          failed:
                            type: number
                          assertionSkipped:
                            type: number
                          agentsInserted:
                            type: number
                            default: 0
                          workflowsInserted:
                            type: number
                            default: 0
                          versionsInserted:
                            type: number
                            default: 0
                          errors:
                            type: array
                            items:
                              type: object
                              properties:
                                index:
                                  type: number
                                id:
                                  type:
                                    - string
                                    - 'null'
                                error:
                                  type: string
                              required:
                                - index
                                - id
                                - error
                        required:
                          - created
                          - skipped
                          - failed
                          - assertionSkipped
                          - errors
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