## SSL Service

_OpenAPI: SSL service — version —_

**Servers**

- `https://ssl.wildix.com` — Production
- `https://ssl-stage.wildix.com` — Stage

### Ssl

#### `GET` `/api/v2/certificate`

Get SSL Certificates for PBX

- operationId: `GetCertificates`
- **Response 200** (`GetCertificatesResponseContent`)
  - `type` — string **(required)**
  - `result` — CertificateResult **(required)**
    - `certificate` — Certificate
      - `privateKey` — string — SSL certificate private key
      - `fullchainPem` — string — Fullchain PEM
- Errors: `400`, `401`, `403`, `500`

#### `GET` `/api/v2/certificate/service`

Get SSL certificate for the auto.wildixin.com service domain

- operationId: `GetServicesCertificate`
- **Response 200** (`GetServicesCertificateResponseContent`)
  - `type` — string **(required)**
  - `result` — CertificateResult **(required)**
    - `certificate` — Certificate
      - `privateKey` — string — SSL certificate private key
      - `fullchainPem` — string — Fullchain PEM
- Errors: `400`, `401`, `403`, `500`

### Schemas appendix — SSL Service

<details><summary>8 component schemas</summary>

**`BadRequestErrorResponseContent`**

_Deprecated structure, only for PBXs_

- `type` — string — Error type
- `reason` — string — Error reason
- `code` — string — Error code

**`Certificate`**

- `privateKey` — string — SSL certificate private key
- `fullchainPem` — string — Fullchain PEM

**`CertificateResult`**

- `certificate` — Certificate
  - `privateKey` — string — SSL certificate private key
  - `fullchainPem` — string — Fullchain PEM

**`CustomInternalServerErrorResponseContent`**

_Deprecated structure, only for PBXs_

- `type` — string — Error type
- `reason` — string — Error reason
- `code` — string — Error code

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetCertificatesResponseContent`**

- `type` — string **(required)**
- `result` — CertificateResult **(required)**
  - `certificate` — Certificate
    - `privateKey` — string — SSL certificate private key
    - `fullchainPem` — string — Fullchain PEM

**`GetServicesCertificateResponseContent`**

- `type` — string **(required)**
- `result` — CertificateResult **(required)**
  - `certificate` — Certificate
    - `privateKey` — string — SSL certificate private key
    - `fullchainPem` — string — Fullchain PEM

**`UnauthorizedResponseContent`**

- `type` — string **(required)** _(default=error)_
- `reason` — string **(required)** _(default=Unauthorized)_
- `code` — string **(required)** _(default=Unauthorized)_

</details>
