## Classound API

_OpenAPI: Classound Service — version —_

**Servers**

- `https://classound-p2p.wildix.com` — Production
- `https://classound-p2p-stable.wildix.com` — Stable
- `https://classound-p2p-stage.wildix.com` — Stage

### Other

#### `POST` `/v1/a2s/sms`

- operationId: `SendSmsFromApplication`
- **Request body** (`application/json` — `SendSmsFromApplicationRequestContent`) **(required)**
  - `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
  - `to` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
  - `message` — string **(required)**
- **Response 200** (`SendSmsFromApplicationResponseContent`)
  - `type` — string _(default=RESULT)_
  - `success` — boolean
  - `status` — string _(default=RECEIVED)_
  - `id` — array
    - _array of_ `string`
  - `company` — string
  - `data` — SendSmsData
    - `from` — string _(pattern=^\+[0-9]{10,14}$)_
    - `to` — string _(pattern=^\+[0-9]{10,14}$)_
    - `message` — string
    - `pbx` — string
    - `extension` — string
- Errors: `400`, `403`, `404`, `408`, `503`

#### `POST` `/v1/a2s/whatsapp/template`

- operationId: `SendWhatsAppTemplateBroadcast`
- **Request body** (`application/json` — `SendWhatsAppTemplateBroadcastRequestContent`) **(required)**
  - `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
  - `campaignName` — string — Optional human-readable campaign label; the server generates the batchId
  - `template` — BroadcastTemplate **(required)**
    - `name` — string **(required)**
  - `recipients` — array **(required)** — Per-recipient targets; each may carry its own template body parameters. Max 5000 per call; the server may enforce a lower per-environment cap. _(minItems=1; maxItems=5000)_
    - _array of_ `BroadcastRecipient`
      - `to` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
      - `params` — BroadcastParams
        - _map of_ `string`
- **Response 202** (`SendWhatsAppTemplateBroadcastResponseContent`)
  - `type` — string **(required)** _(default=BROADCAST.ACCEPTED)_
  - `success` — boolean **(required)**
  - `batchId` — string **(required)**
  - `accepted` — number **(required)** — Number of recipients accepted and enqueued; per-recipient delivery status arrives asynchronously via DLR
  - `rejected` — array — Recipients rejected by validation (e.g. params not matching the template). The rest of the batch is still accepted; rejected recipients are also reported on the status webhook.
    - _array of_ `BroadcastRejection`
      - `to` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
      - `reason` — string **(required)** — Why this recipient was rejected (e.g. params do not match the template).
- Errors: `400`, `403`, `404`, `408`, `500`, `502`, `503`

#### `GET` `/v1/a2s/whatsapp/templates`

- operationId: `ListWhatsAppTemplatesA2S`
- **Parameters**
  - `did` (query) — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- **Response 200** (`ListWhatsAppTemplatesA2SResponseContent`)
  - `type` — string **(required)** _(default=WHATSAPP.TEMPLATES)_
  - `success` — boolean **(required)**
  - `did` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
  - `data` — array **(required)**
    - _array of_ `Template`
      - `name` — string **(required)**
      - `parameterFormat` — string **(required)** _(enum: `NAMED`)_
      - `components` — array **(required)**
        - _array of_ `Component`
          - `type` — string **(required)** _(enum: `HEADER`, `BODY`, `FOOTER`, `BUTTONS`)_
          - `format` — string **(required)** _(enum: `TEXT`, `IMAGE`, `DOCUMENT`, `VIDEO`)_
          - `text` — string
          - `example` — ComponentExample
            - `headerHandle` — array
              - _array of_ `string`
            - `bodyTextNamedParams` — array
              - _(nesting depth limit — see `BodyTextNamedParam` in the Schemas appendix)_
          - `buttons` — array
            - _array of_ `Button`
              - _(nesting depth limit — see `Button` in the Schemas appendix)_
      - `language` — string **(required)**
      - `status` — string **(required)** _(enum: `APPROVED`, `PAUSED`, `REJECTED`)_
      - `category` — string **(required)** _(enum: `MARKETING`, `UTILITY`, `AUTHENTICATION`)_
      - `subCategory` — string
      - `id` — string **(required)**
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `GET` `/v1/esim/bundles`

- operationId: `ListEsimBundles`
- **Parameters**
  - `companyId` (query) — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
- **Response 200** (`ListEsimBundlesResponseContent`)
  - `bundles` — array **(required)** — SIM count breakdown per bundle/plan
    - _array of_ `EsimBundleCount`
      - `bundle` — string **(required)** — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
      - `available` — number **(required)** — SIMs available for provisioning in this bundle
      - `active` — number **(required)** — SIMs actively provisioned in this bundle
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `DELETE` `/v1/esim/endpoint`

- operationId: `DeleteEsimEndpoint`
- **Parameters**
  - `companyId` (query) — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
  - `serial` (query) — string **(required)** — PBX serial number to delete _(minLen=1)_
- **Response 200** (`DeleteEsimEndpointResponseContent`)
  - `status` — string **(required)** — Deletion status
  - `companyId` — string **(required)** — Wildix company ID
  - `serial` — string **(required)** — PBX serial number that was deleted
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `POST` `/v1/esim/order`

Reserve eSIMs for a company. Provisioning runs in a background worker (WMS-26963): a fresh order returns 202 with status PROCESSING - poll GetEsimOrderStatus until COMPLETED / FAILED / STALE. 200 with status SUCCESS is returned only on an idempotent replay of an order still live.

- operationId: `CreateEsimOrder`
- **Request body** (`application/json` — `CreateEsimOrderRequestContent`) **(required)**
  - `partnerId` — string **(required)** — Wildix partner ID _(minLen=1)_
  - `partnerName` — string **(required)** — Partner display name (used for reseller creation) _(minLen=1)_
  - `companyId` — string **(required)** — Wildix company ID _(minLen=1)_
  - `partnerSapId` — string **(required)** — Dealer SAP_ID (the Salesforce Case 'SAP ID'). The reseller is resolved and reused by this stable id instead of a name-derived alias. Always present on the Case; a self/direct partner sends partnerSapId equal to companyId. _(minLen=1)_
  - `companyName` — string **(required)** — Company display name (used for group creation) _(minLen=1)_
  - `countryCode` — string **(required)** — ISO 3166-1 alpha-2 country code (e.g. IT, DE, US) _(pattern=^[A-Z]{2}$; minLen=2; maxLen=2)_
  - `quantity` — number **(required)** — Number of eSIMs to reserve _(min=1; max=1000)_
  - `requestId` — string **(required)** — Unique request ID from Salesforce for idempotency tracking _(minLen=1; maxLen=100)_
  - `partnerEmail` — string — Partner contact email (optional, used for reseller creation)
  - `bundle` — string **(required)** — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
  - `homeLocations` — array **(required)** — List of ISO 3166-1 alpha-2 country codes for the Reseller/Group Home Location. At least one country required. Allows the reseller to serve subscribers across multiple countries. _(minItems=1)_
    - _array of_ `string`
  - `partnerAddress` — string **(required)** — Partner billing address line 1 _(minLen=1)_
  - `partnerPostCode` — string **(required)** — Partner billing postal/zip code _(minLen=1)_
  - `partnerContactNumber` — string **(required)** — Partner contact phone number (E.164 digits only, no +) _(pattern=^[0-9]+$)_
  - `partnerAddress2` — string — Partner billing address line 2 (optional)
  - `partnerTown` — string — Partner billing town/city (optional)
  - `partnerCounty` — string — Partner billing county/state (optional)
  - `partnerDescription` — string — Reseller description (optional) _(minLen=3; maxLen=100)_
- **Response 200** (`CreateEsimOrderResponseContent`)
  - `status` — string **(required)** _(enum: `SUCCESS`, `PROCESSING`, `COMPLETED`, `FAILED`, `STALE`)_
  - `orderId` — string **(required)** — Internal order tracking ID (UUID)
  - `requestId` — string **(required)**
  - `partnerId` — string **(required)**
  - `companyId` — string **(required)**
  - `countryCode` — string **(required)**
  - `quantity` — number **(required)** — Number of eSIMs allocated in this order (equals requested quantity)
  - `totalReserved` — number **(required)** — Total SIMs currently in ALLOCATED state for this company across all orders
  - `bundle` — string — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `POST` `/v1/esim/order/cleanup`

- operationId: `CleanupEsimOrder`
- **Request body** (`application/json` — `CleanupEsimOrderRequestContent`) **(required)**
  - `orderId` — string **(required)** — Order ID returned from POST /esim/order (base64-encoded key) _(minLen=1)_
- **Response 200** (`CleanupEsimOrderResponseContent`)
  - `status` — string **(required)** _(enum: `CLEANED`)_
  - `orderId` — string **(required)** — Order ID that was cleaned up
  - `simsReleased` — number **(required)**
  - `steps` — CleanupStepsMap **(required)** — Map of cleanup step names to their result status (e.g. 'move_to_bookin' -> 'success')
    - _map of_ `string`
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `GET` `/v1/esim/order/status`

Poll the status of an async eSIM order (WMS-26963). CreateEsimOrder provisions in a background worker and returns 202 with status PROCESSING; poll here until a terminal status (COMPLETED / FAILED) or STALE (in-progress order that outlived the worker). Keyed by the same (companyId, requestId, bundle) the order was created with.

- operationId: `GetEsimOrderStatus`
- **Parameters**
  - `requestId` (query) — string **(required)** — Salesforce request ID the order was created with _(minLen=1; maxLen=100)_
  - `companyId` (query) — string — Wildix company ID (order key component)
  - `bundle` (query) — string — Bundle SKU the order was placed for (order key component; may be empty)
- **Response 200** (`GetEsimOrderStatusResponseContent`)
  - `orderId` — string **(required)** — Internal order tracking ID
  - `status` — string **(required)** _(enum: `SUCCESS`, `PROCESSING`, `COMPLETED`, `FAILED`, `STALE`)_
  - `ageSeconds` — number **(required)** — Seconds since the order was last updated
  - `response` — EsimOrderResult — The order result payload carried by GetEsimOrderStatus on COMPLETED. Mirrors the CreateEsimOrder success body (which cannot be reused directly: an @output structure may not be embedded as a member).
    - `status` — string **(required)** _(enum: `SUCCESS`, `PROCESSING`, `COMPLETED`, `FAILED`, `STALE`)_
    - `orderId` — string **(required)** — Internal order tracking ID (UUID)
    - `requestId` — string **(required)**
    - `partnerId` — string **(required)**
    - `companyId` — string **(required)**
    - `countryCode` — string **(required)**
    - `quantity` — number **(required)** — Number of eSIMs allocated in this order
    - `totalReserved` — number **(required)** — Total SIMs currently in ALLOCATED state for this company across all orders
    - `bundle` — string — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
  - `error` — string — Failure message; present only when status is FAILED.
  - `errorCode` — string — Failure code; present only when status is FAILED.
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `GET` `/v1/esim/partner`

- operationId: `GetEsimPartner`
- **Parameters**
  - `partnerId` (query) — string **(required)** — Wildix SAP partner identifier (e.g. W123644). Case preserved verbatim.
- **Response 200** (`GetEsimPartnerResponseContent`)
  - `partnerId` — string **(required)** — Echo of the requested partnerId.
  - `partnerName` — string **(required)** — Canonical partner display name as stored in the eSIM platform.
  - `partnerAddress` — string — Billing address line 1.
  - `partnerPostCode` — string — Billing postal/ZIP code.
  - `partnerContactNumber` — string — E.164 contact number (digits only as stored in the eSIM platform).
  - `partnerAddress2` — string — Billing address line 2 (optional).
  - `partnerTown` — string — Billing town/city (optional).
  - `partnerCounty` — string — Billing county/state (optional).
  - `country` — string — ISO 3166-1 alpha-3 country code. Note: the eSIM platform returns alpha-3 on read; CreateEsimOrderInput.countryCode is alpha-2.
  - `homeLocations` — array — List of ISO 3166-1 alpha-3 country codes the reseller is provisioned for.
    - _array of_ `string`
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `POST` `/v1/esim/partner/create`

