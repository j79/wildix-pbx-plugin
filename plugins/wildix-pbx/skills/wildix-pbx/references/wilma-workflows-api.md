## Wilma Workflows API

_OpenAPI: Wilma Workflows Service — version v2_

**Servers**

- `https://api.wilma.wildix.com` — Production
- `https://api-stable.wilma.wildix.com` — Stable
- `https://api-stage.wilma.wildix.com` — Stage

### Automations

#### `GET` `/v2/workflows/automations`

Lists automations in the company.

- operationId: `ListAutomations`
- **Scopes**: `wilma-workflows:ListAutomations`, `wilma-workflows:read`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `search` (query) — string — Filter by name or description.
  - `enabled` (query) — boolean — Only automations with this enablement state.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListAutomationsResponseContent`)
  - `automations` — array **(required)**
    - _array of_ `AutomationInfo`
      - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
        - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
        - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
        - `name` — string — Human readable name of the actor at the time of the action.
      - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
        - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
        - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
        - `name` — string — Human readable name of the actor at the time of the action.
      - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `name` — string **(required)**
      - `description` — string
      - `enabled` — boolean
      - `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
        - _oneOf_ — exactly one of:
          - **`schedule`**
            - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
              - `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
              - `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.
          - **`event`**
            - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
              - `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
              - `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
              - `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.
          - **`webhook`**
            - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

#### `POST` `/v2/workflows/automations`

Creates a new automation.

- operationId: `CreateAutomation`
- **Scopes**: `wilma-workflows:CreateAutomation`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateAutomationRequestContent`) **(required)**
  - `name` — string **(required)** _(minLen=1; maxLen=256)_
  - `description` — string
  - `enabled` — boolean — Disabled automations keep their configuration but never fire. Defaults to true.
  - `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`schedule`**
        - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
          - `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
          - `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.
      - **`event`**
        - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
          - `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
          - `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
          - `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.
      - **`webhook`**
        - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
  - `task` — AutomationTaskTemplate **(required)** — The task an automation starts when it fires.
    - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
    - `options` — any
- **Response 200** (`CreateAutomationResponseContent`)
  - `automation` — Automation **(required)** — A configured automation. Tasks it started are listed via ListTasks with `automationId`.
    - `name` — string **(required)** _(minLen=1; maxLen=256)_
    - `description` — string
    - `enabled` — boolean — Disabled automations keep their configuration but never fire. Defaults to true.
    - `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`schedule`**
          - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
            - `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
            - `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.
        - **`event`**
          - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
            - `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
            - `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
            - `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.
        - **`webhook`**
          - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
    - `task` — AutomationTaskTemplate **(required)** — The task an automation starts when it fires.
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `options` — any
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.
- Errors: `400`, `403`, `409`

#### `POST` `/v2/workflows/automations/ingest/{token}`

Ingestion endpoint for `webhook`-triggered automations. External integrations POST their JSON
    payload to the automation's unique URL (see GetAutomationWebhookUrl); the started task receives
    the body as context. Authenticated solely by the opaque `token` in the path — not by the
    service's bearer / s2s / xbs auth. Returns 202; `fired` says whether a task was started.

- operationId: `IngestAutomationWebhook`
- **Parameters**
  - `token` (path) — string **(required)** — The opaque secret from the automation's ingestion URL, identifying the automation to fire.
- **Request body** (`application/json` — `IngestAutomationWebhookInputPayload`)
  - any
- **Response 202** (`IngestAutomationWebhookResponseContent`)
  - `fired` — boolean **(required)** — True when the automation was enabled, so a task was started.
  - `taskId` — string — The started task, present when `fired` is true. _(minLen=1; maxLen=128)_
- Errors: `400`, `404`, `503`

#### `GET` `/v2/workflows/automations/items/{automationId}`

Gets an automation.

- operationId: `GetAutomation`
- **Scopes**: `wilma-workflows:GetAutomation`, `wilma-workflows:read`
- **Parameters**
  - `automationId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetAutomationResponseContent`)
  - `automation` — Automation **(required)** — A configured automation. Tasks it started are listed via ListTasks with `automationId`.
    - `name` — string **(required)** _(minLen=1; maxLen=256)_
    - `description` — string
    - `enabled` — boolean — Disabled automations keep their configuration but never fire. Defaults to true.
    - `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`schedule`**
          - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
            - `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
            - `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.
        - **`event`**
          - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
            - `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
            - `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
            - `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.
        - **`webhook`**
          - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
    - `task` — AutomationTaskTemplate **(required)** — The task an automation starts when it fires.
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `options` — any
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.
- Errors: `400`, `403`, `404`

#### `PUT` `/v2/workflows/automations/items/{automationId}`

Updates an automation. The change applies from the next firing; tasks already started are unaffected.

- operationId: `UpdateAutomation`
- **Scopes**: `wilma-workflows:UpdateAutomation`
- **Parameters**
  - `automationId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateAutomationRequestContent`) **(required)**
  - `name` — string **(required)** _(minLen=1; maxLen=256)_
  - `description` — string
  - `enabled` — boolean — Disabled automations keep their configuration but never fire. Defaults to true.
  - `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`schedule`**
        - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
          - `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
          - `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.
      - **`event`**
        - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
          - `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
          - `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
          - `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.
      - **`webhook`**
        - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
  - `task` — AutomationTaskTemplate **(required)** — The task an automation starts when it fires.
    - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
    - `options` — any
  - `revision` — number **(required)** — Revision this update is based on (optimistic locking).
- **Response 200** (`UpdateAutomationResponseContent`)
  - `automation` — Automation **(required)** — A configured automation. Tasks it started are listed via ListTasks with `automationId`.
    - `name` — string **(required)** _(minLen=1; maxLen=256)_
    - `description` — string
    - `enabled` — boolean — Disabled automations keep their configuration but never fire. Defaults to true.
    - `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`schedule`**
          - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
            - `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
            - `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.
        - **`event`**
          - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
            - `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
            - `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
            - `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.
        - **`webhook`**
          - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
    - `task` — AutomationTaskTemplate **(required)** — The task an automation starts when it fires.
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `options` — any
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.
- Errors: `400`, `403`, `404`, `409`

#### `DELETE` `/v2/workflows/automations/items/{automationId}`

Deletes an automation. Tasks it started remain listed until they age out.

- operationId: `DeleteAutomation`
- **Scopes**: `wilma-workflows:DeleteAutomation`
- **Parameters**
  - `automationId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- Errors: `400`, `403`, `404`

#### `POST` `/v2/workflows/automations/items/{automationId}/run`

Fires an automation immediately (manual run, e.g. to test it), regardless of its trigger and enablement, and returns the handle of the started task.

- operationId: `RunAutomation`
- **Scopes**: `wilma-workflows:RunAutomation`
- **Parameters**
  - `automationId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `RunAutomationRequestContent`)
  - `input` — string — Text handed to the agent for this run, standing in for the trigger payload (e.g. test input).
- **Response 202** (`RunAutomationResponseContent`)
  - `taskId` — string **(required)** _(minLen=1; maxLen=128)_
  - `startIndex` — number **(required)**
  - `traceId` — string — Trace recording this task in wilma-traces — the agent's steps, its model calls and the tools it ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to StreamTaskEvents. This is the id to quote when reporting what an automation did: a task started by a firing trigger has no interactive caller watching it, and RunAutomation returns this handle and nothing else. The trace row is written once the task's first step completes, so GetTrace reports NotFound while the task is still `pending`. _(minLen=1; maxLen=128)_
- Errors: `400`, `403`, `404`, `503`

#### `GET` `/v2/workflows/automations/items/{automationId}/webhook-url`

Returns the unique ingestion URL of a `webhook`-triggered automation, including its secret token. Fails with ConflictException when the automation's trigger is not a webhook.

- operationId: `GetAutomationWebhookUrl`
- **Scopes**: `wilma-workflows:GetAutomationWebhookUrl`, `wilma-workflows:read`
- **Parameters**
  - `automationId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetAutomationWebhookUrlResponseContent`)
  - `webhookUrl` — string **(required)** — The ingestion URL external integrations POST payloads to, including the secret token.
- Errors: `400`, `403`, `404`, `409`

#### `GET` `/v2/workflows/subscriptions`

Lists the wda-stream events event-triggered automations need delivered, for every company that
    has an enabled one — the ingress contract between wda-stream and the workflows runtime.

    **Service tokens only.** The answer spans every company on the platform: it is the event
    producer's routing table, not a tenant's view of its own automations, and there is no company
    parameter to scope it with. A user, PBX or API-key token is refused. Every subscription is
    returned in one response, unpaginated, because the producer applies it as a whole — a table
    assembled from several requests can be applied half-built, which looks exactly like a set of
    companies that unsubscribed.

    One selector per event type an enabled automation subscribes to. Disabled automations, and
    companies whose automations are all schedule- or webhook-triggered, appear nowhere. The producer
    sends every occurrence of a selected type; the consumer evaluates the trigger's conditions on
    delivery.

- operationId: `ListSubscriptions`
- **Scopes**: `wilma-workflows:ListSubscriptions`, `wilma-workflows:read`
- **Response 200** (`ListSubscriptionsResponseContent`)
  - `subscriptions` — array **(required)**
    - _array of_ `Subscription`
      - `company` — string **(required)** _(minLen=3; maxLen=30)_
      - `selectors` — array **(required)** — Event types one tenant needs, deduplicated across everything that asked for them. Two selectors never name the same event type. The producer sends every occurrence of each listed type. _(minItems=1; maxItems=200)_
        - _array of_ `SubscriptionSelector`
          - `event` — string **(required)** — A wda-stream event type, as the webhook envelope names it, e.g. 'call:live:progress', 'call:live:transcription', 'call:completed', 'call:summary:completed', 'chat:live:progress', 'conference:live:transcription'. Open-ended: a new wda-stream type needs no model change here. _(minLen=1; maxLen=128)_
          - `conditions` — any — Reserved; not populated. Producers ignore it and send every occurrence. See SubscriptionConditions.
- Errors: `400`, `403`

### Tasks

#### `GET` `/v2/workflows/tasks`

Lists tasks in the company.

- operationId: `ListTasks`
- **Scopes**: `wilma-workflows:ListTasks`, `wilma-workflows:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `agentId` (query) — string _(minLen=12; maxLen=12)_
  - `automationId` (query) — string — Only tasks started by this automation. _(minLen=1; maxLen=128)_
  - `source` (query) — string — Only tasks started from this exact source URI, e.g. 'wilma://copilot/assets/aB3dE5fG7hJ9'. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
  - `status` (query) — string _(enum: `pending`, `running`, `completed`, `failed`, `stopped`)_
  - `from` (query) — string — Only tasks created at or after this time.
  - `to` (query) — string — Only tasks created before this time.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListTasksResponseContent`)
  - `tasks` — array **(required)**
    - _array of_ `Task`
      - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `status` — string **(required)** _(enum: `pending`, `running`, `completed`, `failed`, `stopped`)_
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Published agent version serving this task, selected at start. _(min=1)_
      - `agentDraft` — boolean — True when the task runs the agent's mutable draft.
      - `traceId` — string — Trace recording this task in wilma-traces — the agent's steps, its model calls and the tools it ran, including the failure behind `error` when `status` is `failed`. Read it with the wilma-traces GetTrace operation. Names the task's own trace. Each tool call, skill load and sandbox the task made is recorded as a trace of its own; list them with QueryTraces filtered by `session.traceId`. Reported from the moment the task is accepted, matching the handle StartTask returned, but the trace row is written when the first step completes — so GetTrace reports NotFound while the task is still `pending`. Absent when the task's trace is not the caller's to read, as when a Wildix built-in agent serves it. _(minLen=1; maxLen=128)_
      - `automationId` — string — Automation whose firing started this task; absent for tasks started over the API. _(minLen=1; maxLen=128)_
      - `model` — string — Effective model resolved at start (after 'default' resolution).
      - `source` — TaskSource — Where a task was started from, when not started directly over the API by an administrator. Set by the integrating service so the task can be tied back to the driving resource; tasks started by an automation carry `automationId` on the task itself.
        - `uri` — string **(required)** — Canonical URI of the driving resource, e.g. 'wilma://copilot/assets/{assetId}' for a copilot asset background job. Supplied by the integrating service and opaque to this one: used to route and group, never to authorize. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
        - `metadata` — any — Additional integration-specific context.
      - `schema` — any — JSON Schema the final output was requested to conform to; echoed from StartTask/RunTask.
      - `result` — TaskResult — Final result of a completed task. `structured` is present when the task was started with a `schema`: the agent's final output parsed and validated against that schema. `text` always carries the plain final answer.
        - `text` — string — Final answer as plain text; present with or without a schema, so a caller can check `structured` against what the agent actually said.
        - `structured` — any — Schema-validated structured output; present when the task was started with a schema.
      - `error` — TaskError
        - `code` — string **(required)** — Stable machine-readable error code.
        - `message` — string **(required)**
      - `usage` — SessionUsage
        - `inputTokens` — number
        - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
        - `outputTokens` — number
        - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
        - `totalTokens` — number
      - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `startedAt` — string — Time execution started; absent while pending.
      - `completedAt` — string — Time the task reached a terminal status.
      - `eventCount` — number **(required)**
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

#### `POST` `/v2/workflows/tasks`

Starts a background task asynchronously and returns the event index from which the caller should stream. Follow progress via StreamTaskEvents and fetch the final result via GetTask.

- operationId: `StartTask`
- **Scopes**: `wilma-workflows:StartTask`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `StartTaskRequestContent`) **(required)**
  - `user` — string — The user the task runs on behalf of. Optional: tasks are company-scoped by default; set it when the task should act with a user's data access. _(minLen=12; maxLen=12)_
  - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
  - `agentVersion` — number — Published agent version to run. Mutually exclusive with agentDraft. When neither is set, the agent's deployment configuration selects the version. _(min=1)_
  - `agentDraft` — boolean — Run the agent's current draft (for testing). Mutually exclusive with agentVersion.
  - `input` — string **(required)** — The instructions / input handed to the agent for this task. _(minLen=1; maxLen=100000)_
  - `context` — array — Additional context documents made available to the agent.
    - _array of_ `any`
  - `mentions` — array — Resources the agent reads as context, resolved with the task user's permissions, or company-wide when the task has no user. _(maxItems=20)_
    - _array of_ `Mention`
      - _oneOf_ — exactly one of:
        - **`reference`**
          - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
            - `uri` — string **(required)** — Canonical URI identifying one entity on the Wilma platform, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://skills/aB3dE5fG7hJ9'. The path names the owning service and entity kind. Opaque to the contracts that carry it; non-Wilma schemes (records of external systems) fit the same shape. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
            - `label` — string — Display name of the mention chip. The model sees it only to name a mention that could not be read or was removed. _(maxLen=256)_
  - `schema` — any — JSON Schema the final output must conform to. When set, the agent's final answer is produced and validated as a structured document, returned in `result.structured`; `result.text` still carries the plain final answer.
  - `options` — any
  - `source` — TaskSource — Where a task was started from, when not started directly over the API by an administrator. Set by the integrating service so the task can be tied back to the driving resource; tasks started by an automation carry `automationId` on the task itself.
    - `uri` — string **(required)** — Canonical URI of the driving resource, e.g. 'wilma://copilot/assets/{assetId}' for a copilot asset background job. Supplied by the integrating service and opaque to this one: used to route and group, never to authorize. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
    - `metadata` — any — Additional integration-specific context.
