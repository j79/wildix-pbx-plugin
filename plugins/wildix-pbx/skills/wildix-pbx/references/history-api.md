## History API

_OpenAPI: WDA History service — version v2_

**Servers**

- `https://wda.wildix.com` — Production
- `https://wda-stable.wildix.com` — Stable
- `https://wda-stage.wildix.com` — Stage

### Other

#### `GET` `/v2/history/calls/{callId}/flows/{flowIndex}`

Gets a call by callId and flowIndex.

- operationId: `GetCall`
- **Scopes**: `history:GetCall`, `history:read`
- **Parameters**
  - `callId` (path) — string **(required)**
  - `flowIndex` (path) — number **(required)**
  - `company` (query) — string
- **Response 200** (`GetCallResponseContent`)
  - `call` — CallRecord **(required)**
    - `flowIndex` — number **(required)**
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
    - `connectTime` — number — Duration when the called party's phone rang (Ring Time in UI)
    - `talkTime` — number — Duration of conversation from the moment the call is answered until it ends, excluding hold time
    - `waitTime` — number — Duration spent on IVR, dialplan applications, playback, etc. before the call is answered
    - `queueTime` — number — Duration of call waiting in queue
    - `holdTime` — number — Duration the call was on hold after being answered
    - `duration` — number **(required)** — Total duration = connectTime + waitTime + queueTime + talkTime + holdTime
    - `caller` — CallParticipant
      - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
      - `phone` — string
      - `name` — string
      - `company` — string _(minLen=3; maxLen=30)_
      - `email` — string
      - `userId` — string
      - `userExtension` — string
      - `userDepartment` — string
      - `groupId` — string
      - `groupName` — string
      - `userAgent` — string
      - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
      - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
      - `license` — string
      - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
      - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
      - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
      - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
    - `callee` — CallParticipant
      - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
      - `phone` — string
      - `name` — string
      - `company` — string _(minLen=3; maxLen=30)_
      - `email` — string
      - `userId` — string
      - `userExtension` — string
      - `userDepartment` — string
      - `groupId` — string
      - `groupName` — string
      - `userAgent` — string
      - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
      - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
      - `license` — string
      - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
      - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
      - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
      - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
    - `service` — string
    - `serviceNumber` — string
    - `destination` — string
    - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
    - `trunkName` — string
    - `trunkDirection` — string
    - `queueName` — string
    - `queueId` — string
    - `queuePosition` — number — Position of the call in the queue (1-based). Updated from consume events and emitted on live progress and record flows.
    - `tags` — array
      - _array of_ `string`
    - `flags` — array
      - _array of_ `string`
    - `callerMos` — string
    - `calleeMos` — string
    - `xhoppersConfId` — string
    - `recordings` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
      - _array of_ `string`
    - `recordingsData` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
      - _array of_ `CallFlowRecording`
        - `fileName` — string **(required)**
        - `start` — number **(required)**
        - `end` — number **(required)**
        - `owner` — string **(required)** _(enum: `callee`, `caller`, `system`)_
        - `url` — string **(required)**
        - `pauses` — array **(required)**
          - _array of_ `CallRecordPause`
            - `start` — number
            - `end` — number
            - `reason` — string _(enum: `pause`, `hold`)_
    - `mergeWith` — string
    - `splitReason` — string
    - `splitTransferType` — string
    - `remotePhone` — string
    - `remotePhoneCountryCode` — number
    - `remotePhoneCountryCodeStr` — string
    - `remotePhoneLocation` — string
    - `callStatus` — string _(enum: `COMPLETED`, `MISSED`)_
    - `transcriptionStatus` — string _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
    - `transcriptionLanguage` — string
    - `transcriptionSeconds` — number
    - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
    - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
      - _map of_ `Annotation`
        - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
        - `time` — number **(required)**
        - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
        - `payload` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`tag`**
              - `tag` — string **(required)** _(maxLen=50)_
            - **`text`**
              - `text` — string **(required)** _(maxLen=4096)_
            - **`variables`**
              - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationVariablesValue` in the Schemas appendix)_
            - **`result`**
              - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationResultValue` in the Schemas appendix)_
            - **`metric`**
              - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationMetricValue` in the Schemas appendix)_
        - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
          - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
          - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
          - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).
    - `attachment` — string — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
    - `attachmentType` — string _(enum: `VOICEMAIL`, `FAX`)_
    - `attachmentDestinations` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
      - _array of_ `CallFlowAttachmentDestination`
        - `phone` — string
        - `name` — string
        - `email` — string
        - `userId` — string
        - `userExtension` — string
        - `userDepartment` — string
        - `groupId` — string
        - `groupName` — string
    - `attachments` — array
      - _array of_ `CallFlowAttachment`
        - _oneOf_ — exactly one of:
          - **`recording`**
            - `recording` — CallFlowRecording **(required)**
              - `fileName` — string **(required)**
              - `start` — number **(required)**
              - `end` — number **(required)**
              - `owner` — string **(required)** _(enum: `callee`, `caller`, `system`)_
              - `url` — string **(required)**
              - `pauses` — array **(required)**
                - _(nesting depth limit — see `CallRecordPause` in the Schemas appendix)_
          - **`fax`**
            - `fax` — CallFlowFax **(required)**
              - `url` — string **(required)**
              - `status` — string _(enum: `ok`, `error`)_
              - `destinations` — array
                - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
              - `owner` — string _(enum: `callee`, `caller`, `system`)_
              - `error` — string — Text with the reason for the error in case of unsuccessful fax delivery
          - **`voicemail`**
            - `voicemail` — CallFlowVoicemail **(required)**
              - `url` — string **(required)**
              - `destinations` — array
                - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
              - `owner` — string _(enum: `callee`, `caller`, `system`)_
    - `notifications` — CallFlowNotifications
      - `destinations` — array
        - _array of_ `CallFlowAttachmentDestination`
          - `phone` — string
          - `name` — string
          - `email` — string
          - `userId` — string
          - `userExtension` — string
          - `userDepartment` — string
          - `groupId` — string
          - `groupName` — string
      - `type` — array
        - _array of_ `string`
    - `id` — string **(required)**
    - `pbx` — string **(required)**
    - `time` — number **(required)**
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `licenses` — array **(required)**
      - _array of_ `License`
    - `type` — object **(required)**
- Errors: `400`, `403`, `404`

#### `PUT` `/v2/history/calls/{callId}/flows/{flowIndex}`

Updates a call by callId and flowIndex. Allows modifying call metadata such as tags.

- operationId: `UpdateCall`
- **Scopes**: `history:UpdateCall`
- **Parameters**
  - `callId` (path) — string **(required)**
  - `flowIndex` (path) — number **(required)**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateCallRequestContent`)
  - `tags` — array
    - _array of_ `string`
- **Response 200** (`UpdateCallResponseContent`)
  - `call` — CallRecord **(required)**
    - `flowIndex` — number **(required)**
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
    - `connectTime` — number — Duration when the called party's phone rang (Ring Time in UI)
    - `talkTime` — number — Duration of conversation from the moment the call is answered until it ends, excluding hold time
    - `waitTime` — number — Duration spent on IVR, dialplan applications, playback, etc. before the call is answered
    - `queueTime` — number — Duration of call waiting in queue
    - `holdTime` — number — Duration the call was on hold after being answered
    - `duration` — number **(required)** — Total duration = connectTime + waitTime + queueTime + talkTime + holdTime
    - `caller` — CallParticipant
      - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
      - `phone` — string
      - `name` — string
      - `company` — string _(minLen=3; maxLen=30)_
      - `email` — string
      - `userId` — string
      - `userExtension` — string
      - `userDepartment` — string
      - `groupId` — string
      - `groupName` — string
      - `userAgent` — string
      - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
      - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
      - `license` — string
      - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
      - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
      - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
      - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
    - `callee` — CallParticipant
      - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
      - `phone` — string
      - `name` — string
      - `company` — string _(minLen=3; maxLen=30)_
      - `email` — string
      - `userId` — string
      - `userExtension` — string
      - `userDepartment` — string
      - `groupId` — string
      - `groupName` — string
      - `userAgent` — string
      - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
      - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
      - `license` — string
      - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
      - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
      - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
      - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
    - `service` — string
    - `serviceNumber` — string
    - `destination` — string
    - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
    - `trunkName` — string
    - `trunkDirection` — string
    - `queueName` — string
    - `queueId` — string
    - `queuePosition` — number — Position of the call in the queue (1-based). Updated from consume events and emitted on live progress and record flows.
    - `tags` — array
      - _array of_ `string`
    - `flags` — array
      - _array of_ `string`
    - `callerMos` — string
    - `calleeMos` — string
    - `xhoppersConfId` — string
    - `recordings` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
      - _array of_ `string`
    - `recordingsData` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
      - _array of_ `CallFlowRecording`
        - `fileName` — string **(required)**
        - `start` — number **(required)**
        - `end` — number **(required)**
        - `owner` — string **(required)** _(enum: `callee`, `caller`, `system`)_
        - `url` — string **(required)**
        - `pauses` — array **(required)**
          - _array of_ `CallRecordPause`
            - `start` — number
            - `end` — number
            - `reason` — string _(enum: `pause`, `hold`)_
    - `mergeWith` — string
    - `splitReason` — string
    - `splitTransferType` — string
    - `remotePhone` — string
    - `remotePhoneCountryCode` — number
    - `remotePhoneCountryCodeStr` — string
    - `remotePhoneLocation` — string
    - `callStatus` — string _(enum: `COMPLETED`, `MISSED`)_
    - `transcriptionStatus` — string _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
    - `transcriptionLanguage` — string
    - `transcriptionSeconds` — number
    - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
    - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
      - _map of_ `Annotation`
        - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
        - `time` — number **(required)**
        - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
        - `payload` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`tag`**
              - `tag` — string **(required)** _(maxLen=50)_
            - **`text`**
              - `text` — string **(required)** _(maxLen=4096)_
            - **`variables`**
              - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationVariablesValue` in the Schemas appendix)_
            - **`result`**
              - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationResultValue` in the Schemas appendix)_
            - **`metric`**
              - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationMetricValue` in the Schemas appendix)_
        - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
          - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
          - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
          - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).
    - `attachment` — string — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
    - `attachmentType` — string _(enum: `VOICEMAIL`, `FAX`)_
    - `attachmentDestinations` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
      - _array of_ `CallFlowAttachmentDestination`
        - `phone` — string
        - `name` — string
        - `email` — string
        - `userId` — string
        - `userExtension` — string
        - `userDepartment` — string
        - `groupId` — string
        - `groupName` — string
    - `attachments` — array
      - _array of_ `CallFlowAttachment`
        - _oneOf_ — exactly one of:
          - **`recording`**
            - `recording` — CallFlowRecording **(required)**
              - `fileName` — string **(required)**
              - `start` — number **(required)**
              - `end` — number **(required)**
              - `owner` — string **(required)** _(enum: `callee`, `caller`, `system`)_
              - `url` — string **(required)**
              - `pauses` — array **(required)**
                - _(nesting depth limit — see `CallRecordPause` in the Schemas appendix)_
          - **`fax`**
            - `fax` — CallFlowFax **(required)**
              - `url` — string **(required)**
              - `status` — string _(enum: `ok`, `error`)_
              - `destinations` — array
                - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
              - `owner` — string _(enum: `callee`, `caller`, `system`)_
              - `error` — string — Text with the reason for the error in case of unsuccessful fax delivery
          - **`voicemail`**
            - `voicemail` — CallFlowVoicemail **(required)**
              - `url` — string **(required)**
              - `destinations` — array
                - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
              - `owner` — string _(enum: `callee`, `caller`, `system`)_
    - `notifications` — CallFlowNotifications
      - `destinations` — array
        - _array of_ `CallFlowAttachmentDestination`
          - `phone` — string
          - `name` — string
          - `email` — string
          - `userId` — string
          - `userExtension` — string
          - `userDepartment` — string
          - `groupId` — string
          - `groupName` — string
      - `type` — array
        - _array of_ `string`
    - `id` — string **(required)**
    - `pbx` — string **(required)**
    - `time` — number **(required)**
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `licenses` — array **(required)**
      - _array of_ `License`
    - `type` — object **(required)**
- Errors: `400`, `403`, `404`

#### `GET` `/v2/history/calls/{callId}/flows/{flowIndex}/annotations`

Gets annotations for a call by callId and flowIndex.

- operationId: `GetCallAnnotations`
- **Scopes**: `history:GetCallAnnotations`, `history:read`
- **Parameters**
  - `callId` (path) — string **(required)**
  - `flowIndex` (path) — number **(required)**
  - `company` (query) — string
- **Response 200** (`GetCallAnnotationsResponseContent`)
  - `annotations` — CallAnnotationsRecord **(required)**
    - `id` — string **(required)**
    - `pbx` — string **(required)**
    - `time` — number **(required)**
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `licenses` — array **(required)**
      - _array of_ `License`
    - `type` — object **(required)**
    - `flowIndex` — number **(required)**
    - `flowStartTime` — number **(required)**
    - `callStartTime` — number **(required)**
    - `annotations` — array **(required)** — Every annotation recorded on the conversation, oldest first — the history of what was observed, superseded readings of a keyed value included. _(maxItems=250)_
      - _array of_ `Annotation`
        - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
        - `time` — number **(required)**
        - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
        - `payload` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`tag`**
              - `tag` — string **(required)** _(maxLen=50)_
            - **`text`**
              - `text` — string **(required)** _(maxLen=4096)_
            - **`variables`**
              - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationVariablesValue` in the Schemas appendix)_
            - **`result`**
              - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationResultValue` in the Schemas appendix)_
            - **`metric`**
              - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationMetricValue` in the Schemas appendix)_
        - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
          - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
          - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
          - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).
- Errors: `400`, `403`, `404`

#### `GET` `/v2/history/calls/{callId}/flows/{flowIndex}/transcription`

Gets the transcription for a call by callId and flowIndex.

- operationId: `GetCallTranscription`
- **Scopes**: `history:GetCallTranscription`, `history:read`
- **Parameters**
  - `callId` (path) — string **(required)**
  - `flowIndex` (path) — number **(required)**
  - `company` (query) — string
- **Response 200** (`GetCallTranscriptionResponseContent`)
  - `transcription` — CallTranscriptionRecord **(required)**
    - `id` — string **(required)**
    - `pbx` — string **(required)**
    - `time` — number **(required)**
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `licenses` — array **(required)**
      - _array of_ `License`
    - `type` — object **(required)**
    - `flowIndex` — number **(required)**
    - `flowStartTime` — number **(required)**
    - `callStartTime` — number **(required)**
    - `chunks` — array **(required)**
      - _array of_ `CallTranscriptionChunk`
        - `id` — string **(required)**
        - `time` — number **(required)**
        - `speaker` — string **(required)** _(enum: `callee`, `caller`)_
        - `text` — string **(required)**
        - `language` — string
        - `isFinal` — boolean **(required)**
        - `start` — number **(required)**
        - `end` — number **(required)**
        - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
        - `sentiment` — string — Sentiment label for a transcription chunk. Shared between calls and conferences. _(enum: `POSITIVE`, `NEGATIVE`, `MIXED`, `NEUTRAL`)_
  - `interaction` — CallTranscriptionInteractionRecord
    - `talkRatio` — number — Percentage of the call duration during which the agent was speaking.
    - `wordsPerMinute` — number — Average words per minute spoken by the agent during their speaking time.
    - `interruptions` — number — Number of times the agent interrupted another participant during the conversation.
    - `patience` — number — Average time in seconds the agent waited after another participant finished speaking before responding. _(format=float)_
    - `longestMonologue` — number — Duration in seconds of the agent's longest uninterrupted monologue.
    - `longestCustomerStory` — number — Duration in seconds of another participant’s longest uninterrupted story or response.
    - `participants` — array — Detailed statistics for each call participant.
      - _array of_ `CallTranscriptionInteractionParticipantRecord`
        - `speaker` — string **(required)** _(enum: `callee`, `caller`)_
        - `wordsPerMinute` — number — Average words per minute spoken by the participant during the call.
        - `talkRatio` — number — Percentage of the call duration during which the participant was speaking.
        - `interruptions` — array — List of interruptions where this participant was interrupted during the conversation.
          - _array of_ `CallTranscriptionInterruption`
            - `time` — number **(required)** — Time in milliseconds from the start of the call (e.g., flowStartTime) when the interruption occurred.
            - `chunks` — array **(required)** — IDs of the chunks involved in the interruption — including the interrupting speaker and the chunk that was interrupted.
              - _array of_ `string`
- Errors: `400`, `403`, `404`