- operationId: `CreateEsimPartner`
- **Request body** (`application/json` — `CreateEsimPartnerRequestContent`) **(required)**
  - `partnerId` — string **(required)** _(minLen=1)_
  - `partnerName` — string **(required)** _(minLen=1)_
  - `companyId` — string **(required)** _(minLen=1)_
  - `partnerSapId` — string **(required)** _(pattern=^.*\S.*$; minLen=1)_
  - `companyName` — string **(required)** _(minLen=1)_
  - `countryCode` — string **(required)** _(pattern=^[A-Za-z]{2}$; minLen=2; maxLen=2)_
  - `quantity` — number **(required)** _(min=1; max=1000)_
  - `requestId` — string **(required)** _(minLen=1; maxLen=100)_
  - `partnerEmail` — string
  - `bundle` — string **(required)** — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
  - `homeLocations` — array **(required)** _(minItems=1)_
    - _array of_ `string`
  - `partnerAddress` — string **(required)** _(minLen=3; maxLen=50)_
  - `partnerPostCode` — string **(required)** _(minLen=1)_
  - `partnerContactNumber` — string **(required)** _(pattern=^[0-9]+$; minLen=7)_
  - `partnerAddress2` — string
  - `partnerTown` — string
  - `partnerCounty` — string
  - `partnerDescription` — string _(minLen=3; maxLen=100)_
- **Response 200** (`CreateEsimPartnerResponseContent`)
  - `status` — string **(required)** _(enum: `READY`, `PROVISIONING`)_
  - `ready` — boolean **(required)** — True after the customer group exists under the reseller and the eSIM order can be submitted.
  - `orderCreated` — boolean **(required)** — Always false. Partner creation never creates an eSIM order or reserves a SIM.
  - `errorCode` — string — Neutral machine-readable state returned while reseller billing setup is still in progress.
  - `message` — string — Neutral operator-facing message. Upstream vendor details are never returned.
- Errors: `400`, `403`, `404`, `408`, `500`, `502`, `503`

#### `POST` `/v1/esim/release`

- operationId: `ReleaseEsimSims`
- **Request body** (`application/json` — `ReleaseEsimSimsRequestContent`) **(required)**
  - `companyId` — string **(required)** — Wildix company identifier (e.g. IT_W123644).
  - `bundle` — string **(required)** — Bundle SKU (e.g. PLAN-VC-MSG-2G) whose unprovisioned SIMs to release.
  - `count` — number **(required)** — Number of unprovisioned SIMs to release. Server picks the oldest by allocation date.
- **Response 200** (`ReleaseEsimSimsResponseContent`)
  - `released` — array **(required)** — ICCIDs successfully released back to the free pool.
    - _array of_ `string`
  - `failed` — array **(required)** — ICCIDs that could not be released, with per-ICCID failure reason.
    - _array of_ `ReleaseFailureItem`
      - `iccid` — string **(required)**
      - `reason` — string **(required)**
  - `releasedCount` — number **(required)** — Count of successfully released ICCIDs (echo of released.length for convenience).
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `GET` `/v1/esim/status`

- operationId: `GetEsimStatus`
- **Parameters**
  - `companyId` (query) — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
  - `uid` (query) — string **(required)** — Stable primary identifier of the subscriber _(pattern=^[0-9]{7}$)_
- **Response 200** (`GetEsimStatusResponseContent`)
  - `companyId` — string **(required)** — Wildix company ID
  - `uid` — string **(required)** — Stable primary identifier of the subscriber _(pattern=^[0-9]{7}$)_
  - `extension` — string — User extension on PBX (current value)
  - `phone` — string — Mobile number (E.164 digits only)
  - `iccid` — string — ICCID of the eSIM
  - `esimStatus` — string **(required)** — eSIM status (e.g. INSTALLED, AVAILABLE, RELEASED, ERROR)
  - `subUID` — string — eSIM subscriber UID
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `POST` `/v1/esim/subscriber/provision`

- operationId: `ProvisionEsimSubscriber`
- **Request body** (`application/json` — `ProvisionEsimSubscriberRequestContent`) **(required)**
  - `companyId` — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
  - `uid` — string **(required)** — Stable primary identifier for the subscriber. _(pattern=^[0-9]{7}$)_
  - `serial` — string **(required)** — PBX serial number (maps to KC-PBX / endpointName) _(minLen=1)_
  - `host` — string **(required)** — PBX domain (IP or FQDN, e.g. 'mycompany.wildixin.com') _(minLen=1)_
  - `extension` — string **(required)** — User extension / SIP address on PBX _(minLen=1; maxLen=45)_
  - `phone` — string **(required)** — Mobile number with country code, digits only (MDN-E164) _(minLen=5; maxLen=20)_
  - `email` — string **(required)** — User email address (eSIM QR code is sent to this address) _(minLen=3)_
  - `firstName` — string — User first name
  - `lastName` — string — User last name
  - `userPassword` — string **(required)** — PBX SIP password for the extension (used to register the eSIM to the PBX) _(minLen=1)_
  - `bundle` — string — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
- **Response 200** (`ProvisionEsimSubscriberResponseContent`)
  - `status` — string **(required)** _(enum: `PROVISIONED`, `ALREADY_PROVISIONED`)_
  - `companyId` — string **(required)** — Wildix company ID
  - `uid` — string **(required)** — Unique identifier of the user in the WMS Network (7-digit numeric, 1,000,000–9,999,999) _(pattern=^[0-9]{7}$)_
  - `extension` — string **(required)** — User extension
  - `phone` — string **(required)** — Mobile number (MDN-E164)
  - `subUID` — string **(required)** — eSIM subscriber UID (needed for future updates/deletes)
  - `iccid` — string **(required)** — ICCID of the provisioned eSIM
  - `activationCode` — string — LPA activation code string for eSIM installation
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `GET` `/v1/esim/subscriber/qrcode`

- operationId: `GetEsimQrCode`
- **Parameters**
  - `companyId` (query) — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
  - `uid` (query) — string **(required)** — Stable primary identifier of the subscriber to get the QR code for _(pattern=^[0-9]{7}$)_
- **Response 200** (`GetEsimQrCodeResponseContent`)
  - `companyId` — string **(required)** — Wildix company ID
  - `uid` — string **(required)** — Stable primary identifier of the subscriber _(pattern=^[0-9]{7}$)_
  - `extension` — string — User extension on PBX (current value)
  - `iccid` — string **(required)** — ICCID of the eSIM
  - `activationCode` — string **(required)** — LPA activation code string for eSIM installation (e.g. LPA1:$smdp.example.com$code)
  - `phone` — string — Mobile number (E.164 digits only)
- Errors: `400`, `403`, `404`, `408`, `409`, `500`, `503`

#### `POST` `/v1/esim/subscriber/qrcode/refresh`

- operationId: `RefreshEsimQrCode`
- **Request body** (`application/json` — `RefreshEsimQrCodeRequestContent`) **(required)**
  - `companyId` — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
  - `extension` — string **(required)** — User extension / SIP address on PBX _(minLen=1; maxLen=45)_
- **Response 200** (`RefreshEsimQrCodeResponseContent`)
  - `companyId` — string **(required)** — Wildix company ID
  - `extension` — string **(required)** — User extension on PBX
  - `iccid` — string **(required)** — ICCID of the eSIM
  - `activationCode` — string **(required)** — Regenerated LPA activation code string for eSIM installation
  - `phone` — string — Mobile number (E.164 digits only)
- Errors: `400`, `403`, `404`, `408`, `409`, `500`, `503`

#### `POST` `/v1/esim/subscriber/terminate`

- operationId: `TerminateEsimSubscriber`
- **Request body** (`application/json` — `TerminateEsimSubscriberRequestContent`) **(required)**
  - `companyId` — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
  - `uid` — string **(required)** — Stable primary identifier of the subscriber to terminate _(pattern=^[0-9]{7}$)_
- **Response 200** (`TerminateEsimSubscriberResponseContent`)
  - `status` — string **(required)** _(enum: `TERMINATED`)_
  - `companyId` — string **(required)** — Wildix company ID
  - `uid` — string **(required)** — Stable primary identifier of the terminated subscriber _(pattern=^[0-9]{7}$)_
  - `extension` — string — User extension at time of termination (from DynamoDB)
  - `subUID` — string — eSIM subscriber UID
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `PATCH` `/v1/esim/subscriber/{extension}`

- operationId: `UpdateEsimSubscriber`
- **Parameters**
  - `extension` (path) — string **(required)** — New extension / SIP address. Updates the SIP-ADDRESS and the DynamoDB extension attribute. _(minLen=1; maxLen=45)_
- **Request body** (`application/json` — `UpdateEsimSubscriberRequestContent`)
  - `companyId` — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
  - `email` — string — New email address
  - `firstName` — string — New first name
  - `lastName` — string — New last name
  - `phone` — string — New mobile number with country code, digits only (MDN-E164)
  - `userPassword` — string — New PBX SIP password
  - `bundle` — string — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
  - `newExtension` — string — New extension / SIP address. Changes the subscriber's SIP-ADDRESS and migrates the record. _(minLen=1; maxLen=45)_
- **Response 200** (`UpdateEsimSubscriberResponseContent`)
  - `status` — string **(required)** _(enum: `UPDATED`)_
  - `companyId` — string **(required)** — Wildix company ID
  - `uid` — string **(required)** — Stable primary identifier of the updated subscriber _(pattern=^[0-9]{7}$)_
  - `updatedFields` — array **(required)** — List of fields that were updated
    - _array of_ `string`
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `GET` `/v1/esim/subscribers`

- operationId: `ListEsimSubscribers`
- **Parameters**
  - `companyId` (query) — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
  - `limit` (query) — number — Maximum number of subscribers to return. If omitted, returns all. _(min=1; max=200)_
  - `offset` (query) — number — Number of subscribers to skip (default 0) _(min=0)_
- **Response 200** (`ListEsimSubscribersResponseContent`)
  - `companyId` — string **(required)** — Wildix company ID
  - `subscribers` — array **(required)** — List of provisioned subscribers
    - _array of_ `SubscriberItem`
      - `extension` — string **(required)** — User extension / SIP address on PBX
      - `phone` — string — Mobile number (E.164 digits only)
      - `email` — string — User email address
      - `iccid` — string — ICCID of the eSIM
      - `subUID` — string — eSIM subscriber UID
      - `serial` — string — PBX serial number
      - `bundle` — string — Bundle/plan SKU
      - `firstName` — string — User first name
      - `lastName` — string — User last name
      - `status` — string — eSIM status (e.g. PROVISIONED, ACTIVE)
  - `total` — number **(required)** — Total number of subscribers for this company
  - `limit` — number **(required)** — Maximum number of subscribers returned
  - `offset` — number **(required)** — Number of subscribers skipped
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `POST` `/v1/esim/transforms/sync`

- operationId: `SyncEsimTransforms`
- **Request body** (`application/json` — `SyncEsimTransformsRequestContent`) **(required)**
  - `companyId` — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
  - `transforms` — array **(required)** — List of desired extension-to-E.164 mappings (full snapshot)
    - _array of_ `TransformEntry`
      - `extension` — string **(required)** — PBX extension / short code _(minLen=1; maxLen=45)_
      - `e164` — string **(required)** — E.164 number (digits only, no +) _(minLen=5; maxLen=20)_
- **Response 200** (`SyncEsimTransformsResponseContent`)
  - `companyId` — string **(required)** — Wildix company ID
  - `added` — number **(required)** — Number of transforms added
  - `updated` — number **(required)** — Number of transforms updated
  - `deleted` — number **(required)** — Number of transforms deleted
  - `errors` — array — List of per-transform errors (if any)
    - _array of_ `TransformError`
      - `action` — string — Action attempted: add, update, or delete
      - `extension` — string — Extension that failed
      - `error` — string — Error message from the eSIM provider
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `POST` `/v1/numbers/ordering/order`

- operationId: `CreateNumbersOrder`
- **Request body** (`application/json` — `CreateNumbersOrderRequestContent`) **(required)**
  - `companyId` — string **(required)**
  - `requestId` — string **(required)**
  - `customerOrderId` — string **(required)**
  - `webhookUrl` — string **(required)**
  - `webhookToken` — string **(required)**
  - `data` — OrderSearchCriteria **(required)** — Search criteria for phone number ordering. At least one of city, state, zip, or areaCode must be provided.
    - `country` — string **(required)** _(default=US)_
    - `state` — string
    - `quantity` — number **(required)** _(min=1; max=1000)_
    - `city` — string
    - `zip` — string _(pattern=^[A-Za-z0-9\-]{1,10}$)_
    - `areaCode` — string — Requested area code (NANP NPA, 3 digits, first digit 2-9) for number selection. A leading '+' or country/trunk code '1' is accepted and stripped server-side. _(pattern=^\+?1?[2-9][0-9]{2}$)_
- **Response 200** (`CreateNumbersOrderResponseContent`)
  - `status` — string **(required)**
  - `supplierOrderId` — string
  - `requestId` — string
  - `customerOrderId` — string
  - `orderStatus` — string
  - `message` — string
  - `testMode` — boolean
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `GET` `/v1/s2s/messenger/pages`