- **Response 202** (`StartTaskResponseContent`)
  - `taskId` — string **(required)** _(minLen=1; maxLen=128)_
  - `startIndex` — number **(required)**
  - `traceId` — string — Trace recording this task in wilma-traces — the agent's steps, its model calls and the tools it ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to StreamTaskEvents. This is the id to quote when reporting what an automation did: a task started by a firing trigger has no interactive caller watching it, and RunAutomation returns this handle and nothing else. The trace row is written once the task's first step completes, so GetTrace reports NotFound while the task is still `pending`. _(minLen=1; maxLen=128)_
- Errors: `400`, `403`, `503`

#### `GET` `/v2/workflows/tasks/items/{taskId}`

Gets the state of a task, including its result once completed.

- operationId: `GetTask`
- **Scopes**: `wilma-workflows:GetTask`, `wilma-workflows:read`
- **Parameters**
  - `taskId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetTaskResponseContent`)
  - `task` — Task **(required)** — A background execution of a workflow-channel agent.
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `status` — string **(required)** _(enum: `pending`, `running`, `completed`, `failed`, `stopped`)_
    - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
    - `agentVersion` — number — Published agent version serving this task, selected at start. _(min=1)_
    - `agentDraft` — boolean — True when the task runs the agent's mutable draft.
    - `traceId` — string — Trace recording this task in wilma-traces — the agent's steps, its model calls and the tools it ran, including the failure behind `error` when `status` is `failed`. Read it with the wilma-traces GetTrace operation. Names the task's own trace. Each tool call, skill load and sandbox the task made is recorded as a trace of its own; list them with QueryTraces filtered by `session.traceId`. Reported from the moment the task is accepted, matching the handle StartTask returned, but the trace row is written when the first step completes — so GetTrace reports NotFound while the task is still `pending`. Absent when the task's trace is not the caller's to read, as when a Wildix built-in agent serves it. _(minLen=1; maxLen=128)_
    - `automationId` — string — Automation whose firing started this task; absent for tasks started over the API. _(minLen=1; maxLen=128)_
    - `model` — string — Effective model resolved at start (after 'default' resolution).
    - `source` — TaskSource — Where a task was started from, when not started directly over the API by an administrator. Set by the integrating service so the task can be tied back to the driving resource; tasks started by an automation carry `automationId` on the task itself.
      - `uri` — string **(required)** — Canonical URI of the driving resource, e.g. 'wilma://copilot/assets/{assetId}' for a copilot asset background job. Supplied by the integrating service and opaque to this one: used to route and group, never to authorize. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
      - `metadata` — any — Additional integration-specific context.
    - `schema` — any — JSON Schema the final output was requested to conform to; echoed from StartTask/RunTask.
    - `result` — TaskResult — Final result of a completed task. `structured` is present when the task was started with a `schema`: the agent's final output parsed and validated against that schema. `text` always carries the plain final answer.
      - `text` — string — Final answer as plain text; present with or without a schema, so a caller can check `structured` against what the agent actually said.
      - `structured` — any — Schema-validated structured output; present when the task was started with a schema.
    - `error` — TaskError
      - `code` — string **(required)** — Stable machine-readable error code.
      - `message` — string **(required)**
    - `usage` — SessionUsage
      - `inputTokens` — number
      - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
      - `outputTokens` — number
      - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
      - `totalTokens` — number
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `startedAt` — string — Time execution started; absent while pending.
    - `completedAt` — string — Time the task reached a terminal status.
    - `eventCount` — number **(required)**
- Errors: `400`, `403`, `404`

#### `GET` `/v2/workflows/tasks/items/{taskId}/events`

Returns recorded task events as a plain JSON page, without streaming. The event vocabulary is the shared Wilma session event model. Use this to inspect finished tasks or to catch up before subscribing to StreamTaskEvents.

- operationId: `GetTaskEvents`
- **Scopes**: `wilma-workflows:GetTaskEvents`, `wilma-workflows:read`
- **Parameters**
  - `taskId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `startIndex` (query) — number — Return events with `index >= startIndex`. Defaults to 0. _(min=0)_
  - `limit` (query) — number — Maximum number of events to return. Defaults to 1000. _(min=1; max=1000)_
- **Response 200** (`GetTaskEventsResponseContent`)
  - `events` — array **(required)**
    - _array of_ `WorkflowTaskEvent`
      - _oneOf_ — exactly one of:
        - **`sessionStarted`**
          - `sessionStarted` — SessionStartedEvent **(required)** — Emitted once as the very first event of a session, when it is created. Confirms the session id and the agent the session is bound to.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
            - `agentId` — string _(minLen=12; maxLen=12)_
        - **`sessionIdle`**
          - `sessionIdle` — SessionIdleEvent **(required)** — Terminal event of a successful turn: the session is idle and ready for the next turn.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
        - **`sessionStopped`**
          - `sessionStopped` — SessionStoppedEvent **(required)** — Terminal event emitted when the active turn was cancelled via the channel's stop operation.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `reason` — string **(required)** _(enum: `user`)_
        - **`sessionTerminated`**
          - `sessionTerminated` — SessionTerminatedEvent **(required)** — Terminal event emitted when the platform ended the session rather than let it continue: the session is in `terminated` status. Distinct from SessionStoppedEvent, which records a user or operator asking to stop — folding the two together would leave a refused session indistinguishable from a clean finish in every completion-rate report. On voice the call is hung up as this is emitted; on the other channels there is nothing to hang up and termination is the status alone — history is kept, and the session simply accepts no further turns.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `reason` — string **(required)** _(enum: `guardrail`)_
            - `guardrail` — string — The check whose `end` action terminated the session, when `reason` is `guardrail`. _(minLen=1; maxLen=64)_
            - `message` — string — What the caller was told before the session ended.
        - **`sessionFailed`**
          - `sessionFailed` — SessionFailedEvent **(required)** — Terminal event emitted after TurnFailedEvent: the session is in `failed` status. A new turn starts from the last consistent snapshot.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `code` — string **(required)**
            - `message` — string **(required)**
        - **`turnStarted`**
          - `turnStarted` — TurnStartedEvent **(required)** — Emitted when a turn begins executing. All subsequent events up to the matching TurnCompletedEvent/TurnFailedEvent belong to this turn.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)** — 1-based turn number within the session.
        - **`turnCompleted`**
          - `turnCompleted` — TurnCompletedEvent **(required)** — Emitted when a turn finishes successfully, with aggregate token usage for the turn. Followed by SessionIdleEvent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `usage` — SessionUsage
              - `inputTokens` — number
              - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
              - `outputTokens` — number
              - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
              - `totalTokens` — number
        - **`turnFailed`**
          - `turnFailed` — TurnFailedEvent **(required)** — Emitted when a turn fails with an unrecoverable error. Followed by SessionFailedEvent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `code` — string **(required)** — Stable machine-readable error code.
            - `message` — string **(required)**
        - **`messageReceived`**
          - `messageReceived` — MessageReceivedEvent **(required)** — Emitted right after TurnStartedEvent with the user message that triggered the turn, so a reconnecting client can render the conversation without a separate history fetch.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `message` — string **(required)**
            - `attachments` — array — Input files supplied with this message, as stored — enough to render the attachment alongside the message (name, type, size, thumbnail) without a separate Attachments call. Absent when the turn carried no files.
              - _array of_ `Attachment`
                - _(nesting depth limit — see `Attachment` in the Schemas appendix)_
        - **`messageAppended`**
          - `messageAppended` — MessageAppendedEvent **(required)** — Emitted for every assistant text token chunk. High frequency; drives live rendering of the reply.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `delta` — string **(required)** — The new text fragment.
            - `soFar` — string **(required)** — The full assistant text accumulated so far in this step.
        - **`messageCompleted`**
          - `messageCompleted` — MessageCompletedEvent **(required)** — Emitted once per step when the assistant message text is complete.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `text` — string **(required)**
            - `finishReason` — string **(required)** — Model finish reason for the step, e.g. `stop` or `tool-calls`.
        - **`stepStarted`**
          - `stepStarted` — StepStartedEvent **(required)** — Emitted each time the model starts a new inference step within a turn (a turn spans multiple steps when the model calls tools).
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)** — 1-based step number within the turn.
        - **`stepCompleted`**
          - `stepCompleted` — StepCompletedEvent **(required)** — Emitted when an inference step finishes, with token usage for the step when the provider reports it.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `finishReason` — string **(required)**
            - `usage` — SessionUsage
              - `inputTokens` — number
              - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
              - `outputTokens` — number
              - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
              - `totalTokens` — number
        - **`reasoningDelta`**
          - `reasoningDelta` — ReasoningDeltaEvent **(required)** — Emitted for every reasoning (thinking) token chunk the model produces, when the selected model exposes reasoning. High frequency; intended for live typing indicators.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `delta` — string **(required)** — The new reasoning fragment.
            - `soFar` — string **(required)** — The full reasoning text accumulated so far in this step, so late subscribers do not need to replay every delta.
        - **`reasoningCompleted`**
          - `reasoningCompleted` — ReasoningCompletedEvent **(required)** — Emitted once per step after the model finishes its reasoning block, carrying the complete reasoning text.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `reasoning` — string **(required)**
        - **`invocationStarted`**
          - `invocationStarted` — InvocationStartedEvent **(required)** — Emitted when the model begins one tool invocation, before its input is complete. Every invocation starts here, regardless of how it is fulfilled or whether it suspends the turn. Carries the routing facts needed to render it — who fulfils it, whether the turn suspends, where to surface it, whether the input streams — so a client holding no tool registry (a replay, a shared session, an inspector) still renders correctly.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `callId` — string **(required)** — Stable id of this invocation, referenced by every later event about it.
            - `toolName` — string **(required)**
            - `toolId` — string — The wilma-tools Tool backing this invocation. Absent for built-in tools, connector meta-tools and other capabilities that are not shared Tools. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `toolVersion` — number — Published tool version the model was offered, when `toolId` is set. Records which input schema the invocation was written against. _(min=1)_
            - `fulfilment` — string **(required)** — Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend. _(enum: `server`, `client`, `synthetic`)_
            - `gate` — string **(required)** — Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation). _(enum: `none`, `result`, `decision`)_
            - `surface` — string **(required)** — Where a client should surface an invocation. Affects placement only, never behaviour. _(enum: `hidden`, `activity`, `content`)_
            - `stream` — boolean **(required)** — True when the input arrives as InvocationDeltaEvent chunks ahead of InvocationInputCompletedEvent. Opt-in per tool, so tools with small inputs cost nothing.
        - **`invocationDelta`**
          - `invocationDelta` — InvocationDeltaEvent **(required)** — Emitted for each fragment of an invocation's input as the model writes it, when the tool opted into streamed input. The payload is raw partial JSON text exactly as the model emits it; clients parse it incrementally to render an invocation whose input is itself content — a drafted email, a chart spec, a shared document — while it is being written. High frequency.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `callId` — string **(required)**
            - `delta` — string **(required)** — The new fragment of raw JSON input text.
            - `soFar` — string **(required)** — The raw JSON input text accumulated so far in this invocation, so late subscribers need not replay every delta. Being a prefix, it is not necessarily valid JSON on its own.
        - **`invocationInputCompleted`**
          - `invocationInputCompleted` — InvocationInputCompletedEvent **(required)** — Emitted once per invocation when its input is complete and parsed. Always emitted, whether or not the input streamed.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `callId` — string **(required)**
            - `input` — any **(required)**
        - **`invocationResult`**
          - `invocationResult` — InvocationResultEvent **(required)** — Emitted when an invocation is resolved, however that happened: a server tool finishing, a caller returning a client tool's result on resume, a person answering a question or ruling on an approval, or the runtime supplying a `synthetic` tool's result. Emitted for every invocation without exception, so replaying the log from index 0 reconstructs the same state as watching it live.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `callId` — string **(required)** — Id of the invocation this result answers, matching an InvocationStartedEvent.
            - `toolName` — string **(required)**
            - `toolId` — string — The wilma-tools Tool that executed, echoed from InvocationStartedEvent. Absent for invocations that are not backed by a shared Tool. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `toolVersion` — number — Published tool version that executed, when `toolId` is set. _(min=1)_
            - `status` — string **(required)** _(enum: `completed`, `failed`)_
            - `resolvedBy` — string **(required)** — Who supplied the result recorded by an InvocationResultEvent. _(enum: `server`, `client`, `user`)_
            - `output` — any
            - `error` — string — Present when status is `failed`.
        - **`taskStarted`**
          - `taskStarted` — TaskStartedEvent **(required)** — Emitted when the agent delegates a subtask to a task execution: the `delegate` tool or an agent-call capability. Events emitted inside the task are re-published on the session stream with `origin` set to this task, until the matching TaskCompletedEvent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `taskId` — string **(required)** — Unique id of this task execution; referenced by `origin.taskId` of nested events.
            - `name` — string **(required)** — Task tool name, e.g. `delegate` or the name of the called agent.
            - `agentId` — string — Agent executing the task, when the task is a called or delegated agent. _(minLen=12; maxLen=12)_
            - `agentVersion` — number — Published version of the agent executing the task, resolved when the task started; absent when the task runs a draft. _(min=1)_
            - `instructions` — string **(required)** — The self-contained instructions handed to the task.
        - **`taskCompleted`**
          - `taskCompleted` — TaskCompletedEvent **(required)** — Emitted when a delegated task execution finishes, carrying its final answer as returned to the parent agent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `taskId` — string **(required)**
            - `name` — string **(required)**
            - `output` — string **(required)**
        - **`workflowStepEntered`**
          - `workflowStepEntered` — WorkflowStepEnteredEvent **(required)** — Emitted when the workflow cursor arrives at a step, before the step runs — so every later event in the log belongs to the step most recently entered. The first is the graph's `entry` step; the last is a terminal step, which is where the session left the graph.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number — The turn the step was entered during, when it was entered inside one. Absent when the cursor moved between turns: an `action`, `message` or `variables` step needs no model call, so a chain of them can advance before the next turn begins.
            - `workflow` — string — The nested workflow (AgentWorkflow.nested) this step belongs to. Absent for a step of the main graph, which is how nesting is read off the stream — no separate enter/return events. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `stepId` — string **(required)** — Identifier of a step within its workflow, unique per workflow (the main graph and each nested workflow are separate scopes). Stable and machine-facing: transitions reference it, and a result step's id is the name a caller branches on, so renaming a step's `label` never unwires the graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `label` — string — The step's authored label, so a reader needs no copy of the agent definition to render the stream. _(minLen=1; maxLen=128)_
            - `stage` — string — The step's stage, as authored on it or inherited from upstream. Absent when the graph uses no stages. _(minLen=1; maxLen=64)_
            - `type` — string **(required)** — Which handler a step carries, reported on the session event stream (WorkflowStepEnteredEvent) and in traces. Mirrors the members of AgentWorkflowHandler and exists so a reader does not have to load the agent version snapshot to tell a stretch of conversation from a runtime action: a trace is read long after the fact, by an operator who has the session and not the definition it ran against. `conversation` is the only member that hands the turn to the model; which capability an `action` step performed is named by the invocation events that follow it. _(enum: `conversation`, `message`, `action`, `variables`, `workflow`, `result`, `end`)_
        - **`workflowTransition`**
          - `workflowTransition` — WorkflowTransitionEvent **(required)** — Emitted when a transition is taken, naming the exit and what decided it. Not emitted on a terminal step, which has no exits — a session that ended inside the graph is read from the last WorkflowStepEnteredEvent — and not emitted when a conversation step's conditions all stay false, which is the step simply continuing.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number — The turn the transition was evaluated in. Absent when the cursor moved between turns.
            - `workflow` — string — The nested workflow both steps belong to. Absent in the main graph; a transition never crosses graphs. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `stepId` — string **(required)** — Step being left. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `target` — string **(required)** — Step being entered. A WorkflowStepEnteredEvent for it follows. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `condition` — string **(required)** — Which kind of condition took a transition, as reported on the session event stream (WorkflowTransitionEvent) and in traces. Mirrors the members of AgentWorkflowCondition: `prompt` is the only one the model decides, every other was settled by the runtime with no model call. _(enum: `always`, `prompt`, `expression`, `result`, `failure`, `fallback`)_
            - `reason` — string — The model's one-line reason for the move, as it gave it to the steering tool. Present only for `prompt` conditions.
        - **`workflowMoveRefused`**
          - `workflowMoveRefused` — WorkflowMoveRefusedEvent **(required)** — Emitted when the model asks to move somewhere the live step does not declare as an exit. The runtime refuses, names the legal exits, and the session carries on from the same step, so this is not a failure of the turn: it is the record of what callers keep reaching for and the graph does not offer. Aggregated per step, it is the shortest route to the exit a graph is missing.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `workflow` — string — The nested workflow the live step belongs to. Absent in the main graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `stepId` — string **(required)** — The step the session stayed on. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `requested` — string **(required)** — What the model asked for, verbatim — not necessarily a step that exists.
            - `reason` — string — The model's stated reason for the move it was refused.
        - **`workflowVariablesWritten`**
          - `workflowVariablesWritten` — WorkflowVariablesWrittenEvent **(required)** — Emitted when workflow variables are written: a `variables` step's assignments, or an action step capturing its result into `output`. The only record of the state `expression` conditions branch on and handlebars resolve against, so replaying the log from index 0 reconstructs the same variables the runtime had.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number — The turn the write happened in, when it happened inside one.
            - `workflow` — string — The nested workflow the writing step belongs to. Absent in the main graph. Variables are shared with the main graph either way — a nested workflow has no scope of its own. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `stepId` — string **(required)** — Step that wrote them. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `values` — any **(required)** — The names written and their resolved values, as a JSON object. Only what this write touched, not the whole state; a variable cleared by an empty assignment is present with an empty value.
        - **`guardrailTripped`**
          - `guardrailTripped` — GuardrailTrippedEvent **(required)** — Emitted when a check trips, including when its action is `observe` and the turn proceeds untouched — that is what makes observe mode a way to tune a guardrail against real traffic rather than a switched-off check.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `check` — string **(required)** — The check's `name` in the agent definition. _(minLen=1; maxLen=64)_
            - `preset` — string — A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it. _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_
            - `confidence` — string **(required)** — How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM. _(enum: `low`, `medium`, `high`)_
            - `action` — string **(required)** — The action members by name, for reporting what actually ran. Session events carry this rather than AgentGuardrailAction because an event reports a decision, not a configuration. _(enum: `observe`, `redact`, `block`, `end`)_
            - `reason` — string — The checker's own account of why it tripped. Recorded for whoever tunes the guardrail, and never shown to the caller: telling someone which check caught them is a free oracle for the next attempt.
        - **`guardrailFailed`**
          - `guardrailFailed` — GuardrailFailedEvent **(required)** — Emitted when the checker itself errored or timed out. Carries the errorMode decision, so a reader can tell a turn that was screened and found clean from one that was never screened — without this event a fail-open guardrail would be indistinguishable from a guardrail that found nothing.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `errorMode` — string **(required)** — What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED. _(enum: `open`, `closed`)_
            - `proceeded` — boolean **(required)** — True when the turn was allowed through unscreened (`errorMode: open`), false when it was refused.
            - `reason` — string — Why the checker failed — a timeout, a provider error.
        - **`sandboxStarted`**
          - `sandboxStarted` — SandboxStartedEvent **(required)** — Emitted when the turn is attached to its sandbox, the first time a sandbox-backed tool is used in the turn. A session reuses one sandbox across turns whenever possible.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `sandboxId` — string **(required)** — Provider-side sandbox id, stable while the sandbox is reused across turns.
            - `resumed` — boolean **(required)** — True when an existing sandbox from a previous turn was reattached; false when a fresh sandbox was created.
        - **`sandboxFailed`**
          - `sandboxFailed` — SandboxFailedEvent **(required)** — Emitted when acquiring the sandbox fails; the turn then fails with the same cause. Provides sandbox-level observability distinct from the generic TurnFailedEvent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `message` — string **(required)**
        - **`artifactShared`**
          - `artifactShared` — ArtifactSharedEvent **(required)** — Emitted when the agent shares an artifact via the `share_artifact` tool, after the revision has been uploaded. Carries the file list and card metadata; the viewer reads content URLs and sharing from the wilma-artifacts service. Sharing the same artifact again publishes a new `revision` under the same `artifactId` and emits this event again.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `artifactId` — string **(required)** — Id of the registered artifact; fetch it via wilma-artifacts (GetArtifact, GetArtifactContentUrl, DownloadArtifact). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
            - `title` — string **(required)** — Human-readable title shown to the user.
            - `description` — string — One-line summary shown under the title.
            - `name` — string — Download filename shown to the user. _(minLen=1; maxLen=1024)_
            - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
            - `files` — array **(required)** — Files in this revision, with their paths, sizes and MIME types. _(minItems=1; maxItems=500)_
              - _array of_ `ArtifactFile`
                - _(nesting depth limit — see `ArtifactFile` in the Schemas appendix)_
            - `entry` — string — Path of the file the viewer opens first. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
            - `revision` — number — Revision this event published: 1 for a new artifact, higher when the agent republished it in place.
            - `path` — string — Sandbox path the artifact was shared from: the file, or the folder a bundle's paths are relative to, e.g. `/workspace/report.md` or `/workspace/site`.
            - `callId` — string — Id of the `share_artifact` tool call that produced the artifact.
        - **`compactionStarted`**
          - `compactionStarted` — CompactionStartedEvent **(required)** — Emitted before a turn when the conversation history exceeds the model context budget and is being summarized. The turn starts after CompactionCompletedEvent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
        - **`compactionCompleted`**
          - `compactionCompleted` — CompactionCompletedEvent **(required)** — Emitted when history compaction finishes and the turn proceeds with the summarized history.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
  - `nextStartIndex` — number — Present when more events exist; pass it as `startIndex` of the next call.
- Errors: `400`, `403`, `404`

#### `GET` `/v2/workflows/tasks/items/{taskId}/events/stream`

Replays and tails task events as Server-Sent Events (`text/event-stream`). Each frame carries one WorkflowTaskEvent: `id:` is the event index, `event:` is the union member name, and `data:` is the JSON document of the union value. Reconnect by passing the last seen index + 1 as `startIndex`. The stream ends after the task reaches a terminal status; for finished tasks the recorded events are replayed and the stream closes.

- operationId: `StreamTaskEvents`
- **Scopes**: `wilma-workflows:StreamTaskEvents`, `wilma-workflows:read`
- **Parameters**
  - `taskId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `startIndex` (query) — number — Replay recorded events with `index >= startIndex` before tailing live ones. Defaults to 0. _(min=0)_
