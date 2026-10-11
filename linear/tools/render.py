#!/usr/bin/env python3
"""Generuje pliki Markdown planu (00, 01–22, README) z linear/linear-plan.json i tools/meta.json.

Użycie: python3 linear/tools/render.py [katalog_repozytorium [katalog_wyjściowy [meta.json]]]
"""
import json, os, re, sys, collections

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = sys.argv[1] if len(sys.argv) > 1 else REPO
OUT = sys.argv[2] if len(sys.argv) > 2 else ROOT
LIN = os.path.join(ROOT, "linear")
META_PATH = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "meta.json")
TPL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

plan = json.load(open(os.path.join(LIN, "linear-plan.json"), encoding="utf-8"))
meta = json.load(open(META_PATH, encoding="utf-8"))
P = plan["projects"]
I = plan["issues"]
BYKEY = {i["key"]: i for i in I}
PBY = {p["key"]: p for p in P}
MS = {m["key"]: (p, m) for p in P for m in p["milestones"]}
STATE_PATH = os.path.join(LIN, "linear-deploy-state.json")
DEPLOYED = json.load(open(STATE_PATH, encoding="utf-8"))["issues"] if os.path.exists(STATE_PATH) else {}


def lea(key):
    """Identyfikator zadania w Linear albo „—”, jeśli zadanie nie jest wdrożone."""
    return DEPLOYED[key]["identifier"] if key in DEPLOYED else "—"


BLOCKS = collections.defaultdict(list)
for i in I:
    for b in i["blockedBy"]:
        BLOCKS[b].append(i["key"])


def num(key):
    return int(key[1:3])


def proj_of(key):
    return key[:3]


def stage_of(key):
    """S05-E2-M1 -> S05-E2; S05-START -> None."""
    parts = key.split("-")
    return None if parts[1] == "START" else parts[0] + "-" + parts[1]


def plural(n, one, few, many):
    if n == 1:
        return one
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return few
    return many


def field(desc, name):
    m = re.search(r"\*\*" + re.escape(name) + r":\*\* (.*?)(?:  \n|\n|$)", desc)
    return m.group(1).strip() if m else None


def ms_field(desc, name):
    m = re.search(r"\*\*" + re.escape(name) + r":\*\* (.*?)(?: · \*\*|\n|$)", desc)
    return m.group(1).strip() if m else ""


def is_optional_ms(m):
    return "(opcjonalnie)" in m["name"]


def is_supp(m):
    return m["key"].split("-")[1].startswith("U")


def folder_of(p):
    return meta["projects"][p["key"]]["file"][:-3]


def ms_slug(m):
    import unicodedata
    name = m["name"]
    name = re.sub(r"^(Etap \d+: |Uzupełniająca [\d.]+ · )", "", name)
    s = name.lower().replace("ł", "l")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return m["key"].split("-")[1].lower() + "-" + s


def ms_folder(m):
    p = MS[m["key"]][0]
    return f"{folder_of(p)}/{ms_slug(m)}/"


def ms_label(m):
    """Etykieta w diagramie: dla ścieżek uzupełniających „12.2 · etap k: nazwa”."""
    if is_supp(m):
        mm = re.match(r"Uzupełniająca ([\d.]+) · (.*)", m["name"])
        k = m["key"].split("-")[1][1:]
        return f"{mm.group(1)} · etap {k}: {mm.group(2)}"
    return m["name"]


def ms_table_name(m):
    return m["name"]


def typ(i):
    labels = [l for l in i["labels"] if l not in ("ścieżka uzupełniająca", "opcjonalne")]
    ms = MS.get(i["milestone"]) if i["milestone"] else None
    if "opcjonalne" in i["labels"] and ms and not is_optional_ms(ms[1]):
        labels.append("opcjonalne")
    return ", ".join(labels)


def keys(lst):
    return ", ".join(f"`{k}`" for k in lst) if lst else "—"


def project_issues(pk):
    return [i for i in I if i["project"] == pk]


