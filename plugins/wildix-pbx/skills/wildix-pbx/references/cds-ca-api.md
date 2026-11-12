## CDS CA API

_OpenAPI: CDS - cloud analytics — version —_

**Servers**

- `https://cds-ca.wildix.com` — Production
- `https://cds-ca-stable.wildix.com` — Stable
- `https://cds-ca-stage.wildix.com` — Stage

### Other

#### `GET` `/v1/calls`

Get call history

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| AUTH_OPEN_ID_USER | 60 | 10 |
| AUTH_OPEN_ID_USER | 3600 | 100 |

- operationId: `GetCalls`
- **Scopes**: `analytics:GetCalls`, `analytics:read`
- **Parameters**
  - `dateFrom` (query) — string — Date from. The date should be in the format: YYYY-MM-DD. Defaults to dateTo minus 1 day if not provided. _(pattern=^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$)_
  - `dateTo` (query) — string — Date to. The date should be in the format: YYYY-MM-DD. Defaults to the current date if not provided. _(pattern=^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$)_
  - `status` (query) — string — Status _(enum: `COMPLETED`, `MISSED`)_
  - `direction` (query) — string — Direction _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
  - `limit` (query) — number — The maximum number of rows to return. _(default=1000; min=1; max=3000)_
  - `offset` (query) — number — The offset from which to start. _(default=0; min=0)_
- **Response 200** (`GetCallsResponseContent`)
  - `items` — array **(required)**
    - _array of_ `Call`
      - `id` — string **(required)**
      - `sessionId` — string **(required)**
      - `type` — string **(required)**
      - `time` — string **(required)**
      - `startTime` — string **(required)**
      - `connectTime` — number **(required)**
      - `connectTimeMs` — number **(required)**
      - `talkTime` — number **(required)**
      - `talkTimeMs` — number **(required)**
      - `waitTime` — number **(required)**
      - `waitTimeMs` — number **(required)**
      - `queueTime` — number **(required)**
      - `queueTimeMs` — number **(required)**
      - `holdTime` — number **(required)**
      - `holdTimeMs` — number **(required)**
      - `duration` — number **(required)**
      - `durationMs` — number **(required)**
      - `pbx` — string **(required)**
      - `part` — number **(required)**
      - `service` — string **(required)**
      - `direction` — string **(required)** _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
      - `flags` — string **(required)**
      - `callDestination` — string **(required)**
      - `serviceNumber` — string **(required)**
      - `callCallerType` — string **(required)**
      - `callCallerPhone` — string **(required)**
      - `callCallerName` — string **(required)**
      - `callCallerCompany` — string **(required)**
      - `callCallerEmail` — string **(required)**
      - `callCallerUserId` — string **(required)**
      - `callCallerUserExtension` — string **(required)**
      - `callCallerGroupId` — string **(required)**
      - `callCallerGroupName` — string **(required)**
      - `callCallerDevice` — string **(required)**
      - `callTrunkName` — string **(required)**
      - `callTrunkDirection` — string **(required)**
      - `status` — string **(required)** _(enum: `COMPLETED`, `MISSED`)_
      - `callRemotePhone` — string **(required)**
      - `callRemoteCountryCode` — string **(required)**
      - `callRemoteCountryCodeStr` — string **(required)**
      - `callRemoteLocation` — string **(required)**
      - `callEndCause` — string **(required)**
      - `callEndCauseStr` — string **(required)**
      - `callEndBy` — string **(required)**
      - `callCalleePhone` — string **(required)**
      - `callCalleeType` — string **(required)**
      - `callCalleeName` — string **(required)**
      - `callCalleeCompany` — string **(required)**
      - `callCalleeEmail` — string **(required)**
      - `callCalleeUserId` — string **(required)**
      - `callCalleeUserExtension` — string **(required)**
      - `callCalleeGroupId` — string **(required)**
      - `callCalleeGroupName` — string **(required)**
      - `callCalleeDevice` — string **(required)**
      - `callGroupId` — string **(required)**
      - `callGroupName` — string **(required)**
      - `callRecordings` — string **(required)**
      - `tags` — string **(required)**
      - `callSplitReason` — string **(required)**
      - `callSplitTransferType` — string **(required)**
      - `callMergeWith` — string **(required)**
      - `callCallerMos` — string **(required)**
      - `callCalleeMos` — string **(required)**
      - `conferenceId` — string **(required)**
      - `conferenceSubject` — string **(required)**
