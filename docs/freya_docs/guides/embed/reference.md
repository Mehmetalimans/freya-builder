> ## Documentation Index
> Fetch the complete documentation index at: https://docs.freyavoice.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Client Reference

> Complete reference for FreyaClient methods, properties, and events

`FreyaClient` is the main class exposed by the SDK. Access it via `window.Freya.FreyaClient` after loading the script.

```javascript theme={null}
const { FreyaClient } = window.Freya;
const client = new FreyaClient({ baseUrl, token });
```

***

## Methods

### `connect()`

Opens the WebRTC session and, in call mode, activates the microphone. Returns a promise that resolves once the connection is established.

```javascript theme={null}
await client.connect();
```

Throws if called while already connected. Call `disconnect()` first if you need to start a new session.

***

### `disconnect()`

Ends the current session and releases all media resources. Safe to call multiple times — subsequent calls after the session is already closed are no-ops.

```javascript theme={null}
await client.disconnect();
```

***

### `sendMessage(text)`

Sends a text message to the agent. Primarily used in `"chat"` mode, where the microphone is off and the user communicates by typing.

```javascript theme={null}
await client.sendMessage('What are your opening hours?');
```

| Parameter | Type | Description |
| - | - | - |
| `text` | `string` | The message to send to the agent |

***

### `mute()`

Stops sending microphone audio to the agent without disconnecting the session. Has no effect in `"chat"` mode.

```javascript theme={null}
client.mute();
```

***

### `unmute()`

Resumes sending microphone audio after a call to `mute()`.

```javascript theme={null}
client.unmute();
```

***

### `on(event, handler)`

Registers a handler for the given event. Returns the client instance so calls can be chained.

```javascript theme={null}
client.on('botTranscript', ({ text }) => {
  console.log(text);
});
```

