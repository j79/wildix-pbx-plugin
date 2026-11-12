## URL-Preview Service

_OpenAPI: Url Preview service — version —_

**Servers**

- `https://url-preview.wildix.com` — Production
- `https://url-preview-stage.wildix.com` — Stage

### UrlPreview

#### `GET` `/api/v2/token/`

Echo the caller access token back

- operationId: `GetTokens`
- **Response 200** (`GetTokensResponseContent`)
  - `type` — string **(required)**
  - `result` — TokensResult **(required)**
    - `accessToken` — string — Caller access token
    - `refreshToken` — string — Refresh token, always empty
- Errors: `400`, `401`, `500`

#### `POST` `/api/v2/url/`

Generate Preview from url and return item

- operationId: `GeneratePreview`
- **Parameters**
  - `Accept-Language` (header) — string — Preview language, defaults to en
- **Request body** (`application/json` — `GeneratePreviewRequestContent`) **(required)**
  - `url` — string **(required)** — Url for parsing
- **Response 200** (`GeneratePreviewResponseContent`)
  - `type` — string **(required)**
  - `result` — UrlPreviewResult **(required)**
    - `id` — number — Preview ID (legacy, epoch seconds)
    - `url` — string — Original URL
    - `lang` — string — Page language
    - `title` — string — Page title
    - `description` — string — Page description
    - `image` — string — Preview image URL
- Errors: `400`, `401`, `500`

### Routes non publiées — deprecated (en cours de décommissionnement)

> ⚠️ Les routes ci-dessous ont figuré dans une révision antérieure de la spécification publiée mais **n'y figurent plus**. Elles sont en cours de décommissionnement et peuvent encore répondre pendant quelques mois : leur description est conservée telle qu'elle était documentée, et la date de retrait est indiquée sur chacune. À ne pas utiliser pour de nouveaux développements.

#### `POST` `/api/v2/Url/`

> ⚠️ **Statut : deprecated (non publiée)** — absente de la documentation depuis la révision du 2026-10-18 (groupe d'origine : _UrlPreview_). Équivalent publié : `POST /api/v2/url/` (même section ; chemin renommé).

Generate Preview from url and return item

- operationId: `GeneratePreview`
- **Request body** (`application/json` — `GeneratePreviewRequestContent`)
  - `url` — string **(required)** — Url for parsing
- **Response 200** (`GeneratePreviewResponseContent`)
  - `id` — number — Preview ID
  - `title` — string — Page title
  - `image` — string — Preview image URL
  - `lang` — string — Page language
  - `description` — string — Page description
  - `url` — string — Original URL
- Errors: `400`, `401`, `500`

### Schemas appendix — URL-Preview Service

<details><summary>8 component schemas</summary>

**`BadRequestErrorResponseContent`**

_Deprecated structure, only for PBXs_

- `type` — string — Error type
- `reason` — string — Error reason
- `code` — string — Error code

**`CustomInternalServerErrorResponseContent`**

_Deprecated structure, only for PBXs_

- `type` — string — Error type
- `reason` — string — Error reason
- `code` — string — Error code

**`GeneratePreviewRequestContent`**

- `url` — string **(required)** — Url for parsing

**`GeneratePreviewResponseContent`**

- `type` — string **(required)**
- `result` — UrlPreviewResult **(required)**
  - `id` — number — Preview ID (legacy, epoch seconds)
  - `url` — string — Original URL
  - `lang` — string — Page language
  - `title` — string — Page title
  - `description` — string — Page description
  - `image` — string — Preview image URL

**`GetTokensResponseContent`**

- `type` — string **(required)**
- `result` — TokensResult **(required)**
  - `accessToken` — string — Caller access token
  - `refreshToken` — string — Refresh token, always empty

**`TokensResult`**

- `accessToken` — string — Caller access token
- `refreshToken` — string — Refresh token, always empty

**`UnauthorizedResponseContent`**

- `type` — string **(required)** _(default=error)_
- `reason` — string **(required)** _(default=Unauthorized)_
- `code` — string **(required)** _(default=Unauthorized)_

**`UrlPreviewResult`**

- `id` — number — Preview ID (legacy, epoch seconds)
- `url` — string — Original URL
- `lang` — string — Page language
- `title` — string — Page title
- `description` — string — Page description
- `image` — string — Preview image URL

</details>