Returns the Facebook pages a company can send Messenger messages from.

- operationId: `ListMessengerPages`
- **Parameters**
  - `companyId` (query) — string **(required)** _(minLen=1)_
- **Response 200** (`ListMessengerPagesResponseContent`)
  - `type` — string **(required)** _(default=RESULT)_
  - `success` — boolean **(required)**
  - `timestamp` — number **(required)**
  - `result` — MessengerPagesResult **(required)**
    - `companyId` — string **(required)**
    - `pages` — array _(default=[])_
      - _array of_ `MessengerPage`
        - `id` — string **(required)**
        - `name` — string **(required)**
        - `url` — string **(required)**
        - `channel` — string **(required)**
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `POST` `/v1/s2s/messenger/send`

Sends a Facebook Messenger message from one of the company's pages to a person who wrote to it. Only a reply is possible: free-form for 24 hours from the person's last message, then HUMAN_AGENT tagged for 7 days, and the tag is applied for the caller.

- operationId: `SendMessengerMessage`
- **Request body** (`application/json` — `SendMessengerMessageRequestContent`) **(required)**
  - `companyId` — string **(required)** _(minLen=1)_
  - `from` — string **(required)** — The page to send from, a Facebook Page ID. It must be bound to this company. A String and not a PhoneNumber, which this member name carries on the other send routes: a Page ID is an opaque Meta identifier and is never normalised the way a number is. _(minLen=1)_
  - `to` — string **(required)** — The recipient, a Page Scoped ID, meaningful only together with that page. A String and not a PhoneNumber, which this member name carries on the other send routes: a PSID is an opaque Meta identifier and is never normalised the way a number is. _(minLen=1)_
  - `message` — string — The text of the message. A request must carry a message, media, or both. _(maxLen=2000)_
  - `extension` — string — The extension of the operator sending the message. Recorded on the message detail record, so that a message can be reported per user; nothing is sent with it.
  - `userId` — string — The x-bees user sending the message. Recorded on the message detail record as channel metadata; nothing is sent with it, and it takes no part in resolving an attachment. _(minLen=12; maxLen=12)_
  - `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` — string _(minLen=32; maxLen=32)_
  - `media` — array — Storage file ids to attach, at most ten. Each becomes a message of its own. Requires channelId and messageId, which are what resolve the files in conversation storage; without them the request is rejected. _(maxItems=10)_
    - _array of_ `string`
  - `suggestions` — array — Buttons shown under the message. A quick reply by default, or whatever action the entry names, including the Marketing Messages opt-in request.
    - _array of_ `MessengerSuggestion`
      - `action` — string — What CM.com does when the button is pressed: Reply, Dial, Login, Logout, ViewProduct (in beta) or optin, which is the Marketing Messages opt-in request and is the one action spelled in lower case. Matched without regard to case, and an action outside this list is rejected. Omit it for a quick reply, which is what every button was before this member existed. _(minLen=1)_
      - `label` — string — What the person sees on the button. At most 20 characters, except on an optin, where it is the request being answered and may run to 65. Required for Reply, Dial and optin; a Login and a Logout show no text. _(minLen=1; maxLen=65)_
      - `postbackdata` — string — Returned on the next inbound message when the button is pressed, as postbackData. Required for a Reply, which is the only action that comes back to us as an inbound. _(minLen=1)_
      - `optin` — any — The opt-in request. Required when the action is optin, and meaningless otherwise.
  - `tag` — string — A Meta message tag. Omit it and HUMAN_AGENT is applied when the conversation needs one.
- **Response 200** (`SendMessengerMessageResponseContent`)
  - `type` — string **(required)** _(default=RESULT)_
  - `success` — boolean **(required)**
  - `timestamp` — number **(required)**
  - `result` — MessengerSendResult **(required)** — What the send produced.
    - `from` — string **(required)** — The page the message was sent from, a Facebook Page ID, echoed from the request. A String and not a PhoneNumber, which this member name carries on the other send routes: a Page ID is an opaque Meta identifier and is never normalised the way a number is.
    - `to` — string **(required)** — The recipient, a Page Scoped ID, echoed from the request and meaningful only together with that page. A String and not a PhoneNumber, which this member name carries on the other send routes: a PSID is an opaque Meta identifier and is never normalised the way a number is.
    - `messageId` — string **(required)** — The correlation key of the first message, the one a delivery status carries.
    - `messageIds` — array **(required)** — Every message the request produced, in the order they were sent.
      - _array of_ `string`
    - `windowState` — string **(required)** — The conversation state the message was sent under, OPEN or HUMAN_AGENT.
    - `tag` — string — The tag actually applied, whether it was given or supplied for the caller.
    - `simulated` — boolean — True when the request was recorded but nothing was sent to the supplier.
- Errors: `400`, `403`, `404`, `408`, `409`, `500`, `502`, `503`

#### `GET` `/v1/s2s/rcs/brands` 🆕

Returns the RCS brands a company can send from.

- operationId: `ListRcsBrands`
- **Parameters**
  - `companyId` (query) — string **(required)** _(minLen=1)_
- **Response 200** (`ListRcsBrandsResponseContent`)
  - `type` — string **(required)** _(default=RESULT)_
  - `success` — boolean **(required)**
  - `timestamp` — number **(required)**
  - `result` — RcsBrandsResult **(required)**
    - `companyId` — string **(required)**
    - `brands` — array _(default=[])_
      - _array of_ `RcsBrand`
        - `id` — string **(required)**
        - `name` — string **(required)** — The brand's display name, as the people it writes to see it. Entered when the brand is bound; equal to id for a brand bound without one.
        - `channel` — string **(required)**
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `POST` `/v1/s2s/rcs/send` 🆕

Sends an RCS message from one of the company's brands to a phone number. There is no reply window: the person does not have to have written first.

- operationId: `SendRcsMessage`
- **Request body** (`application/json` — `SendRcsMessageRequestContent`) **(required)**
  - `companyId` — string **(required)** _(minLen=1)_
  - `from` — string **(required)** — The brand to send from, an id ListRcsBrands returns. It must be bound to this company. A String and not a PhoneNumber: a brand id is a name and is never normalised the way a number is. _(minLen=1)_
  - `to` — string **(required)** — The recipient's phone number in E.164. _(pattern=^\+[0-9]{10,14}$)_
  - `message` — string — The text of the message. A request must carry a message, media, or both. _(maxLen=2048)_
  - `extension` — string — The extension of the operator sending the message. Recorded on the message detail record, so that a message can be reported per user; nothing is sent with it.
  - `userId` — string — The x-bees user sending the message. Recorded on the message detail record as channel metadata; nothing is sent with it, and it takes no part in resolving an attachment. _(minLen=12; maxLen=12)_
  - `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` — string _(minLen=32; maxLen=32)_
  - `media` — array — Storage file ids to attach, at most ten. Each becomes a message of its own. Requires channelId and messageId, which are what resolve the files in conversation storage; without them the request is rejected. _(maxItems=10)_
    - _array of_ `string`
  - `suggestions` — array — Suggested replies shown under the message, at most eleven. _(maxItems=11)_
    - _array of_ `RcsSuggestion`
      - `label` — string **(required)** — What the person sees on the button. _(minLen=1; maxLen=25)_
      - `postbackdata` — string **(required)** — Returned on the next inbound message when the button is pressed, as postback. _(minLen=1)_
- **Response 200** (`SendRcsMessageResponseContent`)
  - `type` — string **(required)** _(default=RESULT)_
  - `success` — boolean **(required)**
  - `timestamp` — number **(required)**
  - `result` — RcsSendResult **(required)** — What the send produced.
    - `from` — string **(required)** — The brand the message was sent from, echoed from the request.
    - `to` — string **(required)** — The recipient, echoed from the request. _(pattern=^\+[0-9]{10,14}$)_
    - `messageId` — string **(required)** — The correlation key of the first message, the one a delivery status carries.
    - `messageIds` — array **(required)** — Every message the request produced, in the order they were sent.
      - _array of_ `string`
    - `simulated` — boolean — True when the request was recorded but nothing was sent to the supplier.
- Errors: `400`, `403`, `404`, `408`, `500`, `502`, `503`

#### `POST` `/v1/s2s/sms`

- operationId: `SendSms`
- **Request body** (`application/json` — `SendSmsRequestContent`) **(required)**
  - `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
  - `to` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
  - `pbx` — string **(required)**
  - `company` — string **(required)**
  - `message` — string **(required)**
  - `extension` — string **(required)**
  - `media` — array
    - _array of_ `string`
  - `userId` — string _(minLen=12; maxLen=12)_
  - `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` — string _(minLen=32; maxLen=32)_
- **Response 200** (`SendSmsResponseContent`)
  - `type` — string
  - `success` — boolean
  - `status` — string
  - `id` — array
    - _array of_ `string`
  - `company` — string
  - `data` — SendSmsOutputData
    - `from` — string _(pattern=^\+[0-9]{10,14}$)_
    - `to` — string _(pattern=^\+[0-9]{10,14}$)_
    - `message` — string
    - `pbx` — string
    - `extension` — string
- Errors: `400`, `403`, `404`, `408`, `503`

#### `GET` `/v1/s2s/sms/history`

- operationId: `GetSmsHistory`
- **Parameters**
  - `from` (query) — string _(pattern=^\+[0-9]{10,14}$)_
  - `to` (query) — string _(pattern=^\+[0-9]{10,14}$)_
  - `companyId` (query) — string
- **Response 200** (`GetSmsHistoryResponseContent`)
  - `type` — string
  - `result` — array
    - _array of_ `GetSmsHistoryRecord`
      - `from` — string
      - `to` — string
      - `messageId` — string
      - `messageText` — string
      - `time` — number
- Errors: `400`, `403`, `404`, `408`, `503`

#### `GET` `/v1/s2s/sms/numbers`

- operationId: `ListSmsNumbers`
- **Parameters**
  - `companyId` (query) — string **(required)**
- **Response 200** (`ListSmsNumbersResponseContent`)
  - `type` — string **(required)** _(default=RESULT)_
  - `success` — boolean **(required)**
  - `timestamp` — number **(required)**
  - `result` — SmsNumbersResult **(required)**
    - `companyId` — string **(required)**
    - `numbers` — array _(default=[])_
      - _array of_ `string`
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `POST` `/v1/s2s/whatsapp`

- operationId: `SendWhatsAppMessage`
- **Request body** (`application/json` — `SendWhatsAppMessageRequestContent`) **(required)**
  - `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
  - `to` — string **(required)** — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
  - `pbx` — string **(required)**
  - `company` — string **(required)**
  - `message` — string **(required)**
  - `extension` — string **(required)**
  - `media` — array
    - _array of_ `string`
  - `userId` — string _(minLen=12; maxLen=12)_
  - `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` — string _(minLen=32; maxLen=32)_
- **Response 200** (`SendWhatsAppMessageResponseContent`)
  - `type` — string _(default=RESULT)_
  - `success` — boolean
  - `company` — string
  - `status` — string _(default=RECEIVED)_
  - `id` — array
    - _array of_ `string`
  - `data` — SendWhatsAppMessageData
    - `from` — string _(pattern=^\+[0-9]{10,14}$)_
    - `to` — string — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
    - `pbx` — string
    - `company` — string
    - `message` — string
    - `extension` — string
    - `media` — array
      - _array of_ `string`
    - `userId` — string _(minLen=12; maxLen=12)_
    - `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `messageId` — string _(minLen=32; maxLen=32)_
- Errors: `400`, `403`, `404`, `408`, `503`

#### `GET` `/v1/s2s/whatsapp/history`

- operationId: `GetWhatsAppHistory`
- **Parameters**
  - `from` (query) — string — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
  - `to` (query) — string — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
  - `companyId` (query) — string
- **Response 200** (`GetWhatsAppHistoryResponseContent`)
  - `type` — string
  - `result` — array
    - _array of_ `GetWhatsAppHistoryRecord`
      - `from` — string
      - `to` — string
      - `messageId` — string
      - `messageText` — string
      - `time` — number
- Errors: `400`, `403`, `404`, `408`, `503`

#### `POST` `/v1/s2s/whatsapp/interactive`

- operationId: `SendWhatsAppInteractiveMessage`
- **Request body** (`application/json` — `SendWhatsAppInteractiveMessageRequestContent`) **(required)**
  - `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
  - `to` — string **(required)** — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
  - `pbx` — string **(required)**
  - `company` — string **(required)**
  - `message` — InteractiveMessage **(required)**
    - `type` — string **(required)** _(enum: `list`, `button`)_
    - `header` — InteractiveHeader
      - `type` — string **(required)** _(enum: `text`, `image`, `document`, `video`)_
      - `text` — string
      - `image` — InteractiveMedia
        - `id` — string **(required)**
        - `link` — string **(required)**
        - `filename` — string
      - `video` — InteractiveMedia
        - `id` — string **(required)**
        - `link` — string **(required)**
        - `filename` — string
      - `document` — InteractiveMedia
        - `id` — string **(required)**
        - `link` — string **(required)**
        - `filename` — string
    - `body` — InteractiveBody **(required)**
      - `text` — string **(required)**
    - `footer` — InteractiveFooter
      - `text` — string **(required)**
    - `action` — InteractiveAction **(required)**
      - `buttons` — array
        - _array of_ `InteractiveButton`
          - `type` — string **(required)** _(enum: `reply`)_
          - `reply` — InteractiveButtonReply **(required)**
            - `id` — string **(required)**
            - `title` — string **(required)** _(maxLen=20)_
      - `sections` — array
        - _array of_ `InteractiveSection`
          - `title` — string **(required)**
          - `rows` — array **(required)**
            - _array of_ `InteractiveRow`
              - _(nesting depth limit — see `InteractiveRow` in the Schemas appendix)_
  - `extension` — string **(required)**
  - `userId` — string _(minLen=12; maxLen=12)_
  - `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` — string _(minLen=32; maxLen=32)_
