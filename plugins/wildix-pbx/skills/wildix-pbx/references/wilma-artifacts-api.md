## Wilma Artifacts API

_OpenAPI: Wilma Artifacts Service — version v2_

**Servers**

- `https://api.wilma.wildix.com` — Production
- `https://api-stable.wilma.wildix.com` — Stable
- `https://api-stage.wilma.wildix.com` — Stage

### Artifacts

#### `GET` `/v2/artifacts`

Lists artifacts. Listing is contextual: filter by the producing session or task (and optionally channel, agent or kind). There is no global company-wide browser — discovery of artifacts outside their producing context happens via shared links.

- operationId: `ListArtifacts`
- **Scopes**: `wilma-artifacts:ListArtifacts`, `wilma-artifacts:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the artifacts belong to. Optional: identifies the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
  - `sessionId` (query) — string — Only artifacts produced by this session. _(minLen=1; maxLen=128)_
  - `taskId` (query) — string — Only artifacts produced by this background task.
  - `channel` (query) — string — Only artifacts produced on this channel. Never matches task-produced artifacts, which carry no channel. _(enum: `voice`, `chat`, `assistant`)_
  - `agentId` (query) — string — Only artifacts produced by this agent. _(minLen=12; maxLen=12)_
  - `kind` (query) — string — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
  - `from` (query) — string — Only artifacts created at or after this time.
  - `to` (query) — string — Only artifacts created before this time.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListArtifactsResponseContent`)
  - `artifacts` — array **(required)**
    - _array of_ `Artifact`
      - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
      - `title` — string **(required)** — Human-readable title shown in the UI.
      - `description` — string — One-line summary shown under the title.
      - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
      - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
        - _array of_ `ArtifactFile`
          - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
          - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
          - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
      - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
      - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
        - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
        - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
        - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
        - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
        - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
      - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
      - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
        - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
        - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
      - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
        - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
          - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
          - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
            - _array of_ `ArtifactPrincipal`
              - _(nesting depth limit — see `ArtifactPrincipal` in the Schemas appendix)_
        - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
      - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
      - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
      - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

#### `POST` `/v2/artifacts`

Registers a new artifact and returns a short-lived presigned URL to upload its content.
    Runtime-facing: called by the channel runtimes (assistant, chat, workflows) when an agent
    shares an artifact, not by end clients. The artifact becomes downloadable once the upload
    completes.

- operationId: `CreateArtifact`
- **Scopes**: `wilma-artifacts:CreateArtifact`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the artifact belongs to (the owner). Optional: identifies the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `CreateArtifactRequestContent`) **(required)**
  - `title` — string **(required)** — Human-readable title shown in the UI.
  - `name` — string — Download filename, e.g. 'report.md'. _(minLen=1; maxLen=1024)_
  - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
  - `contentType` — string — MIME type of the content, e.g. 'text/markdown'.
  - `size` — number — Size in bytes of the content that will be uploaded.
  - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
    - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
    - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
    - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
    - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
    - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
- **Response 200** (`CreateArtifactResponseContent`)
  - `artifact` — Artifact **(required)** — An output an agent produced and shared back during a session or task. Each revision is one file in CDS: render it through GetArtifactContentUrl, download it via DownloadArtifact.
    - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `title` — string **(required)** — Human-readable title shown in the UI.
    - `description` — string — One-line summary shown under the title.
    - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
    - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
      - _array of_ `ArtifactFile`
        - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
        - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
        - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
    - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
    - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
      - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
      - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
      - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
      - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
    - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
    - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
      - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
      - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
    - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
      - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
        - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
        - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
          - _array of_ `ArtifactPrincipal`
            - _oneOf_ — exactly one of:
              - **`userId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`groupId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
    - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
    - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `uploadUrl` — string **(required)** — Presigned URL to PUT the artifact content to.
  - `uploadExpiresAt` — string **(required)** — ISO-8601 expiry of the upload URL.
- Errors: `400`, `403`

#### `GET` `/v2/artifacts/items/{artifactId}`

Gets the metadata of a single artifact revision. Accessible to the owner, granted principals, and — when visibility is `company` — any authenticated user of the same company.

- operationId: `GetArtifact`
- **Scopes**: `wilma-artifacts:GetArtifact`, `wilma-artifacts:read`
- **Parameters**
  - `artifactId` (path) — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the artifact belongs to. Optional: identifies the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
  - `revision` (query) — number — Revision to read. Omit for the latest revision. Earlier uploads remain available under the artifact's current access settings. _(min=1)_
