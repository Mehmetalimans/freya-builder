> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# List feedbacks

> Returns feedbacks for a workspace with filters, sorting, pagination, and histogram data.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json get /feedbacks
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
  /feedbacks:
    get:
      tags:
        - Feedbacks
      summary: List feedbacks
      description: >-
        Returns feedbacks for a workspace with filters, sorting, pagination, and
        histogram data.
      operationId: listFeedbacks
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
            format: uuid
            description: Filter by specific call ID
          required: false
          description: Filter by specific call ID
          name: callId
          in: query
        - schema:
            type: string
            enum:
              - 1h
              - 24h
              - week
              - month
              - year
            description: Histogram bucket granularity
          required: false
          description: Histogram bucket granularity
          name: granularity
          in: query
        - schema:
            type: string
            description: Start date for histogram (ISO format)
          required: false
          description: Start date for histogram (ISO format)
          name: startDate
          in: query
        - schema:
            type: string
            description: End date for histogram (ISO format)
          required: false
          description: End date for histogram (ISO format)
          name: endDate
          in: query
        - schema:
            type: string
            enum:
              - active
              - all
              - archived
            default: active
            description: Filter by archive status
          required: false
          description: Filter by archive status
          name: archivedFilter
          in: query
        - schema:
            type: string
            description: Comma-separated feedback IDs to filter by
          required: false
          description: Comma-separated feedback IDs to filter by
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
          description: Feedbacks with pagination and summary
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
                          feedbacks:
                            type: array
                            items:
                              type: object
                              properties:
                                id:
                                  type: string
                                workspaceId:
                                  type:
                                    - string
                                    - 'null'
                                callId:
                                  type:
                                    - string
                                    - 'null'
                                  format: uuid
                                agentId:
                                  type:
                                    - string
                                    - 'null'
                                  format: uuid
                                title:
                                  type: string
                                  minLength: 1
                                description:
                                  type:
                                    - string
                                    - 'null'
                                proposedSolution:
                                  type:
                                    - string
                                    - 'null'
                                solutionNote:
                                  type:
                                    - string
                                    - 'null'
                                type:
                                  type:
                                    - string
                                    - 'null'
                                  enum:
                                    - workflow
                                    - decision-llm
                                    - stt
                                    - tts
                                    - vad-nc
                                    - latency
                                    - platform
                                    - ui
                                    - general
                                    - null
                                severity:
                                  type: number
                                  minimum: 0
                                  maximum: 1
                                  default: 0.5
                                status:
                                  type: string
                                  default: open
                                assignedTo:
                                  type:
                                    - string
                                    - 'null'
                                createdBy:
                                  type: string
                                  default: ai
                                messageId:
                                  type:
                                    - string
                                    - 'null'
                                resolved:
                                  type: boolean
                                  default: false
                                resolvedAt:
                                  type:
                                    - string
                                    - 'null'
                                resolvedBy:
                                  type:
                                    - string
                                    - 'null'
                                solutionId:
                                  type:
                                    - string
                                    - 'null'
                                  format: uuid
                                resolvedByVersionId:
                                  type:
                                    - string
                                    - 'null'
                                  format: uuid
                                number:
                                  type:
                                    - integer
                                    - 'null'
                                createdAt:
                                  type: string
                                updatedAt:
                                  type: string
                                callStartedAt:
                                  type:
                                    - string
                                    - 'null'
                                customerNumber:
                                  type:
                                    - string
                                    - 'null'
                                entityVersionId:
                                  type:
                                    - string
                                    - 'null'
                                  format: uuid
                                versionNumber:
                                  type:
                                    - integer
                                    - 'null'
                                callReviewTag:
                                  type:
                                    - string
                                    - 'null'
                                callReviewNotes:
                                  type:
                                    - string
                                    - 'null'
                                webCallerName:
                                  type:
                                    - string
                                    - 'null'
                                webCallerUserId:
                                  type:
                                    - string
                                    - 'null'
                                hasExternalReference:
                                  type: boolean
                                externalReferences:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      id:
                                        type: string
                                      url:
                                        type: string
                                      label:
                                        type:
                                          - string
                                          - 'null'
                                    required:
                                      - id
                                      - url
                                      - label
                                agentName:
                                  type:
                                    - string
                                    - 'null'
                                agentEntityType:
                                  type:
                                    - string
                                    - 'null'
                                agentWorkflowId:
                                  type:
                                    - string
                                    - 'null'
                                resolvedByName:
                                  type:
                                    - string
                                    - 'null'
                                assignees:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      userId:
                                        type: string
                                      userName:
                                        type:
                                          - string
                                          - 'null'
                                      assignedAt:
                                        type: string
                                    required:
                                      - userId
                                      - assignedAt
                                commentsCount:
                                  type: number
                                openSolutions:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      branchId:
                                        type: string
                                      name:
                                        type: string
                                      entityType:
                                        type: string
                                      entityId:
                                        type: string
                                    required:
                                      - branchId
                                      - name
                                      - entityType
                                      - entityId
                                isArchived:
                                  type: boolean
                                  default: false
                              required:
                                - title
                          pagination:
                            type: object
                            properties:
                              total:
                                type: number
                              limit:
                                type: number
                              offset:
                                type: number
                            required:
                              - total
                              - limit
                              - offset
                          summary:
                            type: object
                            properties:
                              total:
                                type: number
                              resolved:
                                type: number
                              unresolved:
                                type: number
                              byType:
                                type: object
                                additionalProperties:
                                  type: number
                              byStatus:
                                type: object
                                additionalProperties:
                                  type: number
                            required:
                              - total
                              - resolved
                              - unresolved
                              - byType
                          histogram:
                            type: array
                            items:
                              type: object
                              properties:
                                timestamp:
                                  type: string
                                total:
                                  type: number
                                resolved:
                                  type: number
                                unresolved:
                                  type: number
                                filteredTotal:
                                  type: number
                                filteredResolved:
                                  type: number
                                filteredUnresolved:
                                  type: number
                              required:
                                - timestamp
                                - total
                                - resolved
                                - unresolved
                                - filteredTotal
                                - filteredResolved
                                - filteredUnresolved
                          uniqueStatuses:
                            type: array
                            items:
                              type: string
                        required:
                          - success
                          - feedbacks
                          - pagination
                          - summary
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