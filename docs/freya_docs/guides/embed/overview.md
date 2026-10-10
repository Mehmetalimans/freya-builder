> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Embed SDK

> Add a Freya voice or chat agent to any web page — full control over your UI, powered by WebRTC under the hood

## Overview

The Freya Client SDK connects a Freya agent directly from the browser. You build whatever UI you want; the SDK handles WebRTC transport, microphone input, remote audio playback, and the real-time event stream between the page and the agent.

The SDK is loaded as a script tag — no build step or package manager required.

## How it works

The connection flow has two parts: your backend mints a short-lived token, and the browser uses that token to open a WebRTC session.

1. The user does something on your page that should start a session (a button click, a page load, etc.)
2. Your page calls your own backend — never the Freya API directly
3. Your backend calls `POST /api/token/embed` with your API key and returns the token to the browser
4. The browser passes the token to `FreyaClient`, which connects to the agent over WebRTC
5. Events fire as the conversation unfolds — transcripts, speaking state, tool calls — and you handle them however your UI needs

The API key never reaches the browser. The token is scoped to a single session and expires on its own.

## Minting a token

Token minting must happen server-side. The API key used must have the **Issue web call tokens** permission (`calls:web-token`), which allows it to mint tokens for in-browser calls and external embed integrations. You can set this when creating a key from the **API Keys** button in the sidebar.

<CodeGroup>
  ```python Python (FastAPI) theme={null}
  import requests

  @app.get("/api/assistant-token")
  def assistant_token(request: Request):
      resp = requests.post(
          f"{FREYA_BASE_URL}/api/token/embed",
          json={
              "agentId": AGENT_ID,
              "allowedOrigin": f"{request.url.scheme}://{request.headers['host']}",
              "ttlSeconds": 300,
          },
          headers={"Authorization": f"Bearer {API_KEY}"},
      )
      resp.raise_for_status()
      return resp.json()
  ```

  ```javascript Node.js (Express) theme={null}
  app.get('/api/assistant-token', async (req, res) => {
    const resp = await fetch(`${process.env.FREYA_BASE_URL}/api/token/embed`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.FREYA_API_KEY}`,
      },
      body: JSON.stringify({
        agentId: process.env.FREYA_AGENT_ID,
        allowedOrigin: `${req.protocol}://${req.get('host')}`,
        ttlSeconds: 300,
      }),
    });
    res.json(await resp.json());
  });
  ```
</CodeGroup>

The response contains `token`, `expiresAt`, and `baseUrl`. Pass all three to `FreyaClient`.

<Tip>
  If your users are behind firewalls or strict NAT, also fetch TURN credentials server-to-server from `GET /api/token/webrtc/ice-servers` and forward them alongside the token. This saves a round-trip from the browser and keeps TURN credentials off the client.
</Tip>

## Installation

Add the script to your page. The SDK is served directly from the Freya dashboard:

```html theme={null}
<script src="https://app.freyavoice.ai/freya-client.js"></script>
```

This exposes `window.Freya.FreyaClient` globally. No build step, bundler, or package manager is needed.

## Quick start

```html theme={null}
<script src="https://app.freyavoice.ai/freya-client.js"></script>
<script>
  const { FreyaClient } = window.Freya;

  async function startSession() {
    const { token, baseUrl, iceServers } = await fetch('/api/assistant-token')
      .then(r => r.json());

    const client = new FreyaClient({ baseUrl, token, iceServers });

    client.on('stateChanged', (state) => {
      console.log('state:', state); // connecting → connected → ready
    });

    client.on('botTranscript', ({ text }) => {
      appendMessage('agent', text);
    });

    client.on('userTranscript', ({ text, final }) => {
      if (final) appendMessage('user', text);
    });

    await client.connect();
  }
</script>
```

## Configuration

| Option | Type | Required | Default | Description |
| - | - | - | - | - |
| `baseUrl` | `string` | Yes | — | Freya API origin returned by the token endpoint |
| `token` | `string` | Yes | — | Short-lived embed JWT |
| `mode` | `"call"` \| `"chat"` | No | `"call"` | `"call"` activates the microphone; `"chat"` is text-only |
| `metadata` | `Record<string, unknown>` | No | `{}` | Arbitrary key-value pairs forwarded to the agent session |
| `customerVariables` | `Record<string, string>` | No | `{}` | Variables injected into the agent's system prompt at runtime |
| `iceServers` | `RTCIceServer[]` | No | `[]` | TURN/STUN servers for production deployments |

## Modes

### Call mode

The microphone is activated when `connect()` resolves. The agent hears the user in real time and responds with voice. This is the default.

```javascript theme={null}
const { FreyaClient } = window.Freya;
const client = new FreyaClient({ baseUrl, token }); // mode: "call" by default
```

### Chat mode

The microphone stays off. Send text with `sendMessage()` and listen to `botLlmText` or `botTranscript` for the agent's response. If the agent has TTS configured, audio is still played.

```javascript theme={null}
const { FreyaClient } = window.Freya;
const client = new FreyaClient({ baseUrl, token, mode: 'chat' });
await client.connect();
await client.sendMessage('What are your opening hours?');
```

## Token lifecycle

* Tokens expire after `ttlSeconds` (default 300 seconds). Mint a fresh one each time the user starts a new session rather than caching across page loads.
* Set `allowedOrigin` on the server to the exact origin of the embedding page. The Freya backend rejects WebRTC connection attempts from other origins.
* Tokens are single-use for establishing a session. Once a session is open the token is consumed.

## Next steps

<CardGroup cols={2}>
  <Card title="Client Reference" icon="book" href="/guides/embed/reference">
    Full reference for all FreyaClient methods, events, and their payloads.
  </Card>

  <Card title="Agents" icon="robot" href="/guides/fundamentals/agents">
    Configure the agent your embed session connects to — voice, system prompt, and tools.
  </Card>
</CardGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.