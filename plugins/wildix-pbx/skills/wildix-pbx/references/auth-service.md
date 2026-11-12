## Auth Service

_OpenAPI: Auth V2 — version —_

**Servers**

- `https://auth.wildix.com` — Production
- `https://auth-stable.wildix.com` — Stable
- `https://auth-stage.wildix.com` — Stage

### Other

#### `POST` `/api/v2/cpa/`

Get CPA token

- operationId: `GetCPAToken`
- **Response 200** (`GetCPATokenResponseContent`)
  - `type` — string **(required)** _(default=result)_
  - `result` — CPATokenResult **(required)**
    - `token` — string **(required)**
    - `expires` — number **(required)**
- Errors: `401`

#### `POST` `/api/v2/openid/pbx/`

Get token for pbx

- operationId: `GetTokenForPbx`
- **Request body** (`application/json` — `GetTokenForPbxRequestContent`) **(required)**
  - `email` — string **(required)**
  - `domain` — string **(required)**
  - `scope` — string **(required)**
  - `aud` — string
- **Response 200** (`GetTokenForPbxResponseContent`)
  - `type` — string **(required)** _(default=result)_
  - `result` — TokenForPbxResult **(required)**
    - `id_token` — string **(required)**
    - `expires` — number **(required)**
- Errors: `400`, `401`

#### `POST` `/api/v2/openid/service/`

Get token for service

- operationId: `GetTokenForService`
- **Request body** (`application/json` — `GetTokenForServiceRequestContent`) **(required)**
  - `scope` — string **(required)**
  - `aud` — string **(required)**
  - `companyId` — string — Only for s2s auth
  - `email` — string — Only for s2s auth
- **Response 200** (`GetTokenForServiceResponseContent`)
  - `type` — string **(required)** _(default=result)_
  - `result` — OpenIdResult **(required)**
    - `id_token` — string **(required)**
    - `expires` — number **(required)**
- Errors: `400`, `401`

#### `POST` `/api/v2/s2s/`

Get service to service token

- operationId: `GetServiceToServiceToken`
- **Request body** (`application/json` — `GetServiceToServiceTokenRequestContent`) **(required)**
  - `clientId` — string **(required)**
  - `clientSecret` — string **(required)**
  - `scope` — string **(required)**
- **Response 200** (`GetServiceToServiceTokenResponseContent`)
  - `type` — string **(required)** _(default=result)_
  - `result` — ServiceToServiceToken **(required)**
    - `access_token` — string **(required)**
    - `expires_in` — number **(required)**
    - `token_type` — string **(required)**
- Errors: `400`, `401`

#### `GET` `/api/v2/token/`

Get token for auth service, deprecated api for old infrastructure

- operationId: `GetTokenForAuth`
- **Response 200** (`GetTokenForAuthResponseContent`)
  - `type` — string **(required)** _(default=result)_
  - `result` — GetTokenForAuthResult **(required)**
    - `accessToken` — string **(required)**
    - `refreshToken` — string **(required)**
- Errors: `401`

#### `GET` `/api/v2/token/{service}/`

Get token for service, deprecated api for old infrastructure

- operationId: `GetServiceToken`
- **Parameters**
  - `service` (path) — string **(required)**
- **Response 200** (`GetServiceTokenResponseContent`)
  - `type` — string **(required)** _(default=result)_
  - `result` — ServiceTokenResult **(required)**
    - `token` — string **(required)**
- Errors: `401`

#### `GET` `/api/v2/users/me/`

Get token for pbx, deprecated api for old infrastructure

- operationId: `GetSelfInfo`
- **Response 200** (`GetSelfInfoResponseContent`)
  - `type` — string **(required)** _(default=result)_
  - `result` — UserResult **(required)**
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `email` — string **(required)**
    - `extension` — string **(required)**
    - `language` — string **(required)**
    - `jid` — string **(required)**
    - `groupDn` — string **(required)**
    - `licenseType` — string **(required)**
    - `avatar` — string **(required)**
    - `dialplan` — string **(required)**
    - `pbx` — string **(required)**
    - `companyId` — string **(required)**