def kind(i):
    k = i["key"].split("-")[-1]
    if k == "START":
        return "start"
    if k == "D":
        return "D"
    return k[0]  # M lub P


def stage_blockers(m):
    """Uporządkowana suma blokad zadań etapu spoza etapu (bez dowodu etapu)."""
    out = []
    for i in I:
        if i["milestone"] != m["key"] or kind(i) == "D":
            continue
        for b in i["blockedBy"]:
            if stage_of(b) == m["key"]:
                continue
            if b not in out:
                out.append(b)
    return out


def cross_in(pk):
    rows = []
    for i in project_issues(pk):
        for b in i["blockedBy"]:
            if proj_of(b) != pk:
                rows.append((b, i["key"]))
    return rows



ISSUE_ORDER = {i["key"]: n for n, i in enumerate(I)}


def partial_in(pk):
    """Zależności częściowe wchodzące: (etap tego projektu, projekt blokujący, etap blokujący)."""
    out = []
    for b, t in cross_in(pk):
        if t.endswith("-START"):
            continue
        sm = stage_of(t)
        e = (sm.split("-")[1], proj_of(b), stage_of(b).split("-")[1])
        if e not in out:
            out.append(e)
    return out


def partial_out(pk):
    out = []
    for i in I:
        if i["project"] == pk or i["key"].endswith("-START"):
            continue
        for b in i["blockedBy"]:
            if proj_of(b) == pk:
                e = (i["project"], stage_of(i["key"]).split("-")[1])
                if e not in out:
                    out.append(e)
    return out


def stage_word(s):
    k = s[1:]
    return f"etap {k}" if s[0] == "E" else f"ścieżka uzupełniająca, etap {k}"


def blocks_projects(pk):
    return [p["key"] for p in P if pk in p["blockedBy"]]


def pname(pk):
    return PBY[pk]["name"]


def counts(pk):
    iss = project_issues(pk)
    c = collections.Counter(kind(i) for i in iss)
    return len(iss), c["M"], c["D"], c["P"]


def short_summary(pk):
    n, m, d, pr = counts(pk)
    nm = len(PBY[pk]["milestones"])
    return (f"{nm} {plural(nm, 'kamień milowy', 'kamienie milowe', 'kamieni milowych')}, "
            f"{n} {plural(n, 'zadanie', 'zadania', 'zadań')} (1 start, {m} {plural(m, 'materiał', 'materiały', 'materiałów')}, "
            f"{d} {plural(d, 'dowód', 'dowody', 'dowodów')}, {pr} {plural(pr, 'praktyka', 'praktyki', 'praktyk')})")


