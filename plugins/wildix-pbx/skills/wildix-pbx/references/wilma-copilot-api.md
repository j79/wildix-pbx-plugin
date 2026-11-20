## Wilma Copilot API

_OpenAPI: Wilma Copilot Service — version v2_

**Servers**

- `https://api.wilma.wildix.com` — Production
- `https://api-stable.wilma.wildix.com` — Stable
- `https://api-stage.wilma.wildix.com` — Stage

### Assets

#### `GET` `/v2/copilot/assets`

Lists reusable assets in the company.

- operationId: `ListAssets`
- **Scopes**: `wilma-copilot:ListAssets`, `wilma-copilot:read`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `contentType` (query) — string — Filter by content kind. _(enum: `card`, `playbook`, `smart_action`, `knowledge`)_
  - `enabled` (query) — boolean — Filter by enabled state.
  - `search` (query) — string — Filter by name or description.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListAssetsResponseContent`)
  - `assets` — array **(required)**
    - _array of_ `AssetInfo`
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
      - `enabled` — boolean **(required)**
      - `contentType` — string **(required)** — Which kind of content an asset carries. _(enum: `card`, `playbook`, `smart_action`, `knowledge`)_
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

#### `POST` `/v2/copilot/assets`

Creates a new reusable asset.

- operationId: `CreateAsset`
- **Scopes**: `wilma-copilot:CreateAsset`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateAssetRequestContent`) **(required)**
  - `key` — string — Stable programmatic key referenced from suggestions and traces.
  - `name` — string **(required)**
  - `description` — string
  - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
  - `title` — string — Card headline.
  - `subtitle` — string
  - `markdown` — string — Markdown body shown on the card.
  - `footer` — string
  - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
  - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
  - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
  - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`card`**
        - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
          - `content` — union — How a card's body is produced. Exactly one member is set.
            - _oneOf_ — exactly one of:
              - **`static`**
                - `static` — CardStaticContent **(required)** — Static markdown card content.
                  - _(nesting depth limit — see `CardStaticContent` in the Schemas appendix)_
              - **`agent`**
                - `agent` — CardAgentContent **(required)** — Card content generated on demand by an agent.
                  - _(nesting depth limit — see `CardAgentContent` in the Schemas appendix)_
      - **`playbook`**
        - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
          - `goal` — string
          - `steps` — array
            - _array of_ `PlaybookStep`
              - `id` — string **(required)**
              - `title` — string **(required)**
              - `markdown` — string
              - `required` — boolean — Whether the step must be completed.
              - `autoComplete` — boolean — Whether the system marks the step complete automatically from the transcript. While the playbook is shown and the step is open, a decision model asks whether it is done, judging only what was said after the playbook was shown.
              - `autoCompleteInstructions` — string — What makes the step complete, when autoComplete is set. The decision model reads it as the yes/no it answers.
          - `completionCriteria` — union — How a playbook is judged complete. Exactly one member is set.
            - _oneOf_ — exactly one of:
              - **`manual`**
                - `manual` — PlaybookManualCompletion **(required)** — The playbook is completed manually by the agent.
                  - _(nesting depth limit — see `PlaybookManualCompletion` in the Schemas appendix)_
              - **`semantic`**
                - `semantic` — PlaybookSemanticCompletion **(required)** — The playbook is completed automatically when a decision model judges its goal met, judging only what was said after the playbook was shown.
                  - _(nesting depth limit — see `PlaybookSemanticCompletion` in the Schemas appendix)_
      - **`smartAction`**
        - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
          - `actions` — array **(required)**
            - _array of_ `SmartActionItem`
              - `id` — string **(required)**
              - `label` — string **(required)**
              - `description` — string
              - `action` — union **(required)** — A button shown under an asset. Exactly one member is set; it selects what happens when clicked.
                - _(nesting depth limit — see `SmartAction` in the Schemas appendix)_
      - **`knowledge`**
        - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
          - `summary` — string
          - `sources` — string
  - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
- **Response 200** (`CreateAssetResponseContent`)
  - `asset` — Asset **(required)** — A reusable asset. Referenced by profiles via `assets`.
    - `key` — string — Stable programmatic key referenced from suggestions and traces.
    - `name` — string **(required)**
    - `description` — string
    - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
    - `title` — string — Card headline.
    - `subtitle` — string
    - `markdown` — string — Markdown body shown on the card.
    - `footer` — string
    - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
    - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
    - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
    - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`card`**
          - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
            - `content` — union — How a card's body is produced. Exactly one member is set.
              - _oneOf_ — exactly one of:
                - **`static`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`agent`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`playbook`**
          - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
            - `goal` — string
            - `steps` — array
              - _array of_ `PlaybookStep`
                - _(nesting depth limit — see `PlaybookStep` in the Schemas appendix)_
            - `completionCriteria` — union — How a playbook is judged complete. Exactly one member is set.
              - _oneOf_ — exactly one of:
                - **`manual`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`semantic`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`smartAction`**
          - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
            - `actions` — array **(required)**
              - _array of_ `SmartActionItem`
                - _(nesting depth limit — see `SmartActionItem` in the Schemas appendix)_
        - **`knowledge`**
          - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
            - `summary` — string
            - `sources` — string
    - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
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

#### `GET` `/v2/copilot/assets/{assetId}`

Gets an asset.

- operationId: `GetAsset`
- **Scopes**: `wilma-copilot:GetAsset`, `wilma-copilot:read`
- **Parameters**
  - `assetId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetAssetResponseContent`)
  - `asset` — Asset **(required)** — A reusable asset. Referenced by profiles via `assets`.
    - `key` — string — Stable programmatic key referenced from suggestions and traces.
    - `name` — string **(required)**
    - `description` — string
    - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
    - `title` — string — Card headline.
    - `subtitle` — string
    - `markdown` — string — Markdown body shown on the card.
    - `footer` — string
    - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
    - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
    - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
    - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`card`**
          - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
            - `content` — union — How a card's body is produced. Exactly one member is set.
              - _oneOf_ — exactly one of:
                - **`static`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`agent`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`playbook`**
          - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
            - `goal` — string
            - `steps` — array
              - _array of_ `PlaybookStep`
                - _(nesting depth limit — see `PlaybookStep` in the Schemas appendix)_
            - `completionCriteria` — union — How a playbook is judged complete. Exactly one member is set.
              - _oneOf_ — exactly one of:
                - **`manual`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`semantic`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`smartAction`**
          - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
            - `actions` — array **(required)**
              - _array of_ `SmartActionItem`
                - _(nesting depth limit — see `SmartActionItem` in the Schemas appendix)_
        - **`knowledge`**
          - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
            - `summary` — string
            - `sources` — string
    - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
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

#### `PUT` `/v2/copilot/assets/{assetId}`

Updates an asset. Published profile versions that captured this asset are unaffected; the change reaches live conversations when a profile referencing it is republished.

- operationId: `UpdateAsset`
- **Scopes**: `wilma-copilot:UpdateAsset`
- **Parameters**
  - `assetId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateAssetRequestContent`) **(required)**
  - `key` — string — Stable programmatic key referenced from suggestions and traces.
  - `name` — string **(required)**
  - `description` — string
  - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
  - `title` — string — Card headline.
  - `subtitle` — string
  - `markdown` — string — Markdown body shown on the card.
  - `footer` — string
  - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
  - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
  - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
  - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`card`**
        - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
          - `content` — union — How a card's body is produced. Exactly one member is set.
            - _oneOf_ — exactly one of:
              - **`static`**
                - `static` — CardStaticContent **(required)** — Static markdown card content.
                  - _(nesting depth limit — see `CardStaticContent` in the Schemas appendix)_
              - **`agent`**
                - `agent` — CardAgentContent **(required)** — Card content generated on demand by an agent.
                  - _(nesting depth limit — see `CardAgentContent` in the Schemas appendix)_
      - **`playbook`**
        - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
          - `goal` — string
          - `steps` — array
            - _array of_ `PlaybookStep`
              - `id` — string **(required)**
              - `title` — string **(required)**
              - `markdown` — string
              - `required` — boolean — Whether the step must be completed.
              - `autoComplete` — boolean — Whether the system marks the step complete automatically from the transcript. While the playbook is shown and the step is open, a decision model asks whether it is done, judging only what was said after the playbook was shown.
              - `autoCompleteInstructions` — string — What makes the step complete, when autoComplete is set. The decision model reads it as the yes/no it answers.
          - `completionCriteria` — union — How a playbook is judged complete. Exactly one member is set.
            - _oneOf_ — exactly one of:
              - **`manual`**
                - `manual` — PlaybookManualCompletion **(required)** — The playbook is completed manually by the agent.
                  - _(nesting depth limit — see `PlaybookManualCompletion` in the Schemas appendix)_
              - **`semantic`**
                - `semantic` — PlaybookSemanticCompletion **(required)** — The playbook is completed automatically when a decision model judges its goal met, judging only what was said after the playbook was shown.
                  - _(nesting depth limit — see `PlaybookSemanticCompletion` in the Schemas appendix)_
      - **`smartAction`**
        - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
          - `actions` — array **(required)**
            - _array of_ `SmartActionItem`
              - `id` — string **(required)**
              - `label` — string **(required)**
              - `description` — string
              - `action` — union **(required)** — A button shown under an asset. Exactly one member is set; it selects what happens when clicked.
                - _(nesting depth limit — see `SmartAction` in the Schemas appendix)_
      - **`knowledge`**
        - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
          - `summary` — string
          - `sources` — string
  - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
  - `revision` — number **(required)** — Revision this update is based on (optimistic locking).
- **Response 200** (`UpdateAssetResponseContent`)
  - `asset` — Asset **(required)** — A reusable asset. Referenced by profiles via `assets`.
    - `key` — string — Stable programmatic key referenced from suggestions and traces.
    - `name` — string **(required)**
    - `description` — string
    - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
    - `title` — string — Card headline.
    - `subtitle` — string
    - `markdown` — string — Markdown body shown on the card.
    - `footer` — string
    - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
    - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
    - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
    - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`card`**
          - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
            - `content` — union — How a card's body is produced. Exactly one member is set.
              - _oneOf_ — exactly one of:
                - **`static`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`agent`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`playbook`**
          - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
            - `goal` — string
            - `steps` — array
              - _array of_ `PlaybookStep`
                - _(nesting depth limit — see `PlaybookStep` in the Schemas appendix)_
            - `completionCriteria` — union — How a playbook is judged complete. Exactly one member is set.
              - _oneOf_ — exactly one of:
                - **`manual`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`semantic`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`smartAction`**
          - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
            - `actions` — array **(required)**
              - _array of_ `SmartActionItem`
                - _(nesting depth limit — see `SmartActionItem` in the Schemas appendix)_
        - **`knowledge`**
          - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
            - `summary` — string
            - `sources` — string
    - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
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

#### `DELETE` `/v2/copilot/assets/{assetId}`

Deletes an asset and removes it from every profile draft that references it. Fails with ConflictException when a profile draft still references it and detach is not allowed.

- operationId: `DeleteAsset`
- **Scopes**: `wilma-copilot:DeleteAsset`
- **Parameters**
  - `assetId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `detach` (query) — boolean — Detach the asset from referencing profile drafts instead of failing with ConflictException.
- Errors: `400`, `403`, `404`, `409`

### Automations

#### `GET` `/v2/copilot/automations`

Lists reusable automations in the company.

- operationId: `ListAutomations`
- **Scopes**: `wilma-copilot:ListAutomations`, `wilma-copilot:read`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `search` (query) — string — Filter by name or description.
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
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

#### `POST` `/v2/copilot/automations`

Creates a new reusable automation.

- operationId: `CreateAutomation`
- **Scopes**: `wilma-copilot:CreateAutomation`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateAutomationRequestContent`) **(required)**
  - `name` — string **(required)**
  - `description` — string
  - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`agent`**
        - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
          - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
          - `prompt` — string — Prompt handed to the agent; the live conversation context is added automatically.
          - `outputMode` — string — Where the automation's result is delivered. _(enum: `card`, `silent`)_
          - `parameters` — array
            - _array of_ `CopilotVariableBinding`
              - `name` — string **(required)**
              - `type` — string — Declared value type, e.g. 'string' or 'number'.
              - `optional` — boolean
              - `variant` — string **(required)** _(enum: `auto`, `guided`, `predefined`)_
              - `description` — string — Guidance for the model when variant is `guided`.
              - `value` — string — Fixed value when variant is `predefined`. Supports handlebars against the session state, e.g. '{{call.remotePhone}}'.
  - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
- **Response 200** (`CreateAutomationResponseContent`)
  - `automation` — Automation **(required)** — A reusable automation. Referenced by profiles via `automations`.
    - `name` — string **(required)**
    - `description` — string
    - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`agent`**
          - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
            - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
            - `prompt` — string — Prompt handed to the agent; the live conversation context is added automatically.
            - `outputMode` — string — Where the automation's result is delivered. _(enum: `card`, `silent`)_
            - `parameters` — array
              - _array of_ `CopilotVariableBinding`
                - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_
    - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
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

#### `GET` `/v2/copilot/automations/{automationId}`

Gets an automation.

- operationId: `GetAutomation`
- **Scopes**: `wilma-copilot:GetAutomation`, `wilma-copilot:read`
- **Parameters**
  - `automationId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetAutomationResponseContent`)
  - `automation` — Automation **(required)** — A reusable automation. Referenced by profiles via `automations`.
    - `name` — string **(required)**
    - `description` — string
    - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`agent`**
          - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
            - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
            - `prompt` — string — Prompt handed to the agent; the live conversation context is added automatically.
            - `outputMode` — string — Where the automation's result is delivered. _(enum: `card`, `silent`)_
            - `parameters` — array
              - _array of_ `CopilotVariableBinding`
                - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_
    - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
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

#### `PUT` `/v2/copilot/automations/{automationId}`

Updates an automation. Published profile versions that captured this automation are unaffected; the change reaches live conversations when a profile referencing it is republished.

- operationId: `UpdateAutomation`
- **Scopes**: `wilma-copilot:UpdateAutomation`
- **Parameters**
  - `automationId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateAutomationRequestContent`) **(required)**
  - `name` — string **(required)**
  - `description` — string
  - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`agent`**
        - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
          - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
          - `prompt` — string — Prompt handed to the agent; the live conversation context is added automatically.
          - `outputMode` — string — Where the automation's result is delivered. _(enum: `card`, `silent`)_
          - `parameters` — array
            - _array of_ `CopilotVariableBinding`
              - `name` — string **(required)**
              - `type` — string — Declared value type, e.g. 'string' or 'number'.
              - `optional` — boolean
              - `variant` — string **(required)** _(enum: `auto`, `guided`, `predefined`)_
              - `description` — string — Guidance for the model when variant is `guided`.
              - `value` — string — Fixed value when variant is `predefined`. Supports handlebars against the session state, e.g. '{{call.remotePhone}}'.
  - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
  - `revision` — number **(required)** — Revision this update is based on (optimistic locking).
- **Response 200** (`UpdateAutomationResponseContent`)
  - `automation` — Automation **(required)** — A reusable automation. Referenced by profiles via `automations`.
    - `name` — string **(required)**
    - `description` — string
    - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`agent`**
          - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
            - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
            - `prompt` — string — Prompt handed to the agent; the live conversation context is added automatically.
            - `outputMode` — string — Where the automation's result is delivered. _(enum: `card`, `silent`)_
            - `parameters` — array
              - _array of_ `CopilotVariableBinding`
                - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_
    - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
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

#### `DELETE` `/v2/copilot/automations/{automationId}`

Deletes an automation and removes it from every profile draft that references it. Fails with ConflictException when a profile draft still references it and detach is not allowed.

- operationId: `DeleteAutomation`
- **Scopes**: `wilma-copilot:DeleteAutomation`
- **Parameters**
  - `automationId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `detach` (query) — boolean — Detach the automation from referencing profile drafts instead of failing with ConflictException.
- Errors: `400`, `403`, `404`, `409`

### Evaluations

#### `GET` `/v2/copilot/evaluations`

Lists reusable evaluations in the company.

- operationId: `ListEvaluations`
- **Scopes**: `wilma-copilot:ListEvaluations`, `wilma-copilot:read`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `group` (query) — string — Filter by grouping label.
  - `search` (query) — string — Filter by name or description.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListEvaluationsResponseContent`)
  - `evaluations` — array **(required)**
    - _array of_ `EvaluationInfo`
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
      - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
      - `description` — string
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

#### `POST` `/v2/copilot/evaluations`

Creates a new reusable evaluation.

