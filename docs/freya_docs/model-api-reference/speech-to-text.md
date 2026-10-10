> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Speech-to-Text

> Transcribe an audio file to text. Accepts multipart form upload with the audio file and optional parameters. Compatible with the OpenAI audio transcription API.



## OpenAPI

````yaml /api-reference/model-apis-openapi.json post /v1/audio/transcriptions
openapi: 3.1.0
info:
  title: Freya Model APIs
  description: Speech-to-Text and Text-to-Speech APIs powered by Freya.
  version: 1.0.0
servers:
  - url: https://stt.freyavoice.ai
security:
  - bearerAuth: []
paths:
  /v1/audio/transcriptions:
    post:
      summary: Speech-to-Text
      description: >-
        Transcribe an audio file to text. Accepts multipart form upload with the
        audio file and optional parameters. Compatible with the OpenAI audio
        transcription API.
      operationId: createTranscription
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              required:
                - file
              properties:
                file:
                  type: string
                  format: binary
                  description: >-
                    The audio file to transcribe. Supported formats: `wav`,
                    `mp3`, `flac`, `ogg`, `m4a`, `webm`. Maximum size: 15 MB.
                model:
                  type: string
                  default: freya-stt
                  description: The model to use for transcription.
                response_format:
                  type: string
                  default: json
                  enum:
                    - json
                    - text
                    - verbose_json
                  description: >-
                    The format of the response. `json` returns `{"text":
                    "..."}`. `text` returns plain text. `verbose_json` includes
                    language, timing, and word-level data.
                temperature:
                  type: number
                  default: 0
                  description: >-
                    Sampling temperature between 0 and 1. Lower values are more
                    deterministic.
      responses:
        '200':
          description: Transcription successful.
          content:
            application/json:
              schema:
                oneOf:
                  - type: object
                    description: Standard JSON response (response_format=json)
                    properties:
                      text:
                        type: string
                        description: The transcribed text.
                      inference_time_ms:
                        type: number
                        description: Server-side inference time in milliseconds.
                  - type: object
                    description: Verbose JSON response (response_format=verbose_json)
                    properties:
                      text:
                        type: string
                        description: The transcribed text.
                      language:
                        type: string
                        description: Detected or specified language.
                      inference_time_ms:
                        type: number
                        description: Server-side inference time in milliseconds.
                      words:
                        type: array
                        description: Word-level data with confidence scores.
                        items:
                          type: object
                          properties:
                            word:
                              type: string
                            confidence:
                              type: number
              examples:
                json:
                  summary: Standard response
                  value:
                    text: Merhaba, bu bir test konuşmasıdır.
                    inference_time_ms: 342.5
                verbose_json:
                  summary: Verbose response
                  value:
                    text: Merhaba, bu bir test konuşmasıdır.
                    language: Turkish
                    inference_time_ms: 342.5
                    words:
                      - word: Merhaba,
                        confidence: 0.98
                      - word: bu
                        confidence: 0.95
                      - word: bir
                        confidence: 0.97
                      - word: test
                        confidence: 0.92
                      - word: konuşmasıdır.
                        confidence: 0.89
            text/plain:
              schema:
                type: string
                description: Plain text transcription (response_format=text)
        '400':
          description: Bad request — missing file, unsupported format, or file too large.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: object
                    properties:
                      message:
                        type: string
                      type:
                        type: string
                      code:
                        type: string
        '403':
          description: Authentication failed or insufficient credits.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: object
                    properties:
                      message:
                        type: string
                      type:
                        type: string
                      code:
                        type: string
        '429':
          description: Rate limit exceeded.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: object
                    properties:
                      message:
                        type: string
                      type:
                        type: string
                      code:
                        type: string
      servers:
        - url: https://stt.freyavoice.ai
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      description: Bearer token issued by your workspace.

````

This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.