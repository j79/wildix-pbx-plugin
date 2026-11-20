## Wilma Sandbox API

_OpenAPI: Wilma Sandbox Service — version v2_

**Servers**

- `https://api.wilma.wildix.com` — Production
- `https://api-stable.wilma.wildix.com` — Stable
- `https://api-stage.wilma.wildix.com` — Stage

### Sandboxes

#### `GET` `/v2/sandbox/sandboxes`

Lists sandboxes that ran (or are running), newest first. Filter by `snapshotId` to audit every
    sandbox launched from a specific snapshot, or by owner, status or time window to audit usage
    across the company.

- operationId: `ListSandboxes`
- **Scopes**: `wilma-sandbox:ListSandboxes`, `wilma-sandbox:read`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `snapshotId` (query) — string — Only sandboxes launched from this snapshot. _(minLen=12; maxLen=12)_
  - `owner` (query) — string — Only sandboxes that ran for this entity, e.g. 'wilma://agents/UXDT1W9fI3sj'. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
  - `status` (query) — string _(enum: `starting`, `running`, `idle`, `stopped`, `expired`, `failed`)_
  - `from` (query) — string — Only sandboxes created at or after this time.
  - `to` (query) — string — Only sandboxes created at or before this time.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListSandboxesResponseContent`)
  - `sandboxes` — array **(required)**
    - _array of_ `Sandbox`
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `snapshotId` — string — Snapshot used to prepare this sandbox. Absent for sandboxes configured inline on the agent. _(minLen=12; maxLen=12)_
      - `providerSandboxId` — string — Provider-side sandbox id, matching the SandboxStartedEvent of the shared session event stream.
      - `status` — string **(required)** _(enum: `starting`, `running`, `idle`, `stopped`, `expired`, `failed`)_
      - `owner` — string — Canonical URI of the entity the sandbox ran for, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://chats/aB3dE5fG7hJ9'. Carries the owning service and entity kind in its path. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
      - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `lastActiveAt` — string — Last time the sandbox executed something.
      - `stoppedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `stopReason` — string — Why a sandbox stopped. _(enum: `session_ended`, `idle_timeout`, `terminated`, `error`)_
      - `usage` — SandboxUsage — Resource consumption of a sandbox over its lifetime, as metric name to value, e.g. 'cpuSeconds', 'memoryMbPeak', 'networkEgressBytes', 'uptimeSeconds'. The set of metric names is not fixed and may grow.
        - _map of_ `number`
      - `stopErrorMessage` — string — Failure message when status is FAILED.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`

#### `GET` `/v2/sandbox/sandboxes/{sandboxId}`

Retrieves a single sandbox with its status, lineage (snapshot/owner) and resource usage.

- operationId: `GetSandbox`
- **Scopes**: `wilma-sandbox:GetSandbox`, `wilma-sandbox:read`
- **Parameters**
  - `sandboxId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetSandboxResponseContent`)
  - `sandbox` — Sandbox **(required)** — A single sandbox run.
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `snapshotId` — string — Snapshot used to prepare this sandbox. Absent for sandboxes configured inline on the agent. _(minLen=12; maxLen=12)_
    - `providerSandboxId` — string — Provider-side sandbox id, matching the SandboxStartedEvent of the shared session event stream.
    - `status` — string **(required)** _(enum: `starting`, `running`, `idle`, `stopped`, `expired`, `failed`)_
    - `owner` — string — Canonical URI of the entity the sandbox ran for, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://chats/aB3dE5fG7hJ9'. Carries the owning service and entity kind in its path. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `lastActiveAt` — string — Last time the sandbox executed something.
    - `stoppedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `stopReason` — string — Why a sandbox stopped. _(enum: `session_ended`, `idle_timeout`, `terminated`, `error`)_
    - `usage` — SandboxUsage — Resource consumption of a sandbox over its lifetime, as metric name to value, e.g. 'cpuSeconds', 'memoryMbPeak', 'networkEgressBytes', 'uptimeSeconds'. The set of metric names is not fixed and may grow.
      - _map of_ `number`
    - `stopErrorMessage` — string — Failure message when status is FAILED.
- Errors: `400`, `404`

#### `POST` `/v2/sandbox/sandboxes/{sandboxId}/terminate`

Forcibly stops a running sandbox. Idempotent: terminating an already-stopped sandbox succeeds. Intended for operators reclaiming resources or killing a misbehaving sandbox.

