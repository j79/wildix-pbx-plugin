## Wilma Voice API 🆕

_OpenAPI: Wilma Voice Service — version v2_

**Servers**

- `https://api.wilma.wildix.com` — Production
- `https://api-stable.wilma.wildix.com` — Stable
- `https://api-stage.wilma.wildix.com` — Stage

### Calls

#### `GET` `/v2/voice/calls/{callId}/events`

Tails a live call's events as Server-Sent Events (`text/event-stream`): the caller's recognised speech, the agent's spoken sentences, playback, interruptions, language switches and the session lifecycle. Live only — nothing before the subscription is replayed, and the stream is not a record of the call (the session trace is). Ends after an `ended` event whose reason is not `transfer`; after a transfer it stays open briefly for the next session of the same call. What the stream carries is decided HERE, by who is asking, and is not a request parameter: a caller signed in to the system receives everything, including the agent's own commands (`reply`, `say`, `playback`, `interruption`) and its tool calls, and chooses for itself what to show; a guest receives the transcript alone (`started`, `transcription`, `agentTranscription`, `language`, `ended`).

- operationId: `StreamCallEvents`
- **Scopes**: `wilma-voice:StreamCallEvents`, `wilma-voice:read`
- **Parameters**
  - `callId` (path) — string **(required)** — The PBX call id (LinkedID) — `callId` of the voice session's connect query, and the SIP `X-Session-ID` header the caller's own leg received.
  - `company` (query) — string — Owning company. Only S2S callers may set it; every other token carries its company. _(minLen=3; maxLen=30)_
- **Response 200** (`StreamCallEventsOutputPayload`)
  - string
- Errors: `400`, `403`, `404`

### Other

#### `POST` `/v2/voice/describe`

Describes the WebSocket connect parameters, events and commands of the voice protocol. Utility method; the generated shapes are the source of truth for building a WebSocket client or server by hand.

