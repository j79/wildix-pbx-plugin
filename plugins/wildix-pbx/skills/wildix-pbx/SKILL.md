---
name: wildix-pbx
description: Queries and administers any Wildix PBX and the Wildix cloud services (WMS PBX API, x-bees, WDA history/insights, WIM voicebots, Auth) through their REST APIs, using a Company API Key and optionally a legacy PBX Bearer token. Use when the user asks to "query a Wildix PBX", "list users/extensions/call groups/trunks", "get the call history / CDR", "pull transcriptions or call summaries", "check a voicebot", "test a Wildix API route", "audit a PBX", "interroger un PBX Wildix", "récupérer l'historique d'appels", or names a *.wildixin.com domain.
---

# Wildix PBX — API operator

Operate any Wildix PBX and its cloud services through one bundled CLI, `scripts/wildix.py` (Python standard library only), and a split copy of the full Wildix API reference in `references/`. Respond in the user's language.

Run the CLI as `python3 <this skill's base directory>/scripts/wildix.py …`. Below, `wildix.py` stands for that full command.

## 1. Credentials — collect once per PBX

1. Run `wildix.py profiles`. If a profile for the requested PBX exists, `wildix.py use <name>` and go to step 2.
2. Otherwise ask the user (one question, all items together):
   - **PBX domain** — e.g. `client.wildixin.com` (a bare subdomain is accepted).
   - **Company API Key** — `wsk-v1-` followed by 93 characters. Main credential for x-bees, WDA, WIM, Auth and, when the key carries a `userExtension`, PBX-side requests.
   - **Optional legacy PBX Bearer token** — for the historical WMS API (`/api/v1/...`), typically a *Simple Token* application created in the PBX WMS. Basic credentials (`login:password`) are a last-resort alternative.
3. Register: `wildix.py login --pbx <domain> --key <key> [--token <token>] [--basic login:pass] [--name <alias>]`.
4. Verify with `wildix.py whoami`. It reports the key's name, company, scopes and expiry when the Auth service allows it, and tests PBX access with every stored credential. A 401 on `/api/v3/api-keys/self/data` alone does not prove the key is invalid.

Secret handling — non-negotiable:
- Never write keys or tokens into memory, notes, artifacts, documents, code files, commit messages or final answers. Never echo a full key; refer to it masked as the CLI does.
- Credentials live only in the CLI's state file (mode 0600, system temp directory). Offer `wildix.py logout` (or `logout --all`) when the work is done, and always when working on a customer's PBX.

## 2. Find the right route — never load whole reference files

Reference files are large (up to 1.5 MB). Do not `Read` them whole. Use the CLI:

- `wildix.py doc search "<regex>" [--api <ref>]` — searches the compact index of ~940 routes (`references/endpoints-index.md`).
- `wildix.py doc show <ref> <METHOD> <path>` — prints one route: parameters, body fields, response schema, scopes.
- `wildix.py doc schema <ref> <SchemaName>` — prints a component schema from the API's appendix.
- `wildix.py doc grep "<regex>" --api <ref>` — free-text search inside one API's reference.
- `wildix.py apis` — CLI aliases with base URLs and the reference files they cover.

Routing guide (CLI alias → reference file):

| Need | Alias | Reference |
|---|---|---|
| Users, extensions, groups, departments, devices, trunks, dialplans, call groups, phonebooks, sounds, voicemail, PBX call history | `pbx` | `pbx-api`, `cloud-pbx-server-api` |
| Live call control (list calls/devices, make call, transfer, hangup) | `pbx` with `/api/v2/call-control/...` | `cloud-pbx-server-api` |
| ACL groups and permissions | `wms` / `pbx` | `cloud-pbx-api`, `cloud-pbx-server-api` |
| Unified history of calls, chats, conferences; transcriptions | `wda` | `history-api` |
| AI insights: summaries, sentiment, tags, analytics | `wda` | `insights-api` |
| Real-time / event streams | `wda` | `stream-api` |
| x-caracal (WDA) | `wda` | `x-caracal-api` |
| Wilma AI platform: agents, copilot and sessions, tools, skills, workflows, chat, voice, traces, sandbox, secrets, artifacts, audit | `wilma` | `wilma-<service>-api` (e.g. `wilma-agents-api`, `wilma-copilot-api`) |
| Chat channels, messages, x-bees users, chatbots, Kite | `xbees` | `conversations-api`, `users-and-chatbots-api`, `kite-api`, `assistant-api` |
| Voicebots, voices, text-to-speech | `wim` | `voicebots-api` |
| Integrations, calendar, cache | `wim` | `integrations-api`, `calendar-api`, `cache-api` |
| Knowledge bases | `kb` | `knowledge-base-api` |
| Company API keys, tokens | `auth` | `auth-api-keys-service`, `auth-service` |
| SMS/WhatsApp/Messenger/eSIM | `classound` | `classound-api` |
| Webhook events and payloads | — | `references/webhooks.md` (small, can be read) |