- operationId: `TerminateSandbox`
- **Scopes**: `wilma-sandbox:TerminateSandbox`
- **Parameters**
  - `sandboxId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`TerminateSandboxResponseContent`)
  - `sandbox` — Sandbox **(required)** — A single sandbox run.
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `snapshotId` — string — Snapshot used to prepare this sandbox. Absent for sandboxes configured inline on the agent. _(minLen=12; maxLen=12)_
    - `providerSandboxId` — string — Provider-side sandbox id, matching the SandboxStartedEvent of the shared session event stream.
    - `status` — string **(required)** _(enum: `starting`, `running`, `idle`, `stopped`, `expired`, `failed`)_
    - `owner` — string — Canonical URI of the entity the sandbox ran for, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://chats/aB3dE5fG7hJ9'. Carries the owning service and entity kind in its path. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `lastActiveAt` — string — Last time the sandbox executed something.
    - `stoppedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `stopReason` — string — Why a sandbox stopped. _(enum: `session_ended`, `idle_timeout`, `terminated`, `error`)_
    - `usage` — SandboxUsage — Resource consumption of a sandbox over its lifetime, as metric name to value, e.g. 'cpuSeconds', 'memoryMbPeak', 'networkEgressBytes', 'uptimeSeconds'. The set of metric names is not fixed and may grow.
      - _map of_ `number`
    - `stopErrorMessage` — string — Failure message when status is FAILED.
- Errors: `400`, `404`

### Snapshots

#### `GET` `/v2/sandbox/snapshots`

Lists sandbox snapshots for the company, newest first.

- operationId: `ListSnapshots`
- **Scopes**: `wilma-sandbox:ListSnapshots`, `wilma-sandbox:read`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `status` (query) — string _(enum: `pending`, `building`, `ready`, `failed`)_
  - `search` (query) — string — Filter by name or description.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListSnapshotsResponseContent`)
  - `snapshots` — array **(required)**
    - _array of_ `SnapshotInfo`
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
      - `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
      - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
      - `description` — string _(minLen=1; maxLen=1000)_
      - `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
      - `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`

#### `POST` `/v2/sandbox/snapshots`

Creates a snapshot and starts building its image asynchronously. Returns immediately with the
    snapshot in PENDING/BUILDING status; poll GetSnapshot (or watch GetSnapshotBuildLogs) until it
    reaches READY or FAILED. The build config can be changed afterwards with UpdateSnapshot, which
    queues a new image under the same snapshot id.

- operationId: `CreateSnapshot`
- **Scopes**: `wilma-sandbox:CreateSnapshot`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateSnapshotRequestContent`) **(required)**
  - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `commands` — array — Shell commands run in order at build time, on top of the platform runtime.
    - _array of_ `string`
  - `env` — array — Environment variables available at build time and to every sandbox.
    - _array of_ `EnvVar`
      - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
      - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
      - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
        - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
  - `network` — SandboxNetworkPolicy
    - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
    - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
      - _array of_ `string`
- **Response 202** (`CreateSnapshotResponseContent`)
  - `snapshot` — Snapshot **(required)** — The complete configuration of a snapshot. Everything except `name` and `description` is the build configuration. UpdateSnapshot can change it and queue a new immutable image while preserving the snapshot id.
    - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `commands` — array — Shell commands run in order at build time, on top of the platform runtime.
      - _array of_ `string`
    - `env` — array — Environment variables available at build time and to every sandbox.
      - _array of_ `EnvVar`
        - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
        - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
    - `network` — SandboxNetworkPolicy
      - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
      - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
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
    - `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
    - `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
    - `revision` — number **(required)** — Monotonic revision incremented on every metadata update. Pass it back on update for optimistic locking.
    - `build` — SnapshotBuild — Outcome and metrics of the snapshot's image build.
      - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `finishedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `imageDigest` — string — Content digest of the built image, e.g. 'sha256:...'.
      - `imageSizeBytes` — number — Size of the built image in bytes.
      - `errorCode` — string — Machine-readable failure code when status is FAILED, e.g. 'command_failed', 'build_timeout'.
      - `errorMessage` — string — Human-readable build failure message when status is FAILED.
    - `stats` — SnapshotStats — Aggregate runtime usage of a snapshot, populated on GetSnapshot.
      - `activeSandboxes` — number — Sandboxes currently running from this snapshot.
      - `totalSandboxes` — number — Total sandboxes ever launched from this snapshot.
      - `referencingAgents` — number — Number of agents currently referencing this snapshot.
      - `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.
- Errors: `400`, `409`

#### `GET` `/v2/sandbox/snapshots/{snapshotId}`

Retrieves a snapshot, including its full build config, build outcome and runtime usage stats.

