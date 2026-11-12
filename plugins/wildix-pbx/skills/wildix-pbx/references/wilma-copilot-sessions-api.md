## Wilma Copilot Sessions API 🆕

_OpenAPI: Wilma Copilot Sessions Service — version v2_

**Servers**

- `https://api.wilma.wildix.com` — Production
- `https://api-stable.wilma.wildix.com` — Stable
- `https://api-stage.wilma.wildix.com` — Stage

### Context

#### `POST` `/v2/copilot/enrich`

Attaches late-arriving lookup evidence to a relationship — e.g. a CRM match the iframe
    resolved after Open, or a human wrong-match correction. `relationshipId` is the
    client's current belief, not an instruction: evidence runs through the same resolution rules,
    and when it proves the customer is someone else (e.g. a human-confirmed entity bound
    elsewhere), the response returns the authoritative relationship — which may differ from the
    input. Fresh values refresh `contact.*` / `crm.*` state in the relationship's active sessions
    and re-evaluate conditions, so assets can appear mid-call the moment a match lands.

- operationId: `Enrich`
- **Scopes**: `wilma-copilot-sessions:Enrich`, `wilma-copilot-sessions:write`
- **Request body** (`application/json` — `EnrichRequestContent`) **(required)**
  - `company` — string — Company that owns the relationship. Required when calling with a service (s2s) token. _(minLen=3; maxLen=30)_
  - `relationshipId` — string **(required)** — Id of a relationship: the durable, cross-channel view of one customer that copilot sessions attach to. Identities (emails, phones, entities) merge into it as context is ingested. _(minLen=1; maxLen=128)_
  - `lookup` — CopilotContextLookup **(required)** — The result of a client-side contact lookup: the identities and enrichment in scope for the customer. Reused by Open (optional — an already-bound channel or an anonymous call needs none) and Enrich (late-arriving evidence, e.g. a CRM match resolved after open).
    - `emails` — array — Customer email addresses. Identity, first-class: merged into the relationship.
      - _array of_ `string`
    - `phones` — array — Customer phone numbers. Identity, first-class: merged into the relationship.
      - _array of_ `string`
    - `entities` — array — Typed references to records in external systems, e.g. a Salesforce contact. Identity, first-class: merged into the relationship.
      - _array of_ `CopilotContextEntity`
        - `id` — string **(required)**
        - `type` — string **(required)**
    - `attributes` — CopilotContextAttributes — Open string-to-string enrichment carried by a context event, e.g. `phonebook.name`, `call.direction`, `salesforce.deal_stage`, `match.confidence`. Keys are dot-namespaced by source. Values feed the session state that profile conditions evaluate. Identities do not belong here — emails, phones and entity references are first-class envelope fields.
      - _map of_ `string`
- **Response 200** (`EnrichResponseContent`)
  - `relationshipId` — string **(required)** — The authoritative relationship after applying the evidence. May differ from the input when strong evidence re-resolves the customer. _(minLen=1; maxLen=128)_
  - `related` — array **(required)** — Sessions associated with the authoritative relationship, most recent first.
    - _array of_ `CopilotSessionSummary`
      - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
      - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
        - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
        - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
      - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.
- Errors: `400`, `403`, `404`

#### `POST` `/v2/copilot/lookup`

Resolves a lookup to a relationship and its sessions without opening copilot or creating
    anything — a read-only peek. Use it to decide whether a customer has history before opening,
    e.g. to badge the Wilma button. Returns no relationship when nothing matches; relationships
    are only created by Open.

- operationId: `Resolve`
- **Scopes**: `wilma-copilot-sessions:Resolve`, `wilma-copilot-sessions:read`
- **Request body** (`application/json` — `ResolveRequestContent`) **(required)**
  - `company` — string — Company scope. Required when calling with a service (s2s) token. _(minLen=3; maxLen=30)_
  - `lookup` — CopilotContextLookup **(required)** — The result of a client-side contact lookup: the identities and enrichment in scope for the customer. Reused by Open (optional — an already-bound channel or an anonymous call needs none) and Enrich (late-arriving evidence, e.g. a CRM match resolved after open).
    - `emails` — array — Customer email addresses. Identity, first-class: merged into the relationship.
      - _array of_ `string`
    - `phones` — array — Customer phone numbers. Identity, first-class: merged into the relationship.
      - _array of_ `string`
    - `entities` — array — Typed references to records in external systems, e.g. a Salesforce contact. Identity, first-class: merged into the relationship.
      - _array of_ `CopilotContextEntity`
        - `id` — string **(required)**
        - `type` — string **(required)**
    - `attributes` — CopilotContextAttributes — Open string-to-string enrichment carried by a context event, e.g. `phonebook.name`, `call.direction`, `salesforce.deal_stage`, `match.confidence`. Keys are dot-namespaced by source. Values feed the session state that profile conditions evaluate. Identities do not belong here — emails, phones and entity references are first-class envelope fields.
      - _map of_ `string`
- **Response 200** (`ResolveResponseContent`)
  - `relationshipId` — string — The relationship the lookup resolved to, when one matched. Lookup never creates relationships. _(minLen=1; maxLen=128)_
  - `sessions` — array **(required)** — Sessions associated with the matched relationship, most recent first. Empty when nothing matched.
    - _array of_ `CopilotSessionSummary`
      - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
      - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
        - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
        - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
      - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.
- Errors: `400`, `403`

#### `POST` `/v2/copilot/open`

Opens copilot for a client surface. `lookup` (when present) is treated as hints: emails,
    phones and entity references are resolved authoritatively server-side and merged into a
    relationship. Routing picks the session — clients never pass conversation ids: the
    relationship's live conversation session (created automatically when a call or chat starts)
    when one exists, otherwise the relationship's `app` session (server-minted, reused while
    idle). The response returns the sessions already associated with the relationship, so the client
    can render cross-channel history without a second call.

- operationId: `Open`
- **Scopes**: `wilma-copilot-sessions:Open`, `wilma-copilot-sessions:write`
- **Request body** (`application/json` — `OpenRequestContent`)
  - `company` — string — Company that owns the relationship. Required when calling with a service (s2s) token, which is not scoped to a single company. _(minLen=3; maxLen=30)_
  - `lookup` — CopilotContextLookup — The result of a client-side contact lookup: the identities and enrichment in scope for the customer. Reused by Open (optional — an already-bound channel or an anonymous call needs none) and Enrich (late-arriving evidence, e.g. a CRM match resolved after open).
    - `emails` — array — Customer email addresses. Identity, first-class: merged into the relationship.
      - _array of_ `string`
    - `phones` — array — Customer phone numbers. Identity, first-class: merged into the relationship.
      - _array of_ `string`
    - `entities` — array — Typed references to records in external systems, e.g. a Salesforce contact. Identity, first-class: merged into the relationship.
      - _array of_ `CopilotContextEntity`
        - `id` — string **(required)**
        - `type` — string **(required)**
    - `attributes` — CopilotContextAttributes — Open string-to-string enrichment carried by a context event, e.g. `phonebook.name`, `call.direction`, `salesforce.deal_stage`, `match.confidence`. Keys are dot-namespaced by source. Values feed the session state that profile conditions evaluate. Identities do not belong here — emails, phones and entity references are first-class envelope fields.
      - _map of_ `string`
- **Response 200** (`OpenResponseContent`)
  - `relationshipId` — string **(required)** — Id of a relationship: the durable, cross-channel view of one customer that copilot sessions attach to. Identities (emails, phones, entities) merge into it as context is ingested. _(minLen=1; maxLen=128)_
  - `session` — CopilotIngestedSession **(required)** — The session an ingested context event was routed to.
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `state` — string **(required)** — How an ingested event was attached to a session. _(enum: `created`, `reused`)_
  - `related` — array **(required)** — Sessions already associated with the relationship, most recent first. Excludes the session the open was routed to.
    - _array of_ `CopilotSessionSummary`
      - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
      - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
        - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
        - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
      - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.
- Errors: `400`, `403`

#### `GET` `/v2/copilot/relationships/{relationshipId}/sessions`

Lists the copilot sessions associated with a relationship, most recent first — the paginated
    form of the `related` / `sessions` lists Open, Enrich and Resolve return inline. Use it to page
    a customer's cross-channel history, and to refresh after a `relationship` stream event announces
    a new session. Sessions are company-owned and shared within the tenant; an unknown relationship
    in scope returns an empty list rather than an error.

- operationId: `ListRelationshipSessions`
- **Scopes**: `wilma-copilot-sessions:ListRelationshipSessions`, `wilma-copilot-sessions:read`
- **Parameters**
  - `relationshipId` (path) — string **(required)** — The relationship whose sessions to list, as returned by Open, Enrich or Resolve. _(minLen=1; maxLen=128)_
  - `company` (query) — string — Company that owns the relationship. Required when calling with a service (s2s) token, which is not scoped to a single company. _(minLen=3; maxLen=30)_
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListRelationshipSessionsResponseContent`)
  - `sessions` — array **(required)**
    - _array of_ `CopilotSessionSummary`
      - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
      - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
        - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
        - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
      - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.
  - `nextCursor` — string — Present when more sessions exist; pass it as `cursor` of the next call. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

### Sessions

#### `GET` `/v2/copilot/sessions`

Lists copilot sessions a user participated in, most recent first. Lets a user find a session they opened earlier without knowing the relationship.

- operationId: `ListSessions`
- **Scopes**: `wilma-copilot-sessions:ListSessions`, `wilma-copilot-sessions:read`
- **Parameters**
  - `company` (query) — string — Company scope. Required when calling with a service (s2s) token. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user whose participated sessions to list. Defaults to the caller; required when calling with a service (s2s) token. _(minLen=12; maxLen=12)_
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListSessionsResponseContent`)
  - `sessions` — array **(required)**
    - _array of_ `CopilotSessionSummary`
      - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
      - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
        - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
        - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
      - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.
  - `nextCursor` — string — Present when more sessions exist; pass it as `cursor` of the next call. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

#### `POST` `/v2/copilot/sessions/{sessionId}/actions`