#### `GET` `/v2/history/calls/{callId}/flows/{flowIndex}/transcription/text`

Gets the transcription text and chunks for a call by callId and flowIndex.

- operationId: `GetCallTranscriptionText`
- **Scopes**: `history:GetCallTranscriptionText`, `history:read`
- **Parameters**
  - `callId` (path) — string **(required)**
  - `flowIndex` (path) — number **(required)**
  - `company` (query) — string
- **Response 200** (`GetCallTranscriptionTextResponseContent`)
  - `filename` — string **(required)**
  - `text` — string **(required)**
  - `chunks` — array **(required)**
    - _array of_ `TranscriptionTextChunk`
      - `id` — string **(required)**
      - `name` — string **(required)**
      - `text` — string **(required)**
      - `time` — string **(required)**
      - `offset` — number **(required)**
- Errors: `400`, `403`, `404`

#### `GET` `/v2/history/chats/{chatId}`

Gets a chat by chatId.

- operationId: `GetChat`
- **Scopes**: `history:GetChat`, `history:read`
- **Parameters**
  - `chatId` (path) — string **(required)** — A unique identifier that distinguishes each chat session within a channel.
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetChatResponseContent`)
  - `chat` — ChatRecord **(required)**
    - `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
    - `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
    - `time` — number **(required)**
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `pbx` — string
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
    - `waitTime` — number
    - `duration` — number **(required)**
    - `direction` — string **(required)** _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
    - `subject` — string
    - `service` — string
    - `serviceTitle` — string
    - `tags` — array
      - _array of_ `ChatTag`
    - `channel` — Channel **(required)**
      - `subject` — string
      - `description` — string
      - `picture` — string — Picture URL
      - `pictureColor` — string — Picture dominant color represented by a hex value.
      - `access` — string _(enum: `private`, `public`)_
      - `company` — string
      - `context` — ChannelContext
        - `source` — string _(enum: `kite`)_
        - `target` — string
        - `events` — array
          - _array of_ `ChannelContextEvent`
            - `id` — string
            - `owner` — string
            - `start` — string
            - `end` — string
            - `summary` — string
            - `attendees` — array
              - _(nesting depth limit — see `ChannelContextEventAttendee` in the Schemas appendix)_
        - `ptt` — ChannelContextPushToTalk
          - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
      - `kite` — boolean
      - `kiteTarget` — string
      - `kiteVariant` — string
      - `kiteAssign` — string
      - `kiteServiceName` — string
      - `kiteDefaultSubject` — string
      - `service` — string
      - `serviceTitle` — string
      - `serviceRecipient` — string
      - `assignee` — User
        - `id` — string **(required)** _(minLen=12; maxLen=12)_
        - `name` — string
        - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
        - `phone` — string
        - `picture` — string
        - `locale` — string
        - `timeZone` — string
        - `company` — string
        - `bot` — boolean
        - `pbxDomain` — string
        - `pbxPort` — string
        - `pbxExtension` — string
        - `pbxSerial` — string
        - `pbxUserId` — string
        - `pbxGroupId` — string
        - `createdAt` — string
        - `updatedAt` — string
      - `telephony` — boolean
      - `sms` — boolean
      - `mms` — boolean
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
      - `messagingSenderId` — string
      - `messagingReplyUntil` — number
      - `broadcast` — boolean
      - `external` — boolean
      - `autoRecord` — boolean
      - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
      - `transcriptionLanguage` — string
      - `wizyGuestViewOnly` — boolean
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `channelType` — string **(required)** _(enum: `direct`, `group`)_
      - `memberCount` — number **(required)**
      - `createdAt` — string **(required)**
      - `createdBy` — string **(required)**
      - `updatedAt` — string
    - `status` — string _(enum: `WAITFIRSTREPLY`, `WAITREPLYFROMGUEST`, `WAITREPLYFROMAGENT`, `COMPLETED`, `MISSED`)_
    - `participants` — array **(required)**
      - _array of_ `ChatParticipant`
        - `id` — string **(required)**
        - `info` — ChatParticipantInfo **(required)**
          - `id` — string **(required)** _(minLen=12; maxLen=12)_
          - `name` — string
          - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
          - `phone` — string
          - `picture` — string
          - `locale` — string
          - `timeZone` — string
          - `company` — string
          - `bot` — boolean
          - `pbxDomain` — string
          - `pbxPort` — string
          - `pbxExtension` — string
          - `pbxSerial` — string
          - `pbxUserId` — string
          - `pbxGroupId` — string
          - `createdAt` — string
          - `updatedAt` — string
          - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
          - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
    - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
    - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
      - _map of_ `Annotation`
        - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
        - `time` — number **(required)**
        - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
        - `payload` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`tag`**
              - `tag` — string **(required)** _(maxLen=50)_
            - **`text`**
              - `text` — string **(required)** _(maxLen=4096)_
            - **`variables`**
              - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationVariablesValue` in the Schemas appendix)_
            - **`result`**
              - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationResultValue` in the Schemas appendix)_
            - **`metric`**
              - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationMetricValue` in the Schemas appendix)_
        - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
          - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
          - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
          - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).
    - `type` — object **(required)**
- Errors: `400`, `403`, `404`

#### `GET` `/v2/history/chats/{chatId}/annotations`

Gets annotations for a chat by chatId.

- operationId: `GetChatAnnotations`
- **Scopes**: `history:GetChatAnnotations`, `history:read`
- **Parameters**
  - `chatId` (path) — string **(required)** — A unique identifier that distinguishes each chat session within a channel.
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetChatAnnotationsResponseContent`)
  - `annotations` — ChatAnnotationsRecord **(required)**
    - `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
    - `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
    - `time` — number **(required)**
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `type` — object **(required)**
    - `annotations` — array **(required)** — Every annotation recorded on the conversation, oldest first — the history of what was observed, superseded readings of a keyed value included. _(maxItems=250)_
      - _array of_ `Annotation`
        - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
        - `time` — number **(required)**
        - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
        - `payload` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`tag`**
              - `tag` — string **(required)** _(maxLen=50)_
            - **`text`**
              - `text` — string **(required)** _(maxLen=4096)_
            - **`variables`**
              - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationVariablesValue` in the Schemas appendix)_
            - **`result`**
              - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationResultValue` in the Schemas appendix)_
            - **`metric`**
              - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationMetricValue` in the Schemas appendix)_
        - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
          - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
          - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
          - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).
- Errors: `400`, `403`, `404`

#### `GET` `/v2/history/chats/{chatId}/transcription`

Gets the transcription for a chat by chatId.

- operationId: `GetChatTranscription`
- **Scopes**: `history:GetChatTranscription`, `history:read`
- **Parameters**
  - `chatId` (path) — string **(required)** — A unique identifier that distinguishes each chat session within a channel.
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetChatTranscriptionResponseContent`)
  - `transcription` — ChatTranscriptionRecord **(required)**
    - `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
    - `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
    - `time` — number **(required)**
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `type` — object **(required)**
    - `messages` — array **(required)**
      - _array of_ `Message`
        - `text` — string _(minLen=1; maxLen=5000)_
        - `elements` — array
          - _array of_ `Element`
            - _oneOf_ — exactly one of:
              - **`template`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`actions`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`wilma`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `attachments` — array
          - _array of_ `MessageAttachment`
            - `id` — string **(required)**
            - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
            - `mime` — string
            - `name` — string **(required)**
            - `size` — number **(required)**
            - `width` — number
            - `height` — number
            - `thumbnail` — string
        - `quote` — MessageQuote
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
          - `user` — User **(required)**
            - `id` — string **(required)** _(minLen=12; maxLen=12)_
            - `name` — string
            - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
            - `phone` — string
            - `picture` — string
            - `locale` — string
            - `timeZone` — string
            - `company` — string
            - `bot` — boolean
            - `pbxDomain` — string
            - `pbxPort` — string
            - `pbxExtension` — string
            - `pbxSerial` — string
            - `pbxUserId` — string
            - `pbxGroupId` — string
            - `createdAt` — string
            - `updatedAt` — string
          - `text` — string _(minLen=1; maxLen=5000)_
          - `attachments` — array
            - _array of_ `MessageAttachment`
              - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
          - `forward` — MessageForward
            - `forwardCompany` — string
            - `forwardDate` — string **(required)**
            - `forwardEmail` — string
            - `forwardName` — string
            - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
            - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
          - `mentions` — array
            - _array of_ `User`
              - _(nesting depth limit — see `User` in the Schemas appendix)_
          - `giphy` — MessageGiphy
            - `id` — string **(required)** _(minLen=1)_
            - `size` — string **(required)** _(pattern=^\d+$)_
            - `url` — string **(required)** _(minLen=1)_
            - `height` — string **(required)** _(pattern=^\d+$)_
            - `width` — string **(required)** _(pattern=^\d+$)_
          - `createdAt` — string **(required)**
          - `updatedAt` — string
        - `forward` — MessageForward
          - `forwardCompany` — string
          - `forwardDate` — string **(required)**
          - `forwardEmail` — string
          - `forwardName` — string
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `whatsapp` — boolean
        - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
        - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
        - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
        - `sms` — boolean
        - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
        - `markdown` — boolean
        - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
        - `giphy` — MessageGiphy
          - `id` — string **(required)** _(minLen=1)_
          - `size` — string **(required)** _(pattern=^\d+$)_
          - `url` — string **(required)** _(minLen=1)_
          - `height` — string **(required)** _(pattern=^\d+$)_
          - `width` — string **(required)** _(pattern=^\d+$)_
        - `silent` — boolean
        - `event` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `user` — User **(required)**
          - `id` — string **(required)** _(minLen=12; maxLen=12)_
          - `name` — string
          - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
          - `phone` — string
          - `picture` — string
          - `locale` — string
          - `timeZone` — string
          - `company` — string
          - `bot` — boolean
          - `pbxDomain` — string
          - `pbxPort` — string
          - `pbxExtension` — string
          - `pbxSerial` — string
          - `pbxUserId` — string
          - `pbxGroupId` — string
          - `createdAt` — string
          - `updatedAt` — string
        - `edit` — boolean
        - `mentions` — array
          - _array of_ `User`
            - `id` — string **(required)** _(minLen=12; maxLen=12)_
            - `name` — string
            - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
            - `phone` — string
            - `picture` — string
            - `locale` — string
            - `timeZone` — string
            - `company` — string
            - `bot` — boolean
            - `pbxDomain` — string
            - `pbxPort` — string
            - `pbxExtension` — string
            - `pbxSerial` — string
            - `pbxUserId` — string
            - `pbxGroupId` — string
            - `createdAt` — string
            - `updatedAt` — string
        - `latestReactions` — array
          - _array of_ `Reaction`
            - `type` — string
            - `userId` — string _(minLen=12; maxLen=12)_
            - `messageId` — string
            - `user` — User
              - _(nesting depth limit — see `User` in the Schemas appendix)_
        - `reactionCounts` — ReactionCounts
          - _map of_ `number`
        - `createdAt` — string **(required)**
        - `updatedAt` — string
- Errors: `400`, `403`, `404`

#### `GET` `/v2/history/chats/{chatId}/transcription/text`

Gets the transcription text and chunks for a chat by chatId.

- operationId: `GetChatTranscriptionText`
- **Scopes**: `history:GetChatTranscriptionText`, `history:read`
- **Parameters**
  - `chatId` (path) — string **(required)** — A unique identifier that distinguishes each chat session within a channel.
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetChatTranscriptionTextResponseContent`)
  - `filename` — string **(required)**
  - `text` — string **(required)**
  - `messages` — array **(required)**
    - _array of_ `Message`
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _array of_ `Element`
          - _oneOf_ — exactly one of:
            - **`template`**
              - `template` — MessageTemplateConfig **(required)**
                - _(nesting depth limit — see `MessageTemplateConfig` in the Schemas appendix)_
            - **`actions`**
              - `actions` — array **(required)**
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
            - **`wilma`**
              - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
                - _(nesting depth limit — see `WilmaChatElement` in the Schemas appendix)_
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `quote` — MessageQuote
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `user` — User **(required)**
          - `id` — string **(required)** _(minLen=12; maxLen=12)_
          - `name` — string
          - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
          - `phone` — string
          - `picture` — string
          - `locale` — string
          - `timeZone` — string
          - `company` — string
          - `bot` — boolean
          - `pbxDomain` — string
          - `pbxPort` — string
          - `pbxExtension` — string
          - `pbxSerial` — string
          - `pbxUserId` — string
          - `pbxGroupId` — string
          - `createdAt` — string
          - `updatedAt` — string
        - `text` — string _(minLen=1; maxLen=5000)_
        - `attachments` — array
          - _array of_ `MessageAttachment`
            - `id` — string **(required)**
            - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
            - `mime` — string
            - `name` — string **(required)**
            - `size` — number **(required)**
            - `width` — number
            - `height` — number
            - `thumbnail` — string
        - `forward` — MessageForward
          - `forwardCompany` — string
          - `forwardDate` — string **(required)**
          - `forwardEmail` — string
          - `forwardName` — string
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `mentions` — array
          - _array of_ `User`
            - `id` — string **(required)** _(minLen=12; maxLen=12)_
            - `name` — string
            - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
            - `phone` — string
            - `picture` — string
            - `locale` — string
            - `timeZone` — string
            - `company` — string
            - `bot` — boolean
            - `pbxDomain` — string
            - `pbxPort` — string
            - `pbxExtension` — string
            - `pbxSerial` — string
            - `pbxUserId` — string
            - `pbxGroupId` — string
            - `createdAt` — string
            - `updatedAt` — string
        - `giphy` — MessageGiphy
          - `id` — string **(required)** _(minLen=1)_
          - `size` — string **(required)** _(pattern=^\d+$)_
          - `url` — string **(required)** _(minLen=1)_
          - `height` — string **(required)** _(pattern=^\d+$)_
          - `width` — string **(required)** _(pattern=^\d+$)_
        - `createdAt` — string **(required)**
        - `updatedAt` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
      - `sms` — boolean
      - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
      - `markdown` — boolean
      - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
      - `giphy` — MessageGiphy
        - `id` — string **(required)** _(minLen=1)_
        - `size` — string **(required)** _(pattern=^\d+$)_
        - `url` — string **(required)** _(minLen=1)_
        - `height` — string **(required)** _(pattern=^\d+$)_
        - `width` — string **(required)** _(pattern=^\d+$)_
      - `silent` — boolean
      - `event` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - `id` — string **(required)** _(minLen=12; maxLen=12)_
        - `name` — string
        - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
        - `phone` — string
        - `picture` — string
        - `locale` — string
        - `timeZone` — string
        - `company` — string
        - `bot` — boolean
        - `pbxDomain` — string
        - `pbxPort` — string
        - `pbxExtension` — string
        - `pbxSerial` — string
        - `pbxUserId` — string
        - `pbxGroupId` — string
        - `createdAt` — string
        - `updatedAt` — string
      - `edit` — boolean
      - `mentions` — array
        - _array of_ `User`
          - `id` — string **(required)** _(minLen=12; maxLen=12)_
          - `name` — string
          - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
          - `phone` — string
          - `picture` — string
          - `locale` — string
          - `timeZone` — string
          - `company` — string
          - `bot` — boolean
          - `pbxDomain` — string
          - `pbxPort` — string
          - `pbxExtension` — string
          - `pbxSerial` — string
          - `pbxUserId` — string
          - `pbxGroupId` — string
          - `createdAt` — string
          - `updatedAt` — string
      - `latestReactions` — array
        - _array of_ `Reaction`
          - `type` — string
          - `userId` — string _(minLen=12; maxLen=12)_
          - `messageId` — string
          - `user` — User
            - `id` — string **(required)** _(minLen=12; maxLen=12)_
            - `name` — string
            - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
            - `phone` — string
            - `picture` — string
            - `locale` — string
            - `timeZone` — string
            - `company` — string
            - `bot` — boolean
            - `pbxDomain` — string
            - `pbxPort` — string
            - `pbxExtension` — string
            - `pbxSerial` — string
            - `pbxUserId` — string
            - `pbxGroupId` — string
            - `createdAt` — string
            - `updatedAt` — string
      - `reactionCounts` — ReactionCounts
        - _map of_ `number`
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- Errors: `400`, `403`, `404`

#### `GET` `/v2/history/conferences/{conferenceId}`

Gets a conference by conferenceId.

- operationId: `GetConference`
- **Scopes**: `history:GetConference`, `history:read`
- **Parameters**
  - `conferenceId` (path) — string **(required)**
  - `company` (query) — string
