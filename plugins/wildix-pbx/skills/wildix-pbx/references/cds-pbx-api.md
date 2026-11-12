## CDS PBX API

_OpenAPI: CDS - pbx part — version —_

**Servers**

- `https://cds-pbx.wildix.com` — Production
- `https://cds-pbx-stable.wildix.com` — Stable
- `https://cds-pbx-stage.wildix.com` — Stage

### Other

#### `GET` `/api/v1/{type}`

Get items by type

- operationId: `GetItems`
- **Scopes**: `storage:GetItems`, `storage:read`
- **Parameters**
  - `type` (path) — string **(required)** _(enum: `voicemails`, `recordings`, `faxes`, `backups`, `traces`)_
  - `count` (query) — number _(default=15; min=1; max=1000)_
  - `start` (query) — string — Use the 'start' parameter provided in the 'nextPage' field of the response to retrieve the next set of results _(default=)_
  - `order` (query) — string _(default=desc)_
  - `from` (query) — number — Time from - timestamp
  - `to` (query) — number — Time to - timestamp
- **Response 200** (`GetItemsResponseContent`)
  - `items` — array **(required)**
    - _array of_ `PbxFile`
      - `name` — string **(required)**
      - `owner` — string **(required)**
      - `created` — number **(required)**
      - `companyId` — string **(required)**
      - `region` — string **(required)**
      - `size` — number **(required)**
      - `serial` — string **(required)**
      - `domain` — string **(required)**
  - `nextPage` — string **(required)** — Link to retrieve the next set of results
- Errors: `400`, `403`, `404`

#### `POST` `/api/v1/{type}`

Get presigned URL for for upload file by type

- operationId: `GetPresignedUploadUrl`
- **Parameters**
  - `type` (path) — string **(required)** _(enum: `voicemails`, `recordings`, `faxes`, `backups`, `traces`)_