- operationId: `CreateEvaluation`
- **Scopes**: `wilma-copilot:CreateEvaluation`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateEvaluationRequestContent`) **(required)**
  - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
  - `description` — string
  - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
  - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
    - _array of_ `CopilotField`
      - `id` — string **(required)**
      - `name` — string **(required)**
      - `description` — string
      - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
      - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
        - _oneOf_ — exactly one of:
          - **`text`**
            - `text` — CopilotTextParameter **(required)** — Free-form single-line text value.
              - `examples` — array — Example values that steer extraction.
                - _array of_ `string`
          - **`multiline`**
            - `multiline` — CopilotMultilineParameter **(required)** — Free-form multi-line text value.
              - `examples` — array
                - _array of_ `string`
          - **`number`**
            - `number` — CopilotNumberParameter **(required)** — Numeric value with optional bounds.
              - `min` — number
              - `max` — number
          - **`selection`**
            - `selection` — CopilotSelectionParameter **(required)** — Value chosen from a fixed (or AI-extended) set of options.
              - `options` — array **(required)** — The allowed options.
                - _array of_ `string`
              - `multi` — boolean — Whether more than one option may be selected.
              - `adaptive` — boolean — Whether the model may introduce new options beyond `options`.
              - `adaptiveOptions` — array — Options the model introduced when `adaptive` is enabled.
                - _array of_ `string`
  - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
- **Response 200** (`CreateEvaluationResponseContent`)
  - `evaluation` — Evaluation **(required)** — A reusable evaluation. Referenced by profiles via `evaluations`.
    - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
    - `description` — string
    - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
    - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
      - _array of_ `CopilotField`
        - `id` — string **(required)**
        - `name` — string **(required)**
        - `description` — string
        - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
        - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
          - _oneOf_ — exactly one of:
            - **`text`**
              - `text` — CopilotTextParameter **(required)** — Free-form single-line text value.
                - _(nesting depth limit — see `CopilotTextParameter` in the Schemas appendix)_
            - **`multiline`**
              - `multiline` — CopilotMultilineParameter **(required)** — Free-form multi-line text value.
                - _(nesting depth limit — see `CopilotMultilineParameter` in the Schemas appendix)_
            - **`number`**
              - `number` — CopilotNumberParameter **(required)** — Numeric value with optional bounds.
                - _(nesting depth limit — see `CopilotNumberParameter` in the Schemas appendix)_
            - **`selection`**
              - `selection` — CopilotSelectionParameter **(required)** — Value chosen from a fixed (or AI-extended) set of options.
                - _(nesting depth limit — see `CopilotSelectionParameter` in the Schemas appendix)_
    - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
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

#### `GET` `/v2/copilot/evaluations/{evaluationId}`

Gets an evaluation.

- operationId: `GetEvaluation`
- **Scopes**: `wilma-copilot:GetEvaluation`, `wilma-copilot:read`
- **Parameters**
  - `evaluationId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetEvaluationResponseContent`)
  - `evaluation` — Evaluation **(required)** — A reusable evaluation. Referenced by profiles via `evaluations`.
    - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
    - `description` — string
    - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
    - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
      - _array of_ `CopilotField`
        - `id` — string **(required)**
        - `name` — string **(required)**
        - `description` — string
        - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
        - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
          - _oneOf_ — exactly one of:
            - **`text`**
              - `text` — CopilotTextParameter **(required)** — Free-form single-line text value.
                - _(nesting depth limit — see `CopilotTextParameter` in the Schemas appendix)_
            - **`multiline`**
              - `multiline` — CopilotMultilineParameter **(required)** — Free-form multi-line text value.
                - _(nesting depth limit — see `CopilotMultilineParameter` in the Schemas appendix)_
            - **`number`**
              - `number` — CopilotNumberParameter **(required)** — Numeric value with optional bounds.
                - _(nesting depth limit — see `CopilotNumberParameter` in the Schemas appendix)_
            - **`selection`**
              - `selection` — CopilotSelectionParameter **(required)** — Value chosen from a fixed (or AI-extended) set of options.
                - _(nesting depth limit — see `CopilotSelectionParameter` in the Schemas appendix)_
    - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
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

#### `PUT` `/v2/copilot/evaluations/{evaluationId}`

Updates an evaluation. Published profile versions that captured this evaluation are unaffected; the change reaches live conversations when a profile referencing it is republished.

- operationId: `UpdateEvaluation`
- **Scopes**: `wilma-copilot:UpdateEvaluation`
- **Parameters**
  - `evaluationId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateEvaluationRequestContent`) **(required)**
  - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
  - `description` — string
  - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
  - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
    - _array of_ `CopilotField`
      - `id` — string **(required)**
      - `name` — string **(required)**
      - `description` — string
      - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
      - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
        - _oneOf_ — exactly one of:
          - **`text`**
            - `text` — CopilotTextParameter **(required)** — Free-form single-line text value.
              - `examples` — array — Example values that steer extraction.
                - _array of_ `string`
          - **`multiline`**
            - `multiline` — CopilotMultilineParameter **(required)** — Free-form multi-line text value.
              - `examples` — array
                - _array of_ `string`
          - **`number`**
            - `number` — CopilotNumberParameter **(required)** — Numeric value with optional bounds.
              - `min` — number
              - `max` — number
          - **`selection`**
            - `selection` — CopilotSelectionParameter **(required)** — Value chosen from a fixed (or AI-extended) set of options.
              - `options` — array **(required)** — The allowed options.
                - _array of_ `string`
              - `multi` — boolean — Whether more than one option may be selected.
              - `adaptive` — boolean — Whether the model may introduce new options beyond `options`.
              - `adaptiveOptions` — array — Options the model introduced when `adaptive` is enabled.
                - _array of_ `string`
  - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
  - `revision` — number **(required)** — Revision this update is based on (optimistic locking).
- **Response 200** (`UpdateEvaluationResponseContent`)
  - `evaluation` — Evaluation **(required)** — A reusable evaluation. Referenced by profiles via `evaluations`.
    - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
    - `description` — string
    - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
    - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
      - _array of_ `CopilotField`
        - `id` — string **(required)**
        - `name` — string **(required)**
        - `description` — string
        - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
        - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
          - _oneOf_ — exactly one of:
            - **`text`**
              - `text` — CopilotTextParameter **(required)** — Free-form single-line text value.
                - _(nesting depth limit — see `CopilotTextParameter` in the Schemas appendix)_
            - **`multiline`**
              - `multiline` — CopilotMultilineParameter **(required)** — Free-form multi-line text value.
                - _(nesting depth limit — see `CopilotMultilineParameter` in the Schemas appendix)_
            - **`number`**
              - `number` — CopilotNumberParameter **(required)** — Numeric value with optional bounds.
                - _(nesting depth limit — see `CopilotNumberParameter` in the Schemas appendix)_
            - **`selection`**
              - `selection` — CopilotSelectionParameter **(required)** — Value chosen from a fixed (or AI-extended) set of options.
                - _(nesting depth limit — see `CopilotSelectionParameter` in the Schemas appendix)_
    - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
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

#### `DELETE` `/v2/copilot/evaluations/{evaluationId}`

Deletes an evaluation and removes it from every profile draft that references it. Fails with ConflictException when a profile draft still references it and detach is not allowed.

- operationId: `DeleteEvaluation`
- **Scopes**: `wilma-copilot:DeleteEvaluation`
- **Parameters**
  - `evaluationId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `detach` (query) — boolean — Detach the evaluation from referencing profile drafts instead of failing with ConflictException.
- Errors: `400`, `403`, `404`, `409`

### Intents

#### `GET` `/v2/copilot/intents`

Lists reusable intents in the company.

- operationId: `ListIntents`
- **Scopes**: `wilma-copilot:ListIntents`, `wilma-copilot:read`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `search` (query) — string — Filter by name or description.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListIntentsResponseContent`)
  - `intents` — array **(required)**
    - _array of_ `IntentInfo`
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
      - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
      - `description` — string
      - `textMatchEnabled` — boolean **(required)** — Whether literal text matching is enabled, i.e. whether `handlers.textMatch` is set.
      - `aiMatchEnabled` — boolean **(required)** — Whether semantic AI matching is enabled, i.e. whether `handlers.aiMatch` is set.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

#### `POST` `/v2/copilot/intents`

Creates a new reusable intent.

- operationId: `CreateIntent`
- **Scopes**: `wilma-copilot:CreateIntent`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateIntentRequestContent`) **(required)**
  - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
  - `description` — string
  - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
    - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
      - `options` — array
        - _array of_ `IntentTextMatchOption`
          - `id` — string **(required)**
          - `value` — string **(required)** — The phrase, word or pattern to look for, e.g. 'refund', 'W-AIR' or a regex.
          - `mode` — string **(required)** — How a literal phrase is compared against the transcript. _(enum: `exact`, `fuzzy`, `regex`)_
    - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
      - `instructions` — string — Prompt describing when this intent applies.
      - `fields` — array — Structured values the model extracts when the intent matches.
        - _array of_ `CopilotField`
          - `id` — string **(required)**
          - `name` — string **(required)**
          - `description` — string
          - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
          - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
            - _oneOf_ — exactly one of:
              - **`text`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`multiline`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`number`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`selection`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
  - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
- **Response 200** (`CreateIntentResponseContent`)
  - `intent` — Intent **(required)** — A reusable intent. Referenced by profiles via `intents`.
    - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
    - `description` — string
    - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
      - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
        - `options` — array
          - _array of_ `IntentTextMatchOption`
            - `id` — string **(required)**
            - `value` — string **(required)** — The phrase, word or pattern to look for, e.g. 'refund', 'W-AIR' or a regex.
            - `mode` — string **(required)** — How a literal phrase is compared against the transcript. _(enum: `exact`, `fuzzy`, `regex`)_
      - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
        - `instructions` — string — Prompt describing when this intent applies.
        - `fields` — array — Structured values the model extracts when the intent matches.
          - _array of_ `CopilotField`
            - `id` — string **(required)**
            - `name` — string **(required)**
            - `description` — string
            - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
            - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
              - _(nesting depth limit — see `CopilotFieldParameter` in the Schemas appendix)_
      - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
    - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
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

#### `GET` `/v2/copilot/intents/{intentId}`

Gets an intent.

- operationId: `GetIntent`
- **Scopes**: `wilma-copilot:GetIntent`, `wilma-copilot:read`
- **Parameters**
  - `intentId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetIntentResponseContent`)
  - `intent` — Intent **(required)** — A reusable intent. Referenced by profiles via `intents`.
    - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
    - `description` — string
    - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
      - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
        - `options` — array
          - _array of_ `IntentTextMatchOption`
            - `id` — string **(required)**
            - `value` — string **(required)** — The phrase, word or pattern to look for, e.g. 'refund', 'W-AIR' or a regex.
            - `mode` — string **(required)** — How a literal phrase is compared against the transcript. _(enum: `exact`, `fuzzy`, `regex`)_
      - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
        - `instructions` — string — Prompt describing when this intent applies.
        - `fields` — array — Structured values the model extracts when the intent matches.
          - _array of_ `CopilotField`
            - `id` — string **(required)**
            - `name` — string **(required)**
            - `description` — string
            - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
            - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
              - _(nesting depth limit — see `CopilotFieldParameter` in the Schemas appendix)_
      - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
    - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
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

#### `PUT` `/v2/copilot/intents/{intentId}`

Updates an intent. Published profile versions that captured this intent are unaffected; the change reaches live conversations when a profile referencing it is republished.

- operationId: `UpdateIntent`
- **Scopes**: `wilma-copilot:UpdateIntent`
- **Parameters**
  - `intentId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateIntentRequestContent`) **(required)**
  - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
  - `description` — string
  - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
    - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
      - `options` — array
        - _array of_ `IntentTextMatchOption`
          - `id` — string **(required)**
          - `value` — string **(required)** — The phrase, word or pattern to look for, e.g. 'refund', 'W-AIR' or a regex.
          - `mode` — string **(required)** — How a literal phrase is compared against the transcript. _(enum: `exact`, `fuzzy`, `regex`)_
    - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
      - `instructions` — string — Prompt describing when this intent applies.
      - `fields` — array — Structured values the model extracts when the intent matches.
        - _array of_ `CopilotField`
          - `id` — string **(required)**
          - `name` — string **(required)**
          - `description` — string
          - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
          - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
            - _oneOf_ — exactly one of:
              - **`text`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`multiline`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`number`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`selection`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
  - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
  - `revision` — number **(required)** — Revision this update is based on (optimistic locking).
- **Response 200** (`UpdateIntentResponseContent`)
  - `intent` — Intent **(required)** — A reusable intent. Referenced by profiles via `intents`.
    - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
    - `description` — string
    - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
      - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
        - `options` — array
          - _array of_ `IntentTextMatchOption`
            - `id` — string **(required)**
            - `value` — string **(required)** — The phrase, word or pattern to look for, e.g. 'refund', 'W-AIR' or a regex.
            - `mode` — string **(required)** — How a literal phrase is compared against the transcript. _(enum: `exact`, `fuzzy`, `regex`)_
      - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
        - `instructions` — string — Prompt describing when this intent applies.
        - `fields` — array — Structured values the model extracts when the intent matches.
          - _array of_ `CopilotField`
            - `id` — string **(required)**
            - `name` — string **(required)**
            - `description` — string
            - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
            - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
              - _(nesting depth limit — see `CopilotFieldParameter` in the Schemas appendix)_
      - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
    - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
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

#### `DELETE` `/v2/copilot/intents/{intentId}`

Deletes an intent and removes it from every profile draft that references it. Fails with ConflictException when a profile draft still references it and detach is not allowed.

- operationId: `DeleteIntent`
- **Scopes**: `wilma-copilot:DeleteIntent`
- **Parameters**
  - `intentId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `detach` (query) — boolean — Detach the intent from referencing profile drafts instead of failing with ConflictException.
- Errors: `400`, `403`, `404`, `409`

### Profiles

#### `GET` `/v2/copilot/profiles`

Lists copilot profiles in the company.

- operationId: `ListProfiles`
- **Scopes**: `wilma-copilot:ListProfiles`, `wilma-copilot:read`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `status` (query) — string — Filter by status. _(enum: `draft`, `active`)_
  - `channel` (query) — string — Filter by a conversation channel the profile applies to. A profile with no channels applies to every one, so it matches whatever is asked for here. _(enum: `call`, `conference`, `chat`)_
  - `stage` (query) — string — Filter by a stage the profile applies in. A profile with no stages applies in every one, so it matches whatever is asked for here. _(enum: `before`, `during`, `after`)_
  - `search` (query) — string — Filter by name or description.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListProfilesResponseContent`)
  - `profiles` — array **(required)**
    - _array of_ `ProfileInfo`
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
      - `audience` — array — The profile's targeting, so a list row can say what it applies to without reading the definition.
        - _array of_ `CopilotAudienceEntry`
          - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
          - `values` — array **(required)**
            - _array of_ `string`
      - `stages` — array — Stages a resource applies in. An empty or absent list means every stage.
        - _array of_ `CopilotStage`
      - `channels` — array — Conversation channels a resource applies to. An empty or absent list means every channel. A channel filter only constrains the `during` and `after` stages: in `before` there is nothing to be a call, a conference or a chat, so a resource covering only `before` applies whatever this list says.
        - _array of_ `CopilotChannel`
      - `status` — string **(required)** _(enum: `draft`, `active`)_
      - `live` — boolean **(required)**
      - `latestVersion` — number — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
      - `intentCount` — number — Number of referenced intents.
      - `evaluationCount` — number — Number of referenced evaluations.
      - `automationCount` — number — Number of referenced automations.
      - `assetCount` — number — Number of referenced assets.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

#### `POST` `/v2/copilot/profiles`

Creates a new profile draft. The profile is not applied to any conversation until its first version is published.

- operationId: `CreateProfile`
- **Scopes**: `wilma-copilot:CreateProfile`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateProfileRequestContent`) **(required)**
  - `name` — string **(required)**
  - `description` — string
  - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
    - _array of_ `CopilotAudienceEntry`
      - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
      - `values` — array **(required)**
        - _array of_ `string`
  - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
    - _array of_ `CopilotStage`
  - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
    - _array of_ `CopilotChannel`
  - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
  - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
    - _array of_ `CopilotFeature`
      - _oneOf_ — exactly one of:
        - **`csat`**
          - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
        - **`sentiment`**
          - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
        - **`talkRatio`**
          - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
        - **`topics`**
          - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
            - `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
              - _array of_ `string`
            - `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
              - _array of_ `CustomTopicCategory`
                - _(nesting depth limit — see `CustomTopicCategory` in the Schemas appendix)_
        - **`contextualKnowledgeAnswers`**
          - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
            - `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
            - `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
              - _array of_ `string`
            - `agentId` — string — Agent used when source is `agent`.
            - `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_
        - **`signals`**
          - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
            - `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
              - _array of_ `string`
  - `assets` — array — Assets referenced by this profile.
    - _array of_ `string`
  - `intents` — array — Intents referenced by this profile.
    - _array of_ `string`
  - `evaluations` — array — Evaluations referenced by this profile.
    - _array of_ `string`
  - `automations` — array — Automations referenced by this profile.
    - _array of_ `string`
- **Response 200** (`CreateProfileResponseContent`)
  - `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
    - `name` — string **(required)**
    - `description` — string
    - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
      - _array of_ `CopilotAudienceEntry`
        - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
        - `values` — array **(required)**
          - _array of_ `string`
    - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
      - _array of_ `CopilotStage`
    - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
      - _array of_ `CopilotChannel`
    - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
    - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
      - _array of_ `CopilotFeature`
        - _oneOf_ — exactly one of:
          - **`csat`**
            - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
          - **`sentiment`**
            - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
          - **`talkRatio`**
            - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
          - **`topics`**
            - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
              - `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
                - _array of_ `string`
              - `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
                - _(nesting depth limit — see `CustomTopicCategory` in the Schemas appendix)_
          - **`contextualKnowledgeAnswers`**
            - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
              - `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
              - `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
                - _array of_ `string`
              - `agentId` — string — Agent used when source is `agent`.
              - `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_
          - **`signals`**
            - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
              - `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
                - _array of_ `string`
    - `assets` — array — Assets referenced by this profile.
      - _array of_ `string`
    - `intents` — array — Intents referenced by this profile.
      - _array of_ `string`
    - `evaluations` — array — Evaluations referenced by this profile.
      - _array of_ `string`
    - `automations` — array — Automations referenced by this profile.
      - _array of_ `string`
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
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
    - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).
