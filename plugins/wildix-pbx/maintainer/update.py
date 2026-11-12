#!/usr/bin/env python3
"""
Mise à jour du plugin wildix-pbx à partir des spécifications OpenAPI publiées sur docs.wildix.com.

Usage :
  python3 maintainer/update.py --work <dossier_de_travail> [--force] [--today AAAA-MM-JJ]

Étapes :
  1. Découvre les pages de référence REST (sitemap) et leurs spécifications OpenAPI.
  2. Télécharge les spécifications et compare leurs empreintes à spec-hashes.json.
  3. Sans changement (et sans --force) : affiche NO_CHANGE et s'arrête.
  4. Changements sans route ajoutée (retraits, schémas modifiés) : affiche MINOR_CHANGE et s'arrête,
     sans produire de version ; ces changements seront intégrés à la prochaine version avec ajouts.
  5. Routes ajoutées (nouvelles routes, nouveaux services, routes de nouveau publiées) : régénère
     le référentiel au format du plugin, en CONSERVANT toutes les routes disparues de la documentation
     (marquées « deprecated (non publiée) » avec leur date de retrait), produit un rapport des écarts,
     puis construit une nouvelle version du plugin (.plugin).

Le plugin installé n'est jamais modifié : tout est écrit dans le dossier de travail.
Bibliothèque standard + PyYAML (pip install pyyaml si absent).
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import ssl
import sys
import urllib.error
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen  # noqa: E402

BASE = "https://docs.wildix.com"
CTX = ssl.create_default_context()
UA = {"User-Agent": "wildix-pbx-plugin-updater/1.0"}


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.read()


def text(url):
    return fetch(url).decode("utf-8", "replace")


def slug(t):
    t = re.sub(r"\(.*?\)", "", t.replace(" 🆕", "")).lower().replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def anchor(title):
    a = re.sub(r"[^\w\s-]", "", title.lower())
    return re.sub(r"\s", "-", a.strip())


# ===================================================================== découverte
def discover_pages():
    """Renvoie {page: [chemins de spec détectés]} pour chaque page de référence REST."""
    html = text(BASE + "/api-reference/")
    main = re.search(r"/assets/js/main\.[a-f0-9]+\.js", html).group(0)
    rt = re.search(r"/assets/js/runtime~main\.[a-f0-9]+\.js", html).group(0)
    M, R = text(BASE + main), text(BASE + rt)
    names, hashes = {}, {}
    for m in re.finditer(r'\{([^{}]*)\}\[e\]\|\|e\)\+"\."\+\{([^{}]*)\}', R):
        names = dict(re.findall(r'(\d+):"([^"]+)"', m.group(1)))
        hashes = dict(re.findall(r'(\d+):"([a-f0-9]+)"', m.group(2)))
    sm = text(BASE + "/sitemap.xml")
    pages = sorted(set(p.rstrip("/") for p in re.findall(r"<loc>https://docs\.wildix\.com(/api-reference/rest/[^<]+)</loc>", sm)))
    cache, out = {}, {}
    for p in pages:
        mm = re.search(re.escape('"' + p + "-") + r'[a-z0-9]{3}":\{"__comp":"([a-f0-9]+)"', M)
        specs = set()
        if mm:
            comp = mm.group(1)
            deps = re.search(re.escape(comp) + r'":\[\(\)=>Promise\.all\(\[([^\]]*)\]\)', M) or re.search(re.escape(comp) + r'":\[\(\)=>n\.e\((\d+)\)', M)
            for i in re.findall(r"\d+", deps.group(1)) if deps else []:
                if i not in hashes:
                    continue
                if i not in cache:
                    try:
                        cache[i] = text(f"{BASE}/assets/js/{names.get(i, i)}.{hashes[i]}.js")
                    except Exception:
                        cache[i] = ""
                specs.update(re.findall(r'["\'`](/codegen/api/[A-Za-z0-9_.-]+\.openapi\.json)["\'`]', cache[i]))
        out[p] = sorted(specs)
    return out


def guess_spec_names(page):
    """Noms de fichier probables pour une page dont la spec n'est pas détectée (convention Wildix)."""
    parts = page.strip("/").split("/")[3:]  # après api-reference/rest
    if not parts:
        return []
    fam, name = parts[0], (parts[1] if len(parts) > 1 else parts[0])
    fam_map = {"x-bees": "xbees", "x-hoppers": "xhop", "collaboration-services": None}
    f = fam_map.get(fam, fam)
    n = name.replace("_", "-")
    c = []
    if f is None:
        c += [f"{n}-main-client"]
    else:
        c += [f"{f}-{n}-client", f"{f}-client", f"{f}-{n}-main-client", f"{f}-api-client"]
    c += [f"{n}-client"]
    return [x + ".openapi.json" for x in dict.fromkeys(c)]