See [Events](#events) below for the full list.

***

### `off(event, handler)`

Removes a previously registered handler. The `handler` reference must be the same function passed to `on()`.

```javascript theme={null}
const handler = ({ text }) => console.log(text);
client.on('botTranscript', handler);

// Later:
client.off('botTranscript', handler);
```

***

## Properties

### `state`

The current transport state as a string. Reflects the underlying WebRTC connection lifecycle.

| Value | Description |
| - | - |
| `"connecting"` | Session is being established |
| `"connected"` | WebRTC handshake complete |
| `"ready"` | Agent is initialized and ready to interact |
| `"disconnected"` | Session has ended |

```javascript theme={null}
console.log(client.state); // "ready"
```

***

### `isMicEnabled`

Boolean. `true` when the microphone is active and sending audio. Always `false` in `"chat"` mode and when the session is not connected.

```javascript theme={null}
if (!client.isMicEnabled) {
  showMutedIndicator();
}
```

***

## Events

Register handlers with `client.on(event, handler)` and remove them with `client.off(event, handler)`. All handlers receive a single payload argument (or none, for events with no data).

### Connection events

#### `stateChanged`

Fires whenever the connection state changes. Use this to drive loading indicators, connected states, and error UI.

```javascript theme={null}
client.on('stateChanged', (state) => {
  // state: "connecting" | "connected" | "ready" | "disconnected"
});
```

| Payload | Type |
| - | - |
| `state` | `"connecting"` \| `"connected"` \| `"ready"` \| `"disconnected"` |

***

#### `disconnected`

Fires when the session ends, whether closed locally via `disconnect()` or terminated remotely. No payload.

```javascript theme={null}
client.on('disconnected', () => {
  resetUI();
});
```

***

#### `error`

Fires when an error occurs. When `fatal` is `true` the session has already ended — you do not need to call `disconnect()`.

```javascript theme={null}
client.on('error', ({ message, fatal }) => {
  showError(message);
  if (fatal) resetUI();
});
```

| Payload field | Type | Description |
| - | - | - |
| `message` | `string` | Human-readable error description |
| `fatal` | `boolean` | Whether the session has ended as a result |

***

### Agent speech events

#### `botReady`

Fires once after `connect()` when the agent has fully initialized and is ready to receive input. No payload.

```javascript theme={null}
client.on('botReady', () => {
  enableInputControls();
});
```

***

#### `botStartedSpeaking`

Fires when the agent begins a spoken response. No payload. Use this to show a speaking indicator or pause user input.

```javascript theme={null}
client.on('botStartedSpeaking', () => {
  showSpeakingIndicator();
});
```

***

#### `botStoppedSpeaking`

Fires when the agent finishes speaking. No payload. Use this to seal the current transcript turn and reset streaming state.

```javascript theme={null}
client.on('botStoppedSpeaking', () => {
  hideSpeakingIndicator();
  sealCurrentTurn();
});
```

***

#### `botLlmText`

Fires for each token as the LLM generates its response. Concatenate the `text` values to build the full message in real time. Stops firing before `botStoppedSpeaking`.

```javascript theme={null}
let buffer = '';

client.on('botLlmText', ({ text }) => {
  buffer += text;
  renderStreamingMessage(buffer);
});

client.on('botStoppedSpeaking', () => {
  buffer = '';
});
```

| Payload field | Type | Description |
| - | - | - |
| `text` | `string` | A single LLM output token or token fragment |

***

#### `botTranscript`

Fires once per agent turn with the complete response text, after the agent finishes speaking. Use this instead of `botLlmText` if you only need the final result rather than a streaming view.

```javascript theme={null}
client.on('botTranscript', ({ text }) => {
  appendMessage('agent', text);
});
```

| Payload field | Type | Description |
| - | - | - |
| `text` | `string` | The complete agent response for this turn |

***

#### `botOutput`

Fires with TTS-level text chunks. Only fires when LLM streaming (`botLlmText`) is not available. In most configurations you can ignore this event and use `botLlmText` / `botTranscript` instead.

| Payload field | Type | Description |
| - | - | - |
| `text` | `string` | The spoken text chunk |
| `spoken` | `boolean` | Whether this chunk was sent to TTS |

***

### User speech events

#### `userStartedSpeaking`

Fires when voice activity is detected from the user's microphone. No payload. Use this to show a recording indicator.

```javascript theme={null}
client.on('userStartedSpeaking', () => {
  showRecordingIndicator();
});
```

***

#### `userStoppedSpeaking`

Fires when the user's voice activity stops. No payload.

```javascript theme={null}
client.on('userStoppedSpeaking', () => {
  hideRecordingIndicator();
});
```

***

#### `userTranscript`

Fires with the transcription of the user's speech. Partial results arrive with `final: false` as the user speaks; the completed turn arrives with `final: true`.

```javascript theme={null}
client.on('userTranscript', ({ text, final }) => {
  if (final) {
    appendMessage('user', text);
  }
});
```

| Payload field | Type | Description |
| - | - | - |
| `text` | `string` | Transcription of the user's speech so far |
| `final` | `boolean` | `true` when the user's turn is complete |

***

### Tool call events

#### `toolCallStarted`

Fires when the agent decides to invoke a tool, before arguments are assembled.

| Payload field | Type | Description |
| - | - | - |
| `function_name` | `string?` | The name of the tool being called |
| `tool_call_id` | `string?` | Unique identifier for this tool call |

***

#### `toolCallInProgress`

Fires once the agent has fully assembled the arguments for a tool call. This is the right place to update your UI in response to agent actions — you know exactly what the agent is about to do.

```javascript theme={null}
client.on('toolCallInProgress', ({ function_name, arguments: args }) => {
  if (function_name === 'navigate') {
    showPage(args.page);
  }
  if (function_name === 'update_balance') {
    setBalance(args.amount);
  }
});
```

| Payload field | Type | Description |
| - | - | - |
| `function_name` | `string` | The name of the tool being called |
| `tool_call_id` | `string` | Unique identifier for this tool call |
| `arguments` | `Record<string, unknown>` | The fully assembled arguments object |

***

#### `toolCallStopped`

Fires when a tool call completes.

| Payload field | Type | Description |
| - | - | - |
| `function_name` | `string?` | The name of the tool that was called |
| `tool_call_id` | `string?` | Unique identifier for the completed call |

***

### Media track events

#### `trackStarted`

Fires when a remote media track becomes active. The SDK handles remote audio playback automatically — you only need this event if you want access to the raw `MediaStreamTrack` for custom processing.

| Payload | Type |
| - | - |
| `track` | `MediaStreamTrack` |

***

#### `trackStopped`

Fires when a remote media track ends.

| Payload | Type |
| - | - |
| `track` | `MediaStreamTrack` |


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.