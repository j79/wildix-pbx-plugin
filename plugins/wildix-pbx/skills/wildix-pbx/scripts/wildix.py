#!/usr/bin/env python3
"""
wildix.py — client en ligne de commande pour les API Wildix (PBX WMS, x-bees,
WDA, WIM, Auth…). Bibliothèque standard uniquement (aucune dépendance).

Sous-commandes :
  login     enregistre un profil (domaine PBX + Company API Key + token PBX optionnel)
  profiles  liste les profils enregistrés (secrets masqués)
  use       choisit le profil actif
  logout    supprime un profil (ou tous avec --all)
  whoami    teste les accès du profil actif
  apis      liste les alias d'API et leurs adresses de base
  call      exécute une requête HTTP (écritures bloquées sans --yes)
  doc       consulte la référence embarquée (apis | search | show | schema)

Les secrets sont stockés hors du dossier de travail, dans un fichier 0600
situé dans le répertoire temporaire du système (effacé au redémarrage), sauf
si WILDIX_PBX_STATE est défini.
"""
import argparse
import base64
import json
import os
import re
import signal
import ssl
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REF_DIR = os.path.normpath(os.path.join(HERE, "..", "references"))

# --------------------------------------------------------------------------
# Alias d'API -> adresse de base. "{pbx}" = domaine du PBX du profil actif.
# --------------------------------------------------------------------------
APIS = {
    "pbx":         ("https://{pbx}",                      "PBX WMS (API v1 historique + Cloud PBX Server API). Chemins sans /api/ → préfixe /api/v1 ajouté.", ["pbx-api", "cloud-pbx-server-api"]),
    "wms":         ("https://wms-api.wildix.com",         "Cloud PBX API (permissions ACL)", ["cloud-pbx-api"]),
    "xbees":       ("https://api.x-bees.com",             "x-bees : Conversations, Assistant, Kite, Users & ChatBots", ["conversations-api", "assistant-api", "kite-api", "users-and-chatbots-api"]),
    "wda":         ("https://wda.wildix.com",             "WDA : History, Insights, Stream, x-caracal", ["history-api", "insights-api", "stream-api", "x-caracal-api"]),
    "wilma":       ("https://api.wilma.wildix.com",       "Wilma : Agents, Artifacts, Assistant, Audit, Chat, Copilot, Copilot Sessions, Sandbox, Secrets, Skills, Tools, Traces, Voice, Workflows",
                    ["wilma-agents-api", "wilma-artifacts-api", "wilma-assistant-api", "wilma-audit-api", "wilma-chat-api", "wilma-copilot-api",
                     "wilma-copilot-sessions-api", "wilma-sandbox-api", "wilma-secrets-api", "wilma-skills-api", "wilma-tools-api",
                     "wilma-traces-api", "wilma-voice-api", "wilma-workflows-api"]),
    "wim":         ("https://wim.wildix.com",             "WIM : Integrations, Calendar, Cache, VoiceBots", ["integrations-api", "calendar-api", "cache-api", "voicebots-api"]),
    "kb":          ("https://kb.wim.wildix.com",          "Knowledge Base", ["knowledge-base-api"]),
    "wim-tools":   ("https://tools.wim.wildix.com",       "Wim Tools", ["wim-tools-api"]),
    "auth":        ("https://auth.wildix.com",            "Auth Service + Auth API Keys", ["auth-service", "auth-api-keys-service"]),
    "cds-ca":      ("https://cds-ca.wildix.com",          "CDS CA", ["cds-ca-api"]),
    "cds-console": ("https://cds-console-api.wildix.com", "CDS Console", ["cds-console-api"]),
    "cds-pbx":     ("https://cds-pbx.wildix.com",         "CDS PBX", ["cds-pbx-api"]),
    "cds-utils":   ("https://cds-utils.wildix.com",       "CDS Utils", ["cds-utils-api"]),
    "wam":         ("https://wam.wildix.com",             "WAM", ["wam-api"]),
    "wns":         ("https://notifications.wildix.com",   "WNS Email + Push", ["wns-email-api", "wns-push-api"]),
    "broadcasts":  ("https://broadcasts.x-hoppers.com",   "Broadcasts (x-hoppers)", ["broadcasts-api"]),
    "wmp":         ("https://api.wildix.com",             "WMP Info (service marqué deprecated par Wildix)", ["wmp-info-api"]),
    "fs":          ("https://fs.wildix.com",              "Filesharing", ["filesharing-service"]),
    "geo":         ("https://geo.wildix.com",             "GEO", ["geo-service"]),
    "mfa":         ("https://mfa.wildix.com",             "MFA", ["mfa-service"]),
    "ssl":         ("https://ssl.wildix.com",             "SSL", ["ssl-service"]),
    "stt":         ("https://stt.wildix.com",             "Speech-to-text", ["stt-service"]),
    "tts":         ("https://tts.wildix.com",             "Text-to-speech", ["tts-service"]),
    "url-preview": ("https://url-preview.wildix.com",     "URL Preview", ["url-preview-service"]),
    "classound":   ("https://classound-p2p.wildix.com",   "Classound (eSIM, WhatsApp, Messenger)", ["classound-api"]),
}

WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
INLINE_LIMIT = 15000  # caractères au-delà desquels la réponse part dans un fichier


# --------------------------------------------------------------------------
# Profils / secrets
# --------------------------------------------------------------------------
def state_path():
    p = os.environ.get("WILDIX_PBX_STATE")
    if p:
        return p
    uid = os.getuid() if hasattr(os, "getuid") else "u"
    return os.path.join(tempfile.gettempdir(), f"wildix-pbx-{uid}", "profiles.json")


def load_state():
    p = state_path()
    if not os.path.exists(p):
        return {"active": None, "profiles": {}}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_state(st):
    p = state_path()
    os.makedirs(os.path.dirname(p), mode=0o700, exist_ok=True)
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2)


def mask(s):
    if not s:
        return "—"
    return s[:7] + "…" + s[-4:] if len(s) > 14 else "****"


def normalize_pbx(domain):
    d = domain.strip()
    d = re.sub(r"^https?://", "", d).rstrip("/")
    d = d.split("/")[0]
    if "." not in d:
        d = d + ".wildixin.com"
    return d


def active_profile(st, name=None):
    name = name or os.environ.get("WILDIX_PROFILE") or st.get("active")
    if not name or name not in st["profiles"]:
        die("Aucun profil actif. Lancez d'abord : wildix.py login --pbx <domaine> --key <wsk-v1-…> [--token <bearer>]", 2)
    return name, st["profiles"][name]


def die(msg, code=1):
    print(f"ERREUR : {msg}", file=sys.stderr)
    sys.exit(code)


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------
def build_url(api, path, prof, query):
    if path.startswith("http://") or path.startswith("https://"):
        url = path.replace("{pbx}", prof.get("pbx", "{pbx}"))
    else:
        if api not in APIS:
            die(f"Alias d'API inconnu : {api}. Voir : wildix.py apis")
        base = APIS[api][0]
        if "{pbx}" in base:
            if not prof.get("pbx"):
                die("Ce profil n'a pas de domaine PBX (option --pbx de login).")
            base = base.replace("{pbx}", prof["pbx"])
        if not path.startswith("/"):
            path = "/" + path
        if api == "pbx" and not path.lower().startswith("/api/"):
            path = "/api/v1" + path
        url = base + path
    if query:
        sep = "&" if "?" in url else "?"
        url += sep + urllib.parse.urlencode(query, doseq=True)
    return url