- Errors: `400`, `403`, `409`

#### `GET` `/v2/copilot/profiles/{profileId}`

Gets a profile draft, including metadata, referenced library resource ids and version state.

- operationId: `GetProfile`
- **Scopes**: `wilma-copilot:GetProfile`, `wilma-copilot:read`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetProfileResponseContent`)
  - `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
    - `name` — string **(required)**
    - `description` — string
    - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
      - _array of_ `CopilotAudienceEntry`
        - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
        - `values` — array **(required)**
          - _array of_ `string`
    - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
      - _array of_ `CopilotStage`
    - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
      - _array of_ `CopilotChannel`
    - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
    - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
      - _array of_ `CopilotFeature`
        - _oneOf_ — exactly one of:
          - **`csat`**
            - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
          - **`sentiment`**
            - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
          - **`talkRatio`**
            - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
          - **`topics`**
            - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
              - `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
                - _array of_ `string`
              - `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
                - _(nesting depth limit — see `CustomTopicCategory` in the Schemas appendix)_
          - **`contextualKnowledgeAnswers`**
            - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
              - `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
              - `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
                - _array of_ `string`
              - `agentId` — string — Agent used when source is `agent`.
              - `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_
          - **`signals`**
            - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
              - `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
                - _array of_ `string`
    - `assets` — array — Assets referenced by this profile.
      - _array of_ `string`
    - `intents` — array — Intents referenced by this profile.
      - _array of_ `string`
    - `evaluations` — array — Evaluations referenced by this profile.
      - _array of_ `string`
    - `automations` — array — Automations referenced by this profile.
      - _array of_ `string`
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
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
    - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).
- Errors: `400`, `403`, `404`

#### `PUT` `/v2/copilot/profiles/{profileId}`

Updates profile metadata only. Attachments are changed through AttachProfileResource and DeleteProfileResource. Does not affect live conversations until the draft is published.

- operationId: `UpdateProfile`
- **Scopes**: `wilma-copilot:UpdateProfile`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateProfileRequestContent`) **(required)**
  - `name` — string **(required)**
  - `description` — string
  - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
    - _array of_ `CopilotAudienceEntry`
      - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
      - `values` — array **(required)**
        - _array of_ `string`
  - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
    - _array of_ `CopilotStage`
  - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
    - _array of_ `CopilotChannel`
  - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
  - `revision` — number **(required)** — Draft revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.
- **Response 200** (`UpdateProfileResponseContent`)
  - `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
    - `name` — string **(required)**
    - `description` — string
    - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
      - _array of_ `CopilotAudienceEntry`
        - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
        - `values` — array **(required)**
          - _array of_ `string`
    - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
      - _array of_ `CopilotStage`
    - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
      - _array of_ `CopilotChannel`
    - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
    - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
      - _array of_ `CopilotFeature`
        - _oneOf_ — exactly one of:
          - **`csat`**
            - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
          - **`sentiment`**
            - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
          - **`talkRatio`**
            - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
          - **`topics`**
            - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
              - `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
                - _array of_ `string`
              - `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
                - _(nesting depth limit — see `CustomTopicCategory` in the Schemas appendix)_
          - **`contextualKnowledgeAnswers`**
            - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
              - `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
              - `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
                - _array of_ `string`
              - `agentId` — string — Agent used when source is `agent`.
              - `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_
          - **`signals`**
            - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
              - `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
                - _array of_ `string`
    - `assets` — array — Assets referenced by this profile.
      - _array of_ `string`
    - `intents` — array — Intents referenced by this profile.
      - _array of_ `string`
    - `evaluations` — array — Evaluations referenced by this profile.
      - _array of_ `string`
    - `automations` — array — Automations referenced by this profile.
      - _array of_ `string`
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
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
    - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).
- Errors: `400`, `403`, `404`, `409`

#### `DELETE` `/v2/copilot/profiles/{profileId}`

Deletes a profile and its version history. Library resources referenced by the profile are not deleted.

- operationId: `DeleteProfile`
- **Scopes**: `wilma-copilot:DeleteProfile`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- Errors: `400`, `403`, `404`

#### `PATCH` `/v2/copilot/profiles/{profileId}/disable`

Disables a profile so it is no longer applied to live conversations. Its draft and published versions are kept.

- operationId: `DisableProfile`
- **Scopes**: `wilma-copilot:DisableProfile`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`DisableProfileResponseContent`)
  - `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
    - `name` — string **(required)**
    - `description` — string
    - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
      - _array of_ `CopilotAudienceEntry`
        - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
        - `values` — array **(required)**
          - _array of_ `string`
    - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
      - _array of_ `CopilotStage`
    - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
      - _array of_ `CopilotChannel`
    - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
    - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
      - _array of_ `CopilotFeature`
        - _oneOf_ — exactly one of:
          - **`csat`**
            - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
          - **`sentiment`**
            - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
          - **`talkRatio`**
            - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
          - **`topics`**
            - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
              - `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
                - _array of_ `string`
              - `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
                - _(nesting depth limit — see `CustomTopicCategory` in the Schemas appendix)_
          - **`contextualKnowledgeAnswers`**
            - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
              - `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
              - `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
                - _array of_ `string`
              - `agentId` — string — Agent used when source is `agent`.
              - `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_
          - **`signals`**
            - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
              - `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
                - _array of_ `string`
    - `assets` — array — Assets referenced by this profile.
      - _array of_ `string`
    - `intents` — array — Intents referenced by this profile.
      - _array of_ `string`
    - `evaluations` — array — Evaluations referenced by this profile.
      - _array of_ `string`
    - `automations` — array — Automations referenced by this profile.
      - _array of_ `string`
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
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
    - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).
- Errors: `400`, `403`, `404`

#### `PATCH` `/v2/copilot/profiles/{profileId}/enable`

Enables a published profile so its latest version is applied to live conversations.

- operationId: `EnableProfile`
- **Scopes**: `wilma-copilot:EnableProfile`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`EnableProfileResponseContent`)
  - `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
    - `name` — string **(required)**
    - `description` — string
    - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
      - _array of_ `CopilotAudienceEntry`
        - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
        - `values` — array **(required)**
          - _array of_ `string`
    - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
      - _array of_ `CopilotStage`
    - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
      - _array of_ `CopilotChannel`
    - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
    - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
      - _array of_ `CopilotFeature`
        - _oneOf_ — exactly one of:
          - **`csat`**
            - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
          - **`sentiment`**
            - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
          - **`talkRatio`**
            - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
          - **`topics`**
            - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
              - `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
                - _array of_ `string`
              - `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
                - _(nesting depth limit — see `CustomTopicCategory` in the Schemas appendix)_
          - **`contextualKnowledgeAnswers`**
            - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
              - `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
              - `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
                - _array of_ `string`
              - `agentId` — string — Agent used when source is `agent`.
              - `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_
          - **`signals`**
            - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
              - `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
                - _array of_ `string`
    - `assets` — array — Assets referenced by this profile.
      - _array of_ `string`
    - `intents` — array — Intents referenced by this profile.
      - _array of_ `string`
    - `evaluations` — array — Evaluations referenced by this profile.
      - _array of_ `string`
    - `automations` — array — Automations referenced by this profile.
      - _array of_ `string`
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
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
    - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).
- Errors: `400`, `403`, `404`

#### `POST` `/v2/copilot/profiles/{profileId}/resources`

Attaches one feature or reusable library resource to the profile draft. Attaching an already attached resource is idempotent; an existing feature of the same type is updated with the supplied configuration. Does not affect live conversations until the draft is published.

- operationId: `AttachProfileResource`
- **Scopes**: `wilma-copilot:AttachProfileResource`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `AttachProfileResourceRequestContent`) **(required)**
  - `revision` — number **(required)** — Draft revision this update is based on (optimistic locking).
  - `resource` — union **(required)** — One feature or reusable library resource attached to a profile.
    - _oneOf_ — exactly one of:
      - **`feature`**
        - `feature` — union **(required)** — A Copilot feature enabled for a profile, with its type-specific configuration.
          - _oneOf_ — exactly one of:
            - **`csat`**
              - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
            - **`sentiment`**
              - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
            - **`talkRatio`**
              - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
            - **`topics`**
              - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
                - `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
                  - _array of_ `string`
                - `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
                  - _(nesting depth limit — see `CustomTopicCategory` in the Schemas appendix)_
            - **`contextualKnowledgeAnswers`**
              - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
                - `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
                - `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
                  - _array of_ `string`
                - `agentId` — string — Agent used when source is `agent`.
                - `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_
            - **`signals`**
              - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
                - `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
                  - _array of_ `string`
      - **`asset`**
        - `asset` — string **(required)** _(minLen=1; maxLen=128)_
      - **`automation`**
        - `automation` — string **(required)** _(minLen=1; maxLen=128)_
      - **`intent`**
        - `intent` — string **(required)** _(minLen=1; maxLen=128)_
      - **`evaluation`**
        - `evaluation` — string **(required)** _(minLen=1; maxLen=128)_
- **Response 200** (`AttachProfileResourceResponseContent`)
  - `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
    - `name` — string **(required)**
    - `description` — string
    - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
      - _array of_ `CopilotAudienceEntry`
        - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
        - `values` — array **(required)**
          - _array of_ `string`
    - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
      - _array of_ `CopilotStage`
    - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
      - _array of_ `CopilotChannel`
    - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
    - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
      - _array of_ `CopilotFeature`
        - _oneOf_ — exactly one of:
          - **`csat`**
            - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
          - **`sentiment`**
            - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
          - **`talkRatio`**
            - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
          - **`topics`**
            - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
              - `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
                - _array of_ `string`
              - `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
                - _(nesting depth limit — see `CustomTopicCategory` in the Schemas appendix)_
          - **`contextualKnowledgeAnswers`**
            - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
              - `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
              - `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
                - _array of_ `string`
              - `agentId` — string — Agent used when source is `agent`.
              - `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_
          - **`signals`**
            - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
              - `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
                - _array of_ `string`
    - `assets` — array — Assets referenced by this profile.
      - _array of_ `string`
    - `intents` — array — Intents referenced by this profile.
      - _array of_ `string`
    - `evaluations` — array — Evaluations referenced by this profile.
      - _array of_ `string`
    - `automations` — array — Automations referenced by this profile.
      - _array of_ `string`
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
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
    - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).
- Errors: `400`, `403`, `404`, `409`

#### `DELETE` `/v2/copilot/profiles/{profileId}/resources/{resourceType}/{resourceId}`

Deletes one feature or reusable library-resource attachment from the profile draft. Deleting an already absent resource is idempotent. Does not affect live conversations until the draft is published.

- operationId: `DeleteProfileResource`
- **Scopes**: `wilma-copilot:DeleteProfileResource`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `resourceType` (path) — string **(required)** — The kind of resource attached to a profile. _(enum: `feature`, `asset`, `automation`, `intent`, `evaluation`)_
  - `resourceId` (path) — string **(required)** — Identifier of an attached profile resource. For a feature, use the feature union member name, such as `csat` or `sentiment`. _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `revision` (query) — number **(required)** — Draft revision this update is based on (optimistic locking).
- **Response 200** (`DeleteProfileResourceResponseContent`)
  - `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
    - `name` — string **(required)**
    - `description` — string
    - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
      - _array of_ `CopilotAudienceEntry`
        - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
        - `values` — array **(required)**
          - _array of_ `string`
    - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
      - _array of_ `CopilotStage`
    - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
      - _array of_ `CopilotChannel`
    - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
    - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
      - _array of_ `CopilotFeature`
        - _oneOf_ — exactly one of:
          - **`csat`**
            - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
          - **`sentiment`**
            - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
          - **`talkRatio`**
            - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
          - **`topics`**
            - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
              - `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
                - _array of_ `string`
              - `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
                - _(nesting depth limit — see `CustomTopicCategory` in the Schemas appendix)_
          - **`contextualKnowledgeAnswers`**
            - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
              - `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
              - `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
                - _array of_ `string`
              - `agentId` — string — Agent used when source is `agent`.
              - `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_
          - **`signals`**
            - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
              - `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
                - _array of_ `string`
    - `assets` — array — Assets referenced by this profile.
      - _array of_ `string`
    - `intents` — array — Intents referenced by this profile.
      - _array of_ `string`
    - `evaluations` — array — Evaluations referenced by this profile.
      - _array of_ `string`
    - `automations` — array — Automations referenced by this profile.
      - _array of_ `string`
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
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
    - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).
- Errors: `400`, `403`, `404`, `409`

#### `GET` `/v2/copilot/subscriptions`

Lists the wda-stream events copilot needs delivered, for every company that has a published
    profile — the ingress contract between wda-stream and the copilot runtime.

    **Service tokens only.** The answer spans every company on the platform: it is the event
    producer's routing table, not a tenant's view of its own configuration, and there is no company
    parameter to scope it with. A user, PBX or API-key token is refused. Every subscription is
    returned in one response, unpaginated, because the producer applies it as a whole — a table
    assembled from several requests can be applied half-built, which looks exactly like a set of
    companies that unsubscribed.

    Copilot is a state machine over a conversation, not a filter over single events, so the answer
    is coarser than an automation's. A profile that shows an asset after 45 seconds needs a session
    that exists and a timer that is running, which means the conversation's lifecycle events; one
    that reads the transcript needs every transcription event, interim chunks included. What the
    published profiles do *not* need is what this operation leaves out: the surfaces no profile
    targets, transcription for profiles that never read it, and every company with no published
    profile at all.

    Conditions are resolved in the session against accumulated state, so they are never pushed to
    the producer; selectors carry event types only.

- operationId: `ListSubscriptions`
- **Scopes**: `wilma-copilot:ListSubscriptions`, `wilma-copilot:read`
- **Response 200** (`ListSubscriptionsResponseContent`)
  - `subscriptions` — array **(required)**
    - _array of_ `Subscription`
      - `company` — string **(required)** _(minLen=3; maxLen=30)_
      - `selectors` — array **(required)** — Event types one tenant needs, deduplicated across everything that asked for them. Two selectors never name the same event type. The producer sends every occurrence of each listed type. _(minItems=1; maxItems=200)_
        - _array of_ `SubscriptionSelector`
          - `event` — string **(required)** — A wda-stream event type, as the webhook envelope names it, e.g. 'call:live:progress', 'call:live:transcription', 'call:completed', 'call:summary:completed', 'chat:live:progress', 'conference:live:transcription'. Open-ended: a new wda-stream type needs no model change here. _(minLen=1; maxLen=128)_
          - `conditions` — any — Reserved; not populated. Producers ignore it and send every occurrence. See SubscriptionConditions.
- Errors: `400`, `403`

### Versions

#### `GET` `/v2/copilot/profiles/{profileId}/compare-versions`

Returns the field-level differences between two versions, or between a version and the current draft.

- operationId: `CompareProfileVersions`
- **Scopes**: `wilma-copilot:CompareProfileVersions`, `wilma-copilot:read`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `from` (query) — number — Base published version number. Omit when fromDraft is true. _(min=1)_
  - `fromDraft` (query) — boolean — Compare against the current draft instead of a published version.
  - `to` (query) — number — Target published version number. Omit when toDraft is true. _(min=1)_
  - `toDraft` (query) — boolean — Compare against the current draft instead of a published version.
- **Response 200** (`CompareProfileVersionsResponseContent`)
  - `changes` — array **(required)**
    - _array of_ `ProfileVersionChange`
      - `path` — string **(required)** — JSON pointer of the changed field within the profile definition, e.g. '/assets/0/markdown'.
      - `before` — any — Value before the change (absent when the field was added).
      - `after` — any — Value after the change (absent when the field was removed).
- Errors: `400`, `404`

#### `GET` `/v2/copilot/profiles/{profileId}/versions`

Lists the published versions of a profile, newest first.