Submits one user interaction with copilot output — a knowledge-search suggestion click, a
    smart-action invocation, or playbook progress the agent made by hand. The action is appended to
    the session's input mailbox and processed asynchronously by the session worker; outcomes surface
    in the event log as `action` events and asset updates. Clicks also feed the per-resource usage
    statistics in the wilma-copilot config API.

- operationId: `Act`
- **Scopes**: `wilma-copilot-sessions:Act`, `wilma-copilot-sessions:write`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — Company that owns the session. Required when calling with a service (s2s) token, which is not scoped to a single company. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `ActRequestContent`) **(required)**
  - `action` — union **(required)** — One user interaction with copilot output. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`knowledgeSearch`**
        - `knowledgeSearch` — KnowledgeSearchClientAction **(required)** — Launches the knowledge search suggested for a detected question (contextual knowledge answers, `suggest_action` mode).
          - `questionId` — string **(required)** — The suggested question's id — the `questionId` carried by the suggestion asset's action payload.
          - `question` — string — The question text; used when the suggestion is no longer part of the live session state (e.g. after a revive).
      - **`smartAction`**
        - `smartAction` — SmartActionClientAction **(required)** — Invokes one smart action offered by an asset.
          - `assetId` — string **(required)** — Id of the asset carrying the smart action.
          - `actionId` — string **(required)** — Id of the clicked action inside the asset's smart-action list.
          - `variables` — any — Values for `guided` variable bindings collected from the user, keyed by variable name.
      - **`playbook`**
        - `playbook` — PlaybookClientAction **(required)** — Records playbook progress the agent made by hand: the steps that do not auto-complete from the transcript, and — where the playbook allows it — the playbook itself. Progress is append-only, so a step the transcript already completed stays complete and re-sending an id is a no-op.
          - `assetId` — string **(required)** — Id of the asset carrying the playbook.
          - `stepIds` — array — Steps the agent ticked. Ids that are not steps of this playbook are ignored.
            - _array of_ `string`
          - `complete` — boolean — Marks the whole playbook complete. Honoured only when the playbook's `completionCriteria` is `manual` with `allowAgentMarkComplete`; ignored for semantic criteria, where the model owns the goal verdict. Required steps still gate the checkmark either way.
- **Response 202** (`ActResponseContent`)
  - `accepted` — boolean **(required)** — True when the action was accepted into the session mailbox. Follow the event log for outcomes.
- Errors: `400`, `403`, `404`

#### `POST` `/v2/copilot/sessions/{sessionId}/ask`

Records an ask in a copilot session and publishes it as an `ask` event on the session
    stream. The ask itself runs as a regular Wilma session (wilma-assistant): `wilmaSessionId`
    points at it and `accessToken` is a read-only, session-scoped token other agents present to
    wilma-assistant to render the ask output — copilot sessions are shared within the tenant, so
    any agent watching the stream may view it.

- operationId: `Ask`
- **Scopes**: `wilma-copilot-sessions:Ask`, `wilma-copilot-sessions:write`
- **Parameters**
  - `sessionId` (path) — string **(required)** — The copilot session to record the ask in. _(minLen=1; maxLen=128)_
- **Request body** (`application/json` — `AskRequestContent`) **(required)**
  - `company` — string — Company that owns the session. Required when calling with a service (s2s) token. _(minLen=3; maxLen=30)_
  - `wilmaSessionId` — string **(required)** — The Wilma session (wilma-assistant) holding the ask and its output.
  - `accessToken` — string — Read-only, expiring token scoped to `wilmaSessionId`, issued by wilma-assistant. Published on the `ask` event so other agents can view the output.
- **Response 200** (`AskResponseContent`)
  - `index` — number **(required)** — Index of the recorded `ask` event in the session log.
- Errors: `400`, `403`, `404`

#### `GET` `/v2/copilot/sessions/{sessionId}/events`

Returns recorded copilot session events as a plain JSON page, without streaming. Use it to inspect past sessions or to catch up before subscribing to StreamSessionEvents.

- operationId: `GetSessionEvents`
- **Scopes**: `wilma-copilot-sessions:GetSessionEvents`, `wilma-copilot-sessions:read`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — Company that owns the session. Required when calling with a service (s2s) token, which is not scoped to a single company. _(minLen=3; maxLen=30)_
  - `startIndex` (query) — number — Return events with `index >= startIndex`. Defaults to 0. _(min=0)_
  - `limit` (query) — number — Maximum number of events to return. Defaults to 1000. _(min=1; max=1000)_
- **Response 200** (`GetSessionEventsResponseContent`)
  - `events` — array **(required)**
    - _array of_ `CopilotSessionEvent`
      - _oneOf_ — exactly one of:
        - **`lifecycle`**
          - `lifecycle` — CopilotLifecycleEvent **(required)** — Session lifecycle transition. Emitted on attach and on every status transition; `reason` says why the session moved. This is where a client learns the trace recording the session, delivered on attach.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
            - `traceId` — string — Opaque trace identifier generated by the tracing runtime. _(minLen=1; maxLen=128)_
            - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
            - `reason` — string — Why a lifecycle transition happened. _(enum: `created`, `ended`, `stopped`, `inactivity`, `archive_timer`, `revived`, `error`)_
        - **`transcript`**
          - `transcript` — CopilotTranscriptionEvent **(required)** — A live transcription segment from the assisted conversation. Carries the original WDA analytics event without simplification.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `data` — union **(required)** — Original WDA live transcription event for the assisted conversation surface.
              - _oneOf_ — exactly one of:
                - **`call`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`chat`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`conference`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`intent`**
          - `intent` — CopilotIntentEvent **(required)** — An intent detected or updated in the session. Carries the full intent state at this point; re-emitted on updates.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `id` — string **(required)**
            - `state` — any **(required)**
        - **`evaluation`**
          - `evaluation` — CopilotEvaluationEvent **(required)** — An evaluation result detected or updated in the session. Carries the full evaluation state at this point; re-emitted on updates.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `id` — string **(required)**
            - `state` — any **(required)**
        - **`asset`**
          - `asset` — CopilotAssetEvent **(required)** — An asset shown or updated in the session. Carries the full asset state at this point; re-emitted on updates (e.g. playbook progress).
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `id` — string **(required)**
            - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
            - `styling` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
            - `sticky` — boolean
            - `content` — string
            - `state` — any **(required)**
        - **`assistant`**
          - `assistant` — CopilotAssistantEvent **(required)** — An assistant chat shown or updated in the session.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `id` — string **(required)**
            - `state` — any **(required)**
        - **`relationship`**
          - `relationship` — CopilotRelationshipEvent **(required)** — A relationship update visible to an active session — e.g. another session was created or revived on the same relationship.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `relationshipId` — string **(required)** — Id of a relationship: the durable, cross-channel view of one customer that copilot sessions attach to. Identities (emails, phones, entities) merge into it as context is ingested. _(minLen=1; maxLen=128)_
            - `sessionId` — string — The other session attached to the same relationship, when the update is about one. _(minLen=1; maxLen=128)_
        - **`ask`**
          - `ask` — CopilotAskEvent **(required)** — An ask recorded in the session. The ask itself runs as a regular Wilma session (wilma-assistant); any agent in the company can render its output by presenting `accessToken` to wilma-assistant — copilot sessions are shared within the tenant.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `userId` — string **(required)** — The user who asked. _(minLen=12; maxLen=12)_
            - `wilmaSessionId` — string **(required)** — The Wilma session (wilma-assistant) holding the ask and its output.
            - `accessToken` — string — Read-only, session-scoped, expiring token other agents present to wilma-assistant to view the ask output.
        - **`action`**
          - `action` — CopilotActionEvent **(required)** — A client action recorded in the session with its execution outcome. Emitted when the action is accepted (`launched`) and re-emitted when its execution settles (`completed` / `failed`).
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `id` — string **(required)** — Id of the asset the action belongs to.
            - `kind` — string **(required)** — What was invoked: `knowledge_search`, `playbook`, `runAgent`, `transfer`, `handover` or `openUrl`.
            - `status` — string **(required)** _(enum: `launched`, `completed`, `failed`)_
            - `userId` — string — The user who triggered the action. _(minLen=12; maxLen=12)_
            - `result` — any — Execution result payload, for smart actions with `show_card` result mode.
            - `error` — string — Failure description when status is `failed`.
  - `nextStartIndex` — number — Present when more events exist; pass it as `startIndex` of the next call.
- Errors: `400`, `403`, `404`

#### `GET` `/v2/copilot/sessions/{sessionId}/events/stream`

Replays and tails copilot session events as Server-Sent Events (`text/event-stream`). Each frame carries one CopilotSessionEvent: `id:` is the event index, `event:` is the union member name, and `data:` is the JSON document of the union value. The stream closes after a `lifecycle` event that leaves the session dormant (`idle`, `archived`) or `failed`; reconnect with the last seen index + 1 as `startIndex` to resume, including after a dormant session revives. `startIndex` is the only resume cursor — no `Last-Event-ID` header is read, because a client already tracks the index it is rendering, and that is the same cursor GetSessionEvents pages with.

- operationId: `StreamSessionEvents`
- **Scopes**: `wilma-copilot-sessions:StreamSessionEvents`, `wilma-copilot-sessions:read`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — Company that owns the session. Required when calling with a service (s2s) token, which is not scoped to a single company. _(minLen=3; maxLen=30)_
  - `startIndex` (query) — number — Replay recorded events with `index >= startIndex` before tailing live ones. Defaults to 0. _(min=0)_
- **Response 200** (`StreamSessionEventsOutputPayload`)
  - string
- Errors: `400`, `403`, `404`

#### `GET` `/v2/copilot/sessions/{sessionId}/state`

Returns the whole state of a copilot session: the conversation and its participants, the full transcript, and every intent, evaluation, asset, action and ask so far, each named. Reflects the events applied so far and never waits for pending ones.

