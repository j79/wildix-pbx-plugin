## WNS Email API

_OpenAPI: WNS - email notification — version v2_

**Servers**

- `https://notifications.wildix.com` — Production
- `https://notifications-stable.wildix.com` — Stable
- `https://notifications-stage.wildix.com` — Stage

### Other

#### `POST` `/api/v2/mail`

Send email

- operationId: `SendEmail`
- **Request body** (`application/json` — `SendEmailRequestContent`) **(required)**
  - `to` — array **(required)** — The email address (and name, optionally) of the recipients. Interchangeable with Recipients. Acceptable formats are john@example.com. Can include multiple contacts, which should be separated by commas. Can be used together with Cc and Bcc.
    - _array of_ `string`
  - `subject` — string **(required)** — The email subject line.
  - `html` — string **(required)** — Provides the Text part of the message. Mandatory, if the "text" parameter is not specified.
  - `cc` — array — The email address (and name, optionally) of a recipient who is supposed to receive a carbon copy (cc) of this message. Used together with To and Bcc (optional). Acceptable formats are john@example.com. Can include multiple contacts, which should be separated by commas.
    - _array of_ `string`
  - `bcc` — array — The email address (and name, optionally) of a recipient who is supposed to receive a blind carbon copy (bcc) of this message. Use this when you do not want your other recipients to see that you are sending a copy of the message to this email address. Used together with To and Cc (optional). Acceptable formats are john@example.com. Can include multiple contacts, which should be separated by commas.
    - _array of_ `string`
  - `attachments` — array — List of the files attached to this message. The total size of attachments (including inline) should not exceed 15 MB.
    - _array of_ `Attachment`
      - `filename` — string
      - `fileKey` — string
  - `text` — string — Provides the Text part of the message. Mandatory, if the "html" parameter is not specified.
  - `replyTo` — string
- **Response 200** (`SendEmailResponseContent`)
  - `type` — string **(required)** — Type of result _(default=result)_
  - `result` — SendEmailResult **(required)**
    - `messageId` — string **(required)**
- Errors: `400`

#### `POST` `/api/v2/mail/admin`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Send email to admin

- operationId: `SendEmailToAdmin`
- **Request body** (`application/json` — `SendEmailToAdminRequestContent`) **(required)**
  - `companyId` — string **(required)** — ID of the company the PBX belongs to. _(minLen=3; maxLen=30)_
  - `templateKey` — string **(required)** — Identifier of the email template (e.g., integration_warning, integration_paused).
  - `params` — array — Dynamic parameters to fill into the template (e.g., integration name, timestamps, error summary).
    - _array of_ `TemplateParam`
      - `key` — string **(required)**
      - `value` — any **(required)** — The value can be of any type
- **Response 200** (`SendEmailToAdminResponseContent`)
  - `type` — string **(required)** — Type of result _(default=result)_
  - `result` — SendEmailResult **(required)**
    - `messageId` — string **(required)**
- Errors: `400`

#### `POST` `/api/v2/mail/template`

Send templated email

- operationId: `SendTemplatedEmail`
- **Request body** (`application/json` — `SendTemplatedEmailRequestContent`) **(required)**
  - `companyId` — string **(required)** — The unique identifier of the tenant. _(minLen=3; maxLen=30)_
  - `templateKey` — string **(required)** — Identifier of the email template (e.g., integration_warning, integration_paused).
  - `emails` — array — The array of the recipients' email addresses. Acceptable formats are john@example.com. Can include multiple contacts, which should be separated by commas. Note: if the emails field is an empty array or is not provided, it means the email will be sent to the company Admin user.
    - _array of_ `string`
  - `params` — array — Dynamic parameters to fill into the template (e.g., integration name, timestamps, error, summary).
    - _array of_ `TemplateParam`
      - `key` — string **(required)**
      - `value` — any **(required)** — The value can be of any type
- **Response 200** (`SendTemplatedEmailResponseContent`)
  - `type` — string **(required)** — Type of result _(default=result)_
  - `result` — SendEmailsResult **(required)**
    - `messageIds` — array **(required)**
      - _array of_ `string`
- Errors: `400`

#### `POST` `/api/v2/url`

Create pressigned url for attacments

- operationId: `CreatePresignedUrl`
- **Response 200** (`CreatePresignedUrlResponseContent`)
  - `type` — string **(required)** — Type of result _(default=result)_
  - `result` — PresignedUrlResult **(required)**
    - `url` — string **(required)** — Presigned url for upload file
    - `fileKey` — string **(required)** — File id