- **Response 200** (`GetConferenceResponseContent`)
  - `conference` — ConferenceRecord **(required)**
    - `id` — string **(required)**
    - `time` — number **(required)**
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `pbx` — string
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
    - `duration` — number **(required)**
    - `waitTime` — number
    - `subject` — string
    - `direction` — string **(required)** _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
    - `service` — string
    - `status` — string _(enum: `COMPLETED`, `MISSED`)_
    - `participants` — array **(required)**
      - _array of_ `ConferenceAnalyticsRecordParticipant`
        - `jid` — string **(required)**
        - `info` — ConferenceParticipant **(required)**
          - `type` — string **(required)** _(enum: `EXTERNAL`, `EXTERNAL_DIAL_IN`, `PBX`, `PBX_SIP`, `XBS`)_
          - `role` — string _(enum: `CLIENT`, `AGENT`)_
          - `jid` — string — A unique identifier to avoid duplicates if user re-connect from different devices.
          - `name` — string
          - `email` — string
          - `phone` — string
          - `department` — string
          - `company` — string _(minLen=3; maxLen=30)_
          - `pbxSerial` — string
          - `pbxExtension` — string
          - `pbxGroupId` — string
          - `xbsId` — string
          - `license` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
        - `totalDuration` — number **(required)**
        - `totalSpeakDuration` — number **(required)**
        - `joinTime` — number **(required)**
    - `recordings` — array
      - _array of_ `ConferenceRecording`
        - `url` — string **(required)**
        - `start` — number **(required)**
        - `end` — number **(required)**
    - `transcriptionStatus` — string **(required)** _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
    - `transcriptionLanguage` — string
    - `transcriptionSeconds` — number
    - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
    - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
      - _map of_ `Annotation`
        - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
        - `time` — number **(required)**
        - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
        - `payload` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`tag`**
              - `tag` — string **(required)** _(maxLen=50)_
            - **`text`**
              - `text` — string **(required)** _(maxLen=4096)_
            - **`variables`**
              - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationVariablesValue` in the Schemas appendix)_
            - **`result`**
              - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationResultValue` in the Schemas appendix)_
            - **`metric`**
              - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationMetricValue` in the Schemas appendix)_
        - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
          - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
          - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
          - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).
    - `type` — object **(required)**
- Errors: `400`, `403`, `404`

#### `GET` `/v2/history/conferences/{conferenceId}/annotations`

Gets annotations for a conference by conferenceId.

- operationId: `GetConferenceAnnotations`
- **Scopes**: `history:GetConferenceAnnotations`, `history:read`
- **Parameters**
  - `conferenceId` (path) — string **(required)**
  - `company` (query) — string
- **Response 200** (`GetConferenceAnnotationsResponseContent`)
  - `annotations` — ConferenceAnnotationsRecord **(required)**
    - `id` — string **(required)**
    - `time` — number **(required)**
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `type` — object **(required)**
    - `annotations` — array **(required)** — Every annotation recorded on the conversation, oldest first — the history of what was observed, superseded readings of a keyed value included. _(maxItems=250)_
      - _array of_ `Annotation`
        - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
        - `time` — number **(required)**
        - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
        - `payload` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`tag`**
              - `tag` — string **(required)** _(maxLen=50)_
            - **`text`**
              - `text` — string **(required)** _(maxLen=4096)_
            - **`variables`**
              - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationVariablesValue` in the Schemas appendix)_
            - **`result`**
              - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationResultValue` in the Schemas appendix)_
            - **`metric`**
              - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
                - _(nesting depth limit — see `AnnotationMetricValue` in the Schemas appendix)_
        - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
          - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
          - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
          - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).
- Errors: `400`, `403`, `404`

#### `GET` `/v2/history/conferences/{conferenceId}/transcription`

Gets the transcription for a conference by conferenceId.

- operationId: `GetConferenceTranscription`
- **Scopes**: `history:GetConferenceTranscription`, `history:read`
- **Parameters**
  - `conferenceId` (path) — string **(required)**
  - `company` (query) — string
- **Response 200** (`GetConferenceTranscriptionResponseContent`)
  - `transcription` — ConferenceTranscriptionRecord **(required)**
    - `id` — string **(required)**
    - `time` — number **(required)**
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `type` — object **(required)**
    - `transcriptions` — array **(required)**
      - _array of_ `ConferenceTranscription`
        - `start` — number **(required)**
        - `end` — number **(required)**
        - `chunks` — array **(required)**
          - _array of_ `ConferenceTranscriptionChunk`
            - `id` — string **(required)**
            - `time` — number **(required)**
            - `jid` — string **(required)**
            - `text` — string **(required)**
            - `language` — string
            - `isFinal` — boolean **(required)**
            - `start` — number **(required)**
            - `end` — number **(required)**
            - `sentiment` — string — Sentiment label for a transcription chunk. Shared between calls and conferences. _(enum: `POSITIVE`, `NEGATIVE`, `MIXED`, `NEUTRAL`)_
  - `interaction` — ConferenceTranscriptionInteractionRecord
    - `talkRatio` — number — Percentage of the call duration during which the agent was speaking.
    - `wordsPerMinute` — number — Average words per minute spoken by the agent during their speaking time.
    - `interruptions` — number — Number of times the agent interrupted another participant during the conversation.
    - `patience` — number — Average time in seconds the agent waited after another participant finished speaking before responding. _(format=float)_
    - `longestMonologue` — number — Duration in seconds of the agent's longest uninterrupted monologue.
    - `longestCustomerStory` — number — Duration in seconds of another participant’s longest uninterrupted story or response.
    - `participants` — array — Detailed statistics for each participant in the call.
      - _array of_ `ConferenceTranscriptionInteractionParticipantRecord`
        - `jid` — string **(required)** — Unique identifier (JID) of the participant.
        - `wordsPerMinute` — number — Average words per minute spoken by the participant during the call.
        - `talkRatio` — number — Percentage of the call duration during which the participant was speaking.
        - `interruptions` — array — List of interruptions where this participant interrupted or was interrupted during the conversation.
          - _array of_ `ConferenceTranscriptionInterruption`
            - `time` — number **(required)** — Time in milliseconds from the start of the call (e.g., flowStartTime) when the interruption occurred.
            - `chunks` — array **(required)** — IDs of the conversation chunks involved in the interruption, including both the interrupting and interrupted speakers.
              - _array of_ `string`
- Errors: `400`, `403`, `404`

#### `GET` `/v2/history/conferences/{conferenceId}/transcription/text`

Gets the transcription text and chunks for a conference by conferenceId.

- operationId: `GetConferenceTranscriptionText`
- **Scopes**: `history:GetConferenceTranscriptionText`, `history:read`
- **Parameters**
  - `conferenceId` (path) — string **(required)**
  - `company` (query) — string
- **Response 200** (`GetConferenceTranscriptionTextResponseContent`)
  - `filename` — string **(required)**
  - `text` — string **(required)**
  - `chunks` — array **(required)**
    - _array of_ `TranscriptionTextChunk`
      - `id` — string **(required)**
      - `name` — string **(required)**
      - `text` — string **(required)**
      - `time` — string **(required)**
      - `offset` — number **(required)**
- Errors: `400`, `403`, `404`

#### `POST` `/v2/history/conversations`

Retrieves list of conversations using filters.

- operationId: `QueryConversations`
- **Scopes**: `history:QueryConversations`, `history:read`
- **Parameters**
  - `company` (query) — string — Company id. eg. it_w123123. Required for s2s auth.
  - `user` (query) — string — PBX user id. eg. 123123123. Can be applied only for s2s and pbx authorization.
- **Request body** (`application/json` — `QueryConversationsRequestContent`)
  - `limit` — number — The maximum number of rows to return. _(default=50; min=1; max=100)_
  - `offset` — number — The offset from which to start. _(default=0; min=0)_
  - `filter` — QueryConversationsFilter
    - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
    - `flags` — array
      - _array of_ `ConversationFlag`
    - `status` — string _(enum: `COMPLETED`, `MISSED`)_
    - `from` — string _(format=date-time)_
    - `to` — string _(format=date-time)_
    - `tags` — array
      - _array of_ `string`
    - `search` — string _(maxLen=64)_
    - `hasAttachment` — boolean
- **Response 200** (`QueryConversationsResponseContent`)
  - `conversations` — array **(required)**
    - _array of_ `Conversation`
      - _oneOf_ — exactly one of:
        - **`call`**
          - `call` — CallRecord **(required)**
            - `flowIndex` — number **(required)**
            - `startTime` — number **(required)**
            - `endTime` — number **(required)**
            - `connectTime` — number — Duration when the called party's phone rang (Ring Time in UI)
            - `talkTime` — number — Duration of conversation from the moment the call is answered until it ends, excluding hold time
            - `waitTime` — number — Duration spent on IVR, dialplan applications, playback, etc. before the call is answered
            - `queueTime` — number — Duration of call waiting in queue
            - `holdTime` — number — Duration the call was on hold after being answered
            - `duration` — number **(required)** — Total duration = connectTime + waitTime + queueTime + talkTime + holdTime
            - `caller` — CallParticipant
              - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
              - `phone` — string
              - `name` — string
              - `company` — string _(minLen=3; maxLen=30)_
              - `email` — string
              - `userId` — string
              - `userExtension` — string
              - `userDepartment` — string
              - `groupId` — string
              - `groupName` — string
              - `userAgent` — string
              - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
              - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
              - `license` — string
              - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
              - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
              - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
              - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
            - `callee` — CallParticipant
              - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
              - `phone` — string
              - `name` — string
              - `company` — string _(minLen=3; maxLen=30)_
              - `email` — string
              - `userId` — string
              - `userExtension` — string
              - `userDepartment` — string
              - `groupId` — string
              - `groupName` — string
              - `userAgent` — string
              - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
              - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
              - `license` — string
              - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
              - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
              - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
              - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
            - `service` — string
            - `serviceNumber` — string
            - `destination` — string
            - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
            - `trunkName` — string
            - `trunkDirection` — string
            - `queueName` — string
            - `queueId` — string
            - `queuePosition` — number — Position of the call in the queue (1-based). Updated from consume events and emitted on live progress and record flows.
            - `tags` — array
              - _array of_ `string`
            - `flags` — array
              - _array of_ `string`
            - `callerMos` — string
            - `calleeMos` — string
            - `xhoppersConfId` — string
            - `recordings` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
              - _array of_ `string`
            - `recordingsData` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
              - _array of_ `CallFlowRecording`
                - _(nesting depth limit — see `CallFlowRecording` in the Schemas appendix)_
            - `mergeWith` — string
            - `splitReason` — string
            - `splitTransferType` — string
            - `remotePhone` — string
            - `remotePhoneCountryCode` — number
            - `remotePhoneCountryCodeStr` — string
            - `remotePhoneLocation` — string
            - `callStatus` — string _(enum: `COMPLETED`, `MISSED`)_
            - `transcriptionStatus` — string _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
            - `transcriptionLanguage` — string
            - `transcriptionSeconds` — number
            - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
            - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
              - _map of_ `Annotation`
                - _(nesting depth limit — see `Annotation` in the Schemas appendix)_
            - `attachment` — string — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
            - `attachmentType` — string _(enum: `VOICEMAIL`, `FAX`)_
            - `attachmentDestinations` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
              - _array of_ `CallFlowAttachmentDestination`
                - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
            - `attachments` — array
              - _array of_ `CallFlowAttachment`
                - _(nesting depth limit — see `CallFlowAttachment` in the Schemas appendix)_
            - `notifications` — CallFlowNotifications
              - `destinations` — array
                - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
              - `type` — array
                - _array of_ `string`
            - `id` — string **(required)**
            - `pbx` — string **(required)**
            - `time` — number **(required)**
            - `company` — string **(required)** _(minLen=3; maxLen=30)_
            - `licenses` — array **(required)**
              - _array of_ `License`
            - `type` — object **(required)**
        - **`conference`**
          - `conference` — ConferenceRecord **(required)**
            - `id` — string **(required)**
            - `time` — number **(required)**
            - `company` — string **(required)** _(minLen=3; maxLen=30)_
            - `pbx` — string
            - `startTime` — number **(required)**
            - `endTime` — number **(required)**
            - `duration` — number **(required)**
            - `waitTime` — number
            - `subject` — string
            - `direction` — string **(required)** _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
            - `service` — string
            - `status` — string _(enum: `COMPLETED`, `MISSED`)_
            - `participants` — array **(required)**
              - _array of_ `ConferenceAnalyticsRecordParticipant`
                - _(nesting depth limit — see `ConferenceAnalyticsRecordParticipant` in the Schemas appendix)_
            - `recordings` — array
              - _array of_ `ConferenceRecording`
                - _(nesting depth limit — see `ConferenceRecording` in the Schemas appendix)_
            - `transcriptionStatus` — string **(required)** _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
            - `transcriptionLanguage` — string
            - `transcriptionSeconds` — number
            - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
            - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
              - _map of_ `Annotation`
                - _(nesting depth limit — see `Annotation` in the Schemas appendix)_
            - `type` — object **(required)**
- Errors: `400`

#### `POST` `/v2/history/user/calls`

Retrieves list of user calls using filters.

- operationId: `QueryUserCalls`
- **Scopes**: `history:QueryUserCalls`, `history:read`
- **Parameters**
  - `company` (query) — string — Company id. eg. it_w123123. Required for s2s auth.
  - `user` (query) — string — PBX user id. eg. 123123123. Can be applied only for s2s and pbx authorization.
- **Request body** (`application/json` — `QueryUserCallsRequestContent`)
  - `limit` — number — The maximum number of rows to return. _(default=50; min=1; max=100)_
  - `offset` — number — The offset from which to start. _(default=0; min=0)_
  - `filter` — QueryUserCallsFilter
    - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
    - `flags` — array
      - _array of_ `ConversationFlag`
    - `status` — string _(enum: `COMPLETED`, `MISSED`)_
    - `from` — string _(format=date-time)_
    - `to` — string _(format=date-time)_
    - `tags` — array
      - _array of_ `string`
    - `search` — string _(maxLen=64)_
    - `hasAttachment` — boolean
    - `userDirection` — string _(enum: `INCOMING`, `OUTGOING`)_
- **Response 200** (`QueryUserCallsResponseContent`)
  - `calls` — array **(required)**
    - _array of_ `CallRecord`
      - `flowIndex` — number **(required)**
      - `startTime` — number **(required)**
      - `endTime` — number **(required)**
      - `connectTime` — number — Duration when the called party's phone rang (Ring Time in UI)
      - `talkTime` — number — Duration of conversation from the moment the call is answered until it ends, excluding hold time
      - `waitTime` — number — Duration spent on IVR, dialplan applications, playback, etc. before the call is answered
      - `queueTime` — number — Duration of call waiting in queue
      - `holdTime` — number — Duration the call was on hold after being answered
      - `duration` — number **(required)** — Total duration = connectTime + waitTime + queueTime + talkTime + holdTime
      - `caller` — CallParticipant
        - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
        - `phone` — string
        - `name` — string
        - `company` — string _(minLen=3; maxLen=30)_
        - `email` — string
        - `userId` — string
        - `userExtension` — string
        - `userDepartment` — string
        - `groupId` — string
        - `groupName` — string
        - `userAgent` — string
        - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
        - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
        - `license` — string
        - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
        - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
        - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
        - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
      - `callee` — CallParticipant
        - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
        - `phone` — string
        - `name` — string
        - `company` — string _(minLen=3; maxLen=30)_
        - `email` — string
        - `userId` — string
        - `userExtension` — string
        - `userDepartment` — string
        - `groupId` — string
        - `groupName` — string
        - `userAgent` — string
        - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
        - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
        - `license` — string
        - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
        - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
        - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
        - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
      - `service` — string
      - `serviceNumber` — string
      - `destination` — string
      - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
      - `trunkName` — string
      - `trunkDirection` — string
      - `queueName` — string
      - `queueId` — string
      - `queuePosition` — number — Position of the call in the queue (1-based). Updated from consume events and emitted on live progress and record flows.
      - `tags` — array
        - _array of_ `string`
      - `flags` — array
        - _array of_ `string`
      - `callerMos` — string
      - `calleeMos` — string
      - `xhoppersConfId` — string
      - `recordings` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
        - _array of_ `string`
      - `recordingsData` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
        - _array of_ `CallFlowRecording`
          - `fileName` — string **(required)**
          - `start` — number **(required)**
          - `end` — number **(required)**
          - `owner` — string **(required)** _(enum: `callee`, `caller`, `system`)_
          - `url` — string **(required)**
          - `pauses` — array **(required)**
            - _array of_ `CallRecordPause`
              - _(nesting depth limit — see `CallRecordPause` in the Schemas appendix)_
      - `mergeWith` — string
      - `splitReason` — string
      - `splitTransferType` — string
      - `remotePhone` — string
      - `remotePhoneCountryCode` — number
      - `remotePhoneCountryCodeStr` — string
      - `remotePhoneLocation` — string
      - `callStatus` — string _(enum: `COMPLETED`, `MISSED`)_
      - `transcriptionStatus` — string _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
      - `transcriptionLanguage` — string
      - `transcriptionSeconds` — number
      - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
      - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
        - _map of_ `Annotation`
          - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
          - `time` — number **(required)**
          - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
          - `payload` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`tag`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`text`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`variables`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`result`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`metric`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
            - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
            - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
            - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).
      - `attachment` — string — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
      - `attachmentType` — string _(enum: `VOICEMAIL`, `FAX`)_
      - `attachmentDestinations` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
        - _array of_ `CallFlowAttachmentDestination`
          - `phone` — string
          - `name` — string
          - `email` — string
          - `userId` — string
          - `userExtension` — string
          - `userDepartment` — string
          - `groupId` — string
          - `groupName` — string
      - `attachments` — array
        - _array of_ `CallFlowAttachment`
          - _oneOf_ — exactly one of:
            - **`recording`**
              - `recording` — CallFlowRecording **(required)**
                - _(nesting depth limit — see `CallFlowRecording` in the Schemas appendix)_
            - **`fax`**
              - `fax` — CallFlowFax **(required)**
                - _(nesting depth limit — see `CallFlowFax` in the Schemas appendix)_
            - **`voicemail`**
              - `voicemail` — CallFlowVoicemail **(required)**
                - _(nesting depth limit — see `CallFlowVoicemail` in the Schemas appendix)_
      - `notifications` — CallFlowNotifications
        - `destinations` — array
          - _array of_ `CallFlowAttachmentDestination`
            - `phone` — string
            - `name` — string
            - `email` — string
            - `userId` — string
            - `userExtension` — string
            - `userDepartment` — string
            - `groupId` — string
            - `groupName` — string
        - `type` — array
          - _array of_ `string`
      - `id` — string **(required)**
      - `pbx` — string **(required)**
      - `time` — number **(required)**
      - `company` — string **(required)** _(minLen=3; maxLen=30)_
      - `licenses` — array **(required)**
        - _array of_ `License`
      - `type` — object **(required)**
- Errors: `400`

### Schemas appendix — History API

<details><summary>140 component schemas</summary>

**`ActionElement`**

- _oneOf_ — exactly one of:
  - **`button`**
    - `button` — ButtonElement **(required)**
      - `text` — string **(required)** _(minLen=1; maxLen=96)_
      - `handler` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`link`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`reply`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`action`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `variant` — string _(enum: `contained`, `outlined`)_
      - `disabled` — boolean

**`Annotation`**

- `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
- `time` — number **(required)**
- `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
- `payload` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`tag`**
      - `tag` — string **(required)** _(maxLen=50)_
    - **`text`**
      - `text` — string **(required)** _(maxLen=4096)_
    - **`variables`**
      - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
        - `value` — any **(required)**
    - **`result`**
      - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
        - `value` — any **(required)**
    - **`metric`**
      - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
        - `value` — any **(required)** — The reading, as its producer models it: a score, a label, a number, or an object such as `{"customerRatio": 0.42, "agentRatio": 0.58}`.
        - `previous` — any — The reading this one replaces, so a consumer can render the change without loading the history. Absent on the first reading.
        - `label` — string — Human-readable name of the value, e.g. 'CSAT' or 'Talk ratio'. _(maxLen=100)_
- `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
  - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
  - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
  - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).

