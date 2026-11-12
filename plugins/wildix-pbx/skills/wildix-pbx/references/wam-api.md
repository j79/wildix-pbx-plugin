## WAM API

_OpenAPI: WAM - auth for cloud analytics — version v1_

**Servers**

- `https://wam.wildix.com` — Production
- `https://wam-stable.wildix.com` — Stable
- `https://wam-stage.wildix.com` — Stage

### Other

#### `GET` `/api/v1/ts/collaboration`

Get auth info for cloud analytics in collaboration

- operationId: `GetTokenForCollaboration`
- **Response 200** (`GetTokenForCollaborationResponseContent`)
  - `type` — string **(required)** _(default=result)_
  - `result` — AuthResult **(required)**
    - `token` — string **(required)** — Token for authorization
    - `licenseType` — string _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_
- Errors: `400`, `403`

#### `POST` `/api/v1/ts/user/delete`

Delete user

- operationId: `DeleteUser`
- **Request body** (`application/json` — `DeleteUserRequestContent`) **(required)**
  - `uid` — string **(required)** — PBX User Id
  - `email` — string **(required)** — User email
- Errors: `400`, `403`

#### `GET` `/api/v1/ts/xbees`

Get auth info for cloud analytics in xbees

- operationId: `GetTokenForXbees`
- **Response 200** (`GetTokenForXbeesResponseContent`)
  - `type` — string **(required)** _(default=result)_
  - `result` — AuthResult **(required)**
    - `token` — string **(required)** — Token for authorization
    - `licenseType` — string _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_
- Errors: `400`, `403`

### Schemas appendix — WAM API

<details><summary>7 component schemas</summary>

**`AuthResult`**

- `token` — string **(required)** — Token for authorization
- `licenseType` — string _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_

**`BadRequestExceptionResponseContent`**

- `message` — string **(required)**

**`DeleteUserRequestContent`**

- `uid` — string **(required)** — PBX User Id
- `email` — string **(required)** — User email

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetTokenForCollaborationResponseContent`**

- `type` — string **(required)** _(default=result)_
- `result` — AuthResult **(required)**
  - `token` — string **(required)** — Token for authorization
  - `licenseType` — string _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_

**`GetTokenForXbeesResponseContent`**

- `type` — string **(required)** _(default=result)_
- `result` — AuthResult **(required)**
  - `token` — string **(required)** — Token for authorization
  - `licenseType` — string _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_

**`LicenseType`**

- string _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_

</details>