Path rule for alias `pbx`: a path not starting with `/api/` gets `/api/v1` prepended (`/Colleagues/` → `/api/v1/Colleagues/`); paths starting with `/api/` are sent as is. A full `https://…` URL is also accepted, with `{pbx}` substituted.

Routes flagged ⚠️ in the index are **deprecated**: either removed from the published documentation (kept in each API's "Routes non publiées — deprecated" section, with their original description and removal date) or still published but marked `deprecated` by Wildix. They usually still work until their actual decommissioning: use them when the user needs them, but say they are deprecated and name the published replacement when `doc show` or the index offers one. If a deprecated route answers 404/410, it has been decommissioned — report it rather than retrying.

## 3. Execute

`wildix.py call <METHOD> <alias> <path> [-q key=value]… [-d '<json>' | -d @file.json] [-o file] [--all] [--auth key|token|basic|none] [--yes]`

**Always run `doc search` then `doc show` before the first call to a route.** Do not guess paths: near-miss paths (`/v2/voicebots` instead of `/v2/voicebots/bots`) and missing required parameters return a bare 404 with an empty body on the cloud services.

**Reads (GET, and documented read-only POST)** run immediately. Several read operations are POST with a JSON filter body (`QueryUserCalls`, `ListConversations`, `SearchKnowledgeBase`…); the CLI recognises them from `references/readonly-posts.json` and runs them without confirmation. On 401/403 the CLI automatically retries with the profile's other credential and reports which one succeeded (`[auth=…]`). Use `--all` for PBX v1 lists: it pages through `start`/`count` and returns every record. For other APIs, follow the pagination fields shown by `doc show` (cursor, `nextToken`, `limit`/`offset`…) explicitly.

**Writes (POST, PUT, PATCH, DELETE)** are blocked without `--yes`: the CLI prints a dry run (profile, URL, credential, body) and exits with code 3. Mandatory procedure:
1. Run the call without `--yes`, then show the user the exact request in plain words (what will change, on which PBX).
2. Wait for the user's explicit approval in the conversation. Silence or a general "go ahead" given earlier for another action does not count.
3. Re-run with `--yes`. For a batch, list every item, get one approval for the list, then run them.
4. For DELETE or anything irreversible on a customer PBX, read the current state first (GET) and save it to a file so it can be restored.

**Large responses** (over ~15,000 characters) are saved automatically to `./wildix-output/` and the CLI prints the file path plus a structural summary. Analyse those files with Python; do not page them into the conversation. Use `-o` to name the file, `--inline` only for small outputs.

## 4. Deliver

- Answer with what was found or changed, not the raw JSON. For lists and history, produce a table or a file (CSV/XLSX) when the user will reuse the data.
- State which PBX and which credential were used whenever several profiles exist.
- After work on a customer PBX, offer `wildix.py logout <name>`.

## 5. Field notes (verified on a live PBX)

- The Company API Key is sent as `Authorization: Bearer wsk-v1-…` and works on the PBX WMS API v1 (admin context) as well as on x-bees, WDA and WIM. The legacy token is only needed when the key is refused.
- With a Company API Key, WDA user-scoped routes (e.g. `POST /v2/history/user/calls`) require the `user` query parameter = the PBX user **id** (the `id` field from `GET pbx /Colleagues/`, not the extension). Resolve it first: `call GET pbx /Colleagues/ -q search=<extension> -q fields=id,extension,name`.
- PBX v1 lists return `{"type":"result","result":{"total":N,"records":[…]}}`; `--all` handles them.
- `GET /api/v2/call-control/*` routes require a `user` parameter as well. Since the 2026-11-10 revision the PBX API also documents `/call-control/*` again (under `/api/v1`).
- PBX routes show **Company API Key scope** when they accept a Company API Key; a route without it refuses the key (403) — use the legacy token there.

## 6. Troubleshooting

- **401 on every credential** — wrong key/token, or the key is expired. Ask the user to check the key in the admin portal.
- **403** — missing scope. Show the scopes `doc show` lists for the route and the scopes from `whoami`.
- **PBX API answers 401 with the Company API Key** — the key may lack a `userExtension` or the PBX-side scopes; try the legacy Bearer token.
- **Connection refused / proxy error before reaching Wildix** — the Claude environment's network allowlist blocks the domain. Tell the user their organization's admin must allow `*.wildixin.com`, `*.wildix.com`, `api.x-bees.com` and `broadcasts.x-hoppers.com`. Do not try to bypass it.
- **404 on a documented route** — check the path prefix rule above, the trailing slash (PBX v1 routes usually end with `/`), and whether the route is ⚠️ unpublished.

## Reference files

- `references/endpoints-index.md` — every route, one line each (searchable via `doc search`).
- `references/overview.md` — authentication schemes, publication status legend, changes since the previous revision (read it when the user asks what changed).
- `references/<api>.md` — full schemas per API (50 files, revision 2026-11-10) — access via `doc show` / `doc grep` / `doc schema` only.
- `references/webhooks.md` — webhook event types, VoiceBots/Chatbots webhook & SQS integration.
- `references/readonly-posts.json` — POST routes documented as reads (used by the CLI's write guard).