- operationId: `ListProfileVersions`
- **Scopes**: `wilma-copilot:ListProfileVersions`, `wilma-copilot:read`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListProfileVersionsResponseContent`)
  - `versions` — array **(required)**
    - _array of_ `ProfileVersionInfo`
      - `profileId` — string **(required)** _(minLen=1; maxLen=128)_
      - `version` — number **(required)** — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
      - `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
      - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
        - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
        - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
        - `name` — string — Human readable name of the actor at the time of the action.
      - `latest` — boolean — True when this version is the profile's latestVersion.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `404`

#### `POST` `/v2/copilot/profiles/{profileId}/versions`

Publishes the current draft as a new immutable version and updates latestVersion. The referenced intents, evaluations, automations and assets are resolved into the version snapshot, and the wilma-copilot-sessions runtime applies the new version to conversations started after publish.

- operationId: `PublishProfileVersion`
- **Scopes**: `wilma-copilot:PublishProfileVersion`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `PublishProfileVersionRequestContent`) **(required)**
  - `changelog` — string — What changed in this version. _(minLen=1; maxLen=500)_
  - `revision` — number **(required)** — Draft revision this publish is based on (optimistic locking).
- **Response 200** (`PublishProfileVersionResponseContent`)
  - `version` — ProfileVersion **(required)** — Published profile version: an immutable, self-contained snapshot of the profile at publish time.
    - `profileId` — string **(required)** _(minLen=1; maxLen=128)_
    - `version` — number **(required)** — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
    - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
    - `definition` — ProfileDefinitionSnapshot **(required)** — Immutable snapshot of a profile definition at publish time, with all referenced library resources resolved inline.
      - `name` — string **(required)**
      - `description` — string
      - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
        - _array of_ `CopilotAudienceEntry`
          - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
          - `values` — array **(required)**
            - _array of_ `string`
      - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
        - _array of_ `CopilotStage`
      - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
        - _array of_ `CopilotChannel`
      - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
      - `features` — array — Copilot features enabled for this profile at publish time, including their type-specific configuration.
        - _array of_ `CopilotFeature`
          - _oneOf_ — exactly one of:
            - **`csat`**
              - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
            - **`sentiment`**
              - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
            - **`talkRatio`**
              - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
            - **`topics`**
              - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
                - _(nesting depth limit — see `TopicsFeatureConfiguration` in the Schemas appendix)_
            - **`contextualKnowledgeAnswers`**
              - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
                - _(nesting depth limit — see `ContextualKnowledgeAnswersFeatureConfiguration` in the Schemas appendix)_
            - **`signals`**
              - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
                - _(nesting depth limit — see `SignalsFeatureConfiguration` in the Schemas appendix)_
      - `intents` — array **(required)** — Intents resolved from the draft's intents at publish time.
        - _array of_ `IntentSnapshot`
          - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
          - `description` — string
          - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
            - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
              - _(nesting depth limit — see `IntentTextMatch` in the Schemas appendix)_
            - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
              - _(nesting depth limit — see `IntentAiMatch` in the Schemas appendix)_
            - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
          - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
          - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `evaluations` — array **(required)** — Evaluations resolved from the draft's evaluations at publish time.
        - _array of_ `EvaluationSnapshot`
          - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
          - `description` — string
          - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
          - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
            - _array of_ `CopilotField`
              - _(nesting depth limit — see `CopilotField` in the Schemas appendix)_
          - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
          - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `automations` — array **(required)** — Automations resolved from the draft's automations at publish time.
        - _array of_ `AutomationSnapshot`
          - `name` — string **(required)**
          - `description` — string
          - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
            - _oneOf_ — exactly one of:
              - **`agent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
          - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `assets` — array **(required)** — Assets resolved from the draft's assets at publish time.
        - _array of_ `AssetSnapshot`
          - `key` — string — Stable programmatic key referenced from suggestions and traces.
          - `name` — string **(required)**
          - `description` — string
          - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
          - `title` — string — Card headline.
          - `subtitle` — string
          - `markdown` — string — Markdown body shown on the card.
          - `footer` — string
          - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
          - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
          - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
          - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
            - _oneOf_ — exactly one of:
              - **`card`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`playbook`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`smartAction`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`knowledge`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
          - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
- Errors: `400`, `404`, `409`

#### `GET` `/v2/copilot/profiles/{profileId}/versions/{version}`

Retrieves a published profile version, including its full immutable definition snapshot with resolved library resources.

- operationId: `GetProfileVersion`
- **Scopes**: `wilma-copilot:GetProfileVersion`, `wilma-copilot:read`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `version` (path) — number **(required)** — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetProfileVersionResponseContent`)
  - `version` — ProfileVersion **(required)** — Published profile version: an immutable, self-contained snapshot of the profile at publish time.
    - `profileId` — string **(required)** _(minLen=1; maxLen=128)_
    - `version` — number **(required)** — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
    - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
    - `definition` — ProfileDefinitionSnapshot **(required)** — Immutable snapshot of a profile definition at publish time, with all referenced library resources resolved inline.
      - `name` — string **(required)**
      - `description` — string
      - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
        - _array of_ `CopilotAudienceEntry`
          - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
          - `values` — array **(required)**
            - _array of_ `string`
      - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
        - _array of_ `CopilotStage`
      - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
        - _array of_ `CopilotChannel`
      - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
      - `features` — array — Copilot features enabled for this profile at publish time, including their type-specific configuration.
        - _array of_ `CopilotFeature`
          - _oneOf_ — exactly one of:
            - **`csat`**
              - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
            - **`sentiment`**
              - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
            - **`talkRatio`**
              - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
            - **`topics`**
              - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
                - _(nesting depth limit — see `TopicsFeatureConfiguration` in the Schemas appendix)_
            - **`contextualKnowledgeAnswers`**
              - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
                - _(nesting depth limit — see `ContextualKnowledgeAnswersFeatureConfiguration` in the Schemas appendix)_
            - **`signals`**
              - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
                - _(nesting depth limit — see `SignalsFeatureConfiguration` in the Schemas appendix)_
      - `intents` — array **(required)** — Intents resolved from the draft's intents at publish time.
        - _array of_ `IntentSnapshot`
          - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
          - `description` — string
          - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
            - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
              - _(nesting depth limit — see `IntentTextMatch` in the Schemas appendix)_
            - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
              - _(nesting depth limit — see `IntentAiMatch` in the Schemas appendix)_
            - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
          - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
          - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `evaluations` — array **(required)** — Evaluations resolved from the draft's evaluations at publish time.
        - _array of_ `EvaluationSnapshot`
          - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
          - `description` — string
          - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
          - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
            - _array of_ `CopilotField`
              - _(nesting depth limit — see `CopilotField` in the Schemas appendix)_
          - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
          - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `automations` — array **(required)** — Automations resolved from the draft's automations at publish time.
        - _array of_ `AutomationSnapshot`
          - `name` — string **(required)**
          - `description` — string
          - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
            - _oneOf_ — exactly one of:
              - **`agent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
          - `id` — string **(required)** _(minLen=1; maxLen=128)_
      - `assets` — array **(required)** — Assets resolved from the draft's assets at publish time.
        - _array of_ `AssetSnapshot`
          - `key` — string — Stable programmatic key referenced from suggestions and traces.
          - `name` — string **(required)**
          - `description` — string
          - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
          - `title` — string — Card headline.
          - `subtitle` — string
          - `markdown` — string — Markdown body shown on the card.
          - `footer` — string
          - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
          - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
          - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
          - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
            - _oneOf_ — exactly one of:
              - **`card`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`playbook`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`smartAction`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`knowledge`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
          - `id` — string **(required)** _(minLen=1; maxLen=128)_
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
- Errors: `400`, `404`

#### `POST` `/v2/copilot/profiles/{profileId}/versions/{version}/draft`

Replaces the mutable draft with a published version's definition. The draft revision is incremented; published versions and latestVersion are unchanged until the draft is published.

- operationId: `RestoreProfileVersionToDraft`
- **Scopes**: `wilma-copilot:RestoreProfileVersionToDraft`
- **Parameters**
  - `profileId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `version` (path) — number **(required)** — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `RestoreProfileVersionToDraftRequestContent`) **(required)**
  - `revision` — number **(required)** — Draft revision this restore is based on (optimistic locking).
- **Response 200** (`RestoreProfileVersionToDraftResponseContent`)
  - `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
    - `name` — string **(required)**
    - `description` — string
    - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
      - _array of_ `CopilotAudienceEntry`
        - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
        - `values` — array **(required)**
          - _array of_ `string`
    - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
      - _array of_ `CopilotStage`
    - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
      - _array of_ `CopilotChannel`
    - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
    - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
      - _array of_ `CopilotFeature`
        - _oneOf_ — exactly one of:
          - **`csat`**
            - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
          - **`sentiment`**
            - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
          - **`talkRatio`**
            - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
          - **`topics`**
            - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
              - `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
                - _array of_ `string`
              - `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
                - _(nesting depth limit — see `CustomTopicCategory` in the Schemas appendix)_
          - **`contextualKnowledgeAnswers`**
            - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
              - `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
              - `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
                - _array of_ `string`
              - `agentId` — string — Agent used when source is `agent`.
              - `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_
          - **`signals`**
            - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
              - `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
                - _array of_ `string`
    - `assets` — array — Assets referenced by this profile.
      - _array of_ `string`
    - `intents` — array — Intents referenced by this profile.
      - _array of_ `string`
    - `evaluations` — array — Evaluations referenced by this profile.
      - _array of_ `string`
    - `automations` — array — Automations referenced by this profile.
      - _array of_ `string`
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
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
    - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).
- Errors: `400`, `404`, `409`

### Schemas appendix — Wilma Copilot API

<details><summary>128 component schemas</summary>

**`Actor`**

_Who performed an action: an interactive user, an API key or an internal service._

- `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
- `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
- `name` — string — Human readable name of the actor at the time of the action.

**`ActorType`**

- string _(enum: `user`, `api_key`, `service`)_

**`AgentAutomationHandler`**

_Runs a Wilma agent and optionally shows its generated content to the agent._

- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `prompt` — string — Prompt handed to the agent; the live conversation context is added automatically.
- `outputMode` — string — Where the automation's result is delivered. _(enum: `card`, `silent`)_
- `parameters` — array
  - _array of_ `CopilotVariableBinding`
    - `name` — string **(required)**
    - `type` — string — Declared value type, e.g. 'string' or 'number'.
    - `optional` — boolean
    - `variant` — string **(required)** _(enum: `auto`, `guided`, `predefined`)_
    - `description` — string — Guidance for the model when variant is `guided`.
    - `value` — string — Fixed value when variant is `predefined`. Supports handlebars against the session state, e.g. '{{call.remotePhone}}'.

**`Asset`**

_A reusable asset. Referenced by profiles via `assets`._

- `key` — string — Stable programmatic key referenced from suggestions and traces.
- `name` — string **(required)**
- `description` — string
- `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
- `title` — string — Card headline.
- `subtitle` — string
- `markdown` — string — Markdown body shown on the card.
- `footer` — string
- `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
- `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
- `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
- `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`card`**
      - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
        - `content` — union — How a card's body is produced. Exactly one member is set.
          - _(nesting depth limit — see `CardContent` in the Schemas appendix)_
    - **`playbook`**
      - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
        - `goal` — string
        - `steps` — array
          - _(nesting depth limit — see `PlaybookStep` in the Schemas appendix)_
        - `completionCriteria` — union — How a playbook is judged complete. Exactly one member is set.
          - _(nesting depth limit — see `PlaybookCompletionCriteria` in the Schemas appendix)_
    - **`smartAction`**
      - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
        - `actions` — array **(required)**
          - _(nesting depth limit — see `SmartActionItem` in the Schemas appendix)_
    - **`knowledge`**
      - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
        - `summary` — string
        - `sources` — string
- `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
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

**`AssetCard`**

_An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition._

- `content` — union — How a card's body is produced. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`static`**
      - `static` — CardStaticContent **(required)** — Static markdown card content.
        - `markdown` — string
    - **`agent`**
      - `agent` — CardAgentContent **(required)** — Card content generated on demand by an agent.
        - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
        - `variables` — array — Variables passed to the agent when generating the card.
          - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_

**`AssetContent`**

_The kind-specific payload of an asset. Exactly one member is set._

- _oneOf_ — exactly one of:
  - **`card`**
    - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
      - `content` — union — How a card's body is produced. Exactly one member is set.
        - _oneOf_ — exactly one of:
          - **`static`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`agent`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - **`playbook`**
    - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
      - `goal` — string
      - `steps` — array
        - _array of_ `PlaybookStep`
          - _(nesting depth limit — see `PlaybookStep` in the Schemas appendix)_
      - `completionCriteria` — union — How a playbook is judged complete. Exactly one member is set.
        - _oneOf_ — exactly one of:
          - **`manual`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`semantic`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - **`smartAction`**
    - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
      - `actions` — array **(required)**
        - _array of_ `SmartActionItem`
          - _(nesting depth limit — see `SmartActionItem` in the Schemas appendix)_
  - **`knowledge`**
    - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
      - `summary` — string
      - `sources` — string

**`AssetContentType`**

_Which kind of content an asset carries._

- string _(enum: `card`, `playbook`, `smart_action`, `knowledge`)_

**`AssetIcon`**

_Icon shown on the asset card._

- string _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_

**`AssetInfo`**

_Summary entry returned by ListAssets._

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
- `enabled` — boolean **(required)**
- `contentType` — string **(required)** — Which kind of content an asset carries. _(enum: `card`, `playbook`, `smart_action`, `knowledge`)_

**`AssetKnowledge`**

_A knowledge answer with its supporting sources._

- `summary` — string
- `sources` — string

**`AssetPlaybook`**

_A step-by-step playbook for the agent to follow._

- `goal` — string
- `steps` — array
  - _array of_ `PlaybookStep`
    - `id` — string **(required)**
    - `title` — string **(required)**
    - `markdown` — string
    - `required` — boolean — Whether the step must be completed.
    - `autoComplete` — boolean — Whether the system marks the step complete automatically from the transcript. While the playbook is shown and the step is open, a decision model asks whether it is done, judging only what was said after the playbook was shown.
    - `autoCompleteInstructions` — string — What makes the step complete, when autoComplete is set. The decision model reads it as the yes/no it answers.
- `completionCriteria` — union — How a playbook is judged complete. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`manual`**
      - `manual` — PlaybookManualCompletion **(required)** — The playbook is completed manually by the agent.
        - `allowAgentMarkComplete` — boolean **(required)**
    - **`semantic`**
      - `semantic` — PlaybookSemanticCompletion **(required)** — The playbook is completed automatically when a decision model judges its goal met, judging only what was said after the playbook was shown.
        - `description` — string **(required)**
        - `examples` — array
          - _array of_ `string`

**`AssetSeverity`**

_Visual emphasis of the asset card._

- string _(enum: `neutral`, `success`, `warning`, `danger`)_

**`AssetSmartActions`**

_A set of one-click smart actions offered to the agent._

- `actions` — array **(required)**
  - _array of_ `SmartActionItem`
    - `id` — string **(required)**
    - `label` — string **(required)**
    - `description` — string
    - `action` — union **(required)** — A button shown under an asset. Exactly one member is set; it selects what happens when clicked.
      - _oneOf_ — exactly one of:
        - **`openUrl`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`runAgent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`handover`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_

**`AssetSnapshot`**

_Immutable asset snapshot embedded in a published profile version._

- `key` — string — Stable programmatic key referenced from suggestions and traces.
- `name` — string **(required)**
- `description` — string
- `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
- `title` — string — Card headline.
- `subtitle` — string
- `markdown` — string — Markdown body shown on the card.
- `footer` — string
- `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
- `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
- `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
- `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`card`**
      - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
        - `content` — union — How a card's body is produced. Exactly one member is set.
          - _(nesting depth limit — see `CardContent` in the Schemas appendix)_
    - **`playbook`**
      - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
        - `goal` — string
        - `steps` — array
          - _(nesting depth limit — see `PlaybookStep` in the Schemas appendix)_
        - `completionCriteria` — union — How a playbook is judged complete. Exactly one member is set.
          - _(nesting depth limit — see `PlaybookCompletionCriteria` in the Schemas appendix)_
    - **`smartAction`**
      - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
        - `actions` — array **(required)**
          - _(nesting depth limit — see `SmartActionItem` in the Schemas appendix)_
    - **`knowledge`**
      - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
        - `summary` — string
        - `sources` — string
- `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
- `id` — string **(required)** _(minLen=1; maxLen=128)_

**`AttachProfileResourceRequestContent`**

- `revision` — number **(required)** — Draft revision this update is based on (optimistic locking).
- `resource` — union **(required)** — One feature or reusable library resource attached to a profile.
  - _oneOf_ — exactly one of:
    - **`feature`**
      - `feature` — union **(required)** — A Copilot feature enabled for a profile, with its type-specific configuration.
        - _oneOf_ — exactly one of:
          - **`csat`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`sentiment`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`talkRatio`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`topics`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`contextualKnowledgeAnswers`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`signals`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - **`asset`**
      - `asset` — string **(required)** _(minLen=1; maxLen=128)_
    - **`automation`**
      - `automation` — string **(required)** _(minLen=1; maxLen=128)_
    - **`intent`**
      - `intent` — string **(required)** _(minLen=1; maxLen=128)_
    - **`evaluation`**
      - `evaluation` — string **(required)** _(minLen=1; maxLen=128)_