- operationId: `DescribeVoiceProtocol`
- **Scopes**: `wilma-voice:DescribeVoiceProtocol`, `wilma-voice:read`
- **Response 200** (`DescribeVoiceProtocolResponseContent`)
  - `connectParams` — VoiceConnectParams — Parameters supplied on the WebSocket connect (upgrade) request, as query-string parameters.
    - `protocolVersion` — number — Protocol version advertised by the client (query parameter `v`). 0 (or absent) is the legacy PBX protocol; >= 1 enables the sessionStarted event; >= 2 additionally means the client WAITS for `started` before opening its recognition stream and honours the `speech` payload on it.
    - `sessionId` — string **(required)** — Caller-supplied session id, unique per connection. _(minLen=1; maxLen=128)_
    - `agentId` — string **(required)** — Agent to run on this session. _(minLen=12; maxLen=12)_
    - `agentVersion` — number — Published agent version to run. Mutually exclusive with agentDraft. When neither is set, the agent's deployment configuration selects the version. The PBX sends it only for a preview number (`<agentId>-vN`, WMS-27502); a customer call never carries it. _(min=1)_
    - `agentDraft` — boolean — Run the agent's current draft (for testing). Mutually exclusive with agentVersion.
    - `callId` — string — PBX call id, when the session is bridged to a call.
    - `flowIndex` — number — Leg of the PBX call inside `callId` (pbx-data-engine's flow index). Kept on the session as metadata beside `callId` and `dialedNumber`; never interpreted by the runtime.
    - `dialedNumber` — string — The number the caller dialled to reach the agent. Kept on the session as metadata beside `callId` and `flowIndex`.
    - `language` — string — BCP-47 language of the conversation, e.g. 'en-US'.
    - `callerName` — string
    - `callerNumber` — string
    - `callerEmail` — string
    - `callerCompany` — string
    - `voice` — string — Override the TTS voice for this session, as a voice URI, e.g. 'elevenlabs://<voiceId>?apiKey=...'. Defaults to the agent's configured voice.
    - `initialMessage` — string — First message spoken to the caller. Overrides the agent's configured greeting.
    - `variables` — string — Base64-encoded JSON object of agent variables for this session, e.g. base64('{"orderId":"123"}').
    - `inputMode` — string — How caller speech reaches the service. _(enum: `transcription`, `audio`)_
    - `inputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
      - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
      - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
      - `channels` — number — Channel count. Defaults to 1 (mono).
    - `outputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
      - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
      - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
      - `channels` — number — Channel count. Defaults to 1 (mono).
  - `audioWebsocketEvent` — AudioWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
    - `type` — string **(required)** _(default=event)_
    - `event` — AudioEvent **(required)** — A chunk of raw caller audio, base64-encoded in the session's negotiated input format (inputAudio from the connect handshake). Used by web/app clients in AUDIO input mode; the service buffers and transcribes it server-side. Not used in TRANSCRIPTION mode.
      - `type` — object **(required)**
      - `data` — string **(required)**
      - `seq` — number — Optional monotonic chunk sequence number, for gap detection.
  - `transcriptionWebsocketEvent` — TranscriptionWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
    - `type` — string **(required)** _(default=event)_
    - `event` — TranscriptionEvent **(required)** — A transcription chunk of caller speech, provided by a client that does its own speech-to-text (PBX / TRANSCRIPTION mode), or emitted by the service (AUDIO mode) and echoed to the client.
      - `type` — object **(required)**
      - `id` — string **(required)** — Identifier of a transcription chunk within a session.
      - `text` — string **(required)**
      - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
      - `final` — boolean — True when this is the final transcript for the utterance rather than an interim hypothesis. An absent value is read as final: a client that does not distinguish interim results sends none.
      - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only — it drives no behavior, so an operator can see what the recogniser thought during an utterance that never became a turn. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `time` — number **(required)**
  - `agentTranscriptionWebsocketEvent` — AgentTranscriptionWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
    - `type` — string **(required)** _(default=event)_
    - `event` — AgentTranscriptionEvent **(required)** — A recogniser result for the agent's own leg — what the caller hears. Sent by the PBX for new-stack agents only, from the same dual-channel stream that transcribes the caller. Never starts a turn.
      - `type` — object **(required)**
      - `id` — string **(required)** — Identifier of a transcription chunk within a session.
      - `text` — string **(required)**
      - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
      - `final` — boolean — True when this is the final transcript for the utterance rather than an interim hypothesis. An absent value is read as final, as on `TranscriptionEvent`.
      - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only — it drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `time` — number **(required)**
  - `replyWebsocketEvent` — ReplyWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
    - `type` — string **(required)** _(default=event)_
    - `event` — ReplyEvent **(required)** — A final caller phrase that should trigger an agent turn (PBX / TRANSCRIPTION mode).
      - `type` — object **(required)**
      - `id` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
      - `text` — string **(required)**
      - `language` — string — Language the recogniser identified for this completed utterance. THIS is the one that drives the language switch. When the recogniser reports several languages inside one utterance, the PBX sends the LAST labelled segment's language — it is the one the caller is speaking now. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `startTime` — number **(required)**
      - `endTime` — number **(required)**
  - `playbackWebsocketEvent` — PlaybackWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
    - `type` — string **(required)** _(default=event)_
    - `event` — PlaybackEvent **(required)** — Client-reported progress of an in-flight reply playback.
      - `type` — object **(required)**
      - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
      - `text` — string **(required)**
      - `complete` — boolean **(required)**
      - `startTime` — number **(required)**
      - `endTime` — number
  - `interruptionWebsocketEvent` — InterruptionWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
    - `type` — string **(required)** _(default=event)_
    - `event` — InterruptionEvent **(required)** — The caller interrupted (barged in over) a reply that was being played.
      - `type` — object **(required)**
      - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
      - `playedText` — string **(required)** — Portion of the reply that had been played before the interruption.
      - `originalText` — string **(required)** — The full reply text that was being played.
      - `time` — number **(required)**
  - `completeWebsocketEvent` — CompleteWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
    - `type` — string **(required)** _(default=event)_
    - `event` — CompleteEvent **(required)** — The call/conversation completed (e.g. the caller hung up or the call was transferred away).
      - `type` — object **(required)**
      - `reason` — string **(required)**
      - `time` — number **(required)**
  - `controlWebsocketEvent` — ControlWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
    - `type` — string **(required)** _(default=event)_
    - `event` — ControlEvent **(required)** — A lightweight control frame from the client (AUDIO mode).
      - `type` — object **(required)**
      - `action` — string **(required)** — A client control action on the audio input (AUDIO mode). _(enum: `end_of_turn`, `clear`, `keepalive`)_
  - `sessionStartedWebsocketEvent` — SessionStartedWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
    - `type` — string **(required)** _(default=event)_
    - `event` — SessionStartedEvent **(required)** — Emitted once right after the handshake to confirm the session and the agent it is bound to. Sent only when the client advertises protocol version >= 1.
      - `type` — object **(required)**
      - `time` — number **(required)**
      - `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
      - `agentId` — string **(required)** — Agent bound to the session. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Published agent version resolved at connect; absent when running the agent draft. _(min=1)_
      - `traceId` — string — Trace recording this voice session in wilma-traces — the caller's transcribed phrases, the model calls they drove and the tools the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace to follow a call while it is in progress. Sent once at handshake and stable for the connection: a call is one trace. A caller who redials gets a new session and therefore a new trace, since the trace is keyed on the session id supplied at connect. _(minLen=1; maxLen=128)_
      - `agentName` — string — Agent display name.
      - `category` — string — Agent category.
      - `groupId` — string — PBX group used for data ACL; empty when the agent is not assigned to a group.
      - `speech` — VoiceSpeechPayload — Recognition intent for the call, sent on `started` at protocolVersion >= 2. NOT recogniser parameters: the PBX translates it into its provider's API. Against Amazon Transcribe with autoDetect true that is identify-multiple-languages plus language-options and preferred-language; with autoDetect false, a single-language stream on preferredLanguage. Both members the server can get wrong are RESOLVED here rather than forwarded: `engine` is always concrete (an absent one would let the PBX apply a different default than the console built its language list for), and `autoDetect` is clamped to false whenever the language count is below the recogniser's minimum or the recogniser cannot identify languages at all (forwarding true with one candidate makes Amazon reject the stream outright — a dead call).
        - `engine` — string **(required)** — Concrete recogniser URI, resolved from the agent or from the platform default; never absent. See TranscriptionUri. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
        - `languages` — array **(required)** — Every configured language, as candidates for identification.
          - _array of_ `string`
        - `preferredLanguage` — string **(required)** — The language the call starts in, resolved from the channel. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `autoDetect` — boolean **(required)** — Whether to identify the spoken language per utterance. Already clamped by the server — see the shape's documentation.
      - `backgroundSound` — string — Music-on-hold class the PBX should play under the call as ambient background. A BARE NAME, not the configuration object `VoiceBackgroundSoundSettings`: this is the RESOLVED outcome. The server has already applied `enabled` and the class default, so the PBX gets a name to play or nothing at all and needs no resolution rule of its own. TOP LEVEL, NOT INSIDE `speech`, because it is not recognition intent and must not inherit `speech`'s conditions: a call with no configured languages carries no `speech` payload and can still have background audio. ABSENT MEANS OFF, and absence is the only way to say it — there is no value for 'none'. A bot whose administrator never touched the setting sends nothing here, which is exactly what every call sent before it existed, so the PBX needs no new case. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
      - `inputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
        - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
        - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
        - `channels` — number — Channel count. Defaults to 1 (mono).
      - `outputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
        - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
        - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
        - `channels` — number — Channel count. Defaults to 1 (mono).
  - `sessionEndedWebsocketEvent` — SessionEndedWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
    - `type` — string **(required)** _(default=event)_
    - `event` — SessionEndedEvent **(required)** — Terminal server event: the session ended, optionally with an error.
      - `type` — object **(required)**
      - `reason` — string
      - `error` — string — Present when the session ended because of an error.
      - `time` — number **(required)**
  - `errorWebsocketEvent` — ErrorWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
    - `type` — string **(required)** _(default=event)_
    - `event` — VoiceErrorEvent **(required)** — An error surfaced on the connection. Non-terminal unless followed by a SessionEndedEvent.
      - `type` — object **(required)**
      - `code` — string **(required)** — Stable machine-readable error code.
      - `message` — string **(required)**
      - `time` — number **(required)**
  - `sayWebsocketCommand` — SayWebsocketCommand — Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`.
    - `type` — string **(required)** _(default=command)_
    - `command` — SayCommandData **(required)** — Play a reply to the caller. When `audio` is absent the client performs text-to-speech from `text`; when present the server streams synthesized `play` frames for this reply.
      - `text` — string **(required)**
      - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
      - `interruptible` — boolean — Whether the caller may barge in over this reply.
      - `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the agent's stored `VoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
      - `audio` — SayCommandAudioOptions — Audio-stream parameters when the server synthesizes the reply itself (TTS provider configured on the agent): the `say` is followed by a stream of `play` frames on this stream id.
        - `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
        - `sampleRate` — number **(required)**
      - `type` — object **(required)**
  - `playWebsocketCommand` — PlayWebsocketCommand — Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`.
    - `type` — string **(required)** _(default=command)_
    - `command` — PlayCommandData **(required)** — A chunk of synthesized reply audio to play. `data` is base64, PCM-encoded at the sample rate declared in the matching `say` command; an empty `data` marks the end of the stream.
      - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
      - `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
      - `data` — string **(required)**
      - `type` — object **(required)**
  - `stopWebsocketCommand` — StopWebsocketCommand — Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`.
    - `type` — string **(required)** _(default=command)_
    - `command` — StopCommandData **(required)**
      - `type` — object **(required)**
  - `hangupWebsocketCommand` — HangupWebsocketCommand — Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`.
    - `type` — string **(required)** _(default=command)_
    - `command` — HangupCommandData **(required)** — Terminate the session and hang up the call.
      - `reason` — string
      - `type` — object **(required)**
  - `transferWebsocketCommand` — TransferWebsocketCommand — Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`.
    - `type` — string **(required)** _(default=command)_
    - `command` — TransferCommandData **(required)** — Transfer the call to a PBX destination and terminate the session. Honoured on PBX clients.
      - `context` — string **(required)**
      - `extension` — string **(required)**
      - `type` — object **(required)**
  - `callEvent` — union — One event on a live call. The SSE frame's `event:` is the member name and `data:` this whole union document, so a frame reads `data: {"say": {...}}` — never the member's payload on its own.
    - _oneOf_ — exactly one of:
      - **`started`**
        - `started` — VoiceCallStartedEvent **(required)** — The session that answered the call, sent once per session of the call (a transfer starts another).
          - `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
          - `traceId` — string — The session's trace, for the LLM-level detail this stream deliberately omits. Absent for a built-in agent, whose trace is not the tenant's to read. _(minLen=1; maxLen=128)_
          - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
          - `agentName` — string
          - `agentVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
          - `agentDraft` — boolean — True when the session runs the agent's draft.
          - `language` — string — BCP-47 language the call started in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - **`transcription`**
        - `transcription` — VoiceCallTranscriptionEvent **(required)** — A recogniser result for the caller's speech. Interim results (`final: false`) are replaced by the final one with the same `id`.
          - `id` — string **(required)** — Identifier of a transcription chunk within a session.
          - `text` — string **(required)**
          - `final` — boolean **(required)**
          - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
          - `time` — number — Milliseconds since the call started, as the PBX stamps it.
      - **`agentTranscription`**
        - `agentTranscription` — VoiceCallAgentTranscriptionEvent **(required)** — A recogniser result for the AGENT's own leg — what the caller actually heard. Same semantics as VoiceCallTranscriptionEvent; an interrupted reply simply stops.
          - `id` — string **(required)** — Identifier of a transcription chunk within a session.
          - `text` — string **(required)**
          - `final` — boolean **(required)**
          - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
          - `time` — number
      - **`reply`**
        - `reply` — VoiceCallReplyEvent **(required)** — The caller's completed utterance that started a turn — after the runtime's filler and duplicate filter.
          - `id` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
          - `text` — string **(required)**
          - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - **`say`**
        - `say` — VoiceCallSayEvent **(required)** — One sentence the agent speaks, as it is handed to the PBX (after playback sanitizing). Sentences of one reply share `replyId`.
          - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
          - `text` — string **(required)**
          - `interruptible` — boolean **(required)**
      - **`playback`**
        - `playback` — VoiceCallPlaybackEvent **(required)** — The PBX finished (or abandoned) playing a reply.
          - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
          - `complete` — boolean **(required)**
      - **`interruption`**
        - `interruption` — VoiceCallInterruptionEvent **(required)** — The caller talked over the agent. `playedText` is what they heard before the cut.
          - `replyId` — string — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
          - `playedText` — string
          - `originalText` — string
      - **`language`**
        - `language` — VoiceCallLanguageEvent **(required)** — The conversation language changed on a recognised utterance.
          - `from` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
          - `to` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
          - `reason` — string **(required)**
      - **`tool`**
        - `tool` — VoiceCallToolEvent **(required)** — A tool call the agent made during a turn. Name and phase only — arguments and results live in the trace. Sent to a caller signed in to the system; never to a guest.
          - `toolCallId` — string **(required)** — Identifies the tool call inside the turn — the model's own call id, not the PBX call this stream follows.
          - `toolName` — string **(required)**
          - `phase` — string **(required)** _(enum: `started`, `finished`)_
          - `startMessage` — string — The phrase spoken while the tool runs, when the capability configures one.
      - **`ended`**
        - `ended` — VoiceCallEndedEvent **(required)** — The session ended. After `transfer` another session of the same call may follow with its own `started`.
          - `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
          - `reason` — string **(required)** _(enum: `hangup`, `transfer`, `timeout`, `error`, `complete`)_
- Errors: `400`, `403`

### Session

#### `POST` `/v2/voice/sessions/{sessionId}/hangup`

Terminates the voice session and the call.

- operationId: `SendHangup`
- **Scopes**: `wilma-voice:SendHangup`
- **Parameters**
  - `sessionId` (path) — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
- **Request body** (`application/json` — `SendHangupRequestContent`)
  - `reason` — string
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voice/sessions/{sessionId}/play`

Plays the specified audio chunk through the audio stream of the voice session.

- operationId: `SendPlay`
- **Scopes**: `wilma-voice:SendPlay`
- **Parameters**
  - `sessionId` (path) — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
- **Request body** (`application/json` — `SendPlayRequestContent`) **(required)**
  - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
  - `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
  - `data` — string **(required)**
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voice/sessions/{sessionId}/say`

Generates and plays the specified text through the audio stream of the voice session.

- operationId: `SendSay`
- **Scopes**: `wilma-voice:SendSay`
- **Parameters**
  - `sessionId` (path) — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
- **Request body** (`application/json` — `SendSayRequestContent`) **(required)**
  - `text` — string **(required)**
  - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
  - `interruptible` — boolean — Whether the caller may barge in over this reply.
  - `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the agent's stored `VoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
  - `audio` — SayCommandAudioOptions — Audio-stream parameters when the server synthesizes the reply itself (TTS provider configured on the agent): the `say` is followed by a stream of `play` frames on this stream id.
    - `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
    - `sampleRate` — number **(required)**
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voice/sessions/{sessionId}/stop`

Stops any audio currently being played by the voice session.

- operationId: `SendStop`
- **Scopes**: `wilma-voice:SendStop`
- **Parameters**
  - `sessionId` (path) — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voice/sessions/{sessionId}/transfer`

Transfers the call to the specified context and extension, and terminates the voice session.

- operationId: `SendTransfer`
- **Scopes**: `wilma-voice:SendTransfer`
- **Parameters**
  - `sessionId` (path) — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
- **Request body** (`application/json` — `SendTransferRequestContent`) **(required)**
  - `context` — string **(required)**
  - `extension` — string **(required)**
- Errors: `400`, `403`, `404`

### Speech

#### `POST` `/v2/voice/text-to-speech`

Synthesizes one phrase and returns MP3.

    NOT NAMED FOR THE PREVIEW IT SERVES. Auditioning an unsaved voice in the console is the first
    caller, but nothing about the operation is preview-specific — it is the platform's
    text-to-speech, reachable by anything holding the scope, and a name naming one caller's screen
    would have to be worked around by the second one.

    EVERYTHING TRAVELS IN THE REQUEST and the operation reads no stored record — not the agent, and
    no dictionary behind it. The settings being auditioned are unsaved form state, and the rules
    that apply are the ones on `pronunciations`, so what is heard here is what the call would say.

- operationId: `TextToSpeech`
- **Scopes**: `wilma-voice:TextToSpeech`
- **Request body** (`application/json` — `TextToSpeechRequestContent`) **(required)**
  - `voice` — string **(required)** — Voice to speak with, as the URI a call would use — provider, voice id, synthesis parameters and, for a company's own account, `apiKey=secrets:{secretId}`. Passing the call's own value is what keeps an audition from diverging from the call it is auditioning. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
  - `language` — string **(required)** — Language the phrase is in. Reaches the provider as the synthesis language, and is the language `pronunciations` was written for. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `text` — string **(required)** — Text to speak, BEFORE pronunciation rules are applied. _(minLen=1; maxLen=500)_
  - `pronunciations` — array — Rules to apply to `text`, applied SERVER-SIDE by the same helper the call path uses — never pre-applied by the caller, or the form reimplements a rule the server owns and can silently diverge from the call. Pass the language's own list to hear exactly what a call would say. _(maxItems=200)_
    - _array of_ `VoicePronunciation`
      - `phrase` — string **(required)** — The phrase as it appears in the text, e.g. 'Wildix'. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
      - `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA), e.g. 'Wil-dix'. _(maxLen=200)_
      - `encoding` — string — How the `as` member of a pronunciation rule is written. _(enum: `alias`, `ipa`)_