- operationId: `GetSessionState`
- **Scopes**: `wilma-copilot-sessions:GetSessionState`, `wilma-copilot-sessions:read`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — Company that owns the session. Required when calling with a service (s2s) token, which is not scoped to a single company. _(minLen=3; maxLen=30)_
- **Response 200** (`GetSessionStateResponseContent`)
  - `session` — CopilotSessionSummary **(required)** — A compact view of a copilot session associated with a relationship. Sessions are owned by the company and shared within the tenant.
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
    - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
      - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
      - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.
  - `state` — CopilotSessionState **(required)** — What copilot knows about a session's conversation.
    - `conversation` — CopilotConversationState — What WDA reported about the conversation itself. A fact the source has not reported is absent.
      - `callId` — string — WDA call id, for a call.
      - `callFlows` — array — The call's flows, oldest first, when it has more than one: each transfer adds one.
        - _array of_ `CopilotCallFlowState`
          - `flowIndex` — number **(required)**
          - `caller` — string — Id of the calling participant, from `participants`.
          - `callee` — string — Id of the called participant, from `participants`.
          - `direction` — string
          - `status` — string
          - `queue` — string
          - `startTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
          - `endTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
          - `duration` — number — How long the flow lasted, in seconds.
      - `channelId` — string — Chat channel id, for a chat.
      - `chatId` — string — WDA chat id, one chat session within `channelId`, for a chat.
      - `conferenceId` — string — WDA conference id, for a conference.
      - `direction` — string — Direction as WDA reports it, e.g. `INBOUND`, `OUTBOUND`.
      - `status` — string — Status as WDA reports it, e.g. `TALKING`, `ANSWERED`, `MISSED`; `ENDED` for a conversation that ended before WDA sent a final record of it.
      - `flags` — array
        - _array of_ `string`
      - `service` — string
      - `queue` — string
      - `language` — string — Transcription language.
      - `tags` — array
        - _array of_ `string`
      - `startTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `endTime` — string — When the conversation ended; absent while it is in progress.
      - `duration` — number — How long the conversation lasted, in seconds; so far, while it is in progress.
      - `talkTime` — number — Time spent talking, in seconds.
      - `waitTime` — number — Time spent waiting to be answered, in seconds.
      - `holdTime` — number — Time spent on hold, in seconds.
    - `participants` — array **(required)** — Everyone who took part, each once, across every flow of a call.
      - _array of_ `CopilotParticipantState`
        - `id` — string **(required)** — Unique and stable within the session: a person keeps one id across every flow of a transferred call. Transcript lines and call flows refer to participants by it.
        - `name` — string
        - `role` — string — Side of the conversation, e.g. `agent` or `customer`, when known.
        - `company` — string — Company the party belongs to, as the source names it.
        - `department` — string
        - `group` — string — PBX group of a colleague.
        - `extension` — string — PBX extension of a colleague.
        - `phone` — string — Phone number the party was reached on.
        - `country` — string — Country of the party's phone number, ISO 3166-1 alpha-2.
        - `email` — string
    - `transcript` — array **(required)** — The whole transcript, oldest first.
      - _array of_ `CopilotTranscriptState`
        - `id` — string **(required)**
        - `flowIndex` — number — For a call, the flow (`conversation.callFlows[].flowIndex`) the line was said on.
        - `speaker` — string — Id of the participant who spoke, from `participants`: on a call or conference the participant whose audio it was, in a chat the message's author. Absent when the source does not say.
        - `role` — string — Side of the conversation the speaker is on, e.g. `agent` or `customer`, when known.
        - `text` — string **(required)**
        - `time` — string — When the line was said. On a call or conference, when the speaker started speaking; in a chat, when the message was sent.
        - `endTime` — string — When the speaker stopped speaking. Calls and conferences only.
        - `offset` — number — Time from the conversation's start (`conversation.startTime`) to `time`, in milliseconds, so lines lay out on one timeline.
    - `lookup` — CopilotContextLookup — The result of a client-side contact lookup: the identities and enrichment in scope for the customer. Reused by Open (optional — an already-bound channel or an anonymous call needs none) and Enrich (late-arriving evidence, e.g. a CRM match resolved after open).
      - `emails` — array — Customer email addresses. Identity, first-class: merged into the relationship.
        - _array of_ `string`
      - `phones` — array — Customer phone numbers. Identity, first-class: merged into the relationship.
        - _array of_ `string`
      - `entities` — array — Typed references to records in external systems, e.g. a Salesforce contact. Identity, first-class: merged into the relationship.
        - _array of_ `CopilotContextEntity`
          - `id` — string **(required)**
          - `type` — string **(required)**
      - `attributes` — CopilotContextAttributes — Open string-to-string enrichment carried by a context event, e.g. `phonebook.name`, `call.direction`, `salesforce.deal_stage`, `match.confidence`. Keys are dot-namespaced by source. Values feed the session state that profile conditions evaluate. Identities do not belong here — emails, phones and entity references are first-class envelope fields.
        - _map of_ `string`
    - `intents` — array **(required)** — Intents detected so far.
      - _array of_ `CopilotIntentState`
        - `id` — string **(required)**
        - `name` — string **(required)** — The intent's name, as configured.
        - `option` — CopilotIntentOptionState — One option of an intent.
          - `id` — string **(required)**
          - `name` — string — The option's name, as configured.
        - `fields` — any — Values extracted for the intent's fields, by field name.
        - `detectedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `evaluations` — array **(required)** — Evaluation results so far, including the built-in signals `sentiment`, `csat`, `topics` and `talk_ratio`.
      - _array of_ `CopilotEvaluationState`
        - `id` — string **(required)**
        - `name` — string **(required)** — The evaluation's name, as configured; for a built-in signal, `sentiment`, `csat`, `topics` or `talk_ratio`.
        - `value` — any — The current result, shaped by the evaluation: a label, a score, a list.
        - `previous` — any — The result before the latest change.
        - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `assets` — array **(required)** — Assets shown so far, in the order they were first shown.
      - _array of_ `CopilotAssetState`
        - `id` — string **(required)**
        - `name` — string **(required)** — The asset's name, as configured; for an automation or a knowledge answer, the automation's name or the question.
        - `title` — string
        - `content` — string — The body shown: markdown, static or agent-generated.
        - `status` — string — Where the shown body stands, e.g. `pending`, `complete` or `error`; a knowledge answer is `suggested` then `answered`.
        - `state` — any **(required)** — Presentation data of the asset's kind, such as playbook progress, as its latest event carries it.
        - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
        - `styling` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
        - `sticky` — boolean
        - `shownAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
        - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `actions` — array **(required)** — Actions invoked so far, in the order they were invoked.
      - _array of_ `CopilotActionState`
        - `id` — string **(required)** — Id of the asset the action belongs to.
        - `actionId` — string — Id of the action within the asset.
        - `userId` — string — The user who triggered the action. _(minLen=12; maxLen=12)_
        - `kind` — string **(required)** — What was invoked: `knowledge_search`, `playbook`, `runAgent`, `transfer`, `handover` or `openUrl`.
        - `label` — string — The action's label, as the asset shows it.
        - `status` — string **(required)** _(enum: `launched`, `completed`, `failed`)_
        - `result` — any — Execution result payload, for smart actions with `show_card` result mode.
        - `error` — string — Failure description when status is `failed`.
        - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `asks` — array **(required)** — Asks recorded so far, oldest first.
      - _array of_ `CopilotAskState`
        - `userId` — string **(required)** — The user who asked. _(minLen=12; maxLen=12)_
        - `wilmaSessionId` — string **(required)** — The Wilma session (wilma-assistant) holding the ask and its output.
        - `askedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- Errors: `400`, `403`, `404`

#### `POST` `/v2/copilot/sessions/{sessionId}/views`

Reports which copilot assets the user actually saw rendered (impressions). Copilot may emit
    assets nobody sees — the panel can be closed — so emitted counts alone overstate reach. Views
    reported here feed the per-resource emitted / seen / clicked statistics administrators read
    from the wilma-copilot config API. Batch-friendly: report visible assets when they render,
    deduplicated per session by the server.

- operationId: `Track`
- **Scopes**: `wilma-copilot-sessions:Track`, `wilma-copilot-sessions:write`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — Company that owns the session. Required when calling with a service (s2s) token, which is not scoped to a single company. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `TrackRequestContent`) **(required)**
  - `views` — array **(required)**
    - _array of_ `CopilotAssetView`
      - `assetId` — string **(required)**
      - `at` — string — When the asset became visible. Defaults to the time the report is ingested.
- **Response 202** (`TrackResponseContent`)
  - `accepted` — boolean **(required)** — True when the views were recorded.
- Errors: `400`, `403`, `404`

### Schemas appendix — Wilma Copilot Sessions API

<details><summary>106 component schemas</summary>

**`ActRequestContent`**

- `action` — union **(required)** — One user interaction with copilot output. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`knowledgeSearch`**
      - `knowledgeSearch` — KnowledgeSearchClientAction **(required)** — Launches the knowledge search suggested for a detected question (contextual knowledge answers, `suggest_action` mode).
        - `questionId` — string **(required)** — The suggested question's id — the `questionId` carried by the suggestion asset's action payload.
        - `question` — string — The question text; used when the suggestion is no longer part of the live session state (e.g. after a revive).
    - **`smartAction`**
      - `smartAction` — SmartActionClientAction **(required)** — Invokes one smart action offered by an asset.
        - `assetId` — string **(required)** — Id of the asset carrying the smart action.
        - `actionId` — string **(required)** — Id of the clicked action inside the asset's smart-action list.
        - `variables` — any — Values for `guided` variable bindings collected from the user, keyed by variable name.
    - **`playbook`**
      - `playbook` — PlaybookClientAction **(required)** — Records playbook progress the agent made by hand: the steps that do not auto-complete from the transcript, and — where the playbook allows it — the playbook itself. Progress is append-only, so a step the transcript already completed stays complete and re-sending an id is a no-op.
        - `assetId` — string **(required)** — Id of the asset carrying the playbook.
        - `stepIds` — array — Steps the agent ticked. Ids that are not steps of this playbook are ignored.
          - _array of_ `string`
        - `complete` — boolean — Marks the whole playbook complete. Honoured only when the playbook's `completionCriteria` is `manual` with `allowAgentMarkComplete`; ignored for semantic criteria, where the model owns the goal verdict. Required steps still gate the checkmark either way.

**`ActResponseContent`**

- `accepted` — boolean **(required)** — True when the action was accepted into the session mailbox. Follow the event log for outcomes.

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

**`AskRequestContent`**