# ===================================================================== lecture de la révision précédente
def previous_reference(refdir, order):
    """Reconstitue le référentiel complet à partir des fichiers du plugin."""
    parts = [open(os.path.join(refdir, "overview.md"), encoding="utf-8").read().rstrip("\n"), ""]
    for s in order:
        f = os.path.join(refdir, s + ".md")
        if os.path.exists(f):
            parts += [open(f, encoding="utf-8").read().rstrip("\n"), "", "---", ""]
    parts.append(open(os.path.join(refdir, "webhooks.md"), encoding="utf-8").read().rstrip("\n"))
    return "\n".join(parts).split("\n")


def parse_reference(src):
    first = next(i for i, l in enumerate(src) if l.startswith("## ") and not l.startswith(("## Statuts", "## Authentication", "## Changements", "## Table of contents")))
    wh = next(i for i, l in enumerate(src) if l == "# Webhooks")

    def is_tag(j, b):
        t = src[j]
        if "non publi" in t.lower() or t.startswith("### Schemas appendix"):
            return True
        k = j + 1
        while k < b and not src[k].strip():
            k += 1
        return k < b and src[k].startswith("#### `")

    secs = {}
    raw = {}
    starts = [i for i in range(first, wh) if src[i].startswith("## ")] + [wh]
    for a, b in zip(starts, starts[1:]):
        title = src[a][3:].replace(" 🆕", "").strip()
        body = src[a:b]
        while body and body[-1].strip() in ("", "---"):
            body.pop()
        raw[title] = body
        d = {"pub": {}, "unpub": {}}
        tag, unpub, i = None, False, a + 1
        while i < b:
            l = src[i]
            if l.startswith("### ") and is_tag(i, b):
                if "non publi" in l.lower():
                    unpub = True
                elif l.startswith("### Schemas appendix"):
                    break
                else:
                    tag = l[4:].strip()
                i += 1
                continue
            m = re.match(r"^#### `([A-Z]+)` `([^`]+)`", l)
            if m:
                j = i + 1
                while j < b and not src[j].startswith(("#### ", "## ")) and not (src[j].startswith("### ") and is_tag(j, b)):
                    j += 1
                block = src[i:j]
                key = (m.group(1), m.group(2))
                if unpub:
                    mm = re.search(r"groupe d'origine : _([^_]+)_", "\n".join(block))
                    d["unpub"][key] = (mm.group(1) if mm else tag, block)
                else:
                    d["pub"][key] = (tag, block)
                i = j
                continue
            i += 1
        secs[title] = d
    auth = next((i for i, l in enumerate(src) if l == "## Authentication"), 0)
    old_schemes = set(re.findall(r"^\| `([^`]+)` \|", "\n".join(src[auth:first]), re.M))
    mprev = re.search(r"fetched (\d{4}-\d{2}-\d{2})", "\n".join(src[:first]))
    return secs, raw, src[wh:], old_schemes, (mprev.group(1) if mprev else "?")


# ===================================================================== comparaison
def norm(block):
    sig = []
    for x in block:
        x = x.replace(" 🆕", "")
        m = re.match(r"^(\s*)- `([^`]+)`(?: \(([a-z]+)\))? — ([^—_*]+?)(?: \*\*\(required\)\*\*)?(?: — .*)?(?: _\(.*\)_)?$", x)
        if m:
            sig.append((len(m.group(1)), m.group(2), m.group(3), m.group(4).strip(), "(required)" in x.split(" — ")[1] if " — " in x else False))
            continue
        m = re.match(r"^- (?:\*\*)?(Response \d+|Request body|Errors|operationId)(?:\*\*)?:?\s*(.*)$", x)
        if m:
            sig.append((m.group(1), re.sub(r"\(`None`\)|\*\*\(required\)\*\*", "", m.group(2)).strip()))
    return sig