def render_section(p):
    pk = p["key"]
    pm = meta["projects"][pk]
    iss = project_issues(pk)
    start = BYKEY[f"{pk}-START"]
    first_m = next(i["key"] for i in iss if kind(i) == "M")
    L = []
    L.append(f"# {p['name']}: plan wdrożenia w Linear\n")
    if DEPLOYED:
        L.append(f"Team **LEA** (https://linear.app/daankh/team/LEA/overview). Plan jest wdrożony w Linear. Klucze zadań (np. `{first_m}`) są robocze, a identyfikator każdego zadania w Linear (`LEA-…`) jest w kolumnie „Linear” tabel zadań i w pliku `mapowanie-kluczy.csv`.\n")
    else:
        L.append(f"Team **LEA** (https://linear.app/daankh/team/LEA/overview). Plan do przeglądu przed wdrożeniem: nic nie zostało jeszcze utworzone w Linear. Klucze zadań (np. `{first_m}`) są robocze; po wdrożeniu dostaną identyfikatory `LEA-…`.\n")
    L.append(f"**W skrócie:** {short_summary(pk)}. Plik główny z kolejnością projektów: `00-kolejnosc-i-zaleznosci.md`.\n")
    L.append("## 1. Projekt\n")
    L.append("| Pole | Wartość |\n|---|---|")
    L.append(f"| Nazwa | {p['name']} |")
    L.append("| Team | LEA |")
    L.append(f"| Podsumowanie (pole „Summary”) | {p['summary']} |")
    L.append(f"| Etykiety projektu | `{p['label']}` |")
    L.append(f"| Blokowany przez (projekty) | {', '.join(pname(k) for k in p['blockedBy']) or '—'} |")
    L.append(f"| Blokuje (projekty) | {', '.join(pname(k) for k in blocks_projects(pk)) or '—'} |")
    pin = partial_in(pk)
    if pin:
        L.append("| Zależności częściowe (wchodzące) | " + "; ".join(
            f"{stage_word(s)} czeka na {pname(bp)} ({stage_word(bs)})" for s, bp, bs in pin) + " |")
    pout = partial_out(pk)
    if pout:
        L.append("| Zależności częściowe (wychodzące) | " + "; ".join(
            f"{pname(tp)}, {stage_word(ts)}" for tp, ts in pout) + " |")
    L.append("")
    L.append("### Opis projektu (do wklejenia w Linear)\n")
    L.append(p["description"] + "\n")
    L.append("## 2. Kamienie milowe\n")
    L.append("Jeden kamień milowy na etap ścieżki. Kamień milowy jest zamknięty, gdy zamknięte jest zadanie dowodu tego etapu.\n")
    L.append("| # | Kamień milowy | Cel | Poziom po etapie | Zadania |\n|---|---|---|---|---|")
    for n, m in enumerate(p["milestones"], 1):
        d = m["description"]
        cnt = sum(1 for i in iss if i["milestone"] == m["key"])
        L.append(f"| {n} | {ms_table_name(m)} | {ms_field(d, 'Cel')} | {ms_field(d, 'Poziom po etapie') or '—'} | {cnt} |")
    L.append("")
    L.append("## 3. Punkt startu\n")
    has_supp = any(is_supp(m) for m in p["milestones"])
    linear_ref = f" ({lea(start['key'])} w Linear)" if start["key"] in DEPLOYED else ""
    L.append(f"Zadanie **`{start['key']}` · {start['title']}**{linear_ref} to jedyne wejście do projektu: wszystkie zadania pierwszego etapu{' i ścieżek uzupełniających' if has_supp else ''} są przez nie blokowane.\n")
    L.append(f"- **Blokowane przez:** {keys(start['blockedBy'])}")
    L.append(f"- **Odblokowuje:** {keys(BLOCKS[start['key']])}")
    if start["status"] == "Todo":
        L.append("- **Status początkowy:** Todo (brak warunków wejścia)")
    else:
        L.append("- **Status początkowy:** Backlog do czasu zamknięcia zadań blokujących, potem Todo")
    L.append("")
    L.append("Opis zadania (do wklejenia):\n")
    L.append(start["description"] + "\n")
    L.append("## 4. Przepływ zależności\n")
    L.append("Linie ciągłe to zależności wewnątrz projektu, przerywane to zadania z innych projektów. Wewnątrz etapu zadania materiałów są równoległe i wszystkie blokują dowód etapu; dowód etapu blokuje materiały kolejnego etapu.\n")
    L.append("```mermaid\nflowchart TD")
    L.append(f'  START["{num(pk)}. Start"]')
    for m in p["milestones"]:
        L.append(f'  {m["key"].split("-")[1]}["{ms_label(m).replace("`", "")}"]')
    for m in p["milestones"]:
        node = m["key"].split("-")[1]
        for b in stage_blockers(m):
            if proj_of(b) == pk:
                src = "START" if b.endswith("START") else stage_of(b).split("-")[1]
                L.append(f"  {src} --> {node}")
            else:
                L.append(f'  X{b.replace("-", "")}(["{b}"]) -.-> {node}')
    for b in start["blockedBy"]:
        L.append(f'  X{b.replace("-", "")}(["{b}"]) -.-> START')
    L.append("```\n")
    L.append("## 5. Zadania według kamieni milowych\n")
    L.append("Szablon opisu zadania materiału: nazwa materiału, autor lub wydawca, typ, czas, koszt i link (jak w kolumnach poniżej), zdanie „Gotowe, gdy materiał jest przerobiony w zakresie potrzebnym do dowodu etapu” oraz folder roboczy z kolumny „Folder”. Opisy dowodów i praktyk są podane pod tabelą każdego etapu.\n")
    for m in p["milestones"]:
        L.append(f"### {m['name']}\n")
        L.append("Opis kamienia milowego (do wklejenia):\n")
        L.append(m["description"] + "\n")
        L.append("| Klucz | Linear | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |\n|---|---|---|---|---|---|---|---|---|---|")
        mi = [i for i in iss if i["milestone"] == m["key"]]
        for i in mi:
            if kind(i) == "M":
                d = i["description"]
                cz, ko, li = field(d, "Czas"), field(d, "Koszt"), field(d, "Link")
            else:
                cz = ko = li = "—"
            L.append(f"| `{i['key']}` | {lea(i['key'])} | {i['title']} | {typ(i)} | {cz} | {ko} | {li} | {keys(i['blockedBy'])} | {keys(BLOCKS[i['key']])} | `{ms_folder(m)}` |")
        L.append("")
        for i in mi:
            if kind(i) in ("P", "D"):
                L.append(f"**`{i['key']}` · {i['title']}**\n")
                L.append(i["description"] + "\n")
    L.append("## 6. Relacje z innymi projektami\n")
    L.append("**Wchodzące** (zadanie z innego projektu blokuje zadanie tego projektu):\n")
    rin = cross_in(pk)
    if rin:
        for b, t in rin:
            L.append(f"- `{b}` ({BYKEY[b]['title']}) → `{t}`")
    else:
        L.append("- brak")
    L.append("")
    L.append("**Wychodzące** (zadanie tego projektu blokuje zadanie w innym projekcie):\n")
    rout = [(b, t) for b in [i["key"] for i in iss] for t in BLOCKS[b] if proj_of(t) != pk]
    if rout:
        for b, t in rout:
            L.append(f"- `{b}` → `{t}` ({pname(proj_of(t))})")
    else:
        L.append("- brak")
    return "\n".join(L) + "\n"