def auth_candidates(api, prof, forced):
    """Ordre des en-têtes d'authentification à essayer."""
    key, tok, basic = prof.get("key"), prof.get("token"), prof.get("basic")
    avail = {
        "key": ("Bearer " + key) if key else None,
        "token": ("Bearer " + tok) if tok else None,
        "basic": ("Basic " + base64.b64encode(basic.encode()).decode()) if basic else None,
        "none": "",
    }
    if forced:
        if avail.get(forced) is None:
            die(f"Le profil ne contient pas d'identifiant de type « {forced} ».")
        return [(forced, avail[forced])]
    order = ["token", "basic", "key"] if api == "pbx" else ["key", "token"]
    out = [(n, avail[n]) for n in order if avail.get(n)]
    if not out:
        die("Aucun identifiant utilisable dans ce profil.")
    return out


def http(method, url, auth_header, body=None, extra_headers=None, timeout=60):
    headers = {"Accept": "application/json", "User-Agent": "wildix-pbx-skill/0.3"}
    if auth_header:
        headers["Authorization"] = auth_header
    data = None
    if body is not None:
        if isinstance(body, (dict, list)):
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        else:
            data = body if isinstance(body, bytes) else str(body).encode()
            headers.setdefault("Content-Type", "application/json")
    for h in extra_headers or []:
        k, _, v = h.partition(":")
        headers[k.strip()] = v.strip()
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    ctx = ssl.create_default_context()
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.status, dict(r.headers), r.read(), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read(), time.time() - t0
    except urllib.error.URLError as e:
        die(f"Connexion impossible à {url} : {e.reason}")


def parse_body(raw, headers):
    ct = (headers.get("Content-Type") or headers.get("content-type") or "").lower()
    if "json" in ct or raw[:1] in (b"{", b"["):
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            pass
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw


def describe(obj, depth=0, max_depth=2):
    """Résumé structurel compact d'une réponse JSON."""
    pad = "  " * depth
    if isinstance(obj, dict):
        lines = []
        for k, v in list(obj.items())[:40]:
            if isinstance(v, list):
                lines.append(f"{pad}{k}: liste de {len(v)} élément(s)")
                if v and isinstance(v[0], dict) and depth < max_depth:
                    lines.append(f"{pad}  champs du 1er élément : {', '.join(list(v[0].keys())[:25])}")
            elif isinstance(v, dict) and depth < max_depth:
                lines.append(f"{pad}{k}:")
                lines.extend(describe(v, depth + 1, max_depth))
            else:
                s = json.dumps(v, ensure_ascii=False)
                lines.append(f"{pad}{k}: {s[:80]}")
        return lines
    if isinstance(obj, list):
        return [f"{pad}liste de {len(obj)} élément(s)"]
    return [f"{pad}{str(obj)[:200]}"]


def out_dir():
    d = os.environ.get("WILDIX_OUT_DIR") or os.path.join(os.getcwd(), "wildix-output")
    os.makedirs(d, exist_ok=True)
    return d


def emit(status, payload, elapsed, url, out_file=None, force_inline=False):
    print(f"HTTP {status} — {elapsed:.2f}s — {url}", file=sys.stderr)
    if isinstance(payload, bytes):
        path = out_file or os.path.join(out_dir(), f"response-{int(time.time())}.bin")
        with open(path, "wb") as f:
            f.write(payload)
        print(f"Réponse binaire ({len(payload)} octets) enregistrée : {path}")
        return
    text = json.dumps(payload, ensure_ascii=False, indent=2) if not isinstance(payload, str) else payload
    if out_file or (len(text) > INLINE_LIMIT and not force_inline):
        path = out_file or os.path.join(out_dir(), f"response-{int(time.time())}.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Réponse ({len(text)} caractères) enregistrée : {path}")
        if not isinstance(payload, str):
            print("Structure :")
            print("\n".join(describe(payload)))
    else:
        print(text)