- **Response 200** (`TextToSpeechOutputPayload`)
  - string
- Errors: `400`, `403`

#### `GET` `/v2/voice/voices`

Lists the voices a synthesis provider offers, read from the provider's own API and cached per company, provider, credential and language. Answers a URI per voice, so a picker stores what it selected rather than composing one.

- operationId: `ListVoices`
- **Scopes**: `wilma-voice:ListVoices`, `wilma-voice:read`
- **Parameters**
  - `provider` (query) — string **(required)** — Provider whose catalog to read: 'elevenlabs', 'google', 'amazon_polly', 'soniox'. This is the scheme of the URIs answered on `voices`. _(pattern=^[a-z0-9][a-z0-9_-]*$; minLen=1; maxLen=32)_
  - `language` (query) — string — Server-side filter for language-bound providers: only voices whose language SET CONTAINS this code. Ignored for ElevenLabs, whose voices are not language bound. For Soniox it keeps the voices whose model speaks the language. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `credential` (query) — string — A reference to the company's own provider credential, so the picker lists that account's voices including cloned ones. Absent means the platform key. `secrets:{secretId}` ONLY, resolved under the CALLER's company — an id that does not resolve there is rejected. There is no form of this member that carries a key, which is what keeps a provider credential out of a URL on this stack: every one of them lives in `wilma-secrets`, and a reference in a query string is not a secret. A stored voice URI says the same thing the same way: its `apiKey` parameter is a reference, and `validateSpeech` refuses a literal key in one. _(pattern=^secrets:[a-zA-Z0-9_-]{1,64}$; minLen=9; maxLen=72)_
- **Response 200** (`ListVoicesResponseContent`)
  - `voices` — array **(required)**
    - _array of_ `Voice`
      - `uri` — string **(required)** — Voice URI, ready to store as `VoiceLanguage.voice` or send to TextToSpeech. Carries no parameters — the caller appends the synthesis parameters and, where applicable, the `apiKey=secrets:{secretId}` reference it wants. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `name` — string **(required)** — Display name as the provider publishes it, e.g. 'Rachel'. A member rather than part of `metadata` because it is the one thing every provider has and every picker shows.
      - `metadata` — any — The provider's own metadata for this voice, for rendering and filtering only. See VoiceMetadata.
- Errors: `400`, `403`

### Schemas appendix — Wilma Voice API

<details><summary>69 component schemas</summary>

**`AgentTranscriptionEvent`**

_A recogniser result for the agent's own leg — what the caller hears. Sent by the PBX for new-stack agents only, from the same dual-channel stream that transcribes the caller. Never starts a turn._

- `type` — object **(required)**
- `id` — string **(required)** — Identifier of a transcription chunk within a session.
- `text` — string **(required)**
- `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
- `final` — boolean — True when this is the final transcript for the utterance rather than an interim hypothesis. An absent value is read as final, as on `TranscriptionEvent`.
- `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only — it drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `time` — number **(required)**

**`AgentTranscriptionWebsocketEvent`**

_Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`._

- `type` — string **(required)** _(default=event)_
- `event` — AgentTranscriptionEvent **(required)** — A recogniser result for the agent's own leg — what the caller hears. Sent by the PBX for new-stack agents only, from the same dual-channel stream that transcribes the caller. Never starts a turn.
  - `type` — object **(required)**
  - `id` — string **(required)** — Identifier of a transcription chunk within a session.
  - `text` — string **(required)**
  - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
  - `final` — boolean — True when this is the final transcript for the utterance rather than an interim hypothesis. An absent value is read as final, as on `TranscriptionEvent`.
  - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only — it drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `time` — number **(required)**

**`AudioEvent`**

_A chunk of raw caller audio, base64-encoded in the session's negotiated input format (inputAudio from the connect handshake). Used by web/app clients in AUDIO input mode; the service buffers and transcribes it server-side. Not used in TRANSCRIPTION mode._

- `type` — object **(required)**
- `data` — string **(required)**
- `seq` — number — Optional monotonic chunk sequence number, for gap detection.

**`AudioWebsocketEvent`**

_Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`._

- `type` — string **(required)** _(default=event)_
- `event` — AudioEvent **(required)** — A chunk of raw caller audio, base64-encoded in the session's negotiated input format (inputAudio from the connect handshake). Used by web/app clients in AUDIO input mode; the service buffers and transcribes it server-side. Not used in TRANSCRIPTION mode.
  - `type` — object **(required)**
  - `data` — string **(required)**
  - `seq` — number — Optional monotonic chunk sequence number, for gap detection.

**`CompleteEvent`**

_The call/conversation completed (e.g. the caller hung up or the call was transferred away)._

- `type` — object **(required)**
- `reason` — string **(required)**
- `time` — number **(required)**

**`CompleteWebsocketEvent`**

_Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`._

- `type` — string **(required)** _(default=event)_
- `event` — CompleteEvent **(required)** — The call/conversation completed (e.g. the caller hung up or the call was transferred away).
  - `type` — object **(required)**
  - `reason` — string **(required)**
  - `time` — number **(required)**

**`ControlEvent`**

_A lightweight control frame from the client (AUDIO mode)._

- `type` — object **(required)**
- `action` — string **(required)** — A client control action on the audio input (AUDIO mode). _(enum: `end_of_turn`, `clear`, `keepalive`)_

**`ControlWebsocketEvent`**

_Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`._

- `type` — string **(required)** _(default=event)_
- `event` — ControlEvent **(required)** — A lightweight control frame from the client (AUDIO mode).
  - `type` — object **(required)**
  - `action` — string **(required)** — A client control action on the audio input (AUDIO mode). _(enum: `end_of_turn`, `clear`, `keepalive`)_

**`DescribeVoiceProtocolResponseContent`**

