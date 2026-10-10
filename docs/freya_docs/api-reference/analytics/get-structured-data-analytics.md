> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get structured data analytics

> Returns analytics for structured data fields including time series, summaries, distributions, and value counts.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json get /analytics/structured-data
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
  /analytics/structured-data:
    get:
      tags:
        - Analytics
      summary: Get structured data analytics
      description: >-
        Returns analytics for structured data fields including time series,
        summaries, distributions, and value counts.
      operationId: getStructuredDataAnalytics
      parameters:
        - schema:
            type: string
            format: uuid
          required: true
          name: workspaceId
          in: query
        - schema:
            type: string
          required: false
          name: startDate
          in: query
        - schema:
            type: string
          required: false
          name: endDate
          in: query
        - schema:
            type: string
            enum:
              - hour
              - day
              - month
            default: day
          required: false
          name: granularity
          in: query
        - schema:
            type: array
            items:
              type: string
              format: uuid
          required: false
          name: agentIds
          in: query
        - schema:
            type: array
            items:
              type: integer
              exclusiveMinimum: 0
          required: false
          name: structuredDataIds
          in: query
        - schema:
            type: array
            items:
              type: string
              format: uuid
          required: false
          name: assistantIds
          in: query
        - schema:
            type: array
            items:
              type: string
              enum:
                - inbound
                - outbound
                - web
                - inboundPhoneCall
                - outboundPhoneCall
                - webCall
          required: false
          name: callTypes
          in: query
        - schema:
            type: string
            format: uuid
          required: false
          name: phoneNumberId
          in: query
      responses:
        '200':
          description: Structured data analytics
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
                          workspaceId:
                            type: string
                          timeRange:
                            type: object
                            properties:
                              start:
                                type: string
                              end:
                                type: string
                            required:
                              - start
                              - end
                          granularity:
                            type: string
                            enum:
                              - hour
                              - day
                              - month
                          fields:
                            type: array
                            items:
                              type: object
                              properties:
                                id:
                                  type: number
                                name:
                                  type: string
                                type:
                                  type: string
                                agentId:
                                  type: string
                                  format: uuid
                                agentName:
                                  type:
                                    - string
                                    - 'null'
                              required:
                                - id
                                - name
                                - type
                                - agentId
                                - agentName
                          data:
                            type: array
                            items:
                              type: object
                              properties:
                                structuredDataId:
                                  type: number
                                timeSeries:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      date:
                                        type: string
                                      count:
                                        type: number
                                      avg:
                                        type:
                                          - number
                                          - 'null'
                                      sum:
                                        type:
                                          - number
                                          - 'null'
                                      min:
                                        type:
                                          - number
                                          - 'null'
                                      max:
                                        type:
                                          - number
                                          - 'null'
                                      trueCount:
                                        type: number
                                      falseCount:
                                        type: number
                                    required:
                                      - date
                                      - count
                                summary:
                                  type: object
                                  properties:
                                    count:
                                      type: number
                                    avg:
                                      type:
                                        - number
                                        - 'null'
                                    sum:
                                      type:
                                        - number
                                        - 'null'
                                    min:
                                      type:
                                        - number
                                        - 'null'
                                    max:
                                      type:
                                        - number
                                        - 'null'
                                    trueCount:
                                      type: number
                                    falseCount:
                                      type: number
                                    trueRate:
                                      type: number
                                  required:
                                    - count
                                distribution:
                                  type: object
                                  additionalProperties:
                                    type: number
                                valueCounts:
                                  type: object
                                  additionalProperties:
                                    type: number
                              required:
                                - structuredDataId
                                - timeSeries
                                - summary
                          generatedAt:
                            type: string
                        required:
                          - workspaceId
                          - timeRange
                          - granularity
                          - fields
                          - data
                          - generatedAt
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