- **Response 200** (`GetArtifactResponseContent`)
  - `artifact` — Artifact **(required)** — An output an agent produced and shared back during a session or task. Each revision is one file in CDS: render it through GetArtifactContentUrl, download it via DownloadArtifact.
    - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `title` — string **(required)** — Human-readable title shown in the UI.
    - `description` — string — One-line summary shown under the title.
    - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
    - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
      - _array of_ `ArtifactFile`
        - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
        - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
        - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
    - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
    - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
      - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
      - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
      - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
      - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
    - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
    - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
      - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
      - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
    - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
      - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
        - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
        - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
          - _array of_ `ArtifactPrincipal`
            - _oneOf_ — exactly one of:
              - **`userId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`groupId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
    - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
    - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- Errors: `400`, `403`, `404`

#### `DELETE` `/v2/artifacts/items/{artifactId}`

Permanently deletes an artifact, all retained revisions and their CDS files, and invalidates any share link. Terminal and not reversible.

- operationId: `DeleteArtifact`
- **Scopes**: `wilma-artifacts:DeleteArtifact`
- **Parameters**
  - `artifactId` (path) — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the artifact belongs to. Optional: identifies the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`

#### `GET` `/v2/artifacts/items/{artifactId}/content-url`

Returns a short-lived URL that serves an artifact's content for rendering. The entry file sits
    under a signed prefix that every other file of the artifact also resolves against, so a site's
    relative links, stylesheets, scripts and images load exactly as they would from a web server:
    `baseUrl` + a file's `path` serves that file. The URL needs no authorization header, so it can
    be an iframe `src`, an `img` `src` or a plain `fetch`. HTML, SVG and XML are served with a
    sandboxing Content-Security-Policy (an opaque origin, no storage, no cookies, network limited to
    the artifact's own files and a few public CDNs), which holds even if the URL is opened directly;
    render such content in an iframe, never inline in the host page. Same access rules as GetArtifact.

- operationId: `GetArtifactContentUrl`
- **Scopes**: `wilma-artifacts:GetArtifactContentUrl`, `wilma-artifacts:read`
- **Parameters**
  - `artifactId` (path) — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the artifact belongs to. Optional: identifies the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
  - `revision` (query) — number — Revision to read. Omit for the latest revision. Earlier uploads remain available under the artifact's current access settings. _(min=1)_
- **Response 200** (`GetArtifactContentUrlResponseContent`)
  - `url` — string **(required)** — URL of the entry file, ready to render.
  - `baseUrl` — string **(required)** — The signed prefix, ending with `/`. Append a file's `path` (each segment URI-encoded) to serve that file.
  - `expiresAt` — string **(required)** — ISO-8601 expiry of both URLs. Request a new one to keep rendering past it.
  - `artifact` — Artifact **(required)** — An output an agent produced and shared back during a session or task. Each revision is one file in CDS: render it through GetArtifactContentUrl, download it via DownloadArtifact.
    - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `title` — string **(required)** — Human-readable title shown in the UI.
    - `description` — string — One-line summary shown under the title.
    - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
    - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
      - _array of_ `ArtifactFile`
        - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
        - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
        - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
    - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
    - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
      - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
      - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
      - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
      - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
    - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
    - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
      - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
      - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
    - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
      - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
        - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
        - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
          - _array of_ `ArtifactPrincipal`
            - _oneOf_ — exactly one of:
              - **`userId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`groupId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
    - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
    - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- Errors: `400`, `403`, `404`

#### `GET` `/v2/artifacts/items/{artifactId}/download`

Returns a short-lived URL to download an artifact's content: the file itself for a single-file artifact, the stored ZIP for a bundle. Same access rules as GetArtifact.

- operationId: `DownloadArtifact`
- **Scopes**: `wilma-artifacts:DownloadArtifact`, `wilma-artifacts:read`
- **Parameters**
  - `artifactId` (path) — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the artifact belongs to. Optional: identifies the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
  - `revision` (query) — number — Revision to read. Omit for the latest revision. Earlier uploads remain available under the artifact's current access settings. _(min=1)_
- **Response 200** (`DownloadArtifactResponseContent`)
  - `url` — string **(required)** — Short-lived download URL. It needs no authorization header, so hand it straight to the browser.
  - `expiresAt` — string **(required)** — ISO-8601 expiry of the URL.
  - `artifact` — Artifact **(required)** — An output an agent produced and shared back during a session or task. Each revision is one file in CDS: render it through GetArtifactContentUrl, download it via DownloadArtifact.
    - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `title` — string **(required)** — Human-readable title shown in the UI.
    - `description` — string — One-line summary shown under the title.
    - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
    - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
      - _array of_ `ArtifactFile`
        - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
        - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
        - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
    - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
    - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
      - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
      - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
      - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
      - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
    - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
    - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
      - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
      - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
    - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
      - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
        - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
        - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
          - _array of_ `ArtifactPrincipal`
            - _oneOf_ — exactly one of:
              - **`userId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`groupId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
    - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
    - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- Errors: `400`, `403`, `404`

#### `GET` `/v2/artifacts/items/{artifactId}/share-url`

Returns the shareable URL of an artifact whose visibility is `company` using the configured viewer base and artifact id. The URL points to the authenticated artifact viewer and works outside any session context; fails with ConflictException when the artifact is private.

- operationId: `GetArtifactShareUrl`
- **Scopes**: `wilma-artifacts:GetArtifactShareUrl`, `wilma-artifacts:read`
- **Parameters**
  - `artifactId` (path) — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the artifact belongs to. Optional: identifies the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
- **Response 200** (`GetArtifactShareUrlResponseContent`)
  - `url` — string **(required)** — Stable viewer link for service/channel callers. Browser hosts may build their own link from their viewer origin and the artifact id. Contains the artifact id, not an access token; current access settings are checked on every metadata request.
- Errors: `400`, `403`, `404`, `409`

#### `PUT` `/v2/artifacts/items/{artifactId}/sharing`

Sets an artifact's sharing settings: specific per-user/group grants plus a general access
    level — `private` (owner + granted users only) or `company` (anyone in the owner's company
    with the link, sign-in required). The viewer URL is stable across sharing changes. Moving
    back to `private` removes company-wide access; the owner and granted users retain access.
    Already-issued content and download URLs remain usable until their expiry.

- operationId: `UpdateArtifactSharing`
- **Scopes**: `wilma-artifacts:UpdateArtifactSharing`
- **Parameters**
  - `artifactId` (path) — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the artifact belongs to. Optional: identifies the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `UpdateArtifactSharingRequestContent`) **(required)**
  - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
    - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
    - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
      - _array of_ `ArtifactPrincipal`
        - _oneOf_ — exactly one of:
          - **`userId`**
            - `userId` — string **(required)** _(minLen=12; maxLen=12)_
          - **`groupId`**
            - `groupId` — string **(required)**
  - `notify` — ArtifactShareNotify — People to notify when sharing changes, with an optional message.
    - `emails` — array **(required)**
      - _array of_ `string`
    - `message` — string
- **Response 200** (`UpdateArtifactSharingResponseContent`)
  - `artifact` — Artifact **(required)** — An output an agent produced and shared back during a session or task. Each revision is one file in CDS: render it through GetArtifactContentUrl, download it via DownloadArtifact.
    - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `title` — string **(required)** — Human-readable title shown in the UI.
    - `description` — string — One-line summary shown under the title.
    - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
    - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
      - _array of_ `ArtifactFile`
        - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
        - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
        - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
    - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
    - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
      - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
      - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
      - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
      - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
    - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
    - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
      - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
      - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
    - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
      - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
        - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
        - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
          - _array of_ `ArtifactPrincipal`
            - _oneOf_ — exactly one of:
              - **`userId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`groupId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
    - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
    - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- Errors: `400`, `403`, `404`

### Schemas appendix — Wilma Artifacts API

<details><summary>24 component schemas</summary>

**`Artifact`**

_An output an agent produced and shared back during a session or task. Each revision is one file in CDS: render it through GetArtifactContentUrl, download it via DownloadArtifact._

- `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
- `title` — string **(required)** — Human-readable title shown in the UI.
- `description` — string — One-line summary shown under the title.
- `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
- `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
  - _array of_ `ArtifactFile`
    - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
    - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
    - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