- `connectParams` — VoiceConnectParams — Parameters supplied on the WebSocket connect (upgrade) request, as query-string parameters.
  - `protocolVersion` — number — Protocol version advertised by the client (query parameter `v`). 0 (or absent) is the legacy PBX protocol; >= 1 enables the sessionStarted event; >= 2 additionally means the client WAITS for `started` before opening its recognition stream and honours the `speech` payload on it.
  - `sessionId` — string **(required)** — Caller-supplied session id, unique per connection. _(minLen=1; maxLen=128)_
  - `agentId` — string **(required)** — Agent to run on this session. _(minLen=12; maxLen=12)_
  - `agentVersion` — number — Published agent version to run. Mutually exclusive with agentDraft. When neither is set, the agent's deployment configuration selects the version. The PBX sends it only for a preview number (`<agentId>-vN`, WMS-27502); a customer call never carries it. _(min=1)_
  - `agentDraft` — boolean — Run the agent's current draft (for testing). Mutually exclusive with agentVersion.
  - `callId` — string — PBX call id, when the session is bridged to a call.
  - `flowIndex` — number — Leg of the PBX call inside `callId` (pbx-data-engine's flow index). Kept on the session as metadata beside `callId` and `dialedNumber`; never interpreted by the runtime.
  - `dialedNumber` — string — The number the caller dialled to reach the agent. Kept on the session as metadata beside `callId` and `flowIndex`.
  - `language` — string — BCP-47 language of the conversation, e.g. 'en-US'.
  - `callerName` — string
  - `callerNumber` — string
  - `callerEmail` — string
  - `callerCompany` — string
  - `voice` — string — Override the TTS voice for this session, as a voice URI, e.g. 'elevenlabs://<voiceId>?apiKey=...'. Defaults to the agent's configured voice.
  - `initialMessage` — string — First message spoken to the caller. Overrides the agent's configured greeting.
  - `variables` — string — Base64-encoded JSON object of agent variables for this session, e.g. base64('{"orderId":"123"}').
  - `inputMode` — string — How caller speech reaches the service. _(enum: `transcription`, `audio`)_
  - `inputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
    - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
    - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
    - `channels` — number — Channel count. Defaults to 1 (mono).
  - `outputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
    - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
    - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
    - `channels` — number — Channel count. Defaults to 1 (mono).
- `audioWebsocketEvent` — AudioWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
  - `type` — string **(required)** _(default=event)_
  - `event` — AudioEvent **(required)** — A chunk of raw caller audio, base64-encoded in the session's negotiated input format (inputAudio from the connect handshake). Used by web/app clients in AUDIO input mode; the service buffers and transcribes it server-side. Not used in TRANSCRIPTION mode.
    - `type` — object **(required)**
    - `data` — string **(required)**
    - `seq` — number — Optional monotonic chunk sequence number, for gap detection.
- `transcriptionWebsocketEvent` — TranscriptionWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
  - `type` — string **(required)** _(default=event)_
  - `event` — TranscriptionEvent **(required)** — A transcription chunk of caller speech, provided by a client that does its own speech-to-text (PBX / TRANSCRIPTION mode), or emitted by the service (AUDIO mode) and echoed to the client.
    - `type` — object **(required)**
    - `id` — string **(required)** — Identifier of a transcription chunk within a session.
    - `text` — string **(required)**
    - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
    - `final` — boolean — True when this is the final transcript for the utterance rather than an interim hypothesis. An absent value is read as final: a client that does not distinguish interim results sends none.
    - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only — it drives no behavior, so an operator can see what the recogniser thought during an utterance that never became a turn. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `time` — number **(required)**
- `agentTranscriptionWebsocketEvent` — AgentTranscriptionWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
  - `type` — string **(required)** _(default=event)_
  - `event` — AgentTranscriptionEvent **(required)** — A recogniser result for the agent's own leg — what the caller hears. Sent by the PBX for new-stack agents only, from the same dual-channel stream that transcribes the caller. Never starts a turn.
    - `type` — object **(required)**
    - `id` — string **(required)** — Identifier of a transcription chunk within a session.
    - `text` — string **(required)**
    - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
    - `final` — boolean — True when this is the final transcript for the utterance rather than an interim hypothesis. An absent value is read as final, as on `TranscriptionEvent`.
    - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only — it drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `time` — number **(required)**
- `replyWebsocketEvent` — ReplyWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
  - `type` — string **(required)** _(default=event)_
  - `event` — ReplyEvent **(required)** — A final caller phrase that should trigger an agent turn (PBX / TRANSCRIPTION mode).
    - `type` — object **(required)**
    - `id` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
    - `text` — string **(required)**
    - `language` — string — Language the recogniser identified for this completed utterance. THIS is the one that drives the language switch. When the recogniser reports several languages inside one utterance, the PBX sends the LAST labelled segment's language — it is the one the caller is speaking now. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
- `playbackWebsocketEvent` — PlaybackWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
  - `type` — string **(required)** _(default=event)_
  - `event` — PlaybackEvent **(required)** — Client-reported progress of an in-flight reply playback.
    - `type` — object **(required)**
    - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
    - `text` — string **(required)**
    - `complete` — boolean **(required)**
    - `startTime` — number **(required)**
    - `endTime` — number
- `interruptionWebsocketEvent` — InterruptionWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
  - `type` — string **(required)** _(default=event)_
  - `event` — InterruptionEvent **(required)** — The caller interrupted (barged in over) a reply that was being played.
    - `type` — object **(required)**
    - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
    - `playedText` — string **(required)** — Portion of the reply that had been played before the interruption.
    - `originalText` — string **(required)** — The full reply text that was being played.
    - `time` — number **(required)**
- `completeWebsocketEvent` — CompleteWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
  - `type` — string **(required)** _(default=event)_
  - `event` — CompleteEvent **(required)** — The call/conversation completed (e.g. the caller hung up or the call was transferred away).
    - `type` — object **(required)**
    - `reason` — string **(required)**
    - `time` — number **(required)**
- `controlWebsocketEvent` — ControlWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
  - `type` — string **(required)** _(default=event)_
  - `event` — ControlEvent **(required)** — A lightweight control frame from the client (AUDIO mode).
    - `type` — object **(required)**
    - `action` — string **(required)** — A client control action on the audio input (AUDIO mode). _(enum: `end_of_turn`, `clear`, `keepalive`)_
- `sessionStartedWebsocketEvent` — SessionStartedWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
  - `type` — string **(required)** _(default=event)_
  - `event` — SessionStartedEvent **(required)** — Emitted once right after the handshake to confirm the session and the agent it is bound to. Sent only when the client advertises protocol version >= 1.
    - `type` — object **(required)**
    - `time` — number **(required)**
    - `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
    - `agentId` — string **(required)** — Agent bound to the session. _(minLen=12; maxLen=12)_
    - `agentVersion` — number — Published agent version resolved at connect; absent when running the agent draft. _(min=1)_
    - `traceId` — string — Trace recording this voice session in wilma-traces — the caller's transcribed phrases, the model calls they drove and the tools the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace to follow a call while it is in progress. Sent once at handshake and stable for the connection: a call is one trace. A caller who redials gets a new session and therefore a new trace, since the trace is keyed on the session id supplied at connect. _(minLen=1; maxLen=128)_
    - `agentName` — string — Agent display name.
    - `category` — string — Agent category.
    - `groupId` — string — PBX group used for data ACL; empty when the agent is not assigned to a group.
    - `speech` — VoiceSpeechPayload — Recognition intent for the call, sent on `started` at protocolVersion >= 2. NOT recogniser parameters: the PBX translates it into its provider's API. Against Amazon Transcribe with autoDetect true that is identify-multiple-languages plus language-options and preferred-language; with autoDetect false, a single-language stream on preferredLanguage. Both members the server can get wrong are RESOLVED here rather than forwarded: `engine` is always concrete (an absent one would let the PBX apply a different default than the console built its language list for), and `autoDetect` is clamped to false whenever the language count is below the recogniser's minimum or the recogniser cannot identify languages at all (forwarding true with one candidate makes Amazon reject the stream outright — a dead call).
      - `engine` — string **(required)** — Concrete recogniser URI, resolved from the agent or from the platform default; never absent. See TranscriptionUri. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `languages` — array **(required)** — Every configured language, as candidates for identification.
        - _array of_ `string`
      - `preferredLanguage` — string **(required)** — The language the call starts in, resolved from the channel. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `autoDetect` — boolean **(required)** — Whether to identify the spoken language per utterance. Already clamped by the server — see the shape's documentation.
    - `backgroundSound` — string — Music-on-hold class the PBX should play under the call as ambient background. A BARE NAME, not the configuration object `VoiceBackgroundSoundSettings`: this is the RESOLVED outcome. The server has already applied `enabled` and the class default, so the PBX gets a name to play or nothing at all and needs no resolution rule of its own. TOP LEVEL, NOT INSIDE `speech`, because it is not recognition intent and must not inherit `speech`'s conditions: a call with no configured languages carries no `speech` payload and can still have background audio. ABSENT MEANS OFF, and absence is the only way to say it — there is no value for 'none'. A bot whose administrator never touched the setting sends nothing here, which is exactly what every call sent before it existed, so the PBX needs no new case. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `inputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
      - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
      - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
      - `channels` — number — Channel count. Defaults to 1 (mono).
    - `outputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
      - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
      - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
      - `channels` — number — Channel count. Defaults to 1 (mono).
- `sessionEndedWebsocketEvent` — SessionEndedWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
  - `type` — string **(required)** _(default=event)_
  - `event` — SessionEndedEvent **(required)** — Terminal server event: the session ended, optionally with an error.
    - `type` — object **(required)**
    - `reason` — string
    - `error` — string — Present when the session ended because of an error.
    - `time` — number **(required)**
- `errorWebsocketEvent` — ErrorWebsocketEvent — Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`.
  - `type` — string **(required)** _(default=event)_
  - `event` — VoiceErrorEvent **(required)** — An error surfaced on the connection. Non-terminal unless followed by a SessionEndedEvent.
    - `type` — object **(required)**
    - `code` — string **(required)** — Stable machine-readable error code.
    - `message` — string **(required)**
    - `time` — number **(required)**
- `sayWebsocketCommand` — SayWebsocketCommand — Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`.
  - `type` — string **(required)** _(default=command)_
  - `command` — SayCommandData **(required)** — Play a reply to the caller. When `audio` is absent the client performs text-to-speech from `text`; when present the server streams synthesized `play` frames for this reply.
    - `text` — string **(required)**
    - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
    - `interruptible` — boolean — Whether the caller may barge in over this reply.
    - `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the agent's stored `VoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
    - `audio` — SayCommandAudioOptions — Audio-stream parameters when the server synthesizes the reply itself (TTS provider configured on the agent): the `say` is followed by a stream of `play` frames on this stream id.
      - `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
      - `sampleRate` — number **(required)**
    - `type` — object **(required)**
- `playWebsocketCommand` — PlayWebsocketCommand — Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`.
  - `type` — string **(required)** _(default=command)_
  - `command` — PlayCommandData **(required)** — A chunk of synthesized reply audio to play. `data` is base64, PCM-encoded at the sample rate declared in the matching `say` command; an empty `data` marks the end of the stream.
    - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
    - `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
    - `data` — string **(required)**
    - `type` — object **(required)**
- `stopWebsocketCommand` — StopWebsocketCommand — Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`.
  - `type` — string **(required)** _(default=command)_
  - `command` — StopCommandData **(required)**
    - `type` — object **(required)**
- `hangupWebsocketCommand` — HangupWebsocketCommand — Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`.
  - `type` — string **(required)** _(default=command)_
  - `command` — HangupCommandData **(required)** — Terminate the session and hang up the call.
    - `reason` — string
    - `type` — object **(required)**
- `transferWebsocketCommand` — TransferWebsocketCommand — Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`.
  - `type` — string **(required)** _(default=command)_
  - `command` — TransferCommandData **(required)** — Transfer the call to a PBX destination and terminate the session. Honoured on PBX clients.
    - `context` — string **(required)**
    - `extension` — string **(required)**
    - `type` — object **(required)**
- `callEvent` — union — One event on a live call. The SSE frame's `event:` is the member name and `data:` this whole union document, so a frame reads `data: {"say": {...}}` — never the member's payload on its own.
  - _oneOf_ — exactly one of:
    - **`started`**
      - `started` — VoiceCallStartedEvent **(required)** — The session that answered the call, sent once per session of the call (a transfer starts another).
        - `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
        - `traceId` — string — The session's trace, for the LLM-level detail this stream deliberately omits. Absent for a built-in agent, whose trace is not the tenant's to read. _(minLen=1; maxLen=128)_
        - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
        - `agentName` — string
        - `agentVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
        - `agentDraft` — boolean — True when the session runs the agent's draft.
        - `language` — string — BCP-47 language the call started in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - **`transcription`**
      - `transcription` — VoiceCallTranscriptionEvent **(required)** — A recogniser result for the caller's speech. Interim results (`final: false`) are replaced by the final one with the same `id`.
        - `id` — string **(required)** — Identifier of a transcription chunk within a session.
        - `text` — string **(required)**
        - `final` — boolean **(required)**
        - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `time` — number — Milliseconds since the call started, as the PBX stamps it.
    - **`agentTranscription`**
      - `agentTranscription` — VoiceCallAgentTranscriptionEvent **(required)** — A recogniser result for the AGENT's own leg — what the caller actually heard. Same semantics as VoiceCallTranscriptionEvent; an interrupted reply simply stops.
        - `id` — string **(required)** — Identifier of a transcription chunk within a session.
        - `text` — string **(required)**
        - `final` — boolean **(required)**
        - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `time` — number
    - **`reply`**
      - `reply` — VoiceCallReplyEvent **(required)** — The caller's completed utterance that started a turn — after the runtime's filler and duplicate filter.
        - `id` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
        - `text` — string **(required)**
        - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - **`say`**
      - `say` — VoiceCallSayEvent **(required)** — One sentence the agent speaks, as it is handed to the PBX (after playback sanitizing). Sentences of one reply share `replyId`.
        - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
        - `text` — string **(required)**
        - `interruptible` — boolean **(required)**
    - **`playback`**
      - `playback` — VoiceCallPlaybackEvent **(required)** — The PBX finished (or abandoned) playing a reply.
        - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
        - `complete` — boolean **(required)**
    - **`interruption`**
      - `interruption` — VoiceCallInterruptionEvent **(required)** — The caller talked over the agent. `playedText` is what they heard before the cut.
        - `replyId` — string — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
        - `playedText` — string
        - `originalText` — string
    - **`language`**
      - `language` — VoiceCallLanguageEvent **(required)** — The conversation language changed on a recognised utterance.
        - `from` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `to` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `reason` — string **(required)**
    - **`tool`**
      - `tool` — VoiceCallToolEvent **(required)** — A tool call the agent made during a turn. Name and phase only — arguments and results live in the trace. Sent to a caller signed in to the system; never to a guest.
        - `toolCallId` — string **(required)** — Identifies the tool call inside the turn — the model's own call id, not the PBX call this stream follows.
        - `toolName` — string **(required)**
        - `phase` — string **(required)** _(enum: `started`, `finished`)_
        - `startMessage` — string — The phrase spoken while the tool runs, when the capability configures one.
    - **`ended`**
      - `ended` — VoiceCallEndedEvent **(required)** — The session ended. After `transfer` another session of the same call may follow with its own `started`.
        - `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
        - `reason` — string **(required)** _(enum: `hangup`, `transfer`, `timeout`, `error`, `complete`)_

**`ErrorWebsocketEvent`**

_Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`._

- `type` — string **(required)** _(default=event)_
- `event` — VoiceErrorEvent **(required)** — An error surfaced on the connection. Non-terminal unless followed by a SessionEndedEvent.
  - `type` — object **(required)**
  - `code` — string **(required)** — Stable machine-readable error code.
  - `message` — string **(required)**
  - `time` — number **(required)**

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`HangupCommandData`**

_Terminate the session and hang up the call._

- `reason` — string
- `type` — object **(required)**

**`HangupWebsocketCommand`**

_Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`._

- `type` — string **(required)** _(default=command)_
- `command` — HangupCommandData **(required)** — Terminate the session and hang up the call.
  - `reason` — string
  - `type` — object **(required)**

**`InterruptionEvent`**

_The caller interrupted (barged in over) a reply that was being played._

- `type` — object **(required)**
- `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
- `playedText` — string **(required)** — Portion of the reply that had been played before the interruption.
- `originalText` — string **(required)** — The full reply text that was being played.
- `time` — number **(required)**

**`InterruptionWebsocketEvent`**

_Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`._

- `type` — string **(required)** _(default=event)_
- `event` — InterruptionEvent **(required)** — The caller interrupted (barged in over) a reply that was being played.
  - `type` — object **(required)**
  - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
  - `playedText` — string **(required)** — Portion of the reply that had been played before the interruption.
  - `originalText` — string **(required)** — The full reply text that was being played.
  - `time` — number **(required)**

**`ListVoicesResponseContent`**

- `voices` — array **(required)**
  - _array of_ `Voice`
    - `uri` — string **(required)** — Voice URI, ready to store as `VoiceLanguage.voice` or send to TextToSpeech. Carries no parameters — the caller appends the synthesis parameters and, where applicable, the `apiKey=secrets:{secretId}` reference it wants. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `name` — string **(required)** — Display name as the provider publishes it, e.g. 'Rachel'. A member rather than part of `metadata` because it is the one thing every provider has and every picker shows.
    - `metadata` — any — The provider's own metadata for this voice, for rendering and filtering only. See VoiceMetadata.

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`PlayCommandData`**

_A chunk of synthesized reply audio to play. `data` is base64, PCM-encoded at the sample rate declared in the matching `say` command; an empty `data` marks the end of the stream._

- `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
- `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
- `data` — string **(required)**
- `type` — object **(required)**

**`PlayWebsocketCommand`**

_Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`._

- `type` — string **(required)** _(default=command)_
- `command` — PlayCommandData **(required)** — A chunk of synthesized reply audio to play. `data` is base64, PCM-encoded at the sample rate declared in the matching `say` command; an empty `data` marks the end of the stream.
  - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
  - `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
  - `data` — string **(required)**
  - `type` — object **(required)**

**`PlaybackEvent`**

_Client-reported progress of an in-flight reply playback._

- `type` — object **(required)**
- `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
- `text` — string **(required)**
- `complete` — boolean **(required)**
- `startTime` — number **(required)**
- `endTime` — number

**`PlaybackWebsocketEvent`**

_Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`._

- `type` — string **(required)** _(default=event)_
- `event` — PlaybackEvent **(required)** — Client-reported progress of an in-flight reply playback.
  - `type` — object **(required)**
  - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
  - `text` — string **(required)**
  - `complete` — boolean **(required)**
  - `startTime` — number **(required)**
  - `endTime` — number

**`ReplyEvent`**

_A final caller phrase that should trigger an agent turn (PBX / TRANSCRIPTION mode)._

- `type` — object **(required)**
- `id` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
- `text` — string **(required)**
- `language` — string — Language the recogniser identified for this completed utterance. THIS is the one that drives the language switch. When the recogniser reports several languages inside one utterance, the PBX sends the LAST labelled segment's language — it is the one the caller is speaking now. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `startTime` — number **(required)**
- `endTime` — number **(required)**

**`ReplyWebsocketEvent`**

_Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`._

- `type` — string **(required)** _(default=event)_
- `event` — ReplyEvent **(required)** — A final caller phrase that should trigger an agent turn (PBX / TRANSCRIPTION mode).
  - `type` — object **(required)**
  - `id` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
  - `text` — string **(required)**
  - `language` — string — Language the recogniser identified for this completed utterance. THIS is the one that drives the language switch. When the recogniser reports several languages inside one utterance, the PBX sends the LAST labelled segment's language — it is the one the caller is speaking now. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**

**`SayCommandAudioOptions`**

_Audio-stream parameters when the server synthesizes the reply itself (TTS provider configured on the agent): the `say` is followed by a stream of `play` frames on this stream id._

- `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
- `sampleRate` — number **(required)**

**`SayCommandData`**

_Play a reply to the caller. When `audio` is absent the client performs text-to-speech from `text`; when present the server streams synthesized `play` frames for this reply._

- `text` — string **(required)**
- `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
- `interruptible` — boolean — Whether the caller may barge in over this reply.
- `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the agent's stored `VoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
- `audio` — SayCommandAudioOptions — Audio-stream parameters when the server synthesizes the reply itself (TTS provider configured on the agent): the `say` is followed by a stream of `play` frames on this stream id.
  - `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
  - `sampleRate` — number **(required)**
- `type` — object **(required)**

**`SayWebsocketCommand`**

_Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`._

- `type` — string **(required)** _(default=command)_
- `command` — SayCommandData **(required)** — Play a reply to the caller. When `audio` is absent the client performs text-to-speech from `text`; when present the server streams synthesized `play` frames for this reply.
  - `text` — string **(required)**
  - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
  - `interruptible` — boolean — Whether the caller may barge in over this reply.
  - `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the agent's stored `VoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
  - `audio` — SayCommandAudioOptions — Audio-stream parameters when the server synthesizes the reply itself (TTS provider configured on the agent): the `say` is followed by a stream of `play` frames on this stream id.
    - `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
    - `sampleRate` — number **(required)**
  - `type` — object **(required)**

**`SendHangupRequestContent`**

_Terminate the session and hang up the call._

- `reason` — string

**`SendPlayRequestContent`**

_A chunk of synthesized reply audio to play. `data` is base64, PCM-encoded at the sample rate declared in the matching `say` command; an empty `data` marks the end of the stream._

- `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
- `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
- `data` — string **(required)**

**`SendSayRequestContent`**

_Play a reply to the caller. When `audio` is absent the client performs text-to-speech from `text`; when present the server streams synthesized `play` frames for this reply._

- `text` — string **(required)**
- `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
- `interruptible` — boolean — Whether the caller may barge in over this reply.
- `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the agent's stored `VoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
- `audio` — SayCommandAudioOptions — Audio-stream parameters when the server synthesizes the reply itself (TTS provider configured on the agent): the `say` is followed by a stream of `play` frames on this stream id.
  - `streamId` — string **(required)** — Identifies one synthesized audio stream within a session; carried by a `say` command and the `play` frames that render it.
  - `sampleRate` — number **(required)**

**`SendTransferRequestContent`**

_Transfer the call to a PBX destination and terminate the session. Honoured on PBX clients._

- `context` — string **(required)**
- `extension` — string **(required)**

**`SessionEndedEvent`**

_Terminal server event: the session ended, optionally with an error._

- `type` — object **(required)**
- `reason` — string
- `error` — string — Present when the session ended because of an error.
- `time` — number **(required)**

**`SessionEndedWebsocketEvent`**

_Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`._

- `type` — string **(required)** _(default=event)_
- `event` — SessionEndedEvent **(required)** — Terminal server event: the session ended, optionally with an error.
  - `type` — object **(required)**
  - `reason` — string
  - `error` — string — Present when the session ended because of an error.
  - `time` — number **(required)**

**`SessionStartedEvent`**

_Emitted once right after the handshake to confirm the session and the agent it is bound to. Sent only when the client advertises protocol version >= 1._

- `type` — object **(required)**
- `time` — number **(required)**
- `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
- `agentId` — string **(required)** — Agent bound to the session. _(minLen=12; maxLen=12)_
- `agentVersion` — number — Published agent version resolved at connect; absent when running the agent draft. _(min=1)_
- `traceId` — string — Trace recording this voice session in wilma-traces — the caller's transcribed phrases, the model calls they drove and the tools the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace to follow a call while it is in progress. Sent once at handshake and stable for the connection: a call is one trace. A caller who redials gets a new session and therefore a new trace, since the trace is keyed on the session id supplied at connect. _(minLen=1; maxLen=128)_
- `agentName` — string — Agent display name.
- `category` — string — Agent category.
- `groupId` — string — PBX group used for data ACL; empty when the agent is not assigned to a group.
- `speech` — VoiceSpeechPayload — Recognition intent for the call, sent on `started` at protocolVersion >= 2. NOT recogniser parameters: the PBX translates it into its provider's API. Against Amazon Transcribe with autoDetect true that is identify-multiple-languages plus language-options and preferred-language; with autoDetect false, a single-language stream on preferredLanguage. Both members the server can get wrong are RESOLVED here rather than forwarded: `engine` is always concrete (an absent one would let the PBX apply a different default than the console built its language list for), and `autoDetect` is clamped to false whenever the language count is below the recogniser's minimum or the recogniser cannot identify languages at all (forwarding true with one candidate makes Amazon reject the stream outright — a dead call).
  - `engine` — string **(required)** — Concrete recogniser URI, resolved from the agent or from the platform default; never absent. See TranscriptionUri. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
  - `languages` — array **(required)** — Every configured language, as candidates for identification.
    - _array of_ `string`
  - `preferredLanguage` — string **(required)** — The language the call starts in, resolved from the channel. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `autoDetect` — boolean **(required)** — Whether to identify the spoken language per utterance. Already clamped by the server — see the shape's documentation.
- `backgroundSound` — string — Music-on-hold class the PBX should play under the call as ambient background. A BARE NAME, not the configuration object `VoiceBackgroundSoundSettings`: this is the RESOLVED outcome. The server has already applied `enabled` and the class default, so the PBX gets a name to play or nothing at all and needs no resolution rule of its own. TOP LEVEL, NOT INSIDE `speech`, because it is not recognition intent and must not inherit `speech`'s conditions: a call with no configured languages carries no `speech` payload and can still have background audio. ABSENT MEANS OFF, and absence is the only way to say it — there is no value for 'none'. A bot whose administrator never touched the setting sends nothing here, which is exactly what every call sent before it existed, so the PBX needs no new case. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
- `inputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
  - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
  - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
  - `channels` — number — Channel count. Defaults to 1 (mono).
- `outputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
  - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
  - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
  - `channels` — number — Channel count. Defaults to 1 (mono).

**`SessionStartedWebsocketEvent`**

_Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`._

- `type` — string **(required)** _(default=event)_
- `event` — SessionStartedEvent **(required)** — Emitted once right after the handshake to confirm the session and the agent it is bound to. Sent only when the client advertises protocol version >= 1.
  - `type` — object **(required)**
  - `time` — number **(required)**
  - `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
  - `agentId` — string **(required)** — Agent bound to the session. _(minLen=12; maxLen=12)_
  - `agentVersion` — number — Published agent version resolved at connect; absent when running the agent draft. _(min=1)_
  - `traceId` — string — Trace recording this voice session in wilma-traces — the caller's transcribed phrases, the model calls they drove and the tools the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace to follow a call while it is in progress. Sent once at handshake and stable for the connection: a call is one trace. A caller who redials gets a new session and therefore a new trace, since the trace is keyed on the session id supplied at connect. _(minLen=1; maxLen=128)_
  - `agentName` — string — Agent display name.
  - `category` — string — Agent category.
  - `groupId` — string — PBX group used for data ACL; empty when the agent is not assigned to a group.
  - `speech` — VoiceSpeechPayload — Recognition intent for the call, sent on `started` at protocolVersion >= 2. NOT recogniser parameters: the PBX translates it into its provider's API. Against Amazon Transcribe with autoDetect true that is identify-multiple-languages plus language-options and preferred-language; with autoDetect false, a single-language stream on preferredLanguage. Both members the server can get wrong are RESOLVED here rather than forwarded: `engine` is always concrete (an absent one would let the PBX apply a different default than the console built its language list for), and `autoDetect` is clamped to false whenever the language count is below the recogniser's minimum or the recogniser cannot identify languages at all (forwarding true with one candidate makes Amazon reject the stream outright — a dead call).
    - `engine` — string **(required)** — Concrete recogniser URI, resolved from the agent or from the platform default; never absent. See TranscriptionUri. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `languages` — array **(required)** — Every configured language, as candidates for identification.
      - _array of_ `string`
    - `preferredLanguage` — string **(required)** — The language the call starts in, resolved from the channel. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `autoDetect` — boolean **(required)** — Whether to identify the spoken language per utterance. Already clamped by the server — see the shape's documentation.
  - `backgroundSound` — string — Music-on-hold class the PBX should play under the call as ambient background. A BARE NAME, not the configuration object `VoiceBackgroundSoundSettings`: this is the RESOLVED outcome. The server has already applied `enabled` and the class default, so the PBX gets a name to play or nothing at all and needs no resolution rule of its own. TOP LEVEL, NOT INSIDE `speech`, because it is not recognition intent and must not inherit `speech`'s conditions: a call with no configured languages carries no `speech` payload and can still have background audio. ABSENT MEANS OFF, and absence is the only way to say it — there is no value for 'none'. A bot whose administrator never touched the setting sends nothing here, which is exactly what every call sent before it existed, so the PBX needs no new case. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
  - `inputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
    - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
    - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
    - `channels` — number — Channel count. Defaults to 1 (mono).
  - `outputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
    - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
    - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
    - `channels` — number — Channel count. Defaults to 1 (mono).

**`StopCommandData`**

- `type` — object **(required)**

**`StopWebsocketCommand`**

_Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`._

- `type` — string **(required)** _(default=command)_
- `command` — StopCommandData **(required)**
  - `type` — object **(required)**

**`StreamCallEventsOutputPayload`**

_Raw Server-Sent Events byte stream (`text/event-stream`). Each frame carries one VoiceCallEvent: `id:` is a per-connection counter (there is no replay), `event:` the union member name, `data:` the JSON document of the union value, e.g. `{"say": {...}}`._

- string

**`TextToSpeechOutputPayload`**

_The call path streams raw PCM to the PBX; this returns MP3 so a browser <audio> element plays it with no client-side decoding._

- string

**`TextToSpeechRequestContent`**

- `voice` — string **(required)** — Voice to speak with, as the URI a call would use — provider, voice id, synthesis parameters and, for a company's own account, `apiKey=secrets:{secretId}`. Passing the call's own value is what keeps an audition from diverging from the call it is auditioning. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `language` — string **(required)** — Language the phrase is in. Reaches the provider as the synthesis language, and is the language `pronunciations` was written for. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `text` — string **(required)** — Text to speak, BEFORE pronunciation rules are applied. _(minLen=1; maxLen=500)_
- `pronunciations` — array — Rules to apply to `text`, applied SERVER-SIDE by the same helper the call path uses — never pre-applied by the caller, or the form reimplements a rule the server owns and can silently diverge from the call. Pass the language's own list to hear exactly what a call would say. _(maxItems=200)_
  - _array of_ `VoicePronunciation`
    - `phrase` — string **(required)** — The phrase as it appears in the text, e.g. 'Wildix'. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
    - `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA), e.g. 'Wil-dix'. _(maxLen=200)_
    - `encoding` — string — How the `as` member of a pronunciation rule is written. _(enum: `alias`, `ipa`)_