- **Response 200** (`StreamTaskEventsOutputPayload`)
  - string
- Errors: `400`, `403`, `404`

#### `POST` `/v2/workflows/tasks/items/{taskId}/stop`

Requests cancellation of a pending or running task.

- operationId: `StopTask`
- **Scopes**: `wilma-workflows:StopTask`
- **Parameters**
  - `taskId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 202** (`StopTaskResponseContent`)
  - `taskId` — string **(required)** _(minLen=1; maxLen=128)_
  - `accepted` — boolean **(required)**
- Errors: `400`, `403`, `404`

#### `POST` `/v2/workflows/tasks/run`

Runs a task and blocks until it finishes, for callers that only need the end result —
    optionally structured via `schema`. Blocks up to `waitSeconds` (default 60, max 120);
    when the task has not finished in time the call still succeeds with a non-terminal
    `status` and the caller falls back to polling GetTask or streaming StreamTaskEvents with
    the returned handle.

- operationId: `RunTask`
- **Scopes**: `wilma-workflows:RunTask`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `RunTaskRequestContent`) **(required)**
  - `user` — string — The user the task runs on behalf of. Optional: tasks are company-scoped by default; set it when the task should act with a user's data access. _(minLen=12; maxLen=12)_
  - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
  - `agentVersion` — number — Published agent version to run. Mutually exclusive with agentDraft. When neither is set, the agent's deployment configuration selects the version. _(min=1)_
  - `agentDraft` — boolean — Run the agent's current draft (for testing). Mutually exclusive with agentVersion.
  - `input` — string **(required)** — The instructions / input handed to the agent for this task. _(minLen=1; maxLen=100000)_
  - `context` — array — Additional context documents made available to the agent.
    - _array of_ `any`
  - `mentions` — array — Resources the agent reads as context, resolved with the task user's permissions, or company-wide when the task has no user. _(maxItems=20)_
    - _array of_ `Mention`
      - _oneOf_ — exactly one of:
        - **`reference`**
          - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
            - `uri` — string **(required)** — Canonical URI identifying one entity on the Wilma platform, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://skills/aB3dE5fG7hJ9'. The path names the owning service and entity kind. Opaque to the contracts that carry it; non-Wilma schemes (records of external systems) fit the same shape. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
            - `label` — string — Display name of the mention chip. The model sees it only to name a mention that could not be read or was removed. _(maxLen=256)_
  - `schema` — any — JSON Schema the final output must conform to. When set, the agent's final answer is produced and validated as a structured document, returned in `result.structured`; `result.text` still carries the plain final answer.
  - `options` — any
  - `source` — TaskSource — Where a task was started from, when not started directly over the API by an administrator. Set by the integrating service so the task can be tied back to the driving resource; tasks started by an automation carry `automationId` on the task itself.
    - `uri` — string **(required)** — Canonical URI of the driving resource, e.g. 'wilma://copilot/assets/{assetId}' for a copilot asset background job. Supplied by the integrating service and opaque to this one: used to route and group, never to authorize. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
    - `metadata` — any — Additional integration-specific context.
  - `waitSeconds` — number — Maximum seconds to block waiting for the task to finish. Defaults to 60. _(min=1; max=120)_
- **Response 200** (`RunTaskResponseContent`)
  - `taskId` — string **(required)** _(minLen=1; maxLen=128)_
  - `startIndex` — number **(required)**
  - `traceId` — string — Trace recording this task in wilma-traces — the agent's steps, its model calls and the tools it ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to StreamTaskEvents. This is the id to quote when reporting what an automation did: a task started by a firing trigger has no interactive caller watching it, and RunAutomation returns this handle and nothing else. The trace row is written once the task's first step completes, so GetTrace reports NotFound while the task is still `pending`. _(minLen=1; maxLen=128)_
  - `status` — string **(required)** _(enum: `pending`, `running`, `completed`, `failed`, `stopped`)_
  - `result` — TaskResult — Final result of a completed task. `structured` is present when the task was started with a `schema`: the agent's final output parsed and validated against that schema. `text` always carries the plain final answer.
    - `text` — string — Final answer as plain text; present with or without a schema, so a caller can check `structured` against what the agent actually said.
    - `structured` — any — Schema-validated structured output; present when the task was started with a schema.
  - `error` — TaskError
    - `code` — string **(required)** — Stable machine-readable error code.
    - `message` — string **(required)**
- Errors: `400`, `403`, `503`

### Schemas appendix — Wilma Workflows API

<details><summary>96 component schemas</summary>

**`Actor`**

_Who performed an action: an interactive user, an API key or an internal service._

- `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
- `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
- `name` — string — Human readable name of the actor at the time of the action.

**`ActorType`**

- string _(enum: `user`, `api_key`, `service`)_

**`AgentGuardrailActionType`**

_The action members by name, for reporting what actually ran. Session events carry this rather than AgentGuardrailAction because an event reports a decision, not a configuration._

- string _(enum: `observe`, `redact`, `block`, `end`)_

**`AgentGuardrailErrorMode`**

_What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED._

- string _(enum: `open`, `closed`)_

**`AgentGuardrailPreset`**

_A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it._

- string _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_

**`AgentGuardrailSensitivity`**

_How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM._

- string _(enum: `low`, `medium`, `high`)_

**`AgentWorkflowConditionType`**

_Which kind of condition took a transition, as reported on the session event stream (WorkflowTransitionEvent) and in traces. Mirrors the members of AgentWorkflowCondition: `prompt` is the only one the model decides, every other was settled by the runtime with no model call._

- string _(enum: `always`, `prompt`, `expression`, `result`, `failure`, `fallback`)_

**`AgentWorkflowStepType`**

_Which handler a step carries, reported on the session event stream (WorkflowStepEnteredEvent) and in traces. Mirrors the members of AgentWorkflowHandler and exists so a reader does not have to load the agent version snapshot to tell a stretch of conversation from a runtime action: a trace is read long after the fact, by an operator who has the session and not the definition it ran against. `conversation` is the only member that hands the turn to the model; which capability an `action` step performed is named by the invocation events that follow it._

- string _(enum: `conversation`, `message`, `action`, `variables`, `workflow`, `result`, `end`)_

**`ArtifactFile`**

_A file available for preview or download: the single file of an artifact, or an entry inside its archive._

- `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
- `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
- `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.

