## CDS Utils API

_OpenAPI: CDS - utils — version —_

**Servers**

- `https://cds-utils.wildix.com` — Production
- `https://cds-utils-stable.wildix.com` — Stable
- `https://cds-utils-stage.wildix.com` — Stage

### Other

#### `POST` `/v1/preview`

Create preview image for file and return publick link

- operationId: `CreatePreview`
- **Request body** (`application/json` — `CreatePreviewRequestContent`) **(required)**
  - `companyId` — string **(required)**
  - `category` — string **(required)**
  - `id` — string **(required)**
- **Response 200** (`CreatePreviewResponseContent`)
  - `url` — string **(required)**
- Errors: `400`, `404`

### Schemas appendix — CDS Utils API

<details><summary>4 component schemas</summary>

**`BadRequestExceptionResponseContent`**

- `message` — string **(required)**

**`CreatePreviewRequestContent`**

- `companyId` — string **(required)**
- `category` — string **(required)**
- `id` — string **(required)**

**`CreatePreviewResponseContent`**

- `url` — string **(required)**

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

</details>