**`AttachProfileResourceResponseContent`**

- `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
  - `name` — string **(required)**
  - `description` — string
  - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
    - _array of_ `CopilotAudienceEntry`
      - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
      - `values` — array **(required)**
        - _array of_ `string`
  - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
    - _array of_ `CopilotStage`
  - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
    - _array of_ `CopilotChannel`
  - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
  - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
    - _array of_ `CopilotFeature`
      - _oneOf_ — exactly one of:
        - **`csat`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sentiment`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`talkRatio`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`topics`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`contextualKnowledgeAnswers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`signals`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `assets` — array — Assets referenced by this profile.
    - _array of_ `string`
  - `intents` — array — Intents referenced by this profile.
    - _array of_ `string`
  - `evaluations` — array — Evaluations referenced by this profile.
    - _array of_ `string`
  - `automations` — array — Automations referenced by this profile.
    - _array of_ `string`
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
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
  - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).

**`Automation`**

_A reusable automation. Referenced by profiles via `automations`._

- `name` — string **(required)**
- `description` — string
- `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`agent`**
      - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
        - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
        - `prompt` — string — Prompt handed to the agent; the live conversation context is added automatically.
        - `outputMode` — string — Where the automation's result is delivered. _(enum: `card`, `silent`)_
        - `parameters` — array
          - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_
- `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
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

**`AutomationHandler`**

_What the automation does when it fires. Exactly one member is set._

- _oneOf_ — exactly one of:
  - **`agent`**
    - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `prompt` — string — Prompt handed to the agent; the live conversation context is added automatically.
      - `outputMode` — string — Where the automation's result is delivered. _(enum: `card`, `silent`)_
      - `parameters` — array
        - _array of_ `CopilotVariableBinding`
          - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_

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

**`AutomationOutputMode`**

_Where the automation's result is delivered._

- string _(enum: `card`, `silent`)_

**`AutomationSnapshot`**

_Immutable automation snapshot embedded in a published profile version._

- `name` — string **(required)**
- `description` — string
- `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`agent`**
      - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
        - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
        - `prompt` — string — Prompt handed to the agent; the live conversation context is added automatically.
        - `outputMode` — string — Where the automation's result is delivered. _(enum: `card`, `silent`)_
        - `parameters` — array
          - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_
- `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
- `id` — string **(required)** _(minLen=1; maxLen=128)_

**`CardAgentContent`**

_Card content generated on demand by an agent._

- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `variables` — array — Variables passed to the agent when generating the card.
  - _array of_ `CopilotVariableBinding`
    - `name` — string **(required)**
    - `type` — string — Declared value type, e.g. 'string' or 'number'.
    - `optional` — boolean
    - `variant` — string **(required)** _(enum: `auto`, `guided`, `predefined`)_
    - `description` — string — Guidance for the model when variant is `guided`.
    - `value` — string — Fixed value when variant is `predefined`. Supports handlebars against the session state, e.g. '{{call.remotePhone}}'.

**`CardContent`**

_How a card's body is produced. Exactly one member is set._

- _oneOf_ — exactly one of:
  - **`static`**
    - `static` — CardStaticContent **(required)** — Static markdown card content.
      - `markdown` — string
  - **`agent`**
    - `agent` — CardAgentContent **(required)** — Card content generated on demand by an agent.
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `variables` — array — Variables passed to the agent when generating the card.
        - _array of_ `CopilotVariableBinding`
          - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_

**`CardStaticContent`**

_Static markdown card content._

- `markdown` — string

**`CompareProfileVersionsResponseContent`**

- `changes` — array **(required)**
  - _array of_ `ProfileVersionChange`
    - `path` — string **(required)** — JSON pointer of the changed field within the profile definition, e.g. '/assets/0/markdown'.
    - `before` — any — Value before the change (absent when the field was added).
    - `after` — any — Value after the change (absent when the field was removed).

**`ConflictExceptionResponseContent`**

_The request conflicts with the current state of the resource, e.g. a duplicate name, a resource still in use, or an unmet precondition._

- `message` — string **(required)**

**`ContextualKnowledgeAnswersFeatureConfiguration`**

_Configuration for the built-in contextual knowledge answers feature._

- `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
- `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
  - _array of_ `string`
- `agentId` — string — Agent used when source is `agent`.
- `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_

**`ContextualKnowledgeMode`**

_How contextual-knowledge answers are surfaced._

- string _(enum: `suggest_action`, `automatic_answer`)_

**`ContextualKnowledgeSource`**

_Where contextual-knowledge answers are sourced from._

- string _(enum: `knowledge_bases`, `agent`)_

**`CopilotAudienceEntry`**

_One audience entry: a kind, and the values of that kind the profile assists. An entry with no values does not narrow anything._

- `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
- `values` — array **(required)**
  - _array of_ `string`

**`CopilotAudienceKind`**

_The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`._

- string _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_

**`CopilotChannel`**

_The kind of conversation a copilot resource applies to. Singular members and no wildcard, unlike the `calls | chats | any` field this replaces - and `conference` is nameable for the first time. Note that this is the *conversation* channel, not the Wilma runtime channel (`assistant` / `chat` / `voice`) and not the messaging service a chat arrived on (which is `chat.service`)._

- string _(enum: `call`, `conference`, `chat`)_

**`CopilotFeature`**

_A Copilot feature enabled for a profile, with its type-specific configuration._

- _oneOf_ — exactly one of:
  - **`csat`**
    - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
  - **`sentiment`**
    - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
  - **`talkRatio`**
    - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
  - **`topics`**
    - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
      - `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
        - _array of_ `string`
      - `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
        - _array of_ `CustomTopicCategory`
          - _(nesting depth limit — see `CustomTopicCategory` in the Schemas appendix)_
  - **`contextualKnowledgeAnswers`**
    - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
      - `source` — string **(required)** — Where contextual-knowledge answers are sourced from. _(enum: `knowledge_bases`, `agent`)_
      - `knowledgeBaseIds` — array — Knowledge bases used when source is `knowledge_bases`.
        - _array of_ `string`
      - `agentId` — string — Agent used when source is `agent`.
      - `mode` — string **(required)** — How contextual-knowledge answers are surfaced. _(enum: `suggest_action`, `automatic_answer`)_
  - **`signals`**
    - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
      - `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
        - _array of_ `string`

**`CopilotField`**

_A named value the model extracts from the transcript, shared by intent AI matching and evaluations._

- `id` — string **(required)**
- `name` — string **(required)**
- `description` — string
- `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
- `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
  - _oneOf_ — exactly one of:
    - **`text`**
      - `text` — CopilotTextParameter **(required)** — Free-form single-line text value.
        - `examples` — array — Example values that steer extraction.
          - _array of_ `string`
    - **`multiline`**
      - `multiline` — CopilotMultilineParameter **(required)** — Free-form multi-line text value.
        - `examples` — array
          - _array of_ `string`
    - **`number`**
      - `number` — CopilotNumberParameter **(required)** — Numeric value with optional bounds.
        - `min` — number
        - `max` — number
    - **`selection`**
      - `selection` — CopilotSelectionParameter **(required)** — Value chosen from a fixed (or AI-extended) set of options.
        - `options` — array **(required)** — The allowed options.
          - _array of_ `string`
        - `multi` — boolean — Whether more than one option may be selected.
        - `adaptive` — boolean — Whether the model may introduce new options beyond `options`.
        - `adaptiveOptions` — array — Options the model introduced when `adaptive` is enabled.
          - _array of_ `string`

**`CopilotFieldParameter`**

_The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value._

- _oneOf_ — exactly one of:
  - **`text`**
    - `text` — CopilotTextParameter **(required)** — Free-form single-line text value.
      - `examples` — array — Example values that steer extraction.
        - _array of_ `string`
  - **`multiline`**
    - `multiline` — CopilotMultilineParameter **(required)** — Free-form multi-line text value.
      - `examples` — array
        - _array of_ `string`
  - **`number`**
    - `number` — CopilotNumberParameter **(required)** — Numeric value with optional bounds.
      - `min` — number
      - `max` — number
  - **`selection`**
    - `selection` — CopilotSelectionParameter **(required)** — Value chosen from a fixed (or AI-extended) set of options.
      - `options` — array **(required)** — The allowed options.
        - _array of_ `string`
      - `multi` — boolean — Whether more than one option may be selected.
      - `adaptive` — boolean — Whether the model may introduce new options beyond `options`.
      - `adaptiveOptions` — array — Options the model introduced when `adaptive` is enabled.
        - _array of_ `string`

**`CopilotMultilineParameter`**

_Free-form multi-line text value._

- `examples` — array
  - _array of_ `string`

**`CopilotNumberParameter`**

_Numeric value with optional bounds._

- `min` — number
- `max` — number

**`CopilotSelectionParameter`**

_Value chosen from a fixed (or AI-extended) set of options._

- `options` — array **(required)** — The allowed options.
  - _array of_ `string`
- `multi` — boolean — Whether more than one option may be selected.
- `adaptive` — boolean — Whether the model may introduce new options beyond `options`.
- `adaptiveOptions` — array — Options the model introduced when `adaptive` is enabled.
  - _array of_ `string`

**`CopilotSpeaker`**

_Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`)._

- string _(enum: `anyone`, `agent`, `customer`)_

**`CopilotStage`**

_Where in a conversation's life a copilot resource applies. `before` is the pre-conversation session copilot opens from a client lookup (`Open` in `wildix.wilma.copilot.sessions`): a customer is on screen and no call, conference or chat exists yet. `during` is a live conversation. `after` is everything from the conversation ending onwards - wrap-up, and the post-conversation summary that carries CSAT and topics. A conversation that has not started has no channel and no queue, which is the one rule the other two members of this triple follow from: see `CopilotChannelList` and `CopilotAudienceKind`._

- string _(enum: `before`, `during`, `after`)_

**`CopilotTextParameter`**

_Free-form single-line text value._

- `examples` — array — Example values that steer extraction.
  - _array of_ `string`

**`CopilotVariableBinding`**

_Binds an input variable of an agent or tool invocation to a value or a fill strategy._

- `name` — string **(required)**
- `type` — string — Declared value type, e.g. 'string' or 'number'.
- `optional` — boolean
- `variant` — string **(required)** _(enum: `auto`, `guided`, `predefined`)_
- `description` — string — Guidance for the model when variant is `guided`.
- `value` — string — Fixed value when variant is `predefined`. Supports handlebars against the session state, e.g. '{{call.remotePhone}}'.

**`CopilotVariableMode`**

- string _(enum: `auto`, `guided`, `predefined`)_

**`CreateAssetRequestContent`**

_The editable definition of an asset._

- `key` — string — Stable programmatic key referenced from suggestions and traces.
- `name` — string **(required)**
- `description` — string
- `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
- `title` — string — Card headline.
- `subtitle` — string
- `markdown` — string — Markdown body shown on the card.
- `footer` — string
- `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
- `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
- `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
- `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`card`**
      - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
        - `content` — union — How a card's body is produced. Exactly one member is set.
          - _(nesting depth limit — see `CardContent` in the Schemas appendix)_
    - **`playbook`**
      - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
        - `goal` — string
        - `steps` — array
          - _(nesting depth limit — see `PlaybookStep` in the Schemas appendix)_
        - `completionCriteria` — union — How a playbook is judged complete. Exactly one member is set.
          - _(nesting depth limit — see `PlaybookCompletionCriteria` in the Schemas appendix)_
    - **`smartAction`**
      - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
        - `actions` — array **(required)**
          - _(nesting depth limit — see `SmartActionItem` in the Schemas appendix)_
    - **`knowledge`**
      - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
        - `summary` — string
        - `sources` — string
- `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.

**`CreateAssetResponseContent`**

- `asset` — Asset **(required)** — A reusable asset. Referenced by profiles via `assets`.
  - `key` — string — Stable programmatic key referenced from suggestions and traces.
  - `name` — string **(required)**
  - `description` — string
  - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
  - `title` — string — Card headline.
  - `subtitle` — string
  - `markdown` — string — Markdown body shown on the card.
  - `footer` — string
  - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
  - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
  - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
  - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`card`**
        - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
          - _(nesting depth limit — see `AssetCard` in the Schemas appendix)_
      - **`playbook`**
        - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
          - _(nesting depth limit — see `AssetPlaybook` in the Schemas appendix)_
      - **`smartAction`**
        - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
          - _(nesting depth limit — see `AssetSmartActions` in the Schemas appendix)_
      - **`knowledge`**
        - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
          - _(nesting depth limit — see `AssetKnowledge` in the Schemas appendix)_
  - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
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

**`CreateAutomationRequestContent`**

_The editable definition of an automation._

- `name` — string **(required)**
- `description` — string
- `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`agent`**
      - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
        - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
        - `prompt` — string — Prompt handed to the agent; the live conversation context is added automatically.
        - `outputMode` — string — Where the automation's result is delivered. _(enum: `card`, `silent`)_
        - `parameters` — array
          - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_
- `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.

**`CreateAutomationResponseContent`**

- `automation` — Automation **(required)** — A reusable automation. Referenced by profiles via `automations`.
  - `name` — string **(required)**
  - `description` — string
  - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`agent`**
        - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
          - _(nesting depth limit — see `AgentAutomationHandler` in the Schemas appendix)_
  - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
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

**`CreateEvaluationRequestContent`**

_The editable definition of an evaluation._

- `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
- `description` — string
- `instructions` — string **(required)** — Prompt the model follows to score the transcript.
- `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
  - _array of_ `CopilotField`
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `description` — string
    - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
    - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
      - _oneOf_ — exactly one of:
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`multiline`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`number`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`selection`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `conditions` — any — Extra conditions gating whether this evaluation runs for a session.

**`CreateEvaluationResponseContent`**

- `evaluation` — Evaluation **(required)** — A reusable evaluation. Referenced by profiles via `evaluations`.
  - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
  - `description` — string
  - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
  - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
    - _array of_ `CopilotField`
      - `id` — string **(required)**
      - `name` — string **(required)**
      - `description` — string
      - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
      - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
        - _(nesting depth limit — see `CopilotFieldParameter` in the Schemas appendix)_
  - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
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

**`CreateIntentRequestContent`**

_The editable definition of an intent._

- `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
- `description` — string
- `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
  - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
    - `options` — array
      - _array of_ `IntentTextMatchOption`
        - _(nesting depth limit — see `IntentTextMatchOption` in the Schemas appendix)_
  - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
    - `instructions` — string — Prompt describing when this intent applies.
    - `fields` — array — Structured values the model extracts when the intent matches.
      - _array of_ `CopilotField`
        - _(nesting depth limit — see `CopilotField` in the Schemas appendix)_
  - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
- `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.

**`CreateIntentResponseContent`**

- `intent` — Intent **(required)** — A reusable intent. Referenced by profiles via `intents`.
  - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
  - `description` — string
  - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
    - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
      - `options` — array
        - _(nesting depth limit — see `IntentTextMatchOption` in the Schemas appendix)_
    - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
      - `instructions` — string — Prompt describing when this intent applies.
      - `fields` — array — Structured values the model extracts when the intent matches.
        - _(nesting depth limit — see `CopilotField` in the Schemas appendix)_
    - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
  - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
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

**`CreateProfileRequestContent`**

_The editable definition of a profile: metadata plus attached features and library resources. A session asks a decision model at most 200 configured questions, counted across every profile that applies to it, a question shared by two profiles counting once: each topic category and topic, built-in or custom, each included signal, each intent and each evaluation. Questions copilot adds on its own (field guards, playbook steps, closing detection) do not count. Past the limit, the questions are sorted by their `<kind>.<name>` key (`evaluations.upsell`, `intents.refund`, `signals.escalation_requested`, `topics.billing`); those after the first 200 are not asked, and the session trace says which._

- `name` — string **(required)**
- `description` — string
- `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
  - _array of_ `CopilotAudienceEntry`
    - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
    - `values` — array **(required)**
      - _array of_ `string`
- `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
  - _array of_ `CopilotStage`
- `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
  - _array of_ `CopilotChannel`
- `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
- `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
  - _array of_ `CopilotFeature`
    - _oneOf_ — exactly one of:
      - **`csat`**
        - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
      - **`sentiment`**
        - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
      - **`talkRatio`**
        - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
      - **`topics`**
        - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
          - _(nesting depth limit — see `TopicsFeatureConfiguration` in the Schemas appendix)_
      - **`contextualKnowledgeAnswers`**
        - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
          - _(nesting depth limit — see `ContextualKnowledgeAnswersFeatureConfiguration` in the Schemas appendix)_
      - **`signals`**
        - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
          - _(nesting depth limit — see `SignalsFeatureConfiguration` in the Schemas appendix)_
- `assets` — array — Assets referenced by this profile.
  - _array of_ `string`
- `intents` — array — Intents referenced by this profile.
  - _array of_ `string`
- `evaluations` — array — Evaluations referenced by this profile.
  - _array of_ `string`