- Errors: `400`, `403`, `429`

#### `POST` `/v1/dumps`

Create a dump file and get the task id in the queue

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| AUTH_OPEN_ID_USER | 60 | 10 |
| AUTH_OPEN_ID_USER | 3600 | 100 |

- operationId: `CreateDump`
- **Scopes**: `analytics:CreateDump`
- **Parameters**
  - `dateFrom` (query) — string — Date from. The date should be in the format: YYYY-MM-DD. Defaults to dateTo minus 1 day if not provided. _(pattern=^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$)_
  - `dateTo` (query) — string — Date to. The date should be in the format: YYYY-MM-DD. Defaults to the current date if not provided. _(pattern=^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$)_
  - `status` (query) — string — Status _(enum: `COMPLETED`, `MISSED`)_
  - `direction` (query) — string — Direction _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
- **Request body** (`application/json` — `CreateDumpRequestContent`) **(required)**
  - `type` — string **(required)** _(enum: `calls`)_
- **Response 200** (`CreateDumpResponseContent`)
  - `id` — string **(required)** — Id of task in queue
- Errors: `400`, `403`, `429`

#### `GET` `/v1/dumps/{id}`

Checking the task completion status and receiving a link for download dump file

- operationId: `GetDump`
- **Scopes**: `analytics:GetDump`, `analytics:read`
- **Parameters**
  - `id` (path) — string **(required)** — Id of task in queue
- **Response 200** (`GetDumpResponseContent`)
  - `status` — string **(required)** _(enum: `PROCESSED`, `COMPLETED`)_
  - `presignedDownloadUrl` — string — Presigned url for download
- Errors: `400`, `403`, `404`

### Schemas appendix — CDS CA API

<details><summary>13 component schemas</summary>

**`Call`**

- `id` — string **(required)**
- `sessionId` — string **(required)**
- `type` — string **(required)**
- `time` — string **(required)**
- `startTime` — string **(required)**
- `connectTime` — number **(required)**
- `connectTimeMs` — number **(required)**
- `talkTime` — number **(required)**
- `talkTimeMs` — number **(required)**
- `waitTime` — number **(required)**
- `waitTimeMs` — number **(required)**
- `queueTime` — number **(required)**
- `queueTimeMs` — number **(required)**
- `holdTime` — number **(required)**
- `holdTimeMs` — number **(required)**
- `duration` — number **(required)**
- `durationMs` — number **(required)**
- `pbx` — string **(required)**
- `part` — number **(required)**
- `service` — string **(required)**
- `direction` — string **(required)** _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
- `flags` — string **(required)**
- `callDestination` — string **(required)**
- `serviceNumber` — string **(required)**
- `callCallerType` — string **(required)**
- `callCallerPhone` — string **(required)**
- `callCallerName` — string **(required)**
- `callCallerCompany` — string **(required)**
- `callCallerEmail` — string **(required)**
- `callCallerUserId` — string **(required)**
- `callCallerUserExtension` — string **(required)**
- `callCallerGroupId` — string **(required)**
- `callCallerGroupName` — string **(required)**
- `callCallerDevice` — string **(required)**
- `callTrunkName` — string **(required)**
- `callTrunkDirection` — string **(required)**
- `status` — string **(required)** _(enum: `COMPLETED`, `MISSED`)_
- `callRemotePhone` — string **(required)**
- `callRemoteCountryCode` — string **(required)**
- `callRemoteCountryCodeStr` — string **(required)**
- `callRemoteLocation` — string **(required)**
- `callEndCause` — string **(required)**
- `callEndCauseStr` — string **(required)**
- `callEndBy` — string **(required)**
- `callCalleePhone` — string **(required)**
- `callCalleeType` — string **(required)**
- `callCalleeName` — string **(required)**
- `callCalleeCompany` — string **(required)**
- `callCalleeEmail` — string **(required)**
- `callCalleeUserId` — string **(required)**
- `callCalleeUserExtension` — string **(required)**
- `callCalleeGroupId` — string **(required)**
- `callCalleeGroupName` — string **(required)**
- `callCalleeDevice` — string **(required)**
- `callGroupId` — string **(required)**
- `callGroupName` — string **(required)**
- `callRecordings` — string **(required)**
- `tags` — string **(required)**
- `callSplitReason` — string **(required)**
- `callSplitTransferType` — string **(required)**
- `callMergeWith` — string **(required)**
- `callCallerMos` — string **(required)**
- `callCalleeMos` — string **(required)**
- `conferenceId` — string **(required)**
- `conferenceSubject` — string **(required)**