**`ArtifactKind`**

_Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest._

- string _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_

**`ArtifactSharedEvent`**

_Emitted when the agent shares an artifact via the `share_artifact` tool, after the revision has been uploaded. Carries the file list and card metadata; the viewer reads content URLs and sharing from the wilma-artifacts service. Sharing the same artifact again publishes a new `revision` under the same `artifactId` and emits this event again._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `artifactId` — string **(required)** — Id of the registered artifact; fetch it via wilma-artifacts (GetArtifact, GetArtifactContentUrl, DownloadArtifact). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
- `title` — string **(required)** — Human-readable title shown to the user.
- `description` — string — One-line summary shown under the title.
- `name` — string — Download filename shown to the user. _(minLen=1; maxLen=1024)_
- `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
- `files` — array **(required)** — Files in this revision, with their paths, sizes and MIME types. _(minItems=1; maxItems=500)_
  - _array of_ `ArtifactFile`
    - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
    - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
    - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
- `entry` — string — Path of the file the viewer opens first. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
- `revision` — number — Revision this event published: 1 for a new artifact, higher when the agent republished it in place.
- `path` — string — Sandbox path the artifact was shared from: the file, or the folder a bundle's paths are relative to, e.g. `/workspace/report.md` or `/workspace/site`.
- `callId` — string — Id of the `share_artifact` tool call that produced the artifact.

**`Attachment`**

_An input file supplied with session input and included with a user message. Content lives in object storage; download via the owning channel's Attachments API. `contentType`, `size` and `thumbnailUrl` describe the stored content and are therefore absent until the upload has completed._

- `id` — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
- `name` — string **(required)** — Filename shown to the user. Characters storage cannot represent are replaced with underscores. _(minLen=1; maxLen=255)_
- `contentType` — string — MIME type recorded by storage from the uploaded content, e.g. 'application/pdf'. Absent until the upload completes.
- `size` — number — Size in bytes recorded by storage from the uploaded content. Absent until the upload completes.
- `thumbnailUrl` — string — URL of a generated preview image, for rendering a thumbnail without downloading the file. Best-effort: absent until the upload completes, and for content no preview can be generated from.
- `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`Automation`**

_A configured automation. Tasks it started are listed via ListTasks with `automationId`._

- `name` — string **(required)** _(minLen=1; maxLen=256)_
- `description` — string
- `enabled` — boolean — Disabled automations keep their configuration but never fire. Defaults to true.
- `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`schedule`**
      - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
        - `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
        - `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.
    - **`event`**
      - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
        - `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
        - `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
        - `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.
    - **`webhook`**
      - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
- `task` — AutomationTaskTemplate **(required)** — The task an automation starts when it fires.
  - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
  - `options` — any
- `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.
- `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.
- `id` — string **(required)** _(minLen=1; maxLen=128)_
- `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.

**`AutomationEventTrigger`**

_Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload._

- `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
- `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
- `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.

**`AutomationInfo`**

_Summary entry returned by ListAutomations._

- `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.
- `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.
- `id` — string **(required)** _(minLen=1; maxLen=128)_
- `name` — string **(required)**
- `description` — string
- `enabled` — boolean
- `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`schedule`**
      - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
        - `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
        - `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.
    - **`event`**
      - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
        - `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
        - `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
        - `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.
    - **`webhook`**
      - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.

**`AutomationScheduleTrigger`**

_Fires on a cron schedule._

- `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
- `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.

**`AutomationTaskTemplate`**

_The task an automation starts when it fires._

- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `options` — any

**`AutomationTrigger`**

_What causes the automation to fire. Exactly one member is set._

