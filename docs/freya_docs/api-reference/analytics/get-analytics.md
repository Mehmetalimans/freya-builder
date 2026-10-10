> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get analytics

> Returns call analytics for a workspace including summary statistics, time series data, ended reasons, top locations, sentiment distribution, and more.

**Available Metrics:**
- `summary`: Total calls, answered calls, voicemail, durations, answer rate
- `timeSeries`: Call volume over time with configurable granularity
- `endedReasons`: Distribution of call end reasons
- `topCalls`: Longest or most recent calls
- `geoDistribution`: Geographic distribution by country and state
- `callThemes`: Common topics from call analysis
- `sentimentDistribution`: Customer sentiment breakdown



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json get /analytics
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
  /analytics:
    get:
      tags:
        - Analytics
      summary: Get analytics
      description: >-
        Returns call analytics for a workspace including summary statistics,
        time series data, ended reasons, top locations, sentiment distribution,
        and more.


        **Available Metrics:**

        - `summary`: Total calls, answered calls, voicemail, durations, answer
        rate

        - `timeSeries`: Call volume over time with configurable granularity

        - `endedReasons`: Distribution of call end reasons

        - `topCalls`: Longest or most recent calls

        - `geoDistribution`: Geographic distribution by country and state

        - `callThemes`: Common topics from call analysis

        - `sentimentDistribution`: Customer sentiment breakdown
      operationId: getAnalytics
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
            description: Start date for analytics period (ISO format)
          required: false
          description: Start date for analytics period (ISO format)
          name: startDate
          in: query
        - schema:
            type: string
            description: End date for analytics period (ISO format)
          required: false
          description: End date for analytics period (ISO format)
          name: endDate
          in: query
        - schema:
            type: string
            format: uuid
            description: Filter by phone number ID
          required: false
          description: Filter by phone number ID
          name: phoneNumberId
          in: query
        - schema:
            type: string
            format: uuid
            description: Filter by assistant/agent ID
          required: false
          description: Filter by assistant/agent ID
          name: assistantId
          in: query
        - schema:
            type: array
            items:
              type: string
              format: uuid
            description: Filter by multiple assistant IDs
          required: false
          description: Filter by multiple assistant IDs
          name: assistantIds
          in: query
        - schema:
            type: string
            enum:
              - hour
              - day
              - month
            description: 'Time series granularity: hour, day, or month'
          required: false
          description: 'Time series granularity: hour, day, or month'
          name: granularity
          in: query
        - schema:
            type: array
            items:
              type: string
              enum:
                - summary
                - timeSeries
                - endedReasons
                - topCalls
                - geoDistribution
                - callThemes
                - sentimentDistribution
            description: Specific metrics to return (JSON array)
          required: false
          description: Specific metrics to return (JSON array)
          name: metrics
          in: query
        - schema:
            type: string
            minLength: 2
            maxLength: 64
            description: IANA timezone for date calculations
          required: false
          description: IANA timezone for date calculations
          name: timezone
          in: query
        - schema:
            type: array
            items:
              type: string
              minLength: 1
            description: Filter by call status (JSON array)
          required: false
          description: Filter by call status (JSON array)
          name: status
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
            description: 'Filter by call type: inbound, outbound, web (JSON array)'
          required: false
          description: 'Filter by call type: inbound, outbound, web (JSON array)'
          name: callType
          in: query
      responses:
        '200':
          description: Analytics data
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
                          summary:
                            type: object
                            properties:
                              totalCalls:
                                type: number
                              answeredCalls:
                                type: number
                              voicemailCalls:
                                type: number
                              totalDurationSec:
                                type: number
                              averageDurationSec:
                                type: number
                              answerRate:
                                type: number
                            required:
                              - totalCalls
                              - answeredCalls
                              - voicemailCalls
                              - totalDurationSec
                              - averageDurationSec
                              - answerRate
                          timeSeries:
                            type: array
                            items:
                              type: object
                              properties:
                                date:
                                  type: string
                                totalCalls:
                                  type: number
                                answeredCalls:
                                  type: number
                                averageDurationSec:
                                  type: number
                                sentimentCounts:
                                  type: object
                                  properties:
                                    very-unhappy:
                                      type: number
                                    unhappy:
                                      type: number
                                    neutral:
                                      type: number
                                    happy:
                                      type: number
                                    very-happy:
                                      type: number
                                  required:
                                    - very-unhappy
                                    - unhappy
                                    - neutral
                                    - happy
                                    - very-happy
                              required:
                                - date
                                - totalCalls
                                - answeredCalls
                                - averageDurationSec
                          endedReasons:
                            type: array
                            items:
                              type: object
                              properties:
                                reason:
                                  type: string
                                count:
                                  type: number
                              required:
                                - reason
                                - count
                          topCalls:
                            type: array
                            items:
                              type: object
                              properties:
                                callId:
                                  type: string
                                customerNumber:
                                  type:
                                    - string
                                    - 'null'
                                durationSec:
                                  type: number
                                startedAt:
                                  type: string
                                status:
                                  type:
                                    - string
                                    - 'null'
                                endedReason:
                                  type:
                                    - string
                                    - 'null'
                              required:
                                - callId
                                - customerNumber
                                - durationSec
                                - startedAt
                                - status
                                - endedReason
                          geoDistribution:
                            type: object
                            properties:
                              countries:
                                type: array
                                items:
                                  type: object
                                  properties:
                                    countryCode:
                                      type: string
                                    countryName:
                                      type: string
                                    callCount:
                                      type: number
                                  required:
                                    - countryCode
                                    - countryName
                                    - callCount
                              states:
                                type: array
                                items:
                                  type: object
                                  properties:
                                    countryCode:
                                      type: string
                                    countryName:
                                      type: string
                                    stateCode:
                                      type: string
                                    stateName:
                                      type: string
                                    callCount:
                                      type: number
                                  required:
                                    - countryCode
                                    - countryName
                                    - stateCode
                                    - stateName
                                    - callCount
                            required:
                              - countries
                              - states
                          callThemes:
                            type: array
                            items:
                              type: object
                              properties:
                                theme:
                                  type: string
                                count:
                                  type: number
                              required:
                                - theme
                                - count
                          sentimentDistribution:
                            type: array
                            items:
                              type: object
                              properties:
                                bucket:
                                  type: string
                                  enum:
                                    - very-unhappy
                                    - unhappy
                                    - neutral
                                    - happy
                                    - very-happy
                                count:
                                  type: number
                              required:
                                - bucket
                                - count
                          generatedAt:
                            type: string
                        required:
                          - workspaceId
                          - timeRange
                          - granularity
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