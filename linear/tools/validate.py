#!/usr/bin/env python3
"""Sprawdza spójność linear-plan.json, reguł zależności i folderów roboczych.

Użycie: python3 linear/tools/validate.py [katalog_repozytorium]
"""
import collections, json, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIN = os.path.join(ROOT, "linear")
plan = json.load(open(os.path.join(LIN, "linear-plan.json"), encoding="utf-8"))
src = open(os.path.join(LIN, "deploy_linear.py"), encoding="utf-8").read()
ISSUE_LABELS = set(re.findall(r'^\s+"(.*?)": "#[0-9A-F]{6}",', src, re.M))
P, I = plan["projects"], plan["issues"]
K = {i["key"]: i for i in I}
errors, warns = [], []


def E(msg):
    errors.append(msg)


def W(msg):
    warns.append(msg)


# 1. klucze i blokady
for i in I:
    if len(set(i["blockedBy"])) != len(i["blockedBy"]):
        E(f"{i['key']}: zduplikowane blokady")
    for b in i["blockedBy"]:
        if b not in K:
            E(f"{i['key']}: nieistniejąca blokada {b}")
        if b == i["key"]:
            E(f"{i['key']}: blokuje sam siebie")
if len(K) != len(I):
    E("zduplikowane klucze zadań")
ms_keys = [m["key"] for p in P for m in p["milestones"]]
if len(set(ms_keys)) != len(ms_keys):
    E("zduplikowane klucze kamieni milowych")
MS = {m["key"]: (p, m) for p in P for m in p["milestones"]}
for i in I:
    if i["milestone"] and i["milestone"] not in MS:
        E(f"{i['key']}: nieznany kamień milowy {i['milestone']}")
    if i["milestone"] and MS[i["milestone"]][0]["key"] != i["project"]:
        E(f"{i['key']}: kamień milowy z innego projektu")

# 2. cykle
blocks = collections.defaultdict(list)
indeg = collections.Counter()
for i in I:
    for b in i["blockedBy"]:
        blocks[b].append(i["key"])
        indeg[i["key"]] += 1
q = [k for k in K if indeg[k] == 0]
roots = sorted(q)
seen = 0
while q:
    n = q.pop()
    seen += 1
    for m in blocks[n]:
        indeg[m] -= 1
        if indeg[m] == 0:
            q.append(m)
if seen != len(I):
    E(f"graf ma cykl ({len(I) - seen} zadań w cyklach)")
if roots != ["S01-START", "S02-START"]:
    E(f"zadania bez blokad: {roots}")
for i in I:
    want = "Todo" if i["key"] in ("S01-START", "S02-START") else "Backlog"
    if i["status"] != want:
        E(f"{i['key']}: status {i['status']}, oczekiwany {want}")


# 3. etapy
def preds(key, memo={}):
    if key in memo:
        return memo[key]
    out = set()
    st = list(K[key]["blockedBy"])
    while st:
        x = st.pop()
        if x not in out:
            out.add(x)
            st.extend(K[x]["blockedBy"])
    memo[key] = out
    return out


for p in P:
    for m in p["milestones"]:
        items = [i for i in I if i["milestone"] == m["key"]]
        d = [i for i in items if i["key"].endswith("-D")]
        if len(d) != 1:
            E(f"{m['key']}: {len(d)} dowodów")
            continue
        d = d[0]
        optional_stage = "(opcjonalnie)" in m["name"]
        expert = d["title"].startswith("Dowód poziomu E")
        for i in items:
            if i is d:
                continue
            opt = "opcjonalne" in i["labels"] and not optional_stage
            if opt and i["key"] in d["blockedBy"]:
                E(f"{i['key']}: materiał opcjonalny blokuje dowód")
            if not opt and i["key"] not in d["blockedBy"]:
                E(f"{i['key']}: nie blokuje dowodu etapu")
            if opt and blocks[i["key"]]:
                E(f"{i['key']}: materiał opcjonalny coś blokuje")
        ents = {tuple(i["blockedBy"]) for i in items if i is not d}
        if len(ents) > 1:
            E(f"{m['key']}: różne blokady wejścia w etapie")
        if not blocks[d["key"]] and not expert and not optional_stage:
            E(f"{d['key']}: dowód etapu nie blokuje niczego (ślepy zaułek)")
        if optional_stage and blocks[d["key"]]:
            E(f"{d['key']}: etap opcjonalny coś blokuje")
        if optional_stage and any("opcjonalne" not in i["labels"] for i in items):
            E(f"{m['key']}: zadanie bez etykiety „opcjonalne” w etapie opcjonalnym")
        if expert and blocks[d["key"]]:
            W(f"{d['key']}: dowód poziomu E blokuje {blocks[d['key']]}")
    # etap ekspercki wymaga wszystkich nieopcjonalnych etapów
    exp = [i for i in I if i["project"] == p["key"] and i["title"].startswith("Dowód poziomu E")]
    if len(exp) != 1:
        E(f"{p['key']}: {len(exp)} dowodów poziomu E")
    else:
        pr = preds(exp[0]["key"])
        for m in p["milestones"]:
            dk = m["key"] + "-D"
            if dk == exp[0]["key"] or "(opcjonalnie)" in m["name"]:
                continue
            if dk not in pr:
                E(f"{p['key']}: dowód poziomu E nie wymaga {dk}")
    st = K[p["key"] + "-START"]
    first = [i for i in I if i["project"] == p["key"] and "-START" in " ".join(i["blockedBy"])]
    if not first:
        E(f"{p['key']}: start niczego nie odblokowuje")

