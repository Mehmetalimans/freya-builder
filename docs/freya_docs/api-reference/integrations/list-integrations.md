> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# List integrations

> Returns available integrations with optional connection status for the workspace.

When `detail=true`, returns full integration metadata from Nango including available actions, endpoints, and whether the workspace has an active connection.

When `detail=false` (default), returns only connected integrations from the database.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json get /integrations
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
  /integrations:
    get:
      tags:
        - Integrations
      summary: List integrations
      description: >-
        Returns available integrations with optional connection status for the
        workspace.


        When `detail=true`, returns full integration metadata from Nango
        including available actions, endpoints, and whether the workspace has an
        active connection.


        When `detail=false` (default), returns only connected integrations from
        the database.
      operationId: listIntegrations
      parameters:
        - schema:
            type: integer
            exclusiveMinimum: 0
            maximum: 100
            default: 50
            description: Maximum number of results to return (1-100)
          required: false
          description: Maximum number of results to return (1-100)
          name: limit
          in: query
        - schema:
            type:
              - integer
              - 'null'
            minimum: 0
            default: 0
            description: Number of results to skip for pagination
          required: false
          description: Number of results to skip for pagination
          name: offset
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
            format: uuid
            description: Workspace ID
          required: true
          description: Workspace ID
          name: workspaceId
          in: query
        - schema:
            type:
              - boolean
              - 'null'
            default: false
            description: Include detailed integration metadata
          required: false
          description: Include detailed integration metadata
          name: detail
          in: query
      responses:
        '200':
          description: Integrations list
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
                          integrations:
                            type: array
                            items:
                              anyOf:
                                - type: object
                                  properties:
                                    id:
                                      type: string
                                      format: uuid
                                    workspaceId:
                                      type: string
                                      format: uuid
                                    integrationType:
                                      type: string
                                      minLength: 1
                                      maxLength: 50
                                    nangoConnectionId:
                                      type: string
                                      minLength: 1
                                      maxLength: 255
                                    connectedAt:
                                      type: string
                                      format: date-time
                                  required:
                                    - id
                                    - workspaceId
                                    - integrationType
                                    - nangoConnectionId
                                    - connectedAt
                                - type: object
                                  properties:
                                    unique_key:
                                      type: string
                                    display_name:
                                      type: string
                                    provider:
                                      type: string
                                    logo:
                                      type: string
                                    created_at:
                                      type: string
                                    updated_at:
                                      type: string
                                    connection:
                                      type:
                                        - object
                                        - 'null'
                                      properties:
                                        id:
                                          type: string
                                          format: uuid
                                        workspaceId:
                                          type: string
                                          format: uuid
                                        integrationType:
                                          type: string
                                          minLength: 1
                                          maxLength: 50
                                        nangoConnectionId:
                                          type: string
                                          minLength: 1
                                          maxLength: 255
                                        connectedAt:
                                          type: string
                                          format: date-time
                                      required:
                                        - id
                                        - workspaceId
                                        - integrationType
                                        - nangoConnectionId
                                        - connectedAt
                                    config:
                                      type: object
                                      properties:
                                        provider:
                                          type: string
                                        providerConfigKey:
                                          type: string
                                        actions:
                                          type: array
                                          items:
                                            type: object
                                            properties:
                                              id:
                                                type: number
                                                exclusiveMinimum: 0
                                              name:
                                                type: string
                                                minLength: 1
                                                maxLength: 255
                                              type:
                                                type: string
                                                enum:
                                                  - action
                                                  - sync
                                                  - webhook
                                                default: action
                                              returns:
                                                type: array
                                                items:
                                                  type: string
                                                  minLength: 1
                                              description:
                                                type: string
                                                minLength: 1
                                              attributes:
                                                type: object
                                                additionalProperties: {}
                                                default: {}
                                              scopes:
                                                type: array
                                                items:
                                                  type: string
                                                default: []
                                              version:
                                                type: string
                                                pattern: ^\d+\.\d+\.\d+$
                                              is_public:
                                                type: boolean
                                                default: false
                                              pre_built:
                                                type: boolean
                                                default: false
                                              endpoints:
                                                type: array
                                                items:
                                                  type: object
                                                  properties:
                                                    method:
                                                      type: string
                                                      enum:
                                                        - GET
                                                        - POST
                                                        - PUT
                                                        - DELETE
                                                        - PATCH
                                                        - HEAD
                                                        - OPTIONS
                                                    path:
                                                      type: string
                                                      minLength: 1
                                                    group:
                                                      type:
                                                        - string
                                                        - 'null'
                                                  required:
                                                    - method
                                                    - path
                                                minItems: 1
                                              input:
                                                type: string
                                                minLength: 1
                                              enabled:
                                                type: boolean
                                                default: true
                                              last_deployed:
                                                type: string
                                                format: date-time
                                              webhookSubscriptions:
                                                type: array
                                                items: {}
                                                default: []
                                              json_schema:
                                                type: object
                                                additionalProperties: {}
                                              sdk_version:
                                                type: string
                                              is_zero_yaml:
                                                type: boolean
                                              models:
                                                type: array
                                                items:
                                                  type: object
                                                  properties:
                                                    name:
                                                      type: string
                                                      minLength: 1
                                                    fields:
                                                      type: array
                                                      items: {}
                                                  required:
                                                    - name
                                                    - fields
                                                default: []
                                            required:
                                              - id
                                              - name
                                              - returns
                                              - description
                                              - version
                                              - endpoints
                                              - input
                                              - last_deployed
                                      required:
                                        - provider
                                        - providerConfigKey
                                        - actions
                                    orphaned:
                                      type: boolean
                                  required:
                                    - unique_key
                                    - display_name
                                    - provider
                                    - logo
                                    - created_at
                                    - updated_at
                          total:
                            type: integer
                            minimum: 0
                          limit:
                            type: integer
                            exclusiveMinimum: 0
                          offset:
                            type: integer
                            minimum: 0
                        required:
                          - integrations
                          - total
                          - limit
                          - offset
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