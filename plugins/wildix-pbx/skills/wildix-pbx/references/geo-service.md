## GEO Service

_OpenAPI: Geo service — version —_

**Servers**

- `https://geo.wildix.com` — Production
- `https://geo-stage.wildix.com` — Stage

### Geo

#### `GET` `/api/v2/location/ip/{ip}`

Get the address by IP

- operationId: `GetAddressByIp`
- **Parameters**
  - `ip` (path) — string **(required)** — IP address
  - `full` (query) — string — Return the raw MaxMind city record instead of the short form
- **Response 200** (`GetAddressByIpResponseContent`)
  - `type` — string **(required)**
  - `result` — IpLocationResult **(required)**
    - `ip` — string — IP address
    - `continentName` — string — Continent name
    - `countryName` — string — Country name
    - `cityName` — string — City name
    - `location` — GeoLocation
      - `latitude` — number — Latitude _(format=float)_
      - `longitude` — number — Longitude _(format=float)_
      - `accuracyRadius` — number — Accuracy radius
      - `timeZone` — string — Time zone
    - `geoData` — any — Raw MaxMind city record, returned when `full` is set
- Errors: `400`, `401`, `500`

#### `GET` `/api/v2/location/latlng/address/`

Get address by location

- operationId: `GetAddressByLocation`
- **Parameters**
  - `lat` (query) — string **(required)** — Latitude (-90...90)
  - `lng` (query) — string **(required)** — Longitude (-180...180)
- **Response 200** (`GetAddressByLocationResponseContent`)
  - `type` — string **(required)**
  - `result` — any **(required)** — Google address components, keyed by component type
- Errors: `400`, `401`, `500`

#### `GET` `/api/v2/token/`

Echo the caller access token back

- operationId: `GetTokens`
- **Response 200** (`GetTokensResponseContent`)
  - `type` — string **(required)**
  - `result` — TokensResult **(required)**
    - `accessToken` — string — Caller access token
    - `refreshToken` — string — Refresh token, always empty
- Errors: `400`, `401`, `500`

### Schemas appendix — GEO Service

<details><summary>9 component schemas</summary>

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

**`GeoLocation`**

- `latitude` — number — Latitude _(format=float)_
- `longitude` — number — Longitude _(format=float)_
- `accuracyRadius` — number — Accuracy radius
- `timeZone` — string — Time zone

**`GetAddressByIpResponseContent`**

- `type` — string **(required)**
- `result` — IpLocationResult **(required)**
  - `ip` — string — IP address
  - `continentName` — string — Continent name
  - `countryName` — string — Country name
  - `cityName` — string — City name
  - `location` — GeoLocation
    - `latitude` — number — Latitude _(format=float)_
    - `longitude` — number — Longitude _(format=float)_
    - `accuracyRadius` — number — Accuracy radius
    - `timeZone` — string — Time zone
  - `geoData` — any — Raw MaxMind city record, returned when `full` is set

**`GetAddressByLocationResponseContent`**

- `type` — string **(required)**
- `result` — any **(required)** — Google address components, keyed by component type

**`GetTokensResponseContent`**

- `type` — string **(required)**
- `result` — TokensResult **(required)**
  - `accessToken` — string — Caller access token
  - `refreshToken` — string — Refresh token, always empty

**`IpLocationResult`**

- `ip` — string — IP address
- `continentName` — string — Continent name
- `countryName` — string — Country name
- `cityName` — string — City name
- `location` — GeoLocation
  - `latitude` — number — Latitude _(format=float)_
  - `longitude` — number — Longitude _(format=float)_
  - `accuracyRadius` — number — Accuracy radius
  - `timeZone` — string — Time zone
- `geoData` — any — Raw MaxMind city record, returned when `full` is set

**`TokensResult`**

- `accessToken` — string — Caller access token
- `refreshToken` — string — Refresh token, always empty

**`UnauthorizedResponseContent`**

- `type` — string **(required)** _(default=error)_
- `reason` — string **(required)** _(default=Unauthorized)_
- `code` — string **(required)** _(default=Unauthorized)_

</details>
