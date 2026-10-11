> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Text-to-Speech

> Converts text into natural-sounding speech using Freya's TTS model. Returns a binary audio file. Supports the following emotion tags: [pause], [eee], [throat clearing], [mm-hmm], [laughter], [deep breath], [hmm], [cough], [breath]



## OpenAPI

````yaml /api-reference/model-apis-openapi.json post /v1/audio/speech
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
  /v1/audio/speech:
    post:
      summary: Text-to-Speech
      description: >-
        Converts text into natural-sounding speech using Freya's TTS model.
        Returns a binary audio file. Supports the following emotion tags:
        [pause], [eee], [throat clearing], [mm-hmm], [laughter], [deep breath],
        [hmm], [cough], [breath]
      operationId: createSpeech
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - input
                - voice
              properties:
                input:
                  type: string
                  description: The text to synthesize audio for.
                voice:
                  type: string
                  default: leyla
                  enum:
                    - leyla
                    - zeynep
                    - alev
                    - ali
                    - alper
                    - mustafa
                  description: The voice ID to use.
                response_format:
                  type: string
                  default: mp3
                  enum:
                    - mp3
                    - opus
                    - aac
                    - flac
                    - wav
                    - pcm
                  description: Response format for the API request.
                model:
                  type: string
                  default: tts-1
                  enum:
                    - tts-1
                    - tts-1-hd
                  description: >-
                    Quality preset. `tts-1` is faster; `tts-1-hd` is higher
                    quality.
            example:
              model: tts-1
              input: Hello, testing Freya Voice API.
              voice: leyla
      responses:
        '200':
          description: Audio file generated successfully.
          content:
            audio/wav:
              schema:
                type: string
                format: binary
                description: Binary WAV audio data.
        '400':
          description: Bad request — missing or invalid parameters.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
      servers:
        - url: https://tts.freyavoice.ai
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      description: Bearer token issued by your workspace.

````

This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.