**`TranscriptionEvent`**

_A transcription chunk of caller speech, provided by a client that does its own speech-to-text (PBX / TRANSCRIPTION mode), or emitted by the service (AUDIO mode) and echoed to the client._

- `type` — object **(required)**
- `id` — string **(required)** — Identifier of a transcription chunk within a session.
- `text` — string **(required)**
- `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
- `final` — boolean — True when this is the final transcript for the utterance rather than an interim hypothesis. An absent value is read as final: a client that does not distinguish interim results sends none.
- `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only — it drives no behavior, so an operator can see what the recogniser thought during an utterance that never became a turn. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `time` — number **(required)**

**`TranscriptionWebsocketEvent`**

_Envelope of a WebSocket event frame: `{ "type": "event", "event": { ... } }`._

- `type` — string **(required)** _(default=event)_
- `event` — TranscriptionEvent **(required)** — A transcription chunk of caller speech, provided by a client that does its own speech-to-text (PBX / TRANSCRIPTION mode), or emitted by the service (AUDIO mode) and echoed to the client.
  - `type` — object **(required)**
  - `id` — string **(required)** — Identifier of a transcription chunk within a session.
  - `text` — string **(required)**
  - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
  - `final` — boolean — True when this is the final transcript for the utterance rather than an interim hypothesis. An absent value is read as final: a client that does not distinguish interim results sends none.
  - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only — it drives no behavior, so an operator can see what the recogniser thought during an utterance that never became a turn. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `time` — number **(required)**