def describe_change(a, b):
    fa = {x[1] for x in a if len(x) == 5}
    fb = {x[1] for x in b if len(x) == 5}
    pa = {x[1] for x in a if len(x) == 5 and x[2]}
    pb = {x[1] for x in b if len(x) == 5 and x[2]}
    out = []
    if pb - pa:
        out.append("paramètre(s) ajouté(s) : " + ", ".join(f"`{x}`" for x in sorted(pb - pa)))
    if pa - pb:
        out.append("paramètre(s) retiré(s) : " + ", ".join(f"`{x}`" for x in sorted(pa - pb)))
    add, rem = (fb - fa) - (pb - pa), (fa - fb) - (pa - pb)
    if add:
        out.append("champ(s) ajouté(s) : " + ", ".join(f"`{x}`" for x in sorted(add)[:12]) + (" …" if len(add) > 12 else ""))
    if rem:
        out.append("champ(s) retiré(s) : " + ", ".join(f"`{x}`" for x in sorted(rem)[:12]) + (" …" if len(rem) > 12 else ""))
    ea = next((x[1] for x in a if x[0] == "Errors"), "")
    eb = next((x[1] for x in b if x[0] == "Errors"), "")
    if ea != eb:
        out.append(f"codes d'erreur : {ea or '—'} → {eb or '—'}")
    if not out:
        out.append("type, caractère obligatoire ou structure de champ(s) modifié(s)")
    return " ; ".join(out)


def fmt(keys):
    return ", ".join(f"`{m} {p}`" for m, p in keys)