- `automations` — array — Automations referenced by this profile.
  - _array of_ `string`

**`CreateProfileResponseContent`**

- `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
  - `name` — string **(required)**
  - `description` — string
  - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
    - _array of_ `CopilotAudienceEntry`
      - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
      - `values` — array **(required)**
        - _array of_ `string`
  - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
    - _array of_ `CopilotStage`
  - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
    - _array of_ `CopilotChannel`
  - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
  - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
    - _array of_ `CopilotFeature`
      - _oneOf_ — exactly one of:
        - **`csat`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sentiment`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`talkRatio`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`topics`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`contextualKnowledgeAnswers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`signals`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `assets` — array — Assets referenced by this profile.
    - _array of_ `string`
  - `intents` — array — Intents referenced by this profile.
    - _array of_ `string`
  - `evaluations` — array — Evaluations referenced by this profile.
    - _array of_ `string`
  - `automations` — array — Automations referenced by this profile.
    - _array of_ `string`
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
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
  - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).

**`CsatFeatureConfiguration`**

_Configuration for the built-in CSAT feature._

- CsatFeatureConfiguration

**`CustomTopic`**

_A topic of the company's own, in the category that holds it._

- `name` — string **(required)** — The topic's name in `topics` and in conditions; not a name the catalog already uses. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=64)_
- `description` — string **(required)** — What the conversation covers when this topic applies, as the decision model reads it, e.g. 'Customer pays, or asks about paying, by Mastercard'. _(minLen=1; maxLen=500)_

**`CustomTopicCategory`**

_A topic category of the company's own, or the company's topics in a built-in category. A new category is asked like a built-in one, and its topics once it is detected._

- `name` — string **(required)** — A new category's name, or the name of the built-in category its topics are added to. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=64)_
- `description` — string — What a new category covers, as the decision model reads it: required for a new category, and left out when extending a built-in one, which keeps its own. _(minLen=1; maxLen=500)_
- `topics` — array **(required)** _(minItems=1; maxItems=64)_
  - _array of_ `CustomTopic`
    - `name` — string **(required)** — The topic's name in `topics` and in conditions; not a name the catalog already uses. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=64)_
    - `description` — string **(required)** — What the conversation covers when this topic applies, as the decision model reads it, e.g. 'Customer pays, or asks about paying, by Mastercard'. _(minLen=1; maxLen=500)_

**`DeleteProfileResourceResponseContent`**

- `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
  - `name` — string **(required)**
  - `description` — string
  - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
    - _array of_ `CopilotAudienceEntry`
      - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
      - `values` — array **(required)**
        - _array of_ `string`
  - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
    - _array of_ `CopilotStage`
  - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
    - _array of_ `CopilotChannel`
  - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
  - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
    - _array of_ `CopilotFeature`
      - _oneOf_ — exactly one of:
        - **`csat`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sentiment`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`talkRatio`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`topics`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`contextualKnowledgeAnswers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`signals`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `assets` — array — Assets referenced by this profile.
    - _array of_ `string`
  - `intents` — array — Intents referenced by this profile.
    - _array of_ `string`
  - `evaluations` — array — Evaluations referenced by this profile.
    - _array of_ `string`
  - `automations` — array — Automations referenced by this profile.
    - _array of_ `string`
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
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
  - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).

**`DisableProfileResponseContent`**

- `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
  - `name` — string **(required)**
  - `description` — string
  - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
    - _array of_ `CopilotAudienceEntry`
      - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
      - `values` — array **(required)**
        - _array of_ `string`
  - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
    - _array of_ `CopilotStage`
  - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
    - _array of_ `CopilotChannel`
  - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
  - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
    - _array of_ `CopilotFeature`
      - _oneOf_ — exactly one of:
        - **`csat`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sentiment`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`talkRatio`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`topics`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`contextualKnowledgeAnswers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`signals`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `assets` — array — Assets referenced by this profile.
    - _array of_ `string`
  - `intents` — array — Intents referenced by this profile.
    - _array of_ `string`
  - `evaluations` — array — Evaluations referenced by this profile.
    - _array of_ `string`
  - `automations` — array — Automations referenced by this profile.
    - _array of_ `string`
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
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
  - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).

**`EnableProfileResponseContent`**

- `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
  - `name` — string **(required)**
  - `description` — string
  - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
    - _array of_ `CopilotAudienceEntry`
      - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
      - `values` — array **(required)**
        - _array of_ `string`
  - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
    - _array of_ `CopilotStage`
  - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
    - _array of_ `CopilotChannel`
  - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
  - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
    - _array of_ `CopilotFeature`
      - _oneOf_ — exactly one of:
        - **`csat`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sentiment`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`talkRatio`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`topics`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`contextualKnowledgeAnswers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`signals`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `assets` — array — Assets referenced by this profile.
    - _array of_ `string`
  - `intents` — array — Intents referenced by this profile.
    - _array of_ `string`
  - `evaluations` — array — Evaluations referenced by this profile.
    - _array of_ `string`
  - `automations` — array — Automations referenced by this profile.
    - _array of_ `string`
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
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
  - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).

**`Evaluation`**

_A reusable evaluation. Referenced by profiles via `evaluations`._

- `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
- `description` — string
- `instructions` — string **(required)** — Prompt the model follows to score the transcript.
- `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
  - _array of_ `CopilotField`
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `description` — string
    - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
    - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
      - _oneOf_ — exactly one of:
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`multiline`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`number`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`selection`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
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

**`EvaluationInfo`**

_Summary entry returned by ListEvaluations._

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
- `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
- `description` — string

**`EvaluationSnapshot`**

_Immutable evaluation snapshot embedded in a published profile version._

- `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
- `description` — string
- `instructions` — string **(required)** — Prompt the model follows to score the transcript.
- `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
  - _array of_ `CopilotField`
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `description` — string
    - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
    - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
      - _oneOf_ — exactly one of:
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`multiline`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`number`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`selection`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
- `id` — string **(required)** _(minLen=1; maxLen=128)_

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetAssetResponseContent`**

- `asset` — Asset **(required)** — A reusable asset. Referenced by profiles via `assets`.
  - `key` — string — Stable programmatic key referenced from suggestions and traces.
  - `name` — string **(required)**
  - `description` — string
  - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
  - `title` — string — Card headline.
  - `subtitle` — string
  - `markdown` — string — Markdown body shown on the card.
  - `footer` — string
  - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
  - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
  - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
  - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`card`**
        - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
          - _(nesting depth limit — see `AssetCard` in the Schemas appendix)_
      - **`playbook`**
        - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
          - _(nesting depth limit — see `AssetPlaybook` in the Schemas appendix)_
      - **`smartAction`**
        - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
          - _(nesting depth limit — see `AssetSmartActions` in the Schemas appendix)_
      - **`knowledge`**
        - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
          - _(nesting depth limit — see `AssetKnowledge` in the Schemas appendix)_
  - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
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

**`GetAutomationResponseContent`**

- `automation` — Automation **(required)** — A reusable automation. Referenced by profiles via `automations`.
  - `name` — string **(required)**
  - `description` — string
  - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`agent`**
        - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
          - _(nesting depth limit — see `AgentAutomationHandler` in the Schemas appendix)_
  - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
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

**`GetEvaluationResponseContent`**

- `evaluation` — Evaluation **(required)** — A reusable evaluation. Referenced by profiles via `evaluations`.
  - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
  - `description` — string
  - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
  - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
    - _array of_ `CopilotField`
      - `id` — string **(required)**
      - `name` — string **(required)**
      - `description` — string
      - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
      - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
        - _(nesting depth limit — see `CopilotFieldParameter` in the Schemas appendix)_
  - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
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

**`GetIntentResponseContent`**

- `intent` — Intent **(required)** — A reusable intent. Referenced by profiles via `intents`.
  - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
  - `description` — string
  - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
    - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
      - `options` — array
        - _(nesting depth limit — see `IntentTextMatchOption` in the Schemas appendix)_
    - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
      - `instructions` — string — Prompt describing when this intent applies.
      - `fields` — array — Structured values the model extracts when the intent matches.
        - _(nesting depth limit — see `CopilotField` in the Schemas appendix)_
    - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
  - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
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

**`GetProfileResponseContent`**

- `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
  - `name` — string **(required)**
  - `description` — string
  - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
    - _array of_ `CopilotAudienceEntry`
      - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
      - `values` — array **(required)**
        - _array of_ `string`
  - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
    - _array of_ `CopilotStage`
  - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
    - _array of_ `CopilotChannel`
  - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
  - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
    - _array of_ `CopilotFeature`
      - _oneOf_ — exactly one of:
        - **`csat`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sentiment`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`talkRatio`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`topics`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`contextualKnowledgeAnswers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`signals`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `assets` — array — Assets referenced by this profile.
    - _array of_ `string`
  - `intents` — array — Intents referenced by this profile.
    - _array of_ `string`
  - `evaluations` — array — Evaluations referenced by this profile.
    - _array of_ `string`
  - `automations` — array — Automations referenced by this profile.
    - _array of_ `string`
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
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
  - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).

**`GetProfileVersionResponseContent`**

- `version` — ProfileVersion **(required)** — Published profile version: an immutable, self-contained snapshot of the profile at publish time.
  - `profileId` — string **(required)** _(minLen=1; maxLen=128)_
  - `version` — number **(required)** — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
  - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
  - `definition` — ProfileDefinitionSnapshot **(required)** — Immutable snapshot of a profile definition at publish time, with all referenced library resources resolved inline.
    - `name` — string **(required)**
    - `description` — string
    - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
      - _array of_ `CopilotAudienceEntry`
        - _(nesting depth limit — see `CopilotAudienceEntry` in the Schemas appendix)_
    - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
      - _array of_ `CopilotStage`
    - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
      - _array of_ `CopilotChannel`
    - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
    - `features` — array — Copilot features enabled for this profile at publish time, including their type-specific configuration.
      - _array of_ `CopilotFeature`
        - _(nesting depth limit — see `CopilotFeature` in the Schemas appendix)_
    - `intents` — array **(required)** — Intents resolved from the draft's intents at publish time.
      - _array of_ `IntentSnapshot`
        - _(nesting depth limit — see `IntentSnapshot` in the Schemas appendix)_
    - `evaluations` — array **(required)** — Evaluations resolved from the draft's evaluations at publish time.
      - _array of_ `EvaluationSnapshot`
        - _(nesting depth limit — see `EvaluationSnapshot` in the Schemas appendix)_
    - `automations` — array **(required)** — Automations resolved from the draft's automations at publish time.
      - _array of_ `AutomationSnapshot`
        - _(nesting depth limit — see `AutomationSnapshot` in the Schemas appendix)_
    - `assets` — array **(required)** — Assets resolved from the draft's assets at publish time.
      - _array of_ `AssetSnapshot`
        - _(nesting depth limit — see `AssetSnapshot` in the Schemas appendix)_
  - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.

**`Intent`**

_A reusable intent. Referenced by profiles via `intents`._

- `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
- `description` — string
- `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
  - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
    - `options` — array
      - _array of_ `IntentTextMatchOption`
        - _(nesting depth limit — see `IntentTextMatchOption` in the Schemas appendix)_
  - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
    - `instructions` — string — Prompt describing when this intent applies.
    - `fields` — array — Structured values the model extracts when the intent matches.
      - _array of_ `CopilotField`
        - _(nesting depth limit — see `CopilotField` in the Schemas appendix)_
  - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
- `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
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

**`IntentAiMatch`**

_Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are._

- `instructions` — string — Prompt describing when this intent applies.
- `fields` — array — Structured values the model extracts when the intent matches.
  - _array of_ `CopilotField`
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `description` — string
    - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
    - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
      - _oneOf_ — exactly one of:
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`multiline`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`number`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`selection`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_

**`IntentHandlers`**

_The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected._

- `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
  - `options` — array
    - _array of_ `IntentTextMatchOption`
      - `id` — string **(required)**
      - `value` — string **(required)** — The phrase, word or pattern to look for, e.g. 'refund', 'W-AIR' or a regex.
      - `mode` — string **(required)** — How a literal phrase is compared against the transcript. _(enum: `exact`, `fuzzy`, `regex`)_
- `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
  - `instructions` — string — Prompt describing when this intent applies.
  - `fields` — array — Structured values the model extracts when the intent matches.
    - _array of_ `CopilotField`
      - `id` — string **(required)**
      - `name` — string **(required)**
      - `description` — string
      - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
      - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
        - _(nesting depth limit — see `CopilotFieldParameter` in the Schemas appendix)_
- `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_

**`IntentInfo`**

_Summary entry returned by ListIntents._

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
- `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
- `description` — string
- `textMatchEnabled` — boolean **(required)** — Whether literal text matching is enabled, i.e. whether `handlers.textMatch` is set.
- `aiMatchEnabled` — boolean **(required)** — Whether semantic AI matching is enabled, i.e. whether `handlers.aiMatch` is set.

**`IntentSnapshot`**

_Immutable intent snapshot embedded in a published profile version._

- `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
- `description` — string
- `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
  - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
    - `options` — array
      - _array of_ `IntentTextMatchOption`
        - _(nesting depth limit — see `IntentTextMatchOption` in the Schemas appendix)_
  - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
    - `instructions` — string — Prompt describing when this intent applies.
    - `fields` — array — Structured values the model extracts when the intent matches.
      - _array of_ `CopilotField`
        - _(nesting depth limit — see `CopilotField` in the Schemas appendix)_
  - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
- `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
- `id` — string **(required)** _(minLen=1; maxLen=128)_

**`IntentTextMatch`**

_Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation._

- `options` — array
  - _array of_ `IntentTextMatchOption`
    - `id` — string **(required)**
    - `value` — string **(required)** — The phrase, word or pattern to look for, e.g. 'refund', 'W-AIR' or a regex.
    - `mode` — string **(required)** — How a literal phrase is compared against the transcript. _(enum: `exact`, `fuzzy`, `regex`)_

**`IntentTextMatchMode`**

_How a literal phrase is compared against the transcript._

- string _(enum: `exact`, `fuzzy`, `regex`)_

**`IntentTextMatchOption`**

- `id` — string **(required)**
- `value` — string **(required)** — The phrase, word or pattern to look for, e.g. 'refund', 'W-AIR' or a regex.
- `mode` — string **(required)** — How a literal phrase is compared against the transcript. _(enum: `exact`, `fuzzy`, `regex`)_

**`ListAssetsResponseContent`**

- `assets` — array **(required)**
  - _array of_ `AssetInfo`
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
    - `enabled` — boolean **(required)**
    - `contentType` — string **(required)** — Which kind of content an asset carries. _(enum: `card`, `playbook`, `smart_action`, `knowledge`)_
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

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
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListEvaluationsResponseContent`**

- `evaluations` — array **(required)**
  - _array of_ `EvaluationInfo`
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
    - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
    - `description` — string
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListIntentsResponseContent`**

- `intents` — array **(required)**
  - _array of_ `IntentInfo`
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
    - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
    - `description` — string
    - `textMatchEnabled` — boolean **(required)** — Whether literal text matching is enabled, i.e. whether `handlers.textMatch` is set.
    - `aiMatchEnabled` — boolean **(required)** — Whether semantic AI matching is enabled, i.e. whether `handlers.aiMatch` is set.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListProfileVersionsResponseContent`**

- `versions` — array **(required)**
  - _array of_ `ProfileVersionInfo`
    - `profileId` — string **(required)** _(minLen=1; maxLen=128)_
    - `version` — number **(required)** — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
    - `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `latest` — boolean — True when this version is the profile's latestVersion.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListProfilesResponseContent`**

