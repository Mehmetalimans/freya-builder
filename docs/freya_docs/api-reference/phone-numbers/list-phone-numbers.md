> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# List phone numbers

> Returns phone numbers for a workspace with pagination, filtering, and optional counts by column.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json get /phone-numbers
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
  /phone-numbers:
    get:
      tags:
        - Phone Numbers
      summary: List phone numbers
      description: >-
        Returns phone numbers for a workspace with pagination, filtering, and
        optional counts by column.
      operationId: listPhoneNumbers
      parameters:
        - schema:
            type: string
            format: uuid
            description: Workspace ID
          required: true
          description: Workspace ID
          name: workspaceId
          in: query
        - schema:
            type: string
            description: Comma-separated phone number IDs to filter by
          required: false
          description: Comma-separated phone number IDs to filter by
          name: ids
          in: query
        - schema:
            type: string
            description: Filename (without extension) for export
          required: false
          description: Filename (without extension) for export
          name: exportFilename
          in: query
        - schema:
            type: string
            default: '25'
            description: Page size
          required: false
          description: Page size
          name: limit
          in: query
        - schema:
            type: string
            default: '0'
            description: Offset for pagination
          required: false
          description: Offset for pagination
          name: offset
          in: query
        - schema:
            type: string
            description: Base64-encoded filter state
          required: false
          description: Base64-encoded filter state
          name: filters
          in: query
        - schema:
            type: string
            description: Global search term
          required: false
          description: Global search term
          name: search
          in: query
        - schema:
            type: string
            description: Sort field name
          required: false
          description: Sort field name
          name: sortBy
          in: query
        - schema:
            type: string
            enum:
              - asc
              - desc
            description: Sort direction
          required: false
          description: Sort direction
          name: sortOrder
          in: query
        - schema:
            type: string
            description: Set to 'true' to return a file export
          required: false
          description: Set to 'true' to return a file export
          name: export
          in: query
        - schema:
            type: string
            enum:
              - csv
              - xlsx
              - markdown
            description: Export file format
          required: false
          description: Export file format
          name: exportFormat
          in: query
        - schema:
            type: string
            description: JSON array of column definitions {id,label}
          required: false
          description: JSON array of column definitions {id,label}
          name: exportColumns
          in: query
      responses:
        '200':
          description: Phone numbers with pagination
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
                          phoneNumbers:
                            type: array
                            items:
                              type: object
                              properties:
                                id:
                                  type: string
                                number:
                                  type: string
                                friendlyName:
                                  type:
                                    - string
                                    - 'null'
                                workspaceId:
                                  type: string
                                userId:
                                  type: string
                                config:
                                  type:
                                    - object
                                    - 'null'
                                  properties:
                                    capabilities:
                                      type: object
                                      properties:
                                        voice:
                                          type: string
                                        sms:
                                          type: boolean
                                    voiceConfig:
                                      type: string
                                    messagingConfig:
                                      type: string
                                    emergencyCalls:
                                      type: boolean
                                    inboundAgentId:
                                      type: string
                                      format: uuid
                                    outboundAgentId:
                                      type: string
                                      format: uuid
                                    originationUri:
                                      type: string
                                    sipInbound:
                                      type: object
                                      properties:
                                        enabled:
                                          type: boolean
                                      required:
                                        - enabled
                                    sipOutbound:
                                      type: object
                                      properties:
                                        enabled:
                                          type: boolean
                                        endpoint:
                                          type: string
                                          pattern: ^[A-Za-z0-9.\-]*$
                                        port:
                                          type: integer
                                          minimum: 1
                                          maximum: 65535
                                        username:
                                          type: string
                                          pattern: ^[A-Za-z0-9._+\-]*$
                                        password:
                                          type: string
                                        fromDomain:
                                          type: string
                                          pattern: ^[A-Za-z0-9.\-]*$
                                        transportProtocol:
                                          type: string
                                          enum:
                                            - UDP
                                            - TCP
                                            - TLS
                                        secureMedia:
                                          type: boolean
                                        headers:
                                          type: array
                                          items:
                                            type: object
                                            properties:
                                              key:
                                                type: string
                                              value:
                                                type: string
                                            required:
                                              - key
                                              - value
                                    routingPrefix:
                                      type: string
                                    defaultCountry:
                                      type: string
                                  additionalProperties: {}
                                createdAt:
                                  type: string
                                updatedAt:
                                  type: string
                                inboundAgentName:
                                  type:
                                    - string
                                    - 'null'
                                outboundAgentName:
                                  type:
                                    - string
                                    - 'null'
                                inboundAgentEntityType:
                                  type:
                                    - string
                                    - 'null'
                                outboundAgentEntityType:
                                  type:
                                    - string
                                    - 'null'
                                inboundAgentWorkflowId:
                                  type:
                                    - string
                                    - 'null'
                                outboundAgentWorkflowId:
                                  type:
                                    - string
                                    - 'null'
                              required:
                                - id
                                - number
                                - workspaceId
                                - userId
                                - createdAt
                                - updatedAt
                          pagination:
                            type: object
                            properties:
                              total:
                                type: number
                              limit:
                                type: number
                              offset:
                                type: number
                              hasNext:
                                type: boolean
                              hasPrevious:
                                type: boolean
                            required:
                              - total
                              - limit
                              - offset
                              - hasNext
                              - hasPrevious
                        required:
                          - phoneNumbers
                          - pagination
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