- `company` — string — Company that owns the session. Required when calling with a service (s2s) token. _(minLen=3; maxLen=30)_
- `wilmaSessionId` — string **(required)** — The Wilma session (wilma-assistant) holding the ask and its output.
- `accessToken` — string — Read-only, expiring token scoped to `wilmaSessionId`, issued by wilma-assistant. Published on the `ask` event so other agents can view the output.

**`AskResponseContent`**

- `index` — number **(required)** — Index of the recorded `ask` event in the session log.

**`AssetIcon`**

_Icon shown on the asset card._

- string _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_

**`AssetSeverity`**

_Visual emphasis of the asset card._

- string _(enum: `neutral`, `success`, `warning`, `danger`)_

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

**`CallAnalyticsLiveTranscriptionEvent`**

- `id` — string **(required)**
- `pbx` — string **(required)**
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `licenses` — array **(required)**
  - _array of_ `License`
- `event` — object **(required)**
- `flowIndex` — number **(required)**
- `flowStartTime` — number **(required)**
- `callStartTime` — number **(required)**
- `chunk` — CallTranscriptionChunk **(required)**
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
- `participant` — CallParticipant
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

**`CallDevice`**

- string _(enum: `COLLABORATION_WEB`, `COLLABORATION_IOS`, `COLLABORATION_ANDROID`, `XBEES_WEB`, `XBEES_IOS`, `XBEES_ANDROID`, `WILDIX_PHONE`, `WILDIX_DEVICE`, `VOICEBOT`, `UNKNOWN`, `COLLABORATION7_WEB`, `COLLABORATION7_IOS`, … (+5))_

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

**`CallTranscriptionSpeaker`**

- string _(enum: `callee`, `caller`)_

**`ChatAnalyticsLiveTranscriptionEvent`**

- `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
- `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `event` — object **(required)**
- `message` — Message **(required)**
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

**`ChatVerbosity`**

_How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text._

- string _(enum: `none`, `simple`, `full`)_

**`ConferenceAnalyticsLiveTranscriptionEvent`**

- `id` — string **(required)**
- `time` — number **(required)**
- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `event` — object **(required)**
- `conferenceStartTime` — number **(required)**
- `transcriptionStartTime` — number **(required)**
- `chunk` — ConferenceTranscriptionChunk **(required)**
  - `id` — string **(required)**
  - `time` — number **(required)**
  - `jid` — string **(required)**
  - `text` — string **(required)**
  - `language` — string
  - `isFinal` — boolean **(required)**
  - `start` — number **(required)**
  - `end` — number **(required)**
  - `sentiment` — string — Sentiment label for a transcription chunk. Shared between calls and conferences. _(enum: `POSITIVE`, `NEGATIVE`, `MIXED`, `NEUTRAL`)_
- `participant` — ConferenceParticipant
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

**`CopilotActionEvent`**

_A client action recorded in the session with its execution outcome. Emitted when the action is accepted (`launched`) and re-emitted when its execution settles (`completed` / `failed`)._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `id` — string **(required)** — Id of the asset the action belongs to.
- `kind` — string **(required)** — What was invoked: `knowledge_search`, `playbook`, `runAgent`, `transfer`, `handover` or `openUrl`.
- `status` — string **(required)** _(enum: `launched`, `completed`, `failed`)_
- `userId` — string — The user who triggered the action. _(minLen=12; maxLen=12)_
- `result` — any — Execution result payload, for smart actions with `show_card` result mode.
- `error` — string — Failure description when status is `failed`.

**`CopilotActionState`**

_A client action invoked in the session, as its latest action event left it._

- `id` — string **(required)** — Id of the asset the action belongs to.
- `actionId` — string — Id of the action within the asset.
- `userId` — string — The user who triggered the action. _(minLen=12; maxLen=12)_
- `kind` — string **(required)** — What was invoked: `knowledge_search`, `playbook`, `runAgent`, `transfer`, `handover` or `openUrl`.
- `label` — string — The action's label, as the asset shows it.
- `status` — string **(required)** _(enum: `launched`, `completed`, `failed`)_
- `result` — any — Execution result payload, for smart actions with `show_card` result mode.
- `error` — string — Failure description when status is `failed`.
- `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`CopilotActionStatus`**

- string _(enum: `launched`, `completed`, `failed`)_

**`CopilotAskEvent`**

_An ask recorded in the session. The ask itself runs as a regular Wilma session (wilma-assistant); any agent in the company can render its output by presenting `accessToken` to wilma-assistant — copilot sessions are shared within the tenant._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `userId` — string **(required)** — The user who asked. _(minLen=12; maxLen=12)_
- `wilmaSessionId` — string **(required)** — The Wilma session (wilma-assistant) holding the ask and its output.
- `accessToken` — string — Read-only, session-scoped, expiring token other agents present to wilma-assistant to view the ask output.

**`CopilotAskState`**

_An ask recorded in the session. Its output lives in the Wilma session it ran as._

- `userId` — string **(required)** — The user who asked. _(minLen=12; maxLen=12)_
- `wilmaSessionId` — string **(required)** — The Wilma session (wilma-assistant) holding the ask and its output.
- `askedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`CopilotAssetEvent`**

_An asset shown or updated in the session. Carries the full asset state at this point; re-emitted on updates (e.g. playbook progress)._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `id` — string **(required)**
- `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
- `styling` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
- `sticky` — boolean
- `content` — string
- `state` — any **(required)**

**`CopilotAssetState`**

_An asset shown in the session, as its latest asset event left it._

- `id` — string **(required)**
- `name` — string **(required)** — The asset's name, as configured; for an automation or a knowledge answer, the automation's name or the question.
- `title` — string
- `content` — string — The body shown: markdown, static or agent-generated.
- `status` — string — Where the shown body stands, e.g. `pending`, `complete` or `error`; a knowledge answer is `suggested` then `answered`.
- `state` — any **(required)** — Presentation data of the asset's kind, such as playbook progress, as its latest event carries it.
- `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
- `styling` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
- `sticky` — boolean
- `shownAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`CopilotAssetView`**

_One asset the user actually saw rendered in the copilot panel._

- `assetId` — string **(required)**
- `at` — string — When the asset became visible. Defaults to the time the report is ingested.

**`CopilotAssistantEvent`**

_An assistant chat shown or updated in the session._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `id` — string **(required)**
- `state` — any **(required)**

**`CopilotCallFlowState`**

_One WDA flow of a call._

- `flowIndex` — number **(required)**
- `caller` — string — Id of the calling participant, from `participants`.
- `callee` — string — Id of the called participant, from `participants`.
- `direction` — string
- `status` — string
- `queue` — string
- `startTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `endTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `duration` — number — How long the flow lasted, in seconds.

**`CopilotClientAction`**

_One user interaction with copilot output. Exactly one member is set._

- _oneOf_ — exactly one of:
  - **`knowledgeSearch`**
    - `knowledgeSearch` — KnowledgeSearchClientAction **(required)** — Launches the knowledge search suggested for a detected question (contextual knowledge answers, `suggest_action` mode).
      - `questionId` — string **(required)** — The suggested question's id — the `questionId` carried by the suggestion asset's action payload.
      - `question` — string — The question text; used when the suggestion is no longer part of the live session state (e.g. after a revive).
  - **`smartAction`**
    - `smartAction` — SmartActionClientAction **(required)** — Invokes one smart action offered by an asset.
      - `assetId` — string **(required)** — Id of the asset carrying the smart action.
      - `actionId` — string **(required)** — Id of the clicked action inside the asset's smart-action list.
      - `variables` — any — Values for `guided` variable bindings collected from the user, keyed by variable name.
  - **`playbook`**
    - `playbook` — PlaybookClientAction **(required)** — Records playbook progress the agent made by hand: the steps that do not auto-complete from the transcript, and — where the playbook allows it — the playbook itself. Progress is append-only, so a step the transcript already completed stays complete and re-sending an id is a no-op.
      - `assetId` — string **(required)** — Id of the asset carrying the playbook.
      - `stepIds` — array — Steps the agent ticked. Ids that are not steps of this playbook are ignored.
        - _array of_ `string`
      - `complete` — boolean — Marks the whole playbook complete. Honoured only when the playbook's `completionCriteria` is `manual` with `allowAgentMarkComplete`; ignored for semantic criteria, where the model owns the goal verdict. Required steps still gate the checkmark either way.

**`CopilotContextAttributes`**

_Open string-to-string enrichment carried by a context event, e.g. `phonebook.name`, `call.direction`, `salesforce.deal_stage`, `match.confidence`. Keys are dot-namespaced by source. Values feed the session state that profile conditions evaluate. Identities do not belong here — emails, phones and entity references are first-class envelope fields._

- _map of_ `string`

**`CopilotContextConversation`**

_The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids._

- `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
- `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_

**`CopilotContextEntity`**

_A typed reference to a record in an external system. `type` is dot-namespaced by system, e.g. `salesforce.contact`, `salesforce.account`, `hubspot.contact`, `phonebook.contact`._

- `id` — string **(required)**
- `type` — string **(required)**

**`CopilotContextLookup`**

_The result of a client-side contact lookup: the identities and enrichment in scope for the customer. Reused by Open (optional — an already-bound channel or an anonymous call needs none) and Enrich (late-arriving evidence, e.g. a CRM match resolved after open)._

- `emails` — array — Customer email addresses. Identity, first-class: merged into the relationship.
  - _array of_ `string`
- `phones` — array — Customer phone numbers. Identity, first-class: merged into the relationship.
  - _array of_ `string`
- `entities` — array — Typed references to records in external systems, e.g. a Salesforce contact. Identity, first-class: merged into the relationship.
  - _array of_ `CopilotContextEntity`
    - `id` — string **(required)**
    - `type` — string **(required)**
- `attributes` — CopilotContextAttributes — Open string-to-string enrichment carried by a context event, e.g. `phonebook.name`, `call.direction`, `salesforce.deal_stage`, `match.confidence`. Keys are dot-namespaced by source. Values feed the session state that profile conditions evaluate. Identities do not belong here — emails, phones and entity references are first-class envelope fields.
  - _map of_ `string`

**`CopilotConversationKind`**

_The kind of conversation a context event or session refers to._

- string _(enum: `call`, `chat`, `conference`, `app`)_

**`CopilotConversationState`**

_What WDA reported about the conversation itself. A fact the source has not reported is absent._

- `callId` — string — WDA call id, for a call.
- `callFlows` — array — The call's flows, oldest first, when it has more than one: each transfer adds one.
  - _array of_ `CopilotCallFlowState`
    - `flowIndex` — number **(required)**
    - `caller` — string — Id of the calling participant, from `participants`.
    - `callee` — string — Id of the called participant, from `participants`.
    - `direction` — string
    - `status` — string
    - `queue` — string
    - `startTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `endTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `duration` — number — How long the flow lasted, in seconds.
- `channelId` — string — Chat channel id, for a chat.
- `chatId` — string — WDA chat id, one chat session within `channelId`, for a chat.
- `conferenceId` — string — WDA conference id, for a conference.
- `direction` — string — Direction as WDA reports it, e.g. `INBOUND`, `OUTBOUND`.
- `status` — string — Status as WDA reports it, e.g. `TALKING`, `ANSWERED`, `MISSED`; `ENDED` for a conversation that ended before WDA sent a final record of it.
- `flags` — array
  - _array of_ `string`
- `service` — string
- `queue` — string
- `language` — string — Transcription language.
- `tags` — array
  - _array of_ `string`
- `startTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `endTime` — string — When the conversation ended; absent while it is in progress.
- `duration` — number — How long the conversation lasted, in seconds; so far, while it is in progress.
- `talkTime` — number — Time spent talking, in seconds.
- `waitTime` — number — Time spent waiting to be answered, in seconds.
- `holdTime` — number — Time spent on hold, in seconds.

