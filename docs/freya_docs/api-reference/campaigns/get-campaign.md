> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get campaign

> Returns campaign configuration, customers, events, and call IDs.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json get /campaign/{campaignId}
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
  /campaign/{campaignId}:
    get:
      tags:
        - Campaigns
      summary: Get campaign
      description: Returns campaign configuration, customers, events, and call IDs.
      operationId: getCampaign
      parameters:
        - schema:
            type: string
            format: uuid
            description: Campaign ID
          required: true
          description: Campaign ID
          name: campaignId
          in: path
        - schema:
            type: string
            format: uuid
            description: Workspace ID
          required: true
          description: Workspace ID
          name: workspaceId
          in: query
      responses:
        '200':
          description: Campaign details
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
                        $ref: '#/components/schemas/CampaignDetailsResponse'
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
          description: Campaign not found
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
    CampaignDetailsResponse:
      type: object
      properties:
        campaign:
          $ref: '#/components/schemas/Campaign'
      required:
        - campaign
    Campaign:
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
        customers:
          type: array
          items:
            $ref: '#/components/schemas/CampaignCustomer'
          default: []
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
      required:
        - id
        - name
        - workspaceId
        - createdAt
        - updatedAt
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
    CampaignCustomer:
      type: object
      properties:
        phoneNumber:
          type: string
          minLength: 1
        properties:
          type:
            - object
            - 'null'
          additionalProperties: {}
          description: Custom properties to pass to the agent
      required:
        - phoneNumber
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