- operationId: `GetSnapshot`
- **Scopes**: `wilma-sandbox:GetSnapshot`, `wilma-sandbox:read`
- **Parameters**
  - `snapshotId` (path) — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetSnapshotResponseContent`)
  - `snapshot` — Snapshot **(required)** — The complete configuration of a snapshot. Everything except `name` and `description` is the build configuration. UpdateSnapshot can change it and queue a new immutable image while preserving the snapshot id.
    - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `commands` — array — Shell commands run in order at build time, on top of the platform runtime.
      - _array of_ `string`
    - `env` — array — Environment variables available at build time and to every sandbox.
      - _array of_ `EnvVar`
        - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
        - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
    - `network` — SandboxNetworkPolicy
      - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
      - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
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
    - `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
    - `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
    - `revision` — number **(required)** — Monotonic revision incremented on every metadata update. Pass it back on update for optimistic locking.
    - `build` — SnapshotBuild — Outcome and metrics of the snapshot's image build.
      - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `finishedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `imageDigest` — string — Content digest of the built image, e.g. 'sha256:...'.
      - `imageSizeBytes` — number — Size of the built image in bytes.
      - `errorCode` — string — Machine-readable failure code when status is FAILED, e.g. 'command_failed', 'build_timeout'.
      - `errorMessage` — string — Human-readable build failure message when status is FAILED.
    - `stats` — SnapshotStats — Aggregate runtime usage of a snapshot, populated on GetSnapshot.
      - `activeSandboxes` — number — Sandboxes currently running from this snapshot.
      - `totalSandboxes` — number — Total sandboxes ever launched from this snapshot.
      - `referencingAgents` — number — Number of agents currently referencing this snapshot.
      - `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.
- Errors: `400`, `404`

#### `PUT` `/v2/sandbox/snapshots/{snapshotId}`

Updates a snapshot under its existing id. Changed build settings queue a new immutable image; omitted build fields are preserved, and empty commands or env lists clear them. Pending/building snapshots reject updates. The last successful image remains available until another build succeeds; existing session workspaces remain pinned to their original image. To rebuild an unchanged configuration, call RebuildSnapshot.

- operationId: `UpdateSnapshot`
- **Scopes**: `wilma-sandbox:UpdateSnapshot`
- **Parameters**
  - `snapshotId` (path) — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateSnapshotRequestContent`) **(required)**
  - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `commands` — array
    - _array of_ `string`
  - `env` — array
    - _array of_ `EnvVar`
      - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
      - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
      - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
        - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
  - `network` — SandboxNetworkPolicy
    - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
    - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
      - _array of_ `string`
  - `revision` — number **(required)** — Snapshot revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.
- **Response 200** (`UpdateSnapshotResponseContent`)
  - `snapshot` — Snapshot **(required)** — The complete configuration of a snapshot. Everything except `name` and `description` is the build configuration. UpdateSnapshot can change it and queue a new immutable image while preserving the snapshot id.
    - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `commands` — array — Shell commands run in order at build time, on top of the platform runtime.
      - _array of_ `string`
    - `env` — array — Environment variables available at build time and to every sandbox.
      - _array of_ `EnvVar`
        - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
        - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
    - `network` — SandboxNetworkPolicy
      - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
      - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
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
    - `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
    - `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
    - `revision` — number **(required)** — Monotonic revision incremented on every metadata update. Pass it back on update for optimistic locking.
    - `build` — SnapshotBuild — Outcome and metrics of the snapshot's image build.
      - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `finishedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `imageDigest` — string — Content digest of the built image, e.g. 'sha256:...'.
      - `imageSizeBytes` — number — Size of the built image in bytes.
      - `errorCode` — string — Machine-readable failure code when status is FAILED, e.g. 'command_failed', 'build_timeout'.
      - `errorMessage` — string — Human-readable build failure message when status is FAILED.
    - `stats` — SnapshotStats — Aggregate runtime usage of a snapshot, populated on GetSnapshot.
      - `activeSandboxes` — number — Sandboxes currently running from this snapshot.
      - `totalSandboxes` — number — Total sandboxes ever launched from this snapshot.
      - `referencingAgents` — number — Number of agents currently referencing this snapshot.
      - `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.
- Errors: `400`, `404`, `409`

#### `DELETE` `/v2/sandbox/snapshots/{snapshotId}`

Deletes a snapshot. Fails with ConflictException while any agent references it, unless force=true.

- operationId: `DeleteSnapshot`
- **Scopes**: `wilma-sandbox:DeleteSnapshot`
- **Parameters**
  - `snapshotId` (path) — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `force` (query) — boolean — Delete even if agents still reference the snapshot. Those references will fail to launch sandboxes until repointed.
- Errors: `400`, `404`, `409`

#### `GET` `/v2/sandbox/snapshots/{snapshotId}/build-logs`

Returns the build logs of a snapshot, oldest first. Poll while the snapshot is BUILDING to follow progress, or read after a FAILED build to diagnose it.

