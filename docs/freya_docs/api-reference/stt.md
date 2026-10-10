> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Speech-to-Text

> Transcribe audio files or stream real-time audio to text using Freya ASR

## File Transcription

Upload an audio file and receive a text transcription. This endpoint is compatible with the [OpenAI Audio Transcription API](https://platform.openai.com/docs/api-reference/audio/createTranscription).

<Card title="POST /v1/audio/transcriptions" icon="microphone" href="/model-api-reference/post-v1-audio-transcriptions">
  View the full OpenAPI reference for file transcription.
</Card>

### Supported Formats

`wav`, `mp3`, `flac`, `ogg`, `m4a`, `webm` — up to **15 MB** per file.

### Request

```bash theme={null}
curl -X POST "https://stt.freyavoice.ai/v1/audio/transcriptions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@audio.wav" \
  -F "model=freya-stt" \
  -F "response_format=verbose_json"
```

| Parameter | Type | Default | Description |
| :- | :- | :- | :- |
| `file` | binary | *required* | The audio file to transcribe. |
| `model` | string | `freya-stt` | Model identifier. |
| `response_format` | string | `json` | One of `json`, `text`, or `verbose_json`. |
| `temperature` | number | `0.0` | Sampling temperature (0–1). Lower is more deterministic. |

### Response Formats

<Tabs>
  <Tab title="json (default)">
    ```json theme={null}
    {
      "text": "Merhaba, bu bir test konuşmasıdır.",
      "inference_time_ms": 342.5
    }
    ```
  </Tab>

  <Tab title="verbose_json">
    Includes detected language and word-level confidence scores:

    ```json theme={null}
    {
      "text": "Merhaba, bu bir test konuşmasıdır.",
      "language": "Turkish",
      "inference_time_ms": 342.5,
      "words": [
        { "word": "Merhaba,", "confidence": 0.98 },
        { "word": "bu", "confidence": 0.95 },
        { "word": "bir", "confidence": 0.97 },
        { "word": "test", "confidence": 0.92 },
        { "word": "konuşmasıdır.", "confidence": 0.89 }
      ]
    }
    ```
  </Tab>

  <Tab title="text">
    Returns plain text with no JSON wrapper:

    ```
    Merhaba, bu bir test konuşmasıdır.
    ```
  </Tab>
</Tabs>

***

## Real-Time Streaming (WebSocket)

For real-time transcription, connect via WebSocket and stream audio frames. The server uses **LocalAgreement** to emit stable (confirmed) words as they are recognized, plus tentative partial results.

<Warning>
  Real-time streaming is currently in **beta**. The WebSocket endpoint is available at `wss://stt.freyavoice.ai/v1/audio/stream`.
</Warning>

### Connection

```
wss://stt.freyavoice.ai/v1/audio/stream?token=YOUR_API_KEY
```

Pass your API key as the `token` query parameter. Non-browser clients can alternatively use the `Authorization: Bearer YOUR_API_KEY` header during the WebSocket handshake.

### Wire Protocol

The session follows a simple three-phase protocol:

**1. Configure** — Send a JSON text frame with session settings:

```json theme={null}
{
  "type": "config",
  "sample_rate": 16000
}
```

| Field | Type | Default | Description |
| :- | :- | :- | :- |
| `sample_rate` | integer | `16000` | Sample rate of the audio you'll send (resampled to 16 kHz internally). |

**2. Stream audio** — Send raw PCM audio as **binary WebSocket frames**.

* Format: **16-bit signed integer, little-endian, mono**
* Send frames continuously as audio is captured (e.g. every 100–500 ms)

**3. End session** — Send a JSON text frame to signal end-of-audio:

```json theme={null}
{ "type": "eof" }
```

### Server Messages

The server sends JSON text frames throughout the session:

| Type | Description | Fields |
| :- | :- | :- |
| `partial` | Tentative (not yet confirmed) transcription of the latest audio | `text` |
| `final` | Newly confirmed words — append these to your transcript | `text` |
| `result` | Final result after `eof` — the complete transcription | `text`, `word_confidences`, `language` |
| `error` | An error occurred | `message` |

<Tabs>
  <Tab title="partial">
    ```json theme={null}
    { "type": "partial", "text": "merhaba nasıl" }
    ```
  </Tab>

  <Tab title="final">
    ```json theme={null}
    { "type": "final", "text": "merhaba" }
    ```
  </Tab>

  <Tab title="result">
    ```json theme={null}
    {
      "type": "result",
      "text": "Merhaba, nasılsınız?",
      "word_confidences": [
        { "word": "Merhaba,", "confidence": 0.97 },
        { "word": "nasılsınız?", "confidence": 0.94 }
      ],
      "language": "Turkish"
    }
    ```
  </Tab>

  <Tab title="error">
    ```json theme={null}
    { "type": "error", "message": "Invalid config frame." }
    ```
  </Tab>
</Tabs>

### How LocalAgreement Works

The server re-transcribes the accumulated audio buffer on every tick (\~500 ms). It compares consecutive hypotheses and only emits words that both agree on as `final`. The unstable tail is sent as `partial` and may change on the next tick. This gives you low-latency confirmed words without hallucinated flicker.

### JavaScript Example

```javascript theme={null}
const token = "YOUR_API_KEY";
const ws = new WebSocket(`wss://stt.freyavoice.ai/v1/audio/stream?token=${token}`);

ws.onopen = () => {
  // 1. Send config
  ws.send(JSON.stringify({
    type: "config",
    sample_rate: 16000
  }));

  // 2. Stream audio from microphone
  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    const ctx = new AudioContext({ sampleRate: 16000 });
    const source = ctx.createMediaStreamSource(stream);
    const processor = ctx.createScriptProcessor(4096, 1, 1);

    processor.onaudioprocess = (e) => {
      const float32 = e.inputBuffer.getChannelData(0);
      const int16 = new Int16Array(float32.length);
      for (let i = 0; i < float32.length; i++) {
        int16[i] = Math.max(-32768, Math.min(32767, float32[i] * 32768));
      }
      ws.send(int16.buffer);
    };

    source.connect(processor);
    processor.connect(ctx.destination);
  });
};