**`CopilotEvaluationEvent`**

_An evaluation result detected or updated in the session. Carries the full evaluation state at this point; re-emitted on updates._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `id` — string **(required)**
- `state` — any **(required)**

**`CopilotEvaluationState`**

_The latest result of one evaluation._

- `id` — string **(required)**
- `name` — string **(required)** — The evaluation's name, as configured; for a built-in signal, `sentiment`, `csat`, `topics` or `talk_ratio`.
- `value` — any — The current result, shaped by the evaluation: a label, a score, a list.
- `previous` — any — The result before the latest change.
- `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`CopilotIngestedSession`**

_The session an ingested context event was routed to._

- `id` — string **(required)** _(minLen=1; maxLen=128)_
- `state` — string **(required)** — How an ingested event was attached to a session. _(enum: `created`, `reused`)_

**`CopilotIngestedSessionState`**

_How an ingested event was attached to a session._

- string _(enum: `created`, `reused`)_

**`CopilotIntentEvent`**

_An intent detected or updated in the session. Carries the full intent state at this point; re-emitted on updates._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `id` — string **(required)**
- `state` — any **(required)**

**`CopilotIntentOptionState`**

_One option of an intent._

- `id` — string **(required)**
- `name` — string — The option's name, as configured.

**`CopilotIntentState`**

_An intent detected in the conversation._

- `id` — string **(required)**
- `name` — string **(required)** — The intent's name, as configured.
- `option` — CopilotIntentOptionState — One option of an intent.
  - `id` — string **(required)**
  - `name` — string — The option's name, as configured.
- `fields` — any — Values extracted for the intent's fields, by field name.
- `detectedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`CopilotLifecycleEvent`**

_Session lifecycle transition. Emitted on attach and on every status transition; `reason` says why the session moved. This is where a client learns the trace recording the session, delivered on attach._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
- `traceId` — string — Opaque trace identifier generated by the tracing runtime. _(minLen=1; maxLen=128)_
- `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
- `reason` — string — Why a lifecycle transition happened. _(enum: `created`, `ended`, `stopped`, `inactivity`, `archive_timer`, `revived`, `error`)_

**`CopilotLifecycleReason`**

_Why a lifecycle transition happened._

- string _(enum: `created`, `ended`, `stopped`, `inactivity`, `archive_timer`, `revived`, `error`)_

**`CopilotParticipantState`**

_A party of the assisted conversation._

- `id` — string **(required)** — Unique and stable within the session: a person keeps one id across every flow of a transferred call. Transcript lines and call flows refer to participants by it.
- `name` — string
- `role` — string — Side of the conversation, e.g. `agent` or `customer`, when known.
- `company` — string — Company the party belongs to, as the source names it.
- `department` — string
- `group` — string — PBX group of a colleague.
- `extension` — string — PBX extension of a colleague.
- `phone` — string — Phone number the party was reached on.
- `country` — string — Country of the party's phone number, ISO 3166-1 alpha-2.
- `email` — string

**`CopilotRelationshipEvent`**

_A relationship update visible to an active session — e.g. another session was created or revived on the same relationship._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `relationshipId` — string **(required)** — Id of a relationship: the durable, cross-channel view of one customer that copilot sessions attach to. Identities (emails, phones, entities) merge into it as context is ingested. _(minLen=1; maxLen=128)_
- `sessionId` — string — The other session attached to the same relationship, when the update is about one. _(minLen=1; maxLen=128)_

**`CopilotSessionEvent`**

_A single typed copilot session event. Exactly one member is set; the member name doubles as the `event:` field of the SSE frames produced by StreamSessionEvents._

- _oneOf_ — exactly one of:
  - **`lifecycle`**
    - `lifecycle` — CopilotLifecycleEvent **(required)** — Session lifecycle transition. Emitted on attach and on every status transition; `reason` says why the session moved. This is where a client learns the trace recording the session, delivered on attach.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
      - `traceId` — string — Opaque trace identifier generated by the tracing runtime. _(minLen=1; maxLen=128)_
      - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
      - `reason` — string — Why a lifecycle transition happened. _(enum: `created`, `ended`, `stopped`, `inactivity`, `archive_timer`, `revived`, `error`)_
  - **`transcript`**
    - `transcript` — CopilotTranscriptionEvent **(required)** — A live transcription segment from the assisted conversation. Carries the original WDA analytics event without simplification.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `data` — union **(required)** — Original WDA live transcription event for the assisted conversation surface.
        - _oneOf_ — exactly one of:
          - **`call`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`chat`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`conference`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - **`intent`**
    - `intent` — CopilotIntentEvent **(required)** — An intent detected or updated in the session. Carries the full intent state at this point; re-emitted on updates.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `id` — string **(required)**
      - `state` — any **(required)**
  - **`evaluation`**
    - `evaluation` — CopilotEvaluationEvent **(required)** — An evaluation result detected or updated in the session. Carries the full evaluation state at this point; re-emitted on updates.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `id` — string **(required)**
      - `state` — any **(required)**
  - **`asset`**
    - `asset` — CopilotAssetEvent **(required)** — An asset shown or updated in the session. Carries the full asset state at this point; re-emitted on updates (e.g. playbook progress).
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `id` — string **(required)**
      - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
      - `styling` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
      - `sticky` — boolean
      - `content` — string
      - `state` — any **(required)**
  - **`assistant`**
    - `assistant` — CopilotAssistantEvent **(required)** — An assistant chat shown or updated in the session.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `id` — string **(required)**
      - `state` — any **(required)**
  - **`relationship`**
    - `relationship` — CopilotRelationshipEvent **(required)** — A relationship update visible to an active session — e.g. another session was created or revived on the same relationship.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `relationshipId` — string **(required)** — Id of a relationship: the durable, cross-channel view of one customer that copilot sessions attach to. Identities (emails, phones, entities) merge into it as context is ingested. _(minLen=1; maxLen=128)_
      - `sessionId` — string — The other session attached to the same relationship, when the update is about one. _(minLen=1; maxLen=128)_
  - **`ask`**
    - `ask` — CopilotAskEvent **(required)** — An ask recorded in the session. The ask itself runs as a regular Wilma session (wilma-assistant); any agent in the company can render its output by presenting `accessToken` to wilma-assistant — copilot sessions are shared within the tenant.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `userId` — string **(required)** — The user who asked. _(minLen=12; maxLen=12)_
      - `wilmaSessionId` — string **(required)** — The Wilma session (wilma-assistant) holding the ask and its output.
      - `accessToken` — string — Read-only, session-scoped, expiring token other agents present to wilma-assistant to view the ask output.
  - **`action`**
    - `action` — CopilotActionEvent **(required)** — A client action recorded in the session with its execution outcome. Emitted when the action is accepted (`launched`) and re-emitted when its execution settles (`completed` / `failed`).
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `id` — string **(required)** — Id of the asset the action belongs to.
      - `kind` — string **(required)** — What was invoked: `knowledge_search`, `playbook`, `runAgent`, `transfer`, `handover` or `openUrl`.
      - `status` — string **(required)** _(enum: `launched`, `completed`, `failed`)_
      - `userId` — string — The user who triggered the action. _(minLen=12; maxLen=12)_
      - `result` — any — Execution result payload, for smart actions with `show_card` result mode.
      - `error` — string — Failure description when status is `failed`.

**`CopilotSessionState`**

_What copilot knows about a session's conversation._

- `conversation` — CopilotConversationState — What WDA reported about the conversation itself. A fact the source has not reported is absent.
  - `callId` — string — WDA call id, for a call.
  - `callFlows` — array — The call's flows, oldest first, when it has more than one: each transfer adds one.
    - _array of_ `CopilotCallFlowState`
      - `flowIndex` — number **(required)**
      - `caller` — string — Id of the calling participant, from `participants`.
      - `callee` — string — Id of the called participant, from `participants`.
      - `direction` — string
      - `status` — string
      - `queue` — string
      - `startTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `endTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `duration` — number — How long the flow lasted, in seconds.
  - `channelId` — string — Chat channel id, for a chat.
  - `chatId` — string — WDA chat id, one chat session within `channelId`, for a chat.
  - `conferenceId` — string — WDA conference id, for a conference.
  - `direction` — string — Direction as WDA reports it, e.g. `INBOUND`, `OUTBOUND`.
  - `status` — string — Status as WDA reports it, e.g. `TALKING`, `ANSWERED`, `MISSED`; `ENDED` for a conversation that ended before WDA sent a final record of it.
  - `flags` — array
    - _array of_ `string`
  - `service` — string
  - `queue` — string
  - `language` — string — Transcription language.
  - `tags` — array
    - _array of_ `string`
  - `startTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `endTime` — string — When the conversation ended; absent while it is in progress.
  - `duration` — number — How long the conversation lasted, in seconds; so far, while it is in progress.
  - `talkTime` — number — Time spent talking, in seconds.
  - `waitTime` — number — Time spent waiting to be answered, in seconds.
  - `holdTime` — number — Time spent on hold, in seconds.
