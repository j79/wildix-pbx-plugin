## TTS Service

_OpenAPI: TTS service — version —_

**Servers**

- `https://tts.wildix.com` — Production
- `https://tts-stage.wildix.com` — Stage

### TextToSpeech

#### `GET` `/api/v2/audio`

Generate audio from text

- operationId: `GenerateAudio`
- **Parameters**
  - `text` (query) — string **(required)** — Input text
  - `voice` (query) — string — Polly voice id, defaults to Joanna
  - `engine` (query) — string — Convert engine _(enum: `standard`, `neural`)_
  - `speed` (query) — string — Audio speed in percent (20-200), defaults to 100
  - `volume` (query) — string — Audio volume in dB (-15 to 15), defaults to 0
  - `pitch` (query) — string — Audio pitch in percent (-30 to 50), standard engine only
- **Response 200** (`GenerateAudioOutputPayload`)
  - string
- Errors: `400`, `401`, `500`

#### `GET` `/api/v2/settings`

Get available voices for current engine

- operationId: `GetSettings`
- **Parameters**
  - `engine` (query) — string — Convert Engine _(enum: `standard`, `neural`)_
- **Response 200** (`GetSettingsResponseContent`)
  - `type` — string **(required)**
  - `result` — VoicesResult **(required)**
    - `voices` — array — Available Polly voices
      - _array of_ `Voice`
        - `id` — string — Voice ID
        - `title` — string — Voice title
        - `lang` — string — Voice language
- Errors: `400`, `401`, `500`

#### `GET` `/api/v2/token`

Echo the caller access token back

- operationId: `GetTokens`
- **Response 200** (`GetTokensResponseContent`)
  - `type` — string **(required)**
  - `result` — TokensResult **(required)**
    - `accessToken` — string — Caller access token
    - `refreshToken` — string — Refresh token, always empty
- Errors: `400`, `401`, `500`

#### `GET` `/api/v3/languages`

Get the languages a voice agent may be configured with

- operationId: `GetLanguages`
- **Response 200** (`GetLanguagesResponseContent`)
  - `languages` — any — Recognisable languages, sorted by channel code
- Errors: `400`, `401`, `500`

#### `GET` `/api/v3/voices`

Get the curated voice list used by bots

- operationId: `GetVoices`
- **Response 200** (`GetVoicesResponseContent`)
  - `voices` — any — Curated voices, sorted by language
- Errors: `400`, `401`, `500`

### Routes non publiées — deprecated (en cours de décommissionnement)

> ⚠️ Les routes ci-dessous ont figuré dans une révision antérieure de la spécification publiée mais **n'y figurent plus**. Elles sont en cours de décommissionnement et peuvent encore répondre pendant quelques mois : leur description est conservée telle qu'elle était documentée, et la date de retrait est indiquée sur chacune. À ne pas utiliser pour de nouveaux développements.

#### `GET` `/api/v2/Settings`

> ⚠️ **Statut : deprecated (non publiée)** — absente de la documentation depuis la révision du 2026-10-18 (groupe d'origine : _TextToSpeech_). Équivalent publié : `GET /api/v2/settings` (même section ; chemin renommé).

Get available voices for current engine

- operationId: `GetSettings`
- **Parameters**
  - `engine` (query) — string — Convert Engine _(enum: `standard`, `neural`)_
- **Response 200** (`GetSettingsResponseContent`)
  - `voices` — array — List of available voices
    - _array of_ `Voice`
      - `id` — string — Voice ID
      - `title` — string — Voice title
      - `lang` — string — Voice language
- Errors: `400`, `401`, `500`

#### `POST` `/api/v2/Audio`

> ⚠️ **Statut : deprecated (non publiée)** — absente de la documentation depuis la révision du 2026-10-18 (groupe d'origine : _TextToSpeech_). Équivalent publié : `GET /api/v2/audio` (même section ; chemin renommé).

Generate audio from text

- operationId: `GenerateAudio`
- **Request body** (`application/json` — `GenerateAudioRequestContent`)
  - `text` — string **(required)** — Input text
  - `engine` — string — TTS convert engine _(enum: `standard`, `neural`)_
  - `speed` — number — Audio speed (20-200)
  - `volume` — number — Audio volume (-15 to 15)
- Errors: `400`, `401`, `500`

### Schemas appendix — TTS Service

<details><summary>12 component schemas</summary>

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

**`GenerateAudioOutputPayload`**

- string

**`GetLanguagesResponseContent`**

- `languages` — any — Recognisable languages, sorted by channel code

**`GetSettingsResponseContent`**

- `type` — string **(required)**
- `result` — VoicesResult **(required)**
  - `voices` — array — Available Polly voices
    - _array of_ `Voice`
      - `id` — string — Voice ID
      - `title` — string — Voice title
      - `lang` — string — Voice language

**`GetTokensResponseContent`**

- `type` — string **(required)**
- `result` — TokensResult **(required)**
  - `accessToken` — string — Caller access token
  - `refreshToken` — string — Refresh token, always empty

**`GetVoicesResponseContent`**

- `voices` — any — Curated voices, sorted by language

**`TokensResult`**

- `accessToken` — string — Caller access token
- `refreshToken` — string — Refresh token, always empty

**`TtsEngine`**

_TTS convert engine_

- string _(enum: `standard`, `neural`)_

**`UnauthorizedResponseContent`**

- `type` — string **(required)** _(default=error)_
- `reason` — string **(required)** _(default=Unauthorized)_
- `code` — string **(required)** _(default=Unauthorized)_

**`Voice`**

- `id` — string — Voice ID
- `title` — string — Voice title
- `lang` — string — Voice language

**`VoicesResult`**

- `voices` — array — Available Polly voices
  - _array of_ `Voice`
    - `id` — string — Voice ID
    - `title` — string — Voice title
    - `lang` — string — Voice language

</details>