# --------------------------------------------------------------------------
# Commandes
# --------------------------------------------------------------------------
def cmd_login(a):
    st = load_state()
    key = a.key or os.environ.get("WILDIX_API_KEY")
    tok = a.token or os.environ.get("WILDIX_PBX_TOKEN")
    basic = a.basic or os.environ.get("WILDIX_PBX_BASIC")
    if key and not re.match(r"^wsk-v1-[0-9A-Za-z]{93}$", key):
        print("Attention : la clé ne ressemble pas à une Company API Key (wsk-v1- + 93 caractères).", file=sys.stderr)
    if not (key or tok or basic):
        die("Fournissez au moins --key, --token ou --basic.")
    pbx = normalize_pbx(a.pbx) if a.pbx else None
    name = a.name or (pbx.split(".")[0] if pbx else "default")
    st["profiles"][name] = {"pbx": pbx, "key": key, "token": tok, "basic": basic}
    st["active"] = name
    save_state(st)
    print(f"Profil « {name} » enregistré et actif — PBX : {pbx or '—'} ; clé : {mask(key)} ; token : {mask(tok)} ; basic : {'oui' if basic else '—'}")


def cmd_profiles(a):
    st = load_state()
    if not st["profiles"]:
        print("Aucun profil.")
        return
    for n, p in st["profiles"].items():
        star = "*" if n == st.get("active") else " "
        print(f"{star} {n:20} PBX={p.get('pbx') or '—':35} clé={mask(p.get('key'))} token={mask(p.get('token'))} basic={'oui' if p.get('basic') else '—'}")


def cmd_use(a):
    st = load_state()
    if a.name not in st["profiles"]:
        die(f"Profil inconnu : {a.name}")
    st["active"] = a.name
    save_state(st)
    print(f"Profil actif : {a.name}")


def cmd_logout(a):
    st = load_state()
    if a.all:
        st = {"active": None, "profiles": {}}
        save_state(st)
        print("Tous les profils ont été supprimés.")
        return
    name = a.name or st.get("active")
    if name in st["profiles"]:
        del st["profiles"][name]
        if st.get("active") == name:
            st["active"] = next(iter(st["profiles"]), None)
        save_state(st)
        print(f"Profil « {name} » supprimé.")
    else:
        print("Rien à supprimer.")


def cmd_apis(a):
    for k, (base, desc, docs) in APIS.items():
        print(f"{k:12} {base:38} {desc}  [doc : {', '.join(docs)}]")


def try_call(method, api, path, prof, query, body, forced, headers, timeout):
    url = build_url(api, path, prof, query)
    cands = auth_candidates(api, prof, forced)
    last = None
    for i, (name, hdr) in enumerate(cands):
        status, h, raw, el = http(method, url, hdr, body, headers, timeout)
        last = (status, h, raw, el, url, name)
        # bascule automatique sur l'identifiant suivant uniquement en lecture
        if status in (401, 403) and method in ("GET", "HEAD") and i + 1 < len(cands):
            print(f"… {status} avec l'identifiant « {name} », essai avec « {cands[i + 1][0]} »", file=sys.stderr)
            continue
        break
    return last


def cmd_whoami(a):
    st = load_state()
    name, prof = active_profile(st, a.profile)
    print(f"Profil : {name} — PBX : {prof.get('pbx') or '—'}")
    if prof.get("key"):
        s, h, raw, el, url, _ = try_call("GET", "auth", "/api/v3/api-keys/self/data", prof, None, None, "key", None, 30)
        body = parse_body(raw, h)
        print(f"\n[Company API Key] GET {url} → HTTP {s}")
        if s == 200 and isinstance(body, dict):
            k = body.get("apiKey", body)
            print(f"  nom : {k.get('name')} — société : {k.get('companyId')} — extension : {k.get('userExtension') or '—'} — expire : {k.get('expiresAt')}")
            print(f"  scopes : {', '.join(k.get('scopes') or [])}")
        else:
            print("  " + (json.dumps(body, ensure_ascii=False)[:300] if not isinstance(body, bytes) else "(binaire)"))
            print("  (Cette route peut être réservée à l'authentification de service ; un refus ici n'invalide pas la clé.)")
    if prof.get("pbx"):
        for forced in [x for x in ("token", "basic", "key") if prof.get(x)]:
            s, h, raw, el, url, _ = try_call("GET", "pbx", "/api/v1/personal/info/", prof, None, None, forced, None, 30)
            body = parse_body(raw, h)
            print(f"\n[PBX via {forced}] GET {url} → HTTP {s}")
            print("  " + (json.dumps(body, ensure_ascii=False)[:400] if not isinstance(body, bytes) else "(binaire)"))