- `participants` — array **(required)** — Everyone who took part, each once, across every flow of a call.
  - _array of_ `CopilotParticipantState`
    - `id` — string **(required)** — Unique and stable within the session: a person keeps one id across every flow of a transferred call. Transcript lines and call flows refer to participants by it.
    - `name` — string
    - `role` — string — Side of the conversation, e.g. `agent` or `customer`, when known.
    - `company` — string — Company the party belongs to, as the source names it.
    - `department` — string
    - `group` — string — PBX group of a colleague.
    - `extension` — string — PBX extension of a colleague.
    - `phone` — string — Phone number the party was reached on.
    - `country` — string — Country of the party's phone number, ISO 3166-1 alpha-2.
    - `email` — string
- `transcript` — array **(required)** — The whole transcript, oldest first.
  - _array of_ `CopilotTranscriptState`
    - `id` — string **(required)**
    - `flowIndex` — number — For a call, the flow (`conversation.callFlows[].flowIndex`) the line was said on.
    - `speaker` — string — Id of the participant who spoke, from `participants`: on a call or conference the participant whose audio it was, in a chat the message's author. Absent when the source does not say.
    - `role` — string — Side of the conversation the speaker is on, e.g. `agent` or `customer`, when known.
    - `text` — string **(required)**
    - `time` — string — When the line was said. On a call or conference, when the speaker started speaking; in a chat, when the message was sent.
    - `endTime` — string — When the speaker stopped speaking. Calls and conferences only.
    - `offset` — number — Time from the conversation's start (`conversation.startTime`) to `time`, in milliseconds, so lines lay out on one timeline.
- `lookup` — CopilotContextLookup — The result of a client-side contact lookup: the identities and enrichment in scope for the customer. Reused by Open (optional — an already-bound channel or an anonymous call needs none) and Enrich (late-arriving evidence, e.g. a CRM match resolved after open).
  - `emails` — array — Customer email addresses. Identity, first-class: merged into the relationship.
    - _array of_ `string`
  - `phones` — array — Customer phone numbers. Identity, first-class: merged into the relationship.
    - _array of_ `string`
  - `entities` — array — Typed references to records in external systems, e.g. a Salesforce contact. Identity, first-class: merged into the relationship.
    - _array of_ `CopilotContextEntity`
      - `id` — string **(required)**
      - `type` — string **(required)**
  - `attributes` — CopilotContextAttributes — Open string-to-string enrichment carried by a context event, e.g. `phonebook.name`, `call.direction`, `salesforce.deal_stage`, `match.confidence`. Keys are dot-namespaced by source. Values feed the session state that profile conditions evaluate. Identities do not belong here — emails, phones and entity references are first-class envelope fields.
    - _map of_ `string`
- `intents` — array **(required)** — Intents detected so far.
  - _array of_ `CopilotIntentState`
    - `id` — string **(required)**
    - `name` — string **(required)** — The intent's name, as configured.
    - `option` — CopilotIntentOptionState — One option of an intent.
      - `id` — string **(required)**
      - `name` — string — The option's name, as configured.
    - `fields` — any — Values extracted for the intent's fields, by field name.
    - `detectedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `evaluations` — array **(required)** — Evaluation results so far, including the built-in signals `sentiment`, `csat`, `topics` and `talk_ratio`.
  - _array of_ `CopilotEvaluationState`
    - `id` — string **(required)**
    - `name` — string **(required)** — The evaluation's name, as configured; for a built-in signal, `sentiment`, `csat`, `topics` or `talk_ratio`.
    - `value` — any — The current result, shaped by the evaluation: a label, a score, a list.
    - `previous` — any — The result before the latest change.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `assets` — array **(required)** — Assets shown so far, in the order they were first shown.
  - _array of_ `CopilotAssetState`
    - `id` — string **(required)**
    - `name` — string **(required)** — The asset's name, as configured; for an automation or a knowledge answer, the automation's name or the question.
    - `title` — string
    - `content` — string — The body shown: markdown, static or agent-generated.
    - `status` — string — Where the shown body stands, e.g. `pending`, `complete` or `error`; a knowledge answer is `suggested` then `answered`.
    - `state` — any **(required)** — Presentation data of the asset's kind, such as playbook progress, as its latest event carries it.
    - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
    - `styling` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
    - `sticky` — boolean
    - `shownAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `actions` — array **(required)** — Actions invoked so far, in the order they were invoked.
  - _array of_ `CopilotActionState`
    - `id` — string **(required)** — Id of the asset the action belongs to.
    - `actionId` — string — Id of the action within the asset.
    - `userId` — string — The user who triggered the action. _(minLen=12; maxLen=12)_
    - `kind` — string **(required)** — What was invoked: `knowledge_search`, `playbook`, `runAgent`, `transfer`, `handover` or `openUrl`.
    - `label` — string — The action's label, as the asset shows it.
    - `status` — string **(required)** _(enum: `launched`, `completed`, `failed`)_
    - `result` — any — Execution result payload, for smart actions with `show_card` result mode.
    - `error` — string — Failure description when status is `failed`.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `asks` — array **(required)** — Asks recorded so far, oldest first.
  - _array of_ `CopilotAskState`
    - `userId` — string **(required)** — The user who asked. _(minLen=12; maxLen=12)_
    - `wilmaSessionId` — string **(required)** — The Wilma session (wilma-assistant) holding the ask and its output.
    - `askedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`CopilotSessionStatus`**

- string _(enum: `active`, `idle`, `archived`, `failed`)_

**`CopilotSessionSummary`**

_A compact view of a copilot session associated with a relationship. Sessions are owned by the company and shared within the tenant._

- `id` — string **(required)** _(minLen=1; maxLen=128)_
- `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
- `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
  - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
  - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
- `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.

**`CopilotTranscriptState`**

_One transcript line: an utterance of a call or conference, or a chat message._

- `id` — string **(required)**
- `flowIndex` — number — For a call, the flow (`conversation.callFlows[].flowIndex`) the line was said on.
- `speaker` — string — Id of the participant who spoke, from `participants`: on a call or conference the participant whose audio it was, in a chat the message's author. Absent when the source does not say.
- `role` — string — Side of the conversation the speaker is on, e.g. `agent` or `customer`, when known.
- `text` — string **(required)**
- `time` — string — When the line was said. On a call or conference, when the speaker started speaking; in a chat, when the message was sent.
- `endTime` — string — When the speaker stopped speaking. Calls and conferences only.
- `offset` — number — Time from the conversation's start (`conversation.startTime`) to `time`, in milliseconds, so lines lay out on one timeline.

**`CopilotTranscriptionData`**

_Original WDA live transcription event for the assisted conversation surface._

- _oneOf_ — exactly one of:
  - **`call`**
    - `call` — CallAnalyticsLiveTranscriptionEvent **(required)**
      - `id` — string **(required)**
      - `pbx` — string **(required)**
      - `time` — number **(required)**
      - `company` — string **(required)** _(minLen=3; maxLen=30)_
      - `licenses` — array **(required)**
        - _array of_ `License`
      - `event` — object **(required)**
      - `flowIndex` — number **(required)**
      - `flowStartTime` — number **(required)**
      - `callStartTime` — number **(required)**
      - `chunk` — CallTranscriptionChunk **(required)**
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
      - `participant` — CallParticipant
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
  - **`chat`**
    - `chat` — ChatAnalyticsLiveTranscriptionEvent **(required)**
      - `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
      - `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
      - `time` — number **(required)**
      - `company` — string **(required)** _(minLen=3; maxLen=30)_
      - `event` — object **(required)**
      - `message` — Message **(required)**
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
  - **`conference`**
    - `conference` — ConferenceAnalyticsLiveTranscriptionEvent **(required)**
      - `id` — string **(required)**
      - `time` — number **(required)**
      - `company` — string **(required)** _(minLen=3; maxLen=30)_
      - `event` — object **(required)**
      - `conferenceStartTime` — number **(required)**
      - `transcriptionStartTime` — number **(required)**
      - `chunk` — ConferenceTranscriptionChunk **(required)**
        - `id` — string **(required)**
        - `time` — number **(required)**
        - `jid` — string **(required)**
        - `text` — string **(required)**
        - `language` — string
        - `isFinal` — boolean **(required)**
        - `start` — number **(required)**
        - `end` — number **(required)**
        - `sentiment` — string — Sentiment label for a transcription chunk. Shared between calls and conferences. _(enum: `POSITIVE`, `NEGATIVE`, `MIXED`, `NEUTRAL`)_
      - `participant` — ConferenceParticipant
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

**`CopilotTranscriptionEvent`**

_A live transcription segment from the assisted conversation. Carries the original WDA analytics event without simplification._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `data` — union **(required)** — Original WDA live transcription event for the assisted conversation surface.
  - _oneOf_ — exactly one of:
    - **`call`**
      - `call` — CallAnalyticsLiveTranscriptionEvent **(required)**
        - `id` — string **(required)**
        - `pbx` — string **(required)**
        - `time` — number **(required)**
        - `company` — string **(required)** _(minLen=3; maxLen=30)_
        - `licenses` — array **(required)**
          - _(nesting depth limit — see `License` in the Schemas appendix)_
        - `event` — object **(required)**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `flowIndex` — number **(required)**
        - `flowStartTime` — number **(required)**
        - `callStartTime` — number **(required)**
        - `chunk` — CallTranscriptionChunk **(required)**
          - _(nesting depth limit — see `CallTranscriptionChunk` in the Schemas appendix)_
        - `participant` — CallParticipant
          - _(nesting depth limit — see `CallParticipant` in the Schemas appendix)_
    - **`chat`**
      - `chat` — ChatAnalyticsLiveTranscriptionEvent **(required)**
        - `id` — string — A unique chat channel identifier, distinguish each chat channel across different types.
        - `chatId` — string — A unique identifier that distinguishes each chat session within a channel.
        - `time` — number **(required)**
        - `company` — string **(required)** _(minLen=3; maxLen=30)_
        - `event` — object **(required)**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `message` — Message **(required)**
          - _(nesting depth limit — see `Message` in the Schemas appendix)_
    - **`conference`**
      - `conference` — ConferenceAnalyticsLiveTranscriptionEvent **(required)**
        - `id` — string **(required)**
        - `time` — number **(required)**
        - `company` — string **(required)** _(minLen=3; maxLen=30)_
        - `event` — object **(required)**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `conferenceStartTime` — number **(required)**
        - `transcriptionStartTime` — number **(required)**
        - `chunk` — ConferenceTranscriptionChunk **(required)**
          - _(nesting depth limit — see `ConferenceTranscriptionChunk` in the Schemas appendix)_
        - `participant` — ConferenceParticipant
          - _(nesting depth limit — see `ConferenceParticipant` in the Schemas appendix)_

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