- _oneOf_ — exactly one of:
  - **`schedule`**
    - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
      - `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
      - `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.
  - **`event`**
    - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
      - `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
      - `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
      - `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.
  - **`webhook`**
    - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.

**`AutomationWebhookTrigger`**

_Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth._

- AutomationWebhookTrigger

**`CompactionCompletedEvent`**

_Emitted when history compaction finishes and the turn proceeds with the summarized history._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**

**`CompactionStartedEvent`**

_Emitted before a turn when the conversation history exceeds the model context budget and is being summarized. The turn starts after CompactionCompletedEvent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**

**`ConflictExceptionResponseContent`**

_The request conflicts with the current state of the resource, e.g. a duplicate name, a resource still in use, or an unmet precondition._

- `message` — string **(required)**

**`CreateAutomationRequestContent`**

_The editable definition of an automation._

- `name` — string **(required)** _(minLen=1; maxLen=256)_
- `description` — string
- `enabled` — boolean — Disabled automations keep their configuration but never fire. Defaults to true.
- `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`schedule`**
      - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
        - `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
        - `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.
    - **`event`**
      - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
        - `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
        - `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
        - `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.
    - **`webhook`**
      - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
- `task` — AutomationTaskTemplate **(required)** — The task an automation starts when it fires.
  - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
  - `options` — any

**`CreateAutomationResponseContent`**

- `automation` — Automation **(required)** — A configured automation. Tasks it started are listed via ListTasks with `automationId`.
  - `name` — string **(required)** _(minLen=1; maxLen=256)_
  - `description` — string
  - `enabled` — boolean — Disabled automations keep their configuration but never fire. Defaults to true.
  - `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`schedule`**
        - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
          - _(nesting depth limit — see `AutomationScheduleTrigger` in the Schemas appendix)_
      - **`event`**
        - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
          - _(nesting depth limit — see `AutomationEventTrigger` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
  - `task` — AutomationTaskTemplate **(required)** — The task an automation starts when it fires.
    - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
    - `options` — any
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `id` — string **(required)** _(minLen=1; maxLen=128)_
  - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetAutomationResponseContent`**

- `automation` — Automation **(required)** — A configured automation. Tasks it started are listed via ListTasks with `automationId`.
  - `name` — string **(required)** _(minLen=1; maxLen=256)_
  - `description` — string
  - `enabled` — boolean — Disabled automations keep their configuration but never fire. Defaults to true.
  - `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`schedule`**
        - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
          - _(nesting depth limit — see `AutomationScheduleTrigger` in the Schemas appendix)_
      - **`event`**
        - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
          - _(nesting depth limit — see `AutomationEventTrigger` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
  - `task` — AutomationTaskTemplate **(required)** — The task an automation starts when it fires.
    - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
    - `options` — any
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `id` — string **(required)** _(minLen=1; maxLen=128)_
  - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.

**`GetAutomationWebhookUrlResponseContent`**

- `webhookUrl` — string **(required)** — The ingestion URL external integrations POST payloads to, including the secret token.

**`GetTaskEventsResponseContent`**

- `events` — array **(required)**
  - _array of_ `WorkflowTaskEvent`
    - _oneOf_ — exactly one of:
      - **`sessionStarted`**
        - `sessionStarted` — SessionStartedEvent **(required)** — Emitted once as the very first event of a session, when it is created. Confirms the session id and the agent the session is bound to.
          - _(nesting depth limit — see `SessionStartedEvent` in the Schemas appendix)_
      - **`sessionIdle`**
        - `sessionIdle` — SessionIdleEvent **(required)** — Terminal event of a successful turn: the session is idle and ready for the next turn.
          - _(nesting depth limit — see `SessionIdleEvent` in the Schemas appendix)_
      - **`sessionStopped`**
        - `sessionStopped` — SessionStoppedEvent **(required)** — Terminal event emitted when the active turn was cancelled via the channel's stop operation.
          - _(nesting depth limit — see `SessionStoppedEvent` in the Schemas appendix)_
      - **`sessionTerminated`**
        - `sessionTerminated` — SessionTerminatedEvent **(required)** — Terminal event emitted when the platform ended the session rather than let it continue: the session is in `terminated` status. Distinct from SessionStoppedEvent, which records a user or operator asking to stop — folding the two together would leave a refused session indistinguishable from a clean finish in every completion-rate report. On voice the call is hung up as this is emitted; on the other channels there is nothing to hang up and termination is the status alone — history is kept, and the session simply accepts no further turns.
          - _(nesting depth limit — see `SessionTerminatedEvent` in the Schemas appendix)_
      - **`sessionFailed`**
        - `sessionFailed` — SessionFailedEvent **(required)** — Terminal event emitted after TurnFailedEvent: the session is in `failed` status. A new turn starts from the last consistent snapshot.
          - _(nesting depth limit — see `SessionFailedEvent` in the Schemas appendix)_
      - **`turnStarted`**
        - `turnStarted` — TurnStartedEvent **(required)** — Emitted when a turn begins executing. All subsequent events up to the matching TurnCompletedEvent/TurnFailedEvent belong to this turn.
          - _(nesting depth limit — see `TurnStartedEvent` in the Schemas appendix)_
      - **`turnCompleted`**
        - `turnCompleted` — TurnCompletedEvent **(required)** — Emitted when a turn finishes successfully, with aggregate token usage for the turn. Followed by SessionIdleEvent.
          - _(nesting depth limit — see `TurnCompletedEvent` in the Schemas appendix)_
      - **`turnFailed`**
        - `turnFailed` — TurnFailedEvent **(required)** — Emitted when a turn fails with an unrecoverable error. Followed by SessionFailedEvent.
          - _(nesting depth limit — see `TurnFailedEvent` in the Schemas appendix)_
      - **`messageReceived`**
        - `messageReceived` — MessageReceivedEvent **(required)** — Emitted right after TurnStartedEvent with the user message that triggered the turn, so a reconnecting client can render the conversation without a separate history fetch.
          - _(nesting depth limit — see `MessageReceivedEvent` in the Schemas appendix)_
      - **`messageAppended`**
        - `messageAppended` — MessageAppendedEvent **(required)** — Emitted for every assistant text token chunk. High frequency; drives live rendering of the reply.
          - _(nesting depth limit — see `MessageAppendedEvent` in the Schemas appendix)_
      - **`messageCompleted`**
        - `messageCompleted` — MessageCompletedEvent **(required)** — Emitted once per step when the assistant message text is complete.
          - _(nesting depth limit — see `MessageCompletedEvent` in the Schemas appendix)_
      - **`stepStarted`**
        - `stepStarted` — StepStartedEvent **(required)** — Emitted each time the model starts a new inference step within a turn (a turn spans multiple steps when the model calls tools).
          - _(nesting depth limit — see `StepStartedEvent` in the Schemas appendix)_
      - **`stepCompleted`**
        - `stepCompleted` — StepCompletedEvent **(required)** — Emitted when an inference step finishes, with token usage for the step when the provider reports it.
          - _(nesting depth limit — see `StepCompletedEvent` in the Schemas appendix)_
      - **`reasoningDelta`**
        - `reasoningDelta` — ReasoningDeltaEvent **(required)** — Emitted for every reasoning (thinking) token chunk the model produces, when the selected model exposes reasoning. High frequency; intended for live typing indicators.
          - _(nesting depth limit — see `ReasoningDeltaEvent` in the Schemas appendix)_
      - **`reasoningCompleted`**
        - `reasoningCompleted` — ReasoningCompletedEvent **(required)** — Emitted once per step after the model finishes its reasoning block, carrying the complete reasoning text.
          - _(nesting depth limit — see `ReasoningCompletedEvent` in the Schemas appendix)_
      - **`invocationStarted`**
        - `invocationStarted` — InvocationStartedEvent **(required)** — Emitted when the model begins one tool invocation, before its input is complete. Every invocation starts here, regardless of how it is fulfilled or whether it suspends the turn. Carries the routing facts needed to render it — who fulfils it, whether the turn suspends, where to surface it, whether the input streams — so a client holding no tool registry (a replay, a shared session, an inspector) still renders correctly.
          - _(nesting depth limit — see `InvocationStartedEvent` in the Schemas appendix)_
      - **`invocationDelta`**
        - `invocationDelta` — InvocationDeltaEvent **(required)** — Emitted for each fragment of an invocation's input as the model writes it, when the tool opted into streamed input. The payload is raw partial JSON text exactly as the model emits it; clients parse it incrementally to render an invocation whose input is itself content — a drafted email, a chart spec, a shared document — while it is being written. High frequency.
          - _(nesting depth limit — see `InvocationDeltaEvent` in the Schemas appendix)_
      - **`invocationInputCompleted`**
        - `invocationInputCompleted` — InvocationInputCompletedEvent **(required)** — Emitted once per invocation when its input is complete and parsed. Always emitted, whether or not the input streamed.
          - _(nesting depth limit — see `InvocationInputCompletedEvent` in the Schemas appendix)_
      - **`invocationResult`**
        - `invocationResult` — InvocationResultEvent **(required)** — Emitted when an invocation is resolved, however that happened: a server tool finishing, a caller returning a client tool's result on resume, a person answering a question or ruling on an approval, or the runtime supplying a `synthetic` tool's result. Emitted for every invocation without exception, so replaying the log from index 0 reconstructs the same state as watching it live.
          - _(nesting depth limit — see `InvocationResultEvent` in the Schemas appendix)_
      - **`taskStarted`**
        - `taskStarted` — TaskStartedEvent **(required)** — Emitted when the agent delegates a subtask to a task execution: the `delegate` tool or an agent-call capability. Events emitted inside the task are re-published on the session stream with `origin` set to this task, until the matching TaskCompletedEvent.
          - _(nesting depth limit — see `TaskStartedEvent` in the Schemas appendix)_
      - **`taskCompleted`**
        - `taskCompleted` — TaskCompletedEvent **(required)** — Emitted when a delegated task execution finishes, carrying its final answer as returned to the parent agent.
          - _(nesting depth limit — see `TaskCompletedEvent` in the Schemas appendix)_
      - **`workflowStepEntered`**
        - `workflowStepEntered` — WorkflowStepEnteredEvent **(required)** — Emitted when the workflow cursor arrives at a step, before the step runs — so every later event in the log belongs to the step most recently entered. The first is the graph's `entry` step; the last is a terminal step, which is where the session left the graph.
          - _(nesting depth limit — see `WorkflowStepEnteredEvent` in the Schemas appendix)_
      - **`workflowTransition`**
        - `workflowTransition` — WorkflowTransitionEvent **(required)** — Emitted when a transition is taken, naming the exit and what decided it. Not emitted on a terminal step, which has no exits — a session that ended inside the graph is read from the last WorkflowStepEnteredEvent — and not emitted when a conversation step's conditions all stay false, which is the step simply continuing.
          - _(nesting depth limit — see `WorkflowTransitionEvent` in the Schemas appendix)_
      - **`workflowMoveRefused`**
        - `workflowMoveRefused` — WorkflowMoveRefusedEvent **(required)** — Emitted when the model asks to move somewhere the live step does not declare as an exit. The runtime refuses, names the legal exits, and the session carries on from the same step, so this is not a failure of the turn: it is the record of what callers keep reaching for and the graph does not offer. Aggregated per step, it is the shortest route to the exit a graph is missing.
          - _(nesting depth limit — see `WorkflowMoveRefusedEvent` in the Schemas appendix)_
      - **`workflowVariablesWritten`**
        - `workflowVariablesWritten` — WorkflowVariablesWrittenEvent **(required)** — Emitted when workflow variables are written: a `variables` step's assignments, or an action step capturing its result into `output`. The only record of the state `expression` conditions branch on and handlebars resolve against, so replaying the log from index 0 reconstructs the same variables the runtime had.
          - _(nesting depth limit — see `WorkflowVariablesWrittenEvent` in the Schemas appendix)_
      - **`guardrailTripped`**
        - `guardrailTripped` — GuardrailTrippedEvent **(required)** — Emitted when a check trips, including when its action is `observe` and the turn proceeds untouched — that is what makes observe mode a way to tune a guardrail against real traffic rather than a switched-off check.
          - _(nesting depth limit — see `GuardrailTrippedEvent` in the Schemas appendix)_
      - **`guardrailFailed`**
        - `guardrailFailed` — GuardrailFailedEvent **(required)** — Emitted when the checker itself errored or timed out. Carries the errorMode decision, so a reader can tell a turn that was screened and found clean from one that was never screened — without this event a fail-open guardrail would be indistinguishable from a guardrail that found nothing.
          - _(nesting depth limit — see `GuardrailFailedEvent` in the Schemas appendix)_
      - **`sandboxStarted`**
        - `sandboxStarted` — SandboxStartedEvent **(required)** — Emitted when the turn is attached to its sandbox, the first time a sandbox-backed tool is used in the turn. A session reuses one sandbox across turns whenever possible.
          - _(nesting depth limit — see `SandboxStartedEvent` in the Schemas appendix)_
      - **`sandboxFailed`**
        - `sandboxFailed` — SandboxFailedEvent **(required)** — Emitted when acquiring the sandbox fails; the turn then fails with the same cause. Provides sandbox-level observability distinct from the generic TurnFailedEvent.
          - _(nesting depth limit — see `SandboxFailedEvent` in the Schemas appendix)_
      - **`artifactShared`**
        - `artifactShared` — ArtifactSharedEvent **(required)** — Emitted when the agent shares an artifact via the `share_artifact` tool, after the revision has been uploaded. Carries the file list and card metadata; the viewer reads content URLs and sharing from the wilma-artifacts service. Sharing the same artifact again publishes a new `revision` under the same `artifactId` and emits this event again.
          - _(nesting depth limit — see `ArtifactSharedEvent` in the Schemas appendix)_
      - **`compactionStarted`**
        - `compactionStarted` — CompactionStartedEvent **(required)** — Emitted before a turn when the conversation history exceeds the model context budget and is being summarized. The turn starts after CompactionCompletedEvent.
          - _(nesting depth limit — see `CompactionStartedEvent` in the Schemas appendix)_
      - **`compactionCompleted`**
        - `compactionCompleted` — CompactionCompletedEvent **(required)** — Emitted when history compaction finishes and the turn proceeds with the summarized history.
          - _(nesting depth limit — see `CompactionCompletedEvent` in the Schemas appendix)_
- `nextStartIndex` — number — Present when more events exist; pass it as `startIndex` of the next call.

**`GetTaskResponseContent`**

- `task` — Task **(required)** — A background execution of a workflow-channel agent.
  - `id` — string **(required)** _(minLen=1; maxLen=128)_
  - `status` — string **(required)** _(enum: `pending`, `running`, `completed`, `failed`, `stopped`)_
  - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
  - `agentVersion` — number — Published agent version serving this task, selected at start. _(min=1)_
  - `agentDraft` — boolean — True when the task runs the agent's mutable draft.
  - `traceId` — string — Trace recording this task in wilma-traces — the agent's steps, its model calls and the tools it ran, including the failure behind `error` when `status` is `failed`. Read it with the wilma-traces GetTrace operation. Names the task's own trace. Each tool call, skill load and sandbox the task made is recorded as a trace of its own; list them with QueryTraces filtered by `session.traceId`. Reported from the moment the task is accepted, matching the handle StartTask returned, but the trace row is written when the first step completes — so GetTrace reports NotFound while the task is still `pending`. Absent when the task's trace is not the caller's to read, as when a Wildix built-in agent serves it. _(minLen=1; maxLen=128)_
  - `automationId` — string — Automation whose firing started this task; absent for tasks started over the API. _(minLen=1; maxLen=128)_
  - `model` — string — Effective model resolved at start (after 'default' resolution).
  - `source` — TaskSource — Where a task was started from, when not started directly over the API by an administrator. Set by the integrating service so the task can be tied back to the driving resource; tasks started by an automation carry `automationId` on the task itself.
    - `uri` — string **(required)** — Canonical URI of the driving resource, e.g. 'wilma://copilot/assets/{assetId}' for a copilot asset background job. Supplied by the integrating service and opaque to this one: used to route and group, never to authorize. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
    - `metadata` — any — Additional integration-specific context.
  - `schema` — any — JSON Schema the final output was requested to conform to; echoed from StartTask/RunTask.
  - `result` — TaskResult — Final result of a completed task. `structured` is present when the task was started with a `schema`: the agent's final output parsed and validated against that schema. `text` always carries the plain final answer.
    - `text` — string — Final answer as plain text; present with or without a schema, so a caller can check `structured` against what the agent actually said.
    - `structured` — any — Schema-validated structured output; present when the task was started with a schema.
  - `error` — TaskError
    - `code` — string **(required)** — Stable machine-readable error code.
    - `message` — string **(required)**
  - `usage` — SessionUsage
    - `inputTokens` — number
    - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
    - `outputTokens` — number
    - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
    - `totalTokens` — number
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `startedAt` — string — Time execution started; absent while pending.
  - `completedAt` — string — Time the task reached a terminal status.
  - `eventCount` — number **(required)**

**`GuardrailFailedEvent`**

_Emitted when the checker itself errored or timed out. Carries the errorMode decision, so a reader can tell a turn that was screened and found clean from one that was never screened — without this event a fail-open guardrail would be indistinguishable from a guardrail that found nothing._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `errorMode` — string **(required)** — What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED. _(enum: `open`, `closed`)_
- `proceeded` — boolean **(required)** — True when the turn was allowed through unscreened (`errorMode: open`), false when it was refused.
- `reason` — string — Why the checker failed — a timeout, a provider error.

**`GuardrailTrippedEvent`**

_Emitted when a check trips, including when its action is `observe` and the turn proceeds untouched — that is what makes observe mode a way to tune a guardrail against real traffic rather than a switched-off check._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `check` — string **(required)** — The check's `name` in the agent definition. _(minLen=1; maxLen=64)_
- `preset` — string — A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it. _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_
- `confidence` — string **(required)** — How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM. _(enum: `low`, `medium`, `high`)_
- `action` — string **(required)** — The action members by name, for reporting what actually ran. Session events carry this rather than AgentGuardrailAction because an event reports a decision, not a configuration. _(enum: `observe`, `redact`, `block`, `end`)_
- `reason` — string — The checker's own account of why it tripped. Recorded for whoever tunes the guardrail, and never shown to the caller: telling someone which check caught them is a free oracle for the next attempt.

**`IngestAutomationWebhookInputPayload`**

_The webhook payload. Attached to the started task's context._

- any

**`IngestAutomationWebhookResponseContent`**

- `fired` — boolean **(required)** — True when the automation was enabled, so a task was started.
- `taskId` — string — The started task, present when `fired` is true. _(minLen=1; maxLen=128)_

**`InvocationDeltaEvent`**

_Emitted for each fragment of an invocation's input as the model writes it, when the tool opted into streamed input. The payload is raw partial JSON text exactly as the model emits it; clients parse it incrementally to render an invocation whose input is itself content — a drafted email, a chart spec, a shared document — while it is being written. High frequency._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `callId` — string **(required)**
- `delta` — string **(required)** — The new fragment of raw JSON input text.
- `soFar` — string **(required)** — The raw JSON input text accumulated so far in this invocation, so late subscribers need not replay every delta. Being a prefix, it is not necessarily valid JSON on its own.

**`InvocationInputCompletedEvent`**

_Emitted once per invocation when its input is complete and parsed. Always emitted, whether or not the input streamed._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `callId` — string **(required)**
- `input` — any **(required)**

**`InvocationResultEvent`**

_Emitted when an invocation is resolved, however that happened: a server tool finishing, a caller returning a client tool's result on resume, a person answering a question or ruling on an approval, or the runtime supplying a `synthetic` tool's result. Emitted for every invocation without exception, so replaying the log from index 0 reconstructs the same state as watching it live._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `callId` — string **(required)** — Id of the invocation this result answers, matching an InvocationStartedEvent.
- `toolName` — string **(required)**
- `toolId` — string — The wilma-tools Tool that executed, echoed from InvocationStartedEvent. Absent for invocations that are not backed by a shared Tool. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `toolVersion` — number — Published tool version that executed, when `toolId` is set. _(min=1)_
- `status` — string **(required)** _(enum: `completed`, `failed`)_
- `resolvedBy` — string **(required)** — Who supplied the result recorded by an InvocationResultEvent. _(enum: `server`, `client`, `user`)_
- `output` — any
- `error` — string — Present when status is `failed`.

**`InvocationStartedEvent`**

_Emitted when the model begins one tool invocation, before its input is complete. Every invocation starts here, regardless of how it is fulfilled or whether it suspends the turn. Carries the routing facts needed to render it — who fulfils it, whether the turn suspends, where to surface it, whether the input streams — so a client holding no tool registry (a replay, a shared session, an inspector) still renders correctly._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `callId` — string **(required)** — Stable id of this invocation, referenced by every later event about it.
- `toolName` — string **(required)**
- `toolId` — string — The wilma-tools Tool backing this invocation. Absent for built-in tools, connector meta-tools and other capabilities that are not shared Tools. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `toolVersion` — number — Published tool version the model was offered, when `toolId` is set. Records which input schema the invocation was written against. _(min=1)_
- `fulfilment` — string **(required)** — Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend. _(enum: `server`, `client`, `synthetic`)_
- `gate` — string **(required)** — Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation). _(enum: `none`, `result`, `decision`)_
- `surface` — string **(required)** — Where a client should surface an invocation. Affects placement only, never behaviour. _(enum: `hidden`, `activity`, `content`)_
- `stream` — boolean **(required)** — True when the input arrives as InvocationDeltaEvent chunks ahead of InvocationInputCompletedEvent. Opt-in per tool, so tools with small inputs cost nothing.

**`ListAutomationsResponseContent`**

- `automations` — array **(required)**
  - _array of_ `AutomationInfo`
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `name` — string **(required)**
    - `description` — string
    - `enabled` — boolean
    - `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`schedule`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`event`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webhook`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListSubscriptionsResponseContent`**

_The answer to 'what should I send you': one entry per tenant that needs anything at all, and every tenant in one response — the producer holds a single routing table, and a listing it has to assemble from several requests is one that can be applied half-built, which is indistinguishable from a set of tenants that unsubscribed. A tenant absent from the listing needs nothing, and the producer sends it nothing. Ordering is unspecified._

- `subscriptions` — array **(required)**
  - _array of_ `Subscription`
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `selectors` — array **(required)** — Event types one tenant needs, deduplicated across everything that asked for them. Two selectors never name the same event type. The producer sends every occurrence of each listed type. _(minItems=1; maxItems=200)_
      - _array of_ `SubscriptionSelector`
        - _(nesting depth limit — see `SubscriptionSelector` in the Schemas appendix)_

**`ListTasksResponseContent`**

- `tasks` — array **(required)**
  - _array of_ `Task`
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `status` — string **(required)** _(enum: `pending`, `running`, `completed`, `failed`, `stopped`)_
    - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
    - `agentVersion` — number — Published agent version serving this task, selected at start. _(min=1)_
    - `agentDraft` — boolean — True when the task runs the agent's mutable draft.
    - `traceId` — string — Trace recording this task in wilma-traces — the agent's steps, its model calls and the tools it ran, including the failure behind `error` when `status` is `failed`. Read it with the wilma-traces GetTrace operation. Names the task's own trace. Each tool call, skill load and sandbox the task made is recorded as a trace of its own; list them with QueryTraces filtered by `session.traceId`. Reported from the moment the task is accepted, matching the handle StartTask returned, but the trace row is written when the first step completes — so GetTrace reports NotFound while the task is still `pending`. Absent when the task's trace is not the caller's to read, as when a Wildix built-in agent serves it. _(minLen=1; maxLen=128)_
    - `automationId` — string — Automation whose firing started this task; absent for tasks started over the API. _(minLen=1; maxLen=128)_
    - `model` — string — Effective model resolved at start (after 'default' resolution).
    - `source` — TaskSource — Where a task was started from, when not started directly over the API by an administrator. Set by the integrating service so the task can be tied back to the driving resource; tasks started by an automation carry `automationId` on the task itself.
      - `uri` — string **(required)** — Canonical URI of the driving resource, e.g. 'wilma://copilot/assets/{assetId}' for a copilot asset background job. Supplied by the integrating service and opaque to this one: used to route and group, never to authorize. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
      - `metadata` — any — Additional integration-specific context.
    - `schema` — any — JSON Schema the final output was requested to conform to; echoed from StartTask/RunTask.
    - `result` — TaskResult — Final result of a completed task. `structured` is present when the task was started with a `schema`: the agent's final output parsed and validated against that schema. `text` always carries the plain final answer.
      - `text` — string — Final answer as plain text; present with or without a schema, so a caller can check `structured` against what the agent actually said.
      - `structured` — any — Schema-validated structured output; present when the task was started with a schema.
    - `error` — TaskError
      - `code` — string **(required)** — Stable machine-readable error code.
      - `message` — string **(required)**
    - `usage` — SessionUsage
      - `inputTokens` — number
      - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
      - `outputTokens` — number
      - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
      - `totalTokens` — number
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `startedAt` — string — Time execution started; absent while pending.
    - `completedAt` — string — Time the task reached a terminal status.
    - `eventCount` — number **(required)**
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`Mention`**

_Something attached to a message as agent context. A union, so a new kind of context is a new member rather than a change to every operation that carries mentions._

- _oneOf_ — exactly one of:
  - **`reference`**
    - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
      - `uri` — string **(required)** — Canonical URI identifying one entity on the Wilma platform, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://skills/aB3dE5fG7hJ9'. The path names the owning service and entity kind. Opaque to the contracts that carry it; non-Wilma schemes (records of external systems) fit the same shape. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
      - `label` — string — Display name of the mention chip. The model sees it only to name a mention that could not be read or was removed. _(maxLen=256)_

**`MentionReference`**

_A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself._

- `uri` — string **(required)** — Canonical URI identifying one entity on the Wilma platform, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://skills/aB3dE5fG7hJ9'. The path names the owning service and entity kind. Opaque to the contracts that carry it; non-Wilma schemes (records of external systems) fit the same shape. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
- `label` — string — Display name of the mention chip. The model sees it only to name a mention that could not be read or was removed. _(maxLen=256)_

**`MessageAppendedEvent`**

_Emitted for every assistant text token chunk. High frequency; drives live rendering of the reply._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `delta` — string **(required)** — The new text fragment.
- `soFar` — string **(required)** — The full assistant text accumulated so far in this step.

**`MessageCompletedEvent`**

_Emitted once per step when the assistant message text is complete._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `text` — string **(required)**
- `finishReason` — string **(required)** — Model finish reason for the step, e.g. `stop` or `tool-calls`.

**`MessageReceivedEvent`**

_Emitted right after TurnStartedEvent with the user message that triggered the turn, so a reconnecting client can render the conversation without a separate history fetch._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `message` — string **(required)**
- `attachments` — array — Input files supplied with this message, as stored — enough to render the attachment alongside the message (name, type, size, thumbnail) without a separate Attachments call. Absent when the turn carried no files.
  - _array of_ `Attachment`
    - `id` — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `name` — string **(required)** — Filename shown to the user. Characters storage cannot represent are replaced with underscores. _(minLen=1; maxLen=255)_
    - `contentType` — string — MIME type recorded by storage from the uploaded content, e.g. 'application/pdf'. Absent until the upload completes.
    - `size` — number — Size in bytes recorded by storage from the uploaded content. Absent until the upload completes.
    - `thumbnailUrl` — string — URL of a generated preview image, for rendering a thumbnail without downloading the file. Best-effort: absent until the upload completes, and for content no preview can be generated from.
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`ReasoningCompletedEvent`**

_Emitted once per step after the model finishes its reasoning block, carrying the complete reasoning text._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `reasoning` — string **(required)**

**`ReasoningDeltaEvent`**

_Emitted for every reasoning (thinking) token chunk the model produces, when the selected model exposes reasoning. High frequency; intended for live typing indicators._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `delta` — string **(required)** — The new reasoning fragment.
- `soFar` — string **(required)** — The full reasoning text accumulated so far in this step, so late subscribers do not need to replay every delta.

**`RevisionConflictExceptionResponseContent`**

_The resource was modified concurrently; re-read it and retry with the latest revision._

- `message` — string **(required)**
- `type` — string _(default=RevisionConflictException)_
- `currentRevision` — number — The current revision of the resource on the server.

**`RunAutomationRequestContent`**

- `input` — string — Text handed to the agent for this run, standing in for the trigger payload (e.g. test input).

**`RunAutomationResponseContent`**

_Handle returned by operations that start a task: the task and the event index from which the caller should stream._

- `taskId` — string **(required)** _(minLen=1; maxLen=128)_
- `startIndex` — number **(required)**
- `traceId` — string — Trace recording this task in wilma-traces — the agent's steps, its model calls and the tools it ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to StreamTaskEvents. This is the id to quote when reporting what an automation did: a task started by a firing trigger has no interactive caller watching it, and RunAutomation returns this handle and nothing else. The trace row is written once the task's first step completes, so GetTrace reports NotFound while the task is still `pending`. _(minLen=1; maxLen=128)_

**`RunTaskRequestContent`**

- `user` — string — The user the task runs on behalf of. Optional: tasks are company-scoped by default; set it when the task should act with a user's data access. _(minLen=12; maxLen=12)_
- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `agentVersion` — number — Published agent version to run. Mutually exclusive with agentDraft. When neither is set, the agent's deployment configuration selects the version. _(min=1)_
- `agentDraft` — boolean — Run the agent's current draft (for testing). Mutually exclusive with agentVersion.
- `input` — string **(required)** — The instructions / input handed to the agent for this task. _(minLen=1; maxLen=100000)_
- `context` — array — Additional context documents made available to the agent.
  - _array of_ `any`
- `mentions` — array — Resources the agent reads as context, resolved with the task user's permissions, or company-wide when the task has no user. _(maxItems=20)_
  - _array of_ `Mention`
    - _oneOf_ — exactly one of:
      - **`reference`**
        - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
          - _(nesting depth limit — see `MentionReference` in the Schemas appendix)_
- `schema` — any — JSON Schema the final output must conform to. When set, the agent's final answer is produced and validated as a structured document, returned in `result.structured`; `result.text` still carries the plain final answer.
- `options` — any
- `source` — TaskSource — Where a task was started from, when not started directly over the API by an administrator. Set by the integrating service so the task can be tied back to the driving resource; tasks started by an automation carry `automationId` on the task itself.
  - `uri` — string **(required)** — Canonical URI of the driving resource, e.g. 'wilma://copilot/assets/{assetId}' for a copilot asset background job. Supplied by the integrating service and opaque to this one: used to route and group, never to authorize. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
  - `metadata` — any — Additional integration-specific context.
- `waitSeconds` — number — Maximum seconds to block waiting for the task to finish. Defaults to 60. _(min=1; max=120)_

**`RunTaskResponseContent`**

_Handle returned by operations that start a task: the task and the event index from which the caller should stream._

- `taskId` — string **(required)** _(minLen=1; maxLen=128)_
- `startIndex` — number **(required)**
- `traceId` — string — Trace recording this task in wilma-traces — the agent's steps, its model calls and the tools it ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to StreamTaskEvents. This is the id to quote when reporting what an automation did: a task started by a firing trigger has no interactive caller watching it, and RunAutomation returns this handle and nothing else. The trace row is written once the task's first step completes, so GetTrace reports NotFound while the task is still `pending`. _(minLen=1; maxLen=128)_
- `status` — string **(required)** _(enum: `pending`, `running`, `completed`, `failed`, `stopped`)_
- `result` — TaskResult — Final result of a completed task. `structured` is present when the task was started with a `schema`: the agent's final output parsed and validated against that schema. `text` always carries the plain final answer.
  - `text` — string — Final answer as plain text; present with or without a schema, so a caller can check `structured` against what the agent actually said.
  - `structured` — any — Schema-validated structured output; present when the task was started with a schema.
- `error` — TaskError
  - `code` — string **(required)** — Stable machine-readable error code.
  - `message` — string **(required)**

**`SandboxFailedEvent`**

_Emitted when acquiring the sandbox fails; the turn then fails with the same cause. Provides sandbox-level observability distinct from the generic TurnFailedEvent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `message` — string **(required)**

**`SandboxStartedEvent`**

_Emitted when the turn is attached to its sandbox, the first time a sandbox-backed tool is used in the turn. A session reuses one sandbox across turns whenever possible._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `sandboxId` — string **(required)** — Provider-side sandbox id, stable while the sandbox is reused across turns.
- `resumed` — boolean **(required)** — True when an existing sandbox from a previous turn was reattached; false when a fresh sandbox was created.

**`ServiceUnavailableExceptionResponseContent`**

_The service is temporarily unable to handle the request; retry later._

- `message` — string **(required)**

**`SessionFailedEvent`**

_Terminal event emitted after TurnFailedEvent: the session is in `failed` status. A new turn starts from the last consistent snapshot._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `code` — string **(required)**
- `message` — string **(required)**

**`SessionIdleEvent`**

_Terminal event of a successful turn: the session is idle and ready for the next turn._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.

**`SessionInvocationFulfilment`**

_Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend._

- string _(enum: `server`, `client`, `synthetic`)_

**`SessionInvocationGate`**

_Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation)._

- string _(enum: `none`, `result`, `decision`)_

**`SessionInvocationResolver`**

_Who supplied the result recorded by an InvocationResultEvent._

- string _(enum: `server`, `client`, `user`)_

**`SessionInvocationStatus`**

- string _(enum: `completed`, `failed`)_

**`SessionInvocationSurface`**

_Where a client should surface an invocation. Affects placement only, never behaviour._

- string _(enum: `hidden`, `activity`, `content`)_

**`SessionStartedEvent`**

_Emitted once as the very first event of a session, when it is created. Confirms the session id and the agent the session is bound to._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
- `agentId` — string _(minLen=12; maxLen=12)_

**`SessionStopReason`**

- string _(enum: `user`)_

**`SessionStoppedEvent`**

_Terminal event emitted when the active turn was cancelled via the channel's stop operation._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `reason` — string **(required)** _(enum: `user`)_

**`SessionTerminateReason`**

- string _(enum: `guardrail`)_

**`SessionTerminatedEvent`**

_Terminal event emitted when the platform ended the session rather than let it continue: the session is in `terminated` status. Distinct from SessionStoppedEvent, which records a user or operator asking to stop — folding the two together would leave a refused session indistinguishable from a clean finish in every completion-rate report. On voice the call is hung up as this is emitted; on the other channels there is nothing to hang up and termination is the status alone — history is kept, and the session simply accepts no further turns._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `reason` — string **(required)** _(enum: `guardrail`)_
- `guardrail` — string — The check whose `end` action terminated the session, when `reason` is `guardrail`. _(minLen=1; maxLen=64)_
- `message` — string — What the caller was told before the session ended.

**`SessionUsage`**

- `inputTokens` — number
- `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
- `outputTokens` — number
- `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
- `totalTokens` — number

**`StartTaskRequestContent`**

- `user` — string — The user the task runs on behalf of. Optional: tasks are company-scoped by default; set it when the task should act with a user's data access. _(minLen=12; maxLen=12)_
- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `agentVersion` — number — Published agent version to run. Mutually exclusive with agentDraft. When neither is set, the agent's deployment configuration selects the version. _(min=1)_
- `agentDraft` — boolean — Run the agent's current draft (for testing). Mutually exclusive with agentVersion.
- `input` — string **(required)** — The instructions / input handed to the agent for this task. _(minLen=1; maxLen=100000)_
- `context` — array — Additional context documents made available to the agent.
  - _array of_ `any`
- `mentions` — array — Resources the agent reads as context, resolved with the task user's permissions, or company-wide when the task has no user. _(maxItems=20)_
  - _array of_ `Mention`
    - _oneOf_ — exactly one of:
      - **`reference`**
        - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
          - _(nesting depth limit — see `MentionReference` in the Schemas appendix)_
- `schema` — any — JSON Schema the final output must conform to. When set, the agent's final answer is produced and validated as a structured document, returned in `result.structured`; `result.text` still carries the plain final answer.
- `options` — any
- `source` — TaskSource — Where a task was started from, when not started directly over the API by an administrator. Set by the integrating service so the task can be tied back to the driving resource; tasks started by an automation carry `automationId` on the task itself.
  - `uri` — string **(required)** — Canonical URI of the driving resource, e.g. 'wilma://copilot/assets/{assetId}' for a copilot asset background job. Supplied by the integrating service and opaque to this one: used to route and group, never to authorize. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
  - `metadata` — any — Additional integration-specific context.

**`StartTaskResponseContent`**

_Handle returned by operations that start a task: the task and the event index from which the caller should stream._

- `taskId` — string **(required)** _(minLen=1; maxLen=128)_
- `startIndex` — number **(required)**
- `traceId` — string — Trace recording this task in wilma-traces — the agent's steps, its model calls and the tools it ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to StreamTaskEvents. This is the id to quote when reporting what an automation did: a task started by a firing trigger has no interactive caller watching it, and RunAutomation returns this handle and nothing else. The trace row is written once the task's first step completes, so GetTrace reports NotFound while the task is still `pending`. _(minLen=1; maxLen=128)_

**`StepCompletedEvent`**

_Emitted when an inference step finishes, with token usage for the step when the provider reports it._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `finishReason` — string **(required)**
- `usage` — SessionUsage
  - `inputTokens` — number
  - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
  - `outputTokens` — number
  - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
  - `totalTokens` — number

**`StepStartedEvent`**

_Emitted each time the model starts a new inference step within a turn (a turn spans multiple steps when the model calls tools)._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)** — 1-based step number within the turn.

**`StopTaskResponseContent`**

- `taskId` — string **(required)** _(minLen=1; maxLen=128)_
- `accepted` — boolean **(required)**

**`StreamTaskEventsOutputPayload`**

_Raw Server-Sent Events byte stream (`text/event-stream`). Each frame carries one event of the channel's own union (AssistantSessionEvent / ChatSessionEvent / WorkflowTaskEvent): `id:` is the event index, `event:` is the union member name, and `data:` is the JSON document of the union value, e.g. `{"messageAppended": {...}}`._

- string

**`Subscription`**

_What one tenant needs delivered to the service's queue._

- `company` — string **(required)** _(minLen=3; maxLen=30)_
- `selectors` — array **(required)** — Event types one tenant needs, deduplicated across everything that asked for them. Two selectors never name the same event type. The producer sends every occurrence of each listed type. _(minItems=1; maxItems=200)_
  - _array of_ `SubscriptionSelector`
    - `event` — string **(required)** — A wda-stream event type, as the webhook envelope names it, e.g. 'call:live:progress', 'call:live:transcription', 'call:completed', 'call:summary:completed', 'chat:live:progress', 'conference:live:transcription'. Open-ended: a new wda-stream type needs no model change here. _(minLen=1; maxLen=128)_
    - `conditions` — any — Reserved; not populated. Producers ignore it and send every occurrence. See SubscriptionConditions.

**`SubscriptionSelector`**

_One event type a tenant needs delivered. Conditions are evaluated by the consumer, never by the producer._

- `event` — string **(required)** — A wda-stream event type, as the webhook envelope names it, e.g. 'call:live:progress', 'call:live:transcription', 'call:completed', 'call:summary:completed', 'chat:live:progress', 'conference:live:transcription'. Open-ended: a new wda-stream type needs no model change here. _(minLen=1; maxLen=128)_
- `conditions` — any — Reserved; not populated. Producers ignore it and send every occurrence. See SubscriptionConditions.

**`Task`**

_A background execution of a workflow-channel agent._

- `id` — string **(required)** _(minLen=1; maxLen=128)_
- `status` — string **(required)** _(enum: `pending`, `running`, `completed`, `failed`, `stopped`)_
- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `agentVersion` — number — Published agent version serving this task, selected at start. _(min=1)_
- `agentDraft` — boolean — True when the task runs the agent's mutable draft.
- `traceId` — string — Trace recording this task in wilma-traces — the agent's steps, its model calls and the tools it ran, including the failure behind `error` when `status` is `failed`. Read it with the wilma-traces GetTrace operation. Names the task's own trace. Each tool call, skill load and sandbox the task made is recorded as a trace of its own; list them with QueryTraces filtered by `session.traceId`. Reported from the moment the task is accepted, matching the handle StartTask returned, but the trace row is written when the first step completes — so GetTrace reports NotFound while the task is still `pending`. Absent when the task's trace is not the caller's to read, as when a Wildix built-in agent serves it. _(minLen=1; maxLen=128)_
- `automationId` — string — Automation whose firing started this task; absent for tasks started over the API. _(minLen=1; maxLen=128)_
- `model` — string — Effective model resolved at start (after 'default' resolution).
- `source` — TaskSource — Where a task was started from, when not started directly over the API by an administrator. Set by the integrating service so the task can be tied back to the driving resource; tasks started by an automation carry `automationId` on the task itself.
  - `uri` — string **(required)** — Canonical URI of the driving resource, e.g. 'wilma://copilot/assets/{assetId}' for a copilot asset background job. Supplied by the integrating service and opaque to this one: used to route and group, never to authorize. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
  - `metadata` — any — Additional integration-specific context.
- `schema` — any — JSON Schema the final output was requested to conform to; echoed from StartTask/RunTask.
- `result` — TaskResult — Final result of a completed task. `structured` is present when the task was started with a `schema`: the agent's final output parsed and validated against that schema. `text` always carries the plain final answer.
  - `text` — string — Final answer as plain text; present with or without a schema, so a caller can check `structured` against what the agent actually said.
  - `structured` — any — Schema-validated structured output; present when the task was started with a schema.
- `error` — TaskError
  - `code` — string **(required)** — Stable machine-readable error code.
  - `message` — string **(required)**
- `usage` — SessionUsage
  - `inputTokens` — number
  - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
  - `outputTokens` — number
  - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
  - `totalTokens` — number
- `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `startedAt` — string — Time execution started; absent while pending.
- `completedAt` — string — Time the task reached a terminal status.
- `eventCount` — number **(required)**

**`TaskCompletedEvent`**

_Emitted when a delegated task execution finishes, carrying its final answer as returned to the parent agent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `taskId` — string **(required)**
- `name` — string **(required)**
- `output` — string **(required)**

**`TaskError`**

- `code` — string **(required)** — Stable machine-readable error code.
- `message` — string **(required)**

**`TaskOrigin`**

_Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity._

- `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
- `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.

**`TaskResult`**

_Final result of a completed task. `structured` is present when the task was started with a `schema`: the agent's final output parsed and validated against that schema. `text` always carries the plain final answer._

- `text` — string — Final answer as plain text; present with or without a schema, so a caller can check `structured` against what the agent actually said.
- `structured` — any — Schema-validated structured output; present when the task was started with a schema.

**`TaskSource`**

_Where a task was started from, when not started directly over the API by an administrator. Set by the integrating service so the task can be tied back to the driving resource; tasks started by an automation carry `automationId` on the task itself._

- `uri` — string **(required)** — Canonical URI of the driving resource, e.g. 'wilma://copilot/assets/{assetId}' for a copilot asset background job. Supplied by the integrating service and opaque to this one: used to route and group, never to authorize. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
- `metadata` — any — Additional integration-specific context.

**`TaskStartedEvent`**

_Emitted when the agent delegates a subtask to a task execution: the `delegate` tool or an agent-call capability. Events emitted inside the task are re-published on the session stream with `origin` set to this task, until the matching TaskCompletedEvent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `taskId` — string **(required)** — Unique id of this task execution; referenced by `origin.taskId` of nested events.
- `name` — string **(required)** — Task tool name, e.g. `delegate` or the name of the called agent.
- `agentId` — string — Agent executing the task, when the task is a called or delegated agent. _(minLen=12; maxLen=12)_
- `agentVersion` — number — Published version of the agent executing the task, resolved when the task started; absent when the task runs a draft. _(min=1)_
- `instructions` — string **(required)** — The self-contained instructions handed to the task.

**`TaskStatus`**

- string _(enum: `pending`, `running`, `completed`, `failed`, `stopped`)_

**`TurnCompletedEvent`**

_Emitted when a turn finishes successfully, with aggregate token usage for the turn. Followed by SessionIdleEvent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `usage` — SessionUsage
  - `inputTokens` — number
  - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
  - `outputTokens` — number
  - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
  - `totalTokens` — number

**`TurnFailedEvent`**

_Emitted when a turn fails with an unrecoverable error. Followed by SessionFailedEvent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `code` — string **(required)** — Stable machine-readable error code.
- `message` — string **(required)**

**`TurnStartedEvent`**

_Emitted when a turn begins executing. All subsequent events up to the matching TurnCompletedEvent/TurnFailedEvent belong to this turn._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)** — 1-based turn number within the session.