# ===================================================================== assemblage
def assemble(sections, dl, prev_src, today):
    v2, raw_prev, webhooks, old_schemes, prev = parse_reference(prev_src)
    out_sections, report, schemes = [], [], {}
    totals = {"routes": 0, "new": 0, "removed": 0, "kept_unpub": 0, "changed": 0, "back": 0}
    for sec in sections:
        title, spec_file = sec["title"], sec["spec"]
        path = os.path.join(dl, spec_file)
        old = v2.get(title)
        if not os.path.exists(path):
            # service introuvable : section précédente conservée telle quelle
            if title in raw_prev:
                out_sections.append((title, raw_prev[title] + [""], False))
                report.append({"title": title, "service_missing": True, "routes": 0, "new_service": False, "new": [], "removed": [], "still_unpub": [], "back": [], "changed": [], "changes": {}, "deprecated": []})
            continue
        spec = gen.load(path)
        for k, v in ((spec.get("components") or {}).get("securitySchemes") or {}).items():
            schemes.setdefault(k, gen.clean(v.get("description")) or v.get("type", ""))
        new_service = old is None
        g = gen.Gen(spec)
        keys_now = {(m.upper(), p) for _, m, p, _, _ in g.operations()}
        old_pub = set(old["pub"]) if old else set()
        old_unpub = set(old["unpub"]) if old else set()
        new_routes = keys_now - old_pub - old_unpub if old else set()
        back = keys_now & old_unpub
        lines, g, blocks = gen.render_section(path, title, frozenset(new_routes), new_service)
        depr = sorted((m.upper(), p) for _, m, p, op, _ in g.operations() if op.get("deprecated"))
        changed = sorted(k for k in keys_now & old_pub if norm(old["pub"][k][1]) != norm(blocks[k]))
        changes = {f"{m} {p}": describe_change(norm(old["pub"][(m, p)][1]), norm(blocks[(m, p)])) for m, p in changed}
        removed_now = sorted(old_pub - keys_now)
        still_unpub = sorted(old_unpub - keys_now)
        retired = []
        for k in removed_now:
            tag, block = old["pub"][k]
            b = [block[0].replace(" 🆕", "")] + ["", f"> ⚠️ **Statut : deprecated (non publiée)** — absente de la documentation depuis la révision du {today} (groupe d'origine : _{tag}_). Description conservée telle que publiée au {prev}."] + list(block[1:])
            retired.append(b)
        for k in still_unpub:
            retired.append(list(old["unpub"][k][1]))
        if retired:
            lines += ["### Routes non publiées — deprecated (en cours de décommissionnement)", "",
                      "> ⚠️ Les routes ci-dessous ont figuré dans une révision antérieure de la spécification publiée mais **n'y figurent plus**. "
                      "Elles sont en cours de décommissionnement et peuvent encore répondre pendant quelques mois : leur description est conservée telle qu'elle était documentée, "
                      "et la date de retrait est indiquée sur chacune. À ne pas utiliser pour de nouveaux développements.", ""]
            for b in retired:
                lines += b
                if b[-1] != "":
                    lines.append("")
        lines += g.appendix(title)
        out_sections.append((title, lines, new_service))
        n = len(keys_now)
        totals["routes"] += n
        totals["new"] += n if new_service else len(new_routes)
        totals["removed"] += len(removed_now)
        totals["kept_unpub"] += len(retired)
        totals["changed"] += len(changed)
        totals["back"] += len(back)
        report.append({"title": title, "routes": n, "new_service": new_service, "new": sorted(new_routes), "removed": removed_now,
                       "still_unpub": still_unpub, "back": sorted(back), "changed": changed, "changes": changes, "deprecated": depr,
                       "server": ((spec.get("servers") or [{}])[0]).get("url")})
    # sections de la révision précédente absentes de la liste (sécurité : rien ne se perd)
    listed = {s["title"] for s in sections}
    for t, body in raw_prev.items():
        if t not in listed:
            out_sections.append((t, body + [""], False))
            report.append({"title": t, "service_missing": True, "routes": 0, "new_service": False, "new": [], "removed": [], "still_unpub": [], "back": [], "changed": [], "changes": {}, "deprecated": []})

    H = ["# Wildix API Reference (Compiled — full schemas)", "",
         "Generated for use as a reference in Claude Code / automation projects targeting the Wildix PBX and collaboration platform.", "",
         f"Source: the live OpenAPI specifications published under `https://docs.wildix.com/codegen/api/*.openapi.json` (plus `https://docs.wildix.com/pbx-openapi.yaml` for the PBX API), fetched {today}. Previous revision: {prev}.", "",
         "Request bodies are **expanded field by field** (name, type, required flag, description, constraints) instead of only naming the OpenAPI component. Unions (`oneOf`) are expanded per variant. Deeply nested or recursive types are cut off and reproduced in each API's Schemas appendix.", "",
         "## Statuts de publication", "",
         f"- 🆕 **Nouveau service / Nouvelle route** — publié(e) depuis la révision du {prev}.",
         "- ⚠️ **Deprecated (non publiée)** — route présente dans une révision antérieure mais retirée de la documentation publiée : en cours de décommissionnement, pas encore supprimée. Ces routes sont regroupées en fin de section API, sous « Routes non publiées », avec leur description d'origine et leur date de retrait.",
         "- **Company API Key scope** — droit exigé quand la route est appelée avec une Company API Key (`Authorization: Bearer wsk-v1-…`) ; seules les routes PBX qui portent cette mention acceptent ces clés.", "",
         "## Authentication", "", "Security schemes declared by the services (Bearer unless noted):", "", "| Scheme | Meaning |", "|---|---|"]
    for k in sorted(schemes):
        H.append(f"| `{k}` | {schemes[k]}{' 🆕' if k not in old_schemes else ''} |")
    H += ["", "Tokens are obtained from the Auth Service (see that section). Per-operation scopes are listed inline as **Scopes** under each endpoint.", "",
          f"## Changements depuis la révision du {prev}", ""]
    any_change = False
    for r in report:
        a = f"[{r['title']}](#{anchor(r['title'])})"
        if r.get("service_missing"):
            H.append(f"- **{a}** — ⚠️ spécification introuvable : section précédente conservée telle quelle")
            any_change = True
            continue
        if r["new_service"]:
            H.append(f"- **{a}** — 🆕 nouveau service ({r['routes']} routes)")
            any_change = True
            continue
        parts = []
        if r["new"]:
            parts.append(f"{len(r['new'])} nouvelle(s) route(s) : {fmt(r['new'])}")
        if r["removed"]:
            parts.append(f"{len(r['removed'])} route(s) retirée(s) de la documentation, conservée(s) en deprecated : {fmt(r['removed'])}")
        if r["back"]:
            parts.append(f"{len(r['back'])} route(s) de nouveau publiée(s) : {fmt(r['back'])}")
        if parts:
            H.append(f"- **{a}** — " + " ; ".join(parts))
            any_change = True
    if not any_change:
        H.append("- Aucune route ajoutée, retirée ou republiée.")
    dep = [f"  - **{r['title']}** : {fmt(r['deprecated'])}" for r in report if r.get("deprecated")]
    if dep:
        H += ["", f"**Routes publiées mais marquées `deprecated` par Wildix** ({sum(len(r['deprecated']) for r in report)}) — toujours documentées, à remplacer à terme :"] + dep
    H += ["", f"Schémas régénérés à partir des spécifications actuelles : {totals['changed']} route(s) existante(s) présentent des changements de paramètres, de corps, de réponse ou de codes d'erreur (détail dans le rapport des écarts).", "",
          f"**Webhooks** — section reprise sans modification de la révision précédente (non revérifiée automatiquement).", "",
          "## Table of contents", ""]
    for t, _, ns in out_sections:
        H.append(f"- [{t}](#{anchor(t)})" + (" 🆕" if ns else ""))
    H += ["- [Webhooks](#webhooks)", "", "---", ""]
    body = []
    for _, lines, _ in out_sections:
        body += lines + ["---", ""]
    full = "\n".join(H + body + webhooks).rstrip() + "\n"
    return full, {"totals": totals, "sections": report, "previous": prev, "today": today}