- **Response 200** (`SendWhatsAppInteractiveMessageResponseContent`)
  - `type` — string _(default=RESULT)_
  - `success` — boolean
  - `company` — string
  - `status` — string _(default=RECEIVED)_
  - `id` — array
    - _array of_ `string`
  - `data` — SendWhatsAppInteractiveMessageData
    - `from` — string _(pattern=^\+[0-9]{10,14}$)_
    - `to` — string — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
    - `pbx` — string
    - `company` — string
    - `message` — InteractiveMessage
      - `type` — string **(required)** _(enum: `list`, `button`)_
      - `header` — InteractiveHeader
        - `type` — string **(required)** _(enum: `text`, `image`, `document`, `video`)_
        - `text` — string
        - `image` — InteractiveMedia
          - `id` — string **(required)**
          - `link` — string **(required)**
          - `filename` — string
        - `video` — InteractiveMedia
          - `id` — string **(required)**
          - `link` — string **(required)**
          - `filename` — string
        - `document` — InteractiveMedia
          - `id` — string **(required)**
          - `link` — string **(required)**
          - `filename` — string
      - `body` — InteractiveBody **(required)**
        - `text` — string **(required)**
      - `footer` — InteractiveFooter
        - `text` — string **(required)**
      - `action` — InteractiveAction **(required)**
        - `buttons` — array
          - _array of_ `InteractiveButton`
            - `type` — string **(required)** _(enum: `reply`)_
            - `reply` — InteractiveButtonReply **(required)**
              - _(nesting depth limit — see `InteractiveButtonReply` in the Schemas appendix)_
        - `sections` — array
          - _array of_ `InteractiveSection`
            - `title` — string **(required)**
            - `rows` — array **(required)**
              - _(nesting depth limit — see `InteractiveRow` in the Schemas appendix)_
    - `extension` — string
- Errors: `400`, `403`, `404`, `408`, `503`

#### `GET` `/v1/s2s/whatsapp/numbers`

- operationId: `ListWhatsAppNumbers`
- **Parameters**
  - `companyId` (query) — string **(required)**
- **Response 200** (`ListWhatsAppNumbersResponseContent`)
  - `type` — string **(required)** _(default=RESULT)_
  - `success` — boolean **(required)**
  - `timestamp` — number **(required)**
  - `result` — WhatsAppNumbersResult **(required)**
    - `companyId` — string **(required)**
    - `numbers` — array _(default=[])_
      - _array of_ `string`
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `GET` `/v1/s2s/whatsapp/templates`

- operationId: `ListWhatsAppTemplates`
- **Parameters**
  - `did` (query) — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- **Response 200** (`ListWhatsAppTemplatesResponseContent`)
  - `type` — string **(required)** _(default=WHATSAPP.TEMPLATES)_
  - `success` — boolean **(required)**
  - `did` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
  - `data` — array **(required)**
    - _array of_ `Template`
      - `name` — string **(required)**
      - `parameterFormat` — string **(required)** _(enum: `NAMED`)_
      - `components` — array **(required)**
        - _array of_ `Component`
          - `type` — string **(required)** _(enum: `HEADER`, `BODY`, `FOOTER`, `BUTTONS`)_
          - `format` — string **(required)** _(enum: `TEXT`, `IMAGE`, `DOCUMENT`, `VIDEO`)_
          - `text` — string
          - `example` — ComponentExample
            - `headerHandle` — array
              - _array of_ `string`
            - `bodyTextNamedParams` — array
              - _(nesting depth limit — see `BodyTextNamedParam` in the Schemas appendix)_
          - `buttons` — array
            - _array of_ `Button`
              - _(nesting depth limit — see `Button` in the Schemas appendix)_
      - `language` — string **(required)**
      - `status` — string **(required)** _(enum: `APPROVED`, `PAUSED`, `REJECTED`)_
      - `category` — string **(required)** _(enum: `MARKETING`, `UTILITY`, `AUTHENTICATION`)_
      - `subCategory` — string
      - `id` — string **(required)**
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

#### `POST` `/v1/s2s/whatsapp/templates`