**`AnnotationMetricValue`**

_A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits._

- `value` — any **(required)** — The reading, as its producer models it: a score, a label, a number, or an object such as `{"customerRatio": 0.42, "agentRatio": 0.58}`.
- `previous` — any — The reading this one replaces, so a consumer can render the change without loading the history. Absent on the first reading.
- `label` — string — Human-readable name of the value, e.g. 'CSAT' or 'Talk ratio'. _(maxLen=100)_

**`AnnotationPayload`**

- _oneOf_ — exactly one of:
  - **`tag`**
    - `tag` — string **(required)** _(maxLen=50)_
  - **`text`**
    - `text` — string **(required)** _(maxLen=4096)_
  - **`variables`**
    - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
      - `value` — any **(required)**
  - **`result`**
    - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
      - `value` — any **(required)**
  - **`metric`**
    - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
      - `value` — any **(required)** — The reading, as its producer models it: a score, a label, a number, or an object such as `{"customerRatio": 0.42, "agentRatio": 0.58}`.
      - `previous` — any — The reading this one replaces, so a consumer can render the change without loading the history. Absent on the first reading.
      - `label` — string — Human-readable name of the value, e.g. 'CSAT' or 'Talk ratio'. _(maxLen=100)_

**`AnnotationResultValue`**

_Tool result captured for an annotation. Runtime services enforce serialized payload size limits._

- `value` — any **(required)**

**`AnnotationSource`**

_Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape._

- `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
- `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
- `name` — string — Human-readable name of the producer (e.g. tool name, user display name).

**`AnnotationSourceType`**

- string _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_

**`AnnotationVariablesValue`**

_Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits._

- `value` — any **(required)**

**`AnnotationsMap`**

_The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`._

- _map of_ `Annotation`
  - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
  - `time` — number **(required)**
  - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
  - `payload` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — string **(required)** _(maxLen=50)_
      - **`text`**
        - `text` — string **(required)** _(maxLen=4096)_
      - **`variables`**
        - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
          - _(nesting depth limit — see `AnnotationVariablesValue` in the Schemas appendix)_
      - **`result`**
        - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
          - _(nesting depth limit — see `AnnotationResultValue` in the Schemas appendix)_
      - **`metric`**
        - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
          - _(nesting depth limit — see `AnnotationMetricValue` in the Schemas appendix)_
  - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
    - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
    - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
    - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).

**`AnnotationsStatus`**

- string _(enum: `AVAILABLE`, `UNAVAILABLE`)_

**`ButtonActionHandler`**

- `id` — string **(required)** — A unique ID of the action within the message. _(minLen=1; maxLen=32)_

**`ButtonElement`**

- `text` — string **(required)** _(minLen=1; maxLen=96)_
- `handler` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`link`**
      - `link` — ButtonLinkHandler **(required)**
        - `url` — string **(required)** _(minLen=3; maxLen=2048)_
    - **`reply`**
      - `reply` — ButtonReplyHandler **(required)**
        - `text` — string _(minLen=1; maxLen=128)_
    - **`action`**
      - `action` — ButtonActionHandler **(required)**
        - `id` — string **(required)** — A unique ID of the action within the message. _(minLen=1; maxLen=32)_
- `variant` — string _(enum: `contained`, `outlined`)_
- `disabled` — boolean

**`ButtonHandler`**

- _oneOf_ — exactly one of:
  - **`link`**
    - `link` — ButtonLinkHandler **(required)**
      - `url` — string **(required)** _(minLen=3; maxLen=2048)_
  - **`reply`**
    - `reply` — ButtonReplyHandler **(required)**
      - `text` — string _(minLen=1; maxLen=128)_
  - **`action`**
    - `action` — ButtonActionHandler **(required)**
      - `id` — string **(required)** — A unique ID of the action within the message. _(minLen=1; maxLen=32)_

**`ButtonLinkHandler`**

- `url` — string **(required)** _(minLen=3; maxLen=2048)_

**`ButtonReplyHandler`**

- `text` — string _(minLen=1; maxLen=128)_

**`ButtonVariant`**

- string _(enum: `contained`, `outlined`)_

**`CallAnnotationsNotFoundExceptionResponseContent`**

- `message` — string

**`CallAnnotationsRecord`**

- `id` — string **(required)**
- `pbx` — string **(required)**
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `licenses` — array **(required)**
  - _array of_ `License`
- `type` — object **(required)**
- `flowIndex` — number **(required)**
- `flowStartTime` — number **(required)**
- `callStartTime` — number **(required)**
- `annotations` — array **(required)** — Every annotation recorded on the conversation, oldest first — the history of what was observed, superseded readings of a keyed value included. _(maxItems=250)_
  - _array of_ `Annotation`
    - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
    - `time` — number **(required)**
    - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
    - `payload` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`tag`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`variables`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`result`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`metric`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
      - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
      - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
      - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).

**`CallDevice`**

- string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_

**`CallDirection`**

- string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_

**`CallFlowAttachment`**

- _oneOf_ — exactly one of:
  - **`recording`**
    - `recording` — CallFlowRecording **(required)**
      - `fileName` — string **(required)**
      - `start` — number **(required)**
      - `end` — number **(required)**
      - `owner` — string **(required)** _(enum: `callee`, `caller`, `system`)_
      - `url` — string **(required)**
      - `pauses` — array **(required)**
        - _array of_ `CallRecordPause`
          - _(nesting depth limit — see `CallRecordPause` in the Schemas appendix)_
  - **`fax`**
    - `fax` — CallFlowFax **(required)**
      - `url` — string **(required)**
      - `status` — string _(enum: `ok`, `error`)_
      - `destinations` — array
        - _array of_ `CallFlowAttachmentDestination`
          - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
      - `owner` — string _(enum: `callee`, `caller`, `system`)_
      - `error` — string — Text with the reason for the error in case of unsuccessful fax delivery
  - **`voicemail`**
    - `voicemail` — CallFlowVoicemail **(required)**
      - `url` — string **(required)**
      - `destinations` — array
        - _array of_ `CallFlowAttachmentDestination`
          - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
      - `owner` — string _(enum: `callee`, `caller`, `system`)_

**`CallFlowAttachmentDestination`**

- `phone` — string
- `name` — string
- `email` — string
- `userId` — string
- `userExtension` — string
- `userDepartment` — string
- `groupId` — string
- `groupName` — string

**`CallFlowAttachmentStatus`**

- string _(enum: `ok`, `error`)_

**`CallFlowAttachmentType`**

- string _(enum: `VOICEMAIL`, `FAX`)_

**`CallFlowFax`**

- `url` — string **(required)**
- `status` — string _(enum: `ok`, `error`)_
- `destinations` — array
  - _array of_ `CallFlowAttachmentDestination`
    - `phone` — string
    - `name` — string
    - `email` — string
    - `userId` — string
    - `userExtension` — string
    - `userDepartment` — string
    - `groupId` — string
    - `groupName` — string
- `owner` — string _(enum: `callee`, `caller`, `system`)_
- `error` — string — Text with the reason for the error in case of unsuccessful fax delivery

**`CallFlowNotifications`**

- `destinations` — array
  - _array of_ `CallFlowAttachmentDestination`
    - `phone` — string
    - `name` — string
    - `email` — string
    - `userId` — string
    - `userExtension` — string
    - `userDepartment` — string
    - `groupId` — string
    - `groupName` — string
- `type` — array
  - _array of_ `string`

**`CallFlowRecording`**

- `fileName` — string **(required)**
- `start` — number **(required)**
- `end` — number **(required)**
- `owner` — string **(required)** _(enum: `callee`, `caller`, `system`)_
- `url` — string **(required)**
- `pauses` — array **(required)**
  - _array of_ `CallRecordPause`
    - `start` — number
    - `end` — number
    - `reason` — string _(enum: `pause`, `hold`)_

**`CallFlowTranscriptionStatus`**

- string _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_

**`CallFlowVoicemail`**

- `url` — string **(required)**
- `destinations` — array
  - _array of_ `CallFlowAttachmentDestination`
    - `phone` — string
    - `name` — string
    - `email` — string
    - `userId` — string
    - `userExtension` — string
    - `userDepartment` — string
    - `groupId` — string
    - `groupName` — string
- `owner` — string _(enum: `callee`, `caller`, `system`)_

**`CallNotFoundExceptionResponseContent`**

- `message` — string

**`CallParticipant`**

- `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
- `phone` — string
- `name` — string
- `company` — string _(minLen=3; maxLen=30)_
- `email` — string
- `userId` — string
- `userExtension` — string
- `userDepartment` — string
- `groupId` — string
- `groupName` — string
- `userAgent` — string
- `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
- `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
- `license` — string
- `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
- `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
- `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
- `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'

**`CallParticipantRole`**

- string _(enum: `CLIENT`, `AGENT`)_

**`CallParticipantType`**

- string _(enum: `REMOTE`, `LOCAL`)_

**`CallRecord`**

- `flowIndex` — number **(required)**
- `startTime` — number **(required)**
- `endTime` — number **(required)**
- `connectTime` — number — Duration when the called party's phone rang (Ring Time in UI)
- `talkTime` — number — Duration of conversation from the moment the call is answered until it ends, excluding hold time
- `waitTime` — number — Duration spent on IVR, dialplan applications, playback, etc. before the call is answered
- `queueTime` — number — Duration of call waiting in queue
- `holdTime` — number — Duration the call was on hold after being answered
- `duration` — number **(required)** — Total duration = connectTime + waitTime + queueTime + talkTime + holdTime
- `caller` — CallParticipant
  - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
  - `phone` — string
  - `name` — string
  - `company` — string _(minLen=3; maxLen=30)_
  - `email` — string
  - `userId` — string
  - `userExtension` — string
  - `userDepartment` — string
  - `groupId` — string
  - `groupName` — string
  - `userAgent` — string
  - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
  - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
  - `license` — string
  - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
  - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
  - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
  - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
- `callee` — CallParticipant
  - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
  - `phone` — string
  - `name` — string
  - `company` — string _(minLen=3; maxLen=30)_
  - `email` — string
  - `userId` — string
  - `userExtension` — string
  - `userDepartment` — string
  - `groupId` — string
  - `groupName` — string
  - `userAgent` — string
  - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
  - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
  - `license` — string
  - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
  - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
  - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
  - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
- `service` — string
- `serviceNumber` — string
- `destination` — string
- `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
- `trunkName` — string
- `trunkDirection` — string
- `queueName` — string
- `queueId` — string
- `queuePosition` — number — Position of the call in the queue (1-based). Updated from consume events and emitted on live progress and record flows.
- `tags` — array
  - _array of_ `string`
- `flags` — array
  - _array of_ `string`
- `callerMos` — string
- `calleeMos` — string
- `xhoppersConfId` — string
- `recordings` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
  - _array of_ `string`
- `recordingsData` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
  - _array of_ `CallFlowRecording`
    - `fileName` — string **(required)**
    - `start` — number **(required)**
    - `end` — number **(required)**
    - `owner` — string **(required)** _(enum: `callee`, `caller`, `system`)_
    - `url` — string **(required)**
    - `pauses` — array **(required)**
      - _array of_ `CallRecordPause`
        - _(nesting depth limit — see `CallRecordPause` in the Schemas appendix)_
- `mergeWith` — string
- `splitReason` — string
- `splitTransferType` — string
- `remotePhone` — string
- `remotePhoneCountryCode` — number
- `remotePhoneCountryCodeStr` — string
- `remotePhoneLocation` — string
- `callStatus` — string _(enum: `COMPLETED`, `MISSED`)_
- `transcriptionStatus` — string _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
- `transcriptionLanguage` — string
- `transcriptionSeconds` — number
- `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
- `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
  - _map of_ `Annotation`
    - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
    - `time` — number **(required)**
    - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
    - `payload` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`tag`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`variables`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`result`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`metric`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
      - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
      - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
      - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).
- `attachment` — string — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
- `attachmentType` — string _(enum: `VOICEMAIL`, `FAX`)_
- `attachmentDestinations` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
  - _array of_ `CallFlowAttachmentDestination`
    - `phone` — string
    - `name` — string
    - `email` — string
    - `userId` — string
    - `userExtension` — string
    - `userDepartment` — string
    - `groupId` — string
    - `groupName` — string
- `attachments` — array
  - _array of_ `CallFlowAttachment`
    - _oneOf_ — exactly one of:
      - **`recording`**
        - `recording` — CallFlowRecording **(required)**
          - _(nesting depth limit — see `CallFlowRecording` in the Schemas appendix)_
      - **`fax`**
        - `fax` — CallFlowFax **(required)**
          - _(nesting depth limit — see `CallFlowFax` in the Schemas appendix)_
      - **`voicemail`**
        - `voicemail` — CallFlowVoicemail **(required)**
          - _(nesting depth limit — see `CallFlowVoicemail` in the Schemas appendix)_
- `notifications` — CallFlowNotifications
  - `destinations` — array
    - _array of_ `CallFlowAttachmentDestination`
      - `phone` — string
      - `name` — string
      - `email` — string
      - `userId` — string
      - `userExtension` — string
      - `userDepartment` — string
      - `groupId` — string
      - `groupName` — string
  - `type` — array
    - _array of_ `string`
- `id` — string **(required)**
- `pbx` — string **(required)**
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `licenses` — array **(required)**
  - _array of_ `License`
- `type` — object **(required)**

**`CallRecordOwner`**

- string _(enum: `callee`, `caller`, `system`)_

**`CallRecordPause`**

- `start` — number
- `end` — number
- `reason` — string _(enum: `pause`, `hold`)_

**`CallRecordPauseReason`**

- string _(enum: `pause`, `hold`)_

**`CallTranscriptionChunk`**

- `id` — string **(required)**
- `time` — number **(required)**
- `speaker` — string **(required)** _(enum: `callee`, `caller`)_
- `text` — string **(required)**
- `language` — string
- `isFinal` — boolean **(required)**
- `start` — number **(required)**
- `end` — number **(required)**
- `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
- `sentiment` — string — Sentiment label for a transcription chunk. Shared between calls and conferences. _(enum: `POSITIVE`, `NEGATIVE`, `MIXED`, `NEUTRAL`)_

