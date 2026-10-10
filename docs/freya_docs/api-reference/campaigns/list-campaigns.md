> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# List campaigns

> Returns campaigns for a workspace with filters, sorting, pagination, and export support.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json get /campaign
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
  /campaign:
    get:
      tags:
        - Campaigns
      summary: List campaigns
      description: >-
        Returns campaigns for a workspace with filters, sorting, pagination, and
        export support.
      operationId: listCampaigns
      parameters:
        - schema:
            type: string
            format: uuid
            description: Workspace identifier
          required: true
          description: Workspace identifier
          name: workspaceId
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
          description: Campaigns with pagination and status counts
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
                        $ref: '#/components/schemas/CampaignListResponse'
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
  schemas:
    CampaignListResponse:
      type: object
      properties:
        campaigns:
          type: array
          items:
            $ref: '#/components/schemas/CampaignListItem'
        pagination:
          $ref: '#/components/schemas/Pagination'
        statusCounts:
          $ref: '#/components/schemas/CampaignStatusCounts'
      required:
        - campaigns
        - pagination
    CampaignListItem:
      type: object
      properties:
        id:
          type: string
        assistantId:
          type:
            - string
            - 'null'
          format: uuid
        phoneNumberId:
          type:
            - string
            - 'null'
        name:
          type: string
        description:
          type:
            - string
            - 'null'
        status:
          type: string
          enum:
            - draft
            - scheduled
            - active
            - completed
            - partially_completed
          default: draft
        startDate:
          type:
            - string
            - 'null'
          format: date
          description: When campaign starts (YYYY-MM-DD)
        startTime:
          type:
            - string
            - 'null'
          pattern: ^\d{2}:\d{2}(:\d{2})?$
          description: Time on start date + retry window start (HH:MM)
        timezone:
          type: string
          default: UTC
          description: IANA timezone for all times
        endTime:
          type:
            - string
            - 'null'
          pattern: ^\d{2}:\d{2}(:\d{2})?$
          description: Daily retry window end (HH:MM)
        activeDays:
          type: array
          items:
            type: integer
            minimum: 0
            maximum: 6
          default:
            - 0
            - 1
            - 2
            - 3
            - 4
            - 5
            - 6
          description: Days retries can happen (0=Monday, 6=Sunday)
        daySchedules:
          type:
            - object
            - 'null'
          additionalProperties:
            type: object
            properties:
              startTime:
                type: string
                pattern: ^\d{2}:\d{2}(:\d{2})?$
              endTime:
                type: string
                pattern: ^\d{2}:\d{2}(:\d{2})?$
            required:
              - startTime
              - endTime
          description: >-
            Sparse per-day schedule overrides. Keys are day indices (0=Monday).
            Overrides global startTime/endTime for specific days.
        phoneNumber:
          type:
            - string
            - 'null'
        callRetries:
          type: integer
          minimum: 0
          maximum: 10
          default: 0
        retryDelaySeconds:
          type: integer
          minimum: 0
          maximum: 86400
          default: 300
          description: Delay between retries in seconds
        retryDelayMode:
          type: string
          enum:
            - fixed
            - next_day
          default: fixed
        retryConditions:
          $ref: '#/components/schemas/RetryConditions'
        endDate:
          type:
            - string
            - 'null'
          format: date
          description: '@deprecated - No longer used'
        schedulingMode:
          type: string
          enum:
            - even
            - fixed
          default: even
          description: '@deprecated - No longer used'
        callIntervalSeconds:
          type: integer
          minimum: 1
          maximum: 86400
          default: 30
          description: '@deprecated - No longer used'
        maxConcurrency:
          type: integer
          minimum: 1
          maximum: 50
          default: 5
          description: Internal parameter (hardcoded to 5)
        webhookUrl:
          type:
            - string
            - 'null'
        callIds:
          type: array
          items:
            type: string
          default: []
        roomNames:
          type: array
          items:
            type: string
          default: []
        events:
          type: array
          items:
            $ref: '#/components/schemas/CampaignEvent'
          default: []
        version:
          type: string
          enum:
            - v1
            - v2
          default: v1
        workspaceId:
          type: string
        createdAt:
          type: string
        updatedAt:
          type: string
        customerCount:
          type: number
        callCount:
          type: number
        dialedNumbersPreview:
          type: array
          items:
            type: string
          default: []
          description: >-
            First few dialed customer numbers (PII — empty unless the caller
            holds calls:pii; full list via the customers endpoint)
      required:
        - id
        - name
        - workspaceId
        - createdAt
        - updatedAt
    Pagination:
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
    CampaignStatusCounts:
      type: object
      properties:
        all:
          type: number
        active:
          type: number
        scheduled:
          type: number
        completed:
          type: number
        partiallyCompleted:
          type: number
        draft:
          type: number
      required:
        - all
        - active
        - scheduled
        - completed
        - partiallyCompleted
        - draft
    RetryConditions:
      type: array
      items:
        type: string
        enum:
          - Rejected
          - Unreachable
          - Busy
          - No Answer
          - Network Error
          - Invalid
          - Timeout
          - Cancelled
          - Resource Unavailable
          - Service Unavailable
          - Protocol Error
          - Unspecified
          - voicemail
          - exceeded-max-duration
          - inactivity-ended-call
          - rescheduled
      default:
        - No Answer
        - Busy
        - Timeout
        - Unreachable
        - Network Error
        - Resource Unavailable
        - Service Unavailable
        - voicemail
      description: >-
        Array of call outcome values to retry on (SipCodeCategory + special
        endedReason values)
    CampaignEvent:
      type: object
      properties:
        event:
          type: string
        timestamp:
          type: string
          format: date-time
        metadata:
          type: object
          additionalProperties: {}
        message:
          type: string
        data: {}
      required:
        - event
        - timestamp
        - metadata
        - message
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer

````

This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.