- operationId: `GetSnapshotBuildLogs`
- **Scopes**: `wilma-sandbox:GetSnapshotBuildLogs`, `wilma-sandbox:read`
- **Parameters**
  - `snapshotId` (path) — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `cursor` (query) — string — Return log lines recorded at or after this time; pass back `nextCursor` to page. _(minLen=1; maxLen=2048)_
  - `limit` (query) — number _(min=1; max=1000)_
- **Response 200** (`GetSnapshotBuildLogsResponseContent`)
  - `lines` — array **(required)**
    - _array of_ `BuildLogLine`
      - `timestamp` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `stream` — string **(required)** _(enum: `stdout`, `stderr`)_
      - `message` — string **(required)**
  - `building` — boolean **(required)** — True while the build is still running and more lines may appear.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `404`

#### `POST` `/v2/sandbox/snapshots/{snapshotId}/rebuild`

Queues a new image build from the snapshot's current configuration, without changing it. Use it to pick up moving build inputs or to retry a FAILED build. Returns immediately with the snapshot in PENDING/BUILDING status; poll GetSnapshot (or watch GetSnapshotBuildLogs) until it reaches READY or FAILED. Rejected with ConflictException while a build is already pending or running. The last successful image remains available until the new build succeeds; existing session workspaces remain pinned to their original image.

- operationId: `RebuildSnapshot`
- **Scopes**: `wilma-sandbox:RebuildSnapshot`
- **Parameters**
  - `snapshotId` (path) — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 202** (`RebuildSnapshotResponseContent`)
  - `snapshot` — Snapshot **(required)** — The complete configuration of a snapshot. Everything except `name` and `description` is the build configuration. UpdateSnapshot can change it and queue a new immutable image while preserving the snapshot id.
    - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `commands` — array — Shell commands run in order at build time, on top of the platform runtime.
      - _array of_ `string`
    - `env` — array — Environment variables available at build time and to every sandbox.
      - _array of_ `EnvVar`
        - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
        - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
    - `network` — SandboxNetworkPolicy
      - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
      - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
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
    - `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
    - `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
    - `revision` — number **(required)** — Monotonic revision incremented on every metadata update. Pass it back on update for optimistic locking.
    - `build` — SnapshotBuild — Outcome and metrics of the snapshot's image build.
      - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `finishedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `imageDigest` — string — Content digest of the built image, e.g. 'sha256:...'.
      - `imageSizeBytes` — number — Size of the built image in bytes.
      - `errorCode` — string — Machine-readable failure code when status is FAILED, e.g. 'command_failed', 'build_timeout'.
      - `errorMessage` — string — Human-readable build failure message when status is FAILED.
    - `stats` — SnapshotStats — Aggregate runtime usage of a snapshot, populated on GetSnapshot.
      - `activeSandboxes` — number — Sandboxes currently running from this snapshot.
      - `totalSandboxes` — number — Total sandboxes ever launched from this snapshot.
      - `referencingAgents` — number — Number of agents currently referencing this snapshot.
      - `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.
- Errors: `400`, `404`, `409`

#### `POST` `/v2/sandbox/snapshots/{snapshotId}/test`

Launches a short-lived sandbox from a READY snapshot, runs a command in it and returns the result. Use it to verify a snapshot behaves as expected before pointing agents at it.

- operationId: `TestSnapshot`
- **Scopes**: `wilma-sandbox:TestSnapshot`
- **Parameters**
  - `snapshotId` (path) — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `TestSnapshotRequestContent`)
  - `command` — string — Command to run in the sandbox. Defaults to a no-op health check that only verifies the sandbox boots. _(minLen=1; maxLen=4000)_
  - `timeoutSeconds` — number — Maximum run time in seconds. Defaults to 60. _(min=1; max=300)_
- **Response 200** (`TestSnapshotResponseContent`)
  - `exitCode` — number — Process exit code of the command; absent when the sandbox failed to boot.
  - `stdout` — string
  - `stderr` — string
  - `timedOut` — boolean — True when the command was killed by the timeout.
  - `durationMs` — number — How long the command ran, in milliseconds.
  - `errorMessage` — string — Set when the sandbox failed to boot from the snapshot.
- Errors: `400`, `404`, `409`

### Schemas appendix — Wilma Sandbox API

<details><summary>35 component schemas</summary>

**`Actor`**

_Who performed an action: an interactive user, an API key or an internal service._

- `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
- `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
- `name` — string — Human readable name of the actor at the time of the action.

**`ActorType`**

- string _(enum: `user`, `api_key`, `service`)_

**`BuildLogLine`**

- `timestamp` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `stream` — string **(required)** _(enum: `stdout`, `stderr`)_
- `message` — string **(required)**