# ===================================================================== découpage pour le plugin
def split_into(full, refdir):
    src = full.split("\n")
    for f in os.listdir(refdir):
        if f.endswith((".md", ".json")):
            os.remove(os.path.join(refdir, f))
    first = next(i for i, l in enumerate(src) if l.startswith("## ") and not l.startswith(("## Statuts", "## Authentication", "## Changements", "## Table of contents")))
    whi = src.index("# Webhooks")
    open(os.path.join(refdir, "overview.md"), "w", encoding="utf-8").write("\n".join(src[:first]).rstrip() + "\n")

    def is_tag(L, j):
        t = L[j]
        if "non publi" in t.lower() or t.startswith("### Schemas appendix"):
            return True
        k = j + 1
        while k < len(L) and not L[k].strip():
            k += 1
        return k < len(L) and L[k].startswith("#### `")

    secs = [i for i in range(first, whi) if src[i].startswith("## ")] + [whi]
    meta, order = [], []
    for a, b in zip(secs, secs[1:]):
        title = src[a][3:].replace(" 🆕", "").strip()
        s = slug(title)
        body = src[a:b]
        while body and body[-1].strip() in ("", "---"):
            body.pop()
        open(os.path.join(refdir, s + ".md"), "w", encoding="utf-8").write("\n".join(body) + "\n")
        base = ""
        for j, l in enumerate(body):
            if l.startswith("**Servers**") and j + 2 < len(body):
                m = re.search(r"`(https?://[^`]+)`", body[j + 2])
                base = m.group(1) if m else ""
                break
        meta.append((title, s, base, body, "🆕" in src[a]))
        order.append(s)
    open(os.path.join(refdir, "webhooks.md"), "w", encoding="utf-8").write("\n".join(src[whi:]).rstrip() + "\n")
    idx = ["# Index des routes Wildix", "",
           "Une ligne par route : `MÉTHODE chemin — résumé`. ⚠️ = route deprecated (retirée de la documentation, ou marquée deprecated par Wildix) — encore utilisable jusqu'à son décommissionnement. 🆕 = nouvelle route ou nouveau service.",
           "Pour le détail d'une route : `wildix.py doc show <api> <MÉTHODE> <chemin>`.", ""]
    ro = []
    RX = re.compile(r"^(Query|List|Get|Search|Describe|Count|Find|Fetch|Lookup|Preview|Check|Validate|Batch[Gg]et|Retrieve)")
    for title, s, base, L, isnew in meta:
        eps = [i for i, l in enumerate(L) if re.match(r"^#### `(GET|POST|PUT|PATCH|DELETE)`", l)]
        idx.append(f"## {title} — alias `{s}` — {base} ({len(eps)} routes){' 🆕' if isnew else ''}")
        unpub = False
        for i, l in enumerate(L):
            if l.startswith("### ") and is_tag(L, i) and "non publi" in l.lower():
                unpub = True
            m = re.match(r"^#### `(GET|POST|PUT|PATCH|DELETE)` `([^`]+)`(.*)", l)
            if not m:
                continue
            end = next((k for k in range(i + 1, len(L)) if L[k].startswith(("#### ", "## ")) or (L[k].startswith("### ") and is_tag(L, k))), len(L))
            blk = L[i + 1:end]
            summ = ""
            for t in blk:
                t = t.strip()
                if t and not t.startswith(">") and not t.startswith("- "):
                    summ = t.strip("*_ ")
                    break
            dep = unpub or any("Route marquée `deprecated`" in t for t in blk)
            flag = ("⚠️ " if dep else "") + ("🆕 " if ("🆕" in m.group(3) or isnew) else "")
            idx.append(f"- {flag}`{m.group(1)} {m.group(2)}` — {summ[:110]}")
            if m.group(1) == "POST":
                op = next((re.search(r"operationId: `([^`]+)`", t).group(1) for t in blk if "operationId:" in t), None)
                if op and RX.match(op) and not op.startswith("GetOrCreate"):
                    ro.append({"ref": s, "path": m.group(2), "op": op})
        idx.append("")
    open(os.path.join(refdir, "endpoints-index.md"), "w", encoding="utf-8").write("\n".join(idx))
    json.dump(ro, open(os.path.join(refdir, "readonly-posts.json"), "w"), indent=1)
    return meta