let transcript = "";

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);

  if (msg.type === "final") {
    transcript += (transcript ? " " : "") + msg.text;
    console.log("Confirmed:", transcript);
  } else if (msg.type === "partial") {
    console.log("Tentative:", transcript + " " + msg.text);
  } else if (msg.type === "result") {
    console.log("Final result:", msg.text);
  }
};

// 3. When done recording:
// ws.send(JSON.stringify({ type: "eof" }));
```

### Python Example

```python theme={null}
import asyncio
import json
import wave
import websockets

API_KEY = "YOUR_API_KEY"

async def transcribe_stream(audio_path: str):
    uri = f"wss://stt.freyavoice.ai/v1/audio/stream?token={API_KEY}"

    async with websockets.connect(uri) as ws:
        # 1. Configure
        await ws.send(json.dumps({
            "type": "config",
            "sample_rate": 16000,
        }))

        # 2. Stream audio in chunks
        with wave.open(audio_path, "rb") as wf:
            chunk_size = 8000  # 250ms at 16kHz mono 16-bit
            while True:
                data = wf.readframes(chunk_size // 2)
                if not data:
                    break
                await ws.send(data)
                await asyncio.sleep(0.1)

        # 3. Signal end
        await ws.send(json.dumps({"type": "eof"}))

        # 4. Collect results
        async for message in ws:
            msg = json.loads(message)
            if msg["type"] == "final":
                print(f"[confirmed] {msg['text']}")
            elif msg["type"] == "partial":
                print(f"[partial]   {msg['text']}")
            elif msg["type"] == "result":
                print(f"\nFull transcript: {msg['text']}")
                break

asyncio.run(transcribe_stream("audio.wav"))
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.