**`BuildLogStream`**

- string _(enum: `stdout`, `stderr`)_

**`ConflictExceptionResponseContent`**

_The request conflicts with the current state of the resource, e.g. a duplicate name, a resource still in use, or an unmet precondition._

- `message` — string **(required)**

**`CreateSnapshotRequestContent`**

_The complete configuration of a snapshot. Everything except `name` and `description` is the build configuration. UpdateSnapshot can change it and queue a new immutable image while preserving the snapshot id._

- `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
- `description` — string _(minLen=1; maxLen=1000)_
- `commands` — array — Shell commands run in order at build time, on top of the platform runtime.
  - _array of_ `string`
- `env` — array — Environment variables available at build time and to every sandbox.
  - _array of_ `EnvVar`
    - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
    - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
    - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
      - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
- `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
- `network` — SandboxNetworkPolicy
  - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
  - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
    - _array of_ `string`

**`CreateSnapshotResponseContent`**

- `snapshot` — Snapshot **(required)** — The complete configuration of a snapshot. Everything except `name` and `description` is the build configuration. UpdateSnapshot can change it and queue a new immutable image while preserving the snapshot id.
  - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `commands` — array — Shell commands run in order at build time, on top of the platform runtime.
    - _array of_ `string`
  - `env` — array — Environment variables available at build time and to every sandbox.
    - _array of_ `EnvVar`
      - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
      - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
      - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
        - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
  - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
  - `network` — SandboxNetworkPolicy
    - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
    - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
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
  - `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
  - `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
  - `revision` — number **(required)** — Monotonic revision incremented on every metadata update. Pass it back on update for optimistic locking.
  - `build` — SnapshotBuild — Outcome and metrics of the snapshot's image build.
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `finishedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `imageDigest` — string — Content digest of the built image, e.g. 'sha256:...'.
    - `imageSizeBytes` — number — Size of the built image in bytes.
    - `errorCode` — string — Machine-readable failure code when status is FAILED, e.g. 'command_failed', 'build_timeout'.
    - `errorMessage` — string — Human-readable build failure message when status is FAILED.
  - `stats` — SnapshotStats — Aggregate runtime usage of a snapshot, populated on GetSnapshot.
    - `activeSandboxes` — number — Sandboxes currently running from this snapshot.
    - `totalSandboxes` — number — Total sandboxes ever launched from this snapshot.
    - `referencingAgents` — number — Number of agents currently referencing this snapshot.
    - `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.

**`EnvVar`**

_Environment variable available during the build and at runtime. Set exactly one of an inline `value` or a `secret` reference to a secret in wilma-secrets. `secret` is resolved and injected at launch, keeping the credential out of the snapshot image; use it for anything sensitive._

- `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
- `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
- `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
  - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_

**`GetSandboxResponseContent`**

- `sandbox` — Sandbox **(required)** — A single sandbox run.
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `snapshotId` — string — Snapshot used to prepare this sandbox. Absent for sandboxes configured inline on the agent. _(minLen=12; maxLen=12)_
  - `providerSandboxId` — string — Provider-side sandbox id, matching the SandboxStartedEvent of the shared session event stream.
  - `status` — string **(required)** _(enum: `starting`, `running`, `idle`, `stopped`, `expired`, `failed`)_
  - `owner` — string — Canonical URI of the entity the sandbox ran for, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://chats/aB3dE5fG7hJ9'. Carries the owning service and entity kind in its path. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `lastActiveAt` — string — Last time the sandbox executed something.
  - `stoppedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `stopReason` — string — Why a sandbox stopped. _(enum: `session_ended`, `idle_timeout`, `terminated`, `error`)_
  - `usage` — SandboxUsage — Resource consumption of a sandbox over its lifetime, as metric name to value, e.g. 'cpuSeconds', 'memoryMbPeak', 'networkEgressBytes', 'uptimeSeconds'. The set of metric names is not fixed and may grow.
    - _map of_ `number`
  - `stopErrorMessage` — string — Failure message when status is FAILED.

**`GetSnapshotBuildLogsResponseContent`**

- `lines` — array **(required)**
  - _array of_ `BuildLogLine`
    - `timestamp` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `stream` — string **(required)** _(enum: `stdout`, `stderr`)_
    - `message` — string **(required)**
- `building` — boolean **(required)** — True while the build is still running and more lines may appear.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`GetSnapshotResponseContent`**