**`UpdateAutomationRequestContent`**

_The editable definition of an automation._

- `name` — string **(required)** _(minLen=1; maxLen=256)_
- `description` — string
- `enabled` — boolean — Disabled automations keep their configuration but never fire. Defaults to true.
- `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`schedule`**
      - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
        - `cron` — string **(required)** — Cron expression (five fields, e.g. '0 7 * * 1-5').
        - `timeZone` — string — IANA timezone the cron expression is evaluated in. Defaults to 'UTC'.
    - **`event`**
      - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
        - `event` — string **(required)** — The conversation-lifecycle event that fires the automation. _(minLen=1; maxLen=128)_
        - `conditions` — any — Optional filter on the event, evaluated by the workflows service on delivery; omitted or empty means fire on every occurrence of the event.
        - `payload` — any — Optional opt-out of sections of the raw event payload: `{ "includeTranscription": false }`, `includeSummary`, `includeAnnotations`. When any is `false`, the task receives the event payload without those sections instead of the conversation.
    - **`webhook`**
      - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
- `task` — AutomationTaskTemplate **(required)** — The task an automation starts when it fires.
  - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
  - `options` — any
- `revision` — number **(required)** — Revision this update is based on (optimistic locking).

**`UpdateAutomationResponseContent`**

- `automation` — Automation **(required)** — A configured automation. Tasks it started are listed via ListTasks with `automationId`.
  - `name` — string **(required)** _(minLen=1; maxLen=256)_
  - `description` — string
  - `enabled` — boolean — Disabled automations keep their configuration but never fire. Defaults to true.
  - `trigger` — union **(required)** — What causes the automation to fire. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`schedule`**
        - `schedule` — AutomationScheduleTrigger **(required)** — Fires on a cron schedule.
          - _(nesting depth limit — see `AutomationScheduleTrigger` in the Schemas appendix)_
      - **`event`**
        - `event` — AutomationEventTrigger **(required)** — Fires when a conversation-lifecycle event occurs and its conditions match. The started task receives the conversation: the record's facts on `*:completed`, and the whole conversation (record, transcript, analysis) on later events such as `call:summary:completed`. Live events attach their payload.
          - _(nesting depth limit — see `AutomationEventTrigger` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — AutomationWebhookTrigger **(required)** — Fires when an inbound HTTP request is posted to the automation's unique ingestion URL (see GetAutomationWebhookUrl). Lets any external integration drive automations without a native trigger. The posted JSON body is attached to the started task's `context` as the payload. Authenticated solely by the opaque secret embedded in the ingestion URL, not by the service's normal bearer / s2s / xbs auth.
  - `task` — AutomationTaskTemplate **(required)** — The task an automation starts when it fires.
    - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
    - `options` — any
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `id` — string **(required)** _(minLen=1; maxLen=128)_
  - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`WorkflowMoveRefusedEvent`**

_Emitted when the model asks to move somewhere the live step does not declare as an exit. The runtime refuses, names the legal exits, and the session carries on from the same step, so this is not a failure of the turn: it is the record of what callers keep reaching for and the graph does not offer. Aggregated per step, it is the shortest route to the exit a graph is missing._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `workflow` — string — The nested workflow the live step belongs to. Absent in the main graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `stepId` — string **(required)** — The step the session stayed on. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `requested` — string **(required)** — What the model asked for, verbatim — not necessarily a step that exists.
- `reason` — string — The model's stated reason for the move it was refused.

**`WorkflowStepEnteredEvent`**

_Emitted when the workflow cursor arrives at a step, before the step runs — so every later event in the log belongs to the step most recently entered. The first is the graph's `entry` step; the last is a terminal step, which is where the session left the graph._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number — The turn the step was entered during, when it was entered inside one. Absent when the cursor moved between turns: an `action`, `message` or `variables` step needs no model call, so a chain of them can advance before the next turn begins.
- `workflow` — string — The nested workflow (AgentWorkflow.nested) this step belongs to. Absent for a step of the main graph, which is how nesting is read off the stream — no separate enter/return events. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `stepId` — string **(required)** — Identifier of a step within its workflow, unique per workflow (the main graph and each nested workflow are separate scopes). Stable and machine-facing: transitions reference it, and a result step's id is the name a caller branches on, so renaming a step's `label` never unwires the graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `label` — string — The step's authored label, so a reader needs no copy of the agent definition to render the stream. _(minLen=1; maxLen=128)_
- `stage` — string — The step's stage, as authored on it or inherited from upstream. Absent when the graph uses no stages. _(minLen=1; maxLen=64)_
- `type` — string **(required)** — Which handler a step carries, reported on the session event stream (WorkflowStepEnteredEvent) and in traces. Mirrors the members of AgentWorkflowHandler and exists so a reader does not have to load the agent version snapshot to tell a stretch of conversation from a runtime action: a trace is read long after the fact, by an operator who has the session and not the definition it ran against. `conversation` is the only member that hands the turn to the model; which capability an `action` step performed is named by the invocation events that follow it. _(enum: `conversation`, `message`, `action`, `variables`, `workflow`, `result`, `end`)_

**`WorkflowTaskEvent`**

_A single typed event of a background workflow task. A task runs unattended — started by an automation, over the API, or by another agent — so it has neither an interactive user nor a live sender: it can neither suspend for input nor be steered. Its MessageReceivedEvent records the instructions the task was started with. Workflow invocations are always `fulfilment: server`. Note this union describes the task's own execution; the TaskStartedEvent / TaskCompletedEvent members inside it describe sub-agents that the task itself delegates to._

- _oneOf_ — exactly one of:
  - **`sessionStarted`**
    - `sessionStarted` — SessionStartedEvent **(required)** — Emitted once as the very first event of a session, when it is created. Confirms the session id and the agent the session is bound to.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
      - `agentId` — string _(minLen=12; maxLen=12)_
  - **`sessionIdle`**
    - `sessionIdle` — SessionIdleEvent **(required)** — Terminal event of a successful turn: the session is idle and ready for the next turn.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
  - **`sessionStopped`**
    - `sessionStopped` — SessionStoppedEvent **(required)** — Terminal event emitted when the active turn was cancelled via the channel's stop operation.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `reason` — string **(required)** _(enum: `user`)_
  - **`sessionTerminated`**
    - `sessionTerminated` — SessionTerminatedEvent **(required)** — Terminal event emitted when the platform ended the session rather than let it continue: the session is in `terminated` status. Distinct from SessionStoppedEvent, which records a user or operator asking to stop — folding the two together would leave a refused session indistinguishable from a clean finish in every completion-rate report. On voice the call is hung up as this is emitted; on the other channels there is nothing to hang up and termination is the status alone — history is kept, and the session simply accepts no further turns.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `reason` — string **(required)** _(enum: `guardrail`)_
      - `guardrail` — string — The check whose `end` action terminated the session, when `reason` is `guardrail`. _(minLen=1; maxLen=64)_
      - `message` — string — What the caller was told before the session ended.
  - **`sessionFailed`**
    - `sessionFailed` — SessionFailedEvent **(required)** — Terminal event emitted after TurnFailedEvent: the session is in `failed` status. A new turn starts from the last consistent snapshot.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `code` — string **(required)**
      - `message` — string **(required)**
  - **`turnStarted`**
    - `turnStarted` — TurnStartedEvent **(required)** — Emitted when a turn begins executing. All subsequent events up to the matching TurnCompletedEvent/TurnFailedEvent belong to this turn.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)** — 1-based turn number within the session.
  - **`turnCompleted`**
    - `turnCompleted` — TurnCompletedEvent **(required)** — Emitted when a turn finishes successfully, with aggregate token usage for the turn. Followed by SessionIdleEvent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `usage` — SessionUsage
        - `inputTokens` — number
        - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
        - `outputTokens` — number
        - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
        - `totalTokens` — number
  - **`turnFailed`**
    - `turnFailed` — TurnFailedEvent **(required)** — Emitted when a turn fails with an unrecoverable error. Followed by SessionFailedEvent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `code` — string **(required)** — Stable machine-readable error code.
      - `message` — string **(required)**
  - **`messageReceived`**
    - `messageReceived` — MessageReceivedEvent **(required)** — Emitted right after TurnStartedEvent with the user message that triggered the turn, so a reconnecting client can render the conversation without a separate history fetch.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `message` — string **(required)**
      - `attachments` — array — Input files supplied with this message, as stored — enough to render the attachment alongside the message (name, type, size, thumbnail) without a separate Attachments call. Absent when the turn carried no files.
        - _array of_ `Attachment`
          - _(nesting depth limit — see `Attachment` in the Schemas appendix)_
  - **`messageAppended`**
    - `messageAppended` — MessageAppendedEvent **(required)** — Emitted for every assistant text token chunk. High frequency; drives live rendering of the reply.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `delta` — string **(required)** — The new text fragment.
      - `soFar` — string **(required)** — The full assistant text accumulated so far in this step.
  - **`messageCompleted`**
    - `messageCompleted` — MessageCompletedEvent **(required)** — Emitted once per step when the assistant message text is complete.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `text` — string **(required)**
      - `finishReason` — string **(required)** — Model finish reason for the step, e.g. `stop` or `tool-calls`.
  - **`stepStarted`**
    - `stepStarted` — StepStartedEvent **(required)** — Emitted each time the model starts a new inference step within a turn (a turn spans multiple steps when the model calls tools).
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)** — 1-based step number within the turn.
  - **`stepCompleted`**
    - `stepCompleted` — StepCompletedEvent **(required)** — Emitted when an inference step finishes, with token usage for the step when the provider reports it.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `finishReason` — string **(required)**
      - `usage` — SessionUsage
        - `inputTokens` — number
        - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
        - `outputTokens` — number
        - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
        - `totalTokens` — number
  - **`reasoningDelta`**
    - `reasoningDelta` — ReasoningDeltaEvent **(required)** — Emitted for every reasoning (thinking) token chunk the model produces, when the selected model exposes reasoning. High frequency; intended for live typing indicators.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `delta` — string **(required)** — The new reasoning fragment.
      - `soFar` — string **(required)** — The full reasoning text accumulated so far in this step, so late subscribers do not need to replay every delta.
  - **`reasoningCompleted`**
    - `reasoningCompleted` — ReasoningCompletedEvent **(required)** — Emitted once per step after the model finishes its reasoning block, carrying the complete reasoning text.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `reasoning` — string **(required)**
  - **`invocationStarted`**
    - `invocationStarted` — InvocationStartedEvent **(required)** — Emitted when the model begins one tool invocation, before its input is complete. Every invocation starts here, regardless of how it is fulfilled or whether it suspends the turn. Carries the routing facts needed to render it — who fulfils it, whether the turn suspends, where to surface it, whether the input streams — so a client holding no tool registry (a replay, a shared session, an inspector) still renders correctly.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `callId` — string **(required)** — Stable id of this invocation, referenced by every later event about it.
      - `toolName` — string **(required)**
      - `toolId` — string — The wilma-tools Tool backing this invocation. Absent for built-in tools, connector meta-tools and other capabilities that are not shared Tools. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `toolVersion` — number — Published tool version the model was offered, when `toolId` is set. Records which input schema the invocation was written against. _(min=1)_
      - `fulfilment` — string **(required)** — Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend. _(enum: `server`, `client`, `synthetic`)_
      - `gate` — string **(required)** — Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation). _(enum: `none`, `result`, `decision`)_
      - `surface` — string **(required)** — Where a client should surface an invocation. Affects placement only, never behaviour. _(enum: `hidden`, `activity`, `content`)_
      - `stream` — boolean **(required)** — True when the input arrives as InvocationDeltaEvent chunks ahead of InvocationInputCompletedEvent. Opt-in per tool, so tools with small inputs cost nothing.
  - **`invocationDelta`**
    - `invocationDelta` — InvocationDeltaEvent **(required)** — Emitted for each fragment of an invocation's input as the model writes it, when the tool opted into streamed input. The payload is raw partial JSON text exactly as the model emits it; clients parse it incrementally to render an invocation whose input is itself content — a drafted email, a chart spec, a shared document — while it is being written. High frequency.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `callId` — string **(required)**
      - `delta` — string **(required)** — The new fragment of raw JSON input text.
      - `soFar` — string **(required)** — The raw JSON input text accumulated so far in this invocation, so late subscribers need not replay every delta. Being a prefix, it is not necessarily valid JSON on its own.
  - **`invocationInputCompleted`**
    - `invocationInputCompleted` — InvocationInputCompletedEvent **(required)** — Emitted once per invocation when its input is complete and parsed. Always emitted, whether or not the input streamed.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `callId` — string **(required)**
      - `input` — any **(required)**
  - **`invocationResult`**
    - `invocationResult` — InvocationResultEvent **(required)** — Emitted when an invocation is resolved, however that happened: a server tool finishing, a caller returning a client tool's result on resume, a person answering a question or ruling on an approval, or the runtime supplying a `synthetic` tool's result. Emitted for every invocation without exception, so replaying the log from index 0 reconstructs the same state as watching it live.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `callId` — string **(required)** — Id of the invocation this result answers, matching an InvocationStartedEvent.
      - `toolName` — string **(required)**
      - `toolId` — string — The wilma-tools Tool that executed, echoed from InvocationStartedEvent. Absent for invocations that are not backed by a shared Tool. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `toolVersion` — number — Published tool version that executed, when `toolId` is set. _(min=1)_
      - `status` — string **(required)** _(enum: `completed`, `failed`)_
      - `resolvedBy` — string **(required)** — Who supplied the result recorded by an InvocationResultEvent. _(enum: `server`, `client`, `user`)_
      - `output` — any
      - `error` — string — Present when status is `failed`.
  - **`taskStarted`**
    - `taskStarted` — TaskStartedEvent **(required)** — Emitted when the agent delegates a subtask to a task execution: the `delegate` tool or an agent-call capability. Events emitted inside the task are re-published on the session stream with `origin` set to this task, until the matching TaskCompletedEvent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `taskId` — string **(required)** — Unique id of this task execution; referenced by `origin.taskId` of nested events.
      - `name` — string **(required)** — Task tool name, e.g. `delegate` or the name of the called agent.
      - `agentId` — string — Agent executing the task, when the task is a called or delegated agent. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Published version of the agent executing the task, resolved when the task started; absent when the task runs a draft. _(min=1)_
      - `instructions` — string **(required)** — The self-contained instructions handed to the task.
  - **`taskCompleted`**
    - `taskCompleted` — TaskCompletedEvent **(required)** — Emitted when a delegated task execution finishes, carrying its final answer as returned to the parent agent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `taskId` — string **(required)**
      - `name` — string **(required)**
      - `output` — string **(required)**
  - **`workflowStepEntered`**
    - `workflowStepEntered` — WorkflowStepEnteredEvent **(required)** — Emitted when the workflow cursor arrives at a step, before the step runs — so every later event in the log belongs to the step most recently entered. The first is the graph's `entry` step; the last is a terminal step, which is where the session left the graph.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number — The turn the step was entered during, when it was entered inside one. Absent when the cursor moved between turns: an `action`, `message` or `variables` step needs no model call, so a chain of them can advance before the next turn begins.
      - `workflow` — string — The nested workflow (AgentWorkflow.nested) this step belongs to. Absent for a step of the main graph, which is how nesting is read off the stream — no separate enter/return events. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `stepId` — string **(required)** — Identifier of a step within its workflow, unique per workflow (the main graph and each nested workflow are separate scopes). Stable and machine-facing: transitions reference it, and a result step's id is the name a caller branches on, so renaming a step's `label` never unwires the graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `label` — string — The step's authored label, so a reader needs no copy of the agent definition to render the stream. _(minLen=1; maxLen=128)_
      - `stage` — string — The step's stage, as authored on it or inherited from upstream. Absent when the graph uses no stages. _(minLen=1; maxLen=64)_
      - `type` — string **(required)** — Which handler a step carries, reported on the session event stream (WorkflowStepEnteredEvent) and in traces. Mirrors the members of AgentWorkflowHandler and exists so a reader does not have to load the agent version snapshot to tell a stretch of conversation from a runtime action: a trace is read long after the fact, by an operator who has the session and not the definition it ran against. `conversation` is the only member that hands the turn to the model; which capability an `action` step performed is named by the invocation events that follow it. _(enum: `conversation`, `message`, `action`, `variables`, `workflow`, `result`, `end`)_
  - **`workflowTransition`**
    - `workflowTransition` — WorkflowTransitionEvent **(required)** — Emitted when a transition is taken, naming the exit and what decided it. Not emitted on a terminal step, which has no exits — a session that ended inside the graph is read from the last WorkflowStepEnteredEvent — and not emitted when a conversation step's conditions all stay false, which is the step simply continuing.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number — The turn the transition was evaluated in. Absent when the cursor moved between turns.
      - `workflow` — string — The nested workflow both steps belong to. Absent in the main graph; a transition never crosses graphs. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `stepId` — string **(required)** — Step being left. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `target` — string **(required)** — Step being entered. A WorkflowStepEnteredEvent for it follows. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `condition` — string **(required)** — Which kind of condition took a transition, as reported on the session event stream (WorkflowTransitionEvent) and in traces. Mirrors the members of AgentWorkflowCondition: `prompt` is the only one the model decides, every other was settled by the runtime with no model call. _(enum: `always`, `prompt`, `expression`, `result`, `failure`, `fallback`)_
      - `reason` — string — The model's one-line reason for the move, as it gave it to the steering tool. Present only for `prompt` conditions.
  - **`workflowMoveRefused`**
    - `workflowMoveRefused` — WorkflowMoveRefusedEvent **(required)** — Emitted when the model asks to move somewhere the live step does not declare as an exit. The runtime refuses, names the legal exits, and the session carries on from the same step, so this is not a failure of the turn: it is the record of what callers keep reaching for and the graph does not offer. Aggregated per step, it is the shortest route to the exit a graph is missing.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `workflow` — string — The nested workflow the live step belongs to. Absent in the main graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `stepId` — string **(required)** — The step the session stayed on. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `requested` — string **(required)** — What the model asked for, verbatim — not necessarily a step that exists.
      - `reason` — string — The model's stated reason for the move it was refused.
  - **`workflowVariablesWritten`**
    - `workflowVariablesWritten` — WorkflowVariablesWrittenEvent **(required)** — Emitted when workflow variables are written: a `variables` step's assignments, or an action step capturing its result into `output`. The only record of the state `expression` conditions branch on and handlebars resolve against, so replaying the log from index 0 reconstructs the same variables the runtime had.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number — The turn the write happened in, when it happened inside one.
      - `workflow` — string — The nested workflow the writing step belongs to. Absent in the main graph. Variables are shared with the main graph either way — a nested workflow has no scope of its own. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `stepId` — string **(required)** — Step that wrote them. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `values` — any **(required)** — The names written and their resolved values, as a JSON object. Only what this write touched, not the whole state; a variable cleared by an empty assignment is present with an empty value.
  - **`guardrailTripped`**
    - `guardrailTripped` — GuardrailTrippedEvent **(required)** — Emitted when a check trips, including when its action is `observe` and the turn proceeds untouched — that is what makes observe mode a way to tune a guardrail against real traffic rather than a switched-off check.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `check` — string **(required)** — The check's `name` in the agent definition. _(minLen=1; maxLen=64)_
      - `preset` — string — A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it. _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_
      - `confidence` — string **(required)** — How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM. _(enum: `low`, `medium`, `high`)_
      - `action` — string **(required)** — The action members by name, for reporting what actually ran. Session events carry this rather than AgentGuardrailAction because an event reports a decision, not a configuration. _(enum: `observe`, `redact`, `block`, `end`)_
      - `reason` — string — The checker's own account of why it tripped. Recorded for whoever tunes the guardrail, and never shown to the caller: telling someone which check caught them is a free oracle for the next attempt.
  - **`guardrailFailed`**
    - `guardrailFailed` — GuardrailFailedEvent **(required)** — Emitted when the checker itself errored or timed out. Carries the errorMode decision, so a reader can tell a turn that was screened and found clean from one that was never screened — without this event a fail-open guardrail would be indistinguishable from a guardrail that found nothing.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `errorMode` — string **(required)** — What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED. _(enum: `open`, `closed`)_
      - `proceeded` — boolean **(required)** — True when the turn was allowed through unscreened (`errorMode: open`), false when it was refused.
      - `reason` — string — Why the checker failed — a timeout, a provider error.
  - **`sandboxStarted`**
    - `sandboxStarted` — SandboxStartedEvent **(required)** — Emitted when the turn is attached to its sandbox, the first time a sandbox-backed tool is used in the turn. A session reuses one sandbox across turns whenever possible.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `sandboxId` — string **(required)** — Provider-side sandbox id, stable while the sandbox is reused across turns.
      - `resumed` — boolean **(required)** — True when an existing sandbox from a previous turn was reattached; false when a fresh sandbox was created.
  - **`sandboxFailed`**
    - `sandboxFailed` — SandboxFailedEvent **(required)** — Emitted when acquiring the sandbox fails; the turn then fails with the same cause. Provides sandbox-level observability distinct from the generic TurnFailedEvent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `message` — string **(required)**
  - **`artifactShared`**
    - `artifactShared` — ArtifactSharedEvent **(required)** — Emitted when the agent shares an artifact via the `share_artifact` tool, after the revision has been uploaded. Carries the file list and card metadata; the viewer reads content URLs and sharing from the wilma-artifacts service. Sharing the same artifact again publishes a new `revision` under the same `artifactId` and emits this event again.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `artifactId` — string **(required)** — Id of the registered artifact; fetch it via wilma-artifacts (GetArtifact, GetArtifactContentUrl, DownloadArtifact). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
      - `title` — string **(required)** — Human-readable title shown to the user.
      - `description` — string — One-line summary shown under the title.
      - `name` — string — Download filename shown to the user. _(minLen=1; maxLen=1024)_
      - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
      - `files` — array **(required)** — Files in this revision, with their paths, sizes and MIME types. _(minItems=1; maxItems=500)_
        - _array of_ `ArtifactFile`
          - _(nesting depth limit — see `ArtifactFile` in the Schemas appendix)_
      - `entry` — string — Path of the file the viewer opens first. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
      - `revision` — number — Revision this event published: 1 for a new artifact, higher when the agent republished it in place.
      - `path` — string — Sandbox path the artifact was shared from: the file, or the folder a bundle's paths are relative to, e.g. `/workspace/report.md` or `/workspace/site`.
      - `callId` — string — Id of the `share_artifact` tool call that produced the artifact.
  - **`compactionStarted`**
    - `compactionStarted` — CompactionStartedEvent **(required)** — Emitted before a turn when the conversation history exceeds the model context budget and is being summarized. The turn starts after CompactionCompletedEvent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
  - **`compactionCompleted`**
    - `compactionCompleted` — CompactionCompletedEvent **(required)** — Emitted when history compaction finishes and the turn proceeds with the summarized history.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**

**`WorkflowTransitionEvent`**

_Emitted when a transition is taken, naming the exit and what decided it. Not emitted on a terminal step, which has no exits — a session that ended inside the graph is read from the last WorkflowStepEnteredEvent — and not emitted when a conversation step's conditions all stay false, which is the step simply continuing._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number — The turn the transition was evaluated in. Absent when the cursor moved between turns.
- `workflow` — string — The nested workflow both steps belong to. Absent in the main graph; a transition never crosses graphs. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `stepId` — string **(required)** — Step being left. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `target` — string **(required)** — Step being entered. A WorkflowStepEnteredEvent for it follows. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `condition` — string **(required)** — Which kind of condition took a transition, as reported on the session event stream (WorkflowTransitionEvent) and in traces. Mirrors the members of AgentWorkflowCondition: `prompt` is the only one the model decides, every other was settled by the runtime with no model call. _(enum: `always`, `prompt`, `expression`, `result`, `failure`, `fallback`)_
- `reason` — string — The model's one-line reason for the move, as it gave it to the steering tool. Present only for `prompt` conditions.

**`WorkflowVariablesWrittenEvent`**

_Emitted when workflow variables are written: a `variables` step's assignments, or an action step capturing its result into `output`. The only record of the state `expression` conditions branch on and handlebars resolve against, so replaying the log from index 0 reconstructs the same variables the runtime had._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number — The turn the write happened in, when it happened inside one.
- `workflow` — string — The nested workflow the writing step belongs to. Absent in the main graph. Variables are shared with the main graph either way — a nested workflow has no scope of its own. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `stepId` — string **(required)** — Step that wrote them. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `values` — any **(required)** — The names written and their resolved values, as a JSON object. Only what this write touched, not the whole state; a variable cleared by an empty assignment is present with an empty value.

</details>