def all_cross():
    rows = []
    for i in I:
        for b in i["blockedBy"]:
            if proj_of(b) != i["project"]:
                rows.append((b, i["key"]))
    rows.sort(key=lambda r: (num(r[1]), r[1].endswith("-START")))
    return rows


def reason(b, t):
    if t.endswith("-START"):
        d = BYKEY[t]["description"]
        m = re.search(r"- `" + re.escape(b) + r"` · .*? — (.*)", d)
        return m.group(1)
    why = meta["partialReasons"].get(f"{b}>{stage_of(t)}")
    if not why:
        raise SystemExit(f"Brak powodu relacji częściowej {b} > {stage_of(t)}")
    return why


def transitive_reduction(edges):
    adj = collections.defaultdict(set)
    for a, b in edges:
        adj[a].add(b)

    def reach(a, b, skip):
        st, seen = [a], set()
        while st:
            x = st.pop()
            for y in adj[x]:
                if (x, y) == skip:
                    continue
                if y == b:
                    return True
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        return False
    return [(a, b) for a, b in edges if not reach(a, b, (a, b))]


def render_00():
    tpl = open(os.path.join(TPL_DIR, "00.md"), encoding="utf-8").read()
    c = collections.Counter(kind(i) for i in I)
    n_ms = sum(len(p["milestones"]) for p in P)
    n_rel = sum(len(i["blockedBy"]) for i in I)
    cross = all_cross()
    paid = sum(1 for i in I if "płatny" in i["labels"])
    opt_stage = sum(1 for i in I if i["milestone"] and is_optional_ms(MS[i["milestone"]][1]))
    opt_mat = sum(1 for i in I if "opcjonalne" in i["labels"] and i["milestone"] and not is_optional_ms(MS[i["milestone"]][1]))
    vals = dict(n_proj=len(P), n_ms=n_ms, n_start=c["start"], n_mat=c["M"], n_proof=c["D"], n_prac=c["P"],
                n_rel=n_rel, n_cross=len(cross), n_iss=len(I), n_paid=paid, n_opt_stage=opt_stage, n_opt_mat=opt_mat)
    # tabela projektów
    rows = []
    for n, p in enumerate(P, 1):
        pm = meta["projects"][p["key"]]
        start = BYKEY[p["key"] + "-START"]
        rows.append(f"| {n} | [{p['name']}]({pm['file']}) | {meta['layers'][p['label']]} | "
                    f"{', '.join(f'{num(k):02d}' for k in p['blockedBy']) or '—'} | "
                    f"{', '.join(f'{num(k):02d}' for k in blocks_projects(p['key'])) or '—'} | "
                    f"{keys(start['blockedBy'])} | {len(project_issues(p['key']))} |")
    vals["project_rows"] = "\n".join(rows)
    g = ["```mermaid", "flowchart TD"]
    for p in P:
        g.append(f'  P{num(p["key"])}["{p["name"]}"]')
    edges = [(b, p["key"]) for p in P for b in p["blockedBy"]]
    edges.sort(key=lambda e: (num(e[1]), num(e[0])))
    for a, b in transitive_reduction(edges):
        g.append(f"  P{num(a)} --> P{num(b)}")
    seen = []
    for b, t in cross:
        if t.endswith("-START"):
            continue
        e = (proj_of(b), proj_of(t), stage_of(t).split("-")[1])
        if e not in seen:
            seen.append(e)
    for a, b, s in seen:
        g.append(f"  P{num(a)} -.->|{stage_word(s)}| P{num(b)}")
    g.append("```")
    vals["project_graph"] = "\n".join(g)
    rel = []
    for b, t in cross:
        kindtxt = "start projektu" if t.endswith("-START") else "częściowa"
        rel.append(f"| `{b}` · {BYKEY[b]['title']} | `{t}` · {BYKEY[t]['title']} | {kindtxt} | {reason(b, t)} |")
    vals["relation_rows"] = "\n".join(rel)
    files = []
    for p in P:
        pm = meta["projects"][p["key"]]
        files.append(f"| [{pm['file']}]({pm['file']}) | {p['name']} | {len(p['milestones'])} | {len(project_issues(p['key']))} |")
    vals["file_rows"] = "\n".join(files)
    vals.update(txts())
    return tpl.format(**vals)