**`EnrichRequestContent`**

- `company` — string — Company that owns the relationship. Required when calling with a service (s2s) token. _(minLen=3; maxLen=30)_
- `relationshipId` — string **(required)** — Id of a relationship: the durable, cross-channel view of one customer that copilot sessions attach to. Identities (emails, phones, entities) merge into it as context is ingested. _(minLen=1; maxLen=128)_
- `lookup` — CopilotContextLookup **(required)** — The result of a client-side contact lookup: the identities and enrichment in scope for the customer. Reused by Open (optional — an already-bound channel or an anonymous call needs none) and Enrich (late-arriving evidence, e.g. a CRM match resolved after open).
  - `emails` — array — Customer email addresses. Identity, first-class: merged into the relationship.
    - _array of_ `string`
  - `phones` — array — Customer phone numbers. Identity, first-class: merged into the relationship.
    - _array of_ `string`
  - `entities` — array — Typed references to records in external systems, e.g. a Salesforce contact. Identity, first-class: merged into the relationship.
    - _array of_ `CopilotContextEntity`
      - `id` — string **(required)**
      - `type` — string **(required)**
  - `attributes` — CopilotContextAttributes — Open string-to-string enrichment carried by a context event, e.g. `phonebook.name`, `call.direction`, `salesforce.deal_stage`, `match.confidence`. Keys are dot-namespaced by source. Values feed the session state that profile conditions evaluate. Identities do not belong here — emails, phones and entity references are first-class envelope fields.
    - _map of_ `string`

**`EnrichResponseContent`**

- `relationshipId` — string **(required)** — The authoritative relationship after applying the evidence. May differ from the input when strong evidence re-resolves the customer. _(minLen=1; maxLen=128)_
- `related` — array **(required)** — Sessions associated with the authoritative relationship, most recent first.
  - _array of_ `CopilotSessionSummary`
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
    - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
      - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
      - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetSessionEventsResponseContent`**

- `events` — array **(required)**
  - _array of_ `CopilotSessionEvent`
    - _oneOf_ — exactly one of:
      - **`lifecycle`**
        - `lifecycle` — CopilotLifecycleEvent **(required)** — Session lifecycle transition. Emitted on attach and on every status transition; `reason` says why the session moved. This is where a client learns the trace recording the session, delivered on attach.
          - _(nesting depth limit — see `CopilotLifecycleEvent` in the Schemas appendix)_
      - **`transcript`**
        - `transcript` — CopilotTranscriptionEvent **(required)** — A live transcription segment from the assisted conversation. Carries the original WDA analytics event without simplification.
          - _(nesting depth limit — see `CopilotTranscriptionEvent` in the Schemas appendix)_
      - **`intent`**
        - `intent` — CopilotIntentEvent **(required)** — An intent detected or updated in the session. Carries the full intent state at this point; re-emitted on updates.
          - _(nesting depth limit — see `CopilotIntentEvent` in the Schemas appendix)_
      - **`evaluation`**
        - `evaluation` — CopilotEvaluationEvent **(required)** — An evaluation result detected or updated in the session. Carries the full evaluation state at this point; re-emitted on updates.
          - _(nesting depth limit — see `CopilotEvaluationEvent` in the Schemas appendix)_
      - **`asset`**
        - `asset` — CopilotAssetEvent **(required)** — An asset shown or updated in the session. Carries the full asset state at this point; re-emitted on updates (e.g. playbook progress).
          - _(nesting depth limit — see `CopilotAssetEvent` in the Schemas appendix)_
      - **`assistant`**
        - `assistant` — CopilotAssistantEvent **(required)** — An assistant chat shown or updated in the session.
          - _(nesting depth limit — see `CopilotAssistantEvent` in the Schemas appendix)_
      - **`relationship`**
        - `relationship` — CopilotRelationshipEvent **(required)** — A relationship update visible to an active session — e.g. another session was created or revived on the same relationship.
          - _(nesting depth limit — see `CopilotRelationshipEvent` in the Schemas appendix)_
      - **`ask`**
        - `ask` — CopilotAskEvent **(required)** — An ask recorded in the session. The ask itself runs as a regular Wilma session (wilma-assistant); any agent in the company can render its output by presenting `accessToken` to wilma-assistant — copilot sessions are shared within the tenant.
          - _(nesting depth limit — see `CopilotAskEvent` in the Schemas appendix)_
      - **`action`**
        - `action` — CopilotActionEvent **(required)** — A client action recorded in the session with its execution outcome. Emitted when the action is accepted (`launched`) and re-emitted when its execution settles (`completed` / `failed`).
          - _(nesting depth limit — see `CopilotActionEvent` in the Schemas appendix)_
- `nextStartIndex` — number — Present when more events exist; pass it as `startIndex` of the next call.

**`GetSessionStateResponseContent`**

- `session` — CopilotSessionSummary **(required)** — A compact view of a copilot session associated with a relationship. Sessions are owned by the company and shared within the tenant.
  - `id` — string **(required)** _(minLen=1; maxLen=128)_
  - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
  - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
    - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
    - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
  - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.
- `state` — CopilotSessionState **(required)** — What copilot knows about a session's conversation.
  - `conversation` — CopilotConversationState — What WDA reported about the conversation itself. A fact the source has not reported is absent.
    - `callId` — string — WDA call id, for a call.
    - `callFlows` — array — The call's flows, oldest first, when it has more than one: each transfer adds one.
      - _array of_ `CopilotCallFlowState`
        - _(nesting depth limit — see `CopilotCallFlowState` in the Schemas appendix)_
    - `channelId` — string — Chat channel id, for a chat.
    - `chatId` — string — WDA chat id, one chat session within `channelId`, for a chat.
    - `conferenceId` — string — WDA conference id, for a conference.
    - `direction` — string — Direction as WDA reports it, e.g. `INBOUND`, `OUTBOUND`.
    - `status` — string — Status as WDA reports it, e.g. `TALKING`, `ANSWERED`, `MISSED`; `ENDED` for a conversation that ended before WDA sent a final record of it.
    - `flags` — array
      - _array of_ `string`
    - `service` — string
    - `queue` — string
    - `language` — string — Transcription language.
    - `tags` — array
      - _array of_ `string`
    - `startTime` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `endTime` — string — When the conversation ended; absent while it is in progress.
    - `duration` — number — How long the conversation lasted, in seconds; so far, while it is in progress.
    - `talkTime` — number — Time spent talking, in seconds.
    - `waitTime` — number — Time spent waiting to be answered, in seconds.
    - `holdTime` — number — Time spent on hold, in seconds.
  - `participants` — array **(required)** — Everyone who took part, each once, across every flow of a call.
    - _array of_ `CopilotParticipantState`
      - `id` — string **(required)** — Unique and stable within the session: a person keeps one id across every flow of a transferred call. Transcript lines and call flows refer to participants by it.
      - `name` — string
      - `role` — string — Side of the conversation, e.g. `agent` or `customer`, when known.
      - `company` — string — Company the party belongs to, as the source names it.
      - `department` — string
      - `group` — string — PBX group of a colleague.
      - `extension` — string — PBX extension of a colleague.
      - `phone` — string — Phone number the party was reached on.
      - `country` — string — Country of the party's phone number, ISO 3166-1 alpha-2.
      - `email` — string
  - `transcript` — array **(required)** — The whole transcript, oldest first.
    - _array of_ `CopilotTranscriptState`
      - `id` — string **(required)**
      - `flowIndex` — number — For a call, the flow (`conversation.callFlows[].flowIndex`) the line was said on.
      - `speaker` — string — Id of the participant who spoke, from `participants`: on a call or conference the participant whose audio it was, in a chat the message's author. Absent when the source does not say.
      - `role` — string — Side of the conversation the speaker is on, e.g. `agent` or `customer`, when known.
      - `text` — string **(required)**
      - `time` — string — When the line was said. On a call or conference, when the speaker started speaking; in a chat, when the message was sent.
      - `endTime` — string — When the speaker stopped speaking. Calls and conferences only.
      - `offset` — number — Time from the conversation's start (`conversation.startTime`) to `time`, in milliseconds, so lines lay out on one timeline.
  - `lookup` — CopilotContextLookup — The result of a client-side contact lookup: the identities and enrichment in scope for the customer. Reused by Open (optional — an already-bound channel or an anonymous call needs none) and Enrich (late-arriving evidence, e.g. a CRM match resolved after open).
    - `emails` — array — Customer email addresses. Identity, first-class: merged into the relationship.
      - _array of_ `string`
    - `phones` — array — Customer phone numbers. Identity, first-class: merged into the relationship.
      - _array of_ `string`
    - `entities` — array — Typed references to records in external systems, e.g. a Salesforce contact. Identity, first-class: merged into the relationship.
      - _array of_ `CopilotContextEntity`
        - _(nesting depth limit — see `CopilotContextEntity` in the Schemas appendix)_
    - `attributes` — CopilotContextAttributes — Open string-to-string enrichment carried by a context event, e.g. `phonebook.name`, `call.direction`, `salesforce.deal_stage`, `match.confidence`. Keys are dot-namespaced by source. Values feed the session state that profile conditions evaluate. Identities do not belong here — emails, phones and entity references are first-class envelope fields.
      - _map of_ `string`
  - `intents` — array **(required)** — Intents detected so far.
    - _array of_ `CopilotIntentState`
      - `id` — string **(required)**
      - `name` — string **(required)** — The intent's name, as configured.
      - `option` — CopilotIntentOptionState — One option of an intent.
        - _(nesting depth limit — see `CopilotIntentOptionState` in the Schemas appendix)_
      - `fields` — any — Values extracted for the intent's fields, by field name.
      - `detectedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `evaluations` — array **(required)** — Evaluation results so far, including the built-in signals `sentiment`, `csat`, `topics` and `talk_ratio`.
    - _array of_ `CopilotEvaluationState`
      - `id` — string **(required)**
      - `name` — string **(required)** — The evaluation's name, as configured; for a built-in signal, `sentiment`, `csat`, `topics` or `talk_ratio`.
      - `value` — any — The current result, shaped by the evaluation: a label, a score, a list.
      - `previous` — any — The result before the latest change.
      - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `assets` — array **(required)** — Assets shown so far, in the order they were first shown.
    - _array of_ `CopilotAssetState`
      - `id` — string **(required)**
      - `name` — string **(required)** — The asset's name, as configured; for an automation or a knowledge answer, the automation's name or the question.
      - `title` — string
      - `content` — string — The body shown: markdown, static or agent-generated.
      - `status` — string — Where the shown body stands, e.g. `pending`, `complete` or `error`; a knowledge answer is `suggested` then `answered`.
      - `state` — any **(required)** — Presentation data of the asset's kind, such as playbook progress, as its latest event carries it.
      - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
      - `styling` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
      - `sticky` — boolean
      - `shownAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `actions` — array **(required)** — Actions invoked so far, in the order they were invoked.
    - _array of_ `CopilotActionState`
      - `id` — string **(required)** — Id of the asset the action belongs to.
      - `actionId` — string — Id of the action within the asset.
      - `userId` — string — The user who triggered the action. _(minLen=12; maxLen=12)_
      - `kind` — string **(required)** — What was invoked: `knowledge_search`, `playbook`, `runAgent`, `transfer`, `handover` or `openUrl`.
      - `label` — string — The action's label, as the asset shows it.
      - `status` — string **(required)** _(enum: `launched`, `completed`, `failed`)_
      - `result` — any — Execution result payload, for smart actions with `show_card` result mode.
      - `error` — string — Failure description when status is `failed`.
      - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `asks` — array **(required)** — Asks recorded so far, oldest first.
    - _array of_ `CopilotAskState`
      - `userId` — string **(required)** — The user who asked. _(minLen=12; maxLen=12)_
      - `wilmaSessionId` — string **(required)** — The Wilma session (wilma-assistant) holding the ask and its output.
      - `askedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`KnowledgeSearchClientAction`**