- operationId: `SendWhatsAppTemplate`
- **Request body** (`application/json` — `SendWhatsAppTemplateRequestContent`) **(required)**
  - `to` — string **(required)** — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
  - `company` — string **(required)**
  - `pbx` — string **(required)**
  - `extension` — string **(required)**
  - `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
  - `channelId` — string
  - `messageId` — string
  - `userId` — string _(minLen=12; maxLen=12)_
  - `media` — array — Storage file ids for the template's media header. A header carries exactly one media object, so at most one id is accepted. Requires channelId and messageId, which are what resolve the file in conversation storage; without them the request is rejected. Omit it to send the media sample that was approved with the template: a template whose header is IMAGE, DOCUMENT or VIDEO is never rejected for carrying no file. The file must match the approved header format and Meta's size ceiling for it, or the request is rejected before anything is sent.
    - _array of_ `string`
  - `template` — TemplateWithParameters **(required)**
    - `name` — string **(required)**
    - `parameters` — array
      - _array of_ `TemplateParameter`
        - `name` — string **(required)**
        - `value` — string **(required)**
- **Response 200** (`SendWhatsAppTemplateResponseContent`)
  - `type` — string **(required)** _(default=RESULT)_
  - `success` — boolean **(required)**
  - `status` — string **(required)** _(default=RECEIVED)_
  - `id` — string **(required)**
  - `company` — string **(required)**
  - `data` — SendWhatsAppTemplateData **(required)**
    - `from` — string _(pattern=^\+[0-9]{10,14}$)_
    - `to` — string — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
    - `template` — TemplateWithParameters
      - `name` — string **(required)**
      - `parameters` — array
        - _array of_ `TemplateParameter`
          - `name` — string **(required)**
          - `value` — string **(required)**
    - `pbx` — string
    - `extension` — string
- Errors: `400`, `403`, `404`, `408`, `500`, `503`

### Schemas appendix — Classound API

<details><summary>126 component schemas</summary>

**`BodyTextNamedParam`**

- `paramName` — string **(required)**
- `example` — string **(required)**

**`BroadcastParams`**

- _map of_ `string`

**`BroadcastRecipient`**

- `to` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `params` — BroadcastParams
  - _map of_ `string`

**`BroadcastRejectedErrorResponseContent`**

- `type` — string **(required)** _(default=BROADCAST.REJECTED)_
- `success` — boolean _(default=False)_
- `error` — string
- `batchId` — string

**`BroadcastRejection`**

- `to` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `reason` — string **(required)** — Why this recipient was rejected (e.g. params do not match the template).

**`BroadcastTemplate`**

- `name` — string **(required)**

**`Button`**

- `type` — string **(required)** _(enum: `QUICK_REPLY`, `URL`, `PHONE_NUMBER`, `OTP`, `MPM`, `CATALOG`, `FLOW`, `VOICE_CALL`, `APP`)_
- `text` — string **(required)** _(maxLen=1024)_
- `flowId` — number
- `flowAction` — string
- `navigateScreen` — string

**`ButtonType`**

- string _(enum: `QUICK_REPLY`, `URL`, `PHONE_NUMBER`, `OTP`, `MPM`, `CATALOG`, `FLOW`, `VOICE_CALL`, `APP`)_

**`CleanupEsimOrderRequestContent`**

- `orderId` — string **(required)** — Order ID returned from POST /esim/order (base64-encoded key) _(minLen=1)_

**`CleanupEsimOrderResponseContent`**

- `status` — string **(required)** _(enum: `CLEANED`)_
- `orderId` — string **(required)** — Order ID that was cleaned up
- `simsReleased` — number **(required)**
- `steps` — CleanupStepsMap **(required)** — Map of cleanup step names to their result status (e.g. 'move_to_bookin' -> 'success')
  - _map of_ `string`

**`CleanupStepsMap`**

_Map of cleanup step names to their result status (e.g. 'move_to_bookin' -> 'success')_

- _map of_ `string`

**`Component`**

- `type` — string **(required)** _(enum: `HEADER`, `BODY`, `FOOTER`, `BUTTONS`)_
- `format` — string **(required)** _(enum: `TEXT`, `IMAGE`, `DOCUMENT`, `VIDEO`)_
- `text` — string
- `example` — ComponentExample
  - `headerHandle` — array
    - _array of_ `string`
  - `bodyTextNamedParams` — array
    - _array of_ `BodyTextNamedParam`
      - `paramName` — string **(required)**
      - `example` — string **(required)**
- `buttons` — array
  - _array of_ `Button`
    - `type` — string **(required)** _(enum: `QUICK_REPLY`, `URL`, `PHONE_NUMBER`, `OTP`, `MPM`, `CATALOG`, `FLOW`, `VOICE_CALL`, `APP`)_
    - `text` — string **(required)** _(maxLen=1024)_
    - `flowId` — number
    - `flowAction` — string
    - `navigateScreen` — string

**`ComponentExample`**

- `headerHandle` — array
  - _array of_ `string`
- `bodyTextNamedParams` — array
  - _array of_ `BodyTextNamedParam`
    - `paramName` — string **(required)**
    - `example` — string **(required)**

**`ComponentFormat`**

- string _(enum: `TEXT`, `IMAGE`, `DOCUMENT`, `VIDEO`)_

**`ComponentType`**

- string _(enum: `HEADER`, `BODY`, `FOOTER`, `BUTTONS`)_

**`CreateEsimOrderRequestContent`**

- `partnerId` — string **(required)** — Wildix partner ID _(minLen=1)_
- `partnerName` — string **(required)** — Partner display name (used for reseller creation) _(minLen=1)_
- `companyId` — string **(required)** — Wildix company ID _(minLen=1)_
- `partnerSapId` — string **(required)** — Dealer SAP_ID (the Salesforce Case 'SAP ID'). The reseller is resolved and reused by this stable id instead of a name-derived alias. Always present on the Case; a self/direct partner sends partnerSapId equal to companyId. _(minLen=1)_
- `companyName` — string **(required)** — Company display name (used for group creation) _(minLen=1)_
- `countryCode` — string **(required)** — ISO 3166-1 alpha-2 country code (e.g. IT, DE, US) _(pattern=^[A-Z]{2}$; minLen=2; maxLen=2)_
- `quantity` — number **(required)** — Number of eSIMs to reserve _(min=1; max=1000)_
- `requestId` — string **(required)** — Unique request ID from Salesforce for idempotency tracking _(minLen=1; maxLen=100)_
- `partnerEmail` — string — Partner contact email (optional, used for reseller creation)
- `bundle` — string **(required)** — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
- `homeLocations` — array **(required)** — List of ISO 3166-1 alpha-2 country codes for the Reseller/Group Home Location. At least one country required. Allows the reseller to serve subscribers across multiple countries. _(minItems=1)_
  - _array of_ `string`
- `partnerAddress` — string **(required)** — Partner billing address line 1 _(minLen=1)_
- `partnerPostCode` — string **(required)** — Partner billing postal/zip code _(minLen=1)_
- `partnerContactNumber` — string **(required)** — Partner contact phone number (E.164 digits only, no +) _(pattern=^[0-9]+$)_
- `partnerAddress2` — string — Partner billing address line 2 (optional)
- `partnerTown` — string — Partner billing town/city (optional)
- `partnerCounty` — string — Partner billing county/state (optional)
- `partnerDescription` — string — Reseller description (optional) _(minLen=3; maxLen=100)_

**`CreateEsimOrderResponseContent`**

- `status` — string **(required)** _(enum: `SUCCESS`, `PROCESSING`, `COMPLETED`, `FAILED`, `STALE`)_
- `orderId` — string **(required)** — Internal order tracking ID (UUID)
- `requestId` — string **(required)**
- `partnerId` — string **(required)**
- `companyId` — string **(required)**
- `countryCode` — string **(required)**
- `quantity` — number **(required)** — Number of eSIMs allocated in this order (equals requested quantity)
- `totalReserved` — number **(required)** — Total SIMs currently in ALLOCATED state for this company across all orders
- `bundle` — string — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_

**`CreateEsimPartnerRequestContent`**

- `partnerId` — string **(required)** _(minLen=1)_
- `partnerName` — string **(required)** _(minLen=1)_
- `companyId` — string **(required)** _(minLen=1)_
- `partnerSapId` — string **(required)** _(pattern=^.*\S.*$; minLen=1)_
- `companyName` — string **(required)** _(minLen=1)_
- `countryCode` — string **(required)** _(pattern=^[A-Za-z]{2}$; minLen=2; maxLen=2)_
- `quantity` — number **(required)** _(min=1; max=1000)_
- `requestId` — string **(required)** _(minLen=1; maxLen=100)_
- `partnerEmail` — string
- `bundle` — string **(required)** — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
- `homeLocations` — array **(required)** _(minItems=1)_
  - _array of_ `string`
- `partnerAddress` — string **(required)** _(minLen=3; maxLen=50)_
- `partnerPostCode` — string **(required)** _(minLen=1)_
- `partnerContactNumber` — string **(required)** _(pattern=^[0-9]+$; minLen=7)_
- `partnerAddress2` — string
- `partnerTown` — string
- `partnerCounty` — string
- `partnerDescription` — string _(minLen=3; maxLen=100)_

**`CreateEsimPartnerResponseContent`**

- `status` — string **(required)** _(enum: `READY`, `PROVISIONING`)_
- `ready` — boolean **(required)** — True after the customer group exists under the reseller and the eSIM order can be submitted.
- `orderCreated` — boolean **(required)** — Always false. Partner creation never creates an eSIM order or reserves a SIM.
- `errorCode` — string — Neutral machine-readable state returned while reseller billing setup is still in progress.
- `message` — string — Neutral operator-facing message. Upstream vendor details are never returned.

**`CreateNumbersOrderRequestContent`**

- `companyId` — string **(required)**
- `requestId` — string **(required)**
- `customerOrderId` — string **(required)**
- `webhookUrl` — string **(required)**
- `webhookToken` — string **(required)**
- `data` — OrderSearchCriteria **(required)** — Search criteria for phone number ordering. At least one of city, state, zip, or areaCode must be provided.
  - `country` — string **(required)** _(default=US)_
  - `state` — string
  - `quantity` — number **(required)** _(min=1; max=1000)_
  - `city` — string
  - `zip` — string _(pattern=^[A-Za-z0-9\-]{1,10}$)_
  - `areaCode` — string — Requested area code (NANP NPA, 3 digits, first digit 2-9) for number selection. A leading '+' or country/trunk code '1' is accepted and stripped server-side. _(pattern=^\+?1?[2-9][0-9]{2}$)_

**`CreateNumbersOrderResponseContent`**

- `status` — string **(required)**
- `supplierOrderId` — string
- `requestId` — string
- `customerOrderId` — string
- `orderStatus` — string
- `message` — string
- `testMode` — boolean

**`DeleteEsimEndpointResponseContent`**

- `status` — string **(required)** — Deletion status
- `companyId` — string **(required)** — Wildix company ID
- `serial` — string **(required)** — PBX serial number that was deleted

**`EsimBundleCount`**

_SIM count breakdown per bundle/plan_

- `bundle` — string **(required)** — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
- `available` — number **(required)** — SIMs available for provisioning in this bundle
- `active` — number **(required)** — SIMs actively provisioned in this bundle

**`EsimBundleSku`**

_Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products)_

- string _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_

**`EsimCleanupStatus`**

- string _(enum: `CLEANED`)_

**`EsimConflictErrorResponseContent`**

- `message` — string **(required)**
- `errorCode` — string

**`EsimOrderErrorResponseContent`**

- `requestId` — string
- `message` — string **(required)**
- `errorCode` — string

**`EsimOrderResult`**

_The order result payload carried by GetEsimOrderStatus on COMPLETED. Mirrors the CreateEsimOrder success body (which cannot be reused directly: an @output structure may not be embedded as a member)._

- `status` — string **(required)** _(enum: `SUCCESS`, `PROCESSING`, `COMPLETED`, `FAILED`, `STALE`)_
- `orderId` — string **(required)** — Internal order tracking ID (UUID)
- `requestId` — string **(required)**
- `partnerId` — string **(required)**
- `companyId` — string **(required)**
- `countryCode` — string **(required)**
- `quantity` — number **(required)** — Number of eSIMs allocated in this order
- `totalReserved` — number **(required)** — Total SIMs currently in ALLOCATED state for this company across all orders
- `bundle` — string — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_

**`EsimOrderStatus`**

- string _(enum: `SUCCESS`, `PROCESSING`, `COMPLETED`, `FAILED`, `STALE`)_

**`EsimPartnerCreationInternalErrorResponseContent`**

- `status` — string
- `requestId` — string
- `message` — string **(required)**
- `errorCode` — string
- `details` — string

**`EsimPartnerCreationStatus`**

- string _(enum: `READY`, `PROVISIONING`)_

**`EsimPartnerCreationUpstreamErrorResponseContent`**

- `status` — string
- `requestId` — string
- `message` — string **(required)**
- `errorCode` — string
- `details` — string

**`EsimProvisionStatus`**

- string _(enum: `PROVISIONED`, `ALREADY_PROVISIONED`)_

**`EsimTerminateStatus`**

- string _(enum: `TERMINATED`)_

**`EsimUpdateStatus`**

- string _(enum: `UPDATED`)_

**`GatewayTimeoutExceptionResponseContent`**

- `type` — string _(default=gateway-timeout)_
- `description` — string _(default=Connection error occurred)_

**`GetEsimOrderStatusResponseContent`**

- `orderId` — string **(required)** — Internal order tracking ID
- `status` — string **(required)** _(enum: `SUCCESS`, `PROCESSING`, `COMPLETED`, `FAILED`, `STALE`)_
- `ageSeconds` — number **(required)** — Seconds since the order was last updated
- `response` — EsimOrderResult — The order result payload carried by GetEsimOrderStatus on COMPLETED. Mirrors the CreateEsimOrder success body (which cannot be reused directly: an @output structure may not be embedded as a member).
  - `status` — string **(required)** _(enum: `SUCCESS`, `PROCESSING`, `COMPLETED`, `FAILED`, `STALE`)_
  - `orderId` — string **(required)** — Internal order tracking ID (UUID)
  - `requestId` — string **(required)**
  - `partnerId` — string **(required)**
  - `companyId` — string **(required)**
  - `countryCode` — string **(required)**
  - `quantity` — number **(required)** — Number of eSIMs allocated in this order
  - `totalReserved` — number **(required)** — Total SIMs currently in ALLOCATED state for this company across all orders
  - `bundle` — string — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
- `error` — string — Failure message; present only when status is FAILED.
- `errorCode` — string — Failure code; present only when status is FAILED.

**`GetEsimPartnerResponseContent`**

- `partnerId` — string **(required)** — Echo of the requested partnerId.
- `partnerName` — string **(required)** — Canonical partner display name as stored in the eSIM platform.
- `partnerAddress` — string — Billing address line 1.
- `partnerPostCode` — string — Billing postal/ZIP code.
- `partnerContactNumber` — string — E.164 contact number (digits only as stored in the eSIM platform).
- `partnerAddress2` — string — Billing address line 2 (optional).
- `partnerTown` — string — Billing town/city (optional).
- `partnerCounty` — string — Billing county/state (optional).
- `country` — string — ISO 3166-1 alpha-3 country code. Note: the eSIM platform returns alpha-3 on read; CreateEsimOrderInput.countryCode is alpha-2.
- `homeLocations` — array — List of ISO 3166-1 alpha-3 country codes the reseller is provisioned for.
  - _array of_ `string`

**`GetEsimQrCodeResponseContent`**

- `companyId` — string **(required)** — Wildix company ID
- `uid` — string **(required)** — Stable primary identifier of the subscriber _(pattern=^[0-9]{7}$)_
- `extension` — string — User extension on PBX (current value)
- `iccid` — string **(required)** — ICCID of the eSIM
- `activationCode` — string **(required)** — LPA activation code string for eSIM installation (e.g. LPA1:$smdp.example.com$code)
- `phone` — string — Mobile number (E.164 digits only)

**`GetEsimStatusResponseContent`**

- `companyId` — string **(required)** — Wildix company ID
- `uid` — string **(required)** — Stable primary identifier of the subscriber _(pattern=^[0-9]{7}$)_
- `extension` — string — User extension on PBX (current value)
- `phone` — string — Mobile number (E.164 digits only)
- `iccid` — string — ICCID of the eSIM
- `esimStatus` — string **(required)** — eSIM status (e.g. INSTALLED, AVAILABLE, RELEASED, ERROR)
- `subUID` — string — eSIM subscriber UID

**`GetSmsHistoryRecord`**

- `from` — string
- `to` — string
- `messageId` — string
- `messageText` — string
- `time` — number

**`GetSmsHistoryResponseContent`**

- `type` — string
- `result` — array
  - _array of_ `GetSmsHistoryRecord`
    - `from` — string
    - `to` — string
    - `messageId` — string
    - `messageText` — string
    - `time` — number

**`GetWhatsAppHistoryRecord`**

- `from` — string
- `to` — string
- `messageId` — string
- `messageText` — string
- `time` — number

**`GetWhatsAppHistoryResponseContent`**

- `type` — string
- `result` — array
  - _array of_ `GetWhatsAppHistoryRecord`
    - `from` — string
    - `to` — string
    - `messageId` — string
    - `messageText` — string
    - `time` — number

**`HeaderType`**

- string _(enum: `text`, `image`, `document`, `video`)_

**`InteractiveAction`**

- `buttons` — array
  - _array of_ `InteractiveButton`
    - `type` — string **(required)** _(enum: `reply`)_
    - `reply` — InteractiveButtonReply **(required)**
      - `id` — string **(required)**
      - `title` — string **(required)** _(maxLen=20)_
- `sections` — array
  - _array of_ `InteractiveSection`
    - `title` — string **(required)**
    - `rows` — array **(required)**
      - _array of_ `InteractiveRow`
        - _(nesting depth limit — see `InteractiveRow` in the Schemas appendix)_

**`InteractiveBody`**

- `text` — string **(required)**

**`InteractiveButton`**

- `type` — string **(required)** _(enum: `reply`)_
- `reply` — InteractiveButtonReply **(required)**
  - `id` — string **(required)**
  - `title` — string **(required)** _(maxLen=20)_

**`InteractiveButtonReply`**

- `id` — string **(required)**
- `title` — string **(required)** _(maxLen=20)_

**`InteractiveButtonType`**

- string _(enum: `reply`)_

**`InteractiveContentType`**

- string _(enum: `list`, `button`)_

**`InteractiveFooter`**

- `text` — string **(required)**

**`InteractiveHeader`**

- `type` — string **(required)** _(enum: `text`, `image`, `document`, `video`)_
- `text` — string
- `image` — InteractiveMedia
  - `id` — string **(required)**
  - `link` — string **(required)**
  - `filename` — string
- `video` — InteractiveMedia
  - `id` — string **(required)**
  - `link` — string **(required)**
  - `filename` — string
- `document` — InteractiveMedia
  - `id` — string **(required)**
  - `link` — string **(required)**
  - `filename` — string

**`InteractiveMedia`**

- `id` — string **(required)**
- `link` — string **(required)**
- `filename` — string

**`InteractiveMessage`**

- `type` — string **(required)** _(enum: `list`, `button`)_
- `header` — InteractiveHeader
  - `type` — string **(required)** _(enum: `text`, `image`, `document`, `video`)_
  - `text` — string
  - `image` — InteractiveMedia
    - `id` — string **(required)**
    - `link` — string **(required)**
    - `filename` — string
  - `video` — InteractiveMedia
    - `id` — string **(required)**
    - `link` — string **(required)**
    - `filename` — string
  - `document` — InteractiveMedia
    - `id` — string **(required)**
    - `link` — string **(required)**
    - `filename` — string
- `body` — InteractiveBody **(required)**
  - `text` — string **(required)**
- `footer` — InteractiveFooter
  - `text` — string **(required)**
- `action` — InteractiveAction **(required)**
  - `buttons` — array
    - _array of_ `InteractiveButton`
      - `type` — string **(required)** _(enum: `reply`)_
      - `reply` — InteractiveButtonReply **(required)**
        - _(nesting depth limit — see `InteractiveButtonReply` in the Schemas appendix)_
  - `sections` — array
    - _array of_ `InteractiveSection`
      - `title` — string **(required)**
      - `rows` — array **(required)**
        - _(nesting depth limit — see `InteractiveRow` in the Schemas appendix)_

**`InteractiveRow`**

- `id` — string **(required)**
- `title` — string **(required)**
- `description` — string

**`InteractiveSection`**

- `title` — string **(required)**
- `rows` — array **(required)**
  - _array of_ `InteractiveRow`
    - `id` — string **(required)**
    - `title` — string **(required)**
    - `description` — string

**`InternalErrorResponseContent`**

- `type` — string **(required)** _(default=internal-error)_
- `description` — string **(required)**
- `messageIds` — array — The messages that did enter the channel before the request failed, when the request was one that could produce several. A Messenger send that runs out of invocation time partway through a set of attachments returns them here, so a caller retrying the request can narrow it to what never arrived instead of sending every attachment again.
  - _array of_ `string`

**`InternalServerExceptionResponseContent`**

- `type` — string _(default=internal-server-error)_
- `description` — string _(default=Unknown error occured)_

**`ListEsimBundlesResponseContent`**

- `bundles` — array **(required)** — SIM count breakdown per bundle/plan
  - _array of_ `EsimBundleCount`
    - `bundle` — string **(required)** — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
    - `available` — number **(required)** — SIMs available for provisioning in this bundle
    - `active` — number **(required)** — SIMs actively provisioned in this bundle

**`ListEsimSubscribersResponseContent`**

- `companyId` — string **(required)** — Wildix company ID
- `subscribers` — array **(required)** — List of provisioned subscribers
  - _array of_ `SubscriberItem`
    - `extension` — string **(required)** — User extension / SIP address on PBX
    - `phone` — string — Mobile number (E.164 digits only)
    - `email` — string — User email address
    - `iccid` — string — ICCID of the eSIM
    - `subUID` — string — eSIM subscriber UID
    - `serial` — string — PBX serial number
    - `bundle` — string — Bundle/plan SKU
    - `firstName` — string — User first name
    - `lastName` — string — User last name
    - `status` — string — eSIM status (e.g. PROVISIONED, ACTIVE)
- `total` — number **(required)** — Total number of subscribers for this company
- `limit` — number **(required)** — Maximum number of subscribers returned
- `offset` — number **(required)** — Number of subscribers skipped

**`ListMessengerPagesResponseContent`**

- `type` — string **(required)** _(default=RESULT)_
- `success` — boolean **(required)**
- `timestamp` — number **(required)**
- `result` — MessengerPagesResult **(required)**
  - `companyId` — string **(required)**
  - `pages` — array _(default=[])_
    - _array of_ `MessengerPage`
      - `id` — string **(required)**
      - `name` — string **(required)**
      - `url` — string **(required)**
      - `channel` — string **(required)**

**`ListRcsBrandsResponseContent`**

- `type` — string **(required)** _(default=RESULT)_
- `success` — boolean **(required)**
- `timestamp` — number **(required)**
- `result` — RcsBrandsResult **(required)**
  - `companyId` — string **(required)**
  - `brands` — array _(default=[])_
    - _array of_ `RcsBrand`
      - `id` — string **(required)**
      - `name` — string **(required)** — The brand's display name, as the people it writes to see it. Entered when the brand is bound; equal to id for a brand bound without one.
      - `channel` — string **(required)**

**`ListSmsNumbersResponseContent`**

- `type` — string **(required)** _(default=RESULT)_
- `success` — boolean **(required)**
- `timestamp` — number **(required)**
- `result` — SmsNumbersResult **(required)**
  - `companyId` — string **(required)**
  - `numbers` — array _(default=[])_
    - _array of_ `string`

**`ListWhatsAppNumbersResponseContent`**

- `type` — string **(required)** _(default=RESULT)_
- `success` — boolean **(required)**
- `timestamp` — number **(required)**
- `result` — WhatsAppNumbersResult **(required)**
  - `companyId` — string **(required)**
  - `numbers` — array _(default=[])_
    - _array of_ `string`

**`ListWhatsAppTemplatesA2SResponseContent`**

- `type` — string **(required)** _(default=WHATSAPP.TEMPLATES)_
- `success` — boolean **(required)**
- `did` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `data` — array **(required)**
  - _array of_ `Template`
    - `name` — string **(required)**
    - `parameterFormat` — string **(required)** _(enum: `NAMED`)_
    - `components` — array **(required)**
      - _array of_ `Component`
        - _(nesting depth limit — see `Component` in the Schemas appendix)_
    - `language` — string **(required)**
    - `status` — string **(required)** _(enum: `APPROVED`, `PAUSED`, `REJECTED`)_
    - `category` — string **(required)** _(enum: `MARKETING`, `UTILITY`, `AUTHENTICATION`)_
    - `subCategory` — string
    - `id` — string **(required)**

**`ListWhatsAppTemplatesResponseContent`**

- `type` — string **(required)** _(default=WHATSAPP.TEMPLATES)_
- `success` — boolean **(required)**
- `did` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `data` — array **(required)**
  - _array of_ `Template`
    - `name` — string **(required)**
    - `parameterFormat` — string **(required)** _(enum: `NAMED`)_
    - `components` — array **(required)**
      - _array of_ `Component`
        - _(nesting depth limit — see `Component` in the Schemas appendix)_
    - `language` — string **(required)**
    - `status` — string **(required)** _(enum: `APPROVED`, `PAUSED`, `REJECTED`)_
    - `category` — string **(required)** _(enum: `MARKETING`, `UTILITY`, `AUTHENTICATION`)_
    - `subCategory` — string
    - `id` — string **(required)**

**`MessagingWindowClosedErrorResponseContent`**

_The conversation cannot be answered: the person has not written recently enough._

- `type` — string **(required)** _(default=window-closed)_
- `description` — string **(required)**

**`MessengerPage`**

_One Facebook page a company can send from. channel is always "messenger"._

- `id` — string **(required)**
- `name` — string **(required)**
- `url` — string **(required)**
- `channel` — string **(required)**

**`MessengerPagesResult`**

- `companyId` — string **(required)**
- `pages` — array _(default=[])_
  - _array of_ `MessengerPage`
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `url` — string **(required)**
    - `channel` — string **(required)**

**`MessengerSendResult`**

_What the send produced._

- `from` — string **(required)** — The page the message was sent from, a Facebook Page ID, echoed from the request. A String and not a PhoneNumber, which this member name carries on the other send routes: a Page ID is an opaque Meta identifier and is never normalised the way a number is.
- `to` — string **(required)** — The recipient, a Page Scoped ID, echoed from the request and meaningful only together with that page. A String and not a PhoneNumber, which this member name carries on the other send routes: a PSID is an opaque Meta identifier and is never normalised the way a number is.
- `messageId` — string **(required)** — The correlation key of the first message, the one a delivery status carries.
- `messageIds` — array **(required)** — Every message the request produced, in the order they were sent.
  - _array of_ `string`
- `windowState` — string **(required)** — The conversation state the message was sent under, OPEN or HUMAN_AGENT.
- `tag` — string — The tag actually applied, whether it was given or supplied for the caller.
- `simulated` — boolean — True when the request was recorded but nothing was sent to the supplier.

**`MessengerSuggestion`**

_One button under a message. Which members are required depends on the action, which Smithy cannot express and the service enforces: a Reply needs a label and a postbackdata, a Dial and an optin need a label, and a Login and a Logout carry no text at all._

- `action` — string — What CM.com does when the button is pressed: Reply, Dial, Login, Logout, ViewProduct (in beta) or optin, which is the Marketing Messages opt-in request and is the one action spelled in lower case. Matched without regard to case, and an action outside this list is rejected. Omit it for a quick reply, which is what every button was before this member existed. _(minLen=1)_
- `label` — string — What the person sees on the button. At most 20 characters, except on an optin, where it is the request being answered and may run to 65. Required for Reply, Dial and optin; a Login and a Logout show no text. _(minLen=1; maxLen=65)_
- `postbackdata` — string — Returned on the next inbound message when the button is pressed, as postbackData. Required for a Reply, which is the only action that comes back to us as an inbound. _(minLen=1)_
- `optin` — any — The opt-in request. Required when the action is optin, and meaningless otherwise.

**`OrderErrorResponseContent`**

- `type` — string **(required)** _(default=order-error)_
- `description` — string **(required)**
- `requestId` — string
- `customerOrderId` — string
- `errorCode` — string

**`OrderSearchCriteria`**

_Search criteria for phone number ordering. At least one of city, state, zip, or areaCode must be provided._

- `country` — string **(required)** _(default=US)_
- `state` — string
- `quantity` — number **(required)** _(min=1; max=1000)_
- `city` — string
- `zip` — string _(pattern=^[A-Za-z0-9\-]{1,10}$)_
- `areaCode` — string — Requested area code (NANP NPA, 3 digits, first digit 2-9) for number selection. A leading '+' or country/trunk code '1' is accepted and stripped server-side. _(pattern=^\+?1?[2-9][0-9]{2}$)_

**`ParameterFormat`**

- string _(enum: `NAMED`)_

**`ProvisionEsimSubscriberRequestContent`**

- `companyId` — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
- `uid` — string **(required)** — Stable primary identifier for the subscriber. _(pattern=^[0-9]{7}$)_
- `serial` — string **(required)** — PBX serial number (maps to KC-PBX / endpointName) _(minLen=1)_
- `host` — string **(required)** — PBX domain (IP or FQDN, e.g. 'mycompany.wildixin.com') _(minLen=1)_
- `extension` — string **(required)** — User extension / SIP address on PBX _(minLen=1; maxLen=45)_
- `phone` — string **(required)** — Mobile number with country code, digits only (MDN-E164) _(minLen=5; maxLen=20)_
- `email` — string **(required)** — User email address (eSIM QR code is sent to this address) _(minLen=3)_
- `firstName` — string — User first name
- `lastName` — string — User last name
- `userPassword` — string **(required)** — PBX SIP password for the extension (used to register the eSIM to the PBX) _(minLen=1)_
- `bundle` — string — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_

**`ProvisionEsimSubscriberResponseContent`**

- `status` — string **(required)** _(enum: `PROVISIONED`, `ALREADY_PROVISIONED`)_
- `companyId` — string **(required)** — Wildix company ID
- `uid` — string **(required)** — Unique identifier of the user in the WMS Network (7-digit numeric, 1,000,000–9,999,999) _(pattern=^[0-9]{7}$)_
- `extension` — string **(required)** — User extension
- `phone` — string **(required)** — Mobile number (MDN-E164)
- `subUID` — string **(required)** — eSIM subscriber UID (needed for future updates/deletes)
- `iccid` — string **(required)** — ICCID of the provisioned eSIM
- `activationCode` — string — LPA activation code string for eSIM installation

**`RcsBrand`**

_One RCS brand a company can send from. id is the unique name CM.com gives the brand's RCS agent, used as written; channel is always "rcs"._

- `id` — string **(required)**
- `name` — string **(required)** — The brand's display name, as the people it writes to see it. Entered when the brand is bound; equal to id for a brand bound without one.
- `channel` — string **(required)**

**`RcsBrandsResult`**

- `companyId` — string **(required)**
- `brands` — array _(default=[])_
  - _array of_ `RcsBrand`
    - `id` — string **(required)**
    - `name` — string **(required)** — The brand's display name, as the people it writes to see it. Entered when the brand is bound; equal to id for a brand bound without one.
    - `channel` — string **(required)**

**`RcsSendResult`**

_What the send produced._

- `from` — string **(required)** — The brand the message was sent from, echoed from the request.
- `to` — string **(required)** — The recipient, echoed from the request. _(pattern=^\+[0-9]{10,14}$)_
- `messageId` — string **(required)** — The correlation key of the first message, the one a delivery status carries.
- `messageIds` — array **(required)** — Every message the request produced, in the order they were sent.
  - _array of_ `string`
- `simulated` — boolean — True when the request was recorded but nothing was sent to the supplier.

**`RcsSuggestion`**

_One suggested reply under an RCS message._

- `label` — string **(required)** — What the person sees on the button. _(minLen=1; maxLen=25)_
- `postbackdata` — string **(required)** — Returned on the next inbound message when the button is pressed, as postback. _(minLen=1)_

**`RefreshEsimQrCodeRequestContent`**

- `companyId` — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
- `extension` — string **(required)** — User extension / SIP address on PBX _(minLen=1; maxLen=45)_

**`RefreshEsimQrCodeResponseContent`**

- `companyId` — string **(required)** — Wildix company ID
- `extension` — string **(required)** — User extension on PBX
- `iccid` — string **(required)** — ICCID of the eSIM
- `activationCode` — string **(required)** — Regenerated LPA activation code string for eSIM installation
- `phone` — string — Mobile number (E.164 digits only)

**`ReleaseEsimSimsRequestContent`**

- `companyId` — string **(required)** — Wildix company identifier (e.g. IT_W123644).
- `bundle` — string **(required)** — Bundle SKU (e.g. PLAN-VC-MSG-2G) whose unprovisioned SIMs to release.
- `count` — number **(required)** — Number of unprovisioned SIMs to release. Server picks the oldest by allocation date.

**`ReleaseEsimSimsResponseContent`**

- `released` — array **(required)** — ICCIDs successfully released back to the free pool.
  - _array of_ `string`
- `failed` — array **(required)** — ICCIDs that could not be released, with per-ICCID failure reason.
  - _array of_ `ReleaseFailureItem`
    - `iccid` — string **(required)**
    - `reason` — string **(required)**
- `releasedCount` — number **(required)** — Count of successfully released ICCIDs (echo of released.length for convenience).

**`ReleaseFailureItem`**

- `iccid` — string **(required)**
- `reason` — string **(required)**

**`RequestValidationExceptionResponseContent`**

- `type` — string _(default=request-validation)_
- `description` — string _(default=Number does not belong to company)_

**`SendMessengerMessageRequestContent`**

- `companyId` — string **(required)** _(minLen=1)_
- `from` — string **(required)** — The page to send from, a Facebook Page ID. It must be bound to this company. A String and not a PhoneNumber, which this member name carries on the other send routes: a Page ID is an opaque Meta identifier and is never normalised the way a number is. _(minLen=1)_
- `to` — string **(required)** — The recipient, a Page Scoped ID, meaningful only together with that page. A String and not a PhoneNumber, which this member name carries on the other send routes: a PSID is an opaque Meta identifier and is never normalised the way a number is. _(minLen=1)_
- `message` — string — The text of the message. A request must carry a message, media, or both. _(maxLen=2000)_
- `extension` — string — The extension of the operator sending the message. Recorded on the message detail record, so that a message can be reported per user; nothing is sent with it.
- `userId` — string — The x-bees user sending the message. Recorded on the message detail record as channel metadata; nothing is sent with it, and it takes no part in resolving an attachment. _(minLen=12; maxLen=12)_
- `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `messageId` — string _(minLen=32; maxLen=32)_
- `media` — array — Storage file ids to attach, at most ten. Each becomes a message of its own. Requires channelId and messageId, which are what resolve the files in conversation storage; without them the request is rejected. _(maxItems=10)_
  - _array of_ `string`
