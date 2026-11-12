## MFA Service

_OpenAPI: MFA service — version —_

**Servers**

- `https://mfa.wildix.com` — Production
- `https://mfa-stage.wildix.com` — Stage

### Mfa

#### `GET` `/api/v1/trusted-login/{userId}`

Get / check allowed IP addresses for user

- operationId: `GetAllowedIpForUser`
- **Parameters**
  - `userId` (path) — string **(required)** — PBX User ID
  - `ip` (query) — string — If received input IP address we check allow this address
- **Response 200** (`GetAllowedIpForUserResponseContent`)
  - `type` — string **(required)**
  - `result` — array **(required)**
    - _array of_ `TrustedIpItem`
      - `ip` — string — IP address
      - `companyId` — string — Company ID
      - `userId` — number — PBX User ID
      - `country` — string — Country
      - `fullAddress` — string — Full address
      - `updatedAt` — string — Updated date
- Errors: `400`, `401`, `404`, `500`

#### `POST` `/api/v1/trusted-login/{userId}`

Add allowed IP address for user

- operationId: `AddAllowedIpForUser`
- **Parameters**
  - `userId` (path) — string **(required)** — PBX User ID
- **Request body** (`application/json` — `AddAllowedIpForUserRequestContent`) **(required)**
  - `ip` — string **(required)** — IP address to trust
  - `country` — string — Country
  - `fullAddress` — string — Full address
- **Response 200** (`AddAllowedIpForUserResponseContent`)
  - `type` — string **(required)**
  - `result` — string **(required)**
- Errors: `400`, `401`, `404`, `500`

#### `DELETE` `/api/v1/trusted-login/{userId}/{ip}`

Delete IP address for user

- operationId: `DeleteIpForUser`
- **Parameters**
  - `userId` (path) — string **(required)** — PBX User ID
  - `ip` (path) — string **(required)** — IP address
- **Response 200** (`DeleteIpForUserResponseContent`)
  - `type` — string **(required)**
  - `result` — string **(required)**
- Errors: `400`, `401`, `404`, `500`

### Schemas appendix — MFA Service

<details><summary>9 component schemas</summary>

**`AddAllowedIpForUserRequestContent`**

- `ip` — string **(required)** — IP address to trust
- `country` — string — Country
- `fullAddress` — string — Full address

**`AddAllowedIpForUserResponseContent`**

- `type` — string **(required)**
- `result` — string **(required)**

**`BadRequestErrorResponseContent`**

_Deprecated structure, only for PBXs_

- `type` — string — Error type
- `reason` — string — Error reason
- `code` — string — Error code

**`DeleteIpForUserResponseContent`**

- `type` — string **(required)**
- `result` — string **(required)**

**`GetAllowedIpForUserResponseContent`**

- `type` — string **(required)**
- `result` — array **(required)**
  - _array of_ `TrustedIpItem`
    - `ip` — string — IP address
    - `companyId` — string — Company ID
    - `userId` — number — PBX User ID
    - `country` — string — Country
    - `fullAddress` — string — Full address
    - `updatedAt` — string — Updated date

**`InternalServerErrorResponseContent`**

- `message` — string **(required)**

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`TrustedIpItem`**

- `ip` — string — IP address
- `companyId` — string — Company ID
- `userId` — number — PBX User ID
- `country` — string — Country
- `fullAddress` — string — Full address
- `updatedAt` — string — Updated date

**`UnauthorizedResponseContent`**

- `type` — string **(required)** _(default=error)_
- `reason` — string **(required)** _(default=Unauthorized)_
- `code` — string **(required)** _(default=Unauthorized)_

</details>
