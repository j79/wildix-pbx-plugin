## Filesharing Service

_OpenAPI: FS service — version v2_

**Servers**

- `https://fs.wildix.com` — Production
- `https://fs-stage.wildix.com` — Stage

### Other

#### `POST` `/api/v2/File/`

Add (register) a new file on the server

- operationId: `AddFile`
- **Request body** (`application/json` — `AddFileRequestContent`) **(required)**
  - `name` — string **(required)** — Uploaded file name
  - `type` — string **(required)** — Content type
  - `size` — number **(required)** — File size in bytes
- **Response 200** (`AddFileResponseContent`)
  - `type` — string — Response type
  - `result` — FileData
    - `id` — string — File ID (fsId)
    - `name` — string — File name
    - `type` — string — Content type
    - `size` — number — File size in bytes
    - `date` — string — Created date
    - `url` — string — File URL
    - `thumbnail` — string — Thumbnail URL
    - `thumbnailWidth` — number — Thumbnail width
    - `thumbnailHeight` — number — Thumbnail height
    - `thumbnailQuality` — number — Thumbnail quality (0-100)
    - `previewDecoded` — string — Thumbnail base64 encoded
    - `scalePreviewDecoded` — number — Thumbnail scale for previewDecoded (0-1) _(format=float)_
- Errors: `400`, `401`, `500`

#### `GET` `/api/v2/file/{fsId}`

Download a file from server

- operationId: `DownloadFile`
- **Parameters**
  - `fsId` (path) — string **(required)** — File ID
- **Response 200** (`DownloadFileOutputPayload`)
  - string
- Errors: `400`, `401`, `404`, `500`

#### `POST` `/api/v2/file/{fsId}`

Upload a file to the server

- operationId: `UploadFile`
- **Parameters**
  - `fsId` (path) — string **(required)** — File ID
- **Request body** (`application/octet-stream` — `UploadFileInputPayload`) **(required)**
  - string
- **Response 200** (`UploadFileResponseContent`)
  - `type` — string — Response type
  - `result` — FileData
    - `id` — string — File ID (fsId)
    - `name` — string — File name
    - `type` — string — Content type
    - `size` — number — File size in bytes
    - `date` — string — Created date
    - `url` — string — File URL
    - `thumbnail` — string — Thumbnail URL
    - `thumbnailWidth` — number — Thumbnail width
    - `thumbnailHeight` — number — Thumbnail height
    - `thumbnailQuality` — number — Thumbnail quality (0-100)
    - `previewDecoded` — string — Thumbnail base64 encoded
    - `scalePreviewDecoded` — number — Thumbnail scale for previewDecoded (0-1) _(format=float)_
- Errors: `400`, `500`

#### `GET` `/api/v2/file/{fsId}/Info/`

Get info for file

- operationId: `GetFileInfo`
- **Parameters**
  - `fsId` (path) — string **(required)** — File ID
- **Response 200** (`GetFileInfoResponseContent`)
  - `type` — string — Response type
  - `result` — FileData
    - `id` — string — File ID (fsId)
    - `name` — string — File name
    - `type` — string — Content type
    - `size` — number — File size in bytes
    - `date` — string — Created date
    - `url` — string — File URL
    - `thumbnail` — string — Thumbnail URL
    - `thumbnailWidth` — number — Thumbnail width
    - `thumbnailHeight` — number — Thumbnail height
    - `thumbnailQuality` — number — Thumbnail quality (0-100)
    - `previewDecoded` — string — Thumbnail base64 encoded
    - `scalePreviewDecoded` — number — Thumbnail scale for previewDecoded (0-1) _(format=float)_
- Errors: `400`, `404`, `500`

#### `GET` `/api/v2/file/{fsId}/Thumbnail/`

Download a thumbnail for file

- operationId: `DownloadThumbnail`
- **Parameters**
  - `fsId` (path) — string **(required)** — File ID