- `suggestions` — array — Buttons shown under the message. A quick reply by default, or whatever action the entry names, including the Marketing Messages opt-in request.
  - _array of_ `MessengerSuggestion`
    - `action` — string — What CM.com does when the button is pressed: Reply, Dial, Login, Logout, ViewProduct (in beta) or optin, which is the Marketing Messages opt-in request and is the one action spelled in lower case. Matched without regard to case, and an action outside this list is rejected. Omit it for a quick reply, which is what every button was before this member existed. _(minLen=1)_
    - `label` — string — What the person sees on the button. At most 20 characters, except on an optin, where it is the request being answered and may run to 65. Required for Reply, Dial and optin; a Login and a Logout show no text. _(minLen=1; maxLen=65)_
    - `postbackdata` — string — Returned on the next inbound message when the button is pressed, as postbackData. Required for a Reply, which is the only action that comes back to us as an inbound. _(minLen=1)_
    - `optin` — any — The opt-in request. Required when the action is optin, and meaningless otherwise.
- `tag` — string — A Meta message tag. Omit it and HUMAN_AGENT is applied when the conversation needs one.

**`SendMessengerMessageResponseContent`**

- `type` — string **(required)** _(default=RESULT)_
- `success` — boolean **(required)**
- `timestamp` — number **(required)**
- `result` — MessengerSendResult **(required)** — What the send produced.
  - `from` — string **(required)** — The page the message was sent from, a Facebook Page ID, echoed from the request. A String and not a PhoneNumber, which this member name carries on the other send routes: a Page ID is an opaque Meta identifier and is never normalised the way a number is.
  - `to` — string **(required)** — The recipient, a Page Scoped ID, echoed from the request and meaningful only together with that page. A String and not a PhoneNumber, which this member name carries on the other send routes: a PSID is an opaque Meta identifier and is never normalised the way a number is.
  - `messageId` — string **(required)** — The correlation key of the first message, the one a delivery status carries.
  - `messageIds` — array **(required)** — Every message the request produced, in the order they were sent.
    - _array of_ `string`
  - `windowState` — string **(required)** — The conversation state the message was sent under, OPEN or HUMAN_AGENT.
  - `tag` — string — The tag actually applied, whether it was given or supplied for the caller.
  - `simulated` — boolean — True when the request was recorded but nothing was sent to the supplier.