- `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
- `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
  - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
  - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
  - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
  - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
  - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
- `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
- `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
  - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
  - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
- `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
  - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
    - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
    - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
      - _array of_ `ArtifactPrincipal`
        - _(nesting depth limit — see `ArtifactPrincipal` in the Schemas appendix)_
  - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
- `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
- `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
- `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`ArtifactAccess`**

_Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only._

- `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
- `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
  - _array of_ `ArtifactPrincipal`
    - _oneOf_ — exactly one of:
      - **`userId`**
        - `userId` — string **(required)** _(minLen=12; maxLen=12)_
      - **`groupId`**
        - `groupId` — string **(required)**

**`ArtifactCapabilities`**

_What the caller may do with an artifact, resolved for the identity that made the request._

- `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
- `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.

**`ArtifactFile`**

_A file available for preview or download: the single file of an artifact, or an entry inside its archive._

- `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
- `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
- `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.

**`ArtifactKind`**

_Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest._

- string _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_

**`ArtifactPrincipal`**

_A user or group granted direct access to an artifact._

- _oneOf_ — exactly one of:
  - **`userId`**
    - `userId` — string **(required)** _(minLen=12; maxLen=12)_
  - **`groupId`**
    - `groupId` — string **(required)**

**`ArtifactShareNotify`**

_People to notify when sharing changes, with an optional message._

- `emails` — array **(required)**
  - _array of_ `string`
- `message` — string

**`ArtifactSharing`**

_Current sharing state of an artifact._

- `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
  - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
  - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
    - _array of_ `ArtifactPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.

**`ArtifactSource`**

_Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface._

- `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
- `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
- `taskId` — string — Background task (wilma-workflows) that produced the artifact.
- `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
- `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_

**`ArtifactVisibility`**

_General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again._

- string _(enum: `private`, `company`)_

**`ChannelType`**

_A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel._

- string _(enum: `voice`, `chat`, `assistant`)_

**`ConflictExceptionResponseContent`**

_The request conflicts with the current state of the resource, e.g. a duplicate name, a resource still in use, or an unmet precondition._

- `message` — string **(required)**

**`CreateArtifactRequestContent`**

- `title` — string **(required)** — Human-readable title shown in the UI.
- `name` — string — Download filename, e.g. 'report.md'. _(minLen=1; maxLen=1024)_
- `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
- `contentType` — string — MIME type of the content, e.g. 'text/markdown'.
- `size` — number — Size in bytes of the content that will be uploaded.
- `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
  - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
  - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
  - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
  - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
  - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_

**`CreateArtifactResponseContent`**

- `artifact` — Artifact **(required)** — An output an agent produced and shared back during a session or task. Each revision is one file in CDS: render it through GetArtifactContentUrl, download it via DownloadArtifact.
  - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `title` — string **(required)** — Human-readable title shown in the UI.
  - `description` — string — One-line summary shown under the title.
  - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
  - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
    - _array of_ `ArtifactFile`
      - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
      - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
      - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
  - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
  - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
    - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
    - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
    - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
    - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
    - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
  - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
  - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
    - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
    - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
  - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
    - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
      - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
      - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
        - _(nesting depth limit — see `ArtifactPrincipal` in the Schemas appendix)_
    - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
  - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
  - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `uploadUrl` — string **(required)** — Presigned URL to PUT the artifact content to.
- `uploadExpiresAt` — string **(required)** — ISO-8601 expiry of the upload URL.

**`DownloadArtifactResponseContent`**

- `url` — string **(required)** — Short-lived download URL. It needs no authorization header, so hand it straight to the browser.
- `expiresAt` — string **(required)** — ISO-8601 expiry of the URL.
- `artifact` — Artifact **(required)** — An output an agent produced and shared back during a session or task. Each revision is one file in CDS: render it through GetArtifactContentUrl, download it via DownloadArtifact.
  - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `title` — string **(required)** — Human-readable title shown in the UI.
  - `description` — string — One-line summary shown under the title.
  - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
  - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
    - _array of_ `ArtifactFile`
      - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
      - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
      - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
  - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
  - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
    - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
    - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
    - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
    - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
    - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
  - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
  - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
    - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
    - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
  - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
    - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
      - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
      - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
        - _(nesting depth limit — see `ArtifactPrincipal` in the Schemas appendix)_
    - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
  - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
  - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetArtifactContentUrlResponseContent`**

- `url` — string **(required)** — URL of the entry file, ready to render.
- `baseUrl` — string **(required)** — The signed prefix, ending with `/`. Append a file's `path` (each segment URI-encoded) to serve that file.
- `expiresAt` — string **(required)** — ISO-8601 expiry of both URLs. Request a new one to keep rendering past it.
- `artifact` — Artifact **(required)** — An output an agent produced and shared back during a session or task. Each revision is one file in CDS: render it through GetArtifactContentUrl, download it via DownloadArtifact.
  - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `title` — string **(required)** — Human-readable title shown in the UI.
  - `description` — string — One-line summary shown under the title.
  - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
  - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
    - _array of_ `ArtifactFile`
      - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
      - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
      - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
  - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
  - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
    - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
    - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
    - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
    - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
    - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
  - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
  - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
    - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
    - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
  - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
    - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
      - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
      - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
        - _(nesting depth limit — see `ArtifactPrincipal` in the Schemas appendix)_
    - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
  - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
  - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`GetArtifactResponseContent`**

- `artifact` — Artifact **(required)** — An output an agent produced and shared back during a session or task. Each revision is one file in CDS: render it through GetArtifactContentUrl, download it via DownloadArtifact.
  - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `title` — string **(required)** — Human-readable title shown in the UI.
  - `description` — string — One-line summary shown under the title.
  - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
  - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
    - _array of_ `ArtifactFile`
      - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
      - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
      - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
  - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
  - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
    - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
    - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
    - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
    - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
    - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
  - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
  - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
    - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
    - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
  - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
    - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
      - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
      - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
        - _(nesting depth limit — see `ArtifactPrincipal` in the Schemas appendix)_
    - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
  - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
  - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`GetArtifactShareUrlResponseContent`**