**`TransferCommandData`**

_Transfer the call to a PBX destination and terminate the session. Honoured on PBX clients._

- `context` — string **(required)**
- `extension` — string **(required)**
- `type` — object **(required)**

**`TransferWebsocketCommand`**

_Envelope of a WebSocket command frame: `{ "type": "command", "command": { ... } }`._

- `type` — string **(required)** _(default=command)_
- `command` — TransferCommandData **(required)** — Transfer the call to a PBX destination and terminate the session. Honoured on PBX clients.
  - `context` — string **(required)**
  - `extension` — string **(required)**
  - `type` — object **(required)**

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`Voice`**

_One voice a provider offers: the URI to store it by, a name to show, and the provider's own metadata. `uri` IS THE RESULT. It is exactly what goes into `VoiceLanguage.voice`, so a form stores what it was given instead of assembling a string out of a provider name and an id — the one place a client could get the convention wrong._

- `uri` — string **(required)** — Voice URI, ready to store as `VoiceLanguage.voice` or send to TextToSpeech. Carries no parameters — the caller appends the synthesis parameters and, where applicable, the `apiKey=secrets:{secretId}` reference it wants. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `name` — string **(required)** — Display name as the provider publishes it, e.g. 'Rachel'. A member rather than part of `metadata` because it is the one thing every provider has and every picker shows.
- `metadata` — any — The provider's own metadata for this voice, for rendering and filtering only. See VoiceMetadata.