**`CallTranscriptionInteractionParticipantRecord`**

- `speaker` — string **(required)** _(enum: `callee`, `caller`)_
- `wordsPerMinute` — number — Average words per minute spoken by the participant during the call.
- `talkRatio` — number — Percentage of the call duration during which the participant was speaking.
- `interruptions` — array — List of interruptions where this participant was interrupted during the conversation.
  - _array of_ `CallTranscriptionInterruption`
    - `time` — number **(required)** — Time in milliseconds from the start of the call (e.g., flowStartTime) when the interruption occurred.
    - `chunks` — array **(required)** — IDs of the chunks involved in the interruption — including the interrupting speaker and the chunk that was interrupted.
      - _array of_ `string`

**`CallTranscriptionInteractionRecord`**

- `talkRatio` — number — Percentage of the call duration during which the agent was speaking.
- `wordsPerMinute` — number — Average words per minute spoken by the agent during their speaking time.
- `interruptions` — number — Number of times the agent interrupted another participant during the conversation.
- `patience` — number — Average time in seconds the agent waited after another participant finished speaking before responding. _(format=float)_
- `longestMonologue` — number — Duration in seconds of the agent's longest uninterrupted monologue.
- `longestCustomerStory` — number — Duration in seconds of another participant’s longest uninterrupted story or response.
- `participants` — array — Detailed statistics for each call participant.
  - _array of_ `CallTranscriptionInteractionParticipantRecord`
    - `speaker` — string **(required)** _(enum: `callee`, `caller`)_
    - `wordsPerMinute` — number — Average words per minute spoken by the participant during the call.
    - `talkRatio` — number — Percentage of the call duration during which the participant was speaking.
    - `interruptions` — array — List of interruptions where this participant was interrupted during the conversation.
      - _array of_ `CallTranscriptionInterruption`
        - _(nesting depth limit — see `CallTranscriptionInterruption` in the Schemas appendix)_

**`CallTranscriptionInterruption`**

- `time` — number **(required)** — Time in milliseconds from the start of the call (e.g., flowStartTime) when the interruption occurred.
- `chunks` — array **(required)** — IDs of the chunks involved in the interruption — including the interrupting speaker and the chunk that was interrupted.
  - _array of_ `string`

**`CallTranscriptionNotFoundExceptionResponseContent`**

- `message` — string

**`CallTranscriptionRecord`**

- `id` — string **(required)**
- `pbx` — string **(required)**
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `licenses` — array **(required)**
  - _array of_ `License`
- `type` — object **(required)**
- `flowIndex` — number **(required)**
- `flowStartTime` — number **(required)**
- `callStartTime` — number **(required)**
- `chunks` — array **(required)**
  - _array of_ `CallTranscriptionChunk`
    - `id` — string **(required)**
    - `time` — number **(required)**
    - `speaker` — string **(required)** _(enum: `callee`, `caller`)_
    - `text` — string **(required)**
    - `language` — string
    - `isFinal` — boolean **(required)**
    - `start` — number **(required)**
    - `end` — number **(required)**
    - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
    - `sentiment` — string — Sentiment label for a transcription chunk. Shared between calls and conferences. _(enum: `POSITIVE`, `NEGATIVE`, `MIXED`, `NEUTRAL`)_

**`CallTranscriptionSpeaker`**

- string _(enum: `callee`, `caller`)_

**`Channel`**

- `subject` — string
- `description` — string
- `picture` — string — Picture URL
- `pictureColor` — string — Picture dominant color represented by a hex value.
- `access` — string _(enum: `private`, `public`)_
- `company` — string
- `context` — ChannelContext
  - `source` — string _(enum: `kite`)_
  - `target` — string
  - `events` — array
    - _array of_ `ChannelContextEvent`
      - `id` — string
      - `owner` — string
      - `start` — string
      - `end` — string
      - `summary` — string
      - `attendees` — array
        - _(nesting depth limit — see `ChannelContextEventAttendee` in the Schemas appendix)_
  - `ptt` — ChannelContextPushToTalk
    - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
- `kite` — boolean
- `kiteTarget` — string
- `kiteVariant` — string
- `kiteAssign` — string
- `kiteServiceName` — string
- `kiteDefaultSubject` — string
- `service` — string
- `serviceTitle` — string
- `serviceRecipient` — string
- `assignee` — User
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `name` — string
  - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string
  - `picture` — string
  - `locale` — string
  - `timeZone` — string
  - `company` — string
  - `bot` — boolean
  - `pbxDomain` — string
  - `pbxPort` — string
  - `pbxExtension` — string
  - `pbxSerial` — string
  - `pbxUserId` — string
  - `pbxGroupId` — string
  - `createdAt` — string
  - `updatedAt` — string
- `telephony` — boolean
- `sms` — boolean
- `mms` — boolean
- `whatsapp` — boolean
- `whatsappStatus` — string _(enum: `24h_channel_closed`)_
- `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
- `messagingSenderId` — string
- `messagingReplyUntil` — number
- `broadcast` — boolean
- `external` — boolean
- `autoRecord` — boolean
- `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
- `transcriptionLanguage` — string
- `wizyGuestViewOnly` — boolean
- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `channelType` — string **(required)** _(enum: `direct`, `group`)_
- `memberCount` — number **(required)**
- `createdAt` — string **(required)**
- `createdBy` — string **(required)**
- `updatedAt` — string

**`ChannelAccess`**

- string _(enum: `private`, `public`)_

**`ChannelContext`**

- `source` — string _(enum: `kite`)_
- `target` — string
- `events` — array
  - _array of_ `ChannelContextEvent`
    - `id` — string
    - `owner` — string
    - `start` — string
    - `end` — string
    - `summary` — string
    - `attendees` — array
      - _array of_ `ChannelContextEventAttendee`
        - _(nesting depth limit — see `ChannelContextEventAttendee` in the Schemas appendix)_
- `ptt` — ChannelContextPushToTalk
  - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.

**`ChannelContextEvent`**

- `id` — string
- `owner` — string
- `start` — string
- `end` — string
- `summary` — string
- `attendees` — array
  - _array of_ `ChannelContextEventAttendee`
    - `email` — string **(required)**
    - `name` — string
    - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_

**`ChannelContextEventAttendee`**

- `email` — string **(required)**
- `name` — string
- `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_

**`ChannelContextEventAttendeeStatus`**

- string _(enum: `accepted`, `tentative`, `declined`, `none`)_

**`ChannelContextPushToTalk`**

- `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.

**`ChannelContextSource`**

- string _(enum: `kite`)_

**`ChannelMessagingStatus`**

_Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window._

- string _(enum: `window_closed`)_

**`ChannelType`**

- string _(enum: `direct`, `group`)_

**`ChannelWhatsAppStatus`**

- string _(enum: `24h_channel_closed`)_

**`ChatAnnotationsNotFoundExceptionResponseContent`**

- `message` — string

**`ChatAnnotationsRecord`**

- `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
- `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `type` — object **(required)**
- `annotations` — array **(required)** — Every annotation recorded on the conversation, oldest first — the history of what was observed, superseded readings of a keyed value included. _(maxItems=250)_
  - _array of_ `Annotation`
    - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
    - `time` — number **(required)**
    - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
    - `payload` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`tag`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`variables`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`result`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`metric`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
      - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
      - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
      - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).

**`ChatDirection`**

- string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_

**`ChatNotFoundExceptionResponseContent`**

- `message` — string

**`ChatParticipant`**

- `id` — string **(required)**
- `info` — ChatParticipantInfo **(required)**
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `name` — string
  - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string
  - `picture` — string
  - `locale` — string
  - `timeZone` — string
  - `company` — string
  - `bot` — boolean
  - `pbxDomain` — string
  - `pbxPort` — string
  - `pbxExtension` — string
  - `pbxSerial` — string
  - `pbxUserId` — string
  - `pbxGroupId` — string
  - `createdAt` — string
  - `updatedAt` — string
  - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
  - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_

**`ChatParticipantInfo`**

- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `name` — string
- `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `phone` — string
- `picture` — string
- `locale` — string
- `timeZone` — string
- `company` — string
- `bot` — boolean
- `pbxDomain` — string
- `pbxPort` — string
- `pbxExtension` — string
- `pbxSerial` — string
- `pbxUserId` — string
- `pbxGroupId` — string
- `createdAt` — string
- `updatedAt` — string
- `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
- `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_

**`ChatParticipantRole`**

- string _(enum: `CLIENT`, `AGENT`)_

**`ChatParticipantType`**

- string _(enum: `REMOTE`, `LOCAL`)_

**`ChatRecord`**

- `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
- `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `pbx` — string
- `startTime` — number **(required)**
- `endTime` — number **(required)**
- `waitTime` — number
- `duration` — number **(required)**
- `direction` — string **(required)** _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
- `subject` — string
- `service` — string
- `serviceTitle` — string
- `tags` — array
  - _array of_ `ChatTag`
- `channel` — Channel **(required)**
  - `subject` — string
  - `description` — string
  - `picture` — string — Picture URL
  - `pictureColor` — string — Picture dominant color represented by a hex value.
  - `access` — string _(enum: `private`, `public`)_
  - `company` — string
  - `context` — ChannelContext
    - `source` — string _(enum: `kite`)_
    - `target` — string
    - `events` — array
      - _array of_ `ChannelContextEvent`
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
    - `ptt` — ChannelContextPushToTalk
      - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
  - `kite` — boolean
  - `kiteTarget` — string
  - `kiteVariant` — string
  - `kiteAssign` — string
  - `kiteServiceName` — string
  - `kiteDefaultSubject` — string
  - `service` — string
  - `serviceTitle` — string
  - `serviceRecipient` — string
  - `assignee` — User
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `picture` — string
    - `locale` — string
    - `timeZone` — string
    - `company` — string
    - `bot` — boolean
    - `pbxDomain` — string
    - `pbxPort` — string
    - `pbxExtension` — string
    - `pbxSerial` — string
    - `pbxUserId` — string
    - `pbxGroupId` — string
    - `createdAt` — string
    - `updatedAt` — string
  - `telephony` — boolean
  - `sms` — boolean
  - `mms` — boolean
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
  - `messagingSenderId` — string
  - `messagingReplyUntil` — number
  - `broadcast` — boolean
  - `external` — boolean
  - `autoRecord` — boolean
  - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
  - `transcriptionLanguage` — string
  - `wizyGuestViewOnly` — boolean
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `channelType` — string **(required)** _(enum: `direct`, `group`)_
  - `memberCount` — number **(required)**
  - `createdAt` — string **(required)**
  - `createdBy` — string **(required)**
  - `updatedAt` — string
- `status` — string _(enum: `WAITFIRSTREPLY`, `WAITREPLYFROMGUEST`, `WAITREPLYFROMAGENT`, `COMPLETED`, `MISSED`)_
- `participants` — array **(required)**
  - _array of_ `ChatParticipant`
    - `id` — string **(required)**
    - `info` — ChatParticipantInfo **(required)**
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxDomain` — string
      - `pbxPort` — string
      - `pbxExtension` — string
      - `pbxSerial` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
      - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
      - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
- `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
- `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
  - _map of_ `Annotation`
    - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
    - `time` — number **(required)**
    - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
    - `payload` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`tag`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`variables`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`result`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`metric`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
      - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
      - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
      - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).
- `type` — object **(required)**

**`ChatStatus`**

- string _(enum: `WAITFIRSTREPLY`, `WAITREPLYFROMGUEST`, `WAITREPLYFROMAGENT`, `COMPLETED`, `MISSED`)_

**`ChatTag`**

- string _(enum: `sms`, `telephony`, `whatsapp`)_

**`ChatTranscriptionNotFoundExceptionResponseContent`**

- `message` — string

**`ChatTranscriptionRecord`**