- `snapshot` — Snapshot **(required)** — The complete configuration of a snapshot. Everything except `name` and `description` is the build configuration. UpdateSnapshot can change it and queue a new immutable image while preserving the snapshot id.
  - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `commands` — array — Shell commands run in order at build time, on top of the platform runtime.
    - _array of_ `string`
  - `env` — array — Environment variables available at build time and to every sandbox.
    - _array of_ `EnvVar`
      - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
      - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
      - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
        - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
  - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
  - `network` — SandboxNetworkPolicy
    - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
    - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
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
  - `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
  - `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
  - `revision` — number **(required)** — Monotonic revision incremented on every metadata update. Pass it back on update for optimistic locking.
  - `build` — SnapshotBuild — Outcome and metrics of the snapshot's image build.
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `finishedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `imageDigest` — string — Content digest of the built image, e.g. 'sha256:...'.
    - `imageSizeBytes` — number — Size of the built image in bytes.
    - `errorCode` — string — Machine-readable failure code when status is FAILED, e.g. 'command_failed', 'build_timeout'.
    - `errorMessage` — string — Human-readable build failure message when status is FAILED.
  - `stats` — SnapshotStats — Aggregate runtime usage of a snapshot, populated on GetSnapshot.
    - `activeSandboxes` — number — Sandboxes currently running from this snapshot.
    - `totalSandboxes` — number — Total sandboxes ever launched from this snapshot.
    - `referencingAgents` — number — Number of agents currently referencing this snapshot.
    - `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.

**`ListSandboxesResponseContent`**

- `sandboxes` — array **(required)**
  - _array of_ `Sandbox`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `snapshotId` — string — Snapshot used to prepare this sandbox. Absent for sandboxes configured inline on the agent. _(minLen=12; maxLen=12)_
    - `providerSandboxId` — string — Provider-side sandbox id, matching the SandboxStartedEvent of the shared session event stream.
    - `status` — string **(required)** _(enum: `starting`, `running`, `idle`, `stopped`, `expired`, `failed`)_
    - `owner` — string — Canonical URI of the entity the sandbox ran for, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://chats/aB3dE5fG7hJ9'. Carries the owning service and entity kind in its path. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `lastActiveAt` — string — Last time the sandbox executed something.
    - `stoppedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `stopReason` — string — Why a sandbox stopped. _(enum: `session_ended`, `idle_timeout`, `terminated`, `error`)_
    - `usage` — SandboxUsage — Resource consumption of a sandbox over its lifetime, as metric name to value, e.g. 'cpuSeconds', 'memoryMbPeak', 'networkEgressBytes', 'uptimeSeconds'. The set of metric names is not fixed and may grow.
      - _map of_ `number`
    - `stopErrorMessage` — string — Failure message when status is FAILED.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListSnapshotsResponseContent`**

- `snapshots` — array **(required)**
  - _array of_ `SnapshotInfo`
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
    - `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
    - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
    - `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`RebuildSnapshotResponseContent`**

- `snapshot` — Snapshot **(required)** — The complete configuration of a snapshot. Everything except `name` and `description` is the build configuration. UpdateSnapshot can change it and queue a new immutable image while preserving the snapshot id.
  - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `commands` — array — Shell commands run in order at build time, on top of the platform runtime.
    - _array of_ `string`
  - `env` — array — Environment variables available at build time and to every sandbox.
    - _array of_ `EnvVar`
      - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
      - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
      - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
        - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
  - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
  - `network` — SandboxNetworkPolicy
    - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
    - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
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
  - `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
  - `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
  - `revision` — number **(required)** — Monotonic revision incremented on every metadata update. Pass it back on update for optimistic locking.
  - `build` — SnapshotBuild — Outcome and metrics of the snapshot's image build.
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `finishedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `imageDigest` — string — Content digest of the built image, e.g. 'sha256:...'.
    - `imageSizeBytes` — number — Size of the built image in bytes.
    - `errorCode` — string — Machine-readable failure code when status is FAILED, e.g. 'command_failed', 'build_timeout'.
    - `errorMessage` — string — Human-readable build failure message when status is FAILED.
  - `stats` — SnapshotStats — Aggregate runtime usage of a snapshot, populated on GetSnapshot.
    - `activeSandboxes` — number — Sandboxes currently running from this snapshot.
    - `totalSandboxes` — number — Total sandboxes ever launched from this snapshot.
    - `referencingAgents` — number — Number of agents currently referencing this snapshot.
    - `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.

**`RevisionConflictExceptionResponseContent`**

_The resource was modified concurrently; re-read it and retry with the latest revision._

- `message` — string **(required)**
- `type` — string _(default=RevisionConflictException)_
- `currentRevision` — number — The current revision of the resource on the server.

**`Sandbox`**

_A single sandbox run._

- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `snapshotId` — string — Snapshot used to prepare this sandbox. Absent for sandboxes configured inline on the agent. _(minLen=12; maxLen=12)_
- `providerSandboxId` — string — Provider-side sandbox id, matching the SandboxStartedEvent of the shared session event stream.
- `status` — string **(required)** _(enum: `starting`, `running`, `idle`, `stopped`, `expired`, `failed`)_
- `owner` — string — Canonical URI of the entity the sandbox ran for, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://chats/aB3dE5fG7hJ9'. Carries the owning service and entity kind in its path. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
- `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `lastActiveAt` — string — Last time the sandbox executed something.
- `stoppedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `stopReason` — string — Why a sandbox stopped. _(enum: `session_ended`, `idle_timeout`, `terminated`, `error`)_
- `usage` — SandboxUsage — Resource consumption of a sandbox over its lifetime, as metric name to value, e.g. 'cpuSeconds', 'memoryMbPeak', 'networkEgressBytes', 'uptimeSeconds'. The set of metric names is not fixed and may grow.
  - _map of_ `number`
- `stopErrorMessage` — string — Failure message when status is FAILED.

**`SandboxNetworkAccess`**

_Network egress policy for sandboxes launched from the snapshot._

- string _(enum: `allow-all`, `deny-all`, `allowlist`)_

**`SandboxNetworkPolicy`**

- `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
- `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
  - _array of_ `string`

**`SandboxRuntimeStatus`**

- string _(enum: `starting`, `running`, `idle`, `stopped`, `expired`, `failed`)_

**`SandboxSize`**

_Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation._

- string _(enum: `min`, `small`, `large`, `max`)_

**`SandboxStopReason`**

_Why a sandbox stopped._

- string _(enum: `session_ended`, `idle_timeout`, `terminated`, `error`)_

**`SandboxUsage`**

_Resource consumption of a sandbox over its lifetime, as metric name to value, e.g. 'cpuSeconds', 'memoryMbPeak', 'networkEgressBytes', 'uptimeSeconds'. The set of metric names is not fixed and may grow._

- _map of_ `number`

**`SecretRef`**

_A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value._

- `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_

**`Snapshot`**

_The complete configuration of a snapshot. Everything except `name` and `description` is the build configuration. UpdateSnapshot can change it and queue a new immutable image while preserving the snapshot id._

- `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
- `description` — string _(minLen=1; maxLen=1000)_
- `commands` — array — Shell commands run in order at build time, on top of the platform runtime.
  - _array of_ `string`
- `env` — array — Environment variables available at build time and to every sandbox.
  - _array of_ `EnvVar`
    - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
    - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
    - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
      - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
- `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
- `network` — SandboxNetworkPolicy
  - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
  - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
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
- `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
- `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
- `revision` — number **(required)** — Monotonic revision incremented on every metadata update. Pass it back on update for optimistic locking.
- `build` — SnapshotBuild — Outcome and metrics of the snapshot's image build.
  - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `finishedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `imageDigest` — string — Content digest of the built image, e.g. 'sha256:...'.
  - `imageSizeBytes` — number — Size of the built image in bytes.
  - `errorCode` — string — Machine-readable failure code when status is FAILED, e.g. 'command_failed', 'build_timeout'.
  - `errorMessage` — string — Human-readable build failure message when status is FAILED.
- `stats` — SnapshotStats — Aggregate runtime usage of a snapshot, populated on GetSnapshot.
  - `activeSandboxes` — number — Sandboxes currently running from this snapshot.
  - `totalSandboxes` — number — Total sandboxes ever launched from this snapshot.
  - `referencingAgents` — number — Number of agents currently referencing this snapshot.
  - `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.

**`SnapshotBuild`**

_Outcome and metrics of the snapshot's image build._

- `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `finishedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `imageDigest` — string — Content digest of the built image, e.g. 'sha256:...'.
- `imageSizeBytes` — number — Size of the built image in bytes.
- `errorCode` — string — Machine-readable failure code when status is FAILED, e.g. 'command_failed', 'build_timeout'.
- `errorMessage` — string — Human-readable build failure message when status is FAILED.

**`SnapshotInfo`**

_Lightweight snapshot list entry without the full build config._

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
- `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
- `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
- `description` — string _(minLen=1; maxLen=1000)_
- `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
- `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.

**`SnapshotStats`**

_Aggregate runtime usage of a snapshot, populated on GetSnapshot._

- `activeSandboxes` — number — Sandboxes currently running from this snapshot.
- `totalSandboxes` — number — Total sandboxes ever launched from this snapshot.
- `referencingAgents` — number — Number of agents currently referencing this snapshot.
- `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.

**`SnapshotStatus`**

- string _(enum: `pending`, `building`, `ready`, `failed`)_

**`TerminateSandboxResponseContent`**