- `profiles` — array **(required)**
  - _array of_ `ProfileInfo`
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
    - `audience` — array — The profile's targeting, so a list row can say what it applies to without reading the definition.
      - _array of_ `CopilotAudienceEntry`
        - _(nesting depth limit — see `CopilotAudienceEntry` in the Schemas appendix)_
    - `stages` — array — Stages a resource applies in. An empty or absent list means every stage.
      - _array of_ `CopilotStage`
    - `channels` — array — Conversation channels a resource applies to. An empty or absent list means every channel. A channel filter only constrains the `during` and `after` stages: in `before` there is nothing to be a call, a conference or a chat, so a resource covering only `before` applies whatever this list says.
      - _array of_ `CopilotChannel`
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `live` — boolean **(required)**
    - `latestVersion` — number — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
    - `intentCount` — number — Number of referenced intents.
    - `evaluationCount` — number — Number of referenced evaluations.
    - `automationCount` — number — Number of referenced automations.
    - `assetCount` — number — Number of referenced assets.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListSubscriptionsResponseContent`**

_The answer to 'what should I send you': one entry per tenant that needs anything at all, and every tenant in one response — the producer holds a single routing table, and a listing it has to assemble from several requests is one that can be applied half-built, which is indistinguishable from a set of tenants that unsubscribed. A tenant absent from the listing needs nothing, and the producer sends it nothing. Ordering is unspecified._

- `subscriptions` — array **(required)**
  - _array of_ `Subscription`
    - `company` — string **(required)** _(minLen=3; maxLen=30)_
    - `selectors` — array **(required)** — Event types one tenant needs, deduplicated across everything that asked for them. Two selectors never name the same event type. The producer sends every occurrence of each listed type. _(minItems=1; maxItems=200)_
      - _array of_ `SubscriptionSelector`
        - _(nesting depth limit — see `SubscriptionSelector` in the Schemas appendix)_

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`PlaybookCompletionCriteria`**

_How a playbook is judged complete. Exactly one member is set._

- _oneOf_ — exactly one of:
  - **`manual`**
    - `manual` — PlaybookManualCompletion **(required)** — The playbook is completed manually by the agent.
      - `allowAgentMarkComplete` — boolean **(required)**
  - **`semantic`**
    - `semantic` — PlaybookSemanticCompletion **(required)** — The playbook is completed automatically when a decision model judges its goal met, judging only what was said after the playbook was shown.
      - `description` — string **(required)**
      - `examples` — array
        - _array of_ `string`

**`PlaybookManualCompletion`**

_The playbook is completed manually by the agent._

- `allowAgentMarkComplete` — boolean **(required)**

**`PlaybookSemanticCompletion`**

_The playbook is completed automatically when a decision model judges its goal met, judging only what was said after the playbook was shown._

- `description` — string **(required)**
- `examples` — array
  - _array of_ `string`

**`PlaybookStep`**

- `id` — string **(required)**
- `title` — string **(required)**
- `markdown` — string
- `required` — boolean — Whether the step must be completed.
- `autoComplete` — boolean — Whether the system marks the step complete automatically from the transcript. While the playbook is shown and the step is open, a decision model asks whether it is done, judging only what was said after the playbook was shown.
- `autoCompleteInstructions` — string — What makes the step complete, when autoComplete is set. The decision model reads it as the yes/no it answers.

**`Profile`**

_The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot._

- `name` — string **(required)**
- `description` — string
- `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
  - _array of_ `CopilotAudienceEntry`
    - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
    - `values` — array **(required)**
      - _array of_ `string`
- `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
  - _array of_ `CopilotStage`
- `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
  - _array of_ `CopilotChannel`
- `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
- `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
  - _array of_ `CopilotFeature`
    - _oneOf_ — exactly one of:
      - **`csat`**
        - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
      - **`sentiment`**
        - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
      - **`talkRatio`**
        - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
      - **`topics`**
        - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
          - _(nesting depth limit — see `TopicsFeatureConfiguration` in the Schemas appendix)_
      - **`contextualKnowledgeAnswers`**
        - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
          - _(nesting depth limit — see `ContextualKnowledgeAnswersFeatureConfiguration` in the Schemas appendix)_
      - **`signals`**
        - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
          - _(nesting depth limit — see `SignalsFeatureConfiguration` in the Schemas appendix)_
- `assets` — array — Assets referenced by this profile.
  - _array of_ `string`
- `intents` — array — Intents referenced by this profile.
  - _array of_ `string`
- `evaluations` — array — Evaluations referenced by this profile.
  - _array of_ `string`
- `automations` — array — Automations referenced by this profile.
  - _array of_ `string`
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
- `status` — string **(required)** _(enum: `draft`, `active`)_
- `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
- `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
- `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
- `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).

**`ProfileDefinitionSnapshot`**

_Immutable snapshot of a profile definition at publish time, with all referenced library resources resolved inline._

- `name` — string **(required)**
- `description` — string
- `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
  - _array of_ `CopilotAudienceEntry`
    - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
    - `values` — array **(required)**
      - _array of_ `string`
- `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
  - _array of_ `CopilotStage`
- `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
  - _array of_ `CopilotChannel`
- `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
- `features` — array — Copilot features enabled for this profile at publish time, including their type-specific configuration.
  - _array of_ `CopilotFeature`
    - _oneOf_ — exactly one of:
      - **`csat`**
        - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
      - **`sentiment`**
        - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
      - **`talkRatio`**
        - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
      - **`topics`**
        - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
          - _(nesting depth limit — see `TopicsFeatureConfiguration` in the Schemas appendix)_
      - **`contextualKnowledgeAnswers`**
        - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
          - _(nesting depth limit — see `ContextualKnowledgeAnswersFeatureConfiguration` in the Schemas appendix)_
      - **`signals`**
        - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
          - _(nesting depth limit — see `SignalsFeatureConfiguration` in the Schemas appendix)_
- `intents` — array **(required)** — Intents resolved from the draft's intents at publish time.
  - _array of_ `IntentSnapshot`
    - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
    - `description` — string
    - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
      - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
        - _(nesting depth limit — see `IntentTextMatch` in the Schemas appendix)_
      - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
        - _(nesting depth limit — see `IntentAiMatch` in the Schemas appendix)_
      - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
    - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
- `evaluations` — array **(required)** — Evaluations resolved from the draft's evaluations at publish time.
  - _array of_ `EvaluationSnapshot`
    - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
    - `description` — string
    - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
    - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
      - _array of_ `CopilotField`
        - _(nesting depth limit — see `CopilotField` in the Schemas appendix)_
    - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
- `automations` — array **(required)** — Automations resolved from the draft's automations at publish time.
  - _array of_ `AutomationSnapshot`
    - `name` — string **(required)**
    - `description` — string
    - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
    - `id` — string **(required)** _(minLen=1; maxLen=128)_
- `assets` — array **(required)** — Assets resolved from the draft's assets at publish time.
  - _array of_ `AssetSnapshot`
    - `key` — string — Stable programmatic key referenced from suggestions and traces.
    - `name` — string **(required)**
    - `description` — string
    - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
    - `title` — string — Card headline.
    - `subtitle` — string
    - `markdown` — string — Markdown body shown on the card.
    - `footer` — string
    - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
    - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
    - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
    - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`card`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`playbook`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`smartAction`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`knowledge`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
    - `id` — string **(required)** _(minLen=1; maxLen=128)_

**`ProfileInfo`**

_Summary entry returned by ListProfiles._

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
- `audience` — array — The profile's targeting, so a list row can say what it applies to without reading the definition.
  - _array of_ `CopilotAudienceEntry`
    - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
    - `values` — array **(required)**
      - _array of_ `string`
- `stages` — array — Stages a resource applies in. An empty or absent list means every stage.
  - _array of_ `CopilotStage`
- `channels` — array — Conversation channels a resource applies to. An empty or absent list means every channel. A channel filter only constrains the `during` and `after` stages: in `before` there is nothing to be a call, a conference or a chat, so a resource covering only `before` applies whatever this list says.
  - _array of_ `CopilotChannel`
- `status` — string **(required)** _(enum: `draft`, `active`)_
- `live` — boolean **(required)**
- `latestVersion` — number — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
- `intentCount` — number — Number of referenced intents.
- `evaluationCount` — number — Number of referenced evaluations.
- `automationCount` — number — Number of referenced automations.
- `assetCount` — number — Number of referenced assets.

**`ProfileResource`**

_One feature or reusable library resource attached to a profile._

- _oneOf_ — exactly one of:
  - **`feature`**
    - `feature` — union **(required)** — A Copilot feature enabled for a profile, with its type-specific configuration.
      - _oneOf_ — exactly one of:
        - **`csat`**
          - `csat` — CsatFeatureConfiguration **(required)** — Configuration for the built-in CSAT feature.
        - **`sentiment`**
          - `sentiment` — SentimentFeatureConfiguration **(required)** — Configuration for the built-in sentiment feature.
        - **`talkRatio`**
          - `talkRatio` — TalkRatioFeatureConfiguration **(required)** — Configuration for the built-in talk ratio feature.
        - **`topics`**
          - `topics` — TopicsFeatureConfiguration **(required)** — Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit.
            - _(nesting depth limit — see `TopicsFeatureConfiguration` in the Schemas appendix)_
        - **`contextualKnowledgeAnswers`**
          - `contextualKnowledgeAnswers` — ContextualKnowledgeAnswersFeatureConfiguration **(required)** — Configuration for the built-in contextual knowledge answers feature.
            - _(nesting depth limit — see `ContextualKnowledgeAnswersFeatureConfiguration` in the Schemas appendix)_
        - **`signals`**
          - `signals` — SignalsFeatureConfiguration **(required)** — Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit.
            - _(nesting depth limit — see `SignalsFeatureConfiguration` in the Schemas appendix)_
  - **`asset`**
    - `asset` — string **(required)** _(minLen=1; maxLen=128)_
  - **`automation`**
    - `automation` — string **(required)** _(minLen=1; maxLen=128)_
  - **`intent`**
    - `intent` — string **(required)** _(minLen=1; maxLen=128)_
  - **`evaluation`**
    - `evaluation` — string **(required)** _(minLen=1; maxLen=128)_

**`ProfileResourceType`**

_The kind of resource attached to a profile._

- string _(enum: `feature`, `asset`, `automation`, `intent`, `evaluation`)_

**`ProfileStatus`**

- string _(enum: `draft`, `active`)_

**`ProfileVersion`**

_Published profile version: an immutable, self-contained snapshot of the profile at publish time._

- `profileId` — string **(required)** _(minLen=1; maxLen=128)_
- `version` — number **(required)** — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
- `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
- `definition` — ProfileDefinitionSnapshot **(required)** — Immutable snapshot of a profile definition at publish time, with all referenced library resources resolved inline.
  - `name` — string **(required)**
  - `description` — string
  - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
    - _array of_ `CopilotAudienceEntry`
      - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
      - `values` — array **(required)**
        - _array of_ `string`
  - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
    - _array of_ `CopilotStage`
  - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
    - _array of_ `CopilotChannel`
  - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
  - `features` — array — Copilot features enabled for this profile at publish time, including their type-specific configuration.
    - _array of_ `CopilotFeature`
      - _oneOf_ — exactly one of:
        - **`csat`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sentiment`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`talkRatio`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`topics`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`contextualKnowledgeAnswers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`signals`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `intents` — array **(required)** — Intents resolved from the draft's intents at publish time.
    - _array of_ `IntentSnapshot`
      - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
      - `description` — string
      - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
        - _(nesting depth limit — see `IntentHandlers` in the Schemas appendix)_
      - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
      - `id` — string **(required)** _(minLen=1; maxLen=128)_
  - `evaluations` — array **(required)** — Evaluations resolved from the draft's evaluations at publish time.
    - _array of_ `EvaluationSnapshot`
      - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
      - `description` — string
      - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
      - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
        - _(nesting depth limit — see `CopilotField` in the Schemas appendix)_
      - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
      - `id` — string **(required)** _(minLen=1; maxLen=128)_
  - `automations` — array **(required)** — Automations resolved from the draft's automations at publish time.
    - _array of_ `AutomationSnapshot`
      - `name` — string **(required)**
      - `description` — string
      - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
        - _(nesting depth limit — see `AutomationHandler` in the Schemas appendix)_
      - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
      - `id` — string **(required)** _(minLen=1; maxLen=128)_
  - `assets` — array **(required)** — Assets resolved from the draft's assets at publish time.
    - _array of_ `AssetSnapshot`
      - `key` — string — Stable programmatic key referenced from suggestions and traces.
      - `name` — string **(required)**
      - `description` — string
      - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
      - `title` — string — Card headline.
      - `subtitle` — string
      - `markdown` — string — Markdown body shown on the card.
      - `footer` — string
      - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
      - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
      - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
      - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
        - _(nesting depth limit — see `AssetContent` in the Schemas appendix)_
      - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
      - `id` — string **(required)** _(minLen=1; maxLen=128)_
- `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.

**`ProfileVersionChange`**

_One field-level difference between the compared profile definitions._

- `path` — string **(required)** — JSON pointer of the changed field within the profile definition, e.g. '/assets/0/markdown'.
- `before` — any — Value before the change (absent when the field was added).
- `after` — any — Value after the change (absent when the field was removed).

**`ProfileVersionInfo`**

_Version list entry without the full definition snapshot._

- `profileId` — string **(required)** _(minLen=1; maxLen=128)_
- `version` — number **(required)** — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
- `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
- `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.
- `latest` — boolean — True when this version is the profile's latestVersion.

**`PublishProfileVersionRequestContent`**

- `changelog` — string — What changed in this version. _(minLen=1; maxLen=500)_
- `revision` — number **(required)** — Draft revision this publish is based on (optimistic locking).

**`PublishProfileVersionResponseContent`**

- `version` — ProfileVersion **(required)** — Published profile version: an immutable, self-contained snapshot of the profile at publish time.
  - `profileId` — string **(required)** _(minLen=1; maxLen=128)_
  - `version` — number **(required)** — Published profile version number. Monotonic within a profile's version history, starting at 1. _(min=1)_
  - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
  - `definition` — ProfileDefinitionSnapshot **(required)** — Immutable snapshot of a profile definition at publish time, with all referenced library resources resolved inline.
    - `name` — string **(required)**
    - `description` — string
    - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
      - _array of_ `CopilotAudienceEntry`
        - _(nesting depth limit — see `CopilotAudienceEntry` in the Schemas appendix)_
    - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
      - _array of_ `CopilotStage`
    - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
      - _array of_ `CopilotChannel`
    - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
    - `features` — array — Copilot features enabled for this profile at publish time, including their type-specific configuration.
      - _array of_ `CopilotFeature`
        - _(nesting depth limit — see `CopilotFeature` in the Schemas appendix)_
    - `intents` — array **(required)** — Intents resolved from the draft's intents at publish time.
      - _array of_ `IntentSnapshot`
        - _(nesting depth limit — see `IntentSnapshot` in the Schemas appendix)_
    - `evaluations` — array **(required)** — Evaluations resolved from the draft's evaluations at publish time.
      - _array of_ `EvaluationSnapshot`
        - _(nesting depth limit — see `EvaluationSnapshot` in the Schemas appendix)_
    - `automations` — array **(required)** — Automations resolved from the draft's automations at publish time.
      - _array of_ `AutomationSnapshot`
        - _(nesting depth limit — see `AutomationSnapshot` in the Schemas appendix)_
    - `assets` — array **(required)** — Assets resolved from the draft's assets at publish time.
      - _array of_ `AssetSnapshot`
        - _(nesting depth limit — see `AssetSnapshot` in the Schemas appendix)_
  - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.

**`RestoreProfileVersionToDraftRequestContent`**

- `revision` — number **(required)** — Draft revision this restore is based on (optimistic locking).

**`RestoreProfileVersionToDraftResponseContent`**

