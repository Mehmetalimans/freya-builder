> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Request export

> Requests a data export from one of the supported endpoints. The export can be delivered as a direct download URL or sent via email.

**Supported Endpoints:**
- `/api/v2/call` - Export calls
- `/api/v2/campaign` - Export campaigns
- `/api/v2/phone-numbers` - Export phone numbers
- `/api/v2/feedbacks` - Export feedbacks

**Export Formats:**
- `csv` - Comma-separated values
- `xlsx` - Excel spreadsheet
- `markdown` - Markdown table
- `json` - JSON array

The `params` object should include the same query parameters you would use when calling the endpoint directly, including `workspaceId`.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json post /export
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
  /export:
    post:
      tags:
        - Export
      summary: Request export
      description: >-
        Requests a data export from one of the supported endpoints. The export
        can be delivered as a direct download URL or sent via email.


        **Supported Endpoints:**

        - `/api/v2/call` - Export calls

        - `/api/v2/campaign` - Export campaigns

        - `/api/v2/phone-numbers` - Export phone numbers

        - `/api/v2/feedbacks` - Export feedbacks


        **Export Formats:**

        - `csv` - Comma-separated values

        - `xlsx` - Excel spreadsheet

        - `markdown` - Markdown table

        - `json` - JSON array


        The `params` object should include the same query parameters you would
        use when calling the endpoint directly, including `workspaceId`.
      operationId: requestExport
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PostExportRequest'
      responses:
        '200':
          description: Export ready or email sent
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
                        $ref: '#/components/schemas/PostExportResponse'
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
        '429':
          description: Too many export requests
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
        '503':
          description: Email export not configured
      security:
        - bearerAuth: []
components:
  schemas:
    PostExportRequest:
      type: object
      properties:
        endpoint:
          type: string
          enum:
            - /api/v2/call
            - /api/v2/campaign
            - /api/v2/phone-numbers
            - /api/v2/feedbacks
          description: API endpoint to export data from
        params:
          type: object
          additionalProperties:
            type: string
          description: Query parameters to pass to the endpoint (must include workspaceId)
        format:
          type: string
          enum:
            - csv
            - xlsx
            - markdown
            - json
          default: csv
          description: Export file format
        deliveryMethod:
          type: string
          enum:
            - download
            - email
          default: download
          description: How to deliver the export
        email:
          type:
            - string
            - 'null'
          format: email
          description: Email address for email delivery
      required:
        - endpoint
        - params
    PostExportResponse:
      type: object
      properties:
        success:
          type: boolean
        downloadUrl:
          type: string
          format: uri
          description: Signed URL to download the export
        message:
          type: string
      required:
        - success
        - message
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer

````

This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.