- **Response 200** (`DownloadThumbnailOutputPayload`)
  - string
- Errors: `400`, `404`, `500`

### Schemas appendix — Filesharing Service

<details><summary>12 component schemas</summary>

**`AddFileRequestContent`**

- `name` — string **(required)** — Uploaded file name
- `type` — string **(required)** — Content type
- `size` — number **(required)** — File size in bytes

**`AddFileResponseContent`**

- `type` — string — Response type
- `result` — FileData
  - `id` — string — File ID (fsId)
  - `name` — string — File name
  - `type` — string — Content type
  - `size` — number — File size in bytes
  - `date` — string — Created date
  - `url` — string — File URL
  - `thumbnail` — string — Thumbnail URL
  - `thumbnailWidth` — number — Thumbnail width
  - `thumbnailHeight` — number — Thumbnail height
  - `thumbnailQuality` — number — Thumbnail quality (0-100)
  - `previewDecoded` — string — Thumbnail base64 encoded
  - `scalePreviewDecoded` — number — Thumbnail scale for previewDecoded (0-1) _(format=float)_

**`CustomInternalServerErrorResponseContent`**

_Deprecated structure, only for PBXs_

- `type` — string — Error type
- `reason` — string — Error reason
- `code` — string — Error code

**`CustomNotFoundErrorResponseContent`**

_Deprecated structure, only for PBXs_

- `type` — string — Error type
- `reason` — string — Error reason
- `code` — string — Error code

**`DownloadFileOutputPayload`**

- string

**`DownloadThumbnailOutputPayload`**

- string

**`FileData`**

- `id` — string — File ID (fsId)
- `name` — string — File name
- `type` — string — Content type
- `size` — number — File size in bytes
- `date` — string — Created date
- `url` — string — File URL
- `thumbnail` — string — Thumbnail URL
- `thumbnailWidth` — number — Thumbnail width
- `thumbnailHeight` — number — Thumbnail height
- `thumbnailQuality` — number — Thumbnail quality (0-100)
- `previewDecoded` — string — Thumbnail base64 encoded
- `scalePreviewDecoded` — number — Thumbnail scale for previewDecoded (0-1) _(format=float)_

**`GetFileInfoResponseContent`**

- `type` — string — Response type
- `result` — FileData
  - `id` — string — File ID (fsId)
  - `name` — string — File name
  - `type` — string — Content type
  - `size` — number — File size in bytes
  - `date` — string — Created date
  - `url` — string — File URL
  - `thumbnail` — string — Thumbnail URL
  - `thumbnailWidth` — number — Thumbnail width
  - `thumbnailHeight` — number — Thumbnail height
  - `thumbnailQuality` — number — Thumbnail quality (0-100)
  - `previewDecoded` — string — Thumbnail base64 encoded
  - `scalePreviewDecoded` — number — Thumbnail scale for previewDecoded (0-1) _(format=float)_

**`UnauthorizedResponseContent`**

- `type` — string **(required)** _(default=error)_
- `reason` — string **(required)** _(default=Unauthorized)_
- `code` — string **(required)** _(default=Unauthorized)_

**`UploadFileInputPayload`**

_File content_

- string

**`UploadFileResponseContent`**

- `type` — string — Response type
- `result` — FileData
  - `id` — string — File ID (fsId)
  - `name` — string — File name
  - `type` — string — Content type
  - `size` — number — File size in bytes
  - `date` — string — Created date
  - `url` — string — File URL
  - `thumbnail` — string — Thumbnail URL
  - `thumbnailWidth` — number — Thumbnail width
  - `thumbnailHeight` — number — Thumbnail height
  - `thumbnailQuality` — number — Thumbnail quality (0-100)
  - `previewDecoded` — string — Thumbnail base64 encoded
  - `scalePreviewDecoded` — number — Thumbnail scale for previewDecoded (0-1) _(format=float)_

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

</details>