- Errors: `400`

### Schemas appendix — WNS Email API

<details><summary>14 component schemas</summary>

**`Attachment`**

- `filename` — string
- `fileKey` — string

**`BadRequestExceptionResponseContent`**

- `message` — string **(required)**

**`CreatePresignedUrlResponseContent`**

- `type` — string **(required)** — Type of result _(default=result)_
- `result` — PresignedUrlResult **(required)**
  - `url` — string **(required)** — Presigned url for upload file
  - `fileKey` — string **(required)** — File id

**`CustomBadRequestExceptionResponseContent`**

- `reason` — string **(required)** _(default=Invalid request body)_
- `type` — string **(required)** _(default=error)_
- `code` — string **(required)** _(default=Error)_

**`PresignedUrlResult`**

- `url` — string **(required)** — Presigned url for upload file
- `fileKey` — string **(required)** — File id

**`SendEmailRequestContent`**

- `to` — array **(required)** — The email address (and name, optionally) of the recipients. Interchangeable with Recipients. Acceptable formats are john@example.com. Can include multiple contacts, which should be separated by commas. Can be used together with Cc and Bcc.
  - _array of_ `string`
- `subject` — string **(required)** — The email subject line.
- `html` — string **(required)** — Provides the Text part of the message. Mandatory, if the "text" parameter is not specified.
- `cc` — array — The email address (and name, optionally) of a recipient who is supposed to receive a carbon copy (cc) of this message. Used together with To and Bcc (optional). Acceptable formats are john@example.com. Can include multiple contacts, which should be separated by commas.
  - _array of_ `string`
- `bcc` — array — The email address (and name, optionally) of a recipient who is supposed to receive a blind carbon copy (bcc) of this message. Use this when you do not want your other recipients to see that you are sending a copy of the message to this email address. Used together with To and Cc (optional). Acceptable formats are john@example.com. Can include multiple contacts, which should be separated by commas.
  - _array of_ `string`
- `attachments` — array — List of the files attached to this message. The total size of attachments (including inline) should not exceed 15 MB.
  - _array of_ `Attachment`
    - `filename` — string
    - `fileKey` — string
- `text` — string — Provides the Text part of the message. Mandatory, if the "html" parameter is not specified.
- `replyTo` — string

**`SendEmailResponseContent`**

- `type` — string **(required)** — Type of result _(default=result)_
- `result` — SendEmailResult **(required)**
  - `messageId` — string **(required)**

**`SendEmailResult`**

- `messageId` — string **(required)**

**`SendEmailToAdminRequestContent`**

- `companyId` — string **(required)** — ID of the company the PBX belongs to. _(minLen=3; maxLen=30)_
- `templateKey` — string **(required)** — Identifier of the email template (e.g., integration_warning, integration_paused).
- `params` — array — Dynamic parameters to fill into the template (e.g., integration name, timestamps, error summary).
  - _array of_ `TemplateParam`
    - `key` — string **(required)**
    - `value` — any **(required)** — The value can be of any type

**`SendEmailToAdminResponseContent`**

- `type` — string **(required)** — Type of result _(default=result)_
- `result` — SendEmailResult **(required)**
  - `messageId` — string **(required)**

**`SendEmailsResult`**

- `messageIds` — array **(required)**
  - _array of_ `string`

**`SendTemplatedEmailRequestContent`**

- `companyId` — string **(required)** — The unique identifier of the tenant. _(minLen=3; maxLen=30)_
- `templateKey` — string **(required)** — Identifier of the email template (e.g., integration_warning, integration_paused).
- `emails` — array — The array of the recipients' email addresses. Acceptable formats are john@example.com. Can include multiple contacts, which should be separated by commas. Note: if the emails field is an empty array or is not provided, it means the email will be sent to the company Admin user.
  - _array of_ `string`
- `params` — array — Dynamic parameters to fill into the template (e.g., integration name, timestamps, error, summary).
  - _array of_ `TemplateParam`
    - `key` — string **(required)**
    - `value` — any **(required)** — The value can be of any type

**`SendTemplatedEmailResponseContent`**

- `type` — string **(required)** — Type of result _(default=result)_
- `result` — SendEmailsResult **(required)**
  - `messageIds` — array **(required)**
    - _array of_ `string`

**`TemplateParam`**

- `key` — string **(required)**
- `value` — any **(required)** — The value can be of any type

</details>
