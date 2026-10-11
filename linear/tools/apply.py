#!/usr/bin/env python3
"""Stosuje skrypty edycji do planu i odświeża wszystko, co z niego wynika.

Użycie:
    python3 linear/tools/apply.py                 # bez edycji: przegenerowanie Markdown, foldery, walidacja
    python3 linear/tools/apply.py moja_edycja.py  # edycja (funkcja apply(pl)), potem jak wyżej
    python3 linear/tools/apply.py --root KATALOG edycja.py   # na kopii repozytorium (do prób)

Kroki: wczytanie linear/linear-plan.json i tools/meta.json do modelu (model.Plan), wywołanie apply(pl)
z każdego podanego pliku, zapis JSON z nową numeracją kluczy, aktualizacja powodów relacji w meta.json,
generowanie plików Markdown (render.py), synchronizacja folderów roboczych i walidacja (validate.py).

Po wdrożeniu (istnieje linear/linear-deploy-state.json) edycja, która zmienia klucz albo usuwa wdrożone
zadanie lub kamień milowy, jest przerywana przed zapisem: klucze w stanie wdrożenia i w Linear przestałyby
się zgadzać. --allow-renumber wyłącza tę blokadę (tylko przy świadomej migracji Linear i pliku stanu).
Na końcu skrypt wypisuje, które obiekty trzeba zaktualizować lub utworzyć w Linear.
"""
import argparse, importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from model import Plan  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("edits", nargs="*", help="pliki Pythona z funkcją apply(pl)")
ap.add_argument("--root", default=os.path.dirname(os.path.dirname(HERE)), help="katalog repozytorium")
ap.add_argument("--allow-renumber", action="store_true",
                help="pozwól zmienić klucze lub usunąć obiekty już wdrożone do Linear (wymaga ręcznej migracji)")
args = ap.parse_args()
ROOT = os.path.abspath(args.root)
PLAN = os.path.join(ROOT, "linear", "linear-plan.json")
META = os.path.join(ROOT, "linear", "tools", "meta.json")

plan = json.load(open(PLAN, encoding="utf-8"))
meta = json.load(open(META, encoding="utf-8"))
pl = Plan(plan, meta)
for f in args.edits:
    spec = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(f))[0], f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.apply(pl)
    print("edycja:", f)

out, keymap, msmap, reasons = pl.emit()
renamed = {old: new for old, new in keymap.items() if old != new}

# --- ochrona wdrożonego planu
STATE = os.path.join(ROOT, "linear", "linear-deploy-state.json")
state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else None
if state:
    broken = []
    for k in state["issues"]:
        if k not in keymap:
            broken.append(f"{k} ({state['issues'][k]['identifier']}): usunięte z planu")
        elif keymap[k] != k:
            broken.append(f"{k} ({state['issues'][k]['identifier']}): nowy klucz {keymap[k]}")
    for k in state["milestones"]:
        if k not in msmap:
            broken.append(f"kamień {k}: usunięty z planu")
        elif msmap[k] != k:
            broken.append(f"kamień {k}: nowy klucz {msmap[k]}")
    if broken and not args.allow_renumber:
        print("Edycja zmienia klucze lub usuwa obiekty już wdrożone do Linear; nic nie zostało zapisane:")
        for b in broken[:40]:
            print("  " + b)
        if len(broken) > 40:
            print(f"  … i {len(broken) - 40} więcej")
        print("Dodawaj nowe materiały na końcu etapu (after=…), a nowe etapy na końcu projektu albo jako ścieżkę uzupełniającą.")
        sys.exit(2)
with open(PLAN, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(out, ensure_ascii=False, indent=1))
meta["partialReasons"] = reasons
with open(META, "w", encoding="utf-8") as fh:
    json.dump(meta, fh, ensure_ascii=False, indent=1)
if renamed:
    print(f"Zmienione klucze zadań ({len(renamed)}):")
    for old, new in renamed.items():
        print(f"  {old} → {new}")
