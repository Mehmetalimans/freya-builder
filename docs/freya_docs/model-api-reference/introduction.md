> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Introduction

> Freya Model APIs for Speech-to-Text and Text-to-Speech

## Overview

The Freya Model APIs provide direct access to our Speech-to-Text (STT) and Text-to-Speech (TTS) models. These are standalone inference endpoints — separate from the platform Call API.

| Model | Endpoint | Description |
| - | - | - |
| Speech-to-Text | `stt.freyavoice.ai` | Transcribe audio files or stream real-time audio to text |
| Text-to-Speech | `tts.freyavoice.ai` | Convert text to natural-sounding speech |

<Card title="OpenAPI: Model API endpoints" icon="microphone" href="/api-reference/model-apis-openapi.json">
  Browse the full schema for STT and TTS endpoints.
</Card>

## Authentication

All endpoints require a Bearer token issued by your workspace. See the [Authentication guide](/api-reference/authentication) for how to generate an API key.

```bash theme={null}
Authorization: Bearer YOUR_API_KEY
```

## Quick Start

### Speech-to-Text (File Upload)

```bash theme={null}
curl -X POST "https://stt.freyavoice.ai/v1/audio/transcriptions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@audio.wav"
```

### Speech-to-Text (Real-Time Streaming)

Connect via WebSocket for live transcription with partial results:

```
wss://stt.freyavoice.ai/v1/audio/stream?token=YOUR_API_KEY
```

See the [STT documentation](/api-reference/stt) for the full streaming wire protocol and code examples.

### Text-to-Speech

```bash theme={null}
curl -X POST "https://tts.freyavoice.ai/v1/audio/speech" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "Merhaba, Freya ile konuşuyorsunuz.", "voice": "leyla", "model": "tts-1"}'
```

<Note>
  These Model APIs are independent of the Freyavoice Call API. They can be used standalone for any speech processing task, not just within Freya call workflows.
</Note>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.