- **Request body** (`application/json` — `GetPresignedUploadUrlRequestContent`) **(required)**
  - `name` — string **(required)** _(pattern=^[^/#]*$; minLen=1; maxLen=255)_
  - `owner` — string _(default=system; pattern=^[^/#]*$)_
  - `needProcess` — boolean _(default=False)_
  - `created` — string
- **Response 200** (`GetPresignedUploadUrlResponseContent`)
  - `path` — string **(required)**
- Errors: `400`, `403`, `404`

#### `GET` `/api/v1/{type}/{id}`

Download item by id

- operationId: `GetPresignedDownloadUrl`
- **Scopes**: `storage:GetPresignedDownloadUrl`, `storage:read`
- **Parameters**
  - `type` (path) — string **(required)** _(enum: `voicemails`, `recordings`, `faxes`, `backups`, `traces`)_
  - `id` (path) — string **(required)**
- **Response 200** (`GetPresignedDownloadUrlResponseContent`)
  - `path` — string
- Errors: `400`, `403`, `404`

#### `DELETE` `/api/v1/{type}/{id}`

Delete item by id

- operationId: `DeleteItem`
- **Scopes**: `storage:DeleteItem`
- **Parameters**
  - `type` (path) — string **(required)** _(enum: `voicemails`, `recordings`, `faxes`, `backups`, `traces`)_
  - `id` (path) — string **(required)**
- **Response 200** (`DeleteItemResponseContent`)
  - `success` — boolean **(required)**
- Errors: `400`, `403`, `404`

#### `POST` `/v1/batch-delete`

Create a task for deleting list of files

- operationId: `CreateBatchDeleteTask`
- **Scopes**: `storage:CreateBatchDeleteTask`
- **Request body** (`application/json` — `CreateBatchDeleteTaskRequestContent`) **(required)**
  - `type` — string **(required)** _(enum: `voicemails`, `recordings`, `faxes`, `backups`, `traces`)_
  - `items` — array
    - _array of_ `string`
- **Response 200** (`CreateBatchDeleteTaskResponseContent`)
  - `success` — boolean **(required)**
- Errors: `400`, `403`, `404`

#### `POST` `/v1/download`

Create task for preparing list of files for downloading

- operationId: `CreateDownloadTask`
- **Scopes**: `storage:CreateDownloadTask`
- **Request body** (`application/json` — `CreateDownloadTaskRequestContent`) **(required)**
  - `type` — string **(required)** _(enum: `voicemails`, `recordings`, `faxes`, `backups`, `traces`)_
  - `from` — number — Time from - timestamp
  - `to` — number — Time to - timestamp
- **Response 200** (`CreateDownloadTaskResponseContent`)
  - `id` — string **(required)** — Id task in queue
  - `from` — number **(required)** — Time from - timestamp
  - `to` — number **(required)** — Time to - timestamp
- Errors: `400`, `403`, `404`

#### `GET` `/v1/download/{id}`

Check status of task by ID

- operationId: `GetDownloadTaskStatus`
- **Scopes**: `storage:GetDownloadTaskStatus`, `storage:read`
- **Parameters**
  - `id` (path) — string **(required)**
- **Response 200** (`GetDownloadTaskStatusResponseContent`)
  - `status` — string **(required)**
  - `path` — string
- Errors: `400`, `403`, `404`

### Schemas appendix — CDS PBX API

<details><summary>17 component schemas</summary>

**`BadRequestExceptionResponseContent`**

- `message` — string **(required)**

**`CreateBatchDeleteTaskRequestContent`**

- `type` — string **(required)** _(enum: `voicemails`, `recordings`, `faxes`, `backups`, `traces`)_
- `items` — array
  - _array of_ `string`

**`CreateBatchDeleteTaskResponseContent`**

- `success` — boolean **(required)**

**`CreateDownloadTaskRequestContent`**

- `type` — string **(required)** _(enum: `voicemails`, `recordings`, `faxes`, `backups`, `traces`)_
- `from` — number — Time from - timestamp
- `to` — number — Time to - timestamp

**`CreateDownloadTaskResponseContent`**

- `id` — string **(required)** — Id task in queue
- `from` — number **(required)** — Time from - timestamp
- `to` — number **(required)** — Time to - timestamp

**`DeleteItemResponseContent`**

- `success` — boolean **(required)**

**`ErrorData`**

- `reason` — string **(required)**
- `code` — string **(required)**

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetDownloadTaskStatusResponseContent`**

- `status` — string **(required)**
- `path` — string

**`GetItemsResponseContent`**

- `items` — array **(required)**
  - _array of_ `PbxFile`
    - `name` — string **(required)**
    - `owner` — string **(required)**
    - `created` — number **(required)**
    - `companyId` — string **(required)**
    - `region` — string **(required)**
    - `size` — number **(required)**
    - `serial` — string **(required)**
    - `domain` — string **(required)**
- `nextPage` — string **(required)** — Link to retrieve the next set of results

**`GetPresignedDownloadUrlResponseContent`**

- `path` — string

**`GetPresignedUploadUrlRequestContent`**

- `name` — string **(required)** _(pattern=^[^/#]*$; minLen=1; maxLen=255)_
- `owner` — string _(default=system; pattern=^[^/#]*$)_
- `needProcess` — boolean _(default=False)_
- `created` — string

**`GetPresignedUploadUrlResponseContent`**

- `path` — string **(required)**

**`NotFoundExceptionResponseContent`**

- `type` — object **(required)**
- `result` — ErrorData **(required)**
  - `reason` — string **(required)**
  - `code` — string **(required)**

**`PbxFile`**

- `name` — string **(required)**
- `owner` — string **(required)**
- `created` — number **(required)**
- `companyId` — string **(required)**
- `region` — string **(required)**
- `size` — number **(required)**
- `serial` — string **(required)**
- `domain` — string **(required)**

**`PbxFileTypes`**

- string _(enum: `voicemails`, `recordings`, `faxes`, `backups`, `traces`)_

**`ResponseType`**

- string _(enum: `result`, `error`)_

</details>