# 4. etykiety, pola, tytuły
need = ["Materiał", "Autor / wydawca", "Typ", "Czas", "Koszt", "Link"]
for i in I:
    for l in i["labels"]:
        if l not in ISSUE_LABELS:
            E(f"{i['key']}: etykieta spoza ISSUE_LABELS: {l}")
    kind = i["key"].split("-")[-1]
    if kind.startswith("M"):
        for f in need:
            if not re.search(r"\*\*" + re.escape(f) + r":\*\* \S", i["description"]):
                E(f"{i['key']}: brak pola {f}")
        if not i["title"].startswith("Przerobić: "):
            E(f"{i['key']}: tytuł materiału bez „Przerobić:”")
        if "materiał" not in i["labels"]:
            E(f"{i['key']}: brak etykiety materiał")
    if len(i["title"]) > 120:
        W(f"{i['key']}: tytuł ma {len(i['title'])} znaków")
    if i["title"].count("„") != i["title"].count("”"):
        W(f"{i['key']}: niezamknięty cudzysłów w tytule: {i['title']}")
    m = re.findall(r"\*\*Folder roboczy:\*\* `(.*?)`", i["description"])
    if len(m) != 1:
        E(f"{i['key']}: {len(m)} wierszy „Folder roboczy”")
    elif not os.path.isdir(os.path.join(ROOT, m[0])):
        E(f"{i['key']}: folder {m[0]} nie istnieje")
    if not i["description"].rstrip().endswith("`") or "**Folder roboczy:**" not in i["description"].split("\n")[-1]:
        E(f"{i['key']}: opis nie kończy się wierszem „Folder roboczy”")
for p in P:
    if len(p["summary"]) > 255:
        W(f"{p['key']}: podsumowanie > 255 znaków (zostanie ucięte)")
    if len(p["name"]) > 80:
        W(f"{p['key']}: nazwa projektu > 80 znaków")
    for m in p["milestones"]:
        if len(m["name"]) > 80:
            W(f"{m['key']}: nazwa kamienia milowego ma {len(m['name'])} znaków")
    if "start" in p or "target" in p:
        E(f"{p['key']}: projekt ma daty (start/target)")

# 5. pozostałości szacunków czasu
pat = re.compile(r"Czas od zera|Razem od zera|(?:miesięcy|miesiące|miesiąca) przy|h tygodniowo przy|Czas podany dla osoby")
for p in P:
    for t in [p["description"]] + [m["description"] for m in p["milestones"]]:
        for mm in pat.finditer(t):
            E(f"{p['key']}: pozostałość szacunku czasu: …{t[max(0, mm.start() - 40):mm.end() + 40]}…")

# 6. spójność relacji projektów
for p in P:
    st = K[p["key"] + "-START"]
    sp = sorted({b[:3] for b in st["blockedBy"]})
    if sp != sorted(p["blockedBy"]):
        E(f"{p['key']}: blockedBy projektu {sorted(p['blockedBy'])} ≠ projekty blokujące start {sp}")
    m = re.search(r"Opiera się na: ([^.;]*)", p["summary"])
    nums = sorted(int(x) for x in re.findall(r"\b(\d+)\b", m.group(1))) if m else []
    if m and nums != sorted(int(k[1:]) for k in p["blockedBy"]):
        W(f"{p['key']}: „Opiera się na” w podsumowaniu ({nums}) ≠ blockedBy {p['blockedBy']}")
    if p["summary"] not in p["description"].split("\n")[0]:
        E(f"{p['key']}: pierwsza linia opisu ≠ podsumowanie")
    for mm in re.finditer(r"Ścieżka ma (\d+) etap", p["description"]):
        n = sum(1 for m in p["milestones"] if m["key"].split("-")[1].startswith("E"))
        if int(mm.group(1)) != n:
            E(f"{p['key']}: „Ścieżka ma {mm.group(1)} etap…”, a etapów jest {n}")

# 7. pozostałości roboczych znaczników
for p in P:
    for t in [p["description"], p["summary"]] + [m["description"] + m["name"] for m in p["milestones"]]:
        if "TODO" in t:
            E(f"{p['key']}: tekst zawiera TODO")
for i in I:
    if "TODO" in i["description"] or "TODO" in i["title"]:
        E(f"{i['key']}: tekst zawiera TODO")

# 8. podsumowanie
c = collections.Counter(i["key"].split("-")[-1][0] if i["key"].split("-")[-1] != "START" else "S" for i in I)
print(f"Projekty: {len(P)}, kamienie milowe: {len(ms_keys)}, zadania: {len(I)} (start {c['S']}, materiały {c['M']}, "
      f"dowody {c['D']}, praktyki {c['P']}), relacje: {sum(len(i['blockedBy']) for i in I)}")
for w in warns:
    print("OSTRZEŻENIE:", w)
for e in errors:
    print("BŁĄD:", e)
print(f"{len(errors)} błędów, {len(warns)} ostrzeżeń")
sys.exit(1 if errors else 0)