- `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
- `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `type` — object **(required)**
- `messages` — array **(required)**
  - _array of_ `Message`
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `user` — User **(required)**
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxDomain` — string
      - `pbxPort` — string
      - `pbxExtension` — string
      - `pbxSerial` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
    - `edit` — boolean
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `latestReactions` — array
      - _array of_ `Reaction`
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`ChatVerbosity`**

_How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text._

- string _(enum: `none`, `simple`, `full`)_

**`ConferenceAnalyticsRecordParticipant`**

- `jid` — string **(required)**
- `info` — ConferenceParticipant **(required)**
  - `type` — string **(required)** _(enum: `EXTERNAL`, `EXTERNAL_DIAL_IN`, `PBX`, `PBX_SIP`, `XBS`)_
  - `role` — string _(enum: `CLIENT`, `AGENT`)_
  - `jid` — string — A unique identifier to avoid duplicates if user re-connect from different devices.
  - `name` — string
  - `email` — string
  - `phone` — string
  - `department` — string
  - `company` — string _(minLen=3; maxLen=30)_
  - `pbxSerial` — string
  - `pbxExtension` — string
  - `pbxGroupId` — string
  - `xbsId` — string
  - `license` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
- `totalDuration` — number **(required)**
- `totalSpeakDuration` — number **(required)**
- `joinTime` — number **(required)**

**`ConferenceAnnotationsNotFoundExceptionResponseContent`**

- `message` — string

**`ConferenceAnnotationsRecord`**

- `id` — string **(required)**
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `type` — object **(required)**
- `annotations` — array **(required)** — Every annotation recorded on the conversation, oldest first — the history of what was observed, superseded readings of a keyed value included. _(maxItems=250)_
  - _array of_ `Annotation`
    - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
    - `time` — number **(required)**
    - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
    - `payload` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`tag`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`variables`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`result`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`metric`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
      - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
      - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
      - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).

**`ConferenceDirection`**

- string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_

**`ConferenceNotFoundExceptionResponseContent`**

- `message` — string

**`ConferenceParticipant`**

- `type` — string **(required)** _(enum: `EXTERNAL`, `EXTERNAL_DIAL_IN`, `PBX`, `PBX_SIP`, `XBS`)_
- `role` — string _(enum: `CLIENT`, `AGENT`)_
- `jid` — string — A unique identifier to avoid duplicates if user re-connect from different devices.
- `name` — string
- `email` — string
- `phone` — string
- `department` — string
- `company` — string _(minLen=3; maxLen=30)_
- `pbxSerial` — string
- `pbxExtension` — string
- `pbxGroupId` — string
- `xbsId` — string
- `license` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_

**`ConferenceParticipantRole`**

- string _(enum: `CLIENT`, `AGENT`)_

**`ConferenceParticipantType`**

- string _(enum: `EXTERNAL`, `EXTERNAL_DIAL_IN`, `PBX`, `PBX_SIP`, `XBS`)_

**`ConferenceRecord`**

- `id` — string **(required)**
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `pbx` — string
- `startTime` — number **(required)**
- `endTime` — number **(required)**
- `duration` — number **(required)**
- `waitTime` — number
- `subject` — string
- `direction` — string **(required)** _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
- `service` — string
- `status` — string _(enum: `COMPLETED`, `MISSED`)_
- `participants` — array **(required)**
  - _array of_ `ConferenceAnalyticsRecordParticipant`
    - `jid` — string **(required)**
    - `info` — ConferenceParticipant **(required)**
      - `type` — string **(required)** _(enum: `EXTERNAL`, `EXTERNAL_DIAL_IN`, `PBX`, `PBX_SIP`, `XBS`)_
      - `role` — string _(enum: `CLIENT`, `AGENT`)_
      - `jid` — string — A unique identifier to avoid duplicates if user re-connect from different devices.
      - `name` — string
      - `email` — string
      - `phone` — string
      - `department` — string
      - `company` — string _(minLen=3; maxLen=30)_
      - `pbxSerial` — string
      - `pbxExtension` — string
      - `pbxGroupId` — string
      - `xbsId` — string
      - `license` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
    - `totalDuration` — number **(required)**
    - `totalSpeakDuration` — number **(required)**
    - `joinTime` — number **(required)**
- `recordings` — array
  - _array of_ `ConferenceRecording`
    - `url` — string **(required)**
    - `start` — number **(required)**
    - `end` — number **(required)**
- `transcriptionStatus` — string **(required)** _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
- `transcriptionLanguage` — string
- `transcriptionSeconds` — number
- `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
- `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
  - _map of_ `Annotation`
    - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
    - `time` — number **(required)**
    - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
    - `payload` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`tag`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`variables`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`result`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`metric`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
      - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
      - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
      - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).
- `type` — object **(required)**

**`ConferenceRecording`**

- `url` — string **(required)**
- `start` — number **(required)**
- `end` — number **(required)**

**`ConferenceTranscription`**

- `start` — number **(required)**
- `end` — number **(required)**
- `chunks` — array **(required)**
  - _array of_ `ConferenceTranscriptionChunk`
    - `id` — string **(required)**
    - `time` — number **(required)**
    - `jid` — string **(required)**
    - `text` — string **(required)**
    - `language` — string
    - `isFinal` — boolean **(required)**
    - `start` — number **(required)**
    - `end` — number **(required)**
    - `sentiment` — string — Sentiment label for a transcription chunk. Shared between calls and conferences. _(enum: `POSITIVE`, `NEGATIVE`, `MIXED`, `NEUTRAL`)_

**`ConferenceTranscriptionChunk`**

- `id` — string **(required)**
- `time` — number **(required)**
- `jid` — string **(required)**
- `text` — string **(required)**
- `language` — string
- `isFinal` — boolean **(required)**
- `start` — number **(required)**
- `end` — number **(required)**
- `sentiment` — string — Sentiment label for a transcription chunk. Shared between calls and conferences. _(enum: `POSITIVE`, `NEGATIVE`, `MIXED`, `NEUTRAL`)_

**`ConferenceTranscriptionInteractionParticipantRecord`**

- `jid` — string **(required)** — Unique identifier (JID) of the participant.
- `wordsPerMinute` — number — Average words per minute spoken by the participant during the call.
- `talkRatio` — number — Percentage of the call duration during which the participant was speaking.
- `interruptions` — array — List of interruptions where this participant interrupted or was interrupted during the conversation.
  - _array of_ `ConferenceTranscriptionInterruption`
    - `time` — number **(required)** — Time in milliseconds from the start of the call (e.g., flowStartTime) when the interruption occurred.
    - `chunks` — array **(required)** — IDs of the conversation chunks involved in the interruption, including both the interrupting and interrupted speakers.
      - _array of_ `string`

**`ConferenceTranscriptionInteractionRecord`**

- `talkRatio` — number — Percentage of the call duration during which the agent was speaking.
- `wordsPerMinute` — number — Average words per minute spoken by the agent during their speaking time.
- `interruptions` — number — Number of times the agent interrupted another participant during the conversation.
- `patience` — number — Average time in seconds the agent waited after another participant finished speaking before responding. _(format=float)_
- `longestMonologue` — number — Duration in seconds of the agent's longest uninterrupted monologue.
- `longestCustomerStory` — number — Duration in seconds of another participant’s longest uninterrupted story or response.
- `participants` — array — Detailed statistics for each participant in the call.
  - _array of_ `ConferenceTranscriptionInteractionParticipantRecord`
    - `jid` — string **(required)** — Unique identifier (JID) of the participant.
    - `wordsPerMinute` — number — Average words per minute spoken by the participant during the call.
    - `talkRatio` — number — Percentage of the call duration during which the participant was speaking.
    - `interruptions` — array — List of interruptions where this participant interrupted or was interrupted during the conversation.
      - _array of_ `ConferenceTranscriptionInterruption`
        - _(nesting depth limit — see `ConferenceTranscriptionInterruption` in the Schemas appendix)_

**`ConferenceTranscriptionInterruption`**

- `time` — number **(required)** — Time in milliseconds from the start of the call (e.g., flowStartTime) when the interruption occurred.
- `chunks` — array **(required)** — IDs of the conversation chunks involved in the interruption, including both the interrupting and interrupted speakers.
  - _array of_ `string`

**`ConferenceTranscriptionNotFoundExceptionResponseContent`**

- `message` — string

**`ConferenceTranscriptionRecord`**

- `id` — string **(required)**
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `type` — object **(required)**
- `transcriptions` — array **(required)**
  - _array of_ `ConferenceTranscription`
    - `start` — number **(required)**
    - `end` — number **(required)**
    - `chunks` — array **(required)**
      - _array of_ `ConferenceTranscriptionChunk`
        - _(nesting depth limit — see `ConferenceTranscriptionChunk` in the Schemas appendix)_

**`ConferenceTranscriptionStatus`**

- string _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_

**`Conversation`**

- _oneOf_ — exactly one of:
  - **`call`**
    - `call` — CallRecord **(required)**
      - `flowIndex` — number **(required)**
      - `startTime` — number **(required)**
      - `endTime` — number **(required)**
      - `connectTime` — number — Duration when the called party's phone rang (Ring Time in UI)
      - `talkTime` — number — Duration of conversation from the moment the call is answered until it ends, excluding hold time
      - `waitTime` — number — Duration spent on IVR, dialplan applications, playback, etc. before the call is answered
      - `queueTime` — number — Duration of call waiting in queue
      - `holdTime` — number — Duration the call was on hold after being answered
      - `duration` — number **(required)** — Total duration = connectTime + waitTime + queueTime + talkTime + holdTime
      - `caller` — CallParticipant
        - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
        - `phone` — string
        - `name` — string
        - `company` — string _(minLen=3; maxLen=30)_
        - `email` — string
        - `userId` — string
        - `userExtension` — string
        - `userDepartment` — string
        - `groupId` — string
        - `groupName` — string
        - `userAgent` — string
        - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
        - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
        - `license` — string
        - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
        - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
        - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
        - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
      - `callee` — CallParticipant
        - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
        - `phone` — string
        - `name` — string
        - `company` — string _(minLen=3; maxLen=30)_
        - `email` — string
        - `userId` — string
        - `userExtension` — string
        - `userDepartment` — string
        - `groupId` — string
        - `groupName` — string
        - `userAgent` — string
        - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
        - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
        - `license` — string
        - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
        - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
        - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
        - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
      - `service` — string
      - `serviceNumber` — string
      - `destination` — string
      - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
      - `trunkName` — string
      - `trunkDirection` — string
      - `queueName` — string
      - `queueId` — string
      - `queuePosition` — number — Position of the call in the queue (1-based). Updated from consume events and emitted on live progress and record flows.
      - `tags` — array
        - _array of_ `string`
      - `flags` — array
        - _array of_ `string`
      - `callerMos` — string
      - `calleeMos` — string
      - `xhoppersConfId` — string
      - `recordings` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
        - _array of_ `string`
      - `recordingsData` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
        - _array of_ `CallFlowRecording`
          - _(nesting depth limit — see `CallFlowRecording` in the Schemas appendix)_
      - `mergeWith` — string
      - `splitReason` — string
      - `splitTransferType` — string
      - `remotePhone` — string
      - `remotePhoneCountryCode` — number
      - `remotePhoneCountryCodeStr` — string
      - `remotePhoneLocation` — string
      - `callStatus` — string _(enum: `COMPLETED`, `MISSED`)_
      - `transcriptionStatus` — string _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
      - `transcriptionLanguage` — string
      - `transcriptionSeconds` — number
      - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
      - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
        - _map of_ `Annotation`
          - _(nesting depth limit — see `Annotation` in the Schemas appendix)_
      - `attachment` — string — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
      - `attachmentType` — string _(enum: `VOICEMAIL`, `FAX`)_
      - `attachmentDestinations` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
        - _array of_ `CallFlowAttachmentDestination`
          - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
      - `attachments` — array
        - _array of_ `CallFlowAttachment`
          - _(nesting depth limit — see `CallFlowAttachment` in the Schemas appendix)_
      - `notifications` — CallFlowNotifications
        - `destinations` — array
          - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
        - `type` — array
          - _array of_ `string`
      - `id` — string **(required)**
      - `pbx` — string **(required)**
      - `time` — number **(required)**
      - `company` — string **(required)** _(minLen=3; maxLen=30)_
      - `licenses` — array **(required)**
        - _array of_ `License`
      - `type` — object **(required)**
  - **`conference`**
    - `conference` — ConferenceRecord **(required)**
      - `id` — string **(required)**
      - `time` — number **(required)**
      - `company` — string **(required)** _(minLen=3; maxLen=30)_
      - `pbx` — string
      - `startTime` — number **(required)**
      - `endTime` — number **(required)**
      - `duration` — number **(required)**
      - `waitTime` — number
      - `subject` — string
      - `direction` — string **(required)** _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
      - `service` — string
      - `status` — string _(enum: `COMPLETED`, `MISSED`)_
      - `participants` — array **(required)**
        - _array of_ `ConferenceAnalyticsRecordParticipant`
          - _(nesting depth limit — see `ConferenceAnalyticsRecordParticipant` in the Schemas appendix)_
      - `recordings` — array
        - _array of_ `ConferenceRecording`
          - _(nesting depth limit — see `ConferenceRecording` in the Schemas appendix)_
      - `transcriptionStatus` — string **(required)** _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
      - `transcriptionLanguage` — string
      - `transcriptionSeconds` — number
      - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
      - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
        - _map of_ `Annotation`
          - _(nesting depth limit — see `Annotation` in the Schemas appendix)_
      - `type` — object **(required)**

**`ConversationDirection`**

- string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_

**`ConversationFlag`**

- string _(enum: `FAX`, `VOICEMAIL`)_

**`ConversationStatus`**

- string _(enum: `COMPLETED`, `MISSED`)_

**`ConversationUserDirection`**

- string _(enum: `INCOMING`, `OUTGOING`)_

**`Element`**

- _oneOf_ — exactly one of:
  - **`template`**
    - `template` — MessageTemplateConfig **(required)**
      - `whatsapp` — TemplateWithParameters
        - `name` — string **(required)**
        - `parameters` — array
          - _(nesting depth limit — see `TemplateParameter` in the Schemas appendix)_
  - **`actions`**
    - `actions` — array **(required)**
      - _array of_ `ActionElement`
        - _oneOf_ — exactly one of:
          - **`button`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - **`wilma`**
    - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
      - `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
      - `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
      - `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
      - `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
      - `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
      - `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
        - `outcome` — string **(required)** — How the turn ended. _(enum: `done`, `stopped`, `failed`)_
        - `durationMs` — number — From the turn's start to its end. Absent when the turn had not ended.
        - `toolCount` — number **(required)** — Steps the turn took, counted as the Wilma assistant counts its work steps: each tool call and each sandbox step (`SandboxStartedEvent`, `SandboxFailedEvent`).
        - `failedCount` — number **(required)** — Steps that failed: calls that failed, including those the stop or failure cut off, and sandbox steps that failed.
      - `artifacts` — array
        - _array of_ `WilmaChatArtifact`
          - _(nesting depth limit — see `WilmaChatArtifact` in the Schemas appendix)_

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetCallAnnotationsResponseContent`**

- `annotations` — CallAnnotationsRecord **(required)**
  - `id` — string **(required)**
  - `pbx` — string **(required)**
  - `time` — number **(required)**
  - `company` — string **(required)** _(minLen=3; maxLen=30)_
  - `licenses` — array **(required)**
    - _array of_ `License`
  - `type` — object **(required)**
  - `flowIndex` — number **(required)**
  - `flowStartTime` — number **(required)**
  - `callStartTime` — number **(required)**
  - `annotations` — array **(required)** — Every annotation recorded on the conversation, oldest first — the history of what was observed, superseded readings of a keyed value included. _(maxItems=250)_
    - _array of_ `Annotation`
      - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
      - `time` — number **(required)**
      - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
      - `payload` — union **(required)**
        - _(nesting depth limit — see `AnnotationPayload` in the Schemas appendix)_
      - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
        - _(nesting depth limit — see `AnnotationSource` in the Schemas appendix)_

**`GetCallResponseContent`**