_Launches the knowledge search suggested for a detected question (contextual knowledge answers, `suggest_action` mode)._

- `questionId` — string **(required)** — The suggested question's id — the `questionId` carried by the suggestion asset's action payload.
- `question` — string — The question text; used when the suggestion is no longer part of the live session state (e.g. after a revive).

**`License`**

- string _(enum: `x-bees`, `uc`)_

**`ListRelationshipSessionsResponseContent`**

- `sessions` — array **(required)**
  - _array of_ `CopilotSessionSummary`
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
    - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
      - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
      - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.
- `nextCursor` — string — Present when more sessions exist; pass it as `cursor` of the next call. _(minLen=1; maxLen=2048)_

**`ListSessionsResponseContent`**

- `sessions` — array **(required)**
  - _array of_ `CopilotSessionSummary`
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
    - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
      - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
      - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.
- `nextCursor` — string — Present when more sessions exist; pass it as `cursor` of the next call. _(minLen=1; maxLen=2048)_

**`LiveEventType`**

- string _(enum: `chat`, `chat_annotation`, `chat_transcription`, `chat_complete`, `chat_interrupted`, `chat_missed`, `call_cost`, `call`, `call_annotation`, `call_complete`, `call_interrupted`, `call_transcription`, … (+15))_

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

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`OpenRequestContent`**

- `company` — string — Company that owns the relationship. Required when calling with a service (s2s) token, which is not scoped to a single company. _(minLen=3; maxLen=30)_
- `lookup` — CopilotContextLookup — The result of a client-side contact lookup: the identities and enrichment in scope for the customer. Reused by Open (optional — an already-bound channel or an anonymous call needs none) and Enrich (late-arriving evidence, e.g. a CRM match resolved after open).
  - `emails` — array — Customer email addresses. Identity, first-class: merged into the relationship.
    - _array of_ `string`
  - `phones` — array — Customer phone numbers. Identity, first-class: merged into the relationship.
    - _array of_ `string`
  - `entities` — array — Typed references to records in external systems, e.g. a Salesforce contact. Identity, first-class: merged into the relationship.
    - _array of_ `CopilotContextEntity`
      - `id` — string **(required)**
      - `type` — string **(required)**
  - `attributes` — CopilotContextAttributes — Open string-to-string enrichment carried by a context event, e.g. `phonebook.name`, `call.direction`, `salesforce.deal_stage`, `match.confidence`. Keys are dot-namespaced by source. Values feed the session state that profile conditions evaluate. Identities do not belong here — emails, phones and entity references are first-class envelope fields.
    - _map of_ `string`

**`OpenResponseContent`**

- `relationshipId` — string **(required)** — Id of a relationship: the durable, cross-channel view of one customer that copilot sessions attach to. Identities (emails, phones, entities) merge into it as context is ingested. _(minLen=1; maxLen=128)_
- `session` — CopilotIngestedSession **(required)** — The session an ingested context event was routed to.
  - `id` — string **(required)** _(minLen=1; maxLen=128)_
  - `state` — string **(required)** — How an ingested event was attached to a session. _(enum: `created`, `reused`)_
- `related` — array **(required)** — Sessions already associated with the relationship, most recent first. Excludes the session the open was routed to.
  - _array of_ `CopilotSessionSummary`
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
    - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
      - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
      - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.

**`PbxLicenseType`**

- string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_

**`PlaybookClientAction`**

_Records playbook progress the agent made by hand: the steps that do not auto-complete from the transcript, and — where the playbook allows it — the playbook itself. Progress is append-only, so a step the transcript already completed stays complete and re-sending an id is a no-op._

- `assetId` — string **(required)** — Id of the asset carrying the playbook.
- `stepIds` — array — Steps the agent ticked. Ids that are not steps of this playbook are ignored.
  - _array of_ `string`
- `complete` — boolean — Marks the whole playbook complete. Honoured only when the playbook's `completionCriteria` is `manual` with `allowAgentMarkComplete`; ignored for semantic criteria, where the model owns the goal verdict. Required steps still gate the checkmark either way.

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

**`ResolveRequestContent`**

- `company` — string — Company scope. Required when calling with a service (s2s) token. _(minLen=3; maxLen=30)_
- `lookup` — CopilotContextLookup **(required)** — The result of a client-side contact lookup: the identities and enrichment in scope for the customer. Reused by Open (optional — an already-bound channel or an anonymous call needs none) and Enrich (late-arriving evidence, e.g. a CRM match resolved after open).
  - `emails` — array — Customer email addresses. Identity, first-class: merged into the relationship.
    - _array of_ `string`
  - `phones` — array — Customer phone numbers. Identity, first-class: merged into the relationship.
    - _array of_ `string`
  - `entities` — array — Typed references to records in external systems, e.g. a Salesforce contact. Identity, first-class: merged into the relationship.
    - _array of_ `CopilotContextEntity`
      - `id` — string **(required)**
      - `type` — string **(required)**
  - `attributes` — CopilotContextAttributes — Open string-to-string enrichment carried by a context event, e.g. `phonebook.name`, `call.direction`, `salesforce.deal_stage`, `match.confidence`. Keys are dot-namespaced by source. Values feed the session state that profile conditions evaluate. Identities do not belong here — emails, phones and entity references are first-class envelope fields.
    - _map of_ `string`

**`ResolveResponseContent`**

- `relationshipId` — string — The relationship the lookup resolved to, when one matched. Lookup never creates relationships. _(minLen=1; maxLen=128)_
- `sessions` — array **(required)** — Sessions associated with the matched relationship, most recent first. Empty when nothing matched.
  - _array of_ `CopilotSessionSummary`
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `status` — string **(required)** _(enum: `active`, `idle`, `archived`, `failed`)_
    - `conversation` — CopilotContextConversation **(required)** — The conversation a copilot session is bound to. Server-reported (in session summaries) — clients never construct these ids.
      - `id` — string **(required)** — Channel id (chats and conferences), WDA call id (calls), or a server-minted id (`app` sessions).
      - `kind` — string **(required)** — The kind of conversation a context event or session refers to. _(enum: `call`, `chat`, `conference`, `app`)_
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `lastActivityAt` — string — Time of the last event applied to the session; drives the idle and archive transitions.

**`SmartActionClientAction`**

_Invokes one smart action offered by an asset._

- `assetId` — string **(required)** — Id of the asset carrying the smart action.
- `actionId` — string **(required)** — Id of the clicked action inside the asset's smart-action list.
- `variables` — any — Values for `guided` variable bindings collected from the user, keyed by variable name.

**`StreamSessionEventsOutputPayload`**

_Raw Server-Sent Events byte stream (`text/event-stream`). Each frame carries one CopilotSessionEvent: `id:` is the event index, `event:` is the union member name, and `data:` is the JSON document of the union value, e.g. `{"asset": {...}}`._

- string

**`TemplateParameter`**

- `name` — string **(required)**
- `value` — string **(required)**

**`TemplateWithParameters`**

- `name` — string **(required)**
- `parameters` — array
  - _array of_ `TemplateParameter`
    - `name` — string **(required)**
    - `value` — string **(required)**

**`TrackRequestContent`**

- `views` — array **(required)**
  - _array of_ `CopilotAssetView`
    - `assetId` — string **(required)**
    - `at` — string — When the asset became visible. Defaults to the time the report is ingested.

**`TrackResponseContent`**

- `accepted` — boolean **(required)** — True when the views were recorded.

**`TranscriptionSentiment`**

_Sentiment label for a transcription chunk. Shared between calls and conferences._

- string _(enum: `POSITIVE`, `NEGATIVE`, `MIXED`, `NEUTRAL`)_

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
