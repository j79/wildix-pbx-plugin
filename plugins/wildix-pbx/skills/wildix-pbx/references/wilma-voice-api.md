## Wilma Voice API

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

Describes the messages of the voice protocols: the text socket `/v2/voice/ws`, the call socket `/v2/voice/calls/ws` and the call events stream `StreamCallEvents`. Utility method; the generated shapes are the source of truth for building a client or a server by hand.

- operationId: `DescribeVoiceProtocol`
- **Scopes**: `wilma-voice:DescribeVoiceProtocol`, `wilma-voice:read`
- **Response 200** (`DescribeVoiceProtocolResponseContent`)
  - `textSocket` — VoiceTextProtocolFrames — The connect parameters and the messages of the text socket `/v2/voice/ws`.
    - `connectParams` — VoiceConnectParams — Parameters supplied on the WebSocket connect (upgrade) request, as query-string parameters.
      - `protocolVersion` — number — Protocol version advertised by the client (query parameter `v`). 0 (or absent) is the legacy PBX protocol; >= 1 enables the sessionStarted event; >= 2 additionally means the client WAITS for `started` before opening its recognition stream and honours the `speech` payload on it; >= 3 additionally means the client connects again with `resume` after close code `1001`, so the service can move the call to another server while it runs.
      - `sessionId` — string **(required)** — Caller-supplied session id, unique per connection. _(minLen=1; maxLen=128)_
      - `resume` — boolean — True when this connection attaches the running session `sessionId` again, after a close with close code `1001` or a lost connection. The session keeps its history and does not play the greeting again.
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
      - `inputMode` — string — How caller speech reaches the service. _(enum: `transcription`)_
      - `user` — string — Owner user of the session. Absent: no user. The service ignores it for a PBX token with `callId`. _(minLen=12; maxLen=12)_
      - `company` — string — Tenant of the session. Required for a service token, which carries no tenant. For another token a value different from the token tenant gets HTTP 401. _(minLen=3; maxLen=30)_
    - `client` — VoiceTextClientFrames — One example of each message that the client sends on the text socket. An event goes in `{"type": "event", "event": {...}}`; `healthcheck` has no envelope.
      - `healthcheck` — VoiceHealthcheckCommand — Liveness check of the service by the client: `{"type": "healthcheck"}`, with no envelope. The service sends no answer.
        - `type` — string **(required)** _(default=healthcheck)_
      - `transcription` — VoiceTranscriptionEvent — A transcription chunk of caller speech. A client that does its own speech-to-text sends it. When the service does the speech-to-text, the service sends it to the client.
        - `type` — object **(required)**
        - `id` — string — Id of the utterance. The interim chunks and the final chunk of one utterance have the same id. Absent: the service makes a new id.
        - `text` — string **(required)** — Text of the chunk. Must not be empty. _(minLen=1)_
        - `confidence` — number — Confidence of the recogniser. The service ignores a value outside 0 to 1. _(format=double)_
        - `final` — boolean — True when the chunk is the final transcript of the utterance. False for an interim result. Absent: true.
        - `language` — string — Language that the recogniser identified for the chunk. The service records it and does not change the conversation language. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `time` — number — Time of the chunk, in epoch ms. Absent: the time when the service received it.
      - `agentTranscription` — VoiceAgentTranscriptionEvent — A transcription chunk of the agent speech, as the caller hears it. It does not start a turn.
        - `type` — object **(required)**
        - `id` — string — Id of the utterance. Absent: the service makes a new id.
        - `text` — string **(required)** — Text of the chunk. Must not be empty. _(minLen=1)_
        - `confidence` — number — Confidence of the recogniser. The service does not record it. _(format=double)_
        - `final` — boolean — True when the chunk is the final transcript of the utterance. False for an interim result. Absent: true.
        - `language` — string — Language that the recogniser identified for the chunk. The service records it and does not change the conversation language. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `time` — number — Time of the chunk, in epoch ms. Absent: the time when the service received it.
      - `reply` — VoiceReplyEvent — A final caller utterance. It starts an agent turn.
        - `type` — object **(required)**
        - `id` — string — Id of the utterance. Absent: the service makes a new id.
        - `text` — string **(required)** — Text of the utterance. Must not be empty. _(minLen=1)_
        - `time` — number — Time of the utterance, in epoch ms. Absent: the time when the service received it.
        - `language` — string — Language that the recogniser identified for the utterance. A value that is different from the conversation language changes the conversation language. When the utterance has segments in more than one language, send the language of the last segment. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `confidence` — number — Confidence of the recogniser for the utterance. The service ignores a value outside 0 to 1. _(format=double)_
        - `startTime` — number — Start of the speech, in epoch ms on the client clock. The service ignores 0.
        - `endTime` — number — End of the speech, in epoch ms on the client clock. The service ignores 0.
      - `playback` — VoicePlaybackEvent — Progress of the playback of a reply on the client.
        - `type` — object **(required)**
        - `replyId` — string — Reply that the client plays.
        - `text` — string — Text of the reply that the client played.
        - `complete` — boolean **(required)** — True when the client played the reply to its end.
        - `startTime` — number — Start of the playback, in epoch ms on the client clock. The service ignores 0.
        - `endTime` — number — End of the playback, in epoch ms on the client clock. The service ignores 0.
      - `interruption` — VoiceInterruptionEvent — The caller spoke over a reply while the client played it.
        - `type` — object **(required)**
        - `replyId` — string — Reply that the caller interrupted.
        - `playedText` — string — Part of the reply that the client played before the interruption.
        - `originalText` — string — Full text of the reply.
        - `time` — number — Time of the interruption, in epoch ms on the client clock. The service ignores 0.
      - `complete` — VoiceCompleteEvent — The call or the conversation is complete, for example because the caller hung up. The service ends the session. The service also accepts `type` `ended` with the same meaning.
        - `type` — object **(required)**
        - `reason` — string — Why the call is complete. Absent: the value of `type`.
        - `time` — number — Time of the completion, in epoch ms. The service ignores it.
    - `server` — VoiceTextServerFrames — One example of each message that the server sends on the text socket. An event goes in `{"type": "event", "event": {...}}`, a command in `{"type": "command", "command": {...}}`.
      - `started` — VoiceSessionStartedEvent — The session is ready. Sent once after the handshake, on the PBX voice socket only when the client sends protocol version 1 or more.
        - `type` — object **(required)**
        - `time` — number **(required)** — Time of the event, in epoch ms.
        - `sessionId` — string **(required)** — Id of the session. _(minLen=1; maxLen=128)_
        - `agentId` — string **(required)** — Agent of the session. _(minLen=12; maxLen=12)_
        - `agentVersion` — number — Published agent version of the session. Absent when the session runs the agent draft. _(min=1)_
        - `traceId` — string — Trace of the session. It does not change during the session. _(minLen=1; maxLen=128)_
        - `agentName` — string — Display name of the agent.
        - `category` — string — Category of the agent.
        - `groupId` — string — PBX group of the agent, for data access control. Empty when the agent has no group.
        - `speech` — VoiceSpeechPayload — Speech recognition settings of the call. The client applies them to its recogniser.
          - `engine` — string **(required)** — Recogniser URI. Always present. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
          - `languages` — array **(required)** — All configured languages. These are the candidates for language identification.
            - _array of_ `string`
          - `preferredLanguage` — string **(required)** — Language at the start of the call. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
          - `autoDetect` — boolean **(required)** — True to identify the spoken language of each utterance. False when `languages` has fewer languages than the recogniser needs, or when the recogniser cannot identify languages.
        - `backgroundSound` — string — Music-on-hold class to play as background sound of the call. Absent: no background sound. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
      - `ended` — VoiceSessionEndedEvent — The session ended. This is the last event of the session.
        - `type` — object **(required)**
        - `reason` — string — Why the session ended.
        - `error` — string — Present when the session ended because of an error.
        - `time` — number **(required)** — Time of the event, in epoch ms.
      - `error` — VoiceErrorEvent — An error on the connection. The session continues, unless a `ended` event follows.
        - `type` — object **(required)**
        - `code` — string **(required)** — Error code. The value is stable.
        - `message` — string **(required)** — Description of the error.
        - `time` — number **(required)** — Time of the event, in epoch ms.
      - `say` — VoiceSayCommand — Play a reply to the caller. When `audio` is present, the service sends the audio of the reply in `play` commands. When `audio` is absent, the client shows `text` or synthesizes it itself.
        - `text` — string **(required)** — Text of the reply.
        - `replyId` — string **(required)** — Id of the reply.
        - `interruptible` — boolean — True when the caller can interrupt the reply.
        - `audio` — VoiceSayCommandAudioOptions — Audio of a reply that the service synthesizes. `play` commands with this stream id follow the `say` command.
          - `streamId` — string **(required)**
          - `sampleRate` — number **(required)** — Sample rate of the `pcm_s16le` mono audio of the `play` commands, in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000.
        - `type` — object **(required)**
      - `play` — VoicePlayCommand — A chunk of synthesized audio of a reply. `data` is base64 of PCM audio at the sample rate of the `say` command. An empty `data` marks the end of the stream.
        - `replyId` — string **(required)**
        - `streamId` — string **(required)**
        - `data` — string **(required)**
        - `type` — object **(required)**
      - `stop` — VoiceStopCommand — Stop the audio of the agent.
        - `type` — object **(required)**
      - `hangup` — VoiceHangupCommand — End the session and hang up the call.
        - `reason` — string — Why the session ended.
        - `type` — object **(required)**
      - `transfer` — VoiceTransferCommand — Transfer the call to a PBX destination and end the session. Only a PBX client does the transfer.
        - `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
        - `extension` — string **(required)** — Extension of the destination. _(minLen=1)_
        - `type` — object **(required)**
  - `callSocket` — VoiceCallProtocolFrames — The text messages of the call socket `/v2/voice/calls/ws`. The socket has no connect parameters: the first text frame is `start`.
    - `client` — VoiceCallClientFrames — One example of each text message that the client (the PBX) sends on the call socket.
      - `start` — VoiceCallStartFrame — First text frame of a socket, sent within 10 s of the upgrade. Opens a run, or attaches a reconnect to it.
        - `type` — object **(required)**
        - `callId` — string **(required)** — Id of the PBX call. Use it to correlate the call events of the run. _(minLen=1)_
        - `flowIndex` — number **(required)** — Index of this run on the call, from 0. _(min=0)_
        - `sessionId` — string **(required)** — Id of this run. The same on every connection of the run; the cloud attaches a reconnect and settles a takeover by it. _(minLen=1; maxLen=128)_
        - `resume` — boolean **(required)** — True when an earlier connection of this run got agent audio (`audio.begin`): the cloud continues that session without a new greeting.
        - `resumeAtMs` — number **(required)** — Run-clock time of the first audio byte of this connection: 0 on the first connection. _(min=0)_
        - `agent` — VoiceCallStartAgent **(required)** — The agent of the run. At most one of `draft` and `version` is set.
          - `id` — string **(required)** — Agent id. _(minLen=12; maxLen=12)_
          - `draft` — boolean — True to run the unpublished draft. Absent or null: false.
          - `version` — number — Published version to run. Absent or null: the version the agent routing selects. _(min=1)_
        - `language` — string **(required)** — Language of the call, for example `en-US`. The agent starts in its configured language that matches it. _(minLen=1)_
        - `caller` — VoiceCallStartCaller **(required)** — Caller identity from the lookup application of the PBX: an external lookup or the local phonebook. Each member is absent, null or empty when unknown.
          - `name` — string
          - `number` — string
          - `email` — string
          - `company` — string
        - `dialedNumber` — string — Number that the caller dialled. Absent, null or empty when unknown.
        - `variables` — string — Base64 of a JSON object of the `VOICEBOT_*` channel variables. Absent, null or empty when there are none. _(pattern=^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$)_
      - `vad` — VoiceCallVadFrame — Voice activity of the caller as the PBX detects it. Sent when the state changes, and every 100 ms while agent audio plays.
        - `type` — object **(required)**
        - `speaking` — boolean **(required)** — True while the caller speaks.
        - `energyDb` — number **(required)** — Energy of the audio frame that produced the report, in dBFS. _(format=double; min=-96; max=0)_
        - `atMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
      - `dtmf` — VoiceCallDtmfFrame — DTMF input that the PBX collected. The cloud takes `digits` as the caller's reply.
        - `type` — object **(required)**
        - `id` — string **(required)** _(minLen=1; maxLen=127)_
        - `digits` — string **(required)** _(pattern=^[0-9*#A-D]{1,64}$)_
      - `playback` — VoiceCallPlaybackFrame — An agent audio stream changed state on the PBX.
        - `type` — object **(required)**
        - `replyId` — string **(required)** _(minLen=1; maxLen=127)_
        - `streamId` — string **(required)** _(minLen=1; maxLen=127)_
        - `event` — string **(required)** — Event of an agent audio stream. _(enum: `started`, `finished`, `stopped`)_
        - `atMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
        - `playedMs` — number — Audio of the stream that played, in ms. Present with `finished` and `stopped`. _(min=0)_
        - `dropped` — boolean — True when the PBX dropped the stream, for example at its queue limit. Only with `stopped`. Absent: false.
      - `end` — VoiceCallEndFrame — The run ended on the PBX. The PBX sends no audio after it and waits up to 3 s for `ended`.
        - `type` — object **(required)**
        - `reason` — string **(required)** — Who ended the run on the PBX. The live events of the call report it as `VoiceCallEndReason`: `caller-hangup` as `hangup`, `agent-hangup` as `complete`, `agent-transfer` as `transfer`, `timeout` as `timeout`. _(enum: `caller-hangup`, `agent-hangup`, `agent-transfer`, `timeout`)_
    - `server` — VoiceCallServerFrames — One example of each text message that the server (the cloud) sends on the call socket.
      - `started` — VoiceCallStartedFrame — Answer to `start`: the session of the run is ready on this connection. Sent once per connection, also after a reconnect. Example: `{"type":"started","connectionId":"0f6d…","agent":{"id":"a_qqyHI7xWBH","name":"Support"}}`.
        - `type` — object **(required)**
        - `connectionId` — string **(required)** — Id of this connection. Each connection of the run has its own.
        - `agent` — VoiceCallStartedAgent **(required)** — The agent that answers the run.
          - `id` — string **(required)** — Agent id, as in `start.agent.id`. _(minLen=12; maxLen=12)_
          - `name` — string **(required)** — Display name of the agent.
          - `groupId` — string — Group of the agent. Absent when the agent has none.
        - `backgroundSound` — string — Music-on-hold class that the PBX plays after each caller turn until agent audio starts. Absent: none. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
        - `voiceDetection` — VoiceDetectionSettings — Caller voice detection on the PBX.
          - `silenceMs` — number — Silence in ms that ends the caller speech. Absent: 500. _(min=100; max=5000)_
          - `silenceLevelDb` — number — Mean frame level in dBFS below which caller audio is silence. Absent: -36. _(min=-90; max=0)_
          - `speechLevelDb` — number — Mean frame level in dBFS from which caller audio is speech. Absent: -30. _(min=-90; max=0)_
      - `transcription` — VoiceCallTranscriptionFrame — Words of one party. Partials and the final of one utterance share `id`. For the agent, the words that played.
        - `type` — object **(required)**
        - `party` — string **(required)** — A party of the call. _(enum: `caller`, `callee`)_
        - `id` — string **(required)**
        - `final` — boolean **(required)**
        - `text` — string **(required)**
        - `startMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
        - `endMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
        - `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `confidence` — number — Recogniser confidence from 0 to 1. Absent when the text is not from a recogniser, or the engine gives none. _(format=double; min=0; max=1)_
      - `audioBegin` — VoiceCallAudioBeginFrame — Opens an agent audio stream. Binary audio messages of the stream follow until `audio.end`. Streams do not interleave.
        - `type` — object **(required)**
        - `replyId` — string **(required)**
        - `streamId` — string **(required)**
        - `sampleRate` — number **(required)** — Sample rate of the stream's `pcm_s16le` mono audio in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000. _(min=8000; max=48000)_
      - `audioEnd` — VoiceCallAudioEndFrame — Closes an agent audio stream.
        - `type` — object **(required)**
        - `streamId` — string **(required)**
      - `stop` — VoiceCallStopFrame — Stop every agent audio stream of the run: the one that plays and the ones that wait.
        - `type` — object **(required)**
      - `duck` — VoiceCallDuckFrame — Change the volume of a playing reply. `volumeDb` 0 returns it to full volume.
        - `type` — object **(required)**
        - `replyId` — string **(required)**
        - `volumeDb` — number **(required)** — Target gain in dB. _(min=-90; max=0)_
        - `rampMs` — number **(required)** — Ramp duration in ms. _(min=0; max=1000)_
      - `language` — VoiceCallLanguageFrame — The call continues in another language.
        - `type` — object **(required)**
        - `language` — string **(required)** — Language that the call continues in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `transfer` — VoiceCallTransferFrame — Transfer the call after the queued agent audio plays. Terminal: the PBX answers with `end`.
        - `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
        - `extension` — string **(required)** — Extension of the destination. _(minLen=1)_
        - `type` — object **(required)**
      - `hangup` — VoiceCallHangupFrame — Hang up the call after the queued agent audio plays. Terminal: the PBX answers with `end`.
        - `type` — object **(required)**
      - `error` — VoiceCallErrorFrame — An error on the run. When `retryable` is false, the socket closes after it.
        - `type` — object **(required)**
        - `code` — string **(required)** — Stable error code, for example `START_TIMEOUT`, `PROTOCOL_ERROR` or `STT_FAILED`.
        - `retryable` — boolean **(required)**
        - `message` — string **(required)**
      - `ended` — VoiceCallEndedFrame — Answer to `end`: the cloud processed all audio. The socket closes with close code 1000 after it.
        - `type` — object **(required)**
  - `callEvent` — union — One event on a live call. The SSE frame's `event:` is the member name and `data:` this whole union document, so a frame reads `data: {"say": {...}}` — never the member's payload on its own.
    - _oneOf_ — exactly one of:
      - **`started`**
        - `started` — VoiceCallStartedEvent **(required)** — The session that answered the call, sent once per session of the call (a transfer starts another).
          - `sessionId` — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
          - `traceId` — string — The session's trace, for the LLM-level detail this stream deliberately omits. Absent for a built-in agent, whose trace is not the tenant's to read. _(minLen=1; maxLen=128)_
          - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
          - `agentName` — string
          - `agentVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
          - `agentDraft` — boolean — True when the session runs the agent's draft.
          - `language` — string — BCP-47 language the call started in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - **`transcription`**
        - `transcription` — VoiceCallTranscriptionEvent **(required)** — A recogniser result for the caller's speech. Interim results (`final: false`) are replaced by the final one with the same `id`.
          - `id` — string **(required)**
          - `text` — string **(required)**
          - `final` — boolean **(required)**
          - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
          - `time` — number — Milliseconds since the call started, as the PBX stamps it.
          - `finalDropReason` — string — Why the service did not use a final caller transcript as a caller turn. _(enum: `low_confidence`, `other_speaker`)_
      - **`agentTranscription`**
        - `agentTranscription` — VoiceCallAgentTranscriptionEvent **(required)** — A recogniser result for the AGENT's own leg — what the caller actually heard. Same semantics as VoiceCallTranscriptionEvent; an interrupted reply simply stops.
          - `id` — string **(required)**
          - `text` — string **(required)**
          - `final` — boolean **(required)**
          - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
          - `time` — number
      - **`reply`**
        - `reply` — VoiceCallReplyEvent **(required)** — The caller's completed utterance that started a turn — after the runtime's filler and duplicate filter.
          - `id` — string **(required)**
          - `text` — string **(required)**
          - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - **`say`**
        - `say` — VoiceCallSayEvent **(required)** — One sentence the agent speaks, as it is handed to the PBX (after playback sanitizing). Sentences of one reply share `replyId`.
          - `replyId` — string **(required)**
          - `text` — string **(required)**
          - `interruptible` — boolean **(required)**
      - **`playback`**
        - `playback` — VoiceCallPlaybackEvent **(required)** — The PBX finished (or abandoned) playing a reply.
          - `replyId` — string **(required)**
          - `complete` — boolean **(required)**
      - **`interruption`**
        - `interruption` — VoiceCallInterruptionEvent **(required)** — The caller talked over the agent. `playedText` is what they heard before the cut.
          - `replyId` — string
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
          - `phase` — string **(required)** — Phase of a tool call of the agent. _(enum: `started`, `finished`)_
          - `startMessage` — string — The phrase spoken while the tool runs, when the capability configures one.
      - **`ended`**
        - `ended` — VoiceCallEndedEvent **(required)** — The session ended. After `transfer` another session of the same call may follow with its own `started`.
          - `sessionId` — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
          - `reason` — string **(required)** _(enum: `hangup`, `transfer`, `timeout`, `error`, `complete`)_
- Errors: `400`, `403`

### Session

#### `POST` `/v2/voice/sessions/{sessionId}/hangup`

Terminates the voice session and the call.

- operationId: `SendHangup`
- **Scopes**: `wilma-voice:SendHangup`
- **Parameters**
  - `sessionId` (path) — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
- **Request body** (`application/json` — `SendHangupRequestContent`)
  - `reason` — string — Why the session ended.
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voice/sessions/{sessionId}/play`

Plays the specified audio chunk through the audio stream of the voice session.

- operationId: `SendPlay`
- **Scopes**: `wilma-voice:SendPlay`
- **Parameters**
  - `sessionId` (path) — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
- **Request body** (`application/json` — `SendPlayRequestContent`) **(required)**
  - `replyId` — string **(required)**
  - `streamId` — string **(required)**
  - `data` — string **(required)**
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voice/sessions/{sessionId}/say`

Generates and plays the specified text through the audio stream of the voice session.

- operationId: `SendSay`
- **Scopes**: `wilma-voice:SendSay`
- **Parameters**
  - `sessionId` (path) — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
- **Request body** (`application/json` — `SendSayRequestContent`) **(required)**
  - `text` — string **(required)** — Text of the reply.
  - `replyId` — string **(required)** — Id of the reply.
  - `interruptible` — boolean — True when the caller can interrupt the reply.
  - `audio` — VoiceSayCommandAudioOptions — Audio of a reply that the service synthesizes. `play` commands with this stream id follow the `say` command.
    - `streamId` — string **(required)**
    - `sampleRate` — number **(required)** — Sample rate of the `pcm_s16le` mono audio of the `play` commands, in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000.
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voice/sessions/{sessionId}/stop`

Stops any audio currently being played by the voice session.

- operationId: `SendStop`
- **Scopes**: `wilma-voice:SendStop`
- **Parameters**
  - `sessionId` (path) — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voice/sessions/{sessionId}/transfer`

Transfers the call to the specified context and extension, and terminates the voice session.

- operationId: `SendTransfer`
- **Scopes**: `wilma-voice:SendTransfer`
- **Parameters**
  - `sessionId` (path) — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
- **Request body** (`application/json` — `SendTransferRequestContent`) **(required)**
  - `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
  - `extension` — string **(required)** — Extension of the destination. _(minLen=1)_
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

<details><summary>81 component schemas</summary>

**`DescribeVoiceProtocolResponseContent`**

- `textSocket` — VoiceTextProtocolFrames — The connect parameters and the messages of the text socket `/v2/voice/ws`.
  - `connectParams` — VoiceConnectParams — Parameters supplied on the WebSocket connect (upgrade) request, as query-string parameters.
    - `protocolVersion` — number — Protocol version advertised by the client (query parameter `v`). 0 (or absent) is the legacy PBX protocol; >= 1 enables the sessionStarted event; >= 2 additionally means the client WAITS for `started` before opening its recognition stream and honours the `speech` payload on it; >= 3 additionally means the client connects again with `resume` after close code `1001`, so the service can move the call to another server while it runs.
    - `sessionId` — string **(required)** — Caller-supplied session id, unique per connection. _(minLen=1; maxLen=128)_
    - `resume` — boolean — True when this connection attaches the running session `sessionId` again, after a close with close code `1001` or a lost connection. The session keeps its history and does not play the greeting again.
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
    - `inputMode` — string — How caller speech reaches the service. _(enum: `transcription`)_
    - `user` — string — Owner user of the session. Absent: no user. The service ignores it for a PBX token with `callId`. _(minLen=12; maxLen=12)_
    - `company` — string — Tenant of the session. Required for a service token, which carries no tenant. For another token a value different from the token tenant gets HTTP 401. _(minLen=3; maxLen=30)_
  - `client` — VoiceTextClientFrames — One example of each message that the client sends on the text socket. An event goes in `{"type": "event", "event": {...}}`; `healthcheck` has no envelope.
    - `healthcheck` — VoiceHealthcheckCommand — Liveness check of the service by the client: `{"type": "healthcheck"}`, with no envelope. The service sends no answer.
      - `type` — string **(required)** _(default=healthcheck)_
    - `transcription` — VoiceTranscriptionEvent — A transcription chunk of caller speech. A client that does its own speech-to-text sends it. When the service does the speech-to-text, the service sends it to the client.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `id` — string — Id of the utterance. The interim chunks and the final chunk of one utterance have the same id. Absent: the service makes a new id.
      - `text` — string **(required)** — Text of the chunk. Must not be empty. _(minLen=1)_
      - `confidence` — number — Confidence of the recogniser. The service ignores a value outside 0 to 1. _(format=double)_
      - `final` — boolean — True when the chunk is the final transcript of the utterance. False for an interim result. Absent: true.
      - `language` — string — Language that the recogniser identified for the chunk. The service records it and does not change the conversation language. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `time` — number — Time of the chunk, in epoch ms. Absent: the time when the service received it.
    - `agentTranscription` — VoiceAgentTranscriptionEvent — A transcription chunk of the agent speech, as the caller hears it. It does not start a turn.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `id` — string — Id of the utterance. Absent: the service makes a new id.
      - `text` — string **(required)** — Text of the chunk. Must not be empty. _(minLen=1)_
      - `confidence` — number — Confidence of the recogniser. The service does not record it. _(format=double)_
      - `final` — boolean — True when the chunk is the final transcript of the utterance. False for an interim result. Absent: true.
      - `language` — string — Language that the recogniser identified for the chunk. The service records it and does not change the conversation language. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `time` — number — Time of the chunk, in epoch ms. Absent: the time when the service received it.
    - `reply` — VoiceReplyEvent — A final caller utterance. It starts an agent turn.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `id` — string — Id of the utterance. Absent: the service makes a new id.
      - `text` — string **(required)** — Text of the utterance. Must not be empty. _(minLen=1)_
      - `time` — number — Time of the utterance, in epoch ms. Absent: the time when the service received it.
      - `language` — string — Language that the recogniser identified for the utterance. A value that is different from the conversation language changes the conversation language. When the utterance has segments in more than one language, send the language of the last segment. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `confidence` — number — Confidence of the recogniser for the utterance. The service ignores a value outside 0 to 1. _(format=double)_
      - `startTime` — number — Start of the speech, in epoch ms on the client clock. The service ignores 0.
      - `endTime` — number — End of the speech, in epoch ms on the client clock. The service ignores 0.
    - `playback` — VoicePlaybackEvent — Progress of the playback of a reply on the client.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `replyId` — string — Reply that the client plays.
      - `text` — string — Text of the reply that the client played.
      - `complete` — boolean **(required)** — True when the client played the reply to its end.
      - `startTime` — number — Start of the playback, in epoch ms on the client clock. The service ignores 0.
      - `endTime` — number — End of the playback, in epoch ms on the client clock. The service ignores 0.
    - `interruption` — VoiceInterruptionEvent — The caller spoke over a reply while the client played it.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `replyId` — string — Reply that the caller interrupted.
      - `playedText` — string — Part of the reply that the client played before the interruption.
      - `originalText` — string — Full text of the reply.
      - `time` — number — Time of the interruption, in epoch ms on the client clock. The service ignores 0.
    - `complete` — VoiceCompleteEvent — The call or the conversation is complete, for example because the caller hung up. The service ends the session. The service also accepts `type` `ended` with the same meaning.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `reason` — string — Why the call is complete. Absent: the value of `type`.
      - `time` — number — Time of the completion, in epoch ms. The service ignores it.
  - `server` — VoiceTextServerFrames — One example of each message that the server sends on the text socket. An event goes in `{"type": "event", "event": {...}}`, a command in `{"type": "command", "command": {...}}`.
    - `started` — VoiceSessionStartedEvent — The session is ready. Sent once after the handshake, on the PBX voice socket only when the client sends protocol version 1 or more.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `time` — number **(required)** — Time of the event, in epoch ms.
      - `sessionId` — string **(required)** — Id of the session. _(minLen=1; maxLen=128)_
      - `agentId` — string **(required)** — Agent of the session. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Published agent version of the session. Absent when the session runs the agent draft. _(min=1)_
      - `traceId` — string — Trace of the session. It does not change during the session. _(minLen=1; maxLen=128)_
      - `agentName` — string — Display name of the agent.
      - `category` — string — Category of the agent.
      - `groupId` — string — PBX group of the agent, for data access control. Empty when the agent has no group.
      - `speech` — VoiceSpeechPayload — Speech recognition settings of the call. The client applies them to its recogniser.
        - _(nesting depth limit — see `VoiceSpeechPayload` in the Schemas appendix)_
      - `backgroundSound` — string — Music-on-hold class to play as background sound of the call. Absent: no background sound. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `ended` — VoiceSessionEndedEvent — The session ended. This is the last event of the session.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `reason` — string — Why the session ended.
      - `error` — string — Present when the session ended because of an error.
      - `time` — number **(required)** — Time of the event, in epoch ms.
    - `error` — VoiceErrorEvent — An error on the connection. The session continues, unless a `ended` event follows.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `code` — string **(required)** — Error code. The value is stable.
      - `message` — string **(required)** — Description of the error.
      - `time` — number **(required)** — Time of the event, in epoch ms.
    - `say` — VoiceSayCommand — Play a reply to the caller. When `audio` is present, the service sends the audio of the reply in `play` commands. When `audio` is absent, the client shows `text` or synthesizes it itself.
      - `text` — string **(required)** — Text of the reply.
      - `replyId` — string **(required)** — Id of the reply.
      - `interruptible` — boolean — True when the caller can interrupt the reply.
      - `audio` — VoiceSayCommandAudioOptions — Audio of a reply that the service synthesizes. `play` commands with this stream id follow the `say` command.
        - _(nesting depth limit — see `VoiceSayCommandAudioOptions` in the Schemas appendix)_
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `play` — VoicePlayCommand — A chunk of synthesized audio of a reply. `data` is base64 of PCM audio at the sample rate of the `say` command. An empty `data` marks the end of the stream.
      - `replyId` — string **(required)**
      - `streamId` — string **(required)**
      - `data` — string **(required)**
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `stop` — VoiceStopCommand — Stop the audio of the agent.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `hangup` — VoiceHangupCommand — End the session and hang up the call.
      - `reason` — string — Why the session ended.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `transfer` — VoiceTransferCommand — Transfer the call to a PBX destination and end the session. Only a PBX client does the transfer.
      - `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
      - `extension` — string **(required)** — Extension of the destination. _(minLen=1)_
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `callSocket` — VoiceCallProtocolFrames — The text messages of the call socket `/v2/voice/calls/ws`. The socket has no connect parameters: the first text frame is `start`.
  - `client` — VoiceCallClientFrames — One example of each text message that the client (the PBX) sends on the call socket.
    - `start` — VoiceCallStartFrame — First text frame of a socket, sent within 10 s of the upgrade. Opens a run, or attaches a reconnect to it.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `callId` — string **(required)** — Id of the PBX call. Use it to correlate the call events of the run. _(minLen=1)_
      - `flowIndex` — number **(required)** — Index of this run on the call, from 0. _(min=0)_
      - `sessionId` — string **(required)** — Id of this run. The same on every connection of the run; the cloud attaches a reconnect and settles a takeover by it. _(minLen=1; maxLen=128)_
      - `resume` — boolean **(required)** — True when an earlier connection of this run got agent audio (`audio.begin`): the cloud continues that session without a new greeting.
      - `resumeAtMs` — number **(required)** — Run-clock time of the first audio byte of this connection: 0 on the first connection. _(min=0)_
      - `agent` — VoiceCallStartAgent **(required)** — The agent of the run. At most one of `draft` and `version` is set.
        - _(nesting depth limit — see `VoiceCallStartAgent` in the Schemas appendix)_
      - `language` — string **(required)** — Language of the call, for example `en-US`. The agent starts in its configured language that matches it. _(minLen=1)_
      - `caller` — VoiceCallStartCaller **(required)** — Caller identity from the lookup application of the PBX: an external lookup or the local phonebook. Each member is absent, null or empty when unknown.
        - _(nesting depth limit — see `VoiceCallStartCaller` in the Schemas appendix)_
      - `dialedNumber` — string — Number that the caller dialled. Absent, null or empty when unknown.
      - `variables` — string — Base64 of a JSON object of the `VOICEBOT_*` channel variables. Absent, null or empty when there are none. _(pattern=^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$)_
    - `vad` — VoiceCallVadFrame — Voice activity of the caller as the PBX detects it. Sent when the state changes, and every 100 ms while agent audio plays.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `speaking` — boolean **(required)** — True while the caller speaks.
      - `energyDb` — number **(required)** — Energy of the audio frame that produced the report, in dBFS. _(format=double; min=-96; max=0)_
      - `atMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
    - `dtmf` — VoiceCallDtmfFrame — DTMF input that the PBX collected. The cloud takes `digits` as the caller's reply.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `id` — string **(required)** _(minLen=1; maxLen=127)_
      - `digits` — string **(required)** _(pattern=^[0-9*#A-D]{1,64}$)_
    - `playback` — VoiceCallPlaybackFrame — An agent audio stream changed state on the PBX.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `replyId` — string **(required)** _(minLen=1; maxLen=127)_
      - `streamId` — string **(required)** _(minLen=1; maxLen=127)_
      - `event` — string **(required)** — Event of an agent audio stream. _(enum: `started`, `finished`, `stopped`)_
      - `atMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
      - `playedMs` — number — Audio of the stream that played, in ms. Present with `finished` and `stopped`. _(min=0)_
      - `dropped` — boolean — True when the PBX dropped the stream, for example at its queue limit. Only with `stopped`. Absent: false.
    - `end` — VoiceCallEndFrame — The run ended on the PBX. The PBX sends no audio after it and waits up to 3 s for `ended`.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `reason` — string **(required)** — Who ended the run on the PBX. The live events of the call report it as `VoiceCallEndReason`: `caller-hangup` as `hangup`, `agent-hangup` as `complete`, `agent-transfer` as `transfer`, `timeout` as `timeout`. _(enum: `caller-hangup`, `agent-hangup`, `agent-transfer`, `timeout`)_
  - `server` — VoiceCallServerFrames — One example of each text message that the server (the cloud) sends on the call socket.
    - `started` — VoiceCallStartedFrame — Answer to `start`: the session of the run is ready on this connection. Sent once per connection, also after a reconnect. Example: `{"type":"started","connectionId":"0f6d…","agent":{"id":"a_qqyHI7xWBH","name":"Support"}}`.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `connectionId` — string **(required)** — Id of this connection. Each connection of the run has its own.
      - `agent` — VoiceCallStartedAgent **(required)** — The agent that answers the run.
        - _(nesting depth limit — see `VoiceCallStartedAgent` in the Schemas appendix)_
      - `backgroundSound` — string — Music-on-hold class that the PBX plays after each caller turn until agent audio starts. Absent: none. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
      - `voiceDetection` — VoiceDetectionSettings — Caller voice detection on the PBX.
        - _(nesting depth limit — see `VoiceDetectionSettings` in the Schemas appendix)_
    - `transcription` — VoiceCallTranscriptionFrame — Words of one party. Partials and the final of one utterance share `id`. For the agent, the words that played.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `party` — string **(required)** — A party of the call. _(enum: `caller`, `callee`)_
      - `id` — string **(required)**
      - `final` — boolean **(required)**
      - `text` — string **(required)**
      - `startMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
      - `endMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
      - `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `confidence` — number — Recogniser confidence from 0 to 1. Absent when the text is not from a recogniser, or the engine gives none. _(format=double; min=0; max=1)_
    - `audioBegin` — VoiceCallAudioBeginFrame — Opens an agent audio stream. Binary audio messages of the stream follow until `audio.end`. Streams do not interleave.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `replyId` — string **(required)**
      - `streamId` — string **(required)**
      - `sampleRate` — number **(required)** — Sample rate of the stream's `pcm_s16le` mono audio in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000. _(min=8000; max=48000)_
    - `audioEnd` — VoiceCallAudioEndFrame — Closes an agent audio stream.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `streamId` — string **(required)**
    - `stop` — VoiceCallStopFrame — Stop every agent audio stream of the run: the one that plays and the ones that wait.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `duck` — VoiceCallDuckFrame — Change the volume of a playing reply. `volumeDb` 0 returns it to full volume.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `replyId` — string **(required)**
      - `volumeDb` — number **(required)** — Target gain in dB. _(min=-90; max=0)_
      - `rampMs` — number **(required)** — Ramp duration in ms. _(min=0; max=1000)_
    - `language` — VoiceCallLanguageFrame — The call continues in another language.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `language` — string **(required)** — Language that the call continues in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `transfer` — VoiceCallTransferFrame — Transfer the call after the queued agent audio plays. Terminal: the PBX answers with `end`.
      - `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
      - `extension` — string **(required)** — Extension of the destination. _(minLen=1)_
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `hangup` — VoiceCallHangupFrame — Hang up the call after the queued agent audio plays. Terminal: the PBX answers with `end`.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `error` — VoiceCallErrorFrame — An error on the run. When `retryable` is false, the socket closes after it.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `code` — string **(required)** — Stable error code, for example `START_TIMEOUT`, `PROTOCOL_ERROR` or `STT_FAILED`.
      - `retryable` — boolean **(required)**
      - `message` — string **(required)**
    - `ended` — VoiceCallEndedFrame — Answer to `end`: the cloud processed all audio. The socket closes with close code 1000 after it.
      - `type` — object **(required)**
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `callEvent` — union — One event on a live call. The SSE frame's `event:` is the member name and `data:` this whole union document, so a frame reads `data: {"say": {...}}` — never the member's payload on its own.
  - _oneOf_ — exactly one of:
    - **`started`**
      - `started` — VoiceCallStartedEvent **(required)** — The session that answered the call, sent once per session of the call (a transfer starts another).
        - `sessionId` — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
        - `traceId` — string — The session's trace, for the LLM-level detail this stream deliberately omits. Absent for a built-in agent, whose trace is not the tenant's to read. _(minLen=1; maxLen=128)_
        - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
        - `agentName` — string
        - `agentVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
        - `agentDraft` — boolean — True when the session runs the agent's draft.
        - `language` — string — BCP-47 language the call started in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - **`transcription`**
      - `transcription` — VoiceCallTranscriptionEvent **(required)** — A recogniser result for the caller's speech. Interim results (`final: false`) are replaced by the final one with the same `id`.
        - `id` — string **(required)**
        - `text` — string **(required)**
        - `final` — boolean **(required)**
        - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `time` — number — Milliseconds since the call started, as the PBX stamps it.
        - `finalDropReason` — string — Why the service did not use a final caller transcript as a caller turn. _(enum: `low_confidence`, `other_speaker`)_
    - **`agentTranscription`**
      - `agentTranscription` — VoiceCallAgentTranscriptionEvent **(required)** — A recogniser result for the AGENT's own leg — what the caller actually heard. Same semantics as VoiceCallTranscriptionEvent; an interrupted reply simply stops.
        - `id` — string **(required)**
        - `text` — string **(required)**
        - `final` — boolean **(required)**
        - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `time` — number
    - **`reply`**
      - `reply` — VoiceCallReplyEvent **(required)** — The caller's completed utterance that started a turn — after the runtime's filler and duplicate filter.
        - `id` — string **(required)**
        - `text` — string **(required)**
        - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - **`say`**
      - `say` — VoiceCallSayEvent **(required)** — One sentence the agent speaks, as it is handed to the PBX (after playback sanitizing). Sentences of one reply share `replyId`.
        - `replyId` — string **(required)**
        - `text` — string **(required)**
        - `interruptible` — boolean **(required)**
    - **`playback`**
      - `playback` — VoiceCallPlaybackEvent **(required)** — The PBX finished (or abandoned) playing a reply.
        - `replyId` — string **(required)**
        - `complete` — boolean **(required)**
    - **`interruption`**
      - `interruption` — VoiceCallInterruptionEvent **(required)** — The caller talked over the agent. `playedText` is what they heard before the cut.
        - `replyId` — string
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
        - `phase` — string **(required)** — Phase of a tool call of the agent. _(enum: `started`, `finished`)_
        - `startMessage` — string — The phrase spoken while the tool runs, when the capability configures one.
    - **`ended`**
      - `ended` — VoiceCallEndedEvent **(required)** — The session ended. After `transfer` another session of the same call may follow with its own `started`.
        - `sessionId` — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
        - `reason` — string **(required)** _(enum: `hangup`, `transfer`, `timeout`, `error`, `complete`)_

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`ListVoicesResponseContent`**

- `voices` — array **(required)**
  - _array of_ `Voice`
    - `uri` — string **(required)** — Voice URI, ready to store as `VoiceLanguage.voice` or send to TextToSpeech. Carries no parameters — the caller appends the synthesis parameters and, where applicable, the `apiKey=secrets:{secretId}` reference it wants. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `name` — string **(required)** — Display name as the provider publishes it, e.g. 'Rachel'. A member rather than part of `metadata` because it is the one thing every provider has and every picker shows.
    - `metadata` — any — The provider's own metadata for this voice, for rendering and filtering only. See VoiceMetadata.

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`SendHangupRequestContent`**

_End the session and hang up the call._

- `reason` — string — Why the session ended.

**`SendPlayRequestContent`**

_A chunk of synthesized audio of a reply. `data` is base64 of PCM audio at the sample rate of the `say` command. An empty `data` marks the end of the stream._

- `replyId` — string **(required)**
- `streamId` — string **(required)**
- `data` — string **(required)**

**`SendSayRequestContent`**

_Play a reply to the caller. When `audio` is present, the service sends the audio of the reply in `play` commands. When `audio` is absent, the client shows `text` or synthesizes it itself._

- `text` — string **(required)** — Text of the reply.
- `replyId` — string **(required)** — Id of the reply.
- `interruptible` — boolean — True when the caller can interrupt the reply.
- `audio` — VoiceSayCommandAudioOptions — Audio of a reply that the service synthesizes. `play` commands with this stream id follow the `say` command.
  - `streamId` — string **(required)**
  - `sampleRate` — number **(required)** — Sample rate of the `pcm_s16le` mono audio of the `play` commands, in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000.

**`SendTransferRequestContent`**

_Transfer the call to a PBX destination and end the session. Only a PBX client does the transfer._

- `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
- `extension` — string **(required)** — Extension of the destination. _(minLen=1)_

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

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`Voice`**

_One voice a provider offers: the URI to store it by, a name to show, and the provider's own metadata. `uri` IS THE RESULT. It is exactly what goes into `VoiceLanguage.voice`, so a form stores what it was given instead of assembling a string out of a provider name and an id — the one place a client could get the convention wrong._

- `uri` — string **(required)** — Voice URI, ready to store as `VoiceLanguage.voice` or send to TextToSpeech. Carries no parameters — the caller appends the synthesis parameters and, where applicable, the `apiKey=secrets:{secretId}` reference it wants. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `name` — string **(required)** — Display name as the provider publishes it, e.g. 'Rachel'. A member rather than part of `metadata` because it is the one thing every provider has and every picker shows.
- `metadata` — any — The provider's own metadata for this voice, for rendering and filtering only. See VoiceMetadata.

**`VoiceAgentTranscriptionEvent`**

_A transcription chunk of the agent speech, as the caller hears it. It does not start a turn._

- `type` — object **(required)**
- `id` — string — Id of the utterance. Absent: the service makes a new id.
- `text` — string **(required)** — Text of the chunk. Must not be empty. _(minLen=1)_
- `confidence` — number — Confidence of the recogniser. The service does not record it. _(format=double)_
- `final` — boolean — True when the chunk is the final transcript of the utterance. False for an interim result. Absent: true.
- `language` — string — Language that the recogniser identified for the chunk. The service records it and does not change the conversation language. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `time` — number — Time of the chunk, in epoch ms. Absent: the time when the service received it.

**`VoiceCallAgentTranscriptionEvent`**

_A recogniser result for the AGENT's own leg — what the caller actually heard. Same semantics as VoiceCallTranscriptionEvent; an interrupted reply simply stops._

- `id` — string **(required)**
- `text` — string **(required)**
- `final` — boolean **(required)**
- `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `time` — number

**`VoiceCallAudioBeginFrame`**

_Opens an agent audio stream. Binary audio messages of the stream follow until `audio.end`. Streams do not interleave._

- `type` — object **(required)**
- `replyId` — string **(required)**
- `streamId` — string **(required)**
- `sampleRate` — number **(required)** — Sample rate of the stream's `pcm_s16le` mono audio in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000. _(min=8000; max=48000)_

**`VoiceCallAudioEndFrame`**

_Closes an agent audio stream._

- `type` — object **(required)**
- `streamId` — string **(required)**

**`VoiceCallClientEndReason`**

_Who ended the run on the PBX. The live events of the call report it as `VoiceCallEndReason`: `caller-hangup` as `hangup`, `agent-hangup` as `complete`, `agent-transfer` as `transfer`, `timeout` as `timeout`._

- string _(enum: `caller-hangup`, `agent-hangup`, `agent-transfer`, `timeout`)_

**`VoiceCallClientFrameType`**

_Value of `type` in a text frame from the client (the PBX)._

- string _(enum: `start`, `vad`, `dtmf`, `playback`, `end`)_

**`VoiceCallClientFrames`**

_One example of each text message that the client (the PBX) sends on the call socket._

- `start` — VoiceCallStartFrame — First text frame of a socket, sent within 10 s of the upgrade. Opens a run, or attaches a reconnect to it.
  - `type` — object **(required)**
  - `callId` — string **(required)** — Id of the PBX call. Use it to correlate the call events of the run. _(minLen=1)_
  - `flowIndex` — number **(required)** — Index of this run on the call, from 0. _(min=0)_
  - `sessionId` — string **(required)** — Id of this run. The same on every connection of the run; the cloud attaches a reconnect and settles a takeover by it. _(minLen=1; maxLen=128)_
  - `resume` — boolean **(required)** — True when an earlier connection of this run got agent audio (`audio.begin`): the cloud continues that session without a new greeting.
  - `resumeAtMs` — number **(required)** — Run-clock time of the first audio byte of this connection: 0 on the first connection. _(min=0)_
  - `agent` — VoiceCallStartAgent **(required)** — The agent of the run. At most one of `draft` and `version` is set.
    - `id` — string **(required)** — Agent id. _(minLen=12; maxLen=12)_
    - `draft` — boolean — True to run the unpublished draft. Absent or null: false.
    - `version` — number — Published version to run. Absent or null: the version the agent routing selects. _(min=1)_
  - `language` — string **(required)** — Language of the call, for example `en-US`. The agent starts in its configured language that matches it. _(minLen=1)_
  - `caller` — VoiceCallStartCaller **(required)** — Caller identity from the lookup application of the PBX: an external lookup or the local phonebook. Each member is absent, null or empty when unknown.
    - `name` — string
    - `number` — string
    - `email` — string
    - `company` — string
  - `dialedNumber` — string — Number that the caller dialled. Absent, null or empty when unknown.
  - `variables` — string — Base64 of a JSON object of the `VOICEBOT_*` channel variables. Absent, null or empty when there are none. _(pattern=^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$)_
- `vad` — VoiceCallVadFrame — Voice activity of the caller as the PBX detects it. Sent when the state changes, and every 100 ms while agent audio plays.
  - `type` — object **(required)**
  - `speaking` — boolean **(required)** — True while the caller speaks.
  - `energyDb` — number **(required)** — Energy of the audio frame that produced the report, in dBFS. _(format=double; min=-96; max=0)_
  - `atMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
- `dtmf` — VoiceCallDtmfFrame — DTMF input that the PBX collected. The cloud takes `digits` as the caller's reply.
  - `type` — object **(required)**
  - `id` — string **(required)** _(minLen=1; maxLen=127)_
  - `digits` — string **(required)** _(pattern=^[0-9*#A-D]{1,64}$)_
- `playback` — VoiceCallPlaybackFrame — An agent audio stream changed state on the PBX.
  - `type` — object **(required)**
  - `replyId` — string **(required)** _(minLen=1; maxLen=127)_
  - `streamId` — string **(required)** _(minLen=1; maxLen=127)_
  - `event` — string **(required)** — Event of an agent audio stream. _(enum: `started`, `finished`, `stopped`)_
  - `atMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
  - `playedMs` — number — Audio of the stream that played, in ms. Present with `finished` and `stopped`. _(min=0)_
  - `dropped` — boolean — True when the PBX dropped the stream, for example at its queue limit. Only with `stopped`. Absent: false.
- `end` — VoiceCallEndFrame — The run ended on the PBX. The PBX sends no audio after it and waits up to 3 s for `ended`.
  - `type` — object **(required)**
  - `reason` — string **(required)** — Who ended the run on the PBX. The live events of the call report it as `VoiceCallEndReason`: `caller-hangup` as `hangup`, `agent-hangup` as `complete`, `agent-transfer` as `transfer`, `timeout` as `timeout`. _(enum: `caller-hangup`, `agent-hangup`, `agent-transfer`, `timeout`)_

**`VoiceCallDtmfFrame`**

_DTMF input that the PBX collected. The cloud takes `digits` as the caller's reply._

- `type` — object **(required)**
- `id` — string **(required)** _(minLen=1; maxLen=127)_
- `digits` — string **(required)** _(pattern=^[0-9*#A-D]{1,64}$)_

**`VoiceCallDuckFrame`**

_Change the volume of a playing reply. `volumeDb` 0 returns it to full volume._

- `type` — object **(required)**
- `replyId` — string **(required)**
- `volumeDb` — number **(required)** — Target gain in dB. _(min=-90; max=0)_
- `rampMs` — number **(required)** — Ramp duration in ms. _(min=0; max=1000)_

**`VoiceCallEndFrame`**

_The run ended on the PBX. The PBX sends no audio after it and waits up to 3 s for `ended`._

- `type` — object **(required)**
- `reason` — string **(required)** — Who ended the run on the PBX. The live events of the call report it as `VoiceCallEndReason`: `caller-hangup` as `hangup`, `agent-hangup` as `complete`, `agent-transfer` as `transfer`, `timeout` as `timeout`. _(enum: `caller-hangup`, `agent-hangup`, `agent-transfer`, `timeout`)_

**`VoiceCallEndReason`**

- string _(enum: `hangup`, `transfer`, `timeout`, `error`, `complete`)_

**`VoiceCallEndedEvent`**

_The session ended. After `transfer` another session of the same call may follow with its own `started`._

- `sessionId` — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
- `reason` — string **(required)** _(enum: `hangup`, `transfer`, `timeout`, `error`, `complete`)_

**`VoiceCallEndedFrame`**

_Answer to `end`: the cloud processed all audio. The socket closes with close code 1000 after it._

- `type` — object **(required)**

**`VoiceCallErrorFrame`**

_An error on the run. When `retryable` is false, the socket closes after it._

- `type` — object **(required)**
- `code` — string **(required)** — Stable error code, for example `START_TIMEOUT`, `PROTOCOL_ERROR` or `STT_FAILED`.
- `retryable` — boolean **(required)**
- `message` — string **(required)**

**`VoiceCallEvent`**

_One event on a live call. The SSE frame's `event:` is the member name and `data:` this whole union document, so a frame reads `data: {"say": {...}}` — never the member's payload on its own._

- _oneOf_ — exactly one of:
  - **`started`**
    - `started` — VoiceCallStartedEvent **(required)** — The session that answered the call, sent once per session of the call (a transfer starts another).
      - `sessionId` — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
      - `traceId` — string — The session's trace, for the LLM-level detail this stream deliberately omits. Absent for a built-in agent, whose trace is not the tenant's to read. _(minLen=1; maxLen=128)_
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `agentName` — string
      - `agentVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `agentDraft` — boolean — True when the session runs the agent's draft.
      - `language` — string — BCP-47 language the call started in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - **`transcription`**
    - `transcription` — VoiceCallTranscriptionEvent **(required)** — A recogniser result for the caller's speech. Interim results (`final: false`) are replaced by the final one with the same `id`.
      - `id` — string **(required)**
      - `text` — string **(required)**
      - `final` — boolean **(required)**
      - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `time` — number — Milliseconds since the call started, as the PBX stamps it.
      - `finalDropReason` — string — Why the service did not use a final caller transcript as a caller turn. _(enum: `low_confidence`, `other_speaker`)_
  - **`agentTranscription`**
    - `agentTranscription` — VoiceCallAgentTranscriptionEvent **(required)** — A recogniser result for the AGENT's own leg — what the caller actually heard. Same semantics as VoiceCallTranscriptionEvent; an interrupted reply simply stops.
      - `id` — string **(required)**
      - `text` — string **(required)**
      - `final` — boolean **(required)**
      - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `time` — number
  - **`reply`**
    - `reply` — VoiceCallReplyEvent **(required)** — The caller's completed utterance that started a turn — after the runtime's filler and duplicate filter.
      - `id` — string **(required)**
      - `text` — string **(required)**
      - `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - **`say`**
    - `say` — VoiceCallSayEvent **(required)** — One sentence the agent speaks, as it is handed to the PBX (after playback sanitizing). Sentences of one reply share `replyId`.
      - `replyId` — string **(required)**
      - `text` — string **(required)**
      - `interruptible` — boolean **(required)**
  - **`playback`**
    - `playback` — VoiceCallPlaybackEvent **(required)** — The PBX finished (or abandoned) playing a reply.
      - `replyId` — string **(required)**
      - `complete` — boolean **(required)**
  - **`interruption`**
    - `interruption` — VoiceCallInterruptionEvent **(required)** — The caller talked over the agent. `playedText` is what they heard before the cut.
      - `replyId` — string
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
      - `phase` — string **(required)** — Phase of a tool call of the agent. _(enum: `started`, `finished`)_
      - `startMessage` — string — The phrase spoken while the tool runs, when the capability configures one.
  - **`ended`**
    - `ended` — VoiceCallEndedEvent **(required)** — The session ended. After `transfer` another session of the same call may follow with its own `started`.
      - `sessionId` — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
      - `reason` — string **(required)** _(enum: `hangup`, `transfer`, `timeout`, `error`, `complete`)_

**`VoiceCallHangupFrame`**

_Hang up the call after the queued agent audio plays. Terminal: the PBX answers with `end`._

- `type` — object **(required)**

**`VoiceCallInterruptionEvent`**

_The caller talked over the agent. `playedText` is what they heard before the cut._

- `replyId` — string
- `playedText` — string
- `originalText` — string

**`VoiceCallLanguageEvent`**

_The conversation language changed on a recognised utterance._

- `from` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `to` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `reason` — string **(required)**

**`VoiceCallLanguageFrame`**

_The call continues in another language._

- `type` — object **(required)**
- `language` — string **(required)** — Language that the call continues in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_

**`VoiceCallParty`**

_A party of the call._

- string _(enum: `caller`, `callee`)_

**`VoiceCallPlaybackEvent`**

_The PBX finished (or abandoned) playing a reply._

- `replyId` — string **(required)**
- `complete` — boolean **(required)**

**`VoiceCallPlaybackFrame`**

_An agent audio stream changed state on the PBX._

- `type` — object **(required)**
- `replyId` — string **(required)** _(minLen=1; maxLen=127)_
- `streamId` — string **(required)** _(minLen=1; maxLen=127)_
- `event` — string **(required)** — Event of an agent audio stream. _(enum: `started`, `finished`, `stopped`)_
- `atMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
- `playedMs` — number — Audio of the stream that played, in ms. Present with `finished` and `stopped`. _(min=0)_
- `dropped` — boolean — True when the PBX dropped the stream, for example at its queue limit. Only with `stopped`. Absent: false.

**`VoiceCallPlaybackPhase`**

_Event of an agent audio stream._

- string _(enum: `started`, `finished`, `stopped`)_

**`VoiceCallProtocolFrames`**

_The text messages of the call socket `/v2/voice/calls/ws`. The socket has no connect parameters: the first text frame is `start`._

- `client` — VoiceCallClientFrames — One example of each text message that the client (the PBX) sends on the call socket.
  - `start` — VoiceCallStartFrame — First text frame of a socket, sent within 10 s of the upgrade. Opens a run, or attaches a reconnect to it.
    - `type` — object **(required)**
    - `callId` — string **(required)** — Id of the PBX call. Use it to correlate the call events of the run. _(minLen=1)_
    - `flowIndex` — number **(required)** — Index of this run on the call, from 0. _(min=0)_
    - `sessionId` — string **(required)** — Id of this run. The same on every connection of the run; the cloud attaches a reconnect and settles a takeover by it. _(minLen=1; maxLen=128)_
    - `resume` — boolean **(required)** — True when an earlier connection of this run got agent audio (`audio.begin`): the cloud continues that session without a new greeting.
    - `resumeAtMs` — number **(required)** — Run-clock time of the first audio byte of this connection: 0 on the first connection. _(min=0)_
    - `agent` — VoiceCallStartAgent **(required)** — The agent of the run. At most one of `draft` and `version` is set.
      - `id` — string **(required)** — Agent id. _(minLen=12; maxLen=12)_
      - `draft` — boolean — True to run the unpublished draft. Absent or null: false.
      - `version` — number — Published version to run. Absent or null: the version the agent routing selects. _(min=1)_
    - `language` — string **(required)** — Language of the call, for example `en-US`. The agent starts in its configured language that matches it. _(minLen=1)_
    - `caller` — VoiceCallStartCaller **(required)** — Caller identity from the lookup application of the PBX: an external lookup or the local phonebook. Each member is absent, null or empty when unknown.
      - `name` — string
      - `number` — string
      - `email` — string
      - `company` — string
    - `dialedNumber` — string — Number that the caller dialled. Absent, null or empty when unknown.
    - `variables` — string — Base64 of a JSON object of the `VOICEBOT_*` channel variables. Absent, null or empty when there are none. _(pattern=^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$)_
  - `vad` — VoiceCallVadFrame — Voice activity of the caller as the PBX detects it. Sent when the state changes, and every 100 ms while agent audio plays.
    - `type` — object **(required)**
    - `speaking` — boolean **(required)** — True while the caller speaks.
    - `energyDb` — number **(required)** — Energy of the audio frame that produced the report, in dBFS. _(format=double; min=-96; max=0)_
    - `atMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
  - `dtmf` — VoiceCallDtmfFrame — DTMF input that the PBX collected. The cloud takes `digits` as the caller's reply.
    - `type` — object **(required)**
    - `id` — string **(required)** _(minLen=1; maxLen=127)_
    - `digits` — string **(required)** _(pattern=^[0-9*#A-D]{1,64}$)_
  - `playback` — VoiceCallPlaybackFrame — An agent audio stream changed state on the PBX.
    - `type` — object **(required)**
    - `replyId` — string **(required)** _(minLen=1; maxLen=127)_
    - `streamId` — string **(required)** _(minLen=1; maxLen=127)_
    - `event` — string **(required)** — Event of an agent audio stream. _(enum: `started`, `finished`, `stopped`)_
    - `atMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
    - `playedMs` — number — Audio of the stream that played, in ms. Present with `finished` and `stopped`. _(min=0)_
    - `dropped` — boolean — True when the PBX dropped the stream, for example at its queue limit. Only with `stopped`. Absent: false.
  - `end` — VoiceCallEndFrame — The run ended on the PBX. The PBX sends no audio after it and waits up to 3 s for `ended`.
    - `type` — object **(required)**
    - `reason` — string **(required)** — Who ended the run on the PBX. The live events of the call report it as `VoiceCallEndReason`: `caller-hangup` as `hangup`, `agent-hangup` as `complete`, `agent-transfer` as `transfer`, `timeout` as `timeout`. _(enum: `caller-hangup`, `agent-hangup`, `agent-transfer`, `timeout`)_
- `server` — VoiceCallServerFrames — One example of each text message that the server (the cloud) sends on the call socket.
  - `started` — VoiceCallStartedFrame — Answer to `start`: the session of the run is ready on this connection. Sent once per connection, also after a reconnect. Example: `{"type":"started","connectionId":"0f6d…","agent":{"id":"a_qqyHI7xWBH","name":"Support"}}`.
    - `type` — object **(required)**
    - `connectionId` — string **(required)** — Id of this connection. Each connection of the run has its own.
    - `agent` — VoiceCallStartedAgent **(required)** — The agent that answers the run.
      - `id` — string **(required)** — Agent id, as in `start.agent.id`. _(minLen=12; maxLen=12)_
      - `name` — string **(required)** — Display name of the agent.
      - `groupId` — string — Group of the agent. Absent when the agent has none.
    - `backgroundSound` — string — Music-on-hold class that the PBX plays after each caller turn until agent audio starts. Absent: none. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `voiceDetection` — VoiceDetectionSettings — Caller voice detection on the PBX.
      - `silenceMs` — number — Silence in ms that ends the caller speech. Absent: 500. _(min=100; max=5000)_
      - `silenceLevelDb` — number — Mean frame level in dBFS below which caller audio is silence. Absent: -36. _(min=-90; max=0)_
      - `speechLevelDb` — number — Mean frame level in dBFS from which caller audio is speech. Absent: -30. _(min=-90; max=0)_
  - `transcription` — VoiceCallTranscriptionFrame — Words of one party. Partials and the final of one utterance share `id`. For the agent, the words that played.
    - `type` — object **(required)**
    - `party` — string **(required)** — A party of the call. _(enum: `caller`, `callee`)_
    - `id` — string **(required)**
    - `final` — boolean **(required)**
    - `text` — string **(required)**
    - `startMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
    - `endMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
    - `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `confidence` — number — Recogniser confidence from 0 to 1. Absent when the text is not from a recogniser, or the engine gives none. _(format=double; min=0; max=1)_
  - `audioBegin` — VoiceCallAudioBeginFrame — Opens an agent audio stream. Binary audio messages of the stream follow until `audio.end`. Streams do not interleave.
    - `type` — object **(required)**
    - `replyId` — string **(required)**
    - `streamId` — string **(required)**
    - `sampleRate` — number **(required)** — Sample rate of the stream's `pcm_s16le` mono audio in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000. _(min=8000; max=48000)_
  - `audioEnd` — VoiceCallAudioEndFrame — Closes an agent audio stream.
    - `type` — object **(required)**
    - `streamId` — string **(required)**
  - `stop` — VoiceCallStopFrame — Stop every agent audio stream of the run: the one that plays and the ones that wait.
    - `type` — object **(required)**
  - `duck` — VoiceCallDuckFrame — Change the volume of a playing reply. `volumeDb` 0 returns it to full volume.
    - `type` — object **(required)**
    - `replyId` — string **(required)**
    - `volumeDb` — number **(required)** — Target gain in dB. _(min=-90; max=0)_
    - `rampMs` — number **(required)** — Ramp duration in ms. _(min=0; max=1000)_
  - `language` — VoiceCallLanguageFrame — The call continues in another language.
    - `type` — object **(required)**
    - `language` — string **(required)** — Language that the call continues in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `transfer` — VoiceCallTransferFrame — Transfer the call after the queued agent audio plays. Terminal: the PBX answers with `end`.
    - `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
    - `extension` — string **(required)** — Extension of the destination. _(minLen=1)_
    - `type` — object **(required)**
  - `hangup` — VoiceCallHangupFrame — Hang up the call after the queued agent audio plays. Terminal: the PBX answers with `end`.
    - `type` — object **(required)**
  - `error` — VoiceCallErrorFrame — An error on the run. When `retryable` is false, the socket closes after it.
    - `type` — object **(required)**
    - `code` — string **(required)** — Stable error code, for example `START_TIMEOUT`, `PROTOCOL_ERROR` or `STT_FAILED`.
    - `retryable` — boolean **(required)**
    - `message` — string **(required)**
  - `ended` — VoiceCallEndedFrame — Answer to `end`: the cloud processed all audio. The socket closes with close code 1000 after it.
    - `type` — object **(required)**

**`VoiceCallReplyEvent`**

_The caller's completed utterance that started a turn — after the runtime's filler and duplicate filter._

- `id` — string **(required)**
- `text` — string **(required)**
- `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_

**`VoiceCallSayEvent`**

_One sentence the agent speaks, as it is handed to the PBX (after playback sanitizing). Sentences of one reply share `replyId`._

- `replyId` — string **(required)**
- `text` — string **(required)**
- `interruptible` — boolean **(required)**

**`VoiceCallServerFrameType`**

_Value of `type` in a text frame from the server (the cloud)._

- string _(enum: `started`, `transcription`, `audio.begin`, `audio.end`, `stop`, `duck`, `language`, `transfer`, `hangup`, `error`, `ended`)_

**`VoiceCallServerFrames`**

_One example of each text message that the server (the cloud) sends on the call socket._

- `started` — VoiceCallStartedFrame — Answer to `start`: the session of the run is ready on this connection. Sent once per connection, also after a reconnect. Example: `{"type":"started","connectionId":"0f6d…","agent":{"id":"a_qqyHI7xWBH","name":"Support"}}`.
  - `type` — object **(required)**
  - `connectionId` — string **(required)** — Id of this connection. Each connection of the run has its own.
  - `agent` — VoiceCallStartedAgent **(required)** — The agent that answers the run.
    - `id` — string **(required)** — Agent id, as in `start.agent.id`. _(minLen=12; maxLen=12)_
    - `name` — string **(required)** — Display name of the agent.
    - `groupId` — string — Group of the agent. Absent when the agent has none.
  - `backgroundSound` — string — Music-on-hold class that the PBX plays after each caller turn until agent audio starts. Absent: none. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
  - `voiceDetection` — VoiceDetectionSettings — Caller voice detection on the PBX.
    - `silenceMs` — number — Silence in ms that ends the caller speech. Absent: 500. _(min=100; max=5000)_
    - `silenceLevelDb` — number — Mean frame level in dBFS below which caller audio is silence. Absent: -36. _(min=-90; max=0)_
    - `speechLevelDb` — number — Mean frame level in dBFS from which caller audio is speech. Absent: -30. _(min=-90; max=0)_
- `transcription` — VoiceCallTranscriptionFrame — Words of one party. Partials and the final of one utterance share `id`. For the agent, the words that played.
  - `type` — object **(required)**
  - `party` — string **(required)** — A party of the call. _(enum: `caller`, `callee`)_
  - `id` — string **(required)**
  - `final` — boolean **(required)**
  - `text` — string **(required)**
  - `startMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
  - `endMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
  - `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `confidence` — number — Recogniser confidence from 0 to 1. Absent when the text is not from a recogniser, or the engine gives none. _(format=double; min=0; max=1)_
- `audioBegin` — VoiceCallAudioBeginFrame — Opens an agent audio stream. Binary audio messages of the stream follow until `audio.end`. Streams do not interleave.
  - `type` — object **(required)**
  - `replyId` — string **(required)**
  - `streamId` — string **(required)**
  - `sampleRate` — number **(required)** — Sample rate of the stream's `pcm_s16le` mono audio in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000. _(min=8000; max=48000)_
- `audioEnd` — VoiceCallAudioEndFrame — Closes an agent audio stream.
  - `type` — object **(required)**
  - `streamId` — string **(required)**
- `stop` — VoiceCallStopFrame — Stop every agent audio stream of the run: the one that plays and the ones that wait.
  - `type` — object **(required)**
- `duck` — VoiceCallDuckFrame — Change the volume of a playing reply. `volumeDb` 0 returns it to full volume.
  - `type` — object **(required)**
  - `replyId` — string **(required)**
  - `volumeDb` — number **(required)** — Target gain in dB. _(min=-90; max=0)_
  - `rampMs` — number **(required)** — Ramp duration in ms. _(min=0; max=1000)_
- `language` — VoiceCallLanguageFrame — The call continues in another language.
  - `type` — object **(required)**
  - `language` — string **(required)** — Language that the call continues in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `transfer` — VoiceCallTransferFrame — Transfer the call after the queued agent audio plays. Terminal: the PBX answers with `end`.
  - `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
  - `extension` — string **(required)** — Extension of the destination. _(minLen=1)_
  - `type` — object **(required)**
- `hangup` — VoiceCallHangupFrame — Hang up the call after the queued agent audio plays. Terminal: the PBX answers with `end`.
  - `type` — object **(required)**
- `error` — VoiceCallErrorFrame — An error on the run. When `retryable` is false, the socket closes after it.
  - `type` — object **(required)**
  - `code` — string **(required)** — Stable error code, for example `START_TIMEOUT`, `PROTOCOL_ERROR` or `STT_FAILED`.
  - `retryable` — boolean **(required)**
  - `message` — string **(required)**
- `ended` — VoiceCallEndedFrame — Answer to `end`: the cloud processed all audio. The socket closes with close code 1000 after it.
  - `type` — object **(required)**

**`VoiceCallStartAgent`**

_The agent of the run. At most one of `draft` and `version` is set._

- `id` — string **(required)** — Agent id. _(minLen=12; maxLen=12)_
- `draft` — boolean — True to run the unpublished draft. Absent or null: false.
- `version` — number — Published version to run. Absent or null: the version the agent routing selects. _(min=1)_

**`VoiceCallStartCaller`**

_Caller identity from the lookup application of the PBX: an external lookup or the local phonebook. Each member is absent, null or empty when unknown._

- `name` — string
- `number` — string
- `email` — string
- `company` — string

**`VoiceCallStartFrame`**

_First text frame of a socket, sent within 10 s of the upgrade. Opens a run, or attaches a reconnect to it._

- `type` — object **(required)**
- `callId` — string **(required)** — Id of the PBX call. Use it to correlate the call events of the run. _(minLen=1)_
- `flowIndex` — number **(required)** — Index of this run on the call, from 0. _(min=0)_
- `sessionId` — string **(required)** — Id of this run. The same on every connection of the run; the cloud attaches a reconnect and settles a takeover by it. _(minLen=1; maxLen=128)_
- `resume` — boolean **(required)** — True when an earlier connection of this run got agent audio (`audio.begin`): the cloud continues that session without a new greeting.
- `resumeAtMs` — number **(required)** — Run-clock time of the first audio byte of this connection: 0 on the first connection. _(min=0)_
- `agent` — VoiceCallStartAgent **(required)** — The agent of the run. At most one of `draft` and `version` is set.
  - `id` — string **(required)** — Agent id. _(minLen=12; maxLen=12)_
  - `draft` — boolean — True to run the unpublished draft. Absent or null: false.
  - `version` — number — Published version to run. Absent or null: the version the agent routing selects. _(min=1)_
- `language` — string **(required)** — Language of the call, for example `en-US`. The agent starts in its configured language that matches it. _(minLen=1)_
- `caller` — VoiceCallStartCaller **(required)** — Caller identity from the lookup application of the PBX: an external lookup or the local phonebook. Each member is absent, null or empty when unknown.
  - `name` — string
  - `number` — string
  - `email` — string
  - `company` — string
- `dialedNumber` — string — Number that the caller dialled. Absent, null or empty when unknown.
- `variables` — string — Base64 of a JSON object of the `VOICEBOT_*` channel variables. Absent, null or empty when there are none. _(pattern=^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$)_

**`VoiceCallStartedAgent`**

_The agent that answers the run._

- `id` — string **(required)** — Agent id, as in `start.agent.id`. _(minLen=12; maxLen=12)_
- `name` — string **(required)** — Display name of the agent.
- `groupId` — string — Group of the agent. Absent when the agent has none.

**`VoiceCallStartedEvent`**

_The session that answered the call, sent once per session of the call (a transfer starts another)._

- `sessionId` — string **(required)** — Id of the voice session. _(minLen=1; maxLen=128)_
- `traceId` — string — The session's trace, for the LLM-level detail this stream deliberately omits. Absent for a built-in agent, whose trace is not the tenant's to read. _(minLen=1; maxLen=128)_
- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `agentName` — string
- `agentVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
- `agentDraft` — boolean — True when the session runs the agent's draft.
- `language` — string — BCP-47 language the call started in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_

**`VoiceCallStartedFrame`**

_Answer to `start`: the session of the run is ready on this connection. Sent once per connection, also after a reconnect. Example: `{"type":"started","connectionId":"0f6d…","agent":{"id":"a_qqyHI7xWBH","name":"Support"}}`._

- `type` — object **(required)**
- `connectionId` — string **(required)** — Id of this connection. Each connection of the run has its own.
- `agent` — VoiceCallStartedAgent **(required)** — The agent that answers the run.
  - `id` — string **(required)** — Agent id, as in `start.agent.id`. _(minLen=12; maxLen=12)_
  - `name` — string **(required)** — Display name of the agent.
  - `groupId` — string — Group of the agent. Absent when the agent has none.
- `backgroundSound` — string — Music-on-hold class that the PBX plays after each caller turn until agent audio starts. Absent: none. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
- `voiceDetection` — VoiceDetectionSettings — Caller voice detection on the PBX.
  - `silenceMs` — number — Silence in ms that ends the caller speech. Absent: 500. _(min=100; max=5000)_
  - `silenceLevelDb` — number — Mean frame level in dBFS below which caller audio is silence. Absent: -36. _(min=-90; max=0)_
  - `speechLevelDb` — number — Mean frame level in dBFS from which caller audio is speech. Absent: -30. _(min=-90; max=0)_

**`VoiceCallStopFrame`**

_Stop every agent audio stream of the run: the one that plays and the ones that wait._

- `type` — object **(required)**

**`VoiceCallToolEvent`**

_A tool call the agent made during a turn. Name and phase only — arguments and results live in the trace. Sent to a caller signed in to the system; never to a guest._

- `toolCallId` — string **(required)** — Identifies the tool call inside the turn — the model's own call id, not the PBX call this stream follows.
- `toolName` — string **(required)**
- `phase` — string **(required)** — Phase of a tool call of the agent. _(enum: `started`, `finished`)_
- `startMessage` — string — The phrase spoken while the tool runs, when the capability configures one.

**`VoiceCallTranscriptionEvent`**

_A recogniser result for the caller's speech. Interim results (`final: false`) are replaced by the final one with the same `id`._

- `id` — string **(required)**
- `text` — string **(required)**
- `final` — boolean **(required)**
- `language` — string — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `time` — number — Milliseconds since the call started, as the PBX stamps it.
- `finalDropReason` — string — Why the service did not use a final caller transcript as a caller turn. _(enum: `low_confidence`, `other_speaker`)_

**`VoiceCallTranscriptionFrame`**

_Words of one party. Partials and the final of one utterance share `id`. For the agent, the words that played._

- `type` — object **(required)**
- `party` — string **(required)** — A party of the call. _(enum: `caller`, `callee`)_
- `id` — string **(required)**
- `final` — boolean **(required)**
- `text` — string **(required)**
- `startMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
- `endMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_
- `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `confidence` — number — Recogniser confidence from 0 to 1. Absent when the text is not from a recogniser, or the engine gives none. _(format=double; min=0; max=1)_

**`VoiceCallTransferFrame`**

_Transfer the call after the queued agent audio plays. Terminal: the PBX answers with `end`._

- `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
- `extension` — string **(required)** — Extension of the destination. _(minLen=1)_
- `type` — object **(required)**

**`VoiceCallVadFrame`**

_Voice activity of the caller as the PBX detects it. Sent when the state changes, and every 100 ms while agent audio plays._

- `type` — object **(required)**
- `speaking` — boolean **(required)** — True while the caller speaks.
- `energyDb` — number **(required)** — Energy of the audio frame that produced the report, in dBFS. _(format=double; min=-96; max=0)_
- `atMs` — number **(required)** — Run-clock time or duration in ms of PBX audio since the run started. It continues across reconnects. _(min=0)_

**`VoiceCommandType`**

_Value of `type` in the `command` of a command frame._

- string _(enum: `say`, `play`, `stop`, `hangup`, `transfer`)_

**`VoiceCompleteEvent`**

_The call or the conversation is complete, for example because the caller hung up. The service ends the session. The service also accepts `type` `ended` with the same meaning._

- `type` — object **(required)**
- `reason` — string — Why the call is complete. Absent: the value of `type`.
- `time` — number — Time of the completion, in epoch ms. The service ignores it.

**`VoiceConnectParams`**

_Parameters supplied on the WebSocket connect (upgrade) request, as query-string parameters._

- `protocolVersion` — number — Protocol version advertised by the client (query parameter `v`). 0 (or absent) is the legacy PBX protocol; >= 1 enables the sessionStarted event; >= 2 additionally means the client WAITS for `started` before opening its recognition stream and honours the `speech` payload on it; >= 3 additionally means the client connects again with `resume` after close code `1001`, so the service can move the call to another server while it runs.
- `sessionId` — string **(required)** — Caller-supplied session id, unique per connection. _(minLen=1; maxLen=128)_
- `resume` — boolean — True when this connection attaches the running session `sessionId` again, after a close with close code `1001` or a lost connection. The session keeps its history and does not play the greeting again.
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
- `inputMode` — string — How caller speech reaches the service. _(enum: `transcription`)_
- `user` — string — Owner user of the session. Absent: no user. The service ignores it for a PBX token with `callId`. _(minLen=12; maxLen=12)_
- `company` — string — Tenant of the session. Required for a service token, which carries no tenant. For another token a value different from the token tenant gets HTTP 401. _(minLen=3; maxLen=30)_

**`VoiceDetectionSettings`**

_Caller voice detection on the PBX._

- `silenceMs` — number — Silence in ms that ends the caller speech. Absent: 500. _(min=100; max=5000)_
- `silenceLevelDb` — number — Mean frame level in dBFS below which caller audio is silence. Absent: -36. _(min=-90; max=0)_
- `speechLevelDb` — number — Mean frame level in dBFS from which caller audio is speech. Absent: -30. _(min=-90; max=0)_

**`VoiceErrorEvent`**

_An error on the connection. The session continues, unless a `ended` event follows._

- `type` — object **(required)**
- `code` — string **(required)** — Error code. The value is stable.
- `message` — string **(required)** — Description of the error.
- `time` — number **(required)** — Time of the event, in epoch ms.

**`VoiceEventType`**

_Value of `type` in the `event` of an event frame._

- string _(enum: `started`, `ended`, `error`, `transcription`, `agentTranscription`, `reply`, `playback`, `interruption`, `complete`, `thinking`, `tool`)_

**`VoiceHangupCommand`**

_End the session and hang up the call._

- `reason` — string — Why the session ended.
- `type` — object **(required)**

**`VoiceHealthcheckCommand`**

_Liveness check of the service by the client: `{"type": "healthcheck"}`, with no envelope. The service sends no answer._

- `type` — string **(required)** _(default=healthcheck)_

**`VoiceInputMode`**

_How caller speech reaches the service._

- string _(enum: `transcription`)_

**`VoiceInterruptionEvent`**

_The caller spoke over a reply while the client played it._

- `type` — object **(required)**
- `replyId` — string — Reply that the caller interrupted.
- `playedText` — string — Part of the reply that the client played before the interruption.
- `originalText` — string — Full text of the reply.
- `time` — number — Time of the interruption, in epoch ms on the client clock. The service ignores 0.

**`VoicePlayCommand`**

_A chunk of synthesized audio of a reply. `data` is base64 of PCM audio at the sample rate of the `say` command. An empty `data` marks the end of the stream._

- `replyId` — string **(required)**
- `streamId` — string **(required)**
- `data` — string **(required)**
- `type` — object **(required)**

**`VoicePlaybackEvent`**

_Progress of the playback of a reply on the client._

- `type` — object **(required)**
- `replyId` — string — Reply that the client plays.
- `text` — string — Text of the reply that the client played.
- `complete` — boolean **(required)** — True when the client played the reply to its end.
- `startTime` — number — Start of the playback, in epoch ms on the client clock. The service ignores 0.
- `endTime` — number — End of the playback, in epoch ms on the client clock. The service ignores 0.

**`VoicePronunciation`**

_A pronunciation rule for one phrase. Belongs to a LANGUAGE, not to the agent: 'Wildix' is respelled differently for an Italian and a German voice, so one list shared ACROSS languages would fight itself. That is why the rules hang off the language and nowhere else — there is no company-wide dictionary above them to inherit from, or to disagree with._

- `phrase` — string **(required)** — The phrase as it appears in the text, e.g. 'Wildix'. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
- `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA), e.g. 'Wil-dix'. _(maxLen=200)_
- `encoding` — string — How the `as` member of a pronunciation rule is written. _(enum: `alias`, `ipa`)_

**`VoicePronunciationEncoding`**

_How the `as` member of a pronunciation rule is written._

- string _(enum: `alias`, `ipa`)_

**`VoiceReplyEvent`**

_A final caller utterance. It starts an agent turn._

- `type` — object **(required)**
- `id` — string — Id of the utterance. Absent: the service makes a new id.
- `text` — string **(required)** — Text of the utterance. Must not be empty. _(minLen=1)_
- `time` — number — Time of the utterance, in epoch ms. Absent: the time when the service received it.
- `language` — string — Language that the recogniser identified for the utterance. A value that is different from the conversation language changes the conversation language. When the utterance has segments in more than one language, send the language of the last segment. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `confidence` — number — Confidence of the recogniser for the utterance. The service ignores a value outside 0 to 1. _(format=double)_
- `startTime` — number — Start of the speech, in epoch ms on the client clock. The service ignores 0.
- `endTime` — number — End of the speech, in epoch ms on the client clock. The service ignores 0.

**`VoiceSayCommand`**

_Play a reply to the caller. When `audio` is present, the service sends the audio of the reply in `play` commands. When `audio` is absent, the client shows `text` or synthesizes it itself._

- `text` — string **(required)** — Text of the reply.
- `replyId` — string **(required)** — Id of the reply.
- `interruptible` — boolean — True when the caller can interrupt the reply.
- `audio` — VoiceSayCommandAudioOptions — Audio of a reply that the service synthesizes. `play` commands with this stream id follow the `say` command.
  - `streamId` — string **(required)**
  - `sampleRate` — number **(required)** — Sample rate of the `pcm_s16le` mono audio of the `play` commands, in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000.
- `type` — object **(required)**

**`VoiceSayCommandAudioOptions`**

_Audio of a reply that the service synthesizes. `play` commands with this stream id follow the `say` command._

- `streamId` — string **(required)**
- `sampleRate` — number **(required)** — Sample rate of the `pcm_s16le` mono audio of the `play` commands, in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000.

**`VoiceSessionEndedEvent`**

_The session ended. This is the last event of the session._

- `type` — object **(required)**
- `reason` — string — Why the session ended.
- `error` — string — Present when the session ended because of an error.
- `time` — number **(required)** — Time of the event, in epoch ms.

**`VoiceSessionStartedEvent`**

_The session is ready. Sent once after the handshake, on the PBX voice socket only when the client sends protocol version 1 or more._

- `type` — object **(required)**
- `time` — number **(required)** — Time of the event, in epoch ms.
- `sessionId` — string **(required)** — Id of the session. _(minLen=1; maxLen=128)_
- `agentId` — string **(required)** — Agent of the session. _(minLen=12; maxLen=12)_
- `agentVersion` — number — Published agent version of the session. Absent when the session runs the agent draft. _(min=1)_
- `traceId` — string — Trace of the session. It does not change during the session. _(minLen=1; maxLen=128)_
- `agentName` — string — Display name of the agent.
- `category` — string — Category of the agent.
- `groupId` — string — PBX group of the agent, for data access control. Empty when the agent has no group.
- `speech` — VoiceSpeechPayload — Speech recognition settings of the call. The client applies them to its recogniser.
  - `engine` — string **(required)** — Recogniser URI. Always present. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
  - `languages` — array **(required)** — All configured languages. These are the candidates for language identification.
    - _array of_ `string`
  - `preferredLanguage` — string **(required)** — Language at the start of the call. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `autoDetect` — boolean **(required)** — True to identify the spoken language of each utterance. False when `languages` has fewer languages than the recogniser needs, or when the recogniser cannot identify languages.
- `backgroundSound` — string — Music-on-hold class to play as background sound of the call. Absent: no background sound. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_

**`VoiceSpeechPayload`**

_Speech recognition settings of the call. The client applies them to its recogniser._

- `engine` — string **(required)** — Recogniser URI. Always present. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `languages` — array **(required)** — All configured languages. These are the candidates for language identification.
  - _array of_ `string`
- `preferredLanguage` — string **(required)** — Language at the start of the call. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `autoDetect` — boolean **(required)** — True to identify the spoken language of each utterance. False when `languages` has fewer languages than the recogniser needs, or when the recogniser cannot identify languages.

**`VoiceStopCommand`**

_Stop the audio of the agent._

- `type` — object **(required)**

**`VoiceTextClientFrames`**

_One example of each message that the client sends on the text socket. An event goes in `{"type": "event", "event": {...}}`; `healthcheck` has no envelope._

- `healthcheck` — VoiceHealthcheckCommand — Liveness check of the service by the client: `{"type": "healthcheck"}`, with no envelope. The service sends no answer.
  - `type` — string **(required)** _(default=healthcheck)_
- `transcription` — VoiceTranscriptionEvent — A transcription chunk of caller speech. A client that does its own speech-to-text sends it. When the service does the speech-to-text, the service sends it to the client.
  - `type` — object **(required)**
  - `id` — string — Id of the utterance. The interim chunks and the final chunk of one utterance have the same id. Absent: the service makes a new id.
  - `text` — string **(required)** — Text of the chunk. Must not be empty. _(minLen=1)_
  - `confidence` — number — Confidence of the recogniser. The service ignores a value outside 0 to 1. _(format=double)_
  - `final` — boolean — True when the chunk is the final transcript of the utterance. False for an interim result. Absent: true.
  - `language` — string — Language that the recogniser identified for the chunk. The service records it and does not change the conversation language. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `time` — number — Time of the chunk, in epoch ms. Absent: the time when the service received it.
- `agentTranscription` — VoiceAgentTranscriptionEvent — A transcription chunk of the agent speech, as the caller hears it. It does not start a turn.
  - `type` — object **(required)**
  - `id` — string — Id of the utterance. Absent: the service makes a new id.
  - `text` — string **(required)** — Text of the chunk. Must not be empty. _(minLen=1)_
  - `confidence` — number — Confidence of the recogniser. The service does not record it. _(format=double)_
  - `final` — boolean — True when the chunk is the final transcript of the utterance. False for an interim result. Absent: true.
  - `language` — string — Language that the recogniser identified for the chunk. The service records it and does not change the conversation language. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `time` — number — Time of the chunk, in epoch ms. Absent: the time when the service received it.
- `reply` — VoiceReplyEvent — A final caller utterance. It starts an agent turn.
  - `type` — object **(required)**
  - `id` — string — Id of the utterance. Absent: the service makes a new id.
  - `text` — string **(required)** — Text of the utterance. Must not be empty. _(minLen=1)_
  - `time` — number — Time of the utterance, in epoch ms. Absent: the time when the service received it.
  - `language` — string — Language that the recogniser identified for the utterance. A value that is different from the conversation language changes the conversation language. When the utterance has segments in more than one language, send the language of the last segment. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `confidence` — number — Confidence of the recogniser for the utterance. The service ignores a value outside 0 to 1. _(format=double)_
  - `startTime` — number — Start of the speech, in epoch ms on the client clock. The service ignores 0.
  - `endTime` — number — End of the speech, in epoch ms on the client clock. The service ignores 0.
- `playback` — VoicePlaybackEvent — Progress of the playback of a reply on the client.
  - `type` — object **(required)**
  - `replyId` — string — Reply that the client plays.
  - `text` — string — Text of the reply that the client played.
  - `complete` — boolean **(required)** — True when the client played the reply to its end.
  - `startTime` — number — Start of the playback, in epoch ms on the client clock. The service ignores 0.
  - `endTime` — number — End of the playback, in epoch ms on the client clock. The service ignores 0.
- `interruption` — VoiceInterruptionEvent — The caller spoke over a reply while the client played it.
  - `type` — object **(required)**
  - `replyId` — string — Reply that the caller interrupted.
  - `playedText` — string — Part of the reply that the client played before the interruption.
  - `originalText` — string — Full text of the reply.
  - `time` — number — Time of the interruption, in epoch ms on the client clock. The service ignores 0.
- `complete` — VoiceCompleteEvent — The call or the conversation is complete, for example because the caller hung up. The service ends the session. The service also accepts `type` `ended` with the same meaning.
  - `type` — object **(required)**
  - `reason` — string — Why the call is complete. Absent: the value of `type`.
  - `time` — number — Time of the completion, in epoch ms. The service ignores it.

**`VoiceTextProtocolFrames`**

_The connect parameters and the messages of the text socket `/v2/voice/ws`._

- `connectParams` — VoiceConnectParams — Parameters supplied on the WebSocket connect (upgrade) request, as query-string parameters.
  - `protocolVersion` — number — Protocol version advertised by the client (query parameter `v`). 0 (or absent) is the legacy PBX protocol; >= 1 enables the sessionStarted event; >= 2 additionally means the client WAITS for `started` before opening its recognition stream and honours the `speech` payload on it; >= 3 additionally means the client connects again with `resume` after close code `1001`, so the service can move the call to another server while it runs.
  - `sessionId` — string **(required)** — Caller-supplied session id, unique per connection. _(minLen=1; maxLen=128)_
  - `resume` — boolean — True when this connection attaches the running session `sessionId` again, after a close with close code `1001` or a lost connection. The session keeps its history and does not play the greeting again.
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
  - `inputMode` — string — How caller speech reaches the service. _(enum: `transcription`)_
  - `user` — string — Owner user of the session. Absent: no user. The service ignores it for a PBX token with `callId`. _(minLen=12; maxLen=12)_
  - `company` — string — Tenant of the session. Required for a service token, which carries no tenant. For another token a value different from the token tenant gets HTTP 401. _(minLen=3; maxLen=30)_
- `client` — VoiceTextClientFrames — One example of each message that the client sends on the text socket. An event goes in `{"type": "event", "event": {...}}`; `healthcheck` has no envelope.
  - `healthcheck` — VoiceHealthcheckCommand — Liveness check of the service by the client: `{"type": "healthcheck"}`, with no envelope. The service sends no answer.
    - `type` — string **(required)** _(default=healthcheck)_
  - `transcription` — VoiceTranscriptionEvent — A transcription chunk of caller speech. A client that does its own speech-to-text sends it. When the service does the speech-to-text, the service sends it to the client.
    - `type` — object **(required)**
    - `id` — string — Id of the utterance. The interim chunks and the final chunk of one utterance have the same id. Absent: the service makes a new id.
    - `text` — string **(required)** — Text of the chunk. Must not be empty. _(minLen=1)_
    - `confidence` — number — Confidence of the recogniser. The service ignores a value outside 0 to 1. _(format=double)_
    - `final` — boolean — True when the chunk is the final transcript of the utterance. False for an interim result. Absent: true.
    - `language` — string — Language that the recogniser identified for the chunk. The service records it and does not change the conversation language. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `time` — number — Time of the chunk, in epoch ms. Absent: the time when the service received it.
  - `agentTranscription` — VoiceAgentTranscriptionEvent — A transcription chunk of the agent speech, as the caller hears it. It does not start a turn.
    - `type` — object **(required)**
    - `id` — string — Id of the utterance. Absent: the service makes a new id.
    - `text` — string **(required)** — Text of the chunk. Must not be empty. _(minLen=1)_
    - `confidence` — number — Confidence of the recogniser. The service does not record it. _(format=double)_
    - `final` — boolean — True when the chunk is the final transcript of the utterance. False for an interim result. Absent: true.
    - `language` — string — Language that the recogniser identified for the chunk. The service records it and does not change the conversation language. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `time` — number — Time of the chunk, in epoch ms. Absent: the time when the service received it.
  - `reply` — VoiceReplyEvent — A final caller utterance. It starts an agent turn.
    - `type` — object **(required)**
    - `id` — string — Id of the utterance. Absent: the service makes a new id.
    - `text` — string **(required)** — Text of the utterance. Must not be empty. _(minLen=1)_
    - `time` — number — Time of the utterance, in epoch ms. Absent: the time when the service received it.
    - `language` — string — Language that the recogniser identified for the utterance. A value that is different from the conversation language changes the conversation language. When the utterance has segments in more than one language, send the language of the last segment. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `confidence` — number — Confidence of the recogniser for the utterance. The service ignores a value outside 0 to 1. _(format=double)_
    - `startTime` — number — Start of the speech, in epoch ms on the client clock. The service ignores 0.
    - `endTime` — number — End of the speech, in epoch ms on the client clock. The service ignores 0.
  - `playback` — VoicePlaybackEvent — Progress of the playback of a reply on the client.
    - `type` — object **(required)**
    - `replyId` — string — Reply that the client plays.
    - `text` — string — Text of the reply that the client played.
    - `complete` — boolean **(required)** — True when the client played the reply to its end.
    - `startTime` — number — Start of the playback, in epoch ms on the client clock. The service ignores 0.
    - `endTime` — number — End of the playback, in epoch ms on the client clock. The service ignores 0.
  - `interruption` — VoiceInterruptionEvent — The caller spoke over a reply while the client played it.
    - `type` — object **(required)**
    - `replyId` — string — Reply that the caller interrupted.
    - `playedText` — string — Part of the reply that the client played before the interruption.
    - `originalText` — string — Full text of the reply.
    - `time` — number — Time of the interruption, in epoch ms on the client clock. The service ignores 0.
  - `complete` — VoiceCompleteEvent — The call or the conversation is complete, for example because the caller hung up. The service ends the session. The service also accepts `type` `ended` with the same meaning.
    - `type` — object **(required)**
    - `reason` — string — Why the call is complete. Absent: the value of `type`.
    - `time` — number — Time of the completion, in epoch ms. The service ignores it.
- `server` — VoiceTextServerFrames — One example of each message that the server sends on the text socket. An event goes in `{"type": "event", "event": {...}}`, a command in `{"type": "command", "command": {...}}`.
  - `started` — VoiceSessionStartedEvent — The session is ready. Sent once after the handshake, on the PBX voice socket only when the client sends protocol version 1 or more.
    - `type` — object **(required)**
    - `time` — number **(required)** — Time of the event, in epoch ms.
    - `sessionId` — string **(required)** — Id of the session. _(minLen=1; maxLen=128)_
    - `agentId` — string **(required)** — Agent of the session. _(minLen=12; maxLen=12)_
    - `agentVersion` — number — Published agent version of the session. Absent when the session runs the agent draft. _(min=1)_
    - `traceId` — string — Trace of the session. It does not change during the session. _(minLen=1; maxLen=128)_
    - `agentName` — string — Display name of the agent.
    - `category` — string — Category of the agent.
    - `groupId` — string — PBX group of the agent, for data access control. Empty when the agent has no group.
    - `speech` — VoiceSpeechPayload — Speech recognition settings of the call. The client applies them to its recogniser.
      - `engine` — string **(required)** — Recogniser URI. Always present. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `languages` — array **(required)** — All configured languages. These are the candidates for language identification.
        - _array of_ `string`
      - `preferredLanguage` — string **(required)** — Language at the start of the call. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `autoDetect` — boolean **(required)** — True to identify the spoken language of each utterance. False when `languages` has fewer languages than the recogniser needs, or when the recogniser cannot identify languages.
    - `backgroundSound` — string — Music-on-hold class to play as background sound of the call. Absent: no background sound. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
  - `ended` — VoiceSessionEndedEvent — The session ended. This is the last event of the session.
    - `type` — object **(required)**
    - `reason` — string — Why the session ended.
    - `error` — string — Present when the session ended because of an error.
    - `time` — number **(required)** — Time of the event, in epoch ms.
  - `error` — VoiceErrorEvent — An error on the connection. The session continues, unless a `ended` event follows.
    - `type` — object **(required)**
    - `code` — string **(required)** — Error code. The value is stable.
    - `message` — string **(required)** — Description of the error.
    - `time` — number **(required)** — Time of the event, in epoch ms.
  - `say` — VoiceSayCommand — Play a reply to the caller. When `audio` is present, the service sends the audio of the reply in `play` commands. When `audio` is absent, the client shows `text` or synthesizes it itself.
    - `text` — string **(required)** — Text of the reply.
    - `replyId` — string **(required)** — Id of the reply.
    - `interruptible` — boolean — True when the caller can interrupt the reply.
    - `audio` — VoiceSayCommandAudioOptions — Audio of a reply that the service synthesizes. `play` commands with this stream id follow the `say` command.
      - `streamId` — string **(required)**
      - `sampleRate` — number **(required)** — Sample rate of the `pcm_s16le` mono audio of the `play` commands, in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000.
    - `type` — object **(required)**
  - `play` — VoicePlayCommand — A chunk of synthesized audio of a reply. `data` is base64 of PCM audio at the sample rate of the `say` command. An empty `data` marks the end of the stream.
    - `replyId` — string **(required)**
    - `streamId` — string **(required)**
    - `data` — string **(required)**
    - `type` — object **(required)**
  - `stop` — VoiceStopCommand — Stop the audio of the agent.
    - `type` — object **(required)**
  - `hangup` — VoiceHangupCommand — End the session and hang up the call.
    - `reason` — string — Why the session ended.
    - `type` — object **(required)**
  - `transfer` — VoiceTransferCommand — Transfer the call to a PBX destination and end the session. Only a PBX client does the transfer.
    - `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
    - `extension` — string **(required)** — Extension of the destination. _(minLen=1)_
    - `type` — object **(required)**

**`VoiceTextServerFrames`**

_One example of each message that the server sends on the text socket. An event goes in `{"type": "event", "event": {...}}`, a command in `{"type": "command", "command": {...}}`._

- `started` — VoiceSessionStartedEvent — The session is ready. Sent once after the handshake, on the PBX voice socket only when the client sends protocol version 1 or more.
  - `type` — object **(required)**
  - `time` — number **(required)** — Time of the event, in epoch ms.
  - `sessionId` — string **(required)** — Id of the session. _(minLen=1; maxLen=128)_
  - `agentId` — string **(required)** — Agent of the session. _(minLen=12; maxLen=12)_
  - `agentVersion` — number — Published agent version of the session. Absent when the session runs the agent draft. _(min=1)_
  - `traceId` — string — Trace of the session. It does not change during the session. _(minLen=1; maxLen=128)_
  - `agentName` — string — Display name of the agent.
  - `category` — string — Category of the agent.
  - `groupId` — string — PBX group of the agent, for data access control. Empty when the agent has no group.
  - `speech` — VoiceSpeechPayload — Speech recognition settings of the call. The client applies them to its recogniser.
    - `engine` — string **(required)** — Recogniser URI. Always present. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `languages` — array **(required)** — All configured languages. These are the candidates for language identification.
      - _array of_ `string`
    - `preferredLanguage` — string **(required)** — Language at the start of the call. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `autoDetect` — boolean **(required)** — True to identify the spoken language of each utterance. False when `languages` has fewer languages than the recogniser needs, or when the recogniser cannot identify languages.
  - `backgroundSound` — string — Music-on-hold class to play as background sound of the call. Absent: no background sound. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
- `ended` — VoiceSessionEndedEvent — The session ended. This is the last event of the session.
  - `type` — object **(required)**
  - `reason` — string — Why the session ended.
  - `error` — string — Present when the session ended because of an error.
  - `time` — number **(required)** — Time of the event, in epoch ms.
- `error` — VoiceErrorEvent — An error on the connection. The session continues, unless a `ended` event follows.
  - `type` — object **(required)**
  - `code` — string **(required)** — Error code. The value is stable.
  - `message` — string **(required)** — Description of the error.
  - `time` — number **(required)** — Time of the event, in epoch ms.
- `say` — VoiceSayCommand — Play a reply to the caller. When `audio` is present, the service sends the audio of the reply in `play` commands. When `audio` is absent, the client shows `text` or synthesizes it itself.
  - `text` — string **(required)** — Text of the reply.
  - `replyId` — string **(required)** — Id of the reply.
  - `interruptible` — boolean — True when the caller can interrupt the reply.
  - `audio` — VoiceSayCommandAudioOptions — Audio of a reply that the service synthesizes. `play` commands with this stream id follow the `say` command.
    - `streamId` — string **(required)**
    - `sampleRate` — number **(required)** — Sample rate of the `pcm_s16le` mono audio of the `play` commands, in Hz: 8000, 12000, 16000, 24000, 32000, 44100 or 48000.
  - `type` — object **(required)**
- `play` — VoicePlayCommand — A chunk of synthesized audio of a reply. `data` is base64 of PCM audio at the sample rate of the `say` command. An empty `data` marks the end of the stream.
  - `replyId` — string **(required)**
  - `streamId` — string **(required)**
  - `data` — string **(required)**
  - `type` — object **(required)**
- `stop` — VoiceStopCommand — Stop the audio of the agent.
  - `type` — object **(required)**
- `hangup` — VoiceHangupCommand — End the session and hang up the call.
  - `reason` — string — Why the session ended.
  - `type` — object **(required)**
- `transfer` — VoiceTransferCommand — Transfer the call to a PBX destination and end the session. Only a PBX client does the transfer.
  - `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
  - `extension` — string **(required)** — Extension of the destination. _(minLen=1)_
  - `type` — object **(required)**

**`VoiceToolPhase`**

_Phase of a tool call of the agent._

- string _(enum: `started`, `finished`)_

**`VoiceTranscriptionDropReason`**

_Why the service did not use a final caller transcript as a caller turn._

- string _(enum: `low_confidence`, `other_speaker`)_

**`VoiceTranscriptionEvent`**

_A transcription chunk of caller speech. A client that does its own speech-to-text sends it. When the service does the speech-to-text, the service sends it to the client._

- `type` — object **(required)**
- `id` — string — Id of the utterance. The interim chunks and the final chunk of one utterance have the same id. Absent: the service makes a new id.
- `text` — string **(required)** — Text of the chunk. Must not be empty. _(minLen=1)_
- `confidence` — number — Confidence of the recogniser. The service ignores a value outside 0 to 1. _(format=double)_
- `final` — boolean — True when the chunk is the final transcript of the utterance. False for an interim result. Absent: true.
- `language` — string — Language that the recogniser identified for the chunk. The service records it and does not change the conversation language. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `time` — number — Time of the chunk, in epoch ms. Absent: the time when the service received it.

**`VoiceTransferCommand`**

_Transfer the call to a PBX destination and end the session. Only a PBX client does the transfer._

- `context` — string **(required)** — Dialplan context of the destination. _(minLen=1)_
- `extension` — string **(required)** — Extension of the destination. _(minLen=1)_
- `type` — object **(required)**

</details>