- `sandbox` — Sandbox **(required)** — A single sandbox run.
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `snapshotId` — string — Snapshot used to prepare this sandbox. Absent for sandboxes configured inline on the agent. _(minLen=12; maxLen=12)_
  - `providerSandboxId` — string — Provider-side sandbox id, matching the SandboxStartedEvent of the shared session event stream.
  - `status` — string **(required)** _(enum: `starting`, `running`, `idle`, `stopped`, `expired`, `failed`)_
  - `owner` — string — Canonical URI of the entity the sandbox ran for, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://chats/aB3dE5fG7hJ9'. Carries the owning service and entity kind in its path. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `lastActiveAt` — string — Last time the sandbox executed something.
  - `stoppedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `stopReason` — string — Why a sandbox stopped. _(enum: `session_ended`, `idle_timeout`, `terminated`, `error`)_
  - `usage` — SandboxUsage — Resource consumption of a sandbox over its lifetime, as metric name to value, e.g. 'cpuSeconds', 'memoryMbPeak', 'networkEgressBytes', 'uptimeSeconds'. The set of metric names is not fixed and may grow.
    - _map of_ `number`
  - `stopErrorMessage` — string — Failure message when status is FAILED.

**`TestSnapshotRequestContent`**

- `command` — string — Command to run in the sandbox. Defaults to a no-op health check that only verifies the sandbox boots. _(minLen=1; maxLen=4000)_
- `timeoutSeconds` — number — Maximum run time in seconds. Defaults to 60. _(min=1; max=300)_

**`TestSnapshotResponseContent`**

- `exitCode` — number — Process exit code of the command; absent when the sandbox failed to boot.
- `stdout` — string
- `stderr` — string
- `timedOut` — boolean — True when the command was killed by the timeout.
- `durationMs` — number — How long the command ran, in milliseconds.
- `errorMessage` — string — Set when the sandbox failed to boot from the snapshot.

**`UpdateSnapshotRequestContent`**

- `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
- `description` — string _(minLen=1; maxLen=1000)_
- `commands` — array
  - _array of_ `string`
- `env` — array
  - _array of_ `EnvVar`
    - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
    - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
    - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
      - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
- `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
- `network` — SandboxNetworkPolicy
  - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
  - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
    - _array of_ `string`
- `revision` — number **(required)** — Snapshot revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.

**`UpdateSnapshotResponseContent`**

- `snapshot` — Snapshot **(required)** — The complete configuration of a snapshot. Everything except `name` and `description` is the build configuration. UpdateSnapshot can change it and queue a new immutable image while preserving the snapshot id.
  - `name` — string **(required)** _(pattern=^[a-zA-Z0-9][a-zA-Z0-9 _-]*$; minLen=1; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `commands` — array — Shell commands run in order at build time, on top of the platform runtime.
    - _array of_ `string`
  - `env` — array — Environment variables available at build time and to every sandbox.
    - _array of_ `EnvVar`
      - `name` — string **(required)** _(pattern=^[a-zA-Z_][a-zA-Z0-9_]*$; minLen=1; maxLen=256)_
      - `value` — string — Inline plaintext value. Mutually exclusive with `secret`.
      - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
        - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
  - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
  - `network` — SandboxNetworkPolicy
    - `access` — string — Network egress policy for sandboxes launched from the snapshot. _(enum: `allow-all`, `deny-all`, `allowlist`)_
    - `allowedDomains` — array — Domains reachable when access = ALLOWLIST.
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
  - `id` — string **(required)** — Stable identifier of a snapshot. Agents reference this id in their sandbox capability. _(minLen=12; maxLen=12)_
  - `status` — string **(required)** _(enum: `pending`, `building`, `ready`, `failed`)_
  - `revision` — number **(required)** — Monotonic revision incremented on every metadata update. Pass it back on update for optimistic locking.
  - `build` — SnapshotBuild — Outcome and metrics of the snapshot's image build.
    - `startedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `finishedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `imageDigest` — string — Content digest of the built image, e.g. 'sha256:...'.
    - `imageSizeBytes` — number — Size of the built image in bytes.
    - `errorCode` — string — Machine-readable failure code when status is FAILED, e.g. 'command_failed', 'build_timeout'.
    - `errorMessage` — string — Human-readable build failure message when status is FAILED.
  - `stats` — SnapshotStats — Aggregate runtime usage of a snapshot, populated on GetSnapshot.
    - `activeSandboxes` — number — Sandboxes currently running from this snapshot.
    - `totalSandboxes` — number — Total sandboxes ever launched from this snapshot.
    - `referencingAgents` — number — Number of agents currently referencing this snapshot.
    - `lastUsedAt` — string — Last time a sandbox was launched from this snapshot.

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

</details>
