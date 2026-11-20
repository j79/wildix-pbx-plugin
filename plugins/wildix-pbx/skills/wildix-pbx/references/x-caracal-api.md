## x-caracal API

_OpenAPI: WDA x-caracal service — version v2_

**Servers**

- `https://wda.wildix.com` — Production
- `https://wda-stable.wildix.com` — Stable
- `https://wda-stage.wildix.com` — Stage

### Other

#### `POST` `/v2/xcaracal/answered/breakdown/query`

Reads every call of the window on each request: nothing is pre-computed per user, agent, disconnect reason or talk time. Recommended to request it when the user asks for it, not on page open. Answered service calls grouped by service, by agent (the user as a member of one service), by user (across every service of the filter), by disconnect reason (outcome plus raw END reason) or by talk-time band. Every group carries its completed and transferred counts, wait and talk sums and the answering agent's two ring sums; percent of talk time is totalTalkMs over GetAnsweredSummary's totalTalkMs of the same filter. BY_TALK_TIME returns every band, zero-filled, using the talk ladder. Whole, not paginated; more than 1000 groups is rejected with 400.

- operationId: `GetAnsweredBreakdown`
- **Scopes**: `xcaracal:GetAnsweredBreakdown`, `xcaracal:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
- **Request body** (`application/json` — `GetAnsweredBreakdownRequestContent`) **(required)**
  - `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
    - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
      - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
    - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
    - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
      - _array of_ `string`
    - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
      - _array of_ `string`
    - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
      - _array of_ `OutcomeFilterValue`
    - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
      - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
      - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
      - _array of_ `number`
    - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
      - _array of_ `string`
    - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
    - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
  - `talkBandSeconds` — number — Width of each talk band, seconds; 20 when omitted. _(default=20; min=1; max=3600)_
  - `talkBandSteps` — number — Number of talk bands, the last one open-ended; 7 when omitted. _(default=7; min=1; max=60)_
  - `dimension` — string **(required)** — The grain of the answered breakdown. A user is the person (extension); an agent is that user as a member of one service (agentId names the service), so BY_AGENT is one row per user and service, BY_USER one row per user over every service of the filter. _(enum: `byService`, `byAgent`, `byUser`, `byDisconnectReason`, `byTalkTime`)_