**`CallDirection`**

- string _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_

**`CheckDumpStatuses`**

- string _(enum: `PROCESSED`, `COMPLETED`)_

**`ConversationStatus`**

- string _(enum: `COMPLETED`, `MISSED`)_

**`CreateDumpRequestContent`**

- `type` — string **(required)** _(enum: `calls`)_

**`CreateDumpResponseContent`**

- `id` — string **(required)** — Id of task in queue

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetCallsResponseContent`**

- `items` — array **(required)**
  - _array of_ `Call`
    - `id` — string **(required)**
    - `sessionId` — string **(required)**
    - `type` — string **(required)**
    - `time` — string **(required)**
    - `startTime` — string **(required)**
    - `connectTime` — number **(required)**
    - `connectTimeMs` — number **(required)**
    - `talkTime` — number **(required)**
    - `talkTimeMs` — number **(required)**
    - `waitTime` — number **(required)**
    - `waitTimeMs` — number **(required)**
    - `queueTime` — number **(required)**
    - `queueTimeMs` — number **(required)**
    - `holdTime` — number **(required)**
    - `holdTimeMs` — number **(required)**
    - `duration` — number **(required)**
    - `durationMs` — number **(required)**
    - `pbx` — string **(required)**
    - `part` — number **(required)**
    - `service` — string **(required)**
    - `direction` — string **(required)** _(enum: `INTERNAL`, `INBOUND`, `OUTBOUND`, `UNDEFINED`)_
    - `flags` — string **(required)**
    - `callDestination` — string **(required)**
    - `serviceNumber` — string **(required)**
    - `callCallerType` — string **(required)**
    - `callCallerPhone` — string **(required)**
    - `callCallerName` — string **(required)**
    - `callCallerCompany` — string **(required)**
    - `callCallerEmail` — string **(required)**
    - `callCallerUserId` — string **(required)**
    - `callCallerUserExtension` — string **(required)**
    - `callCallerGroupId` — string **(required)**
    - `callCallerGroupName` — string **(required)**
    - `callCallerDevice` — string **(required)**
    - `callTrunkName` — string **(required)**
    - `callTrunkDirection` — string **(required)**
    - `status` — string **(required)** _(enum: `COMPLETED`, `MISSED`)_
    - `callRemotePhone` — string **(required)**
    - `callRemoteCountryCode` — string **(required)**
    - `callRemoteCountryCodeStr` — string **(required)**
    - `callRemoteLocation` — string **(required)**
    - `callEndCause` — string **(required)**
    - `callEndCauseStr` — string **(required)**
    - `callEndBy` — string **(required)**
    - `callCalleePhone` — string **(required)**
    - `callCalleeType` — string **(required)**
    - `callCalleeName` — string **(required)**
    - `callCalleeCompany` — string **(required)**
    - `callCalleeEmail` — string **(required)**
    - `callCalleeUserId` — string **(required)**
    - `callCalleeUserExtension` — string **(required)**
    - `callCalleeGroupId` — string **(required)**
    - `callCalleeGroupName` — string **(required)**
    - `callCalleeDevice` — string **(required)**
    - `callGroupId` — string **(required)**
    - `callGroupName` — string **(required)**
    - `callRecordings` — string **(required)**
    - `tags` — string **(required)**
    - `callSplitReason` — string **(required)**
    - `callSplitTransferType` — string **(required)**
    - `callMergeWith` — string **(required)**
    - `callCallerMos` — string **(required)**
    - `callCalleeMos` — string **(required)**
    - `conferenceId` — string **(required)**
    - `conferenceSubject` — string **(required)**

**`GetDumpResponseContent`**

- `status` — string **(required)** _(enum: `PROCESSED`, `COMPLETED`)_
- `presignedDownloadUrl` — string — Presigned url for download

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`RateLimitExceededExceptionResponseContent`**

- `message` — string **(required)** _(default=Too Many Requests)_

**`TypeOfDumps`**

- string _(enum: `calls`)_

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

</details>