**`VoiceAudioEncoding`**

_Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames)._

- string _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_

**`VoiceAudioFormat`**

_A PCM/compressed audio format description._

- `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
- `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
- `channels` — number — Channel count. Defaults to 1 (mono).

**`VoiceCallAgentTranscriptionEvent`**

_A recogniser result for the AGENT's own leg — what the caller actually heard. Same semantics as VoiceCallTranscriptionEvent; an interrupted reply simply stops._

- `id` — string **(required)** — Identifier of a transcription chunk within a session.
- `text` — string **(required)**
- `final` — boolean **(required)**
- `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `time` — number

**`VoiceCallEndReason`**

- string _(enum: `hangup`, `transfer`, `timeout`, `error`, `complete`)_

**`VoiceCallEndedEvent`**

_The session ended. After `transfer` another session of the same call may follow with its own `started`._

- `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
- `reason` — string **(required)** _(enum: `hangup`, `transfer`, `timeout`, `error`, `complete`)_

**`VoiceCallEvent`**

_One event on a live call. The SSE frame's `event:` is the member name and `data:` this whole union document, so a frame reads `data: {"say": {...}}` — never the member's payload on its own._

- _oneOf_ — exactly one of:
  - **`started`**
    - `started` — VoiceCallStartedEvent **(required)** — The session that answered the call, sent once per session of the call (a transfer starts another).
      - `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
      - `traceId` — string — The session's trace, for the LLM-level detail this stream deliberately omits. Absent for a built-in agent, whose trace is not the tenant's to read. _(minLen=1; maxLen=128)_
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `agentName` — string
      - `agentVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `agentDraft` — boolean — True when the session runs the agent's draft.
      - `language` — string — BCP-47 language the call started in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - **`transcription`**
    - `transcription` — VoiceCallTranscriptionEvent **(required)** — A recogniser result for the caller's speech. Interim results (`final: false`) are replaced by the final one with the same `id`.
      - `id` — string **(required)** — Identifier of a transcription chunk within a session.
      - `text` — string **(required)**
      - `final` — boolean **(required)**
      - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `time` — number — Milliseconds since the call started, as the PBX stamps it.
  - **`agentTranscription`**
    - `agentTranscription` — VoiceCallAgentTranscriptionEvent **(required)** — A recogniser result for the AGENT's own leg — what the caller actually heard. Same semantics as VoiceCallTranscriptionEvent; an interrupted reply simply stops.
      - `id` — string **(required)** — Identifier of a transcription chunk within a session.
      - `text` — string **(required)**
      - `final` — boolean **(required)**
      - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `time` — number
  - **`reply`**
    - `reply` — VoiceCallReplyEvent **(required)** — The caller's completed utterance that started a turn — after the runtime's filler and duplicate filter.
      - `id` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
      - `text` — string **(required)**
      - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - **`say`**
    - `say` — VoiceCallSayEvent **(required)** — One sentence the agent speaks, as it is handed to the PBX (after playback sanitizing). Sentences of one reply share `replyId`.
      - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
      - `text` — string **(required)**
      - `interruptible` — boolean **(required)**
  - **`playback`**
    - `playback` — VoiceCallPlaybackEvent **(required)** — The PBX finished (or abandoned) playing a reply.
      - `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
      - `complete` — boolean **(required)**
  - **`interruption`**
    - `interruption` — VoiceCallInterruptionEvent **(required)** — The caller talked over the agent. `playedText` is what they heard before the cut.
      - `replyId` — string — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
      - `playedText` — string
      - `originalText` — string
  - **`language`**
    - `language` — VoiceCallLanguageEvent **(required)** — The conversation language changed on a recognised utterance.
      - `from` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `to` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `reason` — string **(required)**
  - **`tool`**
    - `tool` — VoiceCallToolEvent **(required)** — A tool call the agent made during a turn. Name and phase only — arguments and results live in the trace. Sent to a caller signed in to the system; never to a guest.
      - `toolCallId` — string **(required)** — Identifies the tool call inside the turn — the model's own call id, not the PBX call this stream follows.
      - `toolName` — string **(required)**
      - `phase` — string **(required)** _(enum: `started`, `finished`)_
      - `startMessage` — string — The phrase spoken while the tool runs, when the capability configures one.
  - **`ended`**
    - `ended` — VoiceCallEndedEvent **(required)** — The session ended. After `transfer` another session of the same call may follow with its own `started`.
      - `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
      - `reason` — string **(required)** _(enum: `hangup`, `transfer`, `timeout`, `error`, `complete`)_

