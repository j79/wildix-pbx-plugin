## STT Service

_OpenAPI: STT service — version —_

**Servers**

- `https://stt.wildix.com` — Production
- `https://stt-stage.wildix.com` — Stage

### SpeechToText

#### `POST` `/api/v1/common`

Get transcription for a common audio

- operationId: `TranscribeCommon`
- **Request body** (`application/octet-stream` — `TranscribeCommonInputPayload`) **(required)**
  - string
- **Response 200** (`TranscribeCommonResponseContent`)
  - `type` — string **(required)**
  - `result` — array **(required)**
    - _array of_ `TranscriptionResult`
      - `transcript` — string — Audio transcription
- Errors: `400`, `401`, `500`

#### `POST` `/api/v1/voicemail`

Get transcription for a voicemail

- operationId: `TranscribeVoicemail`
- **Request body** (`application/octet-stream` — `TranscribeVoicemailInputPayload`) **(required)**
  - string
- **Response 200** (`TranscribeVoicemailResponseContent`)
  - `type` — string **(required)**
  - `result` — array **(required)**
    - _array of_ `TranscriptionResult`
      - `transcript` — string — Audio transcription
- Errors: `400`, `401`, `500`

### Routes non publiées — deprecated (en cours de décommissionnement)

> ⚠️ Les routes ci-dessous ont figuré dans une révision antérieure de la spécification publiée mais **n'y figurent plus**. Elles sont en cours de décommissionnement et peuvent encore répondre pendant quelques mois : leur description est conservée telle qu'elle était documentée, et la date de retrait est indiquée sur chacune. À ne pas utiliser pour de nouveaux développements.

#### `POST` `/api/v1/Common`

> ⚠️ **Statut : deprecated (non publiée)** — absente de la documentation depuis la révision du 2026-10-18 (groupe d'origine : _SpeechToText_). Équivalent publié : `POST /api/v1/common` (même section ; chemin renommé).

Get transcription for a common audio

- operationId: `TranscribeCommon`
- **Request body** (`application/json` — `TranscribeCommonRequestContent`)
  - `file` — string **(required)** — Audio file (ALAW/WAV/MP3)
  - `language` — string — Recognize language code _(enum: `af-ZA`, `am-ET`, `hy-AM`, `az-AZ`, `id-ID`, `ms-MY`, `bn-BD`, `bn-IN`, `ca-ES`, `cs-CZ`, `da-DK`, `de-DE`, … (+107))_
  - `encoding` — string — Audio encoding format _(enum: `LINEAR16`, `FLAC`, `MULAW`, `AMR`, `AMR_WB`)_
  - `hertz` — number — File hertz (8000-44100)
  - `maxAlternatives` — number — Recognize alternatives (1-15)
  - `phrases` — array — Array of string phrases to help recognize
    - _array of_ `string`
- **Response 200** (`TranscribeCommonResponseContent`)
  - `type` — string **(required)**
  - `result` — TranscriptionResult **(required)**
    - `transcript` — string — Audio transcription
- Errors: `400`, `401`, `500`

#### `POST` `/api/v1/Voicemail`

> ⚠️ **Statut : deprecated (non publiée)** — absente de la documentation depuis la révision du 2026-10-18 (groupe d'origine : _SpeechToText_). Équivalent publié : `POST /api/v1/voicemail` (même section ; chemin renommé).

Get transcription for a voicemail

- operationId: `TranscribeVoicemail`
- **Request body** (`application/json` — `TranscribeVoicemailRequestContent`)
  - `file` — string **(required)** — Audio file (ALAW/WAV/MP3)
  - `language` — string — Recognize language code _(enum: `af-ZA`, `am-ET`, `hy-AM`, `az-AZ`, `id-ID`, `ms-MY`, `bn-BD`, `bn-IN`, `ca-ES`, `cs-CZ`, `da-DK`, `de-DE`, … (+107))_
  - `encoding` — string — Audio encoding format _(enum: `LINEAR16`, `FLAC`, `MULAW`, `AMR`, `AMR_WB`)_
  - `hertz` — number — File hertz (8000-44100)
  - `maxAlternatives` — number — Recognize alternatives (1-15)
  - `phrases` — array — Array of string phrases to help recognize
    - _array of_ `string`
- **Response 200** (`TranscribeVoicemailResponseContent`)
  - `type` — string **(required)**
  - `result` — TranscriptionResult **(required)**
    - `transcript` — string — Audio transcription
- Errors: `400`, `401`, `500`

### Schemas appendix — STT Service

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

**`TranscribeCommonInputPayload`**

_multipart/form-data body: the audio file (ALAW/WAV/MP3) plus optional language, encoding, hertz, maxAlternatives and phrases[] fields_

- string

**`TranscribeCommonResponseContent`**

- `type` — string **(required)**
- `result` — array **(required)**
  - _array of_ `TranscriptionResult`
    - `transcript` — string — Audio transcription

**`TranscribeVoicemailInputPayload`**

_multipart/form-data body: the audio file (ALAW/WAV/MP3) plus optional language, encoding, hertz, maxAlternatives and phrases[] fields_

- string

**`TranscribeVoicemailResponseContent`**

- `type` — string **(required)**
- `result` — array **(required)**
  - _array of_ `TranscriptionResult`
    - `transcript` — string — Audio transcription

**`TranscriptionResult`**

- `transcript` — string — Audio transcription

**`UnauthorizedResponseContent`**

- `type` — string **(required)** _(default=error)_
- `reason` — string **(required)** _(default=Unauthorized)_
- `code` — string **(required)** _(default=Unauthorized)_

</details>