- `call` — CallRecord **(required)**
  - `flowIndex` — number **(required)**
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**
  - `connectTime` — number — Duration when the called party's phone rang (Ring Time in UI)
  - `talkTime` — number — Duration of conversation from the moment the call is answered until it ends, excluding hold time
  - `waitTime` — number — Duration spent on IVR, dialplan applications, playback, etc. before the call is answered
  - `queueTime` — number — Duration of call waiting in queue
  - `holdTime` — number — Duration the call was on hold after being answered
  - `duration` — number **(required)** — Total duration = connectTime + waitTime + queueTime + talkTime + holdTime
  - `caller` — CallParticipant
    - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
    - `phone` — string
    - `name` — string
    - `company` — string _(minLen=3; maxLen=30)_
    - `email` — string
    - `userId` — string
    - `userExtension` — string
    - `userDepartment` — string
    - `groupId` — string
    - `groupName` — string
    - `userAgent` — string
    - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
    - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
    - `license` — string
    - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
    - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
    - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
    - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
  - `callee` — CallParticipant
    - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
    - `phone` — string
    - `name` — string
    - `company` — string _(minLen=3; maxLen=30)_
    - `email` — string
    - `userId` — string
    - `userExtension` — string
    - `userDepartment` — string
    - `groupId` — string
    - `groupName` — string
    - `userAgent` — string
    - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
    - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
    - `license` — string
    - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
    - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
    - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
    - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
  - `service` — string
  - `serviceNumber` — string
  - `destination` — string
  - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
  - `trunkName` — string
  - `trunkDirection` — string
  - `queueName` — string
  - `queueId` — string
  - `queuePosition` — number — Position of the call in the queue (1-based). Updated from consume events and emitted on live progress and record flows.
  - `tags` — array
    - _array of_ `string`
  - `flags` — array
    - _array of_ `string`
  - `callerMos` — string
  - `calleeMos` — string
  - `xhoppersConfId` — string
  - `recordings` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
    - _array of_ `string`
  - `recordingsData` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
    - _array of_ `CallFlowRecording`
      - `fileName` — string **(required)**
      - `start` — number **(required)**
      - `end` — number **(required)**
      - `owner` — string **(required)** _(enum: `callee`, `caller`, `system`)_
      - `url` — string **(required)**
      - `pauses` — array **(required)**
        - _(nesting depth limit — see `CallRecordPause` in the Schemas appendix)_
  - `mergeWith` — string
  - `splitReason` — string
  - `splitTransferType` — string
  - `remotePhone` — string
  - `remotePhoneCountryCode` — number
  - `remotePhoneCountryCodeStr` — string
  - `remotePhoneLocation` — string
  - `callStatus` — string _(enum: `COMPLETED`, `MISSED`)_
  - `transcriptionStatus` — string _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
  - `transcriptionLanguage` — string
  - `transcriptionSeconds` — number
  - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
  - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
    - _map of_ `Annotation`
      - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
      - `time` — number **(required)**
      - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
      - `payload` — union **(required)**
        - _(nesting depth limit — see `AnnotationPayload` in the Schemas appendix)_
      - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
        - _(nesting depth limit — see `AnnotationSource` in the Schemas appendix)_
  - `attachment` — string — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
  - `attachmentType` — string _(enum: `VOICEMAIL`, `FAX`)_
  - `attachmentDestinations` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
    - _array of_ `CallFlowAttachmentDestination`
      - `phone` — string
      - `name` — string
      - `email` — string
      - `userId` — string
      - `userExtension` — string
      - `userDepartment` — string
      - `groupId` — string
      - `groupName` — string
  - `attachments` — array
    - _array of_ `CallFlowAttachment`
      - _oneOf_ — exactly one of:
        - **`recording`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`fax`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`voicemail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `notifications` — CallFlowNotifications
    - `destinations` — array
      - _array of_ `CallFlowAttachmentDestination`
        - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
    - `type` — array
      - _array of_ `string`
  - `id` — string **(required)**
  - `pbx` — string **(required)**
  - `time` — number **(required)**
  - `company` — string **(required)** _(minLen=3; maxLen=30)_
  - `licenses` — array **(required)**
    - _array of_ `License`
  - `type` — object **(required)**

**`GetCallTranscriptionResponseContent`**

- `transcription` — CallTranscriptionRecord **(required)**
  - `id` — string **(required)**
  - `pbx` — string **(required)**
  - `time` — number **(required)**
  - `company` — string **(required)** _(minLen=3; maxLen=30)_
  - `licenses` — array **(required)**
    - _array of_ `License`
  - `type` — object **(required)**
  - `flowIndex` — number **(required)**
  - `flowStartTime` — number **(required)**
  - `callStartTime` — number **(required)**
  - `chunks` — array **(required)**
    - _array of_ `CallTranscriptionChunk`
      - `id` — string **(required)**
      - `time` — number **(required)**
      - `speaker` — string **(required)** _(enum: `callee`, `caller`)_
      - `text` — string **(required)**
      - `language` — string
      - `isFinal` — boolean **(required)**
      - `start` — number **(required)**
      - `end` — number **(required)**
      - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
      - `sentiment` — string — Sentiment label for a transcription chunk. Shared between calls and conferences. _(enum: `POSITIVE`, `NEGATIVE`, `MIXED`, `NEUTRAL`)_
- `interaction` — CallTranscriptionInteractionRecord
  - `talkRatio` — number — Percentage of the call duration during which the agent was speaking.
  - `wordsPerMinute` — number — Average words per minute spoken by the agent during their speaking time.
  - `interruptions` — number — Number of times the agent interrupted another participant during the conversation.
  - `patience` — number — Average time in seconds the agent waited after another participant finished speaking before responding. _(format=float)_
  - `longestMonologue` — number — Duration in seconds of the agent's longest uninterrupted monologue.
  - `longestCustomerStory` — number — Duration in seconds of another participant’s longest uninterrupted story or response.
  - `participants` — array — Detailed statistics for each call participant.
    - _array of_ `CallTranscriptionInteractionParticipantRecord`
      - `speaker` — string **(required)** _(enum: `callee`, `caller`)_
      - `wordsPerMinute` — number — Average words per minute spoken by the participant during the call.
      - `talkRatio` — number — Percentage of the call duration during which the participant was speaking.
      - `interruptions` — array — List of interruptions where this participant was interrupted during the conversation.
        - _(nesting depth limit — see `CallTranscriptionInterruption` in the Schemas appendix)_

**`GetCallTranscriptionTextResponseContent`**

- `filename` — string **(required)**
- `text` — string **(required)**
- `chunks` — array **(required)**
  - _array of_ `TranscriptionTextChunk`
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `text` — string **(required)**
    - `time` — string **(required)**
    - `offset` — number **(required)**

**`GetChatAnnotationsResponseContent`**

- `annotations` — ChatAnnotationsRecord **(required)**
  - `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
  - `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
  - `time` — number **(required)**
  - `company` — string **(required)** _(minLen=3; maxLen=30)_
  - `type` — object **(required)**
  - `annotations` — array **(required)** — Every annotation recorded on the conversation, oldest first — the history of what was observed, superseded readings of a keyed value included. _(maxItems=250)_
    - _array of_ `Annotation`
      - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
      - `time` — number **(required)**
      - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
      - `payload` — union **(required)**
        - _(nesting depth limit — see `AnnotationPayload` in the Schemas appendix)_
      - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
        - _(nesting depth limit — see `AnnotationSource` in the Schemas appendix)_

**`GetChatResponseContent`**

- `chat` — ChatRecord **(required)**
  - `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
  - `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
  - `time` — number **(required)**
  - `company` — string **(required)** _(minLen=3; maxLen=30)_
  - `pbx` — string
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**
  - `waitTime` — number
  - `duration` — number **(required)**
  - `direction` — string **(required)** _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
  - `subject` — string
  - `service` — string
  - `serviceTitle` — string
  - `tags` — array
    - _array of_ `ChatTag`
  - `channel` — Channel **(required)**
    - `subject` — string
    - `description` — string
    - `picture` — string — Picture URL
    - `pictureColor` — string — Picture dominant color represented by a hex value.
    - `access` — string _(enum: `private`, `public`)_
    - `company` — string
    - `context` — ChannelContext
      - `source` — string _(enum: `kite`)_
      - `target` — string
      - `events` — array
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
    - `kite` — boolean
    - `kiteTarget` — string
    - `kiteVariant` — string
    - `kiteAssign` — string
    - `kiteServiceName` — string
    - `kiteDefaultSubject` — string
    - `service` — string
    - `serviceTitle` — string
    - `serviceRecipient` — string
    - `assignee` — User
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxDomain` — string
      - `pbxPort` — string
      - `pbxExtension` — string
      - `pbxSerial` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
    - `telephony` — boolean
    - `sms` — boolean
    - `mms` — boolean
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
    - `messagingSenderId` — string
    - `messagingReplyUntil` — number
    - `broadcast` — boolean
    - `external` — boolean
    - `autoRecord` — boolean
    - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
    - `transcriptionLanguage` — string
    - `wizyGuestViewOnly` — boolean
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `channelType` — string **(required)** _(enum: `direct`, `group`)_
    - `memberCount` — number **(required)**
    - `createdAt` — string **(required)**
    - `createdBy` — string **(required)**
    - `updatedAt` — string
  - `status` — string _(enum: `WAITFIRSTREPLY`, `WAITREPLYFROMGUEST`, `WAITREPLYFROMAGENT`, `COMPLETED`, `MISSED`)_
  - `participants` — array **(required)**
    - _array of_ `ChatParticipant`
      - `id` — string **(required)**
      - `info` — ChatParticipantInfo **(required)**
        - _(nesting depth limit — see `ChatParticipantInfo` in the Schemas appendix)_
  - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
  - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
    - _map of_ `Annotation`
      - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
      - `time` — number **(required)**
      - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
      - `payload` — union **(required)**
        - _(nesting depth limit — see `AnnotationPayload` in the Schemas appendix)_
      - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
        - _(nesting depth limit — see `AnnotationSource` in the Schemas appendix)_
  - `type` — object **(required)**

**`GetChatTranscriptionResponseContent`**