def read_body(a):
    if a.data is None:
        return None
    d = a.data
    if d.startswith("@"):
        with open(d[1:], "rb") as f:
            d = f.read().decode("utf-8")
    try:
        return json.loads(d)
    except json.JSONDecodeError:
        return d


def parse_query(items):
    q = []
    for it in items or []:
        k, sep, v = it.partition("=")
        if not sep:
            die(f"Paramètre de requête invalide : {it} (attendu clé=valeur)")
        q.append((k, v))
    return q


def readonly_post(api, path):
    """Vrai si (api, path) correspond à une route POST documentée comme lecture
    (operationId Query*/List*/Get*/Search*/Check*… — voir references/readonly-posts.json)."""
    try:
        with open(os.path.join(REF_DIR, "readonly-posts.json"), encoding="utf-8") as f:
            routes = json.load(f)
    except OSError:
        return None
    p = urllib.parse.urlparse(path).path if path.startswith("http") else path
    p = p.rstrip("/")
    docs = APIS.get(api, (None, None, []))[2]
    for r in routes:
        if docs and r["ref"] not in docs:
            continue
        tpl = r["path"].rstrip("/")
        cands = [tpl]
        if api == "pbx" and not tpl.lower().startswith("/api/"):
            cands.append("/api/v1" + tpl)
        for t in cands:
            rx = "^" + re.sub(r"\\\{[^}]+\\\}", "[^/]+", re.escape(t)) + "$"
            if re.match(rx, p, re.I) or (api == "pbx" and re.match(rx, "/api/v1" + p, re.I)):
                return r["op"]
    return None


def cmd_call(a):
    st = load_state()
    name, prof = active_profile(st, a.profile)
    method = a.method.upper()
    query = parse_query(a.query)
    body = read_body(a)
    url = build_url(a.api, a.path, prof, query)

    ro = readonly_post(a.api, a.path) if method == "POST" else None
    if ro:
        print(f"POST de lecture documentée ({ro}) — exécutée sans confirmation.", file=sys.stderr)

    if method in WRITE_METHODS and not a.yes and not ro:
        cands = auth_candidates(a.api, prof, a.auth)
        print("ÉCRITURE NON EXÉCUTÉE — confirmation requise (relancer avec --yes après accord explicite de l'utilisateur).")
        print(f"  Profil  : {name} (PBX {prof.get('pbx') or '—'})")
        print(f"  Requête : {method} {url}")
        print(f"  Auth    : {cands[0][0]}")
        if body is not None:
            print("  Corps   :")
            print(json.dumps(body, ensure_ascii=False, indent=2) if not isinstance(body, str) else body)
        sys.exit(3)

    if a.all and method == "GET":
        return paginate_pbx(a, prof, query)

    s, h, raw, el, url, used = try_call(method, a.api, a.path, prof, query, body, a.auth, a.header, a.timeout)
    payload = parse_body(raw, h)
    emit(s, payload, el, f"{url} [auth={used}]", a.out, a.inline)
    if s >= 400:
        sys.exit(1)


def paginate_pbx(a, prof, query):
    """Pagination start/count de l'API PBX v1 (result.records / result.total)."""
    page = a.page_size
    start = 0
    records = []
    total = None
    q0 = [(k, v) for k, v in query if k not in ("start", "count")]
    used = None
    while True:
        q = q0 + [("start", str(start)), ("count", str(page))]
        s, h, raw, el, url, used = try_call("GET", a.api, a.path, prof, q, None, a.auth or used, a.header, a.timeout)
        body = parse_body(raw, h)
        if s >= 400 or not isinstance(body, dict):
            emit(s, body, el, url, None, True)
            sys.exit(1)
        res = body.get("result", body)
        recs = res.get("records") if isinstance(res, dict) else None
        if recs is None:
            print("Pagination --all : pas de champ result.records, réponse brute ci-dessous.", file=sys.stderr)
            emit(s, body, el, url, a.out, a.inline)
            return
        records.extend(recs)
        total = res.get("total", total)
        print(f"… {len(records)}/{total if total is not None else '?'}", file=sys.stderr)
        if not recs or len(recs) < page or (total is not None and len(records) >= int(total)):
            break
        start += page
        if len(records) >= a.max_records:
            print(f"Arrêt à {a.max_records} enregistrements (--max-records).", file=sys.stderr)
            break
    emit(200, {"total": total, "count": len(records), "records": records}, 0.0, f"{url} [auth={used}, paginé]", a.out, a.inline)