def report_md(rep):
    t = rep["totals"]
    f = lambda ks: ", ".join(f"`{m} {p}`" for m, p in ks)
    L = ["# Rapport des écarts — référentiel API Wildix", "", f"Révision du {rep['today']}, comparée à la révision du {rep['previous']}.", "", "## Synthèse", "",
         f"- **{t['routes']} routes publiées** dans {sum(1 for s in rep['sections'] if not s.get('service_missing'))} services.",
         f"- **{t['new']} routes nouvelles**" + (f", dont {sum(1 for s in rep['sections'] if s['new_service'])} nouveau(x) service(s)" if any(s['new_service'] for s in rep['sections']) else "") + ".",
         f"- **{t['back']} routes de nouveau publiées**.",
         f"- **{t['removed']} routes retirées** de la documentation depuis la révision précédente ; **{t['kept_unpub']} routes deprecated conservées** au total, avec leur description d'origine et leur date de retrait.",
         f"- **{t['changed']} routes existantes modifiées** dans leur structure.",
         f"- **{sum(len(s.get('deprecated', [])) for s in rep['sections'])} routes publiées mais marquées `deprecated`** par Wildix.", ""]
    if rep.get("unmapped_pages"):
        L += ["## ⚠️ Pages sans spécification exploitable", ""] + [f"- `{p}`" for p in rep["unmapped_pages"]] + [""]
    if rep.get("no_alias"):
        L += ["## Nouveaux serveurs sans alias dans le script", "", "Utiliser l'URL complète avec `wildix.py call` en attendant un alias :", ""] + [f"- **{t}** — `{s}`" for t, s in rep["no_alias"]] + [""]
    L += ["## Détail par service", ""]
    for s in rep["sections"]:
        if s.get("service_missing"):
            L += [f"### {s['title']}", "", "- ⚠️ Spécification introuvable : section précédente conservée telle quelle.", ""]
            continue
        if not any([s["new_service"], s["new"], s["removed"], s["still_unpub"], s["back"], s["changes"], s.get("deprecated")]):
            continue
        L += [f"### {s['title']}" + (" 🆕" if s["new_service"] else ""), ""]
        if s["new_service"]:
            L += [f"- Nouveau service : {s['routes']} routes.", ""]
            continue
        if s["new"]:
            L.append(f"- **Nouvelles routes** : {f(s['new'])}")
        if s["back"]:
            L.append(f"- **De nouveau publiées** : {f(s['back'])}")
        if s["removed"]:
            L.append(f"- **Retirées (conservées en deprecated)** : {f(s['removed'])}")
        if s["still_unpub"]:
            L.append(f"- **Retirées lors d'une révision antérieure (toujours conservées)** : {f(s['still_unpub'])}")
        if s.get("deprecated"):
            L.append(f"- **Marquées `deprecated` par Wildix** : {f(s['deprecated'])}")
        if s["changes"]:
            L.append(f"- **Routes modifiées ({len(s['changes'])})** :")
            for k, v in sorted(s["changes"].items()):
                L.append(f"  - `{k}` — {v}")
        L.append("")
    L += ["## Remarques", "", "- **Webhooks** : section reprise sans modification de la révision précédente.",
          "- Les changements de forme (descriptions, contraintes, renvois à l'annexe) ne sont pas comptés comme des modifications."]
    return "\n".join(L) + "\n"