**`SendRcsMessageRequestContent`**

- `companyId` — string **(required)** _(minLen=1)_
- `from` — string **(required)** — The brand to send from, an id ListRcsBrands returns. It must be bound to this company. A String and not a PhoneNumber: a brand id is a name and is never normalised the way a number is. _(minLen=1)_
- `to` — string **(required)** — The recipient's phone number in E.164. _(pattern=^\+[0-9]{10,14}$)_
- `message` — string — The text of the message. A request must carry a message, media, or both. _(maxLen=2048)_
- `extension` — string — The extension of the operator sending the message. Recorded on the message detail record, so that a message can be reported per user; nothing is sent with it.
- `userId` — string — The x-bees user sending the message. Recorded on the message detail record as channel metadata; nothing is sent with it, and it takes no part in resolving an attachment. _(minLen=12; maxLen=12)_
- `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `messageId` — string _(minLen=32; maxLen=32)_
- `media` — array — Storage file ids to attach, at most ten. Each becomes a message of its own. Requires channelId and messageId, which are what resolve the files in conversation storage; without them the request is rejected. _(maxItems=10)_
  - _array of_ `string`
- `suggestions` — array — Suggested replies shown under the message, at most eleven. _(maxItems=11)_
  - _array of_ `RcsSuggestion`
    - `label` — string **(required)** — What the person sees on the button. _(minLen=1; maxLen=25)_
    - `postbackdata` — string **(required)** — Returned on the next inbound message when the button is pressed, as postback. _(minLen=1)_

**`SendRcsMessageResponseContent`**

- `type` — string **(required)** _(default=RESULT)_
- `success` — boolean **(required)**
- `timestamp` — number **(required)**
- `result` — RcsSendResult **(required)** — What the send produced.
  - `from` — string **(required)** — The brand the message was sent from, echoed from the request.
  - `to` — string **(required)** — The recipient, echoed from the request. _(pattern=^\+[0-9]{10,14}$)_
  - `messageId` — string **(required)** — The correlation key of the first message, the one a delivery status carries.
  - `messageIds` — array **(required)** — Every message the request produced, in the order they were sent.
    - _array of_ `string`
  - `simulated` — boolean — True when the request was recorded but nothing was sent to the supplier.

**`SendSmsData`**

- `from` — string _(pattern=^\+[0-9]{10,14}$)_
- `to` — string _(pattern=^\+[0-9]{10,14}$)_
- `message` — string
- `pbx` — string
- `extension` — string

**`SendSmsFromApplicationRequestContent`**

- `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `to` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `message` — string **(required)**

**`SendSmsFromApplicationResponseContent`**

- `type` — string _(default=RESULT)_
- `success` — boolean
- `status` — string _(default=RECEIVED)_
- `id` — array
  - _array of_ `string`
- `company` — string
- `data` — SendSmsData
  - `from` — string _(pattern=^\+[0-9]{10,14}$)_
  - `to` — string _(pattern=^\+[0-9]{10,14}$)_
  - `message` — string
  - `pbx` — string
  - `extension` — string

**`SendSmsOutputData`**

- `from` — string _(pattern=^\+[0-9]{10,14}$)_
- `to` — string _(pattern=^\+[0-9]{10,14}$)_
- `message` — string
- `pbx` — string
- `extension` — string

**`SendSmsRequestContent`**

- `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `to` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `pbx` — string **(required)**
- `company` — string **(required)**
- `message` — string **(required)**
- `extension` — string **(required)**
- `media` — array
  - _array of_ `string`
- `userId` — string _(minLen=12; maxLen=12)_
- `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `messageId` — string _(minLen=32; maxLen=32)_

**`SendSmsResponseContent`**

- `type` — string
- `success` — boolean
- `status` — string
- `id` — array
  - _array of_ `string`
- `company` — string
- `data` — SendSmsOutputData
  - `from` — string _(pattern=^\+[0-9]{10,14}$)_
  - `to` — string _(pattern=^\+[0-9]{10,14}$)_
  - `message` — string
  - `pbx` — string
  - `extension` — string

**`SendWhatsAppInteractiveMessageData`**

- `from` — string _(pattern=^\+[0-9]{10,14}$)_
- `to` — string — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
- `pbx` — string
- `company` — string
- `message` — InteractiveMessage
  - `type` — string **(required)** _(enum: `list`, `button`)_
  - `header` — InteractiveHeader
    - `type` — string **(required)** _(enum: `text`, `image`, `document`, `video`)_
    - `text` — string
    - `image` — InteractiveMedia
      - `id` — string **(required)**
      - `link` — string **(required)**
      - `filename` — string
    - `video` — InteractiveMedia
      - `id` — string **(required)**
      - `link` — string **(required)**
      - `filename` — string
    - `document` — InteractiveMedia
      - `id` — string **(required)**
      - `link` — string **(required)**
      - `filename` — string
  - `body` — InteractiveBody **(required)**
    - `text` — string **(required)**
  - `footer` — InteractiveFooter
    - `text` — string **(required)**
  - `action` — InteractiveAction **(required)**
    - `buttons` — array
      - _array of_ `InteractiveButton`
        - _(nesting depth limit — see `InteractiveButton` in the Schemas appendix)_
    - `sections` — array
      - _array of_ `InteractiveSection`
        - _(nesting depth limit — see `InteractiveSection` in the Schemas appendix)_
- `extension` — string

**`SendWhatsAppInteractiveMessageRequestContent`**

- `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `to` — string **(required)** — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
- `pbx` — string **(required)**
- `company` — string **(required)**
- `message` — InteractiveMessage **(required)**
  - `type` — string **(required)** _(enum: `list`, `button`)_
  - `header` — InteractiveHeader
    - `type` — string **(required)** _(enum: `text`, `image`, `document`, `video`)_
    - `text` — string
    - `image` — InteractiveMedia
      - `id` — string **(required)**
      - `link` — string **(required)**
      - `filename` — string
    - `video` — InteractiveMedia
      - `id` — string **(required)**
      - `link` — string **(required)**
      - `filename` — string
    - `document` — InteractiveMedia
      - `id` — string **(required)**
      - `link` — string **(required)**
      - `filename` — string
  - `body` — InteractiveBody **(required)**
    - `text` — string **(required)**
  - `footer` — InteractiveFooter
    - `text` — string **(required)**
  - `action` — InteractiveAction **(required)**
    - `buttons` — array
      - _array of_ `InteractiveButton`
        - _(nesting depth limit — see `InteractiveButton` in the Schemas appendix)_
    - `sections` — array
      - _array of_ `InteractiveSection`
        - _(nesting depth limit — see `InteractiveSection` in the Schemas appendix)_
- `extension` — string **(required)**
- `userId` — string _(minLen=12; maxLen=12)_
- `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `messageId` — string _(minLen=32; maxLen=32)_

**`SendWhatsAppInteractiveMessageResponseContent`**

- `type` — string _(default=RESULT)_
- `success` — boolean
- `company` — string
- `status` — string _(default=RECEIVED)_
- `id` — array
  - _array of_ `string`
