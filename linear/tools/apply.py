#!/usr/bin/env python3
"""Stosuje skrypty edycji do planu i odświeża wszystko, co z niego wynika.

Użycie:
    python3 linear/tools/apply.py                 # bez edycji: przegenerowanie Markdown, foldery, walidacja
    python3 linear/tools/apply.py moja_edycja.py  # edycja (funkcja apply(pl)), potem jak wyżej
    python3 linear/tools/apply.py --root KATALOG edycja.py   # na kopii repozytorium (do prób)

Kroki: wczytanie linear/linear-plan.json i tools/meta.json do modelu (model.Plan), wywołanie apply(pl)
z każdego podanego pliku, zapis JSON z nową numeracją kluczy, aktualizacja powodów relacji w meta.json,
generowanie plików Markdown (render.py), synchronizacja folderów roboczych i walidacja (validate.py).
"""
import argparse, importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from model import Plan  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("edits", nargs="*", help="pliki Pythona z funkcją apply(pl)")
ap.add_argument("--root", default=os.path.dirname(os.path.dirname(HERE)), help="katalog repozytorium")
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

r = subprocess.run([sys.executable, os.path.join(HERE, "validate.py"), ROOT])
sys.exit(r.returncode)