# --------------------------------------------------------------------------
# Documentation embarquée
# --------------------------------------------------------------------------
def ref_files():
    return sorted(f[:-3] for f in os.listdir(REF_DIR) if f.endswith(".md"))


def resolve_doc(name):
    files = ref_files()
    if name in files:
        return name
    if name in APIS and len(APIS[name][2]) == 1:
        return APIS[name][2][0]
    m = [f for f in files if name.lower() in f]
    if len(m) == 1:
        return m[0]
    die(f"Référence ambiguë ou inconnue : {name}. Candidats : {', '.join(m or files)}")


def doc_lines(slug):
    with open(os.path.join(REF_DIR, slug + ".md"), encoding="utf-8") as f:
        return f.read().split("\n")


def cmd_doc(a):
    if a.doc_cmd == "apis":
        idx = doc_lines("endpoints-index")
        for l in idx:
            if l.startswith("## "):
                print(l[3:])
        return
    if a.doc_cmd == "search":
        rx = re.compile(a.pattern, re.I)
        cur = None
        n = 0
        for l in doc_lines("endpoints-index"):
            if l.startswith("## "):
                cur = l[3:].split(" — ")[0] + " [" + re.search(r"alias `([^`]+)`", l).group(1) + "]"
                continue
            if a.api and cur and a.api.lower() not in cur.lower():
                continue
            if l.startswith("- ") and rx.search(l):
                print(f"{cur}  {l[2:]}")
                n += 1
                if n >= a.limit:
                    print(f"(limité à {a.limit} résultats)")
                    break
        if n == 0:
            print("Aucune route trouvée. Essayez un autre terme, ou : wildix.py doc grep <motif> --api <ref>")
        return
    if a.doc_cmd == "grep":
        slug = resolve_doc(a.api)
        rx = re.compile(a.pattern, re.I)
        L = doc_lines(slug)
        cur = None
        n = 0
        for i, l in enumerate(L):
            if l.startswith("#### "):
                cur = l[5:]
            if rx.search(l):
                print(f"{slug}:{i + 1}  [{cur or '-'}]  {l.strip()[:200]}")
                n += 1
                if n >= a.limit:
                    break
        return
    if a.doc_cmd == "show":
        slug = resolve_doc(a.api)
        L = doc_lines(slug)
        method = a.method.upper()
        path = a.path.rstrip("/")
        hit = None
        for i, l in enumerate(L):
            m = re.match(r"^#### `([A-Z]+)` `([^`]+)`", l)
            if m and m.group(1) == method and m.group(2).rstrip("/") == path:
                hit = i
                break
        if hit is None:
            die(f"Route {method} {a.path} introuvable dans {slug}. Utilisez : wildix.py doc search <terme>")
        end = len(L)
        for j in range(hit + 1, len(L)):
            if L[j].startswith("#### ") or L[j].startswith("### ") or L[j].startswith("## "):
                end = j
                break
        block = L[hit:end]
        if len(block) > a.max_lines and not a.full:
            print("\n".join(block[: a.max_lines]))
            print(f"\n… ({len(block) - a.max_lines} lignes supplémentaires — relancer avec --full ou --max-lines N)")
        else:
            print("\n".join(block))
        return
    if a.doc_cmd == "schema":
        slug = resolve_doc(a.api)
        L = doc_lines(slug)
        tag = f"**`{a.name}`**"
        hit = next((i for i, l in enumerate(L) if l.strip() == tag), None)
        if hit is None:
            die(f"Schéma {a.name} introuvable dans {slug}.")
        end = len(L)
        for j in range(hit + 1, len(L)):
            if L[j].startswith("**`") or L[j].startswith("</details>") or L[j].startswith("### "):
                end = j
                break
        print("\n".join(L[hit:end][: a.max_lines]))
        return


