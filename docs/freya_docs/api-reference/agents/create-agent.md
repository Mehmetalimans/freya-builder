> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Create agent

> Creates a new AI agent with the specified configuration.



## OpenAPI

````yaml https://staging-app.freyavoice.ai/api/openapi.json post /agents
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
  /agents:
    post:
      tags:
        - Agents
      summary: Create agent
      description: Creates a new AI agent with the specified configuration.
      operationId: createAgent
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  minLength: 1
                  maxLength: 100
                language:
                  type: string
                  maxLength: 10
                config:
                  type: object
                  properties:
                    llmConfig:
                      type: object
                      properties:
                        provider:
                          type: string
                          minLength: 1
                          maxLength: 50
                        model:
                          type: string
                          minLength: 1
                          maxLength: 100
                        baseUrl:
                          type:
                            - string
                            - 'null'
                          maxLength: 2048
                        apiKey:
                          type:
                            - string
                            - 'null'
                          maxLength: 500
                        systemPrompt:
                          type: string
                          minLength: 1
                          maxLength: 200000
                        firstMessage:
                          type:
                            - string
                            - 'null'
                          maxLength: 2000
                          default: null
                        firstMessageMode:
                          type:
                            - string
                            - 'null'
                          enum:
                            - >-
                              assistant-speaks-first-with-model-generated-message
                            - assistant-speaks-first
                            - assistant-waits-for-user
                            - null
                          default: assistant-waits-for-user
                        disableInterruptionsDuringFirstMessage:
                          type: boolean
                          default: false
                        maxTokens:
                          type: integer
                          minimum: 1
                          maximum: 4000
                          default: 1000
                        maxContextWindow:
                          type:
                            - integer
                            - 'null'
                          minimum: 1024
                          maximum: 10000000
                        temperature:
                          type: number
                          minimum: 0
                          maximum: 2
                          default: 0.7
                        tools:
                          type: array
                          items:
                            type: object
                            properties:
                              type:
                                type: string
                                enum:
                                  - function
                              function:
                                type: object
                                properties:
                                  name:
                                    type: string
                                  handler:
                                    type: string
                                  description:
                                    type: string
                                  parameters:
                                    type: object
                                    properties:
                                      type:
                                        type: string
                                      properties:
                                        type: object
                                        additionalProperties: {}
                                      required:
                                        type: array
                                        items:
                                          type: string
                                      items: {}
                                    required:
                                      - type
                                    additionalProperties: {}
                                  transition_to:
                                    type: string
                                required:
                                  - name
                                  - handler
                                  - description
                                  - parameters
                              config:
                                type: object
                                properties:
                                  maxPerNTurns:
                                    type: integer
                                    exclusiveMinimum: 0
                                  alwaysRunsAt:
                                    type: array
                                    items:
                                      type: string
                                      enum:
                                        - each_turn
                                        - start_of_call
                                        - end_of_call
                                  timeoutMs:
                                    type: integer
                                    exclusiveMinimum: 0
                                  maxRetries:
                                    type: integer
                                    minimum: 0
                                    maximum: 5
                                  preSpeech:
                                    type: object
                                    properties:
                                      mode:
                                        type: string
                                        enum:
                                          - static
                                          - auto
                                      message:
                                        type: string
                                      interruptible:
                                        type: boolean
                                      audio_asset_id:
                                        type: string
                                      audio_loop:
                                        type: boolean
                                      audio_volume:
                                        type: number
                                    required:
                                      - mode
                                  interruptible:
                                    type: boolean
                              response_mapping:
                                type: array
                                items:
                                  type: object
                                  properties:
                                    path:
                                      type: string
                                    variable:
                                      type: string
                                    description:
                                      type: string
                                      default: ''
                                  required:
                                    - path
                                    - variable
                              extraction_schema:
                                type: array
                                items:
                                  type: object
                                  properties:
                                    name:
                                      type: string
                                    type:
                                      type: string
                                      enum:
                                        - string
                                        - integer
                                        - float
                                        - boolean
                                        - date
                                        - datetime
                                        - enum
                                    description:
                                      type: string
                                    extraction_prompt:
                                      type: string
                                    validation_pattern:
                                      type: string
                                    max_retries:
                                      type: integer
                                      minimum: 0
                                    required:
                                      type: boolean
                                    overridable:
                                      type: boolean
                                  required:
                                    - name
                                    - type
                              pre_process_code:
                                type:
                                  - string
                                  - 'null'
                              post_process_code:
                                type:
                                  - string
                                  - 'null'
                            required:
                              - type
                              - function
                          default: []
                        additionalSettings:
                          type:
                            - object
                            - 'null'
                          additionalProperties: {}
                          default: {}
                        retryExhaustionMessage:
                          type:
                            - string
                            - 'null'
                          maxLength: 2000
                        farewellMessage:
                          type:
                            - string
                            - 'null'
                          maxLength: 2000
                      required:
                        - provider
                        - model
                        - systemPrompt
                    ttsConfig:
                      type: object
                      properties:
                        provider:
                          type: string
                          minLength: 1
                          maxLength: 50
                        model:
                          type:
                            - string
                            - 'null'
                          maxLength: 100
                          default: null
                        voiceId:
                          type: string
                          minLength: 1
                          maxLength: 100
                        language:
                          type:
                            - string
                            - 'null'
                          minLength: 1
                          default: multi
                        baseUrl:
                          type:
                            - string
                            - 'null'
                          maxLength: 2048
                        apiKey:
                          type:
                            - string
                            - 'null'
                          maxLength: 500
                        additionalSettings:
                          type:
                            - object
                            - 'null'
                          additionalProperties: {}
                          default: {}
                        startSpeakingPlan:
                          type:
                            - object
                            - 'null'
                          properties:
                            waitSeconds:
                              type: number
                              minimum: 0
                              maximum: 5
                              default: 0.4
                            backgroundNoisePhrases:
                              type:
                                - array
                                - 'null'
                              items:
                                type: string
                                minLength: 1
                                maxLength: 100
                              maxItems: 200
                        stopSpeakingPlan:
                          type:
                            - object
                            - 'null'
                          properties:
                            numberOfWords:
                              type: integer
                              minimum: 0
                              maximum: 10
                              default: 1
                            voiceSeconds:
                              type: number
                              minimum: 0
                              maximum: 0.5
                              default: 0.4
                            backOffSeconds:
                              type: number
                              minimum: 0
                              maximum: 3
                              default: 0.4
                            acknowledgementPhrases:
                              type:
                                - array
                                - 'null'
                              items:
                                type: string
                                minLength: 1
                                maxLength: 100
                              maxItems: 200
                            interruptionPhrases:
                              type:
                                - array
                                - 'null'
                              items:
                                type: string
                                minLength: 1
                                maxLength: 100
                              maxItems: 200
                        textSubstitutions:
                          type:
                            - array
                            - 'null'
                          items:
                            type: object
                            properties:
                              pattern:
                                type: string
                                minLength: 1
                                maxLength: 500
                              replacement:
                                type: string
                                maxLength: 500
                              caseInsensitive:
                                type: boolean
                            required:
                              - pattern
                              - replacement
                        speechNormalization:
                          type:
                            - object
                            - 'null'
                          properties:
                            emails:
                              type: boolean
                              default: true
                            urls:
                              type: boolean
                              default: true
                            emojis:
                              type: boolean
                              default: true
                            phoneNumbers:
                              type: boolean
                              default: false
                            identityNumbers:
                              type: boolean
                              default: false
                            generalNumbers:
                              type: boolean
                              default: false
                            advanced:
                              type:
                                - object
                                - 'null'
                              properties:
                                numbers:
                                  type: boolean
                                  default: false
                                money:
                                  type: boolean
                                  default: false
                                dates:
                                  type: boolean
                                  default: false
                                times:
                                  type: boolean
                                  default: false
                                percentages:
                                  type: boolean
                                  default: false
                                fractions:
                                  type: boolean
                                  default: false
                                units:
                                  type: boolean
                                  default: false
                                ordinals:
                                  type: boolean
                                  default: false
                                abbreviations:
                                  type: boolean
                                  default: false
                                iban:
                                  type: boolean
                                  default: false
                                symbols:
                                  type: boolean
                                  default: false
                        normalizationPrompt:
                          type:
                            - string
                            - 'null'
                          maxLength: 8000
                      required:
                        - provider
                        - voiceId
                    sttConfig:
                      type: object
                      properties:
                        provider:
                          type: string
                          minLength: 1
                          maxLength: 50
                        model:
                          type:
                            - string
                            - 'null'
                          maxLength: 100
                          default: null
                        language:
                          type:
                            - string
                            - 'null'
                          minLength: 1
                          default: multi
                        baseUrl:
                          type:
                            - string
                            - 'null'
                          maxLength: 2048
                        apiKey:
                          type:
                            - string
                            - 'null'
                          maxLength: 500
                        additionalSettings:
                          type:
                            - object
                            - 'null'
                          additionalProperties: {}
                          default: {}
                        confidenceReask:
                          type:
                            - object
                            - 'null'
                          properties:
                            enabled:
                              type: boolean
                              default: false
                            threshold:
                              type: number
                              minimum: 0
                              maximum: 1
                              default: 0.3
                            reduction:
                              type: string
                              enum:
                                - min
                              default: min
                            disableOnDigitNodes:
                              type: boolean
                              default: true
                            reaskMode:
                              type: string
                              enum:
                                - phrase
                                - llm
                              default: phrase
                            reaskPhrases:
                              type:
                                - array
                                - 'null'
                              items:
                                type: string
                                maxLength: 2000
                              maxItems: 20
                              default: null
                            maxConsecutiveReasks:
                              type: integer
                              minimum: 0
                              maximum: 5
                              default: 2
                      required:
                        - provider
                    complianceConfig:
                      type: object
                      properties:
                        pciDss:
                          type: boolean
                          default: false
                        mifidIi:
                          type: boolean
                          default: false
                        euAiAct:
                          type: boolean
                          default: false
                        soc2:
                          type: boolean
                          default: false
                    callTimeoutSettings:
                      type:
                        - object
                        - 'null'
                      properties:
                        silenceTimeout:
                          type: integer
                          minimum: 0
                          default: 0
                        maximumDuration:
                          type: integer
                          minimum: 0
                          maximum: 3600
                          default: 600
                        checkInMessage:
                          type:
                            - string
                            - 'null'
                          maxLength: 2000
                          default: null
                        closureMessage:
                          type:
                            - string
                            - 'null'
                          maxLength: 2000
                          default: null
                        maxRetries:
                          type: integer
                          minimum: 0
                          maximum: 10
                          default: 2
                        silenceTimeoutPrompt:
                          type:
                            - string
                            - 'null'
                          maxLength: 2000
                          default: null
                        maxDurationEndCall:
                          type:
                            - object
                            - 'null'
                          properties:
                            messageMode:
                              type: string
                              enum:
                                - llm
                                - custom
                                - none
                              default: llm
                            spokenMessage:
                              type:
                                - string
                                - 'null'
                              maxLength: 2000
                              default: null
                            llmPrompt:
                              type:
                                - string
                                - 'null'
                              maxLength: 2000
                              default: null
                            interruptible:
                              type: boolean
                              default: false
                            triggerTimeout:
                              type:
                                - number
                                - 'null'
                              minimum: 0
                              default: null
                          default: null
                        dynamicWait:
                          type:
                            - object
                            - 'null'
                          properties:
                            enabled:
                              type: boolean
                              default: false
                            maxWaitSeconds:
                              type: integer
                              minimum: 10
                              maximum: 3600
                              default: 300
                            maxRetries:
                              type: integer
                              minimum: 0
                              maximum: 10
                              default: 1
                            checkInMessage:
                              type:
                                - string
                                - 'null'
                              maxLength: 2000
                              default: null
                            checkInPrompt:
                              type:
                                - string
                                - 'null'
                              maxLength: 2000
                              default: null
                            vadConfidence:
                              type:
                                - number
                                - 'null'
                              minimum: 0
                              maximum: 1
                              default: null
                            vadMinVolume:
                              type:
                                - number
                                - 'null'
                              minimum: 0
                              maximum: 1
                              default: null
                            vadStartSecs:
                              type:
                                - number
                                - 'null'
                              minimum: 0
                              maximum: 5
                              default: null
                            vadStopSecs:
                              type:
                                - number
                                - 'null'
                              minimum: 0
                              maximum: 10
                              default: null
                          default: null
                    voicemailDetection:
                      type:
                        - object
                        - 'null'
                      properties:
                        enabled:
                          type: boolean
                          default: false
                        messageMode:
                          type: string
                          enum:
                            - llm
                            - custom
                            - none
                          default: none
                        staticMessage:
                          type:
                            - string
                            - 'null'
                          maxLength: 2000
                          default: null
                        voicemailResponseDelay:
                          type: number
                          minimum: 0
                          maximum: 30
                          default: 2
                    dtmfConfig:
                      type:
                        - object
                        - 'null'
                      properties:
                        enabled:
                          type: boolean
                          default: false
                        timeout:
                          type: number
                          minimum: 0
                          maximum: 30
                          default: 2
                        terminationDigit:
                          type: string
                          enum:
                            - '0'
                            - '1'
                            - '2'
                            - '3'
                            - '4'
                            - '5'
                            - '6'
                            - '7'
                            - '8'
                            - '9'
                            - '#'
                            - '*'
                          default: '#'
                        prefix:
                          type: string
                          maxLength: 100
                          default: 'DTMF: '
                    postConversationAnalysis:
                      type:
                        - object
                        - 'null'
                      properties:
                        summaryPrompt:
                          type:
                            - string
                            - 'null'
                          maxLength: 10000
                          default: null
                        autoDetectProblems:
                          type: boolean
                          default: false
                        problemDetectionPrompt:
                          type:
                            - string
                            - 'null'
                          maxLength: 10000
                          default: null
                        problemDetectionInstructions:
                          type:
                            - string
                            - 'null'
                          maxLength: 10000
                          default: null
                        analysisModel:
                          type:
                            - string
                            - 'null'
                          maxLength: 100
                          default: null
                    privacyConfig:
                      type:
                        - object
                        - 'null'
                      properties:
                        enableRecording:
                          type: boolean
                          default: false
                        getRecordingConsent:
                          type: boolean
                          default: false
                        recordingConsentText:
                          type:
                            - string
                            - 'null'
                          maxLength: 500
                          default: null
                        stopSecs:
                          type: number
                          minimum: 0
                        preSpeechMs:
                          type: number
                          minimum: 0
                        maxDurationSecs:
                          type: number
                          minimum: 0
                    turnAnalyzerConfig:
                      type: object
                      properties:
                        provider:
                          type: string
                          enum:
                            - local
                            - fal
                        url:
                          type:
                            - string
                            - 'null'
                          format: uri
                        modelPath:
                          type:
                            - string
                            - 'null'
                    guardrailsConfig:
                      type:
                        - object
                        - 'null'
                      properties:
                        guardrails_enabled:
                          type: boolean
                          default: false
                        custom_rules_enabled:
                          type: boolean
                          default: false
                        rules:
                          type: array
                          items:
                            type: object
                            properties:
                              id:
                                type:
                                  - string
                                  - 'null'
                              type:
                                type: string
                                enum:
                                  - exact
                                  - regex
                                  - dictionary
                                  - structured
                                  - classifier
                              pattern:
                                type: string
                              action:
                                type: string
                                enum:
                                  - refuse
                                  - regenerate
                                  - log_only
                              enabled:
                                type: boolean
                                default: true
                              description:
                                type:
                                  - string
                                  - 'null'
                              case_sensitive:
                                type: boolean
                                default: false
                              classifier_threshold:
                                type: number
                                minimum: 0
                                maximum: 1
                          default: []
                        refuse_message:
                          type: string
                          default: I'm sorry, I can't help with that.
                        max_regenerate_retries:
                          type: integer
                          minimum: 0
                          maximum: 5
                          default: 2
                        regenerate_wait_message:
                          type: string
                          default: One moment, please.
                        classifier_enabled:
                          type: boolean
                          default: false
                        classifier_provider:
                          type: string
                        classifier_model:
                          type: string
                        input_config:
                          type: object
                          properties:
                            enabled:
                              type: boolean
                              default: false
                            normalize:
                              type: boolean
                              default: true
                            detect_injection:
                              type: boolean
                              default: true
                            detect_weird_input:
                              type: boolean
                              default: true
                            run_classifier:
                              type: boolean
                              default: true
                            refuse_message:
                              type: string
                              default: I'm sorry, I can't help with that.
                            max_input_chars:
                              type: integer
                              minimum: 1
                              maximum: 100000
                              default: 8000
                    piiRedactionConfig:
                      type:
                        - object
                        - 'null'
                      properties:
                        enabled:
                          type: boolean
                          default: false
                        maskEmail:
                          type: boolean
                          default: true
                        maskPhone:
                          type: boolean
                          default: true
                        maskPaymentCard:
                          type: boolean
                          default: true
                        maskNationalId:
                          type: boolean
                          default: true
                        maskIban:
                          type: boolean
                          default: true
                        customRules:
                          type: array
                          items:
                            type: object
                            properties:
                              label:
                                type: string
                                minLength: 1
                                maxLength: 40
                                pattern: ^[A-Z0-9_]+$
                              pattern:
                                type: string
                                minLength: 1
                                maxLength: 500
                              enabled:
                                type: boolean
                                default: true
                            required:
                              - label
                              - pattern
                          default: []
                    routingLlmConfig:
                      type:
                        - object
                        - 'null'
                      properties:
                        provider:
                          type: string
                          minLength: 1
                          maxLength: 50
                        model:
                          type: string
                          minLength: 1
                          maxLength: 100
                        baseUrl:
                          type:
                            - string
                            - 'null'
                          maxLength: 2048
                        apiKey:
                          type:
                            - string
                            - 'null'
                          maxLength: 500
                      required:
                        - provider
                        - model
                    extractionLlmConfig:
                      type:
                        - object
                        - 'null'
                      properties:
                        provider:
                          type: string
                          minLength: 1
                          maxLength: 50
                        model:
                          type: string
                          minLength: 1
                          maxLength: 100
                        baseUrl:
                          type:
                            - string
                            - 'null'
                          maxLength: 2048
                        apiKey:
                          type:
                            - string
                            - 'null'
                          maxLength: 500
                      required:
                        - provider
                        - model
                    backgroundSoundUrl:
                      type:
                        - string
                        - 'null'
                      maxLength: 200
                      default: null
                    syncSource:
                      type:
                        - object
                        - 'null'
                      properties:
                        url:
                          type: string
                          maxLength: 2048
                          format: uri
                        apiKey:
                          type: string
                          maxLength: 500
                        syncedAt:
                          type:
                            - string
                            - 'null'
                          format: date-time
                      required:
                        - url
                        - apiKey
                    testVariables:
                      type: object
                      additionalProperties:
                        type: string
                  required:
                    - llmConfig
                    - ttsConfig
                    - sttConfig
                    - complianceConfig
              required:
                - name
            example:
              workspaceId: 550e8400-e29b-41d4-a716-446655440000
              name: Customer Support Agent
              config:
                llmConfig:
                  provider: openai
                  model: gpt-4o
                  systemPrompt: You are a helpful customer support agent...
                  firstMessage: Hello! How can I help you today?
                  firstMessageMode: assistant-speaks-first
                  maxTokens: 1000
                  temperature: 0.7
                ttsConfig:
                  provider: elevenlabs
                  model: eleven_multilingual_v2
                  voiceId: 21m00Tcm4TlvDq8ikWAM
                  language: en
                  speed: 1
                  stability: 0.5
                  similarityBoost: 0.75
                  additionalSettings: {}
                sttConfig:
                  provider: deepgram
                  model: nova-2
                  language: en
                  temperature: null
                  punctuate: true
                  diarize: false
                  additionalSettings: {}
                complianceConfig:
                  pciDss: false
                  mifidIi: false
                  euAiAct: false
                  soc2: false
      responses:
        '201':
          description: Agent created
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
                          agent:
                            type: object
                            properties:
                              id:
                                type: string
                                format: uuid
                              workspaceId:
                                type: string
                                format: uuid
                              userId:
                                type:
                                  - string
                                  - 'null'
                                format: uuid
                              name:
                                type: string
                              entityType:
                                type:
                                  - string
                                  - 'null'
                                enum:
                                  - workflow
                                  - null
                              workflowId:
                                type:
                                  - string
                                  - 'null'
                                format: uuid
                              config:
                                type: object
                                properties:
                                  llmConfig:
                                    type: object
                                    properties:
                                      provider:
                                        type: string
                                        minLength: 1
                                        maxLength: 50
                                      model:
                                        type: string
                                        minLength: 1
                                        maxLength: 100
                                      baseUrl:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2048
                                      apiKey:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 500
                                      systemPrompt:
                                        type: string
                                        minLength: 1
                                        maxLength: 200000
                                      firstMessage:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2000
                                        default: null
                                      firstMessageMode:
                                        type:
                                          - string
                                          - 'null'
                                        enum:
                                          - >-
                                            assistant-speaks-first-with-model-generated-message
                                          - assistant-speaks-first
                                          - assistant-waits-for-user
                                          - null
                                        default: assistant-waits-for-user
                                      disableInterruptionsDuringFirstMessage:
                                        type: boolean
                                        default: false
                                      maxTokens:
                                        type: integer
                                        minimum: 1
                                        maximum: 4000
                                        default: 1000
                                      maxContextWindow:
                                        type:
                                          - integer
                                          - 'null'
                                        minimum: 1024
                                        maximum: 10000000
                                      temperature:
                                        type: number
                                        minimum: 0
                                        maximum: 2
                                        default: 0.7
                                      tools:
                                        type: array
                                        items:
                                          type: object
                                          properties:
                                            type:
                                              type: string
                                              enum:
                                                - function
                                            function:
                                              type: object
                                              properties:
                                                name:
                                                  type: string
                                                handler:
                                                  type: string
                                                description:
                                                  type: string
                                                parameters:
                                                  type: object
                                                  properties:
                                                    type:
                                                      type: string
                                                    properties:
                                                      type: object
                                                      additionalProperties: {}
                                                    required:
                                                      type: array
                                                      items:
                                                        type: string
                                                    items: {}
                                                  required:
                                                    - type
                                                  additionalProperties: {}
                                                transition_to:
                                                  type: string
                                              required:
                                                - name
                                                - handler
                                                - description
                                                - parameters
                                            config:
                                              type: object
                                              properties:
                                                maxPerNTurns:
                                                  type: integer
                                                  exclusiveMinimum: 0
                                                alwaysRunsAt:
                                                  type: array
                                                  items:
                                                    type: string
                                                    enum:
                                                      - each_turn
                                                      - start_of_call
                                                      - end_of_call
                                                timeoutMs:
                                                  type: integer
                                                  exclusiveMinimum: 0
                                                maxRetries:
                                                  type: integer
                                                  minimum: 0
                                                  maximum: 5
                                                preSpeech:
                                                  type: object
                                                  properties:
                                                    mode:
                                                      type: string
                                                      enum:
                                                        - static
                                                        - auto
                                                    message:
                                                      type: string
                                                    interruptible:
                                                      type: boolean
                                                    audio_asset_id:
                                                      type: string
                                                    audio_loop:
                                                      type: boolean
                                                    audio_volume:
                                                      type: number
                                                  required:
                                                    - mode
                                                interruptible:
                                                  type: boolean
                                            response_mapping:
                                              type: array
                                              items:
                                                type: object
                                                properties:
                                                  path:
                                                    type: string
                                                  variable:
                                                    type: string
                                                  description:
                                                    type: string
                                                    default: ''
                                                required:
                                                  - path
                                                  - variable
                                            extraction_schema:
                                              type: array
                                              items:
                                                type: object
                                                properties:
                                                  name:
                                                    type: string
                                                  type:
                                                    type: string
                                                    enum:
                                                      - string
                                                      - integer
                                                      - float
                                                      - boolean
                                                      - date
                                                      - datetime
                                                      - enum
                                                  description:
                                                    type: string
                                                  extraction_prompt:
                                                    type: string
                                                  validation_pattern:
                                                    type: string
                                                  max_retries:
                                                    type: integer
                                                    minimum: 0
                                                  required:
                                                    type: boolean
                                                  overridable:
                                                    type: boolean
                                                required:
                                                  - name
                                                  - type
                                            pre_process_code:
                                              type:
                                                - string
                                                - 'null'
                                            post_process_code:
                                              type:
                                                - string
                                                - 'null'
                                          required:
                                            - type
                                            - function
                                        default: []
                                      additionalSettings:
                                        type:
                                          - object
                                          - 'null'
                                        additionalProperties: {}
                                        default: {}
                                      retryExhaustionMessage:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2000
                                      farewellMessage:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2000
                                    required:
                                      - provider
                                      - model
                                      - systemPrompt
                                  ttsConfig:
                                    type: object
                                    properties:
                                      provider:
                                        type: string
                                        minLength: 1
                                        maxLength: 50
                                      model:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 100
                                        default: null
                                      voiceId:
                                        type: string
                                        minLength: 1
                                        maxLength: 100
                                      language:
                                        type:
                                          - string
                                          - 'null'
                                        minLength: 1
                                        default: multi
                                      baseUrl:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2048
                                      apiKey:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 500
                                      additionalSettings:
                                        type:
                                          - object
                                          - 'null'
                                        additionalProperties: {}
                                        default: {}
                                      startSpeakingPlan:
                                        type:
                                          - object
                                          - 'null'
                                        properties:
                                          waitSeconds:
                                            type: number
                                            minimum: 0
                                            maximum: 5
                                            default: 0.4
                                          backgroundNoisePhrases:
                                            type:
                                              - array
                                              - 'null'
                                            items:
                                              type: string
                                              minLength: 1
                                              maxLength: 100
                                            maxItems: 200
                                      stopSpeakingPlan:
                                        type:
                                          - object
                                          - 'null'
                                        properties:
                                          numberOfWords:
                                            type: integer
                                            minimum: 0
                                            maximum: 10
                                            default: 1
                                          voiceSeconds:
                                            type: number
                                            minimum: 0
                                            maximum: 0.5
                                            default: 0.4
                                          backOffSeconds:
                                            type: number
                                            minimum: 0
                                            maximum: 3
                                            default: 0.4
                                          acknowledgementPhrases:
                                            type:
                                              - array
                                              - 'null'
                                            items:
                                              type: string
                                              minLength: 1
                                              maxLength: 100
                                            maxItems: 200
                                          interruptionPhrases:
                                            type:
                                              - array
                                              - 'null'
                                            items:
                                              type: string
                                              minLength: 1
                                              maxLength: 100
                                            maxItems: 200
                                      textSubstitutions:
                                        type:
                                          - array
                                          - 'null'
                                        items:
                                          type: object
                                          properties:
                                            pattern:
                                              type: string
                                              minLength: 1
                                              maxLength: 500
                                            replacement:
                                              type: string
                                              maxLength: 500
                                            caseInsensitive:
                                              type: boolean
                                          required:
                                            - pattern
                                            - replacement
                                      speechNormalization:
                                        type:
                                          - object
                                          - 'null'
                                        properties:
                                          emails:
                                            type: boolean
                                            default: true
                                          urls:
                                            type: boolean
                                            default: true
                                          emojis:
                                            type: boolean
                                            default: true
                                          phoneNumbers:
                                            type: boolean
                                            default: false
                                          identityNumbers:
                                            type: boolean
                                            default: false
                                          generalNumbers:
                                            type: boolean
                                            default: false
                                          advanced:
                                            type:
                                              - object
                                              - 'null'
                                            properties:
                                              numbers:
                                                type: boolean
                                                default: false
                                              money:
                                                type: boolean
                                                default: false
                                              dates:
                                                type: boolean
                                                default: false
                                              times:
                                                type: boolean
                                                default: false
                                              percentages:
                                                type: boolean
                                                default: false
                                              fractions:
                                                type: boolean
                                                default: false
                                              units:
                                                type: boolean
                                                default: false
                                              ordinals:
                                                type: boolean
                                                default: false
                                              abbreviations:
                                                type: boolean
                                                default: false
                                              iban:
                                                type: boolean
                                                default: false
                                              symbols:
                                                type: boolean
                                                default: false
                                      normalizationPrompt:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 8000
                                    required:
                                      - provider
                                      - voiceId
                                  sttConfig:
                                    type: object
                                    properties:
                                      provider:
                                        type: string
                                        minLength: 1
                                        maxLength: 50
                                      model:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 100
                                        default: null
                                      language:
                                        type:
                                          - string
                                          - 'null'
                                        minLength: 1
                                        default: multi
                                      baseUrl:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2048
                                      apiKey:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 500
                                      additionalSettings:
                                        type:
                                          - object
                                          - 'null'
                                        additionalProperties: {}
                                        default: {}
                                      confidenceReask:
                                        type:
                                          - object
                                          - 'null'
                                        properties:
                                          enabled:
                                            type: boolean
                                            default: false
                                          threshold:
                                            type: number
                                            minimum: 0
                                            maximum: 1
                                            default: 0.3
                                          reduction:
                                            type: string
                                            enum:
                                              - min
                                            default: min
                                          disableOnDigitNodes:
                                            type: boolean
                                            default: true
                                          reaskMode:
                                            type: string
                                            enum:
                                              - phrase
                                              - llm
                                            default: phrase
                                          reaskPhrases:
                                            type:
                                              - array
                                              - 'null'
                                            items:
                                              type: string
                                              maxLength: 2000
                                            maxItems: 20
                                            default: null
                                          maxConsecutiveReasks:
                                            type: integer
                                            minimum: 0
                                            maximum: 5
                                            default: 2
                                    required:
                                      - provider
                                  complianceConfig:
                                    type: object
                                    properties:
                                      pciDss:
                                        type: boolean
                                        default: false
                                      mifidIi:
                                        type: boolean
                                        default: false
                                      euAiAct:
                                        type: boolean
                                        default: false
                                      soc2:
                                        type: boolean
                                        default: false
                                  callTimeoutSettings:
                                    type:
                                      - object
                                      - 'null'
                                    properties:
                                      silenceTimeout:
                                        type: integer
                                        minimum: 0
                                        default: 0
                                      maximumDuration:
                                        type: integer
                                        minimum: 0
                                        maximum: 3600
                                        default: 600
                                      checkInMessage:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2000
                                        default: null
                                      closureMessage:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2000
                                        default: null
                                      maxRetries:
                                        type: integer
                                        minimum: 0
                                        maximum: 10
                                        default: 2
                                      silenceTimeoutPrompt:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2000
                                        default: null
                                      maxDurationEndCall:
                                        type:
                                          - object
                                          - 'null'
                                        properties:
                                          messageMode:
                                            type: string
                                            enum:
                                              - llm
                                              - custom
                                              - none
                                            default: llm
                                          spokenMessage:
                                            type:
                                              - string
                                              - 'null'
                                            maxLength: 2000
                                            default: null
                                          llmPrompt:
                                            type:
                                              - string
                                              - 'null'
                                            maxLength: 2000
                                            default: null
                                          interruptible:
                                            type: boolean
                                            default: false
                                          triggerTimeout:
                                            type:
                                              - number
                                              - 'null'
                                            minimum: 0
                                            default: null
                                        default: null
                                      dynamicWait:
                                        type:
                                          - object
                                          - 'null'
                                        properties:
                                          enabled:
                                            type: boolean
                                            default: false
                                          maxWaitSeconds:
                                            type: integer
                                            minimum: 10
                                            maximum: 3600
                                            default: 300
                                          maxRetries:
                                            type: integer
                                            minimum: 0
                                            maximum: 10
                                            default: 1
                                          checkInMessage:
                                            type:
                                              - string
                                              - 'null'
                                            maxLength: 2000
                                            default: null
                                          checkInPrompt:
                                            type:
                                              - string
                                              - 'null'
                                            maxLength: 2000
                                            default: null
                                          vadConfidence:
                                            type:
                                              - number
                                              - 'null'
                                            minimum: 0
                                            maximum: 1
                                            default: null
                                          vadMinVolume:
                                            type:
                                              - number
                                              - 'null'
                                            minimum: 0
                                            maximum: 1
                                            default: null
                                          vadStartSecs:
                                            type:
                                              - number
                                              - 'null'
                                            minimum: 0
                                            maximum: 5
                                            default: null
                                          vadStopSecs:
                                            type:
                                              - number
                                              - 'null'
                                            minimum: 0
                                            maximum: 10
                                            default: null
                                        default: null
                                  voicemailDetection:
                                    type:
                                      - object
                                      - 'null'
                                    properties:
                                      enabled:
                                        type: boolean
                                        default: false
                                      messageMode:
                                        type: string
                                        enum:
                                          - llm
                                          - custom
                                          - none
                                        default: none
                                      staticMessage:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2000
                                        default: null
                                      voicemailResponseDelay:
                                        type: number
                                        minimum: 0
                                        maximum: 30
                                        default: 2
                                  dtmfConfig:
                                    type:
                                      - object
                                      - 'null'
                                    properties:
                                      enabled:
                                        type: boolean
                                        default: false
                                      timeout:
                                        type: number
                                        minimum: 0
                                        maximum: 30
                                        default: 2
                                      terminationDigit:
                                        type: string
                                        enum:
                                          - '0'
                                          - '1'
                                          - '2'
                                          - '3'
                                          - '4'
                                          - '5'
                                          - '6'
                                          - '7'
                                          - '8'
                                          - '9'
                                          - '#'
                                          - '*'
                                        default: '#'
                                      prefix:
                                        type: string
                                        maxLength: 100
                                        default: 'DTMF: '
                                  postConversationAnalysis:
                                    type:
                                      - object
                                      - 'null'
                                    properties:
                                      summaryPrompt:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 10000
                                        default: null
                                      autoDetectProblems:
                                        type: boolean
                                        default: false
                                      problemDetectionPrompt:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 10000
                                        default: null
                                      problemDetectionInstructions:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 10000
                                        default: null
                                      analysisModel:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 100
                                        default: null
                                  privacyConfig:
                                    type:
                                      - object
                                      - 'null'
                                    properties:
                                      enableRecording:
                                        type: boolean
                                        default: false
                                      getRecordingConsent:
                                        type: boolean
                                        default: false
                                      recordingConsentText:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 500
                                        default: null
                                      stopSecs:
                                        type: number
                                        minimum: 0
                                      preSpeechMs:
                                        type: number
                                        minimum: 0
                                      maxDurationSecs:
                                        type: number
                                        minimum: 0
                                  turnAnalyzerConfig:
                                    type: object
                                    properties:
                                      provider:
                                        type: string
                                        enum:
                                          - local
                                          - fal
                                      url:
                                        type:
                                          - string
                                          - 'null'
                                        format: uri
                                      modelPath:
                                        type:
                                          - string
                                          - 'null'
                                  guardrailsConfig:
                                    type:
                                      - object
                                      - 'null'
                                    properties:
                                      guardrails_enabled:
                                        type: boolean
                                        default: false
                                      custom_rules_enabled:
                                        type: boolean
                                        default: false
                                      rules:
                                        type: array
                                        items:
                                          type: object
                                          properties:
                                            id:
                                              type:
                                                - string
                                                - 'null'
                                            type:
                                              type: string
                                              enum:
                                                - exact
                                                - regex
                                                - dictionary
                                                - structured
                                                - classifier
                                            pattern:
                                              type: string
                                            action:
                                              type: string
                                              enum:
                                                - refuse
                                                - regenerate
                                                - log_only
                                            enabled:
                                              type: boolean
                                              default: true
                                            description:
                                              type:
                                                - string
                                                - 'null'
                                            case_sensitive:
                                              type: boolean
                                              default: false
                                            classifier_threshold:
                                              type: number
                                              minimum: 0
                                              maximum: 1
                                        default: []
                                      refuse_message:
                                        type: string
                                        default: I'm sorry, I can't help with that.
                                      max_regenerate_retries:
                                        type: integer
                                        minimum: 0
                                        maximum: 5
                                        default: 2
                                      regenerate_wait_message:
                                        type: string
                                        default: One moment, please.
                                      classifier_enabled:
                                        type: boolean
                                        default: false
                                      classifier_provider:
                                        type: string
                                      classifier_model:
                                        type: string
                                      input_config:
                                        type: object
                                        properties:
                                          enabled:
                                            type: boolean
                                            default: false
                                          normalize:
                                            type: boolean
                                            default: true
                                          detect_injection:
                                            type: boolean
                                            default: true
                                          detect_weird_input:
                                            type: boolean
                                            default: true
                                          run_classifier:
                                            type: boolean
                                            default: true
                                          refuse_message:
                                            type: string
                                            default: I'm sorry, I can't help with that.
                                          max_input_chars:
                                            type: integer
                                            minimum: 1
                                            maximum: 100000
                                            default: 8000
                                  piiRedactionConfig:
                                    type:
                                      - object
                                      - 'null'
                                    properties:
                                      enabled:
                                        type: boolean
                                        default: false
                                      maskEmail:
                                        type: boolean
                                        default: true
                                      maskPhone:
                                        type: boolean
                                        default: true
                                      maskPaymentCard:
                                        type: boolean
                                        default: true
                                      maskNationalId:
                                        type: boolean
                                        default: true
                                      maskIban:
                                        type: boolean
                                        default: true
                                      customRules:
                                        type: array
                                        items:
                                          type: object
                                          properties:
                                            label:
                                              type: string
                                              minLength: 1
                                              maxLength: 40
                                              pattern: ^[A-Z0-9_]+$
                                            pattern:
                                              type: string
                                              minLength: 1
                                              maxLength: 500
                                            enabled:
                                              type: boolean
                                              default: true
                                          required:
                                            - label
                                            - pattern
                                        default: []
                                  routingLlmConfig:
                                    type:
                                      - object
                                      - 'null'
                                    properties:
                                      provider:
                                        type: string
                                        minLength: 1
                                        maxLength: 50
                                      model:
                                        type: string
                                        minLength: 1
                                        maxLength: 100
                                      baseUrl:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2048
                                      apiKey:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 500
                                    required:
                                      - provider
                                      - model
                                  extractionLlmConfig:
                                    type:
                                      - object
                                      - 'null'
                                    properties:
                                      provider:
                                        type: string
                                        minLength: 1
                                        maxLength: 50
                                      model:
                                        type: string
                                        minLength: 1
                                        maxLength: 100
                                      baseUrl:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 2048
                                      apiKey:
                                        type:
                                          - string
                                          - 'null'
                                        maxLength: 500
                                    required:
                                      - provider
                                      - model
                                  backgroundSoundUrl:
                                    type:
                                      - string
                                      - 'null'
                                    maxLength: 200
                                    default: null
                                  syncSource:
                                    type:
                                      - object
                                      - 'null'
                                    properties:
                                      url:
                                        type: string
                                        maxLength: 2048
                                        format: uri
                                      apiKey:
                                        type: string
                                        maxLength: 500
                                      syncedAt:
                                        type:
                                          - string
                                          - 'null'
                                        format: date-time
                                    required:
                                      - url
                                      - apiKey
                                  testVariables:
                                    type: object
                                    additionalProperties:
                                      type: string
                                required:
                                  - llmConfig
                                  - ttsConfig
                                  - sttConfig
                                  - complianceConfig
                              isImported:
                                type: boolean
                                default: false
                              createdAt:
                                type: string
                                format: date-time
                              updatedAt:
                                type: string
                                format: date-time
                            required:
                              - id
                              - workspaceId
                              - userId
                              - name
                              - config
                              - createdAt
                              - updatedAt
                        required:
                          - agent
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
        '409':
          description: An agent with this name already exists
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