subprocess.run([sys.executable, os.path.join(HERE, "render.py"), ROOT, ROOT, META], check=True)

# --- foldery robocze: utworzenie brakujących, usunięcie pustych, których nie ma w planie
expected = set()
for p in out["projects"]:
    expected.add(meta["projects"][p["key"]]["file"][:-3])
for i in out["issues"]:
    m = re.search(r"\*\*Folder roboczy:\*\* `(.*?)`", i["description"])
    expected.add(m.group(1).rstrip("/"))
existing = set()
for p in out["projects"]:
    pf = meta["projects"][p["key"]]["file"][:-3]
    full = os.path.join(ROOT, pf)
    if os.path.isdir(full):
        existing.update(f"{pf}/{d}" for d in os.listdir(full) if os.path.isdir(os.path.join(full, d)))
for d in sorted(existing - expected):
    full = os.path.join(ROOT, d)
    content = os.listdir(full)
    if content in ([], [".gitkeep"]):
        for c in content:
            os.remove(os.path.join(full, c))
        os.rmdir(full)
        print("usunięto pusty folder:", d)
    else:
        print("UWAGA: folder z treścią nie pasuje do planu (przenieś treść ręcznie):", d)
for d in sorted(expected):
    full = os.path.join(ROOT, d)
    if not os.path.isdir(full):
        os.makedirs(full)
        if "/" in d:
            open(os.path.join(full, ".gitkeep"), "w").close()
        print("utworzono folder:", d)

# --- co zmienić w Linear
if state:
    old_i = {i["key"]: i for i in plan["issues"]}
    new_i = {i["key"]: i for i in out["issues"]}
    old_m = {m["key"]: m for p in plan["projects"] for m in p["milestones"]}
    new_m = {m["key"]: m for p in out["projects"] for m in p["milestones"]}
    old_p = {p["key"]: p for p in plan["projects"]}
    upd, rel_add, rel_del = [], [], []
    for k, i in new_i.items():
        if k not in state["issues"]:
            continue
        o = old_i.get(k)
        diff = [f for f in ("title", "description", "labels", "status", "milestone") if o and o[f] != i[f]]
        if diff:
            upd.append(f"{state['issues'][k]['identifier']} ({k}): {', '.join(diff)}")
        for b in set(i["blockedBy"]) - set(o["blockedBy"] if o else []):
            rel_add.append(f"{b} → {k}")
        for b in set(o["blockedBy"] if o else []) - set(i["blockedBy"]):
            rel_del.append(f"{b} → {k}")
    for k, m in new_m.items():
        if k in state["milestones"] and k in old_m and (old_m[k]["name"], old_m[k]["description"]) != (m["name"], m["description"]):
            upd.append(f"kamień {k}: nazwa lub opis")
    for p in out["projects"]:
        o = old_p.get(p["key"])
        if p["key"] in state["projects"] and o and any(o[f] != p[f] for f in ("name", "summary", "description", "label")):
            upd.append(f"projekt {p['key']}: nazwa, podsumowanie, opis lub etykieta")
    new_items = [k for k in new_i if k not in state["issues"]] + [k for k in new_m if k not in state["milestones"]]
    if upd or rel_add or rel_del or new_items:
        print("\nDo przeniesienia do Linear (plik stanu tego nie zrobi sam):")
        for u in upd:
            print("  zaktualizować " + u)
        for x in rel_del:
            print("  usunąć relację " + x)
        if new_items or rel_add:
            print(f"  utworzyć {len(new_items)} nowych obiektów i {len(rel_add)} relacji w istniejących zadaniach: "
                  "deploy_linear.py utworzy brakujące obiekty i relacje")
    else:
        print("Plan w Linear nie wymaga zmian.")

sys.stdout.flush()
r = subprocess.run([sys.executable, os.path.join(HERE, "validate.py"), ROOT])
sys.exit(r.returncode)