# --------------------------------------------------------------------------
def main():
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    p = argparse.ArgumentParser(prog="wildix.py", description="Client API Wildix")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("login", help="enregistrer un profil")
    s.add_argument("--pbx", help="domaine du PBX (ex. client.wildixin.com ou client)")
    s.add_argument("--key", help="Company API Key wsk-v1-… (ou variable WILDIX_API_KEY)")
    s.add_argument("--token", help="Bearer token PBX pour l'API WMS historique (ou WILDIX_PBX_TOKEN)")
    s.add_argument("--basic", help="identifiants PBX « login:motdepasse » (ou WILDIX_PBX_BASIC)")
    s.add_argument("--name", help="nom du profil (défaut : sous-domaine du PBX)")
    s.set_defaults(fn=cmd_login)

    s = sub.add_parser("profiles"); s.set_defaults(fn=cmd_profiles)
    s = sub.add_parser("use"); s.add_argument("name"); s.set_defaults(fn=cmd_use)
    s = sub.add_parser("logout"); s.add_argument("name", nargs="?"); s.add_argument("--all", action="store_true"); s.set_defaults(fn=cmd_logout)
    s = sub.add_parser("whoami"); s.add_argument("--profile"); s.set_defaults(fn=cmd_whoami)
    s = sub.add_parser("apis"); s.set_defaults(fn=cmd_apis)

    s = sub.add_parser("call", help="exécuter une requête")
    s.add_argument("method")
    s.add_argument("api", help="alias d'API (voir « apis ») — ignoré si le chemin est une URL complète")
    s.add_argument("path")
    s.add_argument("-q", "--query", action="append", help="paramètre clé=valeur (répétable)")
    s.add_argument("-d", "--data", help="corps JSON, ou @fichier.json")
    s.add_argument("-H", "--header", action="append", help="en-tête supplémentaire « Nom: valeur »")
    s.add_argument("--auth", choices=["key", "token", "basic", "none"], help="forcer un identifiant")
    s.add_argument("--profile")
    s.add_argument("--yes", action="store_true", help="confirme une écriture (POST/PUT/PATCH/DELETE)")
    s.add_argument("--all", action="store_true", help="pagination automatique start/count (API PBX v1)")
    s.add_argument("--page-size", type=int, default=500)
    s.add_argument("--max-records", type=int, default=50000)
    s.add_argument("-o", "--out", help="fichier de sortie")
    s.add_argument("--inline", action="store_true", help="tout afficher même si la réponse est longue")
    s.add_argument("--timeout", type=int, default=60)
    s.set_defaults(fn=cmd_call)

    s = sub.add_parser("doc", help="référence embarquée")
    ds = s.add_subparsers(dest="doc_cmd", required=True)
    d = ds.add_parser("apis")
    d = ds.add_parser("search"); d.add_argument("pattern"); d.add_argument("--api"); d.add_argument("--limit", type=int, default=60)
    d = ds.add_parser("grep"); d.add_argument("pattern"); d.add_argument("--api", required=True); d.add_argument("--limit", type=int, default=60)
    d = ds.add_parser("show"); d.add_argument("api"); d.add_argument("method"); d.add_argument("path"); d.add_argument("--full", action="store_true"); d.add_argument("--max-lines", type=int, default=250)
    d = ds.add_parser("schema"); d.add_argument("api"); d.add_argument("name"); d.add_argument("--max-lines", type=int, default=250)
    s.set_defaults(fn=cmd_doc)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