- `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
  - `name` — string **(required)**
  - `description` — string
  - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
    - _array of_ `CopilotAudienceEntry`
      - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
      - `values` — array **(required)**
        - _array of_ `string`
  - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
    - _array of_ `CopilotStage`
  - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
    - _array of_ `CopilotChannel`
  - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
  - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
    - _array of_ `CopilotFeature`
      - _oneOf_ — exactly one of:
        - **`csat`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sentiment`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`talkRatio`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`topics`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`contextualKnowledgeAnswers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`signals`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `assets` — array — Assets referenced by this profile.
    - _array of_ `string`
  - `intents` — array — Intents referenced by this profile.
    - _array of_ `string`
  - `evaluations` — array — Evaluations referenced by this profile.
    - _array of_ `string`
  - `automations` — array — Automations referenced by this profile.
    - _array of_ `string`
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
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
  - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).

**`RevisionConflictExceptionResponseContent`**

_The resource was modified concurrently; re-read it and retry with the latest revision._

- `message` — string **(required)**
- `type` — string _(default=RevisionConflictException)_
- `currentRevision` — number — The current revision of the resource on the server.

**`SentimentFeatureConfiguration`**

_Configuration for the built-in sentiment feature._

- SentimentFeatureConfiguration

**`SignalsFeatureConfiguration`**

_Configuration for the built-in signals feature, each signal answered by a decision model. The catalog has three groups: - `moments`: moments that need someone now, such as an escalation request, a legal threat or a repeat contact. Asked when a customer turn ends. - `safety`: abuse or threats toward the agent, and hate or discriminatory language. Asked when a customer turn ends. - `sales`: methodology elements (MEDDPICC, BANT), buying signals, the objection raised and its type, and deal risks. Asked once the `sales` or `deal_process` topic category is detected, so a conversation that is not about buying never asks them. The company's own signals are intents. Each signal of an included group counts towards the session's question limit._

- `include` — array — Groups or single signals to detect. Empty or absent means every group. _(maxItems=256)_
  - _array of_ `string`

**`SmartAction`**

_A button shown under an asset. Exactly one member is set; it selects what happens when clicked._

- _oneOf_ — exactly one of:
  - **`openUrl`**
    - `openUrl` — SmartActionOpenUrl **(required)** — Opens a URL for the agent.
      - `url` — string **(required)**
      - `openInNewTab` — boolean
  - **`runAgent`**
    - `runAgent` — SmartActionRunAgent **(required)** — Runs a Wilma agent.
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `variables` — array
        - _array of_ `CopilotVariableBinding`
          - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_
      - `resultMode` — string **(required)** — Where a smart action's result is delivered. _(enum: `show_card`, `silent`)_
      - `requireConfirmation` — boolean — Ask the agent to confirm before running. Defaults to false.
  - **`transfer`**
    - `transfer` — SmartActionTransfer **(required)** — Transfers the live call to a destination. Voice calls only.
      - `destination` — string **(required)** — Extension or phone number to transfer to.
  - **`handover`**
    - `handover` — SmartActionHandover **(required)** — Hands the live chat over to an agent or service. Chats only.
      - `handoverVariant` — string **(required)** — Target of a chat handover smart action. _(enum: `agent`, `service`)_
      - `assignee` — string — Wilma agent to hand over to when handoverVariant is `agent`.
      - `service` — string — x-bees service to hand over to when handoverVariant is `service`.

**`SmartActionHandover`**

_Hands the live chat over to an agent or service. Chats only._

- `handoverVariant` — string **(required)** — Target of a chat handover smart action. _(enum: `agent`, `service`)_
- `assignee` — string — Wilma agent to hand over to when handoverVariant is `agent`.
- `service` — string — x-bees service to hand over to when handoverVariant is `service`.

**`SmartActionHandoverVariant`**

_Target of a chat handover smart action._

- string _(enum: `agent`, `service`)_

**`SmartActionItem`**

_A smart action with its label and payload._

- `id` — string **(required)**
- `label` — string **(required)**
- `description` — string
- `action` — union **(required)** — A button shown under an asset. Exactly one member is set; it selects what happens when clicked.
  - _oneOf_ — exactly one of:
    - **`openUrl`**
      - `openUrl` — SmartActionOpenUrl **(required)** — Opens a URL for the agent.
        - `url` — string **(required)**
        - `openInNewTab` — boolean
    - **`runAgent`**
      - `runAgent` — SmartActionRunAgent **(required)** — Runs a Wilma agent.
        - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
        - `variables` — array
          - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_
        - `resultMode` — string **(required)** — Where a smart action's result is delivered. _(enum: `show_card`, `silent`)_
        - `requireConfirmation` — boolean — Ask the agent to confirm before running. Defaults to false.
    - **`transfer`**
      - `transfer` — SmartActionTransfer **(required)** — Transfers the live call to a destination. Voice calls only.
        - `destination` — string **(required)** — Extension or phone number to transfer to.
    - **`handover`**
      - `handover` — SmartActionHandover **(required)** — Hands the live chat over to an agent or service. Chats only.
        - `handoverVariant` — string **(required)** — Target of a chat handover smart action. _(enum: `agent`, `service`)_
        - `assignee` — string — Wilma agent to hand over to when handoverVariant is `agent`.
        - `service` — string — x-bees service to hand over to when handoverVariant is `service`.

**`SmartActionOpenUrl`**

_Opens a URL for the agent._

- `url` — string **(required)**
- `openInNewTab` — boolean

**`SmartActionResultMode`**

_Where a smart action's result is delivered._

- string _(enum: `show_card`, `silent`)_

**`SmartActionRunAgent`**

_Runs a Wilma agent._

- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `variables` — array
  - _array of_ `CopilotVariableBinding`
    - `name` — string **(required)**
    - `type` — string — Declared value type, e.g. 'string' or 'number'.
    - `optional` — boolean
    - `variant` — string **(required)** _(enum: `auto`, `guided`, `predefined`)_
    - `description` — string — Guidance for the model when variant is `guided`.
    - `value` — string — Fixed value when variant is `predefined`. Supports handlebars against the session state, e.g. '{{call.remotePhone}}'.
- `resultMode` — string **(required)** — Where a smart action's result is delivered. _(enum: `show_card`, `silent`)_
- `requireConfirmation` — boolean — Ask the agent to confirm before running. Defaults to false.

**`SmartActionTransfer`**

_Transfers the live call to a destination. Voice calls only._

- `destination` — string **(required)** — Extension or phone number to transfer to.

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

**`TalkRatioFeatureConfiguration`**

_Configuration for the built-in talk ratio feature._

- TalkRatioFeatureConfiguration

**`TopicsFeatureConfiguration`**

_Configuration for the built-in topics feature. Topics are classified, not summarised: a decision model answers, for each category and topic, whether the conversation covers it, and `topics` holds the names of the categories and topics it does - values a condition can compare. A category is asked on every full-transcript pass until it is detected; its topics are asked once it is. A category's name is in `topics` when the category itself is detected, not when one of its topics is. `custom` adds the company's own: new categories with their topics, and topics added to a built-in category, such as `mastercard` in `payment`. Each category and topic, built-in or custom, counts towards the session's question limit._

- `include` — array — Built-in categories, or single topics in them, to classify against. Empty or absent means every category. _(maxItems=256)_
  - _array of_ `string`
- `custom` — array — The company's own categories, and the topics it adds to built-in ones; at most 64 topics in all. A name is used once across `custom`, and only a category that extends a built-in one uses a catalog name. Topics added to a built-in category are asked like its own: once it is detected when the whole category is included, from the start when only some of its topics are. A built-in category that `include` leaves out entirely cannot be extended. _(maxItems=32)_
  - _array of_ `CustomTopicCategory`
    - `name` — string **(required)** — A new category's name, or the name of the built-in category its topics are added to. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=64)_
    - `description` — string — What a new category covers, as the decision model reads it: required for a new category, and left out when extending a built-in one, which keeps its own. _(minLen=1; maxLen=500)_
    - `topics` — array **(required)** _(minItems=1; maxItems=64)_
      - _array of_ `CustomTopic`
        - _(nesting depth limit — see `CustomTopic` in the Schemas appendix)_

**`UpdateAssetRequestContent`**

_The editable definition of an asset._

- `key` — string — Stable programmatic key referenced from suggestions and traces.
- `name` — string **(required)**
- `description` — string
- `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
- `title` — string — Card headline.
- `subtitle` — string
- `markdown` — string — Markdown body shown on the card.
- `footer` — string
- `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
- `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
- `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
- `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`card`**
      - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
        - `content` — union — How a card's body is produced. Exactly one member is set.
          - _(nesting depth limit — see `CardContent` in the Schemas appendix)_
    - **`playbook`**
      - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
        - `goal` — string
        - `steps` — array
          - _(nesting depth limit — see `PlaybookStep` in the Schemas appendix)_
        - `completionCriteria` — union — How a playbook is judged complete. Exactly one member is set.
          - _(nesting depth limit — see `PlaybookCompletionCriteria` in the Schemas appendix)_
    - **`smartAction`**
      - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
        - `actions` — array **(required)**
          - _(nesting depth limit — see `SmartActionItem` in the Schemas appendix)_
    - **`knowledge`**
      - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
        - `summary` — string
        - `sources` — string
- `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
- `revision` — number **(required)** — Revision this update is based on (optimistic locking).

**`UpdateAssetResponseContent`**

- `asset` — Asset **(required)** — A reusable asset. Referenced by profiles via `assets`.
  - `key` — string — Stable programmatic key referenced from suggestions and traces.
  - `name` — string **(required)**
  - `description` — string
  - `enabled` — boolean — Whether the asset participates in matching. Defaults to true.
  - `title` — string — Card headline.
  - `subtitle` — string
  - `markdown` — string — Markdown body shown on the card.
  - `footer` — string
  - `severity` — string — Visual emphasis of the asset card. _(enum: `neutral`, `success`, `warning`, `danger`)_
  - `icon` — string — Icon shown on the asset card. _(enum: `info`, `lightbulb`, `shield`, `book_open`, `alert`, `sparkles`)_
  - `sticky` — boolean — Keep the asset pinned in the UI rather than dismissible.
  - `content` — union **(required)** — The kind-specific payload of an asset. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`card`**
        - `card` — AssetCard **(required)** — An informational card. `content` selects how the card body is produced (static markdown or agent-generated); the headline and markdown members live on the asset definition.
          - _(nesting depth limit — see `AssetCard` in the Schemas appendix)_
      - **`playbook`**
        - `playbook` — AssetPlaybook **(required)** — A step-by-step playbook for the agent to follow.
          - _(nesting depth limit — see `AssetPlaybook` in the Schemas appendix)_
      - **`smartAction`**
        - `smartAction` — AssetSmartActions **(required)** — A set of one-click smart actions offered to the agent.
          - _(nesting depth limit — see `AssetSmartActions` in the Schemas appendix)_
      - **`knowledge`**
        - `knowledge` — AssetKnowledge **(required)** — A knowledge answer with its supporting sources.
          - _(nesting depth limit — see `AssetKnowledge` in the Schemas appendix)_
  - `conditions` — any — Conditions that show the asset. It is shown at most once per session when they first become true.
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

**`UpdateAutomationRequestContent`**

_The editable definition of an automation._

- `name` — string **(required)**
- `description` — string
- `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`agent`**
      - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
        - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
        - `prompt` — string — Prompt handed to the agent; the live conversation context is added automatically.
        - `outputMode` — string — Where the automation's result is delivered. _(enum: `card`, `silent`)_
        - `parameters` — array
          - _(nesting depth limit — see `CopilotVariableBinding` in the Schemas appendix)_
- `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
- `revision` — number **(required)** — Revision this update is based on (optimistic locking).

**`UpdateAutomationResponseContent`**

- `automation` — Automation **(required)** — A reusable automation. Referenced by profiles via `automations`.
  - `name` — string **(required)**
  - `description` — string
  - `handler` — union **(required)** — What the automation does when it fires. Exactly one member is set.
    - _oneOf_ — exactly one of:
      - **`agent`**
        - `agent` — AgentAutomationHandler **(required)** — Runs a Wilma agent and optionally shows its generated content to the agent.
          - _(nesting depth limit — see `AgentAutomationHandler` in the Schemas appendix)_
  - `conditions` — any — Conditions that trigger the automation. It fires at most once per session when they first become true.
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

**`UpdateEvaluationRequestContent`**

_The editable definition of an evaluation._

- `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
- `description` — string
- `instructions` — string **(required)** — Prompt the model follows to score the transcript.
- `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
  - _array of_ `CopilotField`
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `description` — string
    - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
    - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
      - _oneOf_ — exactly one of:
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`multiline`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`number`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`selection`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
- `revision` — number **(required)** — Revision this update is based on (optimistic locking).

**`UpdateEvaluationResponseContent`**

- `evaluation` — Evaluation **(required)** — A reusable evaluation. Referenced by profiles via `evaluations`.
  - `name` — string **(required)** — Programmatic evaluation name used in the session state and condition fields, e.g. 'csat'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
  - `description` — string
  - `instructions` — string **(required)** — Prompt the model follows to score the transcript.
  - `fields` — array — Structured values the evaluation produces. A `selection` field is answered directly by a decision model; a `text`, `multiline` or `number` field is extracted by a language model, only once the decision model says the value was stated.
    - _array of_ `CopilotField`
      - `id` — string **(required)**
      - `name` — string **(required)**
      - `description` — string
      - `optional` — boolean — Whether the model may leave this field unset. Defaults to true.
      - `parameter` — union **(required)** — The value shape of a field. Exactly one member is set; the member selects how the model extracts and validates the value.
        - _(nesting depth limit — see `CopilotFieldParameter` in the Schemas appendix)_
  - `conditions` — any — Extra conditions gating whether this evaluation runs for a session.
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

**`UpdateIntentRequestContent`**

_The editable definition of an intent._

- `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
- `description` — string
- `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
  - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
    - `options` — array
      - _array of_ `IntentTextMatchOption`
        - _(nesting depth limit — see `IntentTextMatchOption` in the Schemas appendix)_
  - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
    - `instructions` — string — Prompt describing when this intent applies.
    - `fields` — array — Structured values the model extracts when the intent matches.
      - _array of_ `CopilotField`
        - _(nesting depth limit — see `CopilotField` in the Schemas appendix)_
  - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
- `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
- `revision` — number **(required)** — Revision this update is based on (optimistic locking).

**`UpdateIntentResponseContent`**

- `intent` — Intent **(required)** — A reusable intent. Referenced by profiles via `intents`.
  - `name` — string **(required)** — Programmatic intent name used in the session state and condition fields, e.g. 'refund_request'. _(pattern=^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$; minLen=1; maxLen=128)_
  - `description` — string
  - `handlers` — IntentHandlers **(required)** — The detection handlers for an intent. Text matching is attempted first, then AI matching. An absent handler is a matcher that is off - which is what the `enabled` flag on each handler used to say. An intent with neither handler set is never detected.
    - `textMatch` — IntentTextMatch — Literal-text matching. Checked before AI matching; a text hit short-circuits semantic evaluation.
      - `options` — array
        - _(nesting depth limit — see `IntentTextMatchOption` in the Schemas appendix)_
    - `aiMatch` — IntentAiMatch — Semantic (AI) matching. Detects the intent from meaning and extracts structured fields into `intent.<name>.<field>`. A decision model answers whether the intent happened, and whether each field is mentioned; the language model is called only to extract the values of fields that are.
      - `instructions` — string — Prompt describing when this intent applies.
      - `fields` — array — Structured values the model extracts when the intent matches.
        - _(nesting depth limit — see `CopilotField` in the Schemas appendix)_
    - `saidBy` — string — Whose lines a transcript-reading resource is matched against. On an intent, which is the only copilot resource that reads the transcript itself: a profile does not listen, and an asset reacts to what an intent already decided. It matters for the intents that are about behaviour rather than topic - "the customer asked for a refund" and "the agent offered a refund" are different events, and matching over the whole transcript makes them one. The side of each transcript line is already resolved by the runtime (`role: agent | customer`). _(enum: `anyone`, `agent`, `customer`)_
  - `conditions` — any — Extra conditions gating whether this intent is evaluated for a session.
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

**`UpdateProfileRequestContent`**

_Profile fields shared by the editable draft and the published snapshot._

- `name` — string **(required)**
- `description` — string
- `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
  - _array of_ `CopilotAudienceEntry`
    - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
    - `values` — array **(required)**
      - _array of_ `string`
- `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
  - _array of_ `CopilotStage`
- `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
  - _array of_ `CopilotChannel`
- `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
- `revision` — number **(required)** — Draft revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.

**`UpdateProfileResponseContent`**

- `profile` — Profile **(required)** — The complete configuration of a profile, including draft lifecycle state. Referenced library resources are listed by id; a published version resolves them into an immutable snapshot.
  - `name` — string **(required)**
  - `description` — string
  - `audience` — array — Who this profile assists - queues, groups, departments, users, AI agents, chat services and trunks. Empty or absent means everyone in the company. This is the profile's primary scope: an administrator reaches for "my refunds team", not for a conversation medium, and a queue already carries the medium, the skill and the line of business.
    - _array of_ `CopilotAudienceEntry`
      - `kind` — string **(required)** — The kind of thing a profile is aimed at. Two families, and the difference decides which stages the entry can constrain. `user`, `group`, `department` and `agent` name **who is assisted** - a person for the first three, a Wilma AI agent for the last - and in the `before` stage the assisted party is whoever opened copilot, so they constrain every stage. `queue`, `service` and `trunk` describe a **live conversation**, which does not exist in `before` - so an entry of those kinds says nothing there. Values are the tenant's own routing objects: user emails for `user`, Wilma agent ids for `agent`, PBX group and department ids, queue and trunk names as `wda-stream` reports them, and x-bees service uris for `service`. _(enum: `user`, `group`, `department`, `agent`, `queue`, `service`, `trunk`)_
      - `values` — array **(required)**
        - _array of_ `string`
  - `stages` — array — Stages of a conversation this profile applies in. Empty or absent means every stage.
    - _array of_ `CopilotStage`
  - `channels` — array — Conversation channels this profile applies to. Empty or absent means every channel. Only constrains the `during` and `after` stages - nothing is a call, a conference or a chat before it starts - so a profile whose `stages` are `before` alone applies whatever this says.
    - _array of_ `CopilotChannel`
  - `conditions` — any — Conditions under which the profile matches a conversation. An empty tree always matches. Deprecated - see the deprecation note. This shape is deprecated since 2026-08: Profile conditions are resolved once, on the session's first event, so a rule over anything copilot has yet to detect never activates the profile. Use `audience` / `stages` / `channels` for what is known at that moment, and put everything conditional on the assets, intents and automations the profile carries, where conditions are re-evaluated as state changes. Still read for profiles authored before those members existed. _(deprecated)_
  - `features` — array — Copilot features enabled for this profile. Each list item is a typed feature and its configuration.
    - _array of_ `CopilotFeature`
      - _oneOf_ — exactly one of:
        - **`csat`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sentiment`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`talkRatio`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`topics`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`contextualKnowledgeAnswers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`signals`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `assets` — array — Assets referenced by this profile.
    - _array of_ `string`
  - `intents` — array — Intents referenced by this profile.
    - _array of_ `string`
  - `evaluations` — array — Evaluations referenced by this profile.
    - _array of_ `string`
  - `automations` — array — Automations referenced by this profile.
    - _array of_ `string`
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
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the profile is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number the current draft originated from; absent before the first version is published. _(min=1)_
  - `live` — boolean **(required)** — Whether the profile is currently applied to live conversations (its latest version is deployed).

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

</details>