- Errors: `401`

### Schemas appendix — Auth Service

<details><summary>20 component schemas</summary>

**`CPATokenResult`**

- `token` — string **(required)**
- `expires` — number **(required)**

**`CustomValidationErrorsResponseContent`**

_Deprecated structure, only for auth service_

- `type` — string _(default=error)_
- `reason` — string _(default=Validation error)_

**`GetCPATokenResponseContent`**

- `type` — string **(required)** _(default=result)_
- `result` — CPATokenResult **(required)**
  - `token` — string **(required)**
  - `expires` — number **(required)**

**`GetSelfInfoResponseContent`**

- `type` — string **(required)** _(default=result)_
- `result` — UserResult **(required)**
  - `id` — string **(required)**
  - `name` — string **(required)**
  - `email` — string **(required)**
  - `extension` — string **(required)**
  - `language` — string **(required)**
  - `jid` — string **(required)**
  - `groupDn` — string **(required)**
  - `licenseType` — string **(required)**
  - `avatar` — string **(required)**
  - `dialplan` — string **(required)**
  - `pbx` — string **(required)**
  - `companyId` — string **(required)**

**`GetServiceToServiceTokenRequestContent`**

- `clientId` — string **(required)**
- `clientSecret` — string **(required)**
- `scope` — string **(required)**

**`GetServiceToServiceTokenResponseContent`**

- `type` — string **(required)** _(default=result)_
- `result` — ServiceToServiceToken **(required)**
  - `access_token` — string **(required)**
  - `expires_in` — number **(required)**
  - `token_type` — string **(required)**

**`GetServiceTokenResponseContent`**

- `type` — string **(required)** _(default=result)_
- `result` — ServiceTokenResult **(required)**
  - `token` — string **(required)**

**`GetTokenForAuthResponseContent`**

- `type` — string **(required)** _(default=result)_
- `result` — GetTokenForAuthResult **(required)**
  - `accessToken` — string **(required)**
  - `refreshToken` — string **(required)**

**`GetTokenForAuthResult`**

- `accessToken` — string **(required)**
- `refreshToken` — string **(required)**

**`GetTokenForPbxRequestContent`**

- `email` — string **(required)**
- `domain` — string **(required)**
- `scope` — string **(required)**
- `aud` — string

**`GetTokenForPbxResponseContent`**

- `type` — string **(required)** _(default=result)_
- `result` — TokenForPbxResult **(required)**
  - `id_token` — string **(required)**
  - `expires` — number **(required)**

**`GetTokenForServiceRequestContent`**

- `scope` — string **(required)**
- `aud` — string **(required)**
- `companyId` — string — Only for s2s auth
- `email` — string — Only for s2s auth

**`GetTokenForServiceResponseContent`**

- `type` — string **(required)** _(default=result)_
- `result` — OpenIdResult **(required)**
  - `id_token` — string **(required)**
  - `expires` — number **(required)**

**`OpenIdResult`**

- `id_token` — string **(required)**
- `expires` — number **(required)**

**`ServiceToServiceToken`**

- `access_token` — string **(required)**
- `expires_in` — number **(required)**
- `token_type` — string **(required)**

**`ServiceTokenResult`**

- `token` — string **(required)**

**`TokenForPbxResult`**

- `id_token` — string **(required)**
- `expires` — number **(required)**

**`UnauthorizedResponseContent`**

- `type` — string **(required)** _(default=error)_
- `reason` — string **(required)** _(default=Unauthorized)_
- `code` — string **(required)** _(default=Unauthorized)_

**`UserResult`**

- `id` — string **(required)**
- `name` — string **(required)**
- `email` — string **(required)**
- `extension` — string **(required)**
- `language` — string **(required)**
- `jid` — string **(required)**
- `groupDn` — string **(required)**
- `licenseType` — string **(required)**
- `avatar` — string **(required)**
- `dialplan` — string **(required)**
- `pbx` — string **(required)**
- `companyId` — string **(required)**

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

</details>
