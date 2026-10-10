> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get version graph

> Returns every commit (mainline + all branch commits) and every branch for an entity in one payload, for the full commit-graph history view.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json get /versions/{entityType}/{entityId}/graph
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
  /versions/{entityType}/{entityId}/graph:
    get:
      tags:
        - Versions
      summary: Get version graph
      description: >-
        Returns every commit (mainline + all branch commits) and every branch
        for an entity in one payload, for the full commit-graph history view.
      operationId: getVersionGraph
      parameters:
        - schema:
            type: string
            enum:
              - agent
              - workflow
            description: 'Entity type: ''agent'' or ''workflow'''
          required: true
          description: 'Entity type: ''agent'' or ''workflow'''
          name: entityType
          in: path
        - schema:
            type: string
            format: uuid
          required: true
          name: entityId
          in: path
        - schema:
            type: string
            minLength: 1
          required: true
          name: entityId
          in: query
        - schema:
            type: string
            format: uuid
          required: true
          name: workspaceId
          in: query
      responses:
        '200':
          description: Commit graph nodes and branches
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
                          nodes:
                            type: array
                            items:
                              type: object
                              properties:
                                id:
                                  type: string
                                  format: uuid
                                versionNumber:
                                  type: integer
                                  exclusiveMinimum: 0
                                parentVersionId:
                                  type:
                                    - string
                                    - 'null'
                                  format: uuid
                                branchId:
                                  type:
                                    - string
                                    - 'null'
                                  format: uuid
                                isPublished:
                                  type: boolean
                                name:
                                  type:
                                    - string
                                    - 'null'
                                  maxLength: 200
                                  description: Commit subject
                                description:
                                  type:
                                    - string
                                    - 'null'
                                  description: Commit body
                                createdBy:
                                  type:
                                    - string
                                    - 'null'
                                  format: uuid
                                createdAt:
                                  type: string
                                  format: date-time
                                configDiffSummary:
                                  type:
                                    - array
                                    - 'null'
                                  items:
                                    type: object
                                    properties:
                                      section:
                                        type: string
                                      count:
                                        type: integer
                                        minimum: 1
                                    required:
                                      - section
                                      - count
                                closedFeedbacks:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      id:
                                        type: string
                                      number:
                                        type:
                                          - integer
                                          - 'null'
                                      title:
                                        type: string
                                    required:
                                      - id
                                      - number
                                      - title
                                checks:
                                  type:
                                    - object
                                    - 'null'
                                  properties:
                                    status:
                                      type: string
                                      enum:
                                        - pass
                                        - fail
                                        - pending
                                    unit:
                                      type:
                                        - object
                                        - 'null'
                                      properties:
                                        pass:
                                          type: integer
                                          minimum: 0
                                        fail:
                                          type: integer
                                          minimum: 0
                                        error:
                                          type: integer
                                          minimum: 0
                                        running:
                                          type: integer
                                          minimum: 0
                                        stale:
                                          type: integer
                                          minimum: 0
                                      required:
                                        - pass
                                        - fail
                                        - error
                                        - running
                                        - stale
                                    sim:
                                      type:
                                        - object
                                        - 'null'
                                      properties:
                                        passed:
                                          type: integer
                                          minimum: 0
                                        failed:
                                          type: integer
                                          minimum: 0
                                        running:
                                          type: integer
                                          minimum: 0
                                      required:
                                        - passed
                                        - failed
                                        - running
                                  required:
                                    - status
                              required:
                                - id
                                - versionNumber
                                - parentVersionId
                                - branchId
                                - isPublished
                                - createdBy
                                - createdAt
                                - configDiffSummary
                          branches:
                            type: array
                            items:
                              type: object
                              properties:
                                id:
                                  type: string
                                  format: uuid
                                name:
                                  type: string
                                status:
                                  type: string
                                  enum:
                                    - open
                                    - merged
                                    - discarded
                                entityType:
                                  type: string
                                entityId:
                                  type: string
                                agentName:
                                  type:
                                    - string
                                    - 'null'
                                baseVersionId:
                                  type: string
                                  format: uuid
                                baseVersionNumber:
                                  type:
                                    - number
                                    - 'null'
                                headVersionId:
                                  type:
                                    - string
                                    - 'null'
                                  format: uuid
                                headVersionNumber:
                                  type:
                                    - number
                                    - 'null'
                                mergedVersionId:
                                  type:
                                    - string
                                    - 'null'
                                  format: uuid
                                mergedVersionNumber:
                                  type:
                                    - number
                                    - 'null'
                                mergedVersionPublished:
                                  type:
                                    - boolean
                                    - 'null'
                                commitCount:
                                  type: number
                                closesCount:
                                  type: number
                                createdBy:
                                  type:
                                    - string
                                    - 'null'
                                  format: uuid
                                createdAt:
                                  type: string
                                updatedAt:
                                  type: string
                              required:
                                - id
                                - name
                                - status
                                - entityType
                                - entityId
                                - baseVersionId
                                - commitCount
                                - closesCount
                                - createdAt
                                - updatedAt
                        required:
                          - nodes
                          - branches
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
          description: Entity not found
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