- **Response 200** (`GetAnsweredBreakdownResponseContent`)
  - `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
  - `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
  - `dimension` — string **(required)** — The grain of the answered breakdown. A user is the person (extension); an agent is that user as a member of one service (agentId names the service), so BY_AGENT is one row per user and service, BY_USER one row per user over every service of the filter. _(enum: `byService`, `byAgent`, `byUser`, `byDisconnectReason`, `byTalkTime`)_
  - `total` — number **(required)** — The service calls the groups count together; a group's share is its calls divided by total. byAgent and byUser count only calls with an answering agent; a call whose answering agent was not recorded is in no group, so there total can be lower than completed + transferred.
  - `groups` — array **(required)**
    - _array of_ `BreakdownGroup`
      - `serviceId` — string — Set for BY_SERVICE and BY_AGENT: the service of this group.
      - `serviceName` — string — Set with serviceId: the service's stored name. Absent when the PBX sent none.
      - `agentId` — string — Set for BY_AGENT only: the answering agent's id - the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent on BY_USER, where one user spans several services.
      - `userName` — string — Set for BY_AGENT and BY_USER: a non-empty name the calls of the window carry for this user - deterministic, not necessarily the newest. Clients resolve the display name from the PBX user list by userExtension and use this as the fallback. A client without the PBX user list should know the name may belong to an earlier holder of the extension. Each call keeps the name it was stored with (ServiceCallRow.answeredByName). Absent when no call of the window carries a name.
      - `userExtension` — string — Set for BY_AGENT and BY_USER: the user's extension - the key of a BY_USER group.
      - `outcome` — string — Set for BY_DISCONNECT_REASON: the outcome value.
      - `disconnectReason` — string — Set for BY_DISCONNECT_REASON: the raw END reason beside the outcome (ServiceCallRow.disconnectReason); the calls of this group are filter.outcomes [outcome] with filter.disconnectReasons [disconnectReason].
      - `band` — TalkTimeBand — A talk-time band: bandNo from 1, fromSeconds inclusive, toSeconds inclusive and null on the open-ended last band.
        - `bandNo` — number **(required)** — Band number, from 1.
        - `fromSeconds` — number **(required)** — Lowest whole second of talk in the band. Band 1 starts at 1 but also holds the calls with under 1 s of talk.
        - `toSeconds` — number — Highest whole second of talk in the band. Absent on the last band.
      - `abandoned` — number — Set for BY_SERVICE on the unanswered breakdown: service calls in this group whose outcome is abandoned. abandoned + unanswered equals calls.
      - `unanswered` — number — Set for BY_SERVICE on the unanswered breakdown: service calls in this group whose outcome is unanswered.
      - `lost` — number — Set on the unanswered breakdowns (BY_SERVICE and BY_DISCONNECT_REASON): of this group's service calls, those that were the last of their phone call (no later service took the caller).
      - `lostAbandoned` — number — Set with lost: of this group's lost calls, those that were abandoned.
      - `lostUnanswered` — number — Set with lost: of this group's lost calls, those that ended unanswered.
      - `overflow` — number — Set with lost: of this group's service calls, those after which a later service call took the caller. lost + overflow = calls.
      - `calls` — number **(required)** — Service calls in this group; summed over the groups it is total.
      - `completed` — number — Set on the answered breakdowns: service calls in this group whose outcome is completed. completed + transferred equals calls.
      - `transferred` — number — Set on the answered breakdowns: service calls in this group whose outcome is transferred.
      - `avgWaitMs` — number — Average wait, ring included, milliseconds, over this group's service calls - this service's own wait, not the caller's across earlier services. Absent on an empty band. _(format=double)_
      - `maxWaitMs` — number — The longest wait, ring included, milliseconds. Absent on an empty band.
      - `totalWaitMs` — number — Sum of the group's waits in milliseconds; avgWaitMs times calls.
      - `avgTalkMs` — number — Average talk time, hold included, milliseconds. 0 on the unanswered breakdowns; absent on an empty band. _(format=double)_
      - `totalTalkMs` — number — Total talk time, hold included, milliseconds. 0 on the unanswered breakdowns.
      - `totalAnsweringAgentRingToAnswerMs` — number — Set on the answered breakdowns: sum of ServiceCallRow.answeringAgentRingToAnswerMs (from the first ring of the agent who answered to the answer, re-rings included), milliseconds, over the group's service calls that carry one.
      - `totalAnsweringAgentRingMs` — number — Set on the answered breakdowns: sum of ServiceCallRow.answeringAgentRingMs (how long the answering agent's phone actually rang), milliseconds, over the group's service calls that carry one.
      - `avgFinalPosition` — number — Set for BY_SERVICE: average queue position at answer on the answered breakdown; at exit over abandoned service calls only on the unanswered breakdown, the same basis as the unanswered summary's avgFinalPosition. _(format=double)_
  - `talkBandSeconds` — number — Echoed for BY_TALK_TIME: the talk band width applied, seconds.
  - `talkBandSteps` — number — Echoed for BY_TALK_TIME: the number of talk bands applied.
- Errors: `400`, `403`, `404`

#### `POST` `/v2/xcaracal/answered/service-level/query`

Cheap: closed days come from pre-computed daily rows. It reads the individual calls only for today and for yesterday until its daily rows exist (05:20 in the PBX's zone), and whenever the filter names extensions, outcomes, disconnect reasons, an hour range, days of week or a wait or talk band. Suitable for a page's first request. Cumulative service-level ladder over wait time for answered and transferred service calls: waitBandSteps bands of waitBandSeconds seconds, the last open-ended. Percentages are count / total, computed by the client.

- operationId: `GetAnsweredServiceLevel`
- **Scopes**: `xcaracal:GetAnsweredServiceLevel`, `xcaracal:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
- **Request body** (`application/json` — `GetAnsweredServiceLevelRequestContent`) **(required)**
  - `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
    - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
      - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
    - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
    - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
      - _array of_ `string`
    - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
      - _array of_ `string`
    - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
      - _array of_ `OutcomeFilterValue`
    - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
      - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
      - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
      - _array of_ `number`
    - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
      - _array of_ `string`
    - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
    - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
  - `waitBandSeconds` — number — Width of each wait band, seconds; 20 when omitted. _(default=20; min=5; max=120)_
  - `waitBandSteps` — number — Number of wait bands, the last one open-ended; 7 when omitted. _(default=7; min=1; max=60)_
- **Response 200** (`GetAnsweredServiceLevelResponseContent`)
  - `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
  - `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
  - `waitBandSeconds` — number **(required)** — The wait band width applied, seconds: the request's value, or 20.
  - `waitBandSteps` — number **(required)** — The number of wait bands applied: the request's value, or 7.
  - `total` — number **(required)** — Service calls in the base; the last band's cumulative count equals it.
  - `bands` — array **(required)**
    - _array of_ `ServiceLevelBand`
      - `withinSeconds` — number — The band's upper limit in seconds: count holds the calls whose wait was at most this. Absent on the open last band.
      - `count` — number **(required)** — Calls waiting at most withinSeconds: this band and all earlier ones.
      - `delta` — number **(required)** — Calls in this band only.
      - `lost` — number — Set on the abandoned-or-unanswered ladder: of count, the lost service calls (no later service took the caller), cumulative like count.
      - `lostDelta` — number — Set on the abandoned-or-unanswered ladder: of delta, the lost service calls.
      - `overflow` — number — Set on the abandoned-or-unanswered ladder: of count, the overflow service calls (a later service call then took the caller), cumulative like count. lost + overflow = count.
      - `overflowDelta` — number — Set on the abandoned-or-unanswered ladder: of delta, the overflow service calls. lostDelta + overflowDelta = delta.
- Errors: `400`, `403`, `404`

#### `POST` `/v2/xcaracal/answered/summary/query`

Cheap: closed days come from pre-computed daily rows. It reads the individual calls only for today and for yesterday until its daily rows exist (05:20 in the PBX's zone), and whenever the filter names extensions, outcomes, disconnect reasons, an hour range, days of week or a wait or talk band. Suitable for a page's first request. Answered-calls KPIs over complete service calls that were answered or transferred. Talk includes on-call hold.

- operationId: `GetAnsweredSummary`
- **Scopes**: `xcaracal:GetAnsweredSummary`, `xcaracal:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
- **Request body** (`application/json` — `GetAnsweredSummaryRequestContent`) **(required)**
  - `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
    - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
      - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
    - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
    - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
      - _array of_ `string`
    - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
      - _array of_ `string`
    - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
      - _array of_ `OutcomeFilterValue`
    - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
      - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
      - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
      - _array of_ `number`
    - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
      - _array of_ `string`
    - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
    - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- **Response 200** (`GetAnsweredSummaryResponseContent`)
  - `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
  - `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
  - `completed` — number **(required)** — Service calls an agent answered and kept.
  - `transferred` — number **(required)** — As counts.transferred. answered = completed + transferred.
  - `avgWaitMs` — number — Average wait, ring included, milliseconds, over completed and transferred service calls - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
  - `maxWaitMs` — number — The longest wait, ring included, milliseconds, over completed and transferred service calls. Absent when there is none.
  - `avgTalkMs` — number — Average talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none. _(format=double)_
  - `totalTalkMs` — number — Total talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none.
  - `sla` — SlaCounts **(required)** — Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds.
    - `thresholdSeconds` — number **(required)** — The default threshold that applied; on a by-service group, that service's own threshold.
    - `answeredWithin` — number **(required)** — Completed or transferred service calls whose wait, ring included, is at most the threshold that applied to their service - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs).
    - `eligible` — number **(required)** — The SLA denominator: counts.offered minus counts.unknown minus counts.shortAbandoned - the calls whose outcome could be determined, without the calls abandoned within 5 seconds, which gave the service no time to answer.
    - `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. Absent means one threshold applied to every service.
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
  - `unknown` — number **(required)** — As counts.unknown: service calls whose outcome could not be determined, left out of every figure above.
- Errors: `400`, `403`, `404`

#### `GET` `/v2/xcaracal/dashboards`

The dashboards of the user (live wallboards and reports): the predefined dashboards every user gets first, then the user's own, oldest first. A user's dashboards are private to them, within the company.

- operationId: `ListDashboards`
- **Scopes**: `xcaracal:ListDashboards`, `xcaracal:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
  - `user` (query) — string — The unique identifier of the user when a service, PBX or API-key token is used.
  - `kind` (query) — string — Only the dashboards of this kind; absent: every dashboard. _(enum: `live`, `report`)_
- **Response 200** (`ListDashboardsResponseContent`)
  - `dashboards` — array **(required)**
    - _array of_ `Dashboard`
      - `name` — string **(required)** _(minLen=1; maxLen=128)_
      - `kind` — string **(required)** _(enum: `live`, `report`)_
      - `blocks` — array **(required)** _(maxItems=100)_
        - _array of_ `DashboardBlock`
          - `id` — string **(required)** _(minLen=1; maxLen=64)_
          - `type` — string **(required)** _(enum: `chart`, `note`)_
          - `position` — DashboardBlockPosition **(required)** — Place of a block in the 12-column canvas grid.
            - `x` — number **(required)** _(min=0)_
            - `y` — number **(required)** _(min=0)_
            - `w` — number **(required)** _(min=1)_
            - `h` — number **(required)** _(min=1)_
          - `chartId` — string — The catalog chart shown by the block; required when type is chart. _(minLen=1; maxLen=128)_
          - `config` — DashboardBlockConfig — Data settings of a chart block (e.g. entity, queue), opaque to the service.
            - _map of_ `string`
          - `text` — string — The note; only with type note. It may be empty: a user can add a note before writing it. _(maxLen=2000)_
      - `id` — string **(required)** — Chosen by the client, unique among the dashboards of the user. _(pattern=^[A-Za-z0-9_-]+$; minLen=1; maxLen=64)_
      - `createdBy` — string **(required)** — Who created the dashboard: the id of the user, or "system" for a predefined dashboard.
      - `predefined` — boolean — True for a dashboard the service gives every user (createdBy "system"), e.g. the Live view's Main. It is listed before the user's own, and cannot be changed or deleted: a user customises a copy of it (a new dashboard saved under a new id).
      - `createdAt` — string **(required)** — When the dashboard was first saved, ISO 8601.
      - `updatedAt` — string **(required)** — When the dashboard was last saved, ISO 8601.
- Errors: `400`, `403`, `404`

#### `PUT` `/v2/xcaracal/dashboards/{id}`

Saves a dashboard of the user under the id the client chose: creates it when the id is new, otherwise replaces its name and blocks whole. createdAt is kept from the first save. The id of a predefined dashboard is rejected with 400. The kind of a dashboard is set when it is created and cannot change: a save with another kind is rejected with 400. A user can keep at most 50 dashboards of each kind: creating one more is rejected with 400.

- operationId: `PutDashboard`
- **Scopes**: `xcaracal:PutDashboard`
- **Parameters**
  - `id` (path) — string **(required)** — Chosen by the client, unique among the dashboards of the user. _(pattern=^[A-Za-z0-9_-]+$; minLen=1; maxLen=64)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
  - `user` (query) — string — The unique identifier of the user when a service, PBX or API-key token is used.
- **Request body** (`application/json` — `PutDashboardRequestContent`) **(required)**
  - `name` — string **(required)** _(minLen=1; maxLen=128)_
  - `kind` — string **(required)** _(enum: `live`, `report`)_
  - `blocks` — array **(required)** _(maxItems=100)_
    - _array of_ `DashboardBlock`
      - `id` — string **(required)** _(minLen=1; maxLen=64)_
      - `type` — string **(required)** _(enum: `chart`, `note`)_
      - `position` — DashboardBlockPosition **(required)** — Place of a block in the 12-column canvas grid.
        - `x` — number **(required)** _(min=0)_
        - `y` — number **(required)** _(min=0)_
        - `w` — number **(required)** _(min=1)_
        - `h` — number **(required)** _(min=1)_
      - `chartId` — string — The catalog chart shown by the block; required when type is chart. _(minLen=1; maxLen=128)_
      - `config` — DashboardBlockConfig — Data settings of a chart block (e.g. entity, queue), opaque to the service.
        - _map of_ `string`
      - `text` — string — The note; only with type note. It may be empty: a user can add a note before writing it. _(maxLen=2000)_
- **Response 200** (`PutDashboardResponseContent`)
  - `dashboard` — Dashboard **(required)**
    - `name` — string **(required)** _(minLen=1; maxLen=128)_
    - `kind` — string **(required)** _(enum: `live`, `report`)_
    - `blocks` — array **(required)** _(maxItems=100)_
      - _array of_ `DashboardBlock`
        - `id` — string **(required)** _(minLen=1; maxLen=64)_
        - `type` — string **(required)** _(enum: `chart`, `note`)_
        - `position` — DashboardBlockPosition **(required)** — Place of a block in the 12-column canvas grid.
          - `x` — number **(required)** _(min=0)_
          - `y` — number **(required)** _(min=0)_
          - `w` — number **(required)** _(min=1)_
          - `h` — number **(required)** _(min=1)_
        - `chartId` — string — The catalog chart shown by the block; required when type is chart. _(minLen=1; maxLen=128)_
        - `config` — DashboardBlockConfig — Data settings of a chart block (e.g. entity, queue), opaque to the service.
          - _map of_ `string`
        - `text` — string — The note; only with type note. It may be empty: a user can add a note before writing it. _(maxLen=2000)_
    - `id` — string **(required)** — Chosen by the client, unique among the dashboards of the user. _(pattern=^[A-Za-z0-9_-]+$; minLen=1; maxLen=64)_
    - `createdBy` — string **(required)** — Who created the dashboard: the id of the user, or "system" for a predefined dashboard.
    - `predefined` — boolean — True for a dashboard the service gives every user (createdBy "system"), e.g. the Live view's Main. It is listed before the user's own, and cannot be changed or deleted: a user customises a copy of it (a new dashboard saved under a new id).
    - `createdAt` — string **(required)** — When the dashboard was first saved, ISO 8601.
    - `updatedAt` — string **(required)** — When the dashboard was last saved, ISO 8601.
- Errors: `400`, `403`, `404`

#### `DELETE` `/v2/xcaracal/dashboards/{id}`

Deletes a dashboard of the user. Deleting a dashboard that does not exist succeeds; deleting a predefined dashboard is rejected with 400.

- operationId: `DeleteDashboard`
- **Scopes**: `xcaracal:DeleteDashboard`
- **Parameters**
  - `id` (path) — string **(required)** — Chosen by the client, unique among the dashboards of the user. _(pattern=^[A-Za-z0-9_-]+$; minLen=1; maxLen=64)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
  - `user` (query) — string — The unique identifier of the user when a service, PBX or API-key token is used.
- Errors: `400`, `403`, `404`

#### `POST` `/v2/xcaracal/distribution/by-period/query`

Cheap: closed days come from pre-computed daily rows. It reads the individual calls only for today and for yesterday until its daily rows exist (05:20 in the PBX's zone), and whenever the filter names extensions, outcomes, disconnect reasons, an hour range, days of week or a wait or talk band, or the hour granularity. Suitable for a page's first request. The metric block as a dense series of buckets cut in the request timezone; empty buckets carry zero counts. HOUR is the hour of the day (24 buckets) over the whole window.

- operationId: `GetDistributionByPeriod`
- **Scopes**: `xcaracal:GetDistributionByPeriod`, `xcaracal:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
- **Request body** (`application/json` — `GetDistributionByPeriodRequestContent`) **(required)**
  - `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
    - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
      - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
    - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
    - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
      - _array of_ `string`
    - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
      - _array of_ `string`
    - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
      - _array of_ `OutcomeFilterValue`
    - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
      - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
      - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
      - _array of_ `number`
    - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
      - _array of_ `string`
    - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
    - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
  - `granularity` — string **(required)** — Time-bucketing axis. WEEK is ISO-8601, Monday-start. HOUR and DAY_OF_WEEK are recurring buckets (hour of day, ISO day 1-7) over the whole window. _(enum: `hour`, `day`, `week`, `month`, `dayOfWeek`)_
- **Response 200** (`GetDistributionByPeriodResponseContent`)
  - `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
  - `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
  - `granularity` — string **(required)** — Time-bucketing axis. WEEK is ISO-8601, Monday-start. HOUR and DAY_OF_WEEK are recurring buckets (hour of day, ISO day 1-7) over the whole window. _(enum: `hour`, `day`, `week`, `month`, `dayOfWeek`)_
  - `buckets` — array **(required)**
    - _array of_ `PeriodBucket`
      - `bucketKey` — string **(required)** — HH:00 for HOUR, 1-7 for DAY_OF_WEEK (ISO, Monday = 1), YYYY-MM-DD for DAY, YYYY-Www for WEEK, YYYY-MM for MONTH.
      - `sortKey` — number **(required)** — Orders the series.
      - `bucketStart` — string — The bucket's local start. Set for DAY, WEEK and MONTH only. _(format=date-time)_
      - `metrics` — DistributionMetrics **(required)** — The distribution metric block. Every figure here is per service call: a call that went through several services counts in each service with that service's own wait and ringing; the caller's totals across services are on the call list (ServiceCallRow.totalQueueWaitMs and totalQueueRingMs). Waits are over complete service calls; talk is over answered and transferred service calls and includes on-call hold. The service's ring time is avgRingMs: how long agents were being rung for the caller, from the first ring to an answer or the end of the wait; the wait minus it is the time before the first agent was rung. avgAnsweringAgentRingToAnswerMs and avgAnsweringAgentRingMs describe the agent who answered. Averages are null when the base is empty.
        - `counts` — ServiceCallCounts **(required)** — Service call counts by outcome. Each service call (one phone call's stay in one service) counts on its own; a phone call that went through two services is two service calls. completed + transferred + abandoned + unanswered + unknown = offered: the calls whose outcome could not be determined stay in the total, as a count of their own, and are left out of every average and SLA figure. Averages are computed by the service; percentages are left to the client, because every count they need is returned.
          - `offered` — number **(required)** — Every service call in the window, all outcomes, unknown included.
          - `received` — number **(required)** — The service calls that ended in this service, offered - overflow = completed + transferred + lost + unknown. An unknown service call counts as received even when a later service took the caller. Not unique phone calls: a call answered in one service and transferred into another counts in both.
          - `completed` — number **(required)** — Service calls an agent answered and kept: the disconnect reason is neither TRANSFER nor FORWARD. Outcome value completed.
          - `transferred` — number **(required)** — Service calls an agent answered and then handed on (disconnect reason TRANSFER or FORWARD). answered = completed + transferred.
          - `abandoned` — number **(required)** — Service calls nobody answered whose disconnect reason is a hang-up: the caller hung up, or a rule took the call out of the queue.
          - `shortAbandoned` — number **(required)** — Of abandoned, the service calls whose wait, ring included, was at most 5 seconds. Included in abandoned, not an extra outcome.
          - `unanswered` — number **(required)** — Service calls nobody answered that ended for any other reason - a timeout, an empty queue, the caller leaving by a keypad option, a reason the classification does not name, or a hand-off before anyone answered (disconnect reason TRANSFER, FORWARD or PICKUP).
          - `unknown` — number **(required)** — Service calls whose outcome could not be determined from their events. Outcome value unknown; their events can be read with GetServiceCallEvents. Counted in offered and received; left out of every average and SLA figure, because their wait and outcome are not known.
          - `lost` — number **(required)** — Of the abandoned and unanswered service calls, those that were the last service call of their phone call: no later service took the caller. Summed over services it is the number of lost phone calls.
          - `lostAbandoned` — number **(required)** — Of lost, those whose last service call was abandoned: its disconnect reason is a hang-up (see abandoned).
          - `lostUnanswered` — number **(required)** — Of lost, those whose last service call ended unanswered (see unanswered). lostAbandoned + lostUnanswered = lost.
          - `overflow` — number **(required)** — abandoned + unanswered - lost: service calls nobody answered here after which the phone call had a later service call (in another service, or the same one entered again). The caller may have been served there.
        - `avgWaitMs` — number — Average wait, ring included, milliseconds, over the service calls whose outcome could be determined (every outcome; unknown left out) - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
        - `maxWaitMs` — number — The longest wait, ring included, milliseconds, over the same service calls as avgWaitMs. Absent when there is none.
        - `avgTalkMs` — number — Average talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none. _(format=double)_
        - `totalTalkMs` — number — Total talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none.
        - `avgRingMs` — number — The service's ring time. Average time from the first ring to any agent to the answer, or to the end of the service call when nobody answered, milliseconds, over the service calls whose outcome could be determined (answered, abandoned and unanswered together; unknown left out) that rang at least one agent; stretches with no agent ringing are included (ServiceCallRow.ringMs). Absent when there is none. _(format=double)_
        - `avgAnsweringAgentRingToAnswerMs` — number — Average time from the first ring of the agent who answered to the answer, milliseconds, over completed and transferred service calls that carry one; re-rings, and any stretches in between when that agent's phone was not ringing, are included (ServiceCallRow.answeringAgentRingToAnswerMs). Absent when there is none. _(format=double)_
        - `avgAnsweringAgentRingMs` — number — Average of how long the answering agent's phone actually rang, its rings added up, milliseconds, over completed and transferred service calls that carry one (ServiceCallRow.answeringAgentRingMs). Absent when there is none. _(format=double)_
        - `maxStartPosition` — number **(required)** — The highest place in line any caller had on joining, over every service call, unknown included. The highest place could be treated as the maximum number of callers waiting in the queue. With several services in the filter, the busiest service's figure.
        - `maxStartPositionAnswered` — number **(required)** — The deepest place in line on joining, over answered and transferred service calls.
        - `maxStartPositionAbandonedOrUnanswered` — number **(required)** — The deepest place in line on joining, over abandoned and unanswered service calls.
        - `maxFinalPositionAbandoned` — number **(required)** — The deepest place in line when the caller hung up while waiting (abandoned).
        - `maxFinalPositionUnanswered` — number **(required)** — The deepest place in line when the wait ended unanswered (see ServiceCallCounts.unanswered).
        - `sla` — SlaCounts **(required)** — Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds.
          - `thresholdSeconds` — number **(required)** — The default threshold that applied; on a by-service group, that service's own threshold.
          - `answeredWithin` — number **(required)** — Completed or transferred service calls whose wait, ring included, is at most the threshold that applied to their service - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs).
          - `eligible` — number **(required)** — The SLA denominator: counts.offered minus counts.unknown minus counts.shortAbandoned - the calls whose outcome could be determined, without the calls abandoned within 5 seconds, which gave the service no time to answer.
          - `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. Absent means one threshold applied to every service.
            - _array of_ `ServiceSlaSeconds`
              - _(nesting depth limit — see `ServiceSlaSeconds` in the Schemas appendix)_
- Errors: `400`, `403`, `404`

#### `POST` `/v2/xcaracal/distribution/by-service/query`

Cheap: closed days come from pre-computed daily rows. It reads the individual calls only for today and for yesterday until its daily rows exist (05:20 in the PBX's zone), and whenever the filter names extensions, outcomes, disconnect reasons, an hour range, days of week or a wait or talk band. Suitable for a page's first request. The metric block per service. Whole, not paginated; more than 1000 groups is rejected with 400.

- operationId: `GetDistributionByService`
- **Scopes**: `xcaracal:GetDistributionByService`, `xcaracal:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
- **Request body** (`application/json` — `GetDistributionByServiceRequestContent`) **(required)**
  - `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
    - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
      - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
    - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
    - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
      - _array of_ `string`
    - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
      - _array of_ `string`
    - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
      - _array of_ `OutcomeFilterValue`
    - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
      - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
      - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
      - _array of_ `number`
    - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
      - _array of_ `string`
    - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
    - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- **Response 200** (`GetDistributionByServiceResponseContent`)
  - `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
  - `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
  - `groups` — array **(required)**
    - _array of_ `DistributionServiceGroup`
      - `serviceId` — string **(required)** — The service of this group.
      - `serviceName` — string — The service's name as stored with its calls. Absent when the PBX sent none.
      - `metrics` — DistributionMetrics **(required)** — The distribution metric block. Every figure here is per service call: a call that went through several services counts in each service with that service's own wait and ringing; the caller's totals across services are on the call list (ServiceCallRow.totalQueueWaitMs and totalQueueRingMs). Waits are over complete service calls; talk is over answered and transferred service calls and includes on-call hold. The service's ring time is avgRingMs: how long agents were being rung for the caller, from the first ring to an answer or the end of the wait; the wait minus it is the time before the first agent was rung. avgAnsweringAgentRingToAnswerMs and avgAnsweringAgentRingMs describe the agent who answered. Averages are null when the base is empty.
        - `counts` — ServiceCallCounts **(required)** — Service call counts by outcome. Each service call (one phone call's stay in one service) counts on its own; a phone call that went through two services is two service calls. completed + transferred + abandoned + unanswered + unknown = offered: the calls whose outcome could not be determined stay in the total, as a count of their own, and are left out of every average and SLA figure. Averages are computed by the service; percentages are left to the client, because every count they need is returned.
          - `offered` — number **(required)** — Every service call in the window, all outcomes, unknown included.
          - `received` — number **(required)** — The service calls that ended in this service, offered - overflow = completed + transferred + lost + unknown. An unknown service call counts as received even when a later service took the caller. Not unique phone calls: a call answered in one service and transferred into another counts in both.
          - `completed` — number **(required)** — Service calls an agent answered and kept: the disconnect reason is neither TRANSFER nor FORWARD. Outcome value completed.
          - `transferred` — number **(required)** — Service calls an agent answered and then handed on (disconnect reason TRANSFER or FORWARD). answered = completed + transferred.
          - `abandoned` — number **(required)** — Service calls nobody answered whose disconnect reason is a hang-up: the caller hung up, or a rule took the call out of the queue.
          - `shortAbandoned` — number **(required)** — Of abandoned, the service calls whose wait, ring included, was at most 5 seconds. Included in abandoned, not an extra outcome.
          - `unanswered` — number **(required)** — Service calls nobody answered that ended for any other reason - a timeout, an empty queue, the caller leaving by a keypad option, a reason the classification does not name, or a hand-off before anyone answered (disconnect reason TRANSFER, FORWARD or PICKUP).
          - `unknown` — number **(required)** — Service calls whose outcome could not be determined from their events. Outcome value unknown; their events can be read with GetServiceCallEvents. Counted in offered and received; left out of every average and SLA figure, because their wait and outcome are not known.
          - `lost` — number **(required)** — Of the abandoned and unanswered service calls, those that were the last service call of their phone call: no later service took the caller. Summed over services it is the number of lost phone calls.
          - `lostAbandoned` — number **(required)** — Of lost, those whose last service call was abandoned: its disconnect reason is a hang-up (see abandoned).
          - `lostUnanswered` — number **(required)** — Of lost, those whose last service call ended unanswered (see unanswered). lostAbandoned + lostUnanswered = lost.
          - `overflow` — number **(required)** — abandoned + unanswered - lost: service calls nobody answered here after which the phone call had a later service call (in another service, or the same one entered again). The caller may have been served there.
        - `avgWaitMs` — number — Average wait, ring included, milliseconds, over the service calls whose outcome could be determined (every outcome; unknown left out) - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
        - `maxWaitMs` — number — The longest wait, ring included, milliseconds, over the same service calls as avgWaitMs. Absent when there is none.
        - `avgTalkMs` — number — Average talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none. _(format=double)_
        - `totalTalkMs` — number — Total talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none.
        - `avgRingMs` — number — The service's ring time. Average time from the first ring to any agent to the answer, or to the end of the service call when nobody answered, milliseconds, over the service calls whose outcome could be determined (answered, abandoned and unanswered together; unknown left out) that rang at least one agent; stretches with no agent ringing are included (ServiceCallRow.ringMs). Absent when there is none. _(format=double)_
        - `avgAnsweringAgentRingToAnswerMs` — number — Average time from the first ring of the agent who answered to the answer, milliseconds, over completed and transferred service calls that carry one; re-rings, and any stretches in between when that agent's phone was not ringing, are included (ServiceCallRow.answeringAgentRingToAnswerMs). Absent when there is none. _(format=double)_
        - `avgAnsweringAgentRingMs` — number — Average of how long the answering agent's phone actually rang, its rings added up, milliseconds, over completed and transferred service calls that carry one (ServiceCallRow.answeringAgentRingMs). Absent when there is none. _(format=double)_
        - `maxStartPosition` — number **(required)** — The highest place in line any caller had on joining, over every service call, unknown included. The highest place could be treated as the maximum number of callers waiting in the queue. With several services in the filter, the busiest service's figure.
        - `maxStartPositionAnswered` — number **(required)** — The deepest place in line on joining, over answered and transferred service calls.
        - `maxStartPositionAbandonedOrUnanswered` — number **(required)** — The deepest place in line on joining, over abandoned and unanswered service calls.
        - `maxFinalPositionAbandoned` — number **(required)** — The deepest place in line when the caller hung up while waiting (abandoned).
        - `maxFinalPositionUnanswered` — number **(required)** — The deepest place in line when the wait ended unanswered (see ServiceCallCounts.unanswered).
        - `sla` — SlaCounts **(required)** — Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds.
          - `thresholdSeconds` — number **(required)** — The default threshold that applied; on a by-service group, that service's own threshold.
          - `answeredWithin` — number **(required)** — Completed or transferred service calls whose wait, ring included, is at most the threshold that applied to their service - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs).
          - `eligible` — number **(required)** — The SLA denominator: counts.offered minus counts.unknown minus counts.shortAbandoned - the calls whose outcome could be determined, without the calls abandoned within 5 seconds, which gave the service no time to answer.
          - `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. Absent means one threshold applied to every service.
            - _array of_ `ServiceSlaSeconds`
              - _(nesting depth limit — see `ServiceSlaSeconds` in the Schemas appendix)_
- Errors: `400`, `403`, `404`

#### `POST` `/v2/xcaracal/distribution/summary/query`

Cheap: closed days come from pre-computed daily rows. It reads the individual calls only for today and for yesterday until its daily rows exist (05:20 in the PBX's zone), and whenever the filter names extensions, outcomes, disconnect reasons, an hour range, days of week or a wait or talk band. Suitable for a page's first request. One metric block over every service call in the filter.

- operationId: `GetDistributionSummary`
- **Scopes**: `xcaracal:GetDistributionSummary`, `xcaracal:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
- **Request body** (`application/json` — `GetDistributionSummaryRequestContent`) **(required)**
  - `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
    - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
      - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
    - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
    - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
      - _array of_ `string`
    - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
      - _array of_ `string`
    - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
      - _array of_ `OutcomeFilterValue`
    - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
      - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
      - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
      - _array of_ `number`
    - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
      - _array of_ `string`
    - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
    - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- **Response 200** (`GetDistributionSummaryResponseContent`)
  - `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
  - `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
  - `metrics` — DistributionMetrics **(required)** — The distribution metric block. Every figure here is per service call: a call that went through several services counts in each service with that service's own wait and ringing; the caller's totals across services are on the call list (ServiceCallRow.totalQueueWaitMs and totalQueueRingMs). Waits are over complete service calls; talk is over answered and transferred service calls and includes on-call hold. The service's ring time is avgRingMs: how long agents were being rung for the caller, from the first ring to an answer or the end of the wait; the wait minus it is the time before the first agent was rung. avgAnsweringAgentRingToAnswerMs and avgAnsweringAgentRingMs describe the agent who answered. Averages are null when the base is empty.
    - `counts` — ServiceCallCounts **(required)** — Service call counts by outcome. Each service call (one phone call's stay in one service) counts on its own; a phone call that went through two services is two service calls. completed + transferred + abandoned + unanswered + unknown = offered: the calls whose outcome could not be determined stay in the total, as a count of their own, and are left out of every average and SLA figure. Averages are computed by the service; percentages are left to the client, because every count they need is returned.
      - `offered` — number **(required)** — Every service call in the window, all outcomes, unknown included.
      - `received` — number **(required)** — The service calls that ended in this service, offered - overflow = completed + transferred + lost + unknown. An unknown service call counts as received even when a later service took the caller. Not unique phone calls: a call answered in one service and transferred into another counts in both.
      - `completed` — number **(required)** — Service calls an agent answered and kept: the disconnect reason is neither TRANSFER nor FORWARD. Outcome value completed.
      - `transferred` — number **(required)** — Service calls an agent answered and then handed on (disconnect reason TRANSFER or FORWARD). answered = completed + transferred.
      - `abandoned` — number **(required)** — Service calls nobody answered whose disconnect reason is a hang-up: the caller hung up, or a rule took the call out of the queue.
      - `shortAbandoned` — number **(required)** — Of abandoned, the service calls whose wait, ring included, was at most 5 seconds. Included in abandoned, not an extra outcome.
      - `unanswered` — number **(required)** — Service calls nobody answered that ended for any other reason - a timeout, an empty queue, the caller leaving by a keypad option, a reason the classification does not name, or a hand-off before anyone answered (disconnect reason TRANSFER, FORWARD or PICKUP).
      - `unknown` — number **(required)** — Service calls whose outcome could not be determined from their events. Outcome value unknown; their events can be read with GetServiceCallEvents. Counted in offered and received; left out of every average and SLA figure, because their wait and outcome are not known.
      - `lost` — number **(required)** — Of the abandoned and unanswered service calls, those that were the last service call of their phone call: no later service took the caller. Summed over services it is the number of lost phone calls.
      - `lostAbandoned` — number **(required)** — Of lost, those whose last service call was abandoned: its disconnect reason is a hang-up (see abandoned).
      - `lostUnanswered` — number **(required)** — Of lost, those whose last service call ended unanswered (see unanswered). lostAbandoned + lostUnanswered = lost.
      - `overflow` — number **(required)** — abandoned + unanswered - lost: service calls nobody answered here after which the phone call had a later service call (in another service, or the same one entered again). The caller may have been served there.
    - `avgWaitMs` — number — Average wait, ring included, milliseconds, over the service calls whose outcome could be determined (every outcome; unknown left out) - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
    - `maxWaitMs` — number — The longest wait, ring included, milliseconds, over the same service calls as avgWaitMs. Absent when there is none.
    - `avgTalkMs` — number — Average talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none. _(format=double)_
    - `totalTalkMs` — number — Total talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none.
    - `avgRingMs` — number — The service's ring time. Average time from the first ring to any agent to the answer, or to the end of the service call when nobody answered, milliseconds, over the service calls whose outcome could be determined (answered, abandoned and unanswered together; unknown left out) that rang at least one agent; stretches with no agent ringing are included (ServiceCallRow.ringMs). Absent when there is none. _(format=double)_
    - `avgAnsweringAgentRingToAnswerMs` — number — Average time from the first ring of the agent who answered to the answer, milliseconds, over completed and transferred service calls that carry one; re-rings, and any stretches in between when that agent's phone was not ringing, are included (ServiceCallRow.answeringAgentRingToAnswerMs). Absent when there is none. _(format=double)_
    - `avgAnsweringAgentRingMs` — number — Average of how long the answering agent's phone actually rang, its rings added up, milliseconds, over completed and transferred service calls that carry one (ServiceCallRow.answeringAgentRingMs). Absent when there is none. _(format=double)_
    - `maxStartPosition` — number **(required)** — The highest place in line any caller had on joining, over every service call, unknown included. The highest place could be treated as the maximum number of callers waiting in the queue. With several services in the filter, the busiest service's figure.
    - `maxStartPositionAnswered` — number **(required)** — The deepest place in line on joining, over answered and transferred service calls.
    - `maxStartPositionAbandonedOrUnanswered` — number **(required)** — The deepest place in line on joining, over abandoned and unanswered service calls.
    - `maxFinalPositionAbandoned` — number **(required)** — The deepest place in line when the caller hung up while waiting (abandoned).
    - `maxFinalPositionUnanswered` — number **(required)** — The deepest place in line when the wait ended unanswered (see ServiceCallCounts.unanswered).
    - `sla` — SlaCounts **(required)** — Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds.
      - `thresholdSeconds` — number **(required)** — The default threshold that applied; on a by-service group, that service's own threshold.
      - `answeredWithin` — number **(required)** — Completed or transferred service calls whose wait, ring included, is at most the threshold that applied to their service - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs).
      - `eligible` — number **(required)** — The SLA denominator: counts.offered minus counts.unknown minus counts.shortAbandoned - the calls whose outcome could be determined, without the calls abandoned within 5 seconds, which gave the service no time to answer.
      - `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. Absent means one threshold applied to every service.
        - _array of_ `ServiceSlaSeconds`
          - `serviceId` — string **(required)** — The service this threshold applies to.
          - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- Errors: `400`, `403`, `404`

#### `POST` `/v2/xcaracal/services/calls/query`

Cheap: one page of calls, read through an index, however long the window. Pages are requested one at a time. The call list: one row per service call (one phone call's stay in one service), newest first, keyset-paginated; callId lists every service call of one phone call. The calls whose outcome could not be determined are listed with outcome unknown, as they are counted in offered; narrow with the outcomes filter. A value that matches few calls can read the whole window before a page fills.

- operationId: `QueryServiceCalls`
- **Scopes**: `xcaracal:QueryServiceCalls`, `xcaracal:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
- **Request body** (`application/json` — `QueryServiceCallsRequestContent`) **(required)**
  - `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
    - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
      - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
    - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
    - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
      - _array of_ `string`
    - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
      - _array of_ `string`
    - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
      - _array of_ `OutcomeFilterValue`
    - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
      - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
      - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
      - _array of_ `number`
    - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
      - _array of_ `string`
    - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
    - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
  - `cursor` — string — The previous page's nextCursor, passed back unchanged; omit it, or send it empty, for the first page. _(maxLen=2048)_
  - `limit` — number — Rows per page, 1 to 200; 50 when omitted. _(default=50; min=1; max=200)_
  - `callId` — string — Only the service calls of this phone call (its callId, the session id shared by every service call of the phone call), so a drill-down can show every service call of a call that overflowed from one service to another. The window and the other filter members still apply; a key lookup, however long the window.
- **Response 200** (`QueryServiceCallsResponseContent`)
  - `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
  - `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
  - `items` — array **(required)**
    - _array of_ `ServiceCallRow`
      - `callId` — string **(required)** — The phone call's id (its session id), shared by every service call of the call. Not this row's own id: with flowIndex and serviceId it identifies the row.
      - `flowIndex` — number **(required)** — The PBX's step number of this service call within the phone call. Not a count of service calls and not guaranteed to be consecutive (see serviceCallsCount). With callId and serviceId it identifies the row.
      - `serviceId` — string **(required)** — The service of this service call.
      - `serviceName` — string — The service's name as stored with the call. Absent when the PBX sent none.
      - `enteredAt` — string **(required)** — When the caller joined the service's queue. _(format=date-time)_
      - `answeredAt` — string — When an agent answered. Absent when nobody did. _(format=date-time)_
      - `endedAt` — string **(required)** — When this service call ended: the caller left the service's queue, or the answered call ended. _(format=date-time)_
      - `waitMs` — number **(required)** — Wait from entering the queue to the answer or the exit, milliseconds; the ring is inside it.
      - `ringMs` — number — The ringing in this service call, milliseconds: from the first ring to any agent to the answer, or to the end of the service call when nobody answered; stretches with no phone ringing are included. It is inside waitMs; waitMs minus ringMs is the time before the first agent was rung. Absent when no agent was rung.
      - `answeringAgentRingToAnswerMs` — number — In this service call, the time from the first ring of the agent who answered to the answer, milliseconds; re-rings, and any stretches in between when that agent's phone was not ringing, are included. Absent when nobody answered, or when no ring was recorded for that agent.
      - `answeringAgentRingMs` — number — In this service call, how long the answering agent's phone actually rang, milliseconds: each ring of that agent lasts until the next event that names that agent (its cancel or the answer) or names no agent at all, and the rings are added up. Absent when nobody answered, or when no ring was recorded for that agent.
      - `talkMs` — number **(required)** — Talk time from the answer to the end, hold included, milliseconds; 0 when nobody answered.
      - `durationMs` — number **(required)** — The whole span of this service call, milliseconds: from joining the queue to the service call's end, waitMs plus talkMs (the whole unit, as the stream API means duration; the talk time alone is talkMs).
      - `answered` — boolean **(required)** — True exactly when an agent of the service answered: outcome completed or transferred; an unknown row can have answered true.
      - `answeredByAgentId` — string — The agent who answered - the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent when nobody answered.
      - `answeredByName` — string — The answering user's name as stored with the call (the name it had then). Absent when nobody answered.
      - `answeredByExtension` — string — The answering user's extension. Absent when nobody answered.
      - `agentsRung` — number **(required)** — How many different agents the service rang during this service call, whether or not they picked up.
      - `startPosition` — number — The caller's place in line on joining the service's queue, as the PBX sends it (1 = first in line). Absent when the PBX did not send it.
      - `finalPosition` — number — The caller's place in line when the wait ended (answer, hang-up or exit), as the PBX sends it. Absent when the PBX did not send it.
      - `outcome` — string **(required)** — completed | transferred | abandoned | unanswered | unknown. An open vocabulary: a client must tolerate a value not listed here. unknown: the outcome could not be determined from the service call's events (see ServiceCallCounts.unknown); such a row is outside every average and every SLA figure.
      - `disconnectReason` — string — The reason the call left the service, as the PBX gave it on the END event, upper-cased: HANGUP, TRANSFER, FORWARD, PICKUP, TIMEOUT, EMPTY, EXITWITHKEY, COMPATIBILITY, UNKNOWN. Absent when the END carried none. filter.disconnectReasons selects by it. The outcome follows the answer, not the reason: answered then TRANSFER or FORWARD is transferred; nobody answered is abandoned for HANGUP and unanswered for every other reason, a hand-off (TRANSFER, FORWARD, PICKUP) included.
      - `callerPhone` — string — The caller's number as the PBX received it. Absent when the PBX sent none.
      - `callerName` — string — The caller's name as the PBX received it. Absent when the PBX sent none.
      - `lost` — boolean — Set on abandoned and unanswered rows only: true when this was the last service call of its phone call (lost), false when a later service call then took the caller (overflow). Absent on every other row.
      - `totalQueueWaitMs` — number **(required)** — The caller's total queue wait: the sum of waitMs over every service call of this phone call. The same value on every row of the call. It covers the waiting time inside the services' queues only - not the IVR before the first service or between services. Computed when the page is read, so it grows if a later service call arrives. It includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
      - `totalQueueRingMs` — number **(required)** — The caller's total ringing: the sum of ringMs over every service call of this phone call. The same value on every row of the call; a service call without ringMs adds 0. Computed when the page is read, so it grows if a later service call arrives. It includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
      - `serviceCallsCount` — number **(required)** — How many service calls this phone call has: 1 when it stayed in one service; the same service entered twice counts 2. Like totalQueueWaitMs and totalQueueRingMs, it includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
  - `nextCursor` — string — Cursor for the next page; absent on the last page.
- Errors: `400`, `403`, `404`

#### `GET` `/v2/xcaracal/services/calls/{callId}/flows/{flowIndex}/events`

Cheap: one call, looked up by key. One service call in full: its call-list row and its raw lifecycle events (INIT, RING, CANCEL, ANSWER, END) in time order, whole, never paged (a service call reaches the database as one record, so its events always fit one response). An event here is one entry of the stream API's actions list per agent it concerns: an action without an agent is one event, an action naming several agents is one event per agent, and the events of one action share its time; the stream's own 'service call event' is the whole record. 404 when the service call does not exist for the company. callId is the phone call's id, shared by all its service calls; flowIndex picks the stay; serviceId disambiguates the rare case of one flow index entering two services.

- operationId: `GetServiceCallEvents`
- **Scopes**: `xcaracal:GetServiceCallEvents`, `xcaracal:read`
- **Parameters**
  - `callId` (path) — string **(required)** — The phone call's id, as in ServiceCallRow.callId.
  - `flowIndex` (path) — number **(required)** — The service call's flowIndex, as in ServiceCallRow.flowIndex. _(min=0)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
  - `serviceId` (query) — string — The service of the service call, needed only when one flowIndex entered two services. Absent: the service call that entered first.
- **Response 200** (`GetServiceCallEventsResponseContent`)
  - `call` — ServiceCallRow **(required)** — One service call: one phone call's stay in one service (one flow of the call in that service). Ring is nested inside wait; talk includes hold. callerPhone and callerName can be absent; absent does not mean the call had no caller. A call that went from one service to another is several service calls sharing callId (one per service); every report counts each of them on its own.
    - `callId` — string **(required)** — The phone call's id (its session id), shared by every service call of the call. Not this row's own id: with flowIndex and serviceId it identifies the row.
    - `flowIndex` — number **(required)** — The PBX's step number of this service call within the phone call. Not a count of service calls and not guaranteed to be consecutive (see serviceCallsCount). With callId and serviceId it identifies the row.
    - `serviceId` — string **(required)** — The service of this service call.
    - `serviceName` — string — The service's name as stored with the call. Absent when the PBX sent none.
    - `enteredAt` — string **(required)** — When the caller joined the service's queue. _(format=date-time)_
    - `answeredAt` — string — When an agent answered. Absent when nobody did. _(format=date-time)_
    - `endedAt` — string **(required)** — When this service call ended: the caller left the service's queue, or the answered call ended. _(format=date-time)_
    - `waitMs` — number **(required)** — Wait from entering the queue to the answer or the exit, milliseconds; the ring is inside it.
    - `ringMs` — number — The ringing in this service call, milliseconds: from the first ring to any agent to the answer, or to the end of the service call when nobody answered; stretches with no phone ringing are included. It is inside waitMs; waitMs minus ringMs is the time before the first agent was rung. Absent when no agent was rung.
    - `answeringAgentRingToAnswerMs` — number — In this service call, the time from the first ring of the agent who answered to the answer, milliseconds; re-rings, and any stretches in between when that agent's phone was not ringing, are included. Absent when nobody answered, or when no ring was recorded for that agent.
    - `answeringAgentRingMs` — number — In this service call, how long the answering agent's phone actually rang, milliseconds: each ring of that agent lasts until the next event that names that agent (its cancel or the answer) or names no agent at all, and the rings are added up. Absent when nobody answered, or when no ring was recorded for that agent.
    - `talkMs` — number **(required)** — Talk time from the answer to the end, hold included, milliseconds; 0 when nobody answered.
    - `durationMs` — number **(required)** — The whole span of this service call, milliseconds: from joining the queue to the service call's end, waitMs plus talkMs (the whole unit, as the stream API means duration; the talk time alone is talkMs).
    - `answered` — boolean **(required)** — True exactly when an agent of the service answered: outcome completed or transferred; an unknown row can have answered true.
    - `answeredByAgentId` — string — The agent who answered - the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent when nobody answered.
    - `answeredByName` — string — The answering user's name as stored with the call (the name it had then). Absent when nobody answered.
    - `answeredByExtension` — string — The answering user's extension. Absent when nobody answered.
    - `agentsRung` — number **(required)** — How many different agents the service rang during this service call, whether or not they picked up.
    - `startPosition` — number — The caller's place in line on joining the service's queue, as the PBX sends it (1 = first in line). Absent when the PBX did not send it.
    - `finalPosition` — number — The caller's place in line when the wait ended (answer, hang-up or exit), as the PBX sends it. Absent when the PBX did not send it.
    - `outcome` — string **(required)** — completed | transferred | abandoned | unanswered | unknown. An open vocabulary: a client must tolerate a value not listed here. unknown: the outcome could not be determined from the service call's events (see ServiceCallCounts.unknown); such a row is outside every average and every SLA figure.
    - `disconnectReason` — string — The reason the call left the service, as the PBX gave it on the END event, upper-cased: HANGUP, TRANSFER, FORWARD, PICKUP, TIMEOUT, EMPTY, EXITWITHKEY, COMPATIBILITY, UNKNOWN. Absent when the END carried none. filter.disconnectReasons selects by it. The outcome follows the answer, not the reason: answered then TRANSFER or FORWARD is transferred; nobody answered is abandoned for HANGUP and unanswered for every other reason, a hand-off (TRANSFER, FORWARD, PICKUP) included.
    - `callerPhone` — string — The caller's number as the PBX received it. Absent when the PBX sent none.
    - `callerName` — string — The caller's name as the PBX received it. Absent when the PBX sent none.
    - `lost` — boolean — Set on abandoned and unanswered rows only: true when this was the last service call of its phone call (lost), false when a later service call then took the caller (overflow). Absent on every other row.
    - `totalQueueWaitMs` — number **(required)** — The caller's total queue wait: the sum of waitMs over every service call of this phone call. The same value on every row of the call. It covers the waiting time inside the services' queues only - not the IVR before the first service or between services. Computed when the page is read, so it grows if a later service call arrives. It includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
    - `totalQueueRingMs` — number **(required)** — The caller's total ringing: the sum of ringMs over every service call of this phone call. The same value on every row of the call; a service call without ringMs adds 0. Computed when the page is read, so it grows if a later service call arrives. It includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
    - `serviceCallsCount` — number **(required)** — How many service calls this phone call has: 1 when it stayed in one service; the same service entered twice counts 2. Like totalQueueWaitMs and totalQueueRingMs, it includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
  - `events` — array **(required)** — Its lifecycle events in time order, whole. The time to the next event is measured to the next action, not to a sibling event of the same action (one action naming several agents gives several events with one time); for a RING, to that agent's next event or to the next event without an agent.
    - _array of_ `ServiceCallEvent`
      - `time` — string **(required)** — When the PBX recorded this event. _(format=date-time)_
      - `action` — string **(required)** — INIT | RING | CANCEL | ANSWER | END, upper-cased.
      - `reason` — string — The raw reason the PBX gave for this event, upper-cased (END and CANCEL carry one); on END it is the row's disconnectReason. Absent when there is none.
      - `agentId` — string — The agent this event concerns - rung, or answering: the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent on events without an agent.
      - `userName` — string — That user's name as stored with the event. Absent on events without an agent.
      - `userExtension` — string — That user's extension. Absent on events without an agent.
      - `queuePosition` — number — The caller's place in line at this event, as the PBX sends it. Absent when the PBX did not send it.
- Errors: `400`, `403`, `404`

#### `POST` `/v2/xcaracal/unanswered/breakdown/query`

Reads every call of the window on each request: nothing is pre-computed per service or disconnect reason. Recommended to request it when the user asks for it, not on page open. Unanswered service calls grouped by service or by disconnect reason (outcome plus raw END reason). Whole, not paginated; more than 1000 groups is rejected with 400.

- operationId: `GetUnansweredBreakdown`
- **Scopes**: `xcaracal:GetUnansweredBreakdown`, `xcaracal:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
- **Request body** (`application/json` — `GetUnansweredBreakdownRequestContent`) **(required)**
  - `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
    - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
      - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
    - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
    - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
      - _array of_ `string`
    - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
      - _array of_ `string`
    - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
      - _array of_ `OutcomeFilterValue`
    - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
      - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
      - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
      - _array of_ `number`
    - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
      - _array of_ `string`
    - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
    - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
  - `dimension` — string **(required)** — The grain of the unanswered breakdown: one group per service, or one group per outcome and raw END reason. _(enum: `byService`, `byDisconnectReason`)_
- **Response 200** (`GetUnansweredBreakdownResponseContent`)
  - `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
  - `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
  - `dimension` — string **(required)** — The grain of the unanswered breakdown: one group per service, or one group per outcome and raw END reason. _(enum: `byService`, `byDisconnectReason`)_
  - `total` — number **(required)** — The service calls the groups count together; a group's share is its calls divided by total.
  - `groups` — array **(required)**
    - _array of_ `BreakdownGroup`
      - `serviceId` — string — Set for BY_SERVICE and BY_AGENT: the service of this group.
      - `serviceName` — string — Set with serviceId: the service's stored name. Absent when the PBX sent none.
      - `agentId` — string — Set for BY_AGENT only: the answering agent's id - the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent on BY_USER, where one user spans several services.
      - `userName` — string — Set for BY_AGENT and BY_USER: a non-empty name the calls of the window carry for this user - deterministic, not necessarily the newest. Clients resolve the display name from the PBX user list by userExtension and use this as the fallback. A client without the PBX user list should know the name may belong to an earlier holder of the extension. Each call keeps the name it was stored with (ServiceCallRow.answeredByName). Absent when no call of the window carries a name.
      - `userExtension` — string — Set for BY_AGENT and BY_USER: the user's extension - the key of a BY_USER group.
      - `outcome` — string — Set for BY_DISCONNECT_REASON: the outcome value.
      - `disconnectReason` — string — Set for BY_DISCONNECT_REASON: the raw END reason beside the outcome (ServiceCallRow.disconnectReason); the calls of this group are filter.outcomes [outcome] with filter.disconnectReasons [disconnectReason].
      - `band` — TalkTimeBand — A talk-time band: bandNo from 1, fromSeconds inclusive, toSeconds inclusive and null on the open-ended last band.
        - `bandNo` — number **(required)** — Band number, from 1.
        - `fromSeconds` — number **(required)** — Lowest whole second of talk in the band. Band 1 starts at 1 but also holds the calls with under 1 s of talk.
        - `toSeconds` — number — Highest whole second of talk in the band. Absent on the last band.
      - `abandoned` — number — Set for BY_SERVICE on the unanswered breakdown: service calls in this group whose outcome is abandoned. abandoned + unanswered equals calls.
      - `unanswered` — number — Set for BY_SERVICE on the unanswered breakdown: service calls in this group whose outcome is unanswered.
      - `lost` — number — Set on the unanswered breakdowns (BY_SERVICE and BY_DISCONNECT_REASON): of this group's service calls, those that were the last of their phone call (no later service took the caller).
      - `lostAbandoned` — number — Set with lost: of this group's lost calls, those that were abandoned.
      - `lostUnanswered` — number — Set with lost: of this group's lost calls, those that ended unanswered.
      - `overflow` — number — Set with lost: of this group's service calls, those after which a later service call took the caller. lost + overflow = calls.
      - `calls` — number **(required)** — Service calls in this group; summed over the groups it is total.
      - `completed` — number — Set on the answered breakdowns: service calls in this group whose outcome is completed. completed + transferred equals calls.
      - `transferred` — number — Set on the answered breakdowns: service calls in this group whose outcome is transferred.
      - `avgWaitMs` — number — Average wait, ring included, milliseconds, over this group's service calls - this service's own wait, not the caller's across earlier services. Absent on an empty band. _(format=double)_
      - `maxWaitMs` — number — The longest wait, ring included, milliseconds. Absent on an empty band.
      - `totalWaitMs` — number — Sum of the group's waits in milliseconds; avgWaitMs times calls.
      - `avgTalkMs` — number — Average talk time, hold included, milliseconds. 0 on the unanswered breakdowns; absent on an empty band. _(format=double)_
      - `totalTalkMs` — number — Total talk time, hold included, milliseconds. 0 on the unanswered breakdowns.
      - `totalAnsweringAgentRingToAnswerMs` — number — Set on the answered breakdowns: sum of ServiceCallRow.answeringAgentRingToAnswerMs (from the first ring of the agent who answered to the answer, re-rings included), milliseconds, over the group's service calls that carry one.
      - `totalAnsweringAgentRingMs` — number — Set on the answered breakdowns: sum of ServiceCallRow.answeringAgentRingMs (how long the answering agent's phone actually rang), milliseconds, over the group's service calls that carry one.
      - `avgFinalPosition` — number — Set for BY_SERVICE: average queue position at answer on the answered breakdown; at exit over abandoned service calls only on the unanswered breakdown, the same basis as the unanswered summary's avgFinalPosition. _(format=double)_
- Errors: `400`, `403`, `404`

#### `POST` `/v2/xcaracal/unanswered/service-level/query`

Cheap: closed days come from pre-computed daily rows. It reads the individual calls only for today and for yesterday until its daily rows exist (05:20 in the PBX's zone), and whenever the filter names extensions, outcomes, disconnect reasons, an hour range, days of week or a wait or talk band. Suitable for a page's first request. Cumulative ladder over wait time for the service calls nobody answered - abandoned and unanswered together - how long callers waited before they hung up or the wait ended; each band splits into lost and overflow.

- operationId: `GetUnansweredServiceLevel`
- **Scopes**: `xcaracal:GetUnansweredServiceLevel`, `xcaracal:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
- **Request body** (`application/json` — `GetUnansweredServiceLevelRequestContent`) **(required)**
  - `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
    - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
      - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
    - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
    - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
      - _array of_ `string`
    - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
      - _array of_ `string`
    - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
      - _array of_ `OutcomeFilterValue`
    - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
      - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
      - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
      - _array of_ `number`
    - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
      - _array of_ `string`
    - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
    - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
  - `waitBandSeconds` — number — Width of each wait band, seconds; 20 when omitted. _(default=20; min=5; max=120)_
  - `waitBandSteps` — number — Number of wait bands, the last one open-ended; 7 when omitted. _(default=7; min=1; max=60)_
- **Response 200** (`GetUnansweredServiceLevelResponseContent`)
  - `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
  - `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
  - `waitBandSeconds` — number **(required)** — The wait band width applied, seconds: the request's value, or 20.
  - `waitBandSteps` — number **(required)** — The number of wait bands applied: the request's value, or 7.
  - `base` — string **(required)** — Always "abandonedOrUnanswered": the base this ladder is computed over - abandoned and unanswered service calls together. Each band splits into lost and overflow.
  - `total` — number **(required)** — Service calls in the base; the last band's cumulative count equals it.
  - `lost` — number **(required)** — Of total, the lost service calls (no later service took the caller); the last band's cumulative lost equals it.
  - `overflow` — number **(required)** — Of total, the overflow service calls (a later service call then took the caller). lost + overflow = total.
  - `bands` — array **(required)**
    - _array of_ `ServiceLevelBand`
      - `withinSeconds` — number — The band's upper limit in seconds: count holds the calls whose wait was at most this. Absent on the open last band.
      - `count` — number **(required)** — Calls waiting at most withinSeconds: this band and all earlier ones.
      - `delta` — number **(required)** — Calls in this band only.
      - `lost` — number — Set on the abandoned-or-unanswered ladder: of count, the lost service calls (no later service took the caller), cumulative like count.
      - `lostDelta` — number — Set on the abandoned-or-unanswered ladder: of delta, the lost service calls.
      - `overflow` — number — Set on the abandoned-or-unanswered ladder: of count, the overflow service calls (a later service call then took the caller), cumulative like count. lost + overflow = count.
      - `overflowDelta` — number — Set on the abandoned-or-unanswered ladder: of delta, the overflow service calls. lostDelta + overflowDelta = delta.
- Errors: `400`, `403`, `404`

#### `POST` `/v2/xcaracal/unanswered/summary/query`

Cheap: closed days come from pre-computed daily rows. It reads the individual calls only for today and for yesterday until its daily rows exist (05:20 in the PBX's zone), and whenever the filter names extensions, outcomes, disconnect reasons, an hour range, days of week or a wait or talk band. Suitable for a page's first request. Unanswered-calls KPIs over complete service calls that were not answered: abandoned (the caller hung up or was removed by a rule) and unanswered (the wait ended without an answer: a timeout, an empty queue, the caller leaving by a keypad option, a hand-off before anyone answered, or a reason the classification does not name). Waits are how long callers held before the call ended.

- operationId: `GetUnansweredSummary`
- **Scopes**: `xcaracal:GetUnansweredSummary`, `xcaracal:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used, e.g. it_w123123.
- **Request body** (`application/json` — `GetUnansweredSummaryRequestContent`) **(required)**
  - `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
    - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
      - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
      - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
    - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
    - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
      - _array of_ `string`
    - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
      - _array of_ `string`
    - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
      - _array of_ `OutcomeFilterValue`
    - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
      - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
      - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
      - _array of_ `number`
    - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
      - `from` — number **(required)** _(min=0; max=86400)_
      - `to` — number _(min=1; max=86400)_
    - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
      - _array of_ `string`
    - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
    - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- **Response 200** (`GetUnansweredSummaryResponseContent`)
  - `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
  - `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
  - `abandoned` — number **(required)** — As counts.abandoned: nobody answered and the disconnect reason is a hang-up.
  - `shortAbandoned` — number **(required)** — As counts.shortAbandoned: of abandoned, the calls that waited at most 5 seconds, ring included.
  - `unanswered` — number **(required)** — As counts.unanswered: nobody answered and the wait ended for any other reason - a timeout, an empty queue, the caller leaving by a keypad option, a reason the classification does not name, or a hand-off before anyone answered (disconnect reason TRANSFER, FORWARD or PICKUP).
  - `lost` — number **(required)** — Of the abandoned and unanswered service calls, those that were the last service call of their phone call: no later service took the caller. Summed over services it is the number of lost phone calls.
  - `lostAbandoned` — number **(required)** — Of lost, those whose last service call was abandoned: its disconnect reason is a hang-up (see abandoned).
  - `lostUnanswered` — number **(required)** — Of lost, those whose last service call ended unanswered (see unanswered). lostAbandoned + lostUnanswered = lost.
  - `overflow` — number **(required)** — abandoned + unanswered - lost: service calls nobody answered here after which the phone call had a later service call (in another service, or the same one entered again). The caller may have been served there.
  - `avgWaitMs` — number — Average wait, ring included, milliseconds, over abandoned and unanswered service calls together - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
  - `maxWaitMs` — number — The longest wait, milliseconds, over abandoned and unanswered service calls. Absent when there is none.
  - `abandonedAvgWaitMs` — number — Average wait in milliseconds over abandoned service calls only - how long callers held before giving up. avgWaitMs is over abandoned and unanswered service calls together. _(format=double)_
  - `avgStartPosition` — number — Average queue position on entry, over abandoned service calls. _(format=double)_
  - `avgFinalPosition` — number — Average queue position when the call ended, over abandoned service calls. _(format=double)_
  - `sla` — UnansweredSlaCounts **(required)** — Abandoned-within counts: abandonedWithin / eligible is the share of the eligible service calls abandoned within thresholdSeconds. Both leave out the short abandons.
    - `thresholdSeconds` — number **(required)** — The default threshold that applied.
    - `abandonedWithin` — number **(required)** — Abandoned service calls whose wait is at most the threshold that applied to their service, without the short abandons (counts.shortAbandoned), which are outside eligible too.
    - `eligible` — number **(required)** — The denominator, the same as the distribution's sla.eligible: counts.offered minus counts.unknown minus counts.shortAbandoned.
    - `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. abandonedWithin is judged at each service's own threshold, so without this a reader cannot tell which targets produced it. Absent means one threshold applied to every service.
      - _array of_ `ServiceSlaSeconds`
        - `serviceId` — string **(required)** — The service this threshold applies to.
        - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
  - `unknown` — number **(required)** — As counts.unknown: service calls whose outcome could not be determined, left out of every figure above.
- Errors: `400`, `403`, `404`

### Schemas appendix — x-caracal API

<details><summary>53 component schemas</summary>

**`AnsweredBreakdownDimension`**

_The grain of the answered breakdown. A user is the person (extension); an agent is that user as a member of one service (agentId names the service), so BY_AGENT is one row per user and service, BY_USER one row per user over every service of the filter._

- string _(enum: `byService`, `byAgent`, `byUser`, `byDisconnectReason`, `byTalkTime`)_

**`BreakdownGroup`**

_One breakdown group. Only the key fields of the requested dimension are set. Percent of base is calls / total, computed by the client._

- `serviceId` — string — Set for BY_SERVICE and BY_AGENT: the service of this group.
- `serviceName` — string — Set with serviceId: the service's stored name. Absent when the PBX sent none.
- `agentId` — string — Set for BY_AGENT only: the answering agent's id - the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent on BY_USER, where one user spans several services.
- `userName` — string — Set for BY_AGENT and BY_USER: a non-empty name the calls of the window carry for this user - deterministic, not necessarily the newest. Clients resolve the display name from the PBX user list by userExtension and use this as the fallback. A client without the PBX user list should know the name may belong to an earlier holder of the extension. Each call keeps the name it was stored with (ServiceCallRow.answeredByName). Absent when no call of the window carries a name.
- `userExtension` — string — Set for BY_AGENT and BY_USER: the user's extension - the key of a BY_USER group.
- `outcome` — string — Set for BY_DISCONNECT_REASON: the outcome value.
- `disconnectReason` — string — Set for BY_DISCONNECT_REASON: the raw END reason beside the outcome (ServiceCallRow.disconnectReason); the calls of this group are filter.outcomes [outcome] with filter.disconnectReasons [disconnectReason].
- `band` — TalkTimeBand — A talk-time band: bandNo from 1, fromSeconds inclusive, toSeconds inclusive and null on the open-ended last band.
  - `bandNo` — number **(required)** — Band number, from 1.
  - `fromSeconds` — number **(required)** — Lowest whole second of talk in the band. Band 1 starts at 1 but also holds the calls with under 1 s of talk.
  - `toSeconds` — number — Highest whole second of talk in the band. Absent on the last band.
- `abandoned` — number — Set for BY_SERVICE on the unanswered breakdown: service calls in this group whose outcome is abandoned. abandoned + unanswered equals calls.
- `unanswered` — number — Set for BY_SERVICE on the unanswered breakdown: service calls in this group whose outcome is unanswered.
- `lost` — number — Set on the unanswered breakdowns (BY_SERVICE and BY_DISCONNECT_REASON): of this group's service calls, those that were the last of their phone call (no later service took the caller).
- `lostAbandoned` — number — Set with lost: of this group's lost calls, those that were abandoned.
- `lostUnanswered` — number — Set with lost: of this group's lost calls, those that ended unanswered.
- `overflow` — number — Set with lost: of this group's service calls, those after which a later service call took the caller. lost + overflow = calls.
- `calls` — number **(required)** — Service calls in this group; summed over the groups it is total.
- `completed` — number — Set on the answered breakdowns: service calls in this group whose outcome is completed. completed + transferred equals calls.
- `transferred` — number — Set on the answered breakdowns: service calls in this group whose outcome is transferred.
- `avgWaitMs` — number — Average wait, ring included, milliseconds, over this group's service calls - this service's own wait, not the caller's across earlier services. Absent on an empty band. _(format=double)_
- `maxWaitMs` — number — The longest wait, ring included, milliseconds. Absent on an empty band.
- `totalWaitMs` — number — Sum of the group's waits in milliseconds; avgWaitMs times calls.
- `avgTalkMs` — number — Average talk time, hold included, milliseconds. 0 on the unanswered breakdowns; absent on an empty band. _(format=double)_
- `totalTalkMs` — number — Total talk time, hold included, milliseconds. 0 on the unanswered breakdowns.
- `totalAnsweringAgentRingToAnswerMs` — number — Set on the answered breakdowns: sum of ServiceCallRow.answeringAgentRingToAnswerMs (from the first ring of the agent who answered to the answer, re-rings included), milliseconds, over the group's service calls that carry one.
- `totalAnsweringAgentRingMs` — number — Set on the answered breakdowns: sum of ServiceCallRow.answeringAgentRingMs (how long the answering agent's phone actually rang), milliseconds, over the group's service calls that carry one.
- `avgFinalPosition` — number — Set for BY_SERVICE: average queue position at answer on the answered breakdown; at exit over abandoned service calls only on the unanswered breakdown, the same basis as the unanswered summary's avgFinalPosition. _(format=double)_

**`Dashboard`**

- `name` — string **(required)** _(minLen=1; maxLen=128)_
- `kind` — string **(required)** _(enum: `live`, `report`)_
- `blocks` — array **(required)** _(maxItems=100)_
  - _array of_ `DashboardBlock`
    - `id` — string **(required)** _(minLen=1; maxLen=64)_
    - `type` — string **(required)** _(enum: `chart`, `note`)_
    - `position` — DashboardBlockPosition **(required)** — Place of a block in the 12-column canvas grid.
      - `x` — number **(required)** _(min=0)_
      - `y` — number **(required)** _(min=0)_
      - `w` — number **(required)** _(min=1)_
      - `h` — number **(required)** _(min=1)_
    - `chartId` — string — The catalog chart shown by the block; required when type is chart. _(minLen=1; maxLen=128)_
    - `config` — DashboardBlockConfig — Data settings of a chart block (e.g. entity, queue), opaque to the service.
      - _map of_ `string`
    - `text` — string — The note; only with type note. It may be empty: a user can add a note before writing it. _(maxLen=2000)_
- `id` — string **(required)** — Chosen by the client, unique among the dashboards of the user. _(pattern=^[A-Za-z0-9_-]+$; minLen=1; maxLen=64)_
- `createdBy` — string **(required)** — Who created the dashboard: the id of the user, or "system" for a predefined dashboard.
- `predefined` — boolean — True for a dashboard the service gives every user (createdBy "system"), e.g. the Live view's Main. It is listed before the user's own, and cannot be changed or deleted: a user customises a copy of it (a new dashboard saved under a new id).
- `createdAt` — string **(required)** — When the dashboard was first saved, ISO 8601.
- `updatedAt` — string **(required)** — When the dashboard was last saved, ISO 8601.

**`DashboardBlock`**

_One block of a dashboard: a chart from the client's catalog (chartId, config) or a text note (text)._

- `id` — string **(required)** _(minLen=1; maxLen=64)_
- `type` — string **(required)** _(enum: `chart`, `note`)_
- `position` — DashboardBlockPosition **(required)** — Place of a block in the 12-column canvas grid.
  - `x` — number **(required)** _(min=0)_
  - `y` — number **(required)** _(min=0)_
  - `w` — number **(required)** _(min=1)_
  - `h` — number **(required)** _(min=1)_
- `chartId` — string — The catalog chart shown by the block; required when type is chart. _(minLen=1; maxLen=128)_
- `config` — DashboardBlockConfig — Data settings of a chart block (e.g. entity, queue), opaque to the service.
  - _map of_ `string`
- `text` — string — The note; only with type note. It may be empty: a user can add a note before writing it. _(maxLen=2000)_

**`DashboardBlockConfig`**

_Data settings of a chart block (e.g. entity, queue), opaque to the service._

- _map of_ `string`

**`DashboardBlockPosition`**

_Place of a block in the 12-column canvas grid._

- `x` — number **(required)** _(min=0)_
- `y` — number **(required)** _(min=0)_
- `w` — number **(required)** _(min=1)_
- `h` — number **(required)** _(min=1)_

**`DashboardBlockType`**

- string _(enum: `chart`, `note`)_

**`DashboardKind`**

- string _(enum: `live`, `report`)_

**`DistributionMetrics`**

_The distribution metric block. Every figure here is per service call: a call that went through several services counts in each service with that service's own wait and ringing; the caller's totals across services are on the call list (ServiceCallRow.totalQueueWaitMs and totalQueueRingMs). Waits are over complete service calls; talk is over answered and transferred service calls and includes on-call hold. The service's ring time is avgRingMs: how long agents were being rung for the caller, from the first ring to an answer or the end of the wait; the wait minus it is the time before the first agent was rung. avgAnsweringAgentRingToAnswerMs and avgAnsweringAgentRingMs describe the agent who answered. Averages are null when the base is empty._

- `counts` — ServiceCallCounts **(required)** — Service call counts by outcome. Each service call (one phone call's stay in one service) counts on its own; a phone call that went through two services is two service calls. completed + transferred + abandoned + unanswered + unknown = offered: the calls whose outcome could not be determined stay in the total, as a count of their own, and are left out of every average and SLA figure. Averages are computed by the service; percentages are left to the client, because every count they need is returned.
  - `offered` — number **(required)** — Every service call in the window, all outcomes, unknown included.
  - `received` — number **(required)** — The service calls that ended in this service, offered - overflow = completed + transferred + lost + unknown. An unknown service call counts as received even when a later service took the caller. Not unique phone calls: a call answered in one service and transferred into another counts in both.
  - `completed` — number **(required)** — Service calls an agent answered and kept: the disconnect reason is neither TRANSFER nor FORWARD. Outcome value completed.
  - `transferred` — number **(required)** — Service calls an agent answered and then handed on (disconnect reason TRANSFER or FORWARD). answered = completed + transferred.
  - `abandoned` — number **(required)** — Service calls nobody answered whose disconnect reason is a hang-up: the caller hung up, or a rule took the call out of the queue.
  - `shortAbandoned` — number **(required)** — Of abandoned, the service calls whose wait, ring included, was at most 5 seconds. Included in abandoned, not an extra outcome.
  - `unanswered` — number **(required)** — Service calls nobody answered that ended for any other reason - a timeout, an empty queue, the caller leaving by a keypad option, a reason the classification does not name, or a hand-off before anyone answered (disconnect reason TRANSFER, FORWARD or PICKUP).
  - `unknown` — number **(required)** — Service calls whose outcome could not be determined from their events. Outcome value unknown; their events can be read with GetServiceCallEvents. Counted in offered and received; left out of every average and SLA figure, because their wait and outcome are not known.
  - `lost` — number **(required)** — Of the abandoned and unanswered service calls, those that were the last service call of their phone call: no later service took the caller. Summed over services it is the number of lost phone calls.
  - `lostAbandoned` — number **(required)** — Of lost, those whose last service call was abandoned: its disconnect reason is a hang-up (see abandoned).
  - `lostUnanswered` — number **(required)** — Of lost, those whose last service call ended unanswered (see unanswered). lostAbandoned + lostUnanswered = lost.
  - `overflow` — number **(required)** — abandoned + unanswered - lost: service calls nobody answered here after which the phone call had a later service call (in another service, or the same one entered again). The caller may have been served there.
- `avgWaitMs` — number — Average wait, ring included, milliseconds, over the service calls whose outcome could be determined (every outcome; unknown left out) - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
- `maxWaitMs` — number — The longest wait, ring included, milliseconds, over the same service calls as avgWaitMs. Absent when there is none.
- `avgTalkMs` — number — Average talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none. _(format=double)_
- `totalTalkMs` — number — Total talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none.
- `avgRingMs` — number — The service's ring time. Average time from the first ring to any agent to the answer, or to the end of the service call when nobody answered, milliseconds, over the service calls whose outcome could be determined (answered, abandoned and unanswered together; unknown left out) that rang at least one agent; stretches with no agent ringing are included (ServiceCallRow.ringMs). Absent when there is none. _(format=double)_
- `avgAnsweringAgentRingToAnswerMs` — number — Average time from the first ring of the agent who answered to the answer, milliseconds, over completed and transferred service calls that carry one; re-rings, and any stretches in between when that agent's phone was not ringing, are included (ServiceCallRow.answeringAgentRingToAnswerMs). Absent when there is none. _(format=double)_
- `avgAnsweringAgentRingMs` — number — Average of how long the answering agent's phone actually rang, its rings added up, milliseconds, over completed and transferred service calls that carry one (ServiceCallRow.answeringAgentRingMs). Absent when there is none. _(format=double)_
- `maxStartPosition` — number **(required)** — The highest place in line any caller had on joining, over every service call, unknown included. The highest place could be treated as the maximum number of callers waiting in the queue. With several services in the filter, the busiest service's figure.
- `maxStartPositionAnswered` — number **(required)** — The deepest place in line on joining, over answered and transferred service calls.
- `maxStartPositionAbandonedOrUnanswered` — number **(required)** — The deepest place in line on joining, over abandoned and unanswered service calls.
- `maxFinalPositionAbandoned` — number **(required)** — The deepest place in line when the caller hung up while waiting (abandoned).
- `maxFinalPositionUnanswered` — number **(required)** — The deepest place in line when the wait ended unanswered (see ServiceCallCounts.unanswered).
- `sla` — SlaCounts **(required)** — Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds.
  - `thresholdSeconds` — number **(required)** — The default threshold that applied; on a by-service group, that service's own threshold.
  - `answeredWithin` — number **(required)** — Completed or transferred service calls whose wait, ring included, is at most the threshold that applied to their service - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs).
  - `eligible` — number **(required)** — The SLA denominator: counts.offered minus counts.unknown minus counts.shortAbandoned - the calls whose outcome could be determined, without the calls abandoned within 5 seconds, which gave the service no time to answer.
  - `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. Absent means one threshold applied to every service.
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_

**`DistributionServiceGroup`**

- `serviceId` — string **(required)** — The service of this group.
- `serviceName` — string — The service's name as stored with its calls. Absent when the PBX sent none.
- `metrics` — DistributionMetrics **(required)** — The distribution metric block. Every figure here is per service call: a call that went through several services counts in each service with that service's own wait and ringing; the caller's totals across services are on the call list (ServiceCallRow.totalQueueWaitMs and totalQueueRingMs). Waits are over complete service calls; talk is over answered and transferred service calls and includes on-call hold. The service's ring time is avgRingMs: how long agents were being rung for the caller, from the first ring to an answer or the end of the wait; the wait minus it is the time before the first agent was rung. avgAnsweringAgentRingToAnswerMs and avgAnsweringAgentRingMs describe the agent who answered. Averages are null when the base is empty.
  - `counts` — ServiceCallCounts **(required)** — Service call counts by outcome. Each service call (one phone call's stay in one service) counts on its own; a phone call that went through two services is two service calls. completed + transferred + abandoned + unanswered + unknown = offered: the calls whose outcome could not be determined stay in the total, as a count of their own, and are left out of every average and SLA figure. Averages are computed by the service; percentages are left to the client, because every count they need is returned.
    - `offered` — number **(required)** — Every service call in the window, all outcomes, unknown included.
    - `received` — number **(required)** — The service calls that ended in this service, offered - overflow = completed + transferred + lost + unknown. An unknown service call counts as received even when a later service took the caller. Not unique phone calls: a call answered in one service and transferred into another counts in both.
    - `completed` — number **(required)** — Service calls an agent answered and kept: the disconnect reason is neither TRANSFER nor FORWARD. Outcome value completed.
    - `transferred` — number **(required)** — Service calls an agent answered and then handed on (disconnect reason TRANSFER or FORWARD). answered = completed + transferred.
    - `abandoned` — number **(required)** — Service calls nobody answered whose disconnect reason is a hang-up: the caller hung up, or a rule took the call out of the queue.
    - `shortAbandoned` — number **(required)** — Of abandoned, the service calls whose wait, ring included, was at most 5 seconds. Included in abandoned, not an extra outcome.
    - `unanswered` — number **(required)** — Service calls nobody answered that ended for any other reason - a timeout, an empty queue, the caller leaving by a keypad option, a reason the classification does not name, or a hand-off before anyone answered (disconnect reason TRANSFER, FORWARD or PICKUP).
    - `unknown` — number **(required)** — Service calls whose outcome could not be determined from their events. Outcome value unknown; their events can be read with GetServiceCallEvents. Counted in offered and received; left out of every average and SLA figure, because their wait and outcome are not known.
    - `lost` — number **(required)** — Of the abandoned and unanswered service calls, those that were the last service call of their phone call: no later service took the caller. Summed over services it is the number of lost phone calls.
    - `lostAbandoned` — number **(required)** — Of lost, those whose last service call was abandoned: its disconnect reason is a hang-up (see abandoned).
    - `lostUnanswered` — number **(required)** — Of lost, those whose last service call ended unanswered (see unanswered). lostAbandoned + lostUnanswered = lost.
    - `overflow` — number **(required)** — abandoned + unanswered - lost: service calls nobody answered here after which the phone call had a later service call (in another service, or the same one entered again). The caller may have been served there.
  - `avgWaitMs` — number — Average wait, ring included, milliseconds, over the service calls whose outcome could be determined (every outcome; unknown left out) - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
  - `maxWaitMs` — number — The longest wait, ring included, milliseconds, over the same service calls as avgWaitMs. Absent when there is none.
  - `avgTalkMs` — number — Average talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none. _(format=double)_
  - `totalTalkMs` — number — Total talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none.
  - `avgRingMs` — number — The service's ring time. Average time from the first ring to any agent to the answer, or to the end of the service call when nobody answered, milliseconds, over the service calls whose outcome could be determined (answered, abandoned and unanswered together; unknown left out) that rang at least one agent; stretches with no agent ringing are included (ServiceCallRow.ringMs). Absent when there is none. _(format=double)_
  - `avgAnsweringAgentRingToAnswerMs` — number — Average time from the first ring of the agent who answered to the answer, milliseconds, over completed and transferred service calls that carry one; re-rings, and any stretches in between when that agent's phone was not ringing, are included (ServiceCallRow.answeringAgentRingToAnswerMs). Absent when there is none. _(format=double)_
  - `avgAnsweringAgentRingMs` — number — Average of how long the answering agent's phone actually rang, its rings added up, milliseconds, over completed and transferred service calls that carry one (ServiceCallRow.answeringAgentRingMs). Absent when there is none. _(format=double)_
  - `maxStartPosition` — number **(required)** — The highest place in line any caller had on joining, over every service call, unknown included. The highest place could be treated as the maximum number of callers waiting in the queue. With several services in the filter, the busiest service's figure.
  - `maxStartPositionAnswered` — number **(required)** — The deepest place in line on joining, over answered and transferred service calls.
  - `maxStartPositionAbandonedOrUnanswered` — number **(required)** — The deepest place in line on joining, over abandoned and unanswered service calls.
  - `maxFinalPositionAbandoned` — number **(required)** — The deepest place in line when the caller hung up while waiting (abandoned).
  - `maxFinalPositionUnanswered` — number **(required)** — The deepest place in line when the wait ended unanswered (see ServiceCallCounts.unanswered).
  - `sla` — SlaCounts **(required)** — Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds.
    - `thresholdSeconds` — number **(required)** — The default threshold that applied; on a by-service group, that service's own threshold.
    - `answeredWithin` — number **(required)** — Completed or transferred service calls whose wait, ring included, is at most the threshold that applied to their service - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs).
    - `eligible` — number **(required)** — The SLA denominator: counts.offered minus counts.unknown minus counts.shortAbandoned - the calls whose outcome could be determined, without the calls abandoned within 5 seconds, which gave the service no time to answer.
    - `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. Absent means one threshold applied to every service.
      - _array of_ `ServiceSlaSeconds`
        - _(nesting depth limit — see `ServiceSlaSeconds` in the Schemas appendix)_

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetAnsweredBreakdownRequestContent`**

_Company resolution. `company` is accepted only with a service (S2S) token; PBX, API-key and XBS tokens carry the company in their claims and a `company` parameter is rejected._

- `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
  - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
    - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
  - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
  - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
    - _array of_ `string`
  - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
    - _array of_ `string`
  - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
    - _array of_ `OutcomeFilterValue`
  - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
    - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
  - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
    - _array of_ `number`
  - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
    - _array of_ `string`
  - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
  - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- `talkBandSeconds` — number — Width of each talk band, seconds; 20 when omitted. _(default=20; min=1; max=3600)_
- `talkBandSteps` — number — Number of talk bands, the last one open-ended; 7 when omitted. _(default=7; min=1; max=60)_
- `dimension` — string **(required)** — The grain of the answered breakdown. A user is the person (extension); an agent is that user as a member of one service (agentId names the service), so BY_AGENT is one row per user and service, BY_USER one row per user over every service of the filter. _(enum: `byService`, `byAgent`, `byUser`, `byDisconnectReason`, `byTalkTime`)_

**`GetAnsweredBreakdownResponseContent`**

_Fields every windowed report response carries besides its figures. No freshness field: figures lag the live system by up to about a minute (file batching), and a page shows its own request time._

- `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
- `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
- `dimension` — string **(required)** — The grain of the answered breakdown. A user is the person (extension); an agent is that user as a member of one service (agentId names the service), so BY_AGENT is one row per user and service, BY_USER one row per user over every service of the filter. _(enum: `byService`, `byAgent`, `byUser`, `byDisconnectReason`, `byTalkTime`)_
- `total` — number **(required)** — The service calls the groups count together; a group's share is its calls divided by total. byAgent and byUser count only calls with an answering agent; a call whose answering agent was not recorded is in no group, so there total can be lower than completed + transferred.
- `groups` — array **(required)**
  - _array of_ `BreakdownGroup`
    - `serviceId` — string — Set for BY_SERVICE and BY_AGENT: the service of this group.
    - `serviceName` — string — Set with serviceId: the service's stored name. Absent when the PBX sent none.
    - `agentId` — string — Set for BY_AGENT only: the answering agent's id - the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent on BY_USER, where one user spans several services.
    - `userName` — string — Set for BY_AGENT and BY_USER: a non-empty name the calls of the window carry for this user - deterministic, not necessarily the newest. Clients resolve the display name from the PBX user list by userExtension and use this as the fallback. A client without the PBX user list should know the name may belong to an earlier holder of the extension. Each call keeps the name it was stored with (ServiceCallRow.answeredByName). Absent when no call of the window carries a name.
    - `userExtension` — string — Set for BY_AGENT and BY_USER: the user's extension - the key of a BY_USER group.
    - `outcome` — string — Set for BY_DISCONNECT_REASON: the outcome value.
    - `disconnectReason` — string — Set for BY_DISCONNECT_REASON: the raw END reason beside the outcome (ServiceCallRow.disconnectReason); the calls of this group are filter.outcomes [outcome] with filter.disconnectReasons [disconnectReason].
    - `band` — TalkTimeBand — A talk-time band: bandNo from 1, fromSeconds inclusive, toSeconds inclusive and null on the open-ended last band.
      - `bandNo` — number **(required)** — Band number, from 1.
      - `fromSeconds` — number **(required)** — Lowest whole second of talk in the band. Band 1 starts at 1 but also holds the calls with under 1 s of talk.
      - `toSeconds` — number — Highest whole second of talk in the band. Absent on the last band.
    - `abandoned` — number — Set for BY_SERVICE on the unanswered breakdown: service calls in this group whose outcome is abandoned. abandoned + unanswered equals calls.
    - `unanswered` — number — Set for BY_SERVICE on the unanswered breakdown: service calls in this group whose outcome is unanswered.
    - `lost` — number — Set on the unanswered breakdowns (BY_SERVICE and BY_DISCONNECT_REASON): of this group's service calls, those that were the last of their phone call (no later service took the caller).
    - `lostAbandoned` — number — Set with lost: of this group's lost calls, those that were abandoned.
    - `lostUnanswered` — number — Set with lost: of this group's lost calls, those that ended unanswered.
    - `overflow` — number — Set with lost: of this group's service calls, those after which a later service call took the caller. lost + overflow = calls.
    - `calls` — number **(required)** — Service calls in this group; summed over the groups it is total.
    - `completed` — number — Set on the answered breakdowns: service calls in this group whose outcome is completed. completed + transferred equals calls.
    - `transferred` — number — Set on the answered breakdowns: service calls in this group whose outcome is transferred.
    - `avgWaitMs` — number — Average wait, ring included, milliseconds, over this group's service calls - this service's own wait, not the caller's across earlier services. Absent on an empty band. _(format=double)_
    - `maxWaitMs` — number — The longest wait, ring included, milliseconds. Absent on an empty band.
    - `totalWaitMs` — number — Sum of the group's waits in milliseconds; avgWaitMs times calls.
    - `avgTalkMs` — number — Average talk time, hold included, milliseconds. 0 on the unanswered breakdowns; absent on an empty band. _(format=double)_
    - `totalTalkMs` — number — Total talk time, hold included, milliseconds. 0 on the unanswered breakdowns.
    - `totalAnsweringAgentRingToAnswerMs` — number — Set on the answered breakdowns: sum of ServiceCallRow.answeringAgentRingToAnswerMs (from the first ring of the agent who answered to the answer, re-rings included), milliseconds, over the group's service calls that carry one.
    - `totalAnsweringAgentRingMs` — number — Set on the answered breakdowns: sum of ServiceCallRow.answeringAgentRingMs (how long the answering agent's phone actually rang), milliseconds, over the group's service calls that carry one.
    - `avgFinalPosition` — number — Set for BY_SERVICE: average queue position at answer on the answered breakdown; at exit over abandoned service calls only on the unanswered breakdown, the same basis as the unanswered summary's avgFinalPosition. _(format=double)_
- `talkBandSeconds` — number — Echoed for BY_TALK_TIME: the talk band width applied, seconds.
- `talkBandSteps` — number — Echoed for BY_TALK_TIME: the number of talk bands applied.

**`GetAnsweredServiceLevelRequestContent`**

_Company resolution. `company` is accepted only with a service (S2S) token; PBX, API-key and XBS tokens carry the company in their claims and a `company` parameter is rejected._

- `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
  - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
    - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
  - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
  - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
    - _array of_ `string`
  - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
    - _array of_ `string`
  - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
    - _array of_ `OutcomeFilterValue`
  - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
    - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
  - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
    - _array of_ `number`
  - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
    - _array of_ `string`
  - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
  - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- `waitBandSeconds` — number — Width of each wait band, seconds; 20 when omitted. _(default=20; min=5; max=120)_
- `waitBandSteps` — number — Number of wait bands, the last one open-ended; 7 when omitted. _(default=7; min=1; max=60)_

**`GetAnsweredServiceLevelResponseContent`**

_Fields every windowed report response carries besides its figures. No freshness field: figures lag the live system by up to about a minute (file batching), and a page shows its own request time._

- `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
- `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
- `waitBandSeconds` — number **(required)** — The wait band width applied, seconds: the request's value, or 20.
- `waitBandSteps` — number **(required)** — The number of wait bands applied: the request's value, or 7.
- `total` — number **(required)** — Service calls in the base; the last band's cumulative count equals it.
- `bands` — array **(required)**
  - _array of_ `ServiceLevelBand`
    - `withinSeconds` — number — The band's upper limit in seconds: count holds the calls whose wait was at most this. Absent on the open last band.
    - `count` — number **(required)** — Calls waiting at most withinSeconds: this band and all earlier ones.
    - `delta` — number **(required)** — Calls in this band only.
    - `lost` — number — Set on the abandoned-or-unanswered ladder: of count, the lost service calls (no later service took the caller), cumulative like count.
    - `lostDelta` — number — Set on the abandoned-or-unanswered ladder: of delta, the lost service calls.
    - `overflow` — number — Set on the abandoned-or-unanswered ladder: of count, the overflow service calls (a later service call then took the caller), cumulative like count. lost + overflow = count.
    - `overflowDelta` — number — Set on the abandoned-or-unanswered ladder: of delta, the overflow service calls. lostDelta + overflowDelta = delta.

**`GetAnsweredSummaryRequestContent`**

_Company resolution. `company` is accepted only with a service (S2S) token; PBX, API-key and XBS tokens carry the company in their claims and a `company` parameter is rejected._

- `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
  - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
    - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
  - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
  - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
    - _array of_ `string`
  - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
    - _array of_ `string`
  - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
    - _array of_ `OutcomeFilterValue`
  - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
    - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
  - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
    - _array of_ `number`
  - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
    - _array of_ `string`
  - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
  - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_

**`GetAnsweredSummaryResponseContent`**

_Fields every windowed report response carries besides its figures. No freshness field: figures lag the live system by up to about a minute (file batching), and a page shows its own request time._

- `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
- `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
- `completed` — number **(required)** — Service calls an agent answered and kept.
- `transferred` — number **(required)** — As counts.transferred. answered = completed + transferred.
- `avgWaitMs` — number — Average wait, ring included, milliseconds, over completed and transferred service calls - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
- `maxWaitMs` — number — The longest wait, ring included, milliseconds, over completed and transferred service calls. Absent when there is none.
- `avgTalkMs` — number — Average talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none. _(format=double)_
- `totalTalkMs` — number — Total talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none.
- `sla` — SlaCounts **(required)** — Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds.
  - `thresholdSeconds` — number **(required)** — The default threshold that applied; on a by-service group, that service's own threshold.
  - `answeredWithin` — number **(required)** — Completed or transferred service calls whose wait, ring included, is at most the threshold that applied to their service - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs).
  - `eligible` — number **(required)** — The SLA denominator: counts.offered minus counts.unknown minus counts.shortAbandoned - the calls whose outcome could be determined, without the calls abandoned within 5 seconds, which gave the service no time to answer.
  - `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. Absent means one threshold applied to every service.
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- `unknown` — number **(required)** — As counts.unknown: service calls whose outcome could not be determined, left out of every figure above.

**`GetDistributionByPeriodRequestContent`**

_Company resolution. `company` is accepted only with a service (S2S) token; PBX, API-key and XBS tokens carry the company in their claims and a `company` parameter is rejected._

- `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
  - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
    - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
  - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
  - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
    - _array of_ `string`
  - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
    - _array of_ `string`
  - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
    - _array of_ `OutcomeFilterValue`
  - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
    - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
  - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
    - _array of_ `number`
  - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
    - _array of_ `string`
  - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
  - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- `granularity` — string **(required)** — Time-bucketing axis. WEEK is ISO-8601, Monday-start. HOUR and DAY_OF_WEEK are recurring buckets (hour of day, ISO day 1-7) over the whole window. _(enum: `hour`, `day`, `week`, `month`, `dayOfWeek`)_

**`GetDistributionByPeriodResponseContent`**

_Fields every windowed report response carries besides its figures. No freshness field: figures lag the live system by up to about a minute (file batching), and a page shows its own request time._

- `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
- `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
- `granularity` — string **(required)** — Time-bucketing axis. WEEK is ISO-8601, Monday-start. HOUR and DAY_OF_WEEK are recurring buckets (hour of day, ISO day 1-7) over the whole window. _(enum: `hour`, `day`, `week`, `month`, `dayOfWeek`)_
- `buckets` — array **(required)**
  - _array of_ `PeriodBucket`
    - `bucketKey` — string **(required)** — HH:00 for HOUR, 1-7 for DAY_OF_WEEK (ISO, Monday = 1), YYYY-MM-DD for DAY, YYYY-Www for WEEK, YYYY-MM for MONTH.
    - `sortKey` — number **(required)** — Orders the series.
    - `bucketStart` — string — The bucket's local start. Set for DAY, WEEK and MONTH only. _(format=date-time)_
    - `metrics` — DistributionMetrics **(required)** — The distribution metric block. Every figure here is per service call: a call that went through several services counts in each service with that service's own wait and ringing; the caller's totals across services are on the call list (ServiceCallRow.totalQueueWaitMs and totalQueueRingMs). Waits are over complete service calls; talk is over answered and transferred service calls and includes on-call hold. The service's ring time is avgRingMs: how long agents were being rung for the caller, from the first ring to an answer or the end of the wait; the wait minus it is the time before the first agent was rung. avgAnsweringAgentRingToAnswerMs and avgAnsweringAgentRingMs describe the agent who answered. Averages are null when the base is empty.
      - `counts` — ServiceCallCounts **(required)** — Service call counts by outcome. Each service call (one phone call's stay in one service) counts on its own; a phone call that went through two services is two service calls. completed + transferred + abandoned + unanswered + unknown = offered: the calls whose outcome could not be determined stay in the total, as a count of their own, and are left out of every average and SLA figure. Averages are computed by the service; percentages are left to the client, because every count they need is returned.
        - _(nesting depth limit — see `ServiceCallCounts` in the Schemas appendix)_
      - `avgWaitMs` — number — Average wait, ring included, milliseconds, over the service calls whose outcome could be determined (every outcome; unknown left out) - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
      - `maxWaitMs` — number — The longest wait, ring included, milliseconds, over the same service calls as avgWaitMs. Absent when there is none.
      - `avgTalkMs` — number — Average talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none. _(format=double)_
      - `totalTalkMs` — number — Total talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none.
      - `avgRingMs` — number — The service's ring time. Average time from the first ring to any agent to the answer, or to the end of the service call when nobody answered, milliseconds, over the service calls whose outcome could be determined (answered, abandoned and unanswered together; unknown left out) that rang at least one agent; stretches with no agent ringing are included (ServiceCallRow.ringMs). Absent when there is none. _(format=double)_
      - `avgAnsweringAgentRingToAnswerMs` — number — Average time from the first ring of the agent who answered to the answer, milliseconds, over completed and transferred service calls that carry one; re-rings, and any stretches in between when that agent's phone was not ringing, are included (ServiceCallRow.answeringAgentRingToAnswerMs). Absent when there is none. _(format=double)_
      - `avgAnsweringAgentRingMs` — number — Average of how long the answering agent's phone actually rang, its rings added up, milliseconds, over completed and transferred service calls that carry one (ServiceCallRow.answeringAgentRingMs). Absent when there is none. _(format=double)_
      - `maxStartPosition` — number **(required)** — The highest place in line any caller had on joining, over every service call, unknown included. The highest place could be treated as the maximum number of callers waiting in the queue. With several services in the filter, the busiest service's figure.
      - `maxStartPositionAnswered` — number **(required)** — The deepest place in line on joining, over answered and transferred service calls.
      - `maxStartPositionAbandonedOrUnanswered` — number **(required)** — The deepest place in line on joining, over abandoned and unanswered service calls.
      - `maxFinalPositionAbandoned` — number **(required)** — The deepest place in line when the caller hung up while waiting (abandoned).
      - `maxFinalPositionUnanswered` — number **(required)** — The deepest place in line when the wait ended unanswered (see ServiceCallCounts.unanswered).
      - `sla` — SlaCounts **(required)** — Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds.
        - _(nesting depth limit — see `SlaCounts` in the Schemas appendix)_

**`GetDistributionByServiceRequestContent`**

_Company resolution. `company` is accepted only with a service (S2S) token; PBX, API-key and XBS tokens carry the company in their claims and a `company` parameter is rejected._

- `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
  - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
    - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
  - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
  - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
    - _array of_ `string`
  - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
    - _array of_ `string`
  - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
    - _array of_ `OutcomeFilterValue`
  - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
    - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
  - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
    - _array of_ `number`
  - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
    - _array of_ `string`
  - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
  - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_

**`GetDistributionByServiceResponseContent`**

_Fields every windowed report response carries besides its figures. No freshness field: figures lag the live system by up to about a minute (file batching), and a page shows its own request time._

- `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
- `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
- `groups` — array **(required)**
  - _array of_ `DistributionServiceGroup`
    - `serviceId` — string **(required)** — The service of this group.
    - `serviceName` — string — The service's name as stored with its calls. Absent when the PBX sent none.
    - `metrics` — DistributionMetrics **(required)** — The distribution metric block. Every figure here is per service call: a call that went through several services counts in each service with that service's own wait and ringing; the caller's totals across services are on the call list (ServiceCallRow.totalQueueWaitMs and totalQueueRingMs). Waits are over complete service calls; talk is over answered and transferred service calls and includes on-call hold. The service's ring time is avgRingMs: how long agents were being rung for the caller, from the first ring to an answer or the end of the wait; the wait minus it is the time before the first agent was rung. avgAnsweringAgentRingToAnswerMs and avgAnsweringAgentRingMs describe the agent who answered. Averages are null when the base is empty.
      - `counts` — ServiceCallCounts **(required)** — Service call counts by outcome. Each service call (one phone call's stay in one service) counts on its own; a phone call that went through two services is two service calls. completed + transferred + abandoned + unanswered + unknown = offered: the calls whose outcome could not be determined stay in the total, as a count of their own, and are left out of every average and SLA figure. Averages are computed by the service; percentages are left to the client, because every count they need is returned.
        - _(nesting depth limit — see `ServiceCallCounts` in the Schemas appendix)_
      - `avgWaitMs` — number — Average wait, ring included, milliseconds, over the service calls whose outcome could be determined (every outcome; unknown left out) - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
      - `maxWaitMs` — number — The longest wait, ring included, milliseconds, over the same service calls as avgWaitMs. Absent when there is none.
      - `avgTalkMs` — number — Average talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none. _(format=double)_
      - `totalTalkMs` — number — Total talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none.
      - `avgRingMs` — number — The service's ring time. Average time from the first ring to any agent to the answer, or to the end of the service call when nobody answered, milliseconds, over the service calls whose outcome could be determined (answered, abandoned and unanswered together; unknown left out) that rang at least one agent; stretches with no agent ringing are included (ServiceCallRow.ringMs). Absent when there is none. _(format=double)_
      - `avgAnsweringAgentRingToAnswerMs` — number — Average time from the first ring of the agent who answered to the answer, milliseconds, over completed and transferred service calls that carry one; re-rings, and any stretches in between when that agent's phone was not ringing, are included (ServiceCallRow.answeringAgentRingToAnswerMs). Absent when there is none. _(format=double)_
      - `avgAnsweringAgentRingMs` — number — Average of how long the answering agent's phone actually rang, its rings added up, milliseconds, over completed and transferred service calls that carry one (ServiceCallRow.answeringAgentRingMs). Absent when there is none. _(format=double)_
      - `maxStartPosition` — number **(required)** — The highest place in line any caller had on joining, over every service call, unknown included. The highest place could be treated as the maximum number of callers waiting in the queue. With several services in the filter, the busiest service's figure.
      - `maxStartPositionAnswered` — number **(required)** — The deepest place in line on joining, over answered and transferred service calls.
      - `maxStartPositionAbandonedOrUnanswered` — number **(required)** — The deepest place in line on joining, over abandoned and unanswered service calls.
      - `maxFinalPositionAbandoned` — number **(required)** — The deepest place in line when the caller hung up while waiting (abandoned).
      - `maxFinalPositionUnanswered` — number **(required)** — The deepest place in line when the wait ended unanswered (see ServiceCallCounts.unanswered).
      - `sla` — SlaCounts **(required)** — Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds.
        - _(nesting depth limit — see `SlaCounts` in the Schemas appendix)_

**`GetDistributionSummaryRequestContent`**

_Company resolution. `company` is accepted only with a service (S2S) token; PBX, API-key and XBS tokens carry the company in their claims and a `company` parameter is rejected._

- `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
  - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
    - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
  - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
  - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
    - _array of_ `string`
  - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
    - _array of_ `string`
  - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
    - _array of_ `OutcomeFilterValue`
  - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
    - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
  - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
    - _array of_ `number`
  - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
    - _array of_ `string`
  - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
  - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_

**`GetDistributionSummaryResponseContent`**

_Fields every windowed report response carries besides its figures. No freshness field: figures lag the live system by up to about a minute (file batching), and a page shows its own request time._

- `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
- `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
- `metrics` — DistributionMetrics **(required)** — The distribution metric block. Every figure here is per service call: a call that went through several services counts in each service with that service's own wait and ringing; the caller's totals across services are on the call list (ServiceCallRow.totalQueueWaitMs and totalQueueRingMs). Waits are over complete service calls; talk is over answered and transferred service calls and includes on-call hold. The service's ring time is avgRingMs: how long agents were being rung for the caller, from the first ring to an answer or the end of the wait; the wait minus it is the time before the first agent was rung. avgAnsweringAgentRingToAnswerMs and avgAnsweringAgentRingMs describe the agent who answered. Averages are null when the base is empty.
  - `counts` — ServiceCallCounts **(required)** — Service call counts by outcome. Each service call (one phone call's stay in one service) counts on its own; a phone call that went through two services is two service calls. completed + transferred + abandoned + unanswered + unknown = offered: the calls whose outcome could not be determined stay in the total, as a count of their own, and are left out of every average and SLA figure. Averages are computed by the service; percentages are left to the client, because every count they need is returned.
    - `offered` — number **(required)** — Every service call in the window, all outcomes, unknown included.
    - `received` — number **(required)** — The service calls that ended in this service, offered - overflow = completed + transferred + lost + unknown. An unknown service call counts as received even when a later service took the caller. Not unique phone calls: a call answered in one service and transferred into another counts in both.
    - `completed` — number **(required)** — Service calls an agent answered and kept: the disconnect reason is neither TRANSFER nor FORWARD. Outcome value completed.
    - `transferred` — number **(required)** — Service calls an agent answered and then handed on (disconnect reason TRANSFER or FORWARD). answered = completed + transferred.
    - `abandoned` — number **(required)** — Service calls nobody answered whose disconnect reason is a hang-up: the caller hung up, or a rule took the call out of the queue.
    - `shortAbandoned` — number **(required)** — Of abandoned, the service calls whose wait, ring included, was at most 5 seconds. Included in abandoned, not an extra outcome.
    - `unanswered` — number **(required)** — Service calls nobody answered that ended for any other reason - a timeout, an empty queue, the caller leaving by a keypad option, a reason the classification does not name, or a hand-off before anyone answered (disconnect reason TRANSFER, FORWARD or PICKUP).
    - `unknown` — number **(required)** — Service calls whose outcome could not be determined from their events. Outcome value unknown; their events can be read with GetServiceCallEvents. Counted in offered and received; left out of every average and SLA figure, because their wait and outcome are not known.
    - `lost` — number **(required)** — Of the abandoned and unanswered service calls, those that were the last service call of their phone call: no later service took the caller. Summed over services it is the number of lost phone calls.
    - `lostAbandoned` — number **(required)** — Of lost, those whose last service call was abandoned: its disconnect reason is a hang-up (see abandoned).
    - `lostUnanswered` — number **(required)** — Of lost, those whose last service call ended unanswered (see unanswered). lostAbandoned + lostUnanswered = lost.
    - `overflow` — number **(required)** — abandoned + unanswered - lost: service calls nobody answered here after which the phone call had a later service call (in another service, or the same one entered again). The caller may have been served there.
  - `avgWaitMs` — number — Average wait, ring included, milliseconds, over the service calls whose outcome could be determined (every outcome; unknown left out) - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
  - `maxWaitMs` — number — The longest wait, ring included, milliseconds, over the same service calls as avgWaitMs. Absent when there is none.
  - `avgTalkMs` — number — Average talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none. _(format=double)_
  - `totalTalkMs` — number — Total talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none.
  - `avgRingMs` — number — The service's ring time. Average time from the first ring to any agent to the answer, or to the end of the service call when nobody answered, milliseconds, over the service calls whose outcome could be determined (answered, abandoned and unanswered together; unknown left out) that rang at least one agent; stretches with no agent ringing are included (ServiceCallRow.ringMs). Absent when there is none. _(format=double)_
  - `avgAnsweringAgentRingToAnswerMs` — number — Average time from the first ring of the agent who answered to the answer, milliseconds, over completed and transferred service calls that carry one; re-rings, and any stretches in between when that agent's phone was not ringing, are included (ServiceCallRow.answeringAgentRingToAnswerMs). Absent when there is none. _(format=double)_
  - `avgAnsweringAgentRingMs` — number — Average of how long the answering agent's phone actually rang, its rings added up, milliseconds, over completed and transferred service calls that carry one (ServiceCallRow.answeringAgentRingMs). Absent when there is none. _(format=double)_
  - `maxStartPosition` — number **(required)** — The highest place in line any caller had on joining, over every service call, unknown included. The highest place could be treated as the maximum number of callers waiting in the queue. With several services in the filter, the busiest service's figure.
  - `maxStartPositionAnswered` — number **(required)** — The deepest place in line on joining, over answered and transferred service calls.
  - `maxStartPositionAbandonedOrUnanswered` — number **(required)** — The deepest place in line on joining, over abandoned and unanswered service calls.
  - `maxFinalPositionAbandoned` — number **(required)** — The deepest place in line when the caller hung up while waiting (abandoned).
  - `maxFinalPositionUnanswered` — number **(required)** — The deepest place in line when the wait ended unanswered (see ServiceCallCounts.unanswered).
  - `sla` — SlaCounts **(required)** — Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds.
    - `thresholdSeconds` — number **(required)** — The default threshold that applied; on a by-service group, that service's own threshold.
    - `answeredWithin` — number **(required)** — Completed or transferred service calls whose wait, ring included, is at most the threshold that applied to their service - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs).
    - `eligible` — number **(required)** — The SLA denominator: counts.offered minus counts.unknown minus counts.shortAbandoned - the calls whose outcome could be determined, without the calls abandoned within 5 seconds, which gave the service no time to answer.
    - `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. Absent means one threshold applied to every service.
      - _array of_ `ServiceSlaSeconds`
        - _(nesting depth limit — see `ServiceSlaSeconds` in the Schemas appendix)_

**`GetServiceCallEventsResponseContent`**

- `call` — ServiceCallRow **(required)** — One service call: one phone call's stay in one service (one flow of the call in that service). Ring is nested inside wait; talk includes hold. callerPhone and callerName can be absent; absent does not mean the call had no caller. A call that went from one service to another is several service calls sharing callId (one per service); every report counts each of them on its own.
  - `callId` — string **(required)** — The phone call's id (its session id), shared by every service call of the call. Not this row's own id: with flowIndex and serviceId it identifies the row.
  - `flowIndex` — number **(required)** — The PBX's step number of this service call within the phone call. Not a count of service calls and not guaranteed to be consecutive (see serviceCallsCount). With callId and serviceId it identifies the row.
  - `serviceId` — string **(required)** — The service of this service call.
  - `serviceName` — string — The service's name as stored with the call. Absent when the PBX sent none.
  - `enteredAt` — string **(required)** — When the caller joined the service's queue. _(format=date-time)_
  - `answeredAt` — string — When an agent answered. Absent when nobody did. _(format=date-time)_
  - `endedAt` — string **(required)** — When this service call ended: the caller left the service's queue, or the answered call ended. _(format=date-time)_
  - `waitMs` — number **(required)** — Wait from entering the queue to the answer or the exit, milliseconds; the ring is inside it.
  - `ringMs` — number — The ringing in this service call, milliseconds: from the first ring to any agent to the answer, or to the end of the service call when nobody answered; stretches with no phone ringing are included. It is inside waitMs; waitMs minus ringMs is the time before the first agent was rung. Absent when no agent was rung.
  - `answeringAgentRingToAnswerMs` — number — In this service call, the time from the first ring of the agent who answered to the answer, milliseconds; re-rings, and any stretches in between when that agent's phone was not ringing, are included. Absent when nobody answered, or when no ring was recorded for that agent.
  - `answeringAgentRingMs` — number — In this service call, how long the answering agent's phone actually rang, milliseconds: each ring of that agent lasts until the next event that names that agent (its cancel or the answer) or names no agent at all, and the rings are added up. Absent when nobody answered, or when no ring was recorded for that agent.
  - `talkMs` — number **(required)** — Talk time from the answer to the end, hold included, milliseconds; 0 when nobody answered.
  - `durationMs` — number **(required)** — The whole span of this service call, milliseconds: from joining the queue to the service call's end, waitMs plus talkMs (the whole unit, as the stream API means duration; the talk time alone is talkMs).
  - `answered` — boolean **(required)** — True exactly when an agent of the service answered: outcome completed or transferred; an unknown row can have answered true.
  - `answeredByAgentId` — string — The agent who answered - the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent when nobody answered.
  - `answeredByName` — string — The answering user's name as stored with the call (the name it had then). Absent when nobody answered.
  - `answeredByExtension` — string — The answering user's extension. Absent when nobody answered.
  - `agentsRung` — number **(required)** — How many different agents the service rang during this service call, whether or not they picked up.
  - `startPosition` — number — The caller's place in line on joining the service's queue, as the PBX sends it (1 = first in line). Absent when the PBX did not send it.
  - `finalPosition` — number — The caller's place in line when the wait ended (answer, hang-up or exit), as the PBX sends it. Absent when the PBX did not send it.
  - `outcome` — string **(required)** — completed | transferred | abandoned | unanswered | unknown. An open vocabulary: a client must tolerate a value not listed here. unknown: the outcome could not be determined from the service call's events (see ServiceCallCounts.unknown); such a row is outside every average and every SLA figure.
  - `disconnectReason` — string — The reason the call left the service, as the PBX gave it on the END event, upper-cased: HANGUP, TRANSFER, FORWARD, PICKUP, TIMEOUT, EMPTY, EXITWITHKEY, COMPATIBILITY, UNKNOWN. Absent when the END carried none. filter.disconnectReasons selects by it. The outcome follows the answer, not the reason: answered then TRANSFER or FORWARD is transferred; nobody answered is abandoned for HANGUP and unanswered for every other reason, a hand-off (TRANSFER, FORWARD, PICKUP) included.
  - `callerPhone` — string — The caller's number as the PBX received it. Absent when the PBX sent none.
  - `callerName` — string — The caller's name as the PBX received it. Absent when the PBX sent none.
  - `lost` — boolean — Set on abandoned and unanswered rows only: true when this was the last service call of its phone call (lost), false when a later service call then took the caller (overflow). Absent on every other row.
  - `totalQueueWaitMs` — number **(required)** — The caller's total queue wait: the sum of waitMs over every service call of this phone call. The same value on every row of the call. It covers the waiting time inside the services' queues only - not the IVR before the first service or between services. Computed when the page is read, so it grows if a later service call arrives. It includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
  - `totalQueueRingMs` — number **(required)** — The caller's total ringing: the sum of ringMs over every service call of this phone call. The same value on every row of the call; a service call without ringMs adds 0. Computed when the page is read, so it grows if a later service call arrives. It includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
  - `serviceCallsCount` — number **(required)** — How many service calls this phone call has: 1 when it stayed in one service; the same service entered twice counts 2. Like totalQueueWaitMs and totalQueueRingMs, it includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
- `events` — array **(required)** — Its lifecycle events in time order, whole. The time to the next event is measured to the next action, not to a sibling event of the same action (one action naming several agents gives several events with one time); for a RING, to that agent's next event or to the next event without an agent.
  - _array of_ `ServiceCallEvent`
    - `time` — string **(required)** — When the PBX recorded this event. _(format=date-time)_
    - `action` — string **(required)** — INIT | RING | CANCEL | ANSWER | END, upper-cased.
    - `reason` — string — The raw reason the PBX gave for this event, upper-cased (END and CANCEL carry one); on END it is the row's disconnectReason. Absent when there is none.
    - `agentId` — string — The agent this event concerns - rung, or answering: the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent on events without an agent.
    - `userName` — string — That user's name as stored with the event. Absent on events without an agent.
    - `userExtension` — string — That user's extension. Absent on events without an agent.
    - `queuePosition` — number — The caller's place in line at this event, as the PBX sends it. Absent when the PBX did not send it.

**`GetUnansweredBreakdownRequestContent`**

_Company resolution. `company` is accepted only with a service (S2S) token; PBX, API-key and XBS tokens carry the company in their claims and a `company` parameter is rejected._

- `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
  - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
    - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
  - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
  - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
    - _array of_ `string`
  - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
    - _array of_ `string`
  - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
    - _array of_ `OutcomeFilterValue`
  - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
    - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
  - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
    - _array of_ `number`
  - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
    - _array of_ `string`
  - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
  - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- `dimension` — string **(required)** — The grain of the unanswered breakdown: one group per service, or one group per outcome and raw END reason. _(enum: `byService`, `byDisconnectReason`)_

**`GetUnansweredBreakdownResponseContent`**

_Fields every windowed report response carries besides its figures. No freshness field: figures lag the live system by up to about a minute (file batching), and a page shows its own request time._

- `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
- `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
- `dimension` — string **(required)** — The grain of the unanswered breakdown: one group per service, or one group per outcome and raw END reason. _(enum: `byService`, `byDisconnectReason`)_
- `total` — number **(required)** — The service calls the groups count together; a group's share is its calls divided by total.
- `groups` — array **(required)**
  - _array of_ `BreakdownGroup`
    - `serviceId` — string — Set for BY_SERVICE and BY_AGENT: the service of this group.
    - `serviceName` — string — Set with serviceId: the service's stored name. Absent when the PBX sent none.
    - `agentId` — string — Set for BY_AGENT only: the answering agent's id - the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent on BY_USER, where one user spans several services.
    - `userName` — string — Set for BY_AGENT and BY_USER: a non-empty name the calls of the window carry for this user - deterministic, not necessarily the newest. Clients resolve the display name from the PBX user list by userExtension and use this as the fallback. A client without the PBX user list should know the name may belong to an earlier holder of the extension. Each call keeps the name it was stored with (ServiceCallRow.answeredByName). Absent when no call of the window carries a name.
    - `userExtension` — string — Set for BY_AGENT and BY_USER: the user's extension - the key of a BY_USER group.
    - `outcome` — string — Set for BY_DISCONNECT_REASON: the outcome value.
    - `disconnectReason` — string — Set for BY_DISCONNECT_REASON: the raw END reason beside the outcome (ServiceCallRow.disconnectReason); the calls of this group are filter.outcomes [outcome] with filter.disconnectReasons [disconnectReason].
    - `band` — TalkTimeBand — A talk-time band: bandNo from 1, fromSeconds inclusive, toSeconds inclusive and null on the open-ended last band.
      - `bandNo` — number **(required)** — Band number, from 1.
      - `fromSeconds` — number **(required)** — Lowest whole second of talk in the band. Band 1 starts at 1 but also holds the calls with under 1 s of talk.
      - `toSeconds` — number — Highest whole second of talk in the band. Absent on the last band.
    - `abandoned` — number — Set for BY_SERVICE on the unanswered breakdown: service calls in this group whose outcome is abandoned. abandoned + unanswered equals calls.
    - `unanswered` — number — Set for BY_SERVICE on the unanswered breakdown: service calls in this group whose outcome is unanswered.
    - `lost` — number — Set on the unanswered breakdowns (BY_SERVICE and BY_DISCONNECT_REASON): of this group's service calls, those that were the last of their phone call (no later service took the caller).
    - `lostAbandoned` — number — Set with lost: of this group's lost calls, those that were abandoned.
    - `lostUnanswered` — number — Set with lost: of this group's lost calls, those that ended unanswered.
    - `overflow` — number — Set with lost: of this group's service calls, those after which a later service call took the caller. lost + overflow = calls.
    - `calls` — number **(required)** — Service calls in this group; summed over the groups it is total.
    - `completed` — number — Set on the answered breakdowns: service calls in this group whose outcome is completed. completed + transferred equals calls.
    - `transferred` — number — Set on the answered breakdowns: service calls in this group whose outcome is transferred.
    - `avgWaitMs` — number — Average wait, ring included, milliseconds, over this group's service calls - this service's own wait, not the caller's across earlier services. Absent on an empty band. _(format=double)_
    - `maxWaitMs` — number — The longest wait, ring included, milliseconds. Absent on an empty band.
    - `totalWaitMs` — number — Sum of the group's waits in milliseconds; avgWaitMs times calls.
    - `avgTalkMs` — number — Average talk time, hold included, milliseconds. 0 on the unanswered breakdowns; absent on an empty band. _(format=double)_
    - `totalTalkMs` — number — Total talk time, hold included, milliseconds. 0 on the unanswered breakdowns.
    - `totalAnsweringAgentRingToAnswerMs` — number — Set on the answered breakdowns: sum of ServiceCallRow.answeringAgentRingToAnswerMs (from the first ring of the agent who answered to the answer, re-rings included), milliseconds, over the group's service calls that carry one.
    - `totalAnsweringAgentRingMs` — number — Set on the answered breakdowns: sum of ServiceCallRow.answeringAgentRingMs (how long the answering agent's phone actually rang), milliseconds, over the group's service calls that carry one.
    - `avgFinalPosition` — number — Set for BY_SERVICE: average queue position at answer on the answered breakdown; at exit over abandoned service calls only on the unanswered breakdown, the same basis as the unanswered summary's avgFinalPosition. _(format=double)_

**`GetUnansweredServiceLevelRequestContent`**

_Company resolution. `company` is accepted only with a service (S2S) token; PBX, API-key and XBS tokens carry the company in their claims and a `company` parameter is rejected._

- `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
  - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
    - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
  - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
  - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
    - _array of_ `string`
  - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
    - _array of_ `string`
  - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
    - _array of_ `OutcomeFilterValue`
  - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
    - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
  - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
    - _array of_ `number`
  - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
    - _array of_ `string`
  - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
  - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- `waitBandSeconds` — number — Width of each wait band, seconds; 20 when omitted. _(default=20; min=5; max=120)_
- `waitBandSteps` — number — Number of wait bands, the last one open-ended; 7 when omitted. _(default=7; min=1; max=60)_

**`GetUnansweredServiceLevelResponseContent`**

_Fields every windowed report response carries besides its figures. No freshness field: figures lag the live system by up to about a minute (file batching), and a page shows its own request time._

- `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
- `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
- `waitBandSeconds` — number **(required)** — The wait band width applied, seconds: the request's value, or 20.
- `waitBandSteps` — number **(required)** — The number of wait bands applied: the request's value, or 7.
- `base` — string **(required)** — Always "abandonedOrUnanswered": the base this ladder is computed over - abandoned and unanswered service calls together. Each band splits into lost and overflow.
- `total` — number **(required)** — Service calls in the base; the last band's cumulative count equals it.
- `lost` — number **(required)** — Of total, the lost service calls (no later service took the caller); the last band's cumulative lost equals it.
- `overflow` — number **(required)** — Of total, the overflow service calls (a later service call then took the caller). lost + overflow = total.
- `bands` — array **(required)**
  - _array of_ `ServiceLevelBand`
    - `withinSeconds` — number — The band's upper limit in seconds: count holds the calls whose wait was at most this. Absent on the open last band.
    - `count` — number **(required)** — Calls waiting at most withinSeconds: this band and all earlier ones.
    - `delta` — number **(required)** — Calls in this band only.
    - `lost` — number — Set on the abandoned-or-unanswered ladder: of count, the lost service calls (no later service took the caller), cumulative like count.
    - `lostDelta` — number — Set on the abandoned-or-unanswered ladder: of delta, the lost service calls.
    - `overflow` — number — Set on the abandoned-or-unanswered ladder: of count, the overflow service calls (a later service call then took the caller), cumulative like count. lost + overflow = count.
    - `overflowDelta` — number — Set on the abandoned-or-unanswered ladder: of delta, the overflow service calls. lostDelta + overflowDelta = delta.

**`GetUnansweredSummaryRequestContent`**

_Company resolution. `company` is accepted only with a service (S2S) token; PBX, API-key and XBS tokens carry the company in their claims and a `company` parameter is rejected._

- `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
  - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
    - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
  - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
  - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
    - _array of_ `string`
  - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
    - _array of_ `string`
  - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
    - _array of_ `OutcomeFilterValue`
  - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
    - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
  - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
    - _array of_ `number`
  - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
    - _array of_ `string`
  - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
  - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_

**`GetUnansweredSummaryResponseContent`**

_Fields every windowed report response carries besides its figures. No freshness field: figures lag the live system by up to about a minute (file batching), and a page shows its own request time._

- `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
- `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
- `abandoned` — number **(required)** — As counts.abandoned: nobody answered and the disconnect reason is a hang-up.
- `shortAbandoned` — number **(required)** — As counts.shortAbandoned: of abandoned, the calls that waited at most 5 seconds, ring included.
- `unanswered` — number **(required)** — As counts.unanswered: nobody answered and the wait ended for any other reason - a timeout, an empty queue, the caller leaving by a keypad option, a reason the classification does not name, or a hand-off before anyone answered (disconnect reason TRANSFER, FORWARD or PICKUP).
- `lost` — number **(required)** — Of the abandoned and unanswered service calls, those that were the last service call of their phone call: no later service took the caller. Summed over services it is the number of lost phone calls.
- `lostAbandoned` — number **(required)** — Of lost, those whose last service call was abandoned: its disconnect reason is a hang-up (see abandoned).
- `lostUnanswered` — number **(required)** — Of lost, those whose last service call ended unanswered (see unanswered). lostAbandoned + lostUnanswered = lost.
- `overflow` — number **(required)** — abandoned + unanswered - lost: service calls nobody answered here after which the phone call had a later service call (in another service, or the same one entered again). The caller may have been served there.
- `avgWaitMs` — number — Average wait, ring included, milliseconds, over abandoned and unanswered service calls together - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
- `maxWaitMs` — number — The longest wait, milliseconds, over abandoned and unanswered service calls. Absent when there is none.
- `abandonedAvgWaitMs` — number — Average wait in milliseconds over abandoned service calls only - how long callers held before giving up. avgWaitMs is over abandoned and unanswered service calls together. _(format=double)_
- `avgStartPosition` — number — Average queue position on entry, over abandoned service calls. _(format=double)_
- `avgFinalPosition` — number — Average queue position when the call ended, over abandoned service calls. _(format=double)_
- `sla` — UnansweredSlaCounts **(required)** — Abandoned-within counts: abandonedWithin / eligible is the share of the eligible service calls abandoned within thresholdSeconds. Both leave out the short abandons.
  - `thresholdSeconds` — number **(required)** — The default threshold that applied.
  - `abandonedWithin` — number **(required)** — Abandoned service calls whose wait is at most the threshold that applied to their service, without the short abandons (counts.shortAbandoned), which are outside eligible too.
  - `eligible` — number **(required)** — The denominator, the same as the distribution's sla.eligible: counts.offered minus counts.unknown minus counts.shortAbandoned.
  - `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. abandonedWithin is judged at each service's own threshold, so without this a reader cannot tell which targets produced it. Absent means one threshold applied to every service.
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- `unknown` — number **(required)** — As counts.unknown: service calls whose outcome could not be determined, left out of every figure above.

**`Granularity`**

_Time-bucketing axis. WEEK is ISO-8601, Monday-start. HOUR and DAY_OF_WEEK are recurring buckets (hour of day, ISO day 1-7) over the whole window._

- string _(enum: `hour`, `day`, `week`, `month`, `dayOfWeek`)_

**`HourRange`**

_A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to._

- `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
- `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_

**`ListDashboardsResponseContent`**

- `dashboards` — array **(required)**
  - _array of_ `Dashboard`
    - `name` — string **(required)** _(minLen=1; maxLen=128)_
    - `kind` — string **(required)** _(enum: `live`, `report`)_
    - `blocks` — array **(required)** _(maxItems=100)_
      - _array of_ `DashboardBlock`
        - _(nesting depth limit — see `DashboardBlock` in the Schemas appendix)_
    - `id` — string **(required)** — Chosen by the client, unique among the dashboards of the user. _(pattern=^[A-Za-z0-9_-]+$; minLen=1; maxLen=64)_
    - `createdBy` — string **(required)** — Who created the dashboard: the id of the user, or "system" for a predefined dashboard.
    - `predefined` — boolean — True for a dashboard the service gives every user (createdBy "system"), e.g. the Live view's Main. It is listed before the user's own, and cannot be changed or deleted: a user customises a copy of it (a new dashboard saved under a new id).
    - `createdAt` — string **(required)** — When the dashboard was first saved, ISO 8601.
    - `updatedAt` — string **(required)** — When the dashboard was last saved, ISO 8601.

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`OutcomeFilterValue`**

_The count names filter.outcomes accepts, each selecting the service calls of the ServiceCallCounts member of the same name (answered: completed + transferred)._

- string _(enum: `offered`, `received`, `answered`, `completed`, `transferred`, `abandoned`, `unanswered`, `unknown`, `lost`, `lostAbandoned`, `lostUnanswered`, `overflow`)_

**`PeriodBucket`**

_One bucket. bucketKey is HH:00 for HOUR, 1-7 for DAY_OF_WEEK (ISO, Monday = 1), YYYY-MM-DD, YYYY-Www or YYYY-MM otherwise; sortKey orders the series; bucketStart is the bucket's local start and is set for DAY, WEEK and MONTH only._

- `bucketKey` — string **(required)** — HH:00 for HOUR, 1-7 for DAY_OF_WEEK (ISO, Monday = 1), YYYY-MM-DD for DAY, YYYY-Www for WEEK, YYYY-MM for MONTH.
- `sortKey` — number **(required)** — Orders the series.
- `bucketStart` — string — The bucket's local start. Set for DAY, WEEK and MONTH only. _(format=date-time)_
- `metrics` — DistributionMetrics **(required)** — The distribution metric block. Every figure here is per service call: a call that went through several services counts in each service with that service's own wait and ringing; the caller's totals across services are on the call list (ServiceCallRow.totalQueueWaitMs and totalQueueRingMs). Waits are over complete service calls; talk is over answered and transferred service calls and includes on-call hold. The service's ring time is avgRingMs: how long agents were being rung for the caller, from the first ring to an answer or the end of the wait; the wait minus it is the time before the first agent was rung. avgAnsweringAgentRingToAnswerMs and avgAnsweringAgentRingMs describe the agent who answered. Averages are null when the base is empty.
  - `counts` — ServiceCallCounts **(required)** — Service call counts by outcome. Each service call (one phone call's stay in one service) counts on its own; a phone call that went through two services is two service calls. completed + transferred + abandoned + unanswered + unknown = offered: the calls whose outcome could not be determined stay in the total, as a count of their own, and are left out of every average and SLA figure. Averages are computed by the service; percentages are left to the client, because every count they need is returned.
    - `offered` — number **(required)** — Every service call in the window, all outcomes, unknown included.
    - `received` — number **(required)** — The service calls that ended in this service, offered - overflow = completed + transferred + lost + unknown. An unknown service call counts as received even when a later service took the caller. Not unique phone calls: a call answered in one service and transferred into another counts in both.
    - `completed` — number **(required)** — Service calls an agent answered and kept: the disconnect reason is neither TRANSFER nor FORWARD. Outcome value completed.
    - `transferred` — number **(required)** — Service calls an agent answered and then handed on (disconnect reason TRANSFER or FORWARD). answered = completed + transferred.
    - `abandoned` — number **(required)** — Service calls nobody answered whose disconnect reason is a hang-up: the caller hung up, or a rule took the call out of the queue.
    - `shortAbandoned` — number **(required)** — Of abandoned, the service calls whose wait, ring included, was at most 5 seconds. Included in abandoned, not an extra outcome.
    - `unanswered` — number **(required)** — Service calls nobody answered that ended for any other reason - a timeout, an empty queue, the caller leaving by a keypad option, a reason the classification does not name, or a hand-off before anyone answered (disconnect reason TRANSFER, FORWARD or PICKUP).
    - `unknown` — number **(required)** — Service calls whose outcome could not be determined from their events. Outcome value unknown; their events can be read with GetServiceCallEvents. Counted in offered and received; left out of every average and SLA figure, because their wait and outcome are not known.
    - `lost` — number **(required)** — Of the abandoned and unanswered service calls, those that were the last service call of their phone call: no later service took the caller. Summed over services it is the number of lost phone calls.
    - `lostAbandoned` — number **(required)** — Of lost, those whose last service call was abandoned: its disconnect reason is a hang-up (see abandoned).
    - `lostUnanswered` — number **(required)** — Of lost, those whose last service call ended unanswered (see unanswered). lostAbandoned + lostUnanswered = lost.
    - `overflow` — number **(required)** — abandoned + unanswered - lost: service calls nobody answered here after which the phone call had a later service call (in another service, or the same one entered again). The caller may have been served there.
  - `avgWaitMs` — number — Average wait, ring included, milliseconds, over the service calls whose outcome could be determined (every outcome; unknown left out) - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs). Absent when there is none. _(format=double)_
  - `maxWaitMs` — number — The longest wait, ring included, milliseconds, over the same service calls as avgWaitMs. Absent when there is none.
  - `avgTalkMs` — number — Average talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none. _(format=double)_
  - `totalTalkMs` — number — Total talk time, hold included, milliseconds, over completed and transferred service calls. Absent when there is none.
  - `avgRingMs` — number — The service's ring time. Average time from the first ring to any agent to the answer, or to the end of the service call when nobody answered, milliseconds, over the service calls whose outcome could be determined (answered, abandoned and unanswered together; unknown left out) that rang at least one agent; stretches with no agent ringing are included (ServiceCallRow.ringMs). Absent when there is none. _(format=double)_
  - `avgAnsweringAgentRingToAnswerMs` — number — Average time from the first ring of the agent who answered to the answer, milliseconds, over completed and transferred service calls that carry one; re-rings, and any stretches in between when that agent's phone was not ringing, are included (ServiceCallRow.answeringAgentRingToAnswerMs). Absent when there is none. _(format=double)_
  - `avgAnsweringAgentRingMs` — number — Average of how long the answering agent's phone actually rang, its rings added up, milliseconds, over completed and transferred service calls that carry one (ServiceCallRow.answeringAgentRingMs). Absent when there is none. _(format=double)_
  - `maxStartPosition` — number **(required)** — The highest place in line any caller had on joining, over every service call, unknown included. The highest place could be treated as the maximum number of callers waiting in the queue. With several services in the filter, the busiest service's figure.
  - `maxStartPositionAnswered` — number **(required)** — The deepest place in line on joining, over answered and transferred service calls.
  - `maxStartPositionAbandonedOrUnanswered` — number **(required)** — The deepest place in line on joining, over abandoned and unanswered service calls.
  - `maxFinalPositionAbandoned` — number **(required)** — The deepest place in line when the caller hung up while waiting (abandoned).
  - `maxFinalPositionUnanswered` — number **(required)** — The deepest place in line when the wait ended unanswered (see ServiceCallCounts.unanswered).
  - `sla` — SlaCounts **(required)** — Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds.
    - `thresholdSeconds` — number **(required)** — The default threshold that applied; on a by-service group, that service's own threshold.
    - `answeredWithin` — number **(required)** — Completed or transferred service calls whose wait, ring included, is at most the threshold that applied to their service - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs).
    - `eligible` — number **(required)** — The SLA denominator: counts.offered minus counts.unknown minus counts.shortAbandoned - the calls whose outcome could be determined, without the calls abandoned within 5 seconds, which gave the service no time to answer.
    - `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. Absent means one threshold applied to every service.
      - _array of_ `ServiceSlaSeconds`
        - _(nesting depth limit — see `ServiceSlaSeconds` in the Schemas appendix)_

**`PutDashboardRequestContent`**

_Company resolution. `company` is accepted only with a service (S2S) token; PBX, API-key and XBS tokens carry the company in their claims and a `company` parameter is rejected._

- `name` — string **(required)** _(minLen=1; maxLen=128)_
- `kind` — string **(required)** _(enum: `live`, `report`)_
- `blocks` — array **(required)** _(maxItems=100)_
  - _array of_ `DashboardBlock`
    - `id` — string **(required)** _(minLen=1; maxLen=64)_
    - `type` — string **(required)** _(enum: `chart`, `note`)_
    - `position` — DashboardBlockPosition **(required)** — Place of a block in the 12-column canvas grid.
      - `x` — number **(required)** _(min=0)_
      - `y` — number **(required)** _(min=0)_
      - `w` — number **(required)** _(min=1)_
      - `h` — number **(required)** _(min=1)_
    - `chartId` — string — The catalog chart shown by the block; required when type is chart. _(minLen=1; maxLen=128)_
    - `config` — DashboardBlockConfig — Data settings of a chart block (e.g. entity, queue), opaque to the service.
      - _map of_ `string`
    - `text` — string — The note; only with type note. It may be empty: a user can add a note before writing it. _(maxLen=2000)_

**`PutDashboardResponseContent`**

- `dashboard` — Dashboard **(required)**
  - `name` — string **(required)** _(minLen=1; maxLen=128)_
  - `kind` — string **(required)** _(enum: `live`, `report`)_
  - `blocks` — array **(required)** _(maxItems=100)_
    - _array of_ `DashboardBlock`
      - `id` — string **(required)** _(minLen=1; maxLen=64)_
      - `type` — string **(required)** _(enum: `chart`, `note`)_
      - `position` — DashboardBlockPosition **(required)** — Place of a block in the 12-column canvas grid.
        - _(nesting depth limit — see `DashboardBlockPosition` in the Schemas appendix)_
      - `chartId` — string — The catalog chart shown by the block; required when type is chart. _(minLen=1; maxLen=128)_
      - `config` — DashboardBlockConfig — Data settings of a chart block (e.g. entity, queue), opaque to the service.
        - _(nesting depth limit — see `DashboardBlockConfig` in the Schemas appendix)_
      - `text` — string — The note; only with type note. It may be empty: a user can add a note before writing it. _(maxLen=2000)_
  - `id` — string **(required)** — Chosen by the client, unique among the dashboards of the user. _(pattern=^[A-Za-z0-9_-]+$; minLen=1; maxLen=64)_
  - `createdBy` — string **(required)** — Who created the dashboard: the id of the user, or "system" for a predefined dashboard.
  - `predefined` — boolean — True for a dashboard the service gives every user (createdBy "system"), e.g. the Live view's Main. It is listed before the user's own, and cannot be changed or deleted: a user customises a copy of it (a new dashboard saved under a new id).
  - `createdAt` — string **(required)** — When the dashboard was first saved, ISO 8601.
  - `updatedAt` — string **(required)** — When the dashboard was last saved, ISO 8601.

**`QueryServiceCallsRequestContent`**

_Company resolution. `company` is accepted only with a service (S2S) token; PBX, API-key and XBS tokens carry the company in their claims and a `company` parameter is rejected._

- `filter` — ReportFilter **(required)** — What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction.
  - `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
    - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
    - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
  - `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
  - `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
    - _array of_ `string`
  - `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
    - _array of_ `string`
  - `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
    - _array of_ `OutcomeFilterValue`
  - `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
    - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
    - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
  - `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
    - _array of_ `number`
  - `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
    - `from` — number **(required)** _(min=0; max=86400)_
    - `to` — number _(min=1; max=86400)_
  - `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
    - _array of_ `string`
  - `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
  - `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
    - _array of_ `ServiceSlaSeconds`
      - `serviceId` — string **(required)** — The service this threshold applies to.
      - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_
- `cursor` — string — The previous page's nextCursor, passed back unchanged; omit it, or send it empty, for the first page. _(maxLen=2048)_
- `limit` — number — Rows per page, 1 to 200; 50 when omitted. _(default=50; min=1; max=200)_
- `callId` — string — Only the service calls of this phone call (its callId, the session id shared by every service call of the phone call), so a drill-down can show every service call of a call that overflowed from one service to another. The window and the other filter members still apply; a key lookup, however long the window.

**`QueryServiceCallsResponseContent`**

_Fields every windowed report response carries besides its figures. No freshness field: figures lag the live system by up to about a minute (file batching), and a page shows its own request time._

- `timeZone` — string **(required)** — The IANA timezone the dates and buckets of this response are in - the PBX's own zone unless the request named one of the zones that PBX has stamped.
- `pbx` — string **(required)** — The PBX serial this response covers - from `filter.pbx` or from the caller's token.
- `items` — array **(required)**
  - _array of_ `ServiceCallRow`
    - `callId` — string **(required)** — The phone call's id (its session id), shared by every service call of the call. Not this row's own id: with flowIndex and serviceId it identifies the row.
    - `flowIndex` — number **(required)** — The PBX's step number of this service call within the phone call. Not a count of service calls and not guaranteed to be consecutive (see serviceCallsCount). With callId and serviceId it identifies the row.
    - `serviceId` — string **(required)** — The service of this service call.
    - `serviceName` — string — The service's name as stored with the call. Absent when the PBX sent none.
    - `enteredAt` — string **(required)** — When the caller joined the service's queue. _(format=date-time)_
    - `answeredAt` — string — When an agent answered. Absent when nobody did. _(format=date-time)_
    - `endedAt` — string **(required)** — When this service call ended: the caller left the service's queue, or the answered call ended. _(format=date-time)_
    - `waitMs` — number **(required)** — Wait from entering the queue to the answer or the exit, milliseconds; the ring is inside it.
    - `ringMs` — number — The ringing in this service call, milliseconds: from the first ring to any agent to the answer, or to the end of the service call when nobody answered; stretches with no phone ringing are included. It is inside waitMs; waitMs minus ringMs is the time before the first agent was rung. Absent when no agent was rung.
    - `answeringAgentRingToAnswerMs` — number — In this service call, the time from the first ring of the agent who answered to the answer, milliseconds; re-rings, and any stretches in between when that agent's phone was not ringing, are included. Absent when nobody answered, or when no ring was recorded for that agent.
    - `answeringAgentRingMs` — number — In this service call, how long the answering agent's phone actually rang, milliseconds: each ring of that agent lasts until the next event that names that agent (its cancel or the answer) or names no agent at all, and the rings are added up. Absent when nobody answered, or when no ring was recorded for that agent.
    - `talkMs` — number **(required)** — Talk time from the answer to the end, hold included, milliseconds; 0 when nobody answered.
    - `durationMs` — number **(required)** — The whole span of this service call, milliseconds: from joining the queue to the service call's end, waitMs plus talkMs (the whole unit, as the stream API means duration; the talk time alone is talkMs).
    - `answered` — boolean **(required)** — True exactly when an agent of the service answered: outcome completed or transferred; an unknown row can have answered true.
    - `answeredByAgentId` — string — The agent who answered - the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent when nobody answered.
    - `answeredByName` — string — The answering user's name as stored with the call (the name it had then). Absent when nobody answered.
    - `answeredByExtension` — string — The answering user's extension. Absent when nobody answered.
    - `agentsRung` — number **(required)** — How many different agents the service rang during this service call, whether or not they picked up.
    - `startPosition` — number — The caller's place in line on joining the service's queue, as the PBX sends it (1 = first in line). Absent when the PBX did not send it.
    - `finalPosition` — number — The caller's place in line when the wait ended (answer, hang-up or exit), as the PBX sends it. Absent when the PBX did not send it.
    - `outcome` — string **(required)** — completed | transferred | abandoned | unanswered | unknown. An open vocabulary: a client must tolerate a value not listed here. unknown: the outcome could not be determined from the service call's events (see ServiceCallCounts.unknown); such a row is outside every average and every SLA figure.
    - `disconnectReason` — string — The reason the call left the service, as the PBX gave it on the END event, upper-cased: HANGUP, TRANSFER, FORWARD, PICKUP, TIMEOUT, EMPTY, EXITWITHKEY, COMPATIBILITY, UNKNOWN. Absent when the END carried none. filter.disconnectReasons selects by it. The outcome follows the answer, not the reason: answered then TRANSFER or FORWARD is transferred; nobody answered is abandoned for HANGUP and unanswered for every other reason, a hand-off (TRANSFER, FORWARD, PICKUP) included.
    - `callerPhone` — string — The caller's number as the PBX received it. Absent when the PBX sent none.
    - `callerName` — string — The caller's name as the PBX received it. Absent when the PBX sent none.
    - `lost` — boolean — Set on abandoned and unanswered rows only: true when this was the last service call of its phone call (lost), false when a later service call then took the caller (overflow). Absent on every other row.
    - `totalQueueWaitMs` — number **(required)** — The caller's total queue wait: the sum of waitMs over every service call of this phone call. The same value on every row of the call. It covers the waiting time inside the services' queues only - not the IVR before the first service or between services. Computed when the page is read, so it grows if a later service call arrives. It includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
    - `totalQueueRingMs` — number **(required)** — The caller's total ringing: the sum of ringMs over every service call of this phone call. The same value on every row of the call; a service call without ringMs adds 0. Computed when the page is read, so it grows if a later service call arrives. It includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
    - `serviceCallsCount` — number **(required)** — How many service calls this phone call has: 1 when it stayed in one service; the same service entered twice counts 2. Like totalQueueWaitMs and totalQueueRingMs, it includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
- `nextCursor` — string — Cursor for the next page; absent on the last page.

**`ReportDate`**

_The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available._

- `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
- `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
- `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.

**`ReportFilter`**

_What a report is computed over - the window, the scope and the SLA thresholds - as one object. An omitted or empty list means no restriction._

- `date` — ReportDate **(required)** — The report window. Both dates are inclusive calendar days in `timeZone`; from == to is one day. Windows longer than 90 days are rejected with 400. The data is planned to be kept for 3 months: do not rely on older calls being available.
  - `from` — string **(required)** — First day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
  - `to` — string **(required)** — Last day of the window, YYYY-MM-DD, inclusive. _(pattern=^\d{4}-\d{2}-\d{2}$)_
  - `timeZone` — string — IANA timezone the dates and buckets are interpreted in. Defaults to the PBX's own zone. Must be a zone the PBX has stamped on its calls and one the database knows; any other zone is rejected with 400 naming the accepted ones. Echoed in every response as timeZone.
- `pbx` — string — Serial of the PBX the report is about. A report covers one PBX. With a user or PBX token, any PBX of the token's company, and the token's own PBX when omitted; a PBX of another company gives an empty report. Required with a service or API-key token.
- `serviceIds` — array — Services (call groups, queues) to include, by id. _(maxItems=1000)_
  - _array of_ `string`
- `extensions` — array — Users to include, by extension, e.g. ["101", "102"], across every service: the calls one of them answered, and the calls nobody answered (abandoned, unanswered or unknown, a hand-off before anyone answered included) that rang one of them, alone or among several users. A call that rang several of the named users counts once. Only all-digit extensions are accepted; any other entry is rejected with 400. _(maxItems=1000)_
  - _array of_ `string`
- `outcomes` — array — Keep the calls of the counts named, combined with OR: a call matching several values is listed once. The filter takes 12 count names; ServiceCallRow.outcome has only 5 stored values, so do not map one onto the other. Each value selects exactly the calls of the ServiceCallCounts member of the same name (answered: completed + transferred, which has no member of its own), under the same other filters: offered (every call: completed + transferred + abandoned + unanswered + unknown; the same as no outcomes), received (offered - overflow), answered (completed + transferred), completed, transferred, abandoned, unanswered, lost (lostAbandoned + lostUnanswered), lostAbandoned, lostUnanswered, overflow (abandoned + unanswered - lost), unknown (calls whose outcome could not be determined). Repeated or overlapping values are allowed: the result is their union, and a selection that keeps every call (e.g. received + overflow) is answered as offered. Filters on different members combine with AND; a combination no call can match returns an empty result, not an error. lost, overflow and received are judged over the whole phone call, whatever services the request names. A closed list: any other value is rejected with 400. ServiceCallRow.outcome keeps its own five values: a lost or overflow row shows abandoned or unanswered. SLOW PATH like hourRange on every aggregate, except a selection that keeps every call, answered as offered from the daily rows; the call list reads off the index, but a value that matches few calls can read the whole window before a page fills. _(maxItems=1000)_
  - _array of_ `OutcomeFilterValue`
- `hourRange` — HourRange — A time-of-day window on the time the call entered the service's queue, in the report's timezone. from is inclusive, to exclusive, both HH:MM (24-hour); to may be 24:00; from must be before to.
  - `from` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
  - `to` — string **(required)** _(pattern=^(([01]\d|2[0-3]):[0-5]\d|24:00)$)_
- `daysOfWeek` — array — ISO weekdays to include, 1 = Monday to 7 = Sunday, judged on the queue entry time in the report's timezone - the drill-down of a day-of-week row. SLOW PATH like hourRange: computed from the individual calls of the whole window on every operation.
  - _array of_ `number`
- `waitSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
  - `from` — number **(required)** _(min=0; max=86400)_
  - `to` — number _(min=1; max=86400)_
- `talkSecondsRange` — SecondsRange — A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut.
  - `from` — number **(required)** _(min=0; max=86400)_
  - `to` — number _(min=1; max=86400)_
- `disconnectReasons` — array — Keep only the calls of the BreakdownGroup.disconnectReason values listed, matched exactly as either breakdown by disconnect reason (answered or unanswered) returns them; with outcomes [the row's outcome] it selects one disconnect-reason row; send an empty string for the group without a reason - the drill-down of a disconnect-reason row. SLOW PATH like hourRange on every aggregate. _(maxItems=1000)_
  - _array of_ `string`
- `slaSeconds` — number — SLA threshold in seconds. A service call is within SLA when it was answered and its wait, ring included, is at most this many seconds. The default for every service not named in serviceSlaSeconds. A multiple of 5 from 5 to 120 (the stored wait histogram has 5-second slots to 120 s); any other value is rejected with 400. 20 when omitted. _(default=20; min=5; max=120)_
- `serviceSlaSeconds` — array — Per-service SLA thresholds overriding slaSeconds for the services named. Each service call is judged at its own service's threshold; the unanswered summary's abandonedWithin uses the same targets. A serviceId with no service call in the window is ignored; a duplicate serviceId is rejected with 400. Each threshold is a multiple of 5 from 5 to 120; any other value is rejected with 400. _(maxItems=1000)_
  - _array of_ `ServiceSlaSeconds`
    - `serviceId` — string **(required)** — The service this threshold applies to.
    - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_

**`SecondsRange`**

_A right-closed band of seconds, the ladders' own: more than from and at most to, except that a band from 0 includes a zero value (the ladders put zero in their first band); to omitted means no upper bound. from is 0 or more and below to. Waits are judged in milliseconds against the band's seconds; talk times on whole seconds (floor), as the talk-time bands are cut._

- `from` — number **(required)** _(min=0; max=86400)_
- `to` — number _(min=1; max=86400)_

**`ServiceCallCounts`**

_Service call counts by outcome. Each service call (one phone call's stay in one service) counts on its own; a phone call that went through two services is two service calls. completed + transferred + abandoned + unanswered + unknown = offered: the calls whose outcome could not be determined stay in the total, as a count of their own, and are left out of every average and SLA figure. Averages are computed by the service; percentages are left to the client, because every count they need is returned._

- `offered` — number **(required)** — Every service call in the window, all outcomes, unknown included.
- `received` — number **(required)** — The service calls that ended in this service, offered - overflow = completed + transferred + lost + unknown. An unknown service call counts as received even when a later service took the caller. Not unique phone calls: a call answered in one service and transferred into another counts in both.
- `completed` — number **(required)** — Service calls an agent answered and kept: the disconnect reason is neither TRANSFER nor FORWARD. Outcome value completed.
- `transferred` — number **(required)** — Service calls an agent answered and then handed on (disconnect reason TRANSFER or FORWARD). answered = completed + transferred.
- `abandoned` — number **(required)** — Service calls nobody answered whose disconnect reason is a hang-up: the caller hung up, or a rule took the call out of the queue.
- `shortAbandoned` — number **(required)** — Of abandoned, the service calls whose wait, ring included, was at most 5 seconds. Included in abandoned, not an extra outcome.
- `unanswered` — number **(required)** — Service calls nobody answered that ended for any other reason - a timeout, an empty queue, the caller leaving by a keypad option, a reason the classification does not name, or a hand-off before anyone answered (disconnect reason TRANSFER, FORWARD or PICKUP).
- `unknown` — number **(required)** — Service calls whose outcome could not be determined from their events. Outcome value unknown; their events can be read with GetServiceCallEvents. Counted in offered and received; left out of every average and SLA figure, because their wait and outcome are not known.
- `lost` — number **(required)** — Of the abandoned and unanswered service calls, those that were the last service call of their phone call: no later service took the caller. Summed over services it is the number of lost phone calls.
- `lostAbandoned` — number **(required)** — Of lost, those whose last service call was abandoned: its disconnect reason is a hang-up (see abandoned).
- `lostUnanswered` — number **(required)** — Of lost, those whose last service call ended unanswered (see unanswered). lostAbandoned + lostUnanswered = lost.
- `overflow` — number **(required)** — abandoned + unanswered - lost: service calls nobody answered here after which the phone call had a later service call (in another service, or the same one entered again). The caller may have been served there.

**`ServiceCallEvent`**

_One raw lifecycle event of a service call: one entry of the stream API's actions list, one event per agent the entry names. time can be in whole seconds on some calls._

- `time` — string **(required)** — When the PBX recorded this event. _(format=date-time)_
- `action` — string **(required)** — INIT | RING | CANCEL | ANSWER | END, upper-cased.
- `reason` — string — The raw reason the PBX gave for this event, upper-cased (END and CANCEL carry one); on END it is the row's disconnectReason. Absent when there is none.
- `agentId` — string — The agent this event concerns - rung, or answering: the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent on events without an agent.
- `userName` — string — That user's name as stored with the event. Absent on events without an agent.
- `userExtension` — string — That user's extension. Absent on events without an agent.
- `queuePosition` — number — The caller's place in line at this event, as the PBX sends it. Absent when the PBX did not send it.

**`ServiceCallRow`**

_One service call: one phone call's stay in one service (one flow of the call in that service). Ring is nested inside wait; talk includes hold. callerPhone and callerName can be absent; absent does not mean the call had no caller. A call that went from one service to another is several service calls sharing callId (one per service); every report counts each of them on its own._

- `callId` — string **(required)** — The phone call's id (its session id), shared by every service call of the call. Not this row's own id: with flowIndex and serviceId it identifies the row.
- `flowIndex` — number **(required)** — The PBX's step number of this service call within the phone call. Not a count of service calls and not guaranteed to be consecutive (see serviceCallsCount). With callId and serviceId it identifies the row.
- `serviceId` — string **(required)** — The service of this service call.
- `serviceName` — string — The service's name as stored with the call. Absent when the PBX sent none.
- `enteredAt` — string **(required)** — When the caller joined the service's queue. _(format=date-time)_
- `answeredAt` — string — When an agent answered. Absent when nobody did. _(format=date-time)_
- `endedAt` — string **(required)** — When this service call ended: the caller left the service's queue, or the answered call ended. _(format=date-time)_
- `waitMs` — number **(required)** — Wait from entering the queue to the answer or the exit, milliseconds; the ring is inside it.
- `ringMs` — number — The ringing in this service call, milliseconds: from the first ring to any agent to the answer, or to the end of the service call when nobody answered; stretches with no phone ringing are included. It is inside waitMs; waitMs minus ringMs is the time before the first agent was rung. Absent when no agent was rung.
- `answeringAgentRingToAnswerMs` — number — In this service call, the time from the first ring of the agent who answered to the answer, milliseconds; re-rings, and any stretches in between when that agent's phone was not ringing, are included. Absent when nobody answered, or when no ring was recorded for that agent.
- `answeringAgentRingMs` — number — In this service call, how long the answering agent's phone actually rang, milliseconds: each ring of that agent lasts until the next event that names that agent (its cancel or the answer) or names no agent at all, and the rings are added up. Absent when nobody answered, or when no ring was recorded for that agent.
- `talkMs` — number **(required)** — Talk time from the answer to the end, hold included, milliseconds; 0 when nobody answered.
- `durationMs` — number **(required)** — The whole span of this service call, milliseconds: from joining the queue to the service call's end, waitMs plus talkMs (the whole unit, as the stream API means duration; the talk time alone is talkMs).
- `answered` — boolean **(required)** — True exactly when an agent of the service answered: outcome completed or transferred; an unknown row can have answered true.
- `answeredByAgentId` — string — The agent who answered - the user as a member of this service, <company>_<pbx>_<service>_<extension>. Absent when nobody answered.
- `answeredByName` — string — The answering user's name as stored with the call (the name it had then). Absent when nobody answered.
- `answeredByExtension` — string — The answering user's extension. Absent when nobody answered.
- `agentsRung` — number **(required)** — How many different agents the service rang during this service call, whether or not they picked up.
- `startPosition` — number — The caller's place in line on joining the service's queue, as the PBX sends it (1 = first in line). Absent when the PBX did not send it.
- `finalPosition` — number — The caller's place in line when the wait ended (answer, hang-up or exit), as the PBX sends it. Absent when the PBX did not send it.
- `outcome` — string **(required)** — completed | transferred | abandoned | unanswered | unknown. An open vocabulary: a client must tolerate a value not listed here. unknown: the outcome could not be determined from the service call's events (see ServiceCallCounts.unknown); such a row is outside every average and every SLA figure.
- `disconnectReason` — string — The reason the call left the service, as the PBX gave it on the END event, upper-cased: HANGUP, TRANSFER, FORWARD, PICKUP, TIMEOUT, EMPTY, EXITWITHKEY, COMPATIBILITY, UNKNOWN. Absent when the END carried none. filter.disconnectReasons selects by it. The outcome follows the answer, not the reason: answered then TRANSFER or FORWARD is transferred; nobody answered is abandoned for HANGUP and unanswered for every other reason, a hand-off (TRANSFER, FORWARD, PICKUP) included.
- `callerPhone` — string — The caller's number as the PBX received it. Absent when the PBX sent none.
- `callerName` — string — The caller's name as the PBX received it. Absent when the PBX sent none.
- `lost` — boolean — Set on abandoned and unanswered rows only: true when this was the last service call of its phone call (lost), false when a later service call then took the caller (overflow). Absent on every other row.
- `totalQueueWaitMs` — number **(required)** — The caller's total queue wait: the sum of waitMs over every service call of this phone call. The same value on every row of the call. It covers the waiting time inside the services' queues only - not the IVR before the first service or between services. Computed when the page is read, so it grows if a later service call arrives. It includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
- `totalQueueRingMs` — number **(required)** — The caller's total ringing: the sum of ringMs over every service call of this phone call. The same value on every row of the call; a service call without ringMs adds 0. Computed when the page is read, so it grows if a later service call arrives. It includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.
- `serviceCallsCount` — number **(required)** — How many service calls this phone call has: 1 when it stayed in one service; the same service entered twice counts 2. Like totalQueueWaitMs and totalQueueRingMs, it includes service calls in services outside the request's service filter, and service calls whose outcome could not be determined.

**`ServiceLevelBand`**

_One band of a cumulative service-level ladder. count is cumulative (this band and every earlier one); delta is this band's own; withinSeconds is null on the open-ended last band._

- `withinSeconds` — number — The band's upper limit in seconds: count holds the calls whose wait was at most this. Absent on the open last band.
- `count` — number **(required)** — Calls waiting at most withinSeconds: this band and all earlier ones.
- `delta` — number **(required)** — Calls in this band only.
- `lost` — number — Set on the abandoned-or-unanswered ladder: of count, the lost service calls (no later service took the caller), cumulative like count.
- `lostDelta` — number — Set on the abandoned-or-unanswered ladder: of delta, the lost service calls.
- `overflow` — number — Set on the abandoned-or-unanswered ladder: of count, the overflow service calls (a later service call then took the caller), cumulative like count. lost + overflow = count.
- `overflowDelta` — number — Set on the abandoned-or-unanswered ladder: of delta, the overflow service calls. lostDelta + overflowDelta = delta.

**`ServiceSlaSeconds`**

_One service's SLA threshold._

- `serviceId` — string **(required)** — The service this threshold applies to.
- `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_

**`SlaCounts`**

_Counts, not a percentage: the service level is answeredWithin divided by eligible. Over several services or periods, add the counts first and divide once; never average percentages. eligible already leaves out the service calls of unknown outcome and the short abandons - do not subtract counts.unknown or counts.shortAbandoned again; show 'no calls' rather than 0 % when eligible is 0. answeredWithin counts completed and transferred service calls whose wait is at most thresholdSeconds._

- `thresholdSeconds` — number **(required)** — The default threshold that applied; on a by-service group, that service's own threshold.
- `answeredWithin` — number **(required)** — Completed or transferred service calls whose wait, ring included, is at most the threshold that applied to their service - this service's own wait, not the caller's wait across earlier services (the caller's whole wait across services is ServiceCallRow.totalQueueWaitMs).
- `eligible` — number **(required)** — The SLA denominator: counts.offered minus counts.unknown minus counts.shortAbandoned - the calls whose outcome could be determined, without the calls abandoned within 5 seconds, which gave the service no time to answer.
- `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. Absent means one threshold applied to every service.
  - _array of_ `ServiceSlaSeconds`
    - `serviceId` — string **(required)** — The service this threshold applies to.
    - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_

**`TalkTimeBand`**

_A talk-time band: bandNo from 1, fromSeconds inclusive, toSeconds inclusive and null on the open-ended last band._

- `bandNo` — number **(required)** — Band number, from 1.
- `fromSeconds` — number **(required)** — Lowest whole second of talk in the band. Band 1 starts at 1 but also holds the calls with under 1 s of talk.
- `toSeconds` — number — Highest whole second of talk in the band. Absent on the last band.

**`UnansweredBreakdownDimension`**

_The grain of the unanswered breakdown: one group per service, or one group per outcome and raw END reason._

- string _(enum: `byService`, `byDisconnectReason`)_

**`UnansweredSlaCounts`**

_Abandoned-within counts: abandonedWithin / eligible is the share of the eligible service calls abandoned within thresholdSeconds. Both leave out the short abandons._

- `thresholdSeconds` — number **(required)** — The default threshold that applied.
- `abandonedWithin` — number **(required)** — Abandoned service calls whose wait is at most the threshold that applied to their service, without the short abandons (counts.shortAbandoned), which are outside eligible too.
- `eligible` — number **(required)** — The denominator, the same as the distribution's sla.eligible: counts.offered minus counts.unknown minus counts.shortAbandoned.
- `serviceSlaSeconds` — array — Present only when the request sent serviceSlaSeconds: the overrides that actually applied, i.e. for services with at least one service call in the window. abandonedWithin is judged at each service's own threshold, so without this a reader cannot tell which targets produced it. Absent means one threshold applied to every service.
  - _array of_ `ServiceSlaSeconds`
    - `serviceId` — string **(required)** — The service this threshold applies to.
    - `slaSeconds` — number **(required)** — This service's SLA threshold, seconds; the same rules as filter.slaSeconds. _(min=5; max=120)_

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

</details>