def txts():
    n_ms = sum(len(p["milestones"]) for p in P)
    return dict(proj_txt=f"{len(P)} {plural(len(P), 'projekt', 'projekty', 'projektów')}",
                ms_txt=f"{n_ms} {plural(n_ms, 'kamień milowy', 'kamienie milowe', 'kamieni milowych')}",
                iss_txt=f"{len(I)} {plural(len(I), 'zadanie', 'zadania', 'zadań')}")


def render_readme():
    tpl = open(os.path.join(TPL_DIR, "README.md"), encoding="utf-8").read()
    c = collections.Counter(kind(i) for i in I)
    rows = []
    for p in P:
        pm = meta["projects"][p["key"]]
        f = folder_of(p)
        rows.append(f"| [{p['name']}](linear/{pm['file']}) | {meta['layers'][p['label']]} | {len(p['milestones'])} | "
                    f"{len(project_issues(p['key']))} | [`{f}/`]({f}/) |")
    n_ms = sum(len(p["milestones"]) for p in P)
    return tpl.format(n_proj=len(P), n_ms=n_ms, n_iss=len(I), n_rel=sum(len(i["blockedBy"]) for i in I), **txts(),
                      n_start=c["start"], n_mat=c["M"], n_proof=c["D"], n_prac=c["P"], project_rows="\n".join(rows))


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "linear"), exist_ok=True)
    for p in P:
        with open(os.path.join(OUT, "linear", meta["projects"][p["key"]]["file"]), "w", encoding="utf-8") as f:
            f.write(render_section(p))
    with open(os.path.join(OUT, "linear", "00-kolejnosc-i-zaleznosci.md"), "w", encoding="utf-8") as f:
        f.write(render_00())
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write(render_readme())