**`VoiceCallInterruptionEvent`**

_The caller talked over the agent. `playedText` is what they heard before the cut._

- `replyId` — string — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
- `playedText` — string
- `originalText` — string

**`VoiceCallLanguageEvent`**

_The conversation language changed on a recognised utterance._

- `from` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `to` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `reason` — string **(required)**

**`VoiceCallPlaybackEvent`**

_The PBX finished (or abandoned) playing a reply._

- `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
- `complete` — boolean **(required)**

**`VoiceCallReplyEvent`**

_The caller's completed utterance that started a turn — after the runtime's filler and duplicate filter._

- `id` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
- `text` — string **(required)**
- `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_

**`VoiceCallSayEvent`**

_One sentence the agent speaks, as it is handed to the PBX (after playback sanitizing). Sentences of one reply share `replyId`._

- `replyId` — string **(required)** — Correlates a caller phrase, the agent reply it produced, and the playback/interruption of that reply.
- `text` — string **(required)**
- `interruptible` — boolean **(required)**

**`VoiceCallStartedEvent`**

_The session that answered the call, sent once per session of the call (a transfer starts another)._

- `sessionId` — string **(required)** — Caller-facing voice session identifier, unique per connection. Supplied by the client at connect (the PBX call/session id, or a client-generated id for web sessions). _(minLen=1; maxLen=128)_
- `traceId` — string — The session's trace, for the LLM-level detail this stream deliberately omits. Absent for a built-in agent, whose trace is not the tenant's to read. _(minLen=1; maxLen=128)_
- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `agentName` — string
- `agentVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
- `agentDraft` — boolean — True when the session runs the agent's draft.
- `language` — string — BCP-47 language the call started in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_

**`VoiceCallToolEvent`**

_A tool call the agent made during a turn. Name and phase only — arguments and results live in the trace. Sent to a caller signed in to the system; never to a guest._

- `toolCallId` — string **(required)** — Identifies the tool call inside the turn — the model's own call id, not the PBX call this stream follows.
- `toolName` — string **(required)**
- `phase` — string **(required)** _(enum: `started`, `finished`)_
- `startMessage` — string — The phrase spoken while the tool runs, when the capability configures one.

**`VoiceCallToolPhase`**

- string _(enum: `started`, `finished`)_

**`VoiceCallTranscriptionEvent`**

_A recogniser result for the caller's speech. Interim results (`final: false`) are replaced by the final one with the same `id`._

- `id` — string **(required)** — Identifier of a transcription chunk within a session.
- `text` — string **(required)**
- `final` — boolean **(required)**
- `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `time` — number — Milliseconds since the call started, as the PBX stamps it.

**`VoiceCommandType`**

_Discriminator for the inner payload of a `command` frame._

- string _(enum: `say`, `play`, `stop`, `hangup`, `transfer`)_

**`VoiceConnectParams`**

_Parameters supplied on the WebSocket connect (upgrade) request, as query-string parameters._

- `protocolVersion` — number — Protocol version advertised by the client (query parameter `v`). 0 (or absent) is the legacy PBX protocol; >= 1 enables the sessionStarted event; >= 2 additionally means the client WAITS for `started` before opening its recognition stream and honours the `speech` payload on it.
- `sessionId` — string **(required)** — Caller-supplied session id, unique per connection. _(minLen=1; maxLen=128)_
- `agentId` — string **(required)** — Agent to run on this session. _(minLen=12; maxLen=12)_
- `agentVersion` — number — Published agent version to run. Mutually exclusive with agentDraft. When neither is set, the agent's deployment configuration selects the version. The PBX sends it only for a preview number (`<agentId>-vN`, WMS-27502); a customer call never carries it. _(min=1)_
- `agentDraft` — boolean — Run the agent's current draft (for testing). Mutually exclusive with agentVersion.
- `callId` — string — PBX call id, when the session is bridged to a call.
- `flowIndex` — number — Leg of the PBX call inside `callId` (pbx-data-engine's flow index). Kept on the session as metadata beside `callId` and `dialedNumber`; never interpreted by the runtime.
- `dialedNumber` — string — The number the caller dialled to reach the agent. Kept on the session as metadata beside `callId` and `flowIndex`.
- `language` — string — BCP-47 language of the conversation, e.g. 'en-US'.
- `callerName` — string
- `callerNumber` — string
- `callerEmail` — string
- `callerCompany` — string
- `voice` — string — Override the TTS voice for this session, as a voice URI, e.g. 'elevenlabs://<voiceId>?apiKey=...'. Defaults to the agent's configured voice.
- `initialMessage` — string — First message spoken to the caller. Overrides the agent's configured greeting.
- `variables` — string — Base64-encoded JSON object of agent variables for this session, e.g. base64('{"orderId":"123"}').
- `inputMode` — string — How caller speech reaches the service. _(enum: `transcription`, `audio`)_
- `inputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
  - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
  - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
  - `channels` — number — Channel count. Defaults to 1 (mono).
- `outputAudio` — VoiceAudioFormat — A PCM/compressed audio format description.
  - `encoding` — string **(required)** — Encoding of raw audio carried over the connection (client `audio` chunks and server `play` frames). _(enum: `pcm_s16le`, `mulaw`, `alaw`, `opus`)_
  - `sampleRate` — number **(required)** — Samples per second, e.g. 8000, 16000 or 24000.
  - `channels` — number — Channel count. Defaults to 1 (mono).

**`VoiceControlAction`**

_A client control action on the audio input (AUDIO mode)._

- string _(enum: `end_of_turn`, `clear`, `keepalive`)_

**`VoiceErrorEvent`**

_An error surfaced on the connection. Non-terminal unless followed by a SessionEndedEvent._

- `type` — object **(required)**
- `code` — string **(required)** — Stable machine-readable error code.
- `message` — string **(required)**
- `time` — number **(required)**

**`VoiceEventType`**

_Discriminator for the inner payload of an `event` frame._

- string _(enum: `started`, `ended`, `error`, `audio`, `transcription`, `agentTranscription`, `reply`, `playback`, `interruption`, `complete`, `control`)_

**`VoiceInputMode`**

_How caller speech reaches the service._

- string _(enum: `transcription`, `audio`)_

**`VoicePronunciation`**

_A pronunciation rule for one phrase. Belongs to a LANGUAGE, not to the agent: 'Wildix' is respelled differently for an Italian and a German voice, so one list shared ACROSS languages would fight itself. That is why the rules hang off the language and nowhere else — there is no company-wide dictionary above them to inherit from, or to disagree with._

- `phrase` — string **(required)** — The phrase as it appears in the text, e.g. 'Wildix'. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
- `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA), e.g. 'Wil-dix'. _(maxLen=200)_
- `encoding` — string — How the `as` member of a pronunciation rule is written. _(enum: `alias`, `ipa`)_

**`VoicePronunciationEncoding`**

_How the `as` member of a pronunciation rule is written._

- string _(enum: `alias`, `ipa`)_

**`VoiceSpeechPayload`**

_Recognition intent for the call, sent on `started` at protocolVersion >= 2. NOT recogniser parameters: the PBX translates it into its provider's API. Against Amazon Transcribe with autoDetect true that is identify-multiple-languages plus language-options and preferred-language; with autoDetect false, a single-language stream on preferredLanguage. Both members the server can get wrong are RESOLVED here rather than forwarded: `engine` is always concrete (an absent one would let the PBX apply a different default than the console built its language list for), and `autoDetect` is clamped to false whenever the language count is below the recogniser's minimum or the recogniser cannot identify languages at all (forwarding true with one candidate makes Amazon reject the stream outright — a dead call)._

- `engine` — string **(required)** — Concrete recogniser URI, resolved from the agent or from the platform default; never absent. See TranscriptionUri. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `languages` — array **(required)** — Every configured language, as candidates for identification.
  - _array of_ `string`
- `preferredLanguage` — string **(required)** — The language the call starts in, resolved from the channel. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `autoDetect` — boolean **(required)** — Whether to identify the spoken language per utterance. Already clamped by the server — see the shape's documentation.

</details>