# ===================================================================== programme principal
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True, help="dossier de travail (créé si absent)")
    ap.add_argument("--force", action="store_true", help="régénérer même sans changement des spécifications")
    ap.add_argument("--today", default=datetime.date.today().isoformat())
    a = ap.parse_args()

    plugin_root = os.path.dirname(HERE)
    work = os.path.abspath(a.work)
    dl = os.path.join(work, "specs")
    os.makedirs(dl, exist_ok=True)
    sections = json.load(open(os.path.join(HERE, "sections.json"), encoding="utf-8"))
    old_hashes = json.load(open(os.path.join(HERE, "spec-hashes.json"), encoding="utf-8"))

    # 1. découverte
    pages = discover_pages()
    by_page = {s["page"]: s for s in sections}
    unmapped = []
    for p, specs in pages.items():
        if p in by_page:
            continue
        if len(p.strip("/").split("/")) < 4 and not specs:
            continue  # page d'accueil d'une famille d'API (ex. /api-reference/rest/wda), sans spécification
        cand = [s.split("/")[-1] for s in specs] or guess_spec_names(p)
        found = None
        for c in cand:
            try:
                b = fetch(f"{BASE}/codegen/api/{c}")
                json.loads(b)
                found = c.replace(".openapi.json", ".json")
                open(os.path.join(dl, found), "wb").write(b)
                break
            except Exception:
                continue
        if not found:
            unmapped.append(p)
            continue
        info = json.load(open(os.path.join(dl, found))).get("info", {})
        title = gen.clean(info.get("title")) or p.rsplit("/", 1)[-1]
        title = re.sub(r"\s+(service|Service)$", " API", title)
        if any(s["title"] == title for s in sections):
            title = f"{title} ({p.rsplit('/', 1)[-1]})"
        sections.append({"title": title, "spec": found, "page": p})

    # 2. téléchargement
    new_hashes, missing = {}, []
    for s in sections:
        f = s["spec"]
        url = f"{BASE}/pbx-openapi.yaml" if f == "pbx-openapi.yaml" else f"{BASE}/codegen/api/{f.replace('.json', '.openapi.json')}"
        try:
            b = fetch(url)
            open(os.path.join(dl, f), "wb").write(b)
            new_hashes[f] = hashlib.sha256(b).hexdigest()
        except Exception as e:
            missing.append((s["title"], str(e)))
    changed_specs = sorted(f for f, h in new_hashes.items() if old_hashes.get(f) != h)
    added = [s["title"] for s in sections if s["spec"] not in old_hashes]
    status = {"changed_specs": changed_specs, "new_services": added, "missing_specs": missing, "unmapped_pages": unmapped}
    if not changed_specs and not added and not missing and not unmapped and not a.force:
        print("NO_CHANGE")
        print(json.dumps(status, ensure_ascii=False))
        return

    # 3. régénération
    refdir = os.path.join(plugin_root, "skills", "wildix-pbx", "references")
    idx = open(os.path.join(refdir, "endpoints-index.md"), encoding="utf-8").read()
    order = re.findall(r"^## .*? — alias `([^`]+)`", idx, re.M)
    prev_src = previous_reference(refdir, order)
    full, rep = assemble(sections, dl, prev_src, a.today)

    # alias manquants pour de nouveaux serveurs
    sys.path.insert(0, os.path.join(plugin_root, "skills", "wildix-pbx", "scripts"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("wildix_cli", os.path.join(plugin_root, "skills", "wildix-pbx", "scripts", "wildix.py"))
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    bases = {v[0] for v in cli.APIS.values()}
    rep["no_alias"] = [(s["title"], s["server"]) for s in rep["sections"] if s.get("server") and "{" not in s["server"] and s["server"] not in bases]
    rep["unmapped_pages"] = unmapped
    rep["status"] = status

    # Règle de publication : une nouvelle version n'est produite que si des routes sont AJOUTÉES
    # (nouvelles routes, nouveaux services ou routes de nouveau publiées). Les retraits et les
    # changements de schéma seuls sont une mise à jour mineure : rien n'est publié, ils seront
    # intégrés (routes retirées marquées deprecated) lors de la prochaine version avec ajouts.
    t = rep["totals"]
    additions = t["new"] + t["back"]
    if additions == 0 and not a.force:
        removed = [f"{s['title']} : {m} {p}" for s in rep["sections"] for m, p in s.get("removed", [])]
        print("MINOR_CHANGE")
        print(json.dumps({"removed_routes": removed, "changed_routes": t["changed"], "missing_specs": missing,
                          "unmapped_pages": unmapped, "changed_specs": changed_specs}, ensure_ascii=False))
        return

    # 4. nouvelle version du plugin
    build = os.path.join(work, "plugin")
    if os.path.exists(build):
        shutil.rmtree(build)
    shutil.copytree(plugin_root, build, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
    split_into(full, os.path.join(build, "skills", "wildix-pbx", "references"))
    pj = os.path.join(build, ".claude-plugin", "plugin.json")
    meta = json.load(open(pj, encoding="utf-8"))
    major, minor, patch = (int(x) for x in meta["version"].split("."))
    meta["version"] = f"{major}.{minor}.{patch + 1}"
    json.dump(meta, open(pj, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    n_services = sum(1 for s in rep["sections"] if not s.get("service_missing"))
    for rel in ("README.md", os.path.join("skills", "wildix-pbx", "SKILL.md")):
        p = os.path.join(build, rel)
        t = open(p, encoding="utf-8").read()
        t = re.sub(r"révision du \d{4}-\d{2}-\d{2}, \d+ services", f"révision du {a.today}, {n_services} services", t)
        t = re.sub(r"\(\d+ files, revision \d{4}-\d{2}-\d{2}\)", f"({n_services} files, revision {a.today})", t)
        open(p, "w", encoding="utf-8").write(t)
    json.dump(new_hashes, open(os.path.join(build, "maintainer", "spec-hashes.json"), "w"), indent=1)
    json.dump([{"title": s["title"], "spec": s["spec"], "page": s["page"]} for s in sections], open(os.path.join(build, "maintainer", "sections.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # contrôle : aucune route de la révision précédente ne doit manquer
    prev_keys = set()
    cur = None
    for l in prev_src:
        if l.startswith("# Webhooks"):
            break
        if l.startswith("## "):
            cur = l[3:].replace(" 🆕", "").strip()
        m = re.match(r"^#### `([A-Z]+)` `([^`]+)`", l)
        if m and cur:
            prev_keys.add((cur, m.group(1), m.group(2)))
    new_keys = set()
    cur = None
    for l in full.split("\n"):
        if l.startswith("# Webhooks"):
            break
        if l.startswith("## "):
            cur = l[3:].replace(" 🆕", "").strip()
        m = re.match(r"^#### `([A-Z]+)` `([^`]+)`", l)
        if m and cur:
            new_keys.add((cur, m.group(1), m.group(2)))
    lost = sorted(prev_keys - new_keys)
    rep["lost_routes"] = [list(x) for x in lost]

    zpath = os.path.join(work, f"wildix-pbx-{meta['version']}.plugin")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(build):
            for fn in files:
                fp = os.path.join(root, fn)
                z.write(fp, os.path.relpath(fp, build))
    open(os.path.join(work, f"{a.today.replace('-', '')}_wildix-api-reference-full.md"), "w", encoding="utf-8").write(full)
    rpath = os.path.join(work, f"rapport-ecarts-{a.today.replace('-', '')}.md")
    open(rpath, "w", encoding="utf-8").write(report_md(rep))
    json.dump(rep, open(os.path.join(work, "report.json"), "w"), indent=1, ensure_ascii=False)
    print("UPDATED" if not lost else "UPDATED_WITH_LOST_ROUTES")
    print(json.dumps({"version": meta["version"], "plugin": zpath, "report": rpath, "totals": rep["totals"], "lost_routes": len(lost),
                      "changed_specs": changed_specs, "new_services": added, "missing_specs": missing, "unmapped_pages": unmapped,
                      "no_alias": rep["no_alias"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