- `transcription` — ChatTranscriptionRecord **(required)**
  - `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
  - `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
  - `time` — number **(required)**
  - `company` — string **(required)** _(minLen=3; maxLen=30)_
  - `type` — object **(required)**
  - `messages` — array **(required)**
    - _array of_ `Message`
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `quote` — MessageQuote
        - _(nesting depth limit — see `MessageQuote` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
      - `sms` — boolean
      - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
      - `markdown` — boolean
      - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `silent` — boolean
      - `event` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `edit` — boolean
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `latestReactions` — array
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
      - `reactionCounts` — ReactionCounts
        - _(nesting depth limit — see `ReactionCounts` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string

**`GetChatTranscriptionTextResponseContent`**

- `filename` — string **(required)**
- `text` — string **(required)**
- `messages` — array **(required)**
  - _array of_ `Message`
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `user` — User **(required)**
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxDomain` — string
      - `pbxPort` — string
      - `pbxExtension` — string
      - `pbxSerial` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
    - `edit` — boolean
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `latestReactions` — array
      - _array of_ `Reaction`
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`GetConferenceAnnotationsResponseContent`**

- `annotations` — ConferenceAnnotationsRecord **(required)**
  - `id` — string **(required)**
  - `time` — number **(required)**
  - `company` — string **(required)** _(minLen=3; maxLen=30)_
  - `type` — object **(required)**
  - `annotations` — array **(required)** — Every annotation recorded on the conversation, oldest first — the history of what was observed, superseded readings of a keyed value included. _(maxItems=250)_
    - _array of_ `Annotation`
      - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
      - `time` — number **(required)**
      - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
      - `payload` — union **(required)**
        - _(nesting depth limit — see `AnnotationPayload` in the Schemas appendix)_
      - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
        - _(nesting depth limit — see `AnnotationSource` in the Schemas appendix)_

**`GetConferenceResponseContent`**

- `conference` — ConferenceRecord **(required)**
  - `id` — string **(required)**
  - `time` — number **(required)**
  - `company` — string **(required)** _(minLen=3; maxLen=30)_
  - `pbx` — string
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**
  - `duration` — number **(required)**
  - `waitTime` — number
  - `subject` — string
  - `direction` — string **(required)** _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
  - `service` — string
  - `status` — string _(enum: `COMPLETED`, `MISSED`)_
  - `participants` — array **(required)**
    - _array of_ `ConferenceAnalyticsRecordParticipant`
      - `jid` — string **(required)**
      - `info` — ConferenceParticipant **(required)**
        - _(nesting depth limit — see `ConferenceParticipant` in the Schemas appendix)_
      - `totalDuration` — number **(required)**
      - `totalSpeakDuration` — number **(required)**
      - `joinTime` — number **(required)**
  - `recordings` — array
    - _array of_ `ConferenceRecording`
      - `url` — string **(required)**
      - `start` — number **(required)**
      - `end` — number **(required)**
  - `transcriptionStatus` — string **(required)** _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
  - `transcriptionLanguage` — string
  - `transcriptionSeconds` — number
  - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
  - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
    - _map of_ `Annotation`
      - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
      - `time` — number **(required)**
      - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
      - `payload` — union **(required)**
        - _(nesting depth limit — see `AnnotationPayload` in the Schemas appendix)_
      - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
        - _(nesting depth limit — see `AnnotationSource` in the Schemas appendix)_
  - `type` — object **(required)**

**`GetConferenceTranscriptionResponseContent`**

- `transcription` — ConferenceTranscriptionRecord **(required)**
  - `id` — string **(required)**
  - `time` — number **(required)**
  - `company` — string **(required)** _(minLen=3; maxLen=30)_
  - `type` — object **(required)**
  - `transcriptions` — array **(required)**
    - _array of_ `ConferenceTranscription`
      - `start` — number **(required)**
      - `end` — number **(required)**
      - `chunks` — array **(required)**
        - _(nesting depth limit — see `ConferenceTranscriptionChunk` in the Schemas appendix)_
- `interaction` — ConferenceTranscriptionInteractionRecord
  - `talkRatio` — number — Percentage of the call duration during which the agent was speaking.
  - `wordsPerMinute` — number — Average words per minute spoken by the agent during their speaking time.
  - `interruptions` — number — Number of times the agent interrupted another participant during the conversation.
  - `patience` — number — Average time in seconds the agent waited after another participant finished speaking before responding. _(format=float)_
  - `longestMonologue` — number — Duration in seconds of the agent's longest uninterrupted monologue.
  - `longestCustomerStory` — number — Duration in seconds of another participant’s longest uninterrupted story or response.
  - `participants` — array — Detailed statistics for each participant in the call.
    - _array of_ `ConferenceTranscriptionInteractionParticipantRecord`
      - `jid` — string **(required)** — Unique identifier (JID) of the participant.
      - `wordsPerMinute` — number — Average words per minute spoken by the participant during the call.
      - `talkRatio` — number — Percentage of the call duration during which the participant was speaking.
      - `interruptions` — array — List of interruptions where this participant interrupted or was interrupted during the conversation.
        - _(nesting depth limit — see `ConferenceTranscriptionInterruption` in the Schemas appendix)_

**`GetConferenceTranscriptionTextResponseContent`**

- `filename` — string **(required)**
- `text` — string **(required)**
- `chunks` — array **(required)**
  - _array of_ `TranscriptionTextChunk`
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `text` — string **(required)**
    - `time` — string **(required)**
    - `offset` — number **(required)**

**`License`**

- string _(enum: `x-bees`, `uc`)_

**`Message`**

- `text` — string _(minLen=1; maxLen=5000)_
- `elements` — array
  - _array of_ `Element`
    - _oneOf_ — exactly one of:
      - **`template`**
        - `template` — MessageTemplateConfig **(required)**
          - _(nesting depth limit — see `MessageTemplateConfig` in the Schemas appendix)_
      - **`actions`**
        - `actions` — array **(required)**
          - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
      - **`wilma`**
        - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
          - _(nesting depth limit — see `WilmaChatElement` in the Schemas appendix)_
- `attachments` — array
  - _array of_ `MessageAttachment`
    - `id` — string **(required)**
    - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
    - `mime` — string
    - `name` — string **(required)**
    - `size` — number **(required)**
    - `width` — number
    - `height` — number
    - `thumbnail` — string
- `quote` — MessageQuote
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` — User **(required)**
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `picture` — string
    - `locale` — string
    - `timeZone` — string
    - `company` — string
    - `bot` — boolean
    - `pbxDomain` — string
    - `pbxPort` — string
    - `pbxExtension` — string
    - `pbxSerial` — string
    - `pbxUserId` — string
    - `pbxGroupId` — string
    - `createdAt` — string
    - `updatedAt` — string
  - `text` — string _(minLen=1; maxLen=5000)_
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `mentions` — array
    - _array of_ `User`
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxDomain` — string
      - `pbxPort` — string
      - `pbxExtension` — string
      - `pbxSerial` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string
- `forward` — MessageForward
  - `forwardCompany` — string
  - `forwardDate` — string **(required)**
  - `forwardEmail` — string
  - `forwardName` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `whatsapp` — boolean
- `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
- `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
- `sms` — boolean
- `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
- `markdown` — boolean
- `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
- `giphy` — MessageGiphy
  - `id` — string **(required)** _(minLen=1)_
  - `size` — string **(required)** _(pattern=^\d+$)_
  - `url` — string **(required)** _(minLen=1)_
  - `height` — string **(required)** _(pattern=^\d+$)_
  - `width` — string **(required)** _(pattern=^\d+$)_
- `silent` — boolean
- `event` — string
- `messageId` — string **(required)** _(minLen=32; maxLen=32)_
- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `user` — User **(required)**
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `name` — string
  - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string
  - `picture` — string
  - `locale` — string
  - `timeZone` — string
  - `company` — string
  - `bot` — boolean
  - `pbxDomain` — string
  - `pbxPort` — string
  - `pbxExtension` — string
  - `pbxSerial` — string
  - `pbxUserId` — string
  - `pbxGroupId` — string
  - `createdAt` — string
  - `updatedAt` — string
- `edit` — boolean
- `mentions` — array
  - _array of_ `User`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `picture` — string
    - `locale` — string
    - `timeZone` — string
    - `company` — string
    - `bot` — boolean
    - `pbxDomain` — string
    - `pbxPort` — string
    - `pbxExtension` — string
    - `pbxSerial` — string
    - `pbxUserId` — string
    - `pbxGroupId` — string
    - `createdAt` — string
    - `updatedAt` — string
- `latestReactions` — array
  - _array of_ `Reaction`
    - `type` — string
    - `userId` — string _(minLen=12; maxLen=12)_
    - `messageId` — string
    - `user` — User
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxDomain` — string
      - `pbxPort` — string
      - `pbxExtension` — string
      - `pbxSerial` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
- `reactionCounts` — ReactionCounts
  - _map of_ `number`
- `createdAt` — string **(required)**
- `updatedAt` — string

**`MessageAttachment`**

- `id` — string **(required)**
- `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
- `mime` — string
- `name` — string **(required)**
- `size` — number **(required)**
- `width` — number
- `height` — number
- `thumbnail` — string

**`MessageForward`**

- `forwardCompany` — string
- `forwardDate` — string **(required)**
- `forwardEmail` — string
- `forwardName` — string
- `messageId` — string **(required)** _(minLen=32; maxLen=32)_
- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_

**`MessageGiphy`**

- `id` — string **(required)** _(minLen=1)_
- `size` — string **(required)** _(pattern=^\d+$)_
- `url` — string **(required)** _(minLen=1)_
- `height` — string **(required)** _(pattern=^\d+$)_
- `width` — string **(required)** _(pattern=^\d+$)_

**`MessageMessagingStatus`**

_The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier._

- string _(enum: `trying`, `sent`, `error`, `delivered`)_

**`MessageQuote`**

- `messageId` — string **(required)** _(minLen=32; maxLen=32)_
- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `user` — User **(required)**
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `name` — string
  - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string
  - `picture` — string
  - `locale` — string
  - `timeZone` — string
  - `company` — string
  - `bot` — boolean
  - `pbxDomain` — string
  - `pbxPort` — string
  - `pbxExtension` — string
  - `pbxSerial` — string
  - `pbxUserId` — string
  - `pbxGroupId` — string
  - `createdAt` — string
  - `updatedAt` — string
- `text` — string _(minLen=1; maxLen=5000)_
- `attachments` — array
  - _array of_ `MessageAttachment`
    - `id` — string **(required)**
    - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
    - `mime` — string
    - `name` — string **(required)**
    - `size` — number **(required)**
    - `width` — number
    - `height` — number
    - `thumbnail` — string
- `forward` — MessageForward
  - `forwardCompany` — string
  - `forwardDate` — string **(required)**
  - `forwardEmail` — string
  - `forwardName` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `mentions` — array
  - _array of_ `User`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `picture` — string
    - `locale` — string
    - `timeZone` — string
    - `company` — string
    - `bot` — boolean
    - `pbxDomain` — string
    - `pbxPort` — string
    - `pbxExtension` — string
    - `pbxSerial` — string
    - `pbxUserId` — string
    - `pbxGroupId` — string
    - `createdAt` — string
    - `updatedAt` — string
- `giphy` — MessageGiphy
  - `id` — string **(required)** _(minLen=1)_
  - `size` — string **(required)** _(pattern=^\d+$)_
  - `url` — string **(required)** _(minLen=1)_
  - `height` — string **(required)** _(pattern=^\d+$)_
  - `width` — string **(required)** _(pattern=^\d+$)_
- `createdAt` — string **(required)**
- `updatedAt` — string

**`MessageSmsStatus`**

- string _(enum: `sent`, `delivered`, `trying`, `error`)_

**`MessageTemplateConfig`**

- `whatsapp` — TemplateWithParameters
  - `name` — string **(required)**
  - `parameters` — array
    - _array of_ `TemplateParameter`
      - `name` — string **(required)**
      - `value` — string **(required)**

**`MessageType`**

- string _(enum: `regular`, `system`, `deleted`)_

**`MessageWhatsAppStatus`**

- string _(enum: `trying`, `sent`, `delivered`, `error`)_

**`MessagingChannel`**

_A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number._

- string _(enum: `messenger`, `instagram`, `rcs`)_

**`PbxLicenseType`**

- string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_

**`QueryConversationsFilter`**

- `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
- `flags` — array
  - _array of_ `ConversationFlag`
- `status` — string _(enum: `COMPLETED`, `MISSED`)_
- `from` — string _(format=date-time)_
- `to` — string _(format=date-time)_
- `tags` — array
  - _array of_ `string`
- `search` — string _(maxLen=64)_
- `hasAttachment` — boolean

**`QueryConversationsRequestContent`**

- `limit` — number — The maximum number of rows to return. _(default=50; min=1; max=100)_
- `offset` — number — The offset from which to start. _(default=0; min=0)_
- `filter` — QueryConversationsFilter
  - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
  - `flags` — array
    - _array of_ `ConversationFlag`
  - `status` — string _(enum: `COMPLETED`, `MISSED`)_
  - `from` — string _(format=date-time)_
  - `to` — string _(format=date-time)_
  - `tags` — array
    - _array of_ `string`
  - `search` — string _(maxLen=64)_
  - `hasAttachment` — boolean

**`QueryConversationsResponseContent`**

- `conversations` — array **(required)**
  - _array of_ `Conversation`
    - _oneOf_ — exactly one of:
      - **`call`**
        - `call` — CallRecord **(required)**
          - _(nesting depth limit — see `CallRecord` in the Schemas appendix)_
      - **`conference`**
        - `conference` — ConferenceRecord **(required)**
          - _(nesting depth limit — see `ConferenceRecord` in the Schemas appendix)_

**`QueryUserCallsFilter`**

- `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
- `flags` — array
  - _array of_ `ConversationFlag`
- `status` — string _(enum: `COMPLETED`, `MISSED`)_
- `from` — string _(format=date-time)_
- `to` — string _(format=date-time)_
- `tags` — array
  - _array of_ `string`
- `search` — string _(maxLen=64)_
- `hasAttachment` — boolean
- `userDirection` — string _(enum: `INCOMING`, `OUTGOING`)_

**`QueryUserCallsRequestContent`**

- `limit` — number — The maximum number of rows to return. _(default=50; min=1; max=100)_
- `offset` — number — The offset from which to start. _(default=0; min=0)_
- `filter` — QueryUserCallsFilter
  - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`)_
  - `flags` — array
    - _array of_ `ConversationFlag`
  - `status` — string _(enum: `COMPLETED`, `MISSED`)_
  - `from` — string _(format=date-time)_
  - `to` — string _(format=date-time)_
  - `tags` — array
    - _array of_ `string`
  - `search` — string _(maxLen=64)_
  - `hasAttachment` — boolean
  - `userDirection` — string _(enum: `INCOMING`, `OUTGOING`)_

**`QueryUserCallsResponseContent`**

- `calls` — array **(required)**
  - _array of_ `CallRecord`
    - `flowIndex` — number **(required)**
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
    - `connectTime` — number — Duration when the called party's phone rang (Ring Time in UI)
    - `talkTime` — number — Duration of conversation from the moment the call is answered until it ends, excluding hold time
    - `waitTime` — number — Duration spent on IVR, dialplan applications, playback, etc. before the call is answered
    - `queueTime` — number — Duration of call waiting in queue
    - `holdTime` — number — Duration the call was on hold after being answered
    - `duration` — number **(required)** — Total duration = connectTime + waitTime + queueTime + talkTime + holdTime
    - `caller` — CallParticipant
      - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
      - `phone` — string
      - `name` — string
      - `company` — string _(minLen=3; maxLen=30)_
      - `email` — string
      - `userId` — string
      - `userExtension` — string
      - `userDepartment` — string
      - `groupId` — string
      - `groupName` — string
      - `userAgent` — string
      - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
      - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
      - `license` — string
      - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
      - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
      - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
      - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
    - `callee` — CallParticipant
      - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
      - `phone` — string
      - `name` — string
      - `company` — string _(minLen=3; maxLen=30)_
      - `email` — string
      - `userId` — string
      - `userExtension` — string
      - `userDepartment` — string
      - `groupId` — string
      - `groupName` — string
      - `userAgent` — string
      - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
      - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
      - `license` — string
      - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
      - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
      - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
      - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
    - `service` — string
    - `serviceNumber` — string
    - `destination` — string
    - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
    - `trunkName` — string
    - `trunkDirection` — string
    - `queueName` — string
    - `queueId` — string
    - `queuePosition` — number — Position of the call in the queue (1-based). Updated from consume events and emitted on live progress and record flows.
    - `tags` — array
      - _array of_ `string`
    - `flags` — array
      - _array of_ `string`
    - `callerMos` — string
    - `calleeMos` — string
    - `xhoppersConfId` — string
    - `recordings` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
      - _array of_ `string`
    - `recordingsData` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
      - _array of_ `CallFlowRecording`
        - _(nesting depth limit — see `CallFlowRecording` in the Schemas appendix)_
    - `mergeWith` — string
    - `splitReason` — string
    - `splitTransferType` — string
    - `remotePhone` — string
    - `remotePhoneCountryCode` — number
    - `remotePhoneCountryCodeStr` — string
    - `remotePhoneLocation` — string
    - `callStatus` — string _(enum: `COMPLETED`, `MISSED`)_
    - `transcriptionStatus` — string _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
    - `transcriptionLanguage` — string
    - `transcriptionSeconds` — number
    - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
    - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
      - _map of_ `Annotation`
        - _(nesting depth limit — see `Annotation` in the Schemas appendix)_
    - `attachment` — string — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
    - `attachmentType` — string _(enum: `VOICEMAIL`, `FAX`)_
    - `attachmentDestinations` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
      - _array of_ `CallFlowAttachmentDestination`
        - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `CallFlowAttachment`
        - _(nesting depth limit — see `CallFlowAttachment` in the Schemas appendix)_
    - `notifications` — CallFlowNotifications
      - `destinations` — array
        - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
      - `type` — array
        - _array of_ `string`
    - `id` — string **(required)**
    - `pbx` — string **(required)**
    - `time` — number **(required)**
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `licenses` — array **(required)**
      - _array of_ `License`
    - `type` — object **(required)**

**`Reaction`**

- `type` — string
- `userId` — string _(minLen=12; maxLen=12)_
- `messageId` — string
- `user` — User
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `name` — string
  - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string
  - `picture` — string
  - `locale` — string
  - `timeZone` — string
  - `company` — string
  - `bot` — boolean
  - `pbxDomain` — string
  - `pbxPort` — string
  - `pbxExtension` — string
  - `pbxSerial` — string
  - `pbxUserId` — string
  - `pbxGroupId` — string
  - `createdAt` — string
  - `updatedAt` — string

**`ReactionCounts`**

- _map of_ `number`

**`RecordType`**

- string _(enum: `call`, `call_transcription`, `call_annotations`, `conference`, `conference_transcription`, `conference_annotations`, `chat`, `chat_transcription`, `chat_annotations`)_

**`TemplateParameter`**

- `name` — string **(required)**
- `value` — string **(required)**

**`TemplateWithParameters`**

- `name` — string **(required)**
- `parameters` — array
  - _array of_ `TemplateParameter`
    - `name` — string **(required)**
    - `value` — string **(required)**

**`TranscriptionSentiment`**

_Sentiment label for a transcription chunk. Shared between calls and conferences._

- string _(enum: `POSITIVE`, `NEGATIVE`, `MIXED`, `NEUTRAL`)_

**`TranscriptionTextChunk`**

- `id` — string **(required)**
- `name` — string **(required)**
- `text` — string **(required)**
- `time` — string **(required)**
- `offset` — number **(required)**

**`UpdateCallRequestContent`**

- `tags` — array
  - _array of_ `string`

**`UpdateCallResponseContent`**

- `call` — CallRecord **(required)**
  - `flowIndex` — number **(required)**
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**
  - `connectTime` — number — Duration when the called party's phone rang (Ring Time in UI)
  - `talkTime` — number — Duration of conversation from the moment the call is answered until it ends, excluding hold time
  - `waitTime` — number — Duration spent on IVR, dialplan applications, playback, etc. before the call is answered
  - `queueTime` — number — Duration of call waiting in queue
  - `holdTime` — number — Duration the call was on hold after being answered
  - `duration` — number **(required)** — Total duration = connectTime + waitTime + queueTime + talkTime + holdTime
  - `caller` — CallParticipant
    - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
    - `phone` — string
    - `name` — string
    - `company` — string _(minLen=3; maxLen=30)_
    - `email` — string
    - `userId` — string
    - `userExtension` — string
    - `userDepartment` — string
    - `groupId` — string
    - `groupName` — string
    - `userAgent` — string
    - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
    - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
    - `license` — string
    - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
    - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
    - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
    - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
  - `callee` — CallParticipant
    - `type` — string **(required)** _(enum: `REMOTE`, `LOCAL`)_
    - `phone` — string
    - `name` — string
    - `company` — string _(minLen=3; maxLen=30)_
    - `email` — string
    - `userId` — string
    - `userExtension` — string
    - `userDepartment` — string
    - `groupId` — string
    - `groupName` — string
    - `userAgent` — string
    - `userDevice` — string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_
    - `role` — string **(required)** _(enum: `CLIENT`, `AGENT`)_
    - `license` — string
    - `sipCallId` — string — A unique identifier for the SIP call session used to control the call e.g., answer, hold, transfer, hang up.
    - `publicAddress` — string — Represents a network endpoint consisting of a public IP address and a port number. Example: '123.45.67.89:59317'
    - `privateAddress` — string — Represents a network endpoint consisting of a private IP address and a port number. Example: '172.16.1.2:54003'
    - `location` — string — The location specifies a geographic point using latitude and longitude coordinates. Example 'lat=29.3008&lon=1.7002'
  - `service` — string
  - `serviceNumber` — string
  - `destination` — string
  - `direction` — string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
  - `trunkName` — string
  - `trunkDirection` — string
  - `queueName` — string
  - `queueId` — string
  - `queuePosition` — number — Position of the call in the queue (1-based). Updated from consume events and emitted on live progress and record flows.
  - `tags` — array
    - _array of_ `string`
  - `flags` — array
    - _array of_ `string`
  - `callerMos` — string
  - `calleeMos` — string
  - `xhoppersConfId` — string
  - `recordings` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
    - _array of_ `string`
  - `recordingsData` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
    - _array of_ `CallFlowRecording`
      - `fileName` — string **(required)**
      - `start` — number **(required)**
      - `end` — number **(required)**
      - `owner` — string **(required)** _(enum: `callee`, `caller`, `system`)_
      - `url` — string **(required)**
      - `pauses` — array **(required)**
        - _(nesting depth limit — see `CallRecordPause` in the Schemas appendix)_
  - `mergeWith` — string
  - `splitReason` — string
  - `splitTransferType` — string
  - `remotePhone` — string
  - `remotePhoneCountryCode` — number
  - `remotePhoneCountryCodeStr` — string
  - `remotePhoneLocation` — string
  - `callStatus` — string _(enum: `COMPLETED`, `MISSED`)_
  - `transcriptionStatus` — string _(enum: `AVAILABLE`, `POST_TRANSCRIPTION`, `UNAVAILABLE`)_
  - `transcriptionLanguage` — string
  - `transcriptionSeconds` — number
  - `annotationsStatus` — string _(enum: `AVAILABLE`, `UNAVAILABLE`)_
  - `annotationsByKey` — AnnotationsMap — The newest annotation per `AnnotationKey`: the current value of everything the conversation tracks, without reading the history. Keyed annotations only — a one-off annotation appears solely in `annotations`.
    - _map of_ `Annotation`
      - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
      - `time` — number **(required)**
      - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
      - `payload` — union **(required)**
        - _(nesting depth limit — see `AnnotationPayload` in the Schemas appendix)_
      - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
        - _(nesting depth limit — see `AnnotationSource` in the Schemas appendix)_
  - `attachment` — string — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
  - `attachmentType` — string _(enum: `VOICEMAIL`, `FAX`)_
  - `attachmentDestinations` — array — Consider to use `attachments` instead. This shape is deprecated. _(deprecated)_
    - _array of_ `CallFlowAttachmentDestination`
      - `phone` — string
      - `name` — string
      - `email` — string
      - `userId` — string
      - `userExtension` — string
      - `userDepartment` — string
      - `groupId` — string
      - `groupName` — string
  - `attachments` — array
    - _array of_ `CallFlowAttachment`
      - _oneOf_ — exactly one of:
        - **`recording`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`fax`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`voicemail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `notifications` — CallFlowNotifications
    - `destinations` — array
      - _array of_ `CallFlowAttachmentDestination`
        - _(nesting depth limit — see `CallFlowAttachmentDestination` in the Schemas appendix)_
    - `type` — array
      - _array of_ `string`
  - `id` — string **(required)**
  - `pbx` — string **(required)**
  - `time` — number **(required)**
  - `company` — string **(required)** _(minLen=3; maxLen=30)_
  - `licenses` — array **(required)**
    - _array of_ `License`
  - `type` — object **(required)**

**`User`**

- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `name` — string
- `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `phone` — string
- `picture` — string
- `locale` — string
- `timeZone` — string
- `company` — string
- `bot` — boolean
- `pbxDomain` — string
- `pbxPort` — string
- `pbxExtension` — string
- `pbxSerial` — string
- `pbxUserId` — string
- `pbxGroupId` — string
- `createdAt` — string
- `updatedAt` — string

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`WilmaChatArtifact`**

_An artifact the turn shared. The files stay in the artifacts store; `artifactId` opens it._

- `artifactId` — string **(required)** _(minLen=1; maxLen=64)_
- `title` — string **(required)** _(minLen=1; maxLen=256)_
- `kind` — string **(required)** _(minLen=1; maxLen=32)_
- `size` — number **(required)** _(min=0)_
- `name` — string _(minLen=1; maxLen=256)_

**`WilmaChatElement`**

_On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex)._

- `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
- `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
- `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
- `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
- `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
- `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
  - `outcome` — string **(required)** — How the turn ended. _(enum: `done`, `stopped`, `failed`)_
  - `durationMs` — number — From the turn's start to its end. Absent when the turn had not ended.
  - `toolCount` — number **(required)** — Steps the turn took, counted as the Wilma assistant counts its work steps: each tool call and each sandbox step (`SandboxStartedEvent`, `SandboxFailedEvent`).
  - `failedCount` — number **(required)** — Steps that failed: calls that failed, including those the stop or failure cut off, and sandbox steps that failed.
- `artifacts` — array
  - _array of_ `WilmaChatArtifact`
    - `artifactId` — string **(required)** _(minLen=1; maxLen=64)_
    - `title` — string **(required)** _(minLen=1; maxLen=256)_
    - `kind` — string **(required)** _(minLen=1; maxLen=32)_
    - `size` — number **(required)** _(min=0)_
    - `name` — string _(minLen=1; maxLen=256)_

**`WilmaChatTurnOutcome`**

_How the turn ended._

- string _(enum: `done`, `stopped`, `failed`)_

**`WilmaChatTurnSummary`**

_How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log._

- `outcome` — string **(required)** — How the turn ended. _(enum: `done`, `stopped`, `failed`)_
- `durationMs` — number — From the turn's start to its end. Absent when the turn had not ended.
- `toolCount` — number **(required)** — Steps the turn took, counted as the Wilma assistant counts its work steps: each tool call and each sandbox step (`SandboxStartedEvent`, `SandboxFailedEvent`).
- `failedCount` — number **(required)** — Steps that failed: calls that failed, including those the stop or failure cut off, and sandbox steps that failed.

</details>