- `data` — SendWhatsAppInteractiveMessageData
  - `from` — string _(pattern=^\+[0-9]{10,14}$)_
  - `to` — string — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
  - `pbx` — string
  - `company` — string
  - `message` — InteractiveMessage
    - `type` — string **(required)** _(enum: `list`, `button`)_
    - `header` — InteractiveHeader
      - `type` — string **(required)** _(enum: `text`, `image`, `document`, `video`)_
      - `text` — string
      - `image` — InteractiveMedia
        - _(nesting depth limit — see `InteractiveMedia` in the Schemas appendix)_
      - `video` — InteractiveMedia
        - _(nesting depth limit — see `InteractiveMedia` in the Schemas appendix)_
      - `document` — InteractiveMedia
        - _(nesting depth limit — see `InteractiveMedia` in the Schemas appendix)_
    - `body` — InteractiveBody **(required)**
      - `text` — string **(required)**
    - `footer` — InteractiveFooter
      - `text` — string **(required)**
    - `action` — InteractiveAction **(required)**
      - `buttons` — array
        - _(nesting depth limit — see `InteractiveButton` in the Schemas appendix)_
      - `sections` — array
        - _(nesting depth limit — see `InteractiveSection` in the Schemas appendix)_
  - `extension` — string

**`SendWhatsAppMessageData`**

- `from` — string _(pattern=^\+[0-9]{10,14}$)_
- `to` — string — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
- `pbx` — string
- `company` — string
- `message` — string
- `extension` — string
- `media` — array
  - _array of_ `string`
- `userId` — string _(minLen=12; maxLen=12)_
- `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `messageId` — string _(minLen=32; maxLen=32)_

**`SendWhatsAppMessageRequestContent`**

- `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `to` — string **(required)** — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
- `pbx` — string **(required)**
- `company` — string **(required)**
- `message` — string **(required)**
- `extension` — string **(required)**
- `media` — array
  - _array of_ `string`
- `userId` — string _(minLen=12; maxLen=12)_
- `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `messageId` — string _(minLen=32; maxLen=32)_

**`SendWhatsAppMessageResponseContent`**

- `type` — string _(default=RESULT)_
- `success` — boolean
- `company` — string
- `status` — string _(default=RECEIVED)_
- `id` — array
  - _array of_ `string`
- `data` — SendWhatsAppMessageData
  - `from` — string _(pattern=^\+[0-9]{10,14}$)_
  - `to` — string — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
  - `pbx` — string
  - `company` — string
  - `message` — string
  - `extension` — string
  - `media` — array
    - _array of_ `string`
  - `userId` — string _(minLen=12; maxLen=12)_
  - `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` — string _(minLen=32; maxLen=32)_

**`SendWhatsAppTemplateBroadcastRequestContent`**

- `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `campaignName` — string — Optional human-readable campaign label; the server generates the batchId
- `template` — BroadcastTemplate **(required)**
  - `name` — string **(required)**
- `recipients` — array **(required)** — Per-recipient targets; each may carry its own template body parameters. Max 5000 per call; the server may enforce a lower per-environment cap. _(minItems=1; maxItems=5000)_
  - _array of_ `BroadcastRecipient`
    - `to` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
    - `params` — BroadcastParams
      - _map of_ `string`

**`SendWhatsAppTemplateBroadcastResponseContent`**

- `type` — string **(required)** _(default=BROADCAST.ACCEPTED)_
- `success` — boolean **(required)**
- `batchId` — string **(required)**
- `accepted` — number **(required)** — Number of recipients accepted and enqueued; per-recipient delivery status arrives asynchronously via DLR
- `rejected` — array — Recipients rejected by validation (e.g. params not matching the template). The rest of the batch is still accepted; rejected recipients are also reported on the status webhook.
  - _array of_ `BroadcastRejection`
    - `to` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
    - `reason` — string **(required)** — Why this recipient was rejected (e.g. params do not match the template).

**`SendWhatsAppTemplateData`**

- `from` — string _(pattern=^\+[0-9]{10,14}$)_
- `to` — string — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
- `template` — TemplateWithParameters
  - `name` — string **(required)**
  - `parameters` — array
    - _array of_ `TemplateParameter`
      - `name` — string **(required)**
      - `value` — string **(required)**
- `pbx` — string
- `extension` — string

**`SendWhatsAppTemplateRequestContent`**

- `to` — string **(required)** — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
- `company` — string **(required)**
- `pbx` — string **(required)**
- `extension` — string **(required)**
- `from` — string **(required)** _(pattern=^\+[0-9]{10,14}$)_
- `channelId` — string
- `messageId` — string
- `userId` — string _(minLen=12; maxLen=12)_
- `media` — array — Storage file ids for the template's media header. A header carries exactly one media object, so at most one id is accepted. Requires channelId and messageId, which are what resolve the file in conversation storage; without them the request is rejected. Omit it to send the media sample that was approved with the template: a template whose header is IMAGE, DOCUMENT or VIDEO is never rejected for carrying no file. The file must match the approved header format and Meta's size ceiling for it, or the request is rejected before anything is sent.
  - _array of_ `string`
- `template` — TemplateWithParameters **(required)**
  - `name` — string **(required)**
  - `parameters` — array
    - _array of_ `TemplateParameter`
      - `name` — string **(required)**
      - `value` — string **(required)**

**`SendWhatsAppTemplateResponseContent`**

- `type` — string **(required)** _(default=RESULT)_
- `success` — boolean **(required)**
- `status` — string **(required)** _(default=RECEIVED)_
- `id` — string **(required)**
- `company` — string **(required)**
- `data` — SendWhatsAppTemplateData **(required)**
  - `from` — string _(pattern=^\+[0-9]{10,14}$)_
  - `to` — string — A WhatsApp user: a phone number, or the Business-Scoped User ID (BSUID, `<ISO country code>.<up to 128 letters and digits>`) Meta sends instead of the number for a user with a username. Classound and x-bees keep a BSUID in Meta's spelling, such as `TR.3189549211436051`, and never change its letter case; x-bees finds a user by a BSUID regardless of letter case. Authentication templates cannot be sent to a BSUID. _(pattern=^(\+[0-9]{10,14}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
  - `template` — TemplateWithParameters
    - `name` — string **(required)**
    - `parameters` — array
      - _array of_ `TemplateParameter`
        - _(nesting depth limit — see `TemplateParameter` in the Schemas appendix)_
  - `pbx` — string
  - `extension` — string

**`SmsNumbersResult`**

- `companyId` — string **(required)**
- `numbers` — array _(default=[])_
  - _array of_ `string`

**`SubscriberItem`**

_A provisioned eSIM subscriber_

- `extension` — string **(required)** — User extension / SIP address on PBX
- `phone` — string — Mobile number (E.164 digits only)
- `email` — string — User email address
- `iccid` — string — ICCID of the eSIM
- `subUID` — string — eSIM subscriber UID
- `serial` — string — PBX serial number
- `bundle` — string — Bundle/plan SKU
- `firstName` — string — User first name
- `lastName` — string — User last name
- `status` — string — eSIM status (e.g. PROVISIONED, ACTIVE)

**`SupplierRejectedErrorResponseContent`**

_The messaging supplier refused the message._

- `type` — string **(required)** _(default=supplier-rejected)_
- `description` — string **(required)**
- `messageIds` — array — The messages that did enter the channel before the supplier refused one of them. The first refusal stops the rest, so a Messenger send of several attachments can be refused with some already delivered; a caller retrying the request can narrow it to what is missing from this list.
  - _array of_ `string`

**`SyncEsimTransformsRequestContent`**

- `companyId` — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
- `transforms` — array **(required)** — List of desired extension-to-E.164 mappings (full snapshot)
  - _array of_ `TransformEntry`
    - `extension` — string **(required)** — PBX extension / short code _(minLen=1; maxLen=45)_
    - `e164` — string **(required)** — E.164 number (digits only, no +) _(minLen=5; maxLen=20)_

**`SyncEsimTransformsResponseContent`**

- `companyId` — string **(required)** — Wildix company ID
- `added` — number **(required)** — Number of transforms added
- `updated` — number **(required)** — Number of transforms updated
- `deleted` — number **(required)** — Number of transforms deleted
- `errors` — array — List of per-transform errors (if any)
  - _array of_ `TransformError`
    - `action` — string — Action attempted: add, update, or delete
    - `extension` — string — Extension that failed
    - `error` — string — Error message from the eSIM provider

**`Template`**

- `name` — string **(required)**
- `parameterFormat` — string **(required)** _(enum: `NAMED`)_
- `components` — array **(required)**
  - _array of_ `Component`
    - `type` — string **(required)** _(enum: `HEADER`, `BODY`, `FOOTER`, `BUTTONS`)_
    - `format` — string **(required)** _(enum: `TEXT`, `IMAGE`, `DOCUMENT`, `VIDEO`)_
    - `text` — string
    - `example` — ComponentExample
      - `headerHandle` — array
        - _array of_ `string`
      - `bodyTextNamedParams` — array
        - _(nesting depth limit — see `BodyTextNamedParam` in the Schemas appendix)_
    - `buttons` — array
      - _array of_ `Button`
        - _(nesting depth limit — see `Button` in the Schemas appendix)_
- `language` — string **(required)**
- `status` — string **(required)** _(enum: `APPROVED`, `PAUSED`, `REJECTED`)_
- `category` — string **(required)** _(enum: `MARKETING`, `UTILITY`, `AUTHENTICATION`)_
- `subCategory` — string
- `id` — string **(required)**

**`TemplateCategory`**

- string _(enum: `MARKETING`, `UTILITY`, `AUTHENTICATION`)_

**`TemplateParameter`**

- `name` — string **(required)**
- `value` — string **(required)**

**`TemplateStatus`**

- string _(enum: `APPROVED`, `PAUSED`, `REJECTED`)_

**`TemplateWithParameters`**

- `name` — string **(required)**
- `parameters` — array
  - _array of_ `TemplateParameter`
    - `name` — string **(required)**
    - `value` — string **(required)**

**`TerminateEsimSubscriberRequestContent`**

- `companyId` — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
- `uid` — string **(required)** — Stable primary identifier of the subscriber to terminate _(pattern=^[0-9]{7}$)_

**`TerminateEsimSubscriberResponseContent`**

- `status` — string **(required)** _(enum: `TERMINATED`)_
- `companyId` — string **(required)** — Wildix company ID
- `uid` — string **(required)** — Stable primary identifier of the terminated subscriber _(pattern=^[0-9]{7}$)_
- `extension` — string — User extension at time of termination (from DynamoDB)
- `subUID` — string — eSIM subscriber UID

**`TransformEntry`**

- `extension` — string **(required)** — PBX extension / short code _(minLen=1; maxLen=45)_
- `e164` — string **(required)** — E.164 number (digits only, no +) _(minLen=5; maxLen=20)_

**`TransformError`**

- `action` — string — Action attempted: add, update, or delete
- `extension` — string — Extension that failed
- `error` — string — Error message from the eSIM provider

**`UpdateEsimSubscriberRequestContent`**

- `companyId` — string — Wildix company ID. Optional when using PBX token (resolved from authorizer).
- `email` — string — New email address
- `firstName` — string — New first name
- `lastName` — string — New last name
- `phone` — string — New mobile number with country code, digits only (MDN-E164)
- `userPassword` — string — New PBX SIP password
- `bundle` — string — Valid eSIM bundle/plan SKUs (SUBSCRIBER.TARIFF products) _(enum: `PLAN-VC-MSG-2G`, `PLAN-VC-MSG-4G`, `PLAN-VC-MSG-10G`, `PLAN-VC-MSG-20G`, `PLAN-VC-MSG-UNLTD`, `PLAN-VC-MSG-BKGND`)_
- `newExtension` — string — New extension / SIP address. Changes the subscriber's SIP-ADDRESS and migrates the record. _(minLen=1; maxLen=45)_

**`UpdateEsimSubscriberResponseContent`**

- `status` — string **(required)** _(enum: `UPDATED`)_
- `companyId` — string **(required)** — Wildix company ID
- `uid` — string **(required)** — Stable primary identifier of the updated subscriber _(pattern=^[0-9]{7}$)_
- `updatedFields` — array **(required)** — List of fields that were updated
  - _array of_ `string`

**`UserNotFoundExceptionResponseContent`**

- `type` — string _(default=user-not-found)_
- `description` — string _(default=Customer doesn't exist)_

**`WhatsAppNumbersResult`**

- `companyId` — string **(required)**
- `numbers` — array _(default=[])_
  - _array of_ `string`

</details>