- `url` — string **(required)** — Stable viewer link for service/channel callers. Browser hosts may build their own link from their viewer origin and the artifact id. Contains the artifact id, not an access token; current access settings are checked on every metadata request.

**`ListArtifactsResponseContent`**

- `artifacts` — array **(required)**
  - _array of_ `Artifact`
    - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `title` — string **(required)** — Human-readable title shown in the UI.
    - `description` — string — One-line summary shown under the title.
    - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
    - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
      - _array of_ `ArtifactFile`
        - _(nesting depth limit — see `ArtifactFile` in the Schemas appendix)_
    - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
    - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
      - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
      - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
      - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
      - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
    - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
    - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
      - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
      - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
    - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
      - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
        - _(nesting depth limit — see `ArtifactAccess` in the Schemas appendix)_
      - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
    - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
    - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`UpdateArtifactSharingRequestContent`**

- `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
  - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
  - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
    - _array of_ `ArtifactPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `notify` — ArtifactShareNotify — People to notify when sharing changes, with an optional message.
  - `emails` — array **(required)**
    - _array of_ `string`
  - `message` — string

**`UpdateArtifactSharingResponseContent`**

- `artifact` — Artifact **(required)** — An output an agent produced and shared back during a session or task. Each revision is one file in CDS: render it through GetArtifactContentUrl, download it via DownloadArtifact.
  - `id` — string **(required)** — Nano-id artifact identifier (12 characters), unguessable by design. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `title` — string **(required)** — Human-readable title shown in the UI.
  - `description` — string — One-line summary shown under the title.
  - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
  - `files` — array **(required)** — Files available in this revision: one for a single file, or the entries inside a bundle archive. _(minItems=1; maxItems=500)_
    - _array of_ `ArtifactFile`
      - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
      - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
      - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
  - `entry` — string — Path of the file the viewer opens first; when supplied, always one of files. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
  - `source` — ArtifactSource **(required)** — Provenance of an artifact: the runtime, session or task, and agent that produced it. Exactly one reference is present: a channel session sets `channel` and `sessionId`, a background task sets `taskId` and no channel, since a task has no delivery surface.
    - `channel` — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
    - `sessionId` — string — Session that produced the artifact (assistant / chat channels). _(minLen=1; maxLen=128)_
    - `taskId` — string — Background task (wilma-workflows) that produced the artifact.
    - `agentId` — string — Agent that produced the artifact. _(minLen=12; maxLen=12)_
    - `agentVersion` — number — Published agent version that produced the artifact; absent for draft runs. _(min=1)_
  - `ownerId` — string — The user the artifact belongs to. Absent when a service produced it outside any user's session. _(minLen=12; maxLen=12)_
  - `capabilities` — ArtifactCapabilities — What the caller may do with an artifact, resolved for the identity that made the request.
    - `canShare` — boolean **(required)** — Whether the caller may change the artifact's sharing settings.
    - `canDelete` — boolean **(required)** — Whether the caller may delete the artifact.
  - `sharing` — ArtifactSharing **(required)** — Current sharing state of an artifact.
    - `access` — ArtifactAccess **(required)** — Sharing settings for an artifact: specific per-user/group grants ("people with access") plus a general access level. Shared access is view-only.
      - `visibility` — string **(required)** — General access level of an artifact, applied on top of any specific-user grants. Shared access is view-only. Artifacts are company-internal: there is no public level, and every access requires authentication. Moving back to `private` removes company-wide access; the same viewer link still opens for the owner and granted users. Sharing can be enabled again. _(enum: `private`, `company`)_
      - `grants` — array — Specific users or groups granted direct view access, independent of `visibility`. The owner always has access.
        - _(nesting depth limit — see `ArtifactPrincipal` in the Schemas appendix)_
    - `sharedAt` — string — ISO-8601 time the current period of company-wide sharing began. Absent while private.
  - `revision` — number **(required)** — Monotonic revision, incremented each time the agent republishes the artifact in place. _(min=1)_
  - `latestRevision` — number **(required)** — Latest available revision, even when a historical revision was requested. _(min=1)_
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

</details>
