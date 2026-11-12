#!/usr/bin/env python3
"""Génère une section Markdown (format référentiel V2) à partir d'une spécification OpenAPI 3."""
import json
import re
import sys

import yaml

METHODS = ["get", "post", "put", "patch", "delete"]
MAX_DEPTH = 6          # profondeur d'expansion dans les routes
APPX_DEPTH = 4         # profondeur d'expansion dans l'annexe
ENUM_MAX = 12


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) if path.endswith((".yaml", ".yml")) else json.load(f)


def clean(s):
    if s is None:
        return ""
    return re.sub(r"\s+", " ", str(s)).strip()


def split_scopes(desc):
    """Retire le bloc « Allowed Auth Scopes » de la description et renvoie (desc, scopes)."""
    if not desc:
        return "", []
    m = re.search(r"#+\s*Allowed Auth Scopes\s*\n(.*?)(?=\n#+\s|\Z)", desc, re.S)
    scopes = []
    if m:
        for line in m.group(1).splitlines():
            line = line.strip()
            if line.startswith("-"):
                scopes.append(line.lstrip("- ").strip().strip("`"))
        desc = desc[: m.start()] + desc[m.end():]
    return desc.strip(), scopes


class Gen:
    def __init__(self, spec):
        self.spec = spec
        self.schemas = (spec.get("components") or {}).get("schemas") or {}

    # ---------------------------------------------------------------- schémas
    def ref_name(self, s):
        if isinstance(s, dict) and "$ref" in s:
            return s["$ref"].split("/")[-1]
        return None

    def deref(self, s):
        seen = 0
        while isinstance(s, dict) and "$ref" in s and seen < 20:
            name = s["$ref"].split("/")[-1]
            s = self.schemas.get(name, {})
            seen += 1
        return s or {}

    def is_union(self, s):
        return bool(s.get("oneOf") or s.get("anyOf"))

    def is_complex(self, s):
        s = self.deref(s)
        if self.is_union(s) or s.get("allOf"):
            return True
        if s.get("type") == "object" or "properties" in s:
            return bool(s.get("properties")) or bool(s.get("additionalProperties"))
        if s.get("type") == "array":
            return True
        return False

    def merged(self, s):
        """Fusionne allOf et renvoie un schéma objet."""
        s = self.deref(s)
        if not s.get("allOf"):
            return s
        out = {"type": "object", "properties": {}, "required": []}
        for part in s["allOf"]:
            p = self.merged(part)
            out["properties"].update(p.get("properties") or {})
            out["required"] += p.get("required") or []
            if p.get("description") and not out.get("description"):
                out["description"] = p["description"]
        for k in ("properties", "required"):
            if s.get(k):
                if k == "properties":
                    out[k].update(s[k])
                else:
                    out[k] += s[k]
        return out

    def type_label(self, raw):
        name = self.ref_name(raw)
        s = self.merged(raw)
        if self.is_union(s):
            return "union"
        t = s.get("type")
        if isinstance(t, list):
            t = "|".join(str(x) for x in t if x != "null")
        if name and (t == "object" or s.get("properties") or s.get("allOf")):
            return name
        if not t:
            if s.get("properties"):
                return "object"
            return "any"
        return t

    def constraints(self, raw):
        s = self.deref(raw)
        c = []
        if "default" in s:
            c.append(f"default={s['default']}")
        if s.get("format"):
            c.append(f"format={s['format']}")
        if s.get("pattern"):
            c.append(f"pattern={s['pattern']}")
        for k, lab in (("minLength", "minLen"), ("maxLength", "maxLen"), ("minimum", "min"), ("maximum", "max"),
                       ("minItems", "minItems"), ("maxItems", "maxItems")):
            if k in s:
                c.append(f"{lab}={s[k]}")
        if s.get("enum"):
            vals = [f"`{v}`" for v in s["enum"][:ENUM_MAX]]
            more = len(s["enum"]) - ENUM_MAX
            c.append("enum: " + ", ".join(vals) + (f", … (+{more})" if more > 0 else ""))
        if s.get("deprecated"):
            c.append("deprecated")
        return f" _({'; '.join(c)})_" if c else ""

    def field_line(self, pad, name, raw, required, desc_override=None):
        s = self.deref(raw)
        desc = clean(desc_override if desc_override is not None else (raw.get("description") if isinstance(raw, dict) and raw.get("description") else s.get("description")))
        line = f"{pad}- `{name}` — {self.type_label(raw)}"
        if required:
            line += " **(required)**"
        if desc:
            line += f" — {desc}"
        line += self.constraints(raw)
        return line

    def expand(self, raw, depth, limit, stack, pad_level):
        """Renvoie les lignes décrivant le contenu (propriétés) d'un schéma."""
        pad = "  " * pad_level
        name = self.ref_name(raw)
        s = self.merged(raw)
        lines = []
        if depth >= limit or (name and name in stack):
            target = name or self.ref_name(s.get("items") or {}) or self.ref_name(s.get("additionalProperties") or {} if isinstance(s.get("additionalProperties"), dict) else {})
            if not self.is_complex(raw):
                return lines
            if target:
                lines.append(f"{pad}- _(nesting depth limit — see `{target}` in the Schemas appendix)_")
            elif s.get("type") == "array" and not self.is_complex(s.get("items") or {}):
                lines.append(f"{pad}- _array of_ `{self.type_label(s.get('items') or {})}`")
            else:
                lines.append(f"{pad}- _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_")
            return lines
        st = stack | ({name} if name else set())
        if self.is_union(s):
            variants = s.get("oneOf") or s.get("anyOf")
            kw = "oneOf" if s.get("oneOf") else "anyOf"
            lines.append(f"{pad}- _{kw}_ — {'exactly one' if kw == 'oneOf' else 'one or more'} of:")
            for v in variants:
                vm = self.merged(v)
                props = vm.get("properties") or {}
                label = list(props)[0] if len(props) == 1 else (self.ref_name(v) or clean(vm.get("title")) or self.type_label(v))
                lines.append(f"{pad}  - **`{label}`**")
                lines += self.expand(v, depth + 1, limit, st, pad_level + 2)
            return lines
        t = s.get("type")
        if t == "array" or "items" in s:
            it = s.get("items") or {}
            iname = self.ref_name(it) or self.type_label(it)
            lines.append(f"{pad}- _array of_ `{iname}`")
            if self.is_complex(it):
                lines += self.expand(it, depth + 1, limit, st, pad_level + 1)
            return lines
        props = s.get("properties") or {}
        req = set(s.get("required") or [])
        for pn, pv in props.items():
            lines.append(self.field_line(pad, pn, pv, pn in req))
            if self.is_complex(pv):
                lines += self.expand(pv, depth + 1, limit, st, pad_level + 1)
        ap = s.get("additionalProperties")
        if isinstance(ap, dict) and ap:
            lines.append(f"{pad}- _map of_ `{self.ref_name(ap) or self.type_label(ap)}`")
            if self.is_complex(ap):
                lines += self.expand(ap, depth + 1, limit, st, pad_level + 1)
        return lines

    # ---------------------------------------------------------------- routes
    def params(self, op, path_item):
        out = []
        seen = set()
        for p in (op.get("parameters") or []) + (path_item.get("parameters") or []):
            p = self.deref(p) if "$ref" in p else p
            key = (p.get("name"), p.get("in"))
            if key in seen:
                continue
            seen.add(key)
            out.append(p)
        return out

    def render_op(self, method, path, op, path_item):
        L = [f"#### `{method.upper()}` `{path}`", ""]
        desc, scopes = split_scopes(op.get("description") or "")
        summ = clean(op.get("summary"))
        desc_c = desc.strip()
        if op.get("deprecated"):
            L += ["> ⚠️ Route marquée `deprecated` dans la spécification publiée.", ""]
        if summ and summ != clean(desc_c):
            L += [f"**{summ}**", ""]
        if desc_c:
            # les titres internes aux descriptions (### Rate Limits…) deviennent du gras
            desc_c = re.sub(r"^#{1,6}\s+(.+?)\s*#*$", r"**\1**", desc_c, flags=re.M)
            L += [desc_c, ""]
        if op.get("operationId"):
            L.append(f"- operationId: `{op['operationId']}`")
        if scopes:
            L.append("- **Scopes**: " + ", ".join(f"`{s}`" for s in scopes))
        cak = op.get("x-wildix-companyApiKeyScope")
        if cak:
            cak = cak if isinstance(cak, list) else [cak]
            L.append("- **Company API Key scope**: " + ", ".join(f"`{s}`" for s in cak))
        ps = self.params(op, path_item)
        if ps:
            L.append("- **Parameters**")
            for p in ps:
                sch = p.get("schema") or {}
                line = f"  - `{p.get('name')}` ({p.get('in')}) — {self.type_label(sch) if sch else 'string'}"
                if p.get("required"):
                    line += " **(required)**"
                if p.get("description"):
                    line += f" — {clean(p['description'])}"
                line += self.constraints(sch) if sch else ""
                L.append(line)
        rb = op.get("requestBody")
        if rb:
            rb = self.deref(rb) if "$ref" in rb else rb
            content = rb.get("content") or {}
            if content:
                ct, media = next(iter(content.items()))
                sch = media.get("schema") or {}
                nm = self.ref_name(sch)
                L.append(f"- **Request body** (`{ct}`" + (f" — `{nm}`" if nm else "") + ")" + (" **(required)**" if rb.get("required") else ""))
                L += self.expand(sch, 0, MAX_DEPTH, set(), 1) if self.is_complex(sch) else [f"  - {self.type_label(sch)}{self.constraints(sch)}"]
        resps = op.get("responses") or {}
        ok = [c for c in resps if str(c).startswith("2")]
        errs = [str(c) for c in resps if not str(c).startswith("2")]
        for c in ok[:1]:
            r = resps[c]
            r = self.deref(r) if "$ref" in r else r
            content = r.get("content") or {}
            if content:
                ct, media = next(iter(content.items()))
                sch = media.get("schema") or {}
                nm = self.ref_name(sch)
                L.append(f"- **Response {c}**" + (f" (`{nm}`)" if nm else (f" (`{ct}`)" if ct != "application/json" else "")))
                if self.is_complex(sch):
                    L += self.expand(sch, 0, MAX_DEPTH, set(), 1)
                elif sch:
                    L.append(f"  - {self.type_label(sch)}{self.constraints(sch)}")
            # réponse sans contenu : rien à afficher (format V2)
        for c in ok[1:]:
            errs.insert(0, str(c))
        if errs:
            L.append("- Errors: " + ", ".join(f"`{e}`" for e in errs))
        L.append("")
        return L

    def operations(self):
        """Liste ordonnée (tag, méthode, chemin, op, path_item)."""
        out = []
        for path, item in (self.spec.get("paths") or {}).items():
            for m in METHODS:
                if m in item:
                    op = item[m]
                    tag = (op.get("tags") or ["Other"])[0]
                    out.append((tag, m, path, op, item))
        return out

    def appendix(self, title):
        names = sorted(self.schemas)
        L = [f"### Schemas appendix — {title}", "", f"<details><summary>{len(names)} component schemas</summary>", ""]
        for n in names:
            raw = {"$ref": f"#/components/schemas/{n}"}
            s = self.merged(raw)
            L.append(f"**`{n}`**")
            L.append("")
            if s.get("description"):
                L.append(f"_{clean(s['description'])}_")
                L.append("")
            if self.is_complex(raw):
                L += self.expand(raw, 0, APPX_DEPTH, set(), 0)
            else:
                L.append(f"- {self.type_label(raw)}{self.constraints(raw)}")
            L.append("")
        L += ["</details>", ""]
        return L


def render_section(spec_path, title, new_routes=frozenset(), new_service=False):
    spec = load(spec_path)
    g = Gen(spec)
    info = spec.get("info") or {}
    L = [f"## {title}" + (" 🆕" if new_service else ""), "", f"_OpenAPI: {clean(info.get('title'))} — version {info.get('version') or '—'}_", ""]
    servers = spec.get("servers") or []
    if servers:
        L += ["**Servers**", ""]
        for s in servers:
            L.append(f"- `{s.get('url')}` — {clean(s.get('description'))}")
        L.append("")
    ops = g.operations()
    tags = []
    for t, *_ in ops:
        if t not in tags:
            tags.append(t)
    blocks = {}
    for tag in tags:
        L += [f"### {tag}", ""]
        for t, m, p, op, item in ops:
            if t != tag:
                continue
            b = g.render_op(m, p, op, item)
            if (m.upper(), p) in new_routes:
                b[0] += " 🆕"
            blocks[(m.upper(), p)] = b
            L += b
    return L, g, blocks


if __name__ == "__main__":
    lines, g, _ = render_section(sys.argv[1], sys.argv[2])
    lines += g.appendix(sys.argv[2])
    print("\n".join(lines))
