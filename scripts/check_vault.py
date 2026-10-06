#!/usr/bin/env python3
"""Перевірка vault: frontmatter, коректність wiki-посилань, досяжність усіх нотаток з MOC.
Запуск: python3 scripts/check_vault.py [--dot graph.dot]
Скрипт призначений для людини (студента); агент працює з vault лише через MCP."""
import re, sys, pathlib, collections
ROOT = pathlib.Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else pathlib.Path(__file__).resolve().parent.parent
TYPES = {"concept", "component", "decision", "glossary", "moc"}
RELATIONS = {  # зв'язок: (допустимі типи джерела, допустимі типи цілі)
    "depends_on": ({"component"}, {"component"}),
    "implements": ({"component"}, {"concept"}),
    "part_of": ({"concept"}, {"concept"}),
    "decided_by": ({"component", "concept"}, {"decision"}),
    "supersedes": ({"decision"}, {"decision"}),
}
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)  # посилання всередині коду не рахуються
LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")

def parse(p):
    t = p.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    fm, body = {}, t
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); fm[k.strip()] = v.strip()
        body = m.group(2)
    return fm, body

def load():
    notes = {}
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in (".git", "_templates") or rel.name == "README.md":
            continue
        fm, body = parse(p)
        notes[p.stem] = {"path": str(rel), "fm": fm, "links": set(LINK.findall(fm_text(p) + CODE.sub("", body)))}
    return notes

def fm_text(p):
    m = re.match(r"---\n(.*?)\n---\n", p.read_text(encoding="utf-8"), re.S)
    return m.group(1) if m else ""

def main():
    notes = load(); errors = []
    for name, n in notes.items():
        fm = n["fm"]
        if fm.get("type") not in TYPES: errors.append(f"{n['path']}: невідомий або відсутній type")
        for req in ("created", "tags"):
            if req not in fm: errors.append(f"{n['path']}: немає поля {req}")
        for l in n["links"]:
            if l.strip() not in notes: errors.append(f"{n['path']}: бите посилання [[{l}]]")
    rel_count = collections.Counter()
    for name, n in notes.items():
        for rel, (src_t, dst_t) in RELATIONS.items():
            if rel not in n["fm"]: continue
            if n["fm"].get("type") not in src_t:
                errors.append(f"{n['path']}: зв'язок {rel} недопустимий для type={n['fm'].get('type')}")
            for tgt in LINK.findall(n["fm"][rel]):
                tgt = tgt.strip(); rel_count[rel] += 1
                if tgt not in notes: errors.append(f"{n['path']}: {rel} → неіснуюча [[{tgt}]]")
                elif notes[tgt]["fm"].get("type") not in dst_t:
                    errors.append(f"{n['path']}: {rel} → [[{tgt}]] має type={notes[tgt]['fm'].get('type')}, очікується {sorted(dst_t)}")
    start = "MOC-Застосунок"; seen = {start}; q = collections.deque([start])
    while q:
        for l in notes[q.popleft()]["links"]:
            l = l.strip()
            if l in notes and l not in seen: seen.add(l); q.append(l)
    unreachable = sorted(set(notes) - seen)
    by = collections.Counter(n["fm"].get("type") for n in notes.values())
    edges = sum(len(n["links"]) for n in notes.values())
    print(f"Нотаток: {len(notes)}; за типами: {dict(by)}; посилань: {edges}")
    print(f"Типізованих зв'язків: {sum(rel_count.values())}; за типами: {dict(rel_count)}")
    print(f"Досяжних з MOC: {len(seen)} з {len(notes)}")
    for u in unreachable: print("  НЕДОСЯЖНА:", u)
    for e in errors: print("  ПОМИЛКА:", e)
    if "--dot" in sys.argv:
        col = {"concept": "#DDEBF7", "component": "#E2F0D9", "decision": "#FFF2CC", "glossary": "#F2F2F2", "moc": "#F8CBAD"}
        out = ['digraph G {rankdir=LR; layout=fdp; overlap=false; splines=true; node [fontname="DejaVu Sans",fontsize=9,shape=box,style="rounded,filled"]; edge [color="#888888",arrowsize=0.5];']
        for k, n in notes.items(): out.append(f'"{k}" [fillcolor="{col.get(n["fm"].get("type"), "white")}"];')
        for k, n in notes.items():
            for l in n["links"]:
                if l.strip() in notes: out.append(f'"{k}" -> "{l.strip()}";')
        out.append("}"); pathlib.Path(sys.argv[sys.argv.index("--dot") + 1]).write_text("\n".join(out), encoding="utf-8")
    sys.exit(1 if errors or unreachable else 0)
main()
