#!/usr/bin/env python3
"""Uruchamia deploy_linear.main() na atrapie API Linear i sprawdza, co zostałoby utworzone.

Użycie: python3 linear/tools/mock_deploy.py [katalog z deploy_linear.py i linear-plan.json] [--interrupt N]
Domyślny katalog to linear/. Nic nie jest wysyłane do Linear; pracuje na kopii w katalogu tymczasowym.
--interrupt N: przerywa po N wywołaniach mutacji, potem wznawia, żeby sprawdzić brak duplikatów.
"""
import importlib.util, itertools, json, os, re, shutil, sys, tempfile

args = [a for a in sys.argv[1:] if not a.startswith("--") and not a.isdigit()]
src_dir = os.path.abspath(args[0]) if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
interrupt = int(sys.argv[sys.argv.index("--interrupt") + 1]) if "--interrupt" in sys.argv else None
work = tempfile.mkdtemp(prefix="mockdeploy-")
shutil.copy(os.path.join(src_dir, "deploy_linear.py"), work)
shutil.copy(os.path.join(src_dir, "linear-plan.json"), work)
spec = importlib.util.spec_from_file_location("deploy_linear", os.path.join(work, "deploy_linear.py"))
dl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dl)
plan = json.load(open(os.path.join(work, "linear-plan.json"), encoding="utf-8"))

ids = itertools.count(1)
DB = {"labels": {}, "plabels": {}, "projects": {}, "milestones": {}, "issues": {}, "relations": []}
STATES = [{"id": "st-b", "name": "Backlog", "type": "backlog", "position": 0},
          {"id": "st-t", "name": "Todo", "type": "unstarted", "position": 1},
          {"id": "st-p", "name": "In Progress", "type": "started", "position": 2}]
calls = {"n": 0}


class Stop(Exception):
    pass


class FakeLinear:
    def __init__(self, key, pause):
        self.calls = 0

    def gql(self, query, variables=None):
        v = variables or {}
        self.calls += 1
        if "mutation" in query:
            calls["n"] += 1
            if interrupt and calls["n"] == interrupt:
                raise Stop()
        if "teams(filter" in query:
            return {"teams": {"nodes": [{"id": "team-1", "name": "Learning", "states": {"nodes": STATES}}]}}
        if "team(id:" in query:
            return {"team": {"labels": {"nodes": [{"id": i, "name": n} for n, i in DB["labels"].items()]}}}
        if "projectLabels(first" in query:
            return {"projectLabels": {"nodes": [{"id": i, "name": n} for n, i in DB["plabels"].items()]}}
        inp = v.get("input", {})
        if "issueLabelCreate" in query:
            assert inp["name"] not in DB["labels"], "duplikat etykiety"
            assert re.match(r"^#[0-9A-F]{6}$", inp["color"])
            DB["labels"][inp["name"]] = f"lab-{next(ids)}"
            return {"issueLabelCreate": {"issueLabel": {"id": DB["labels"][inp["name"]]}}}
        if "projectLabelCreate" in query:
            DB["plabels"][inp["name"]] = f"plab-{next(ids)}"
            return {"projectLabelCreate": {"projectLabel": {"id": DB["plabels"][inp["name"]]}}}
        if "projectCreate" in query:
            assert inp["teamIds"] == ["team-1"]
            assert len(inp["description"]) <= 255
            assert inp["name"] not in [p["name"] for p in DB["projects"].values()], "duplikat projektu"
            for k in ("startDate", "targetDate"):
                if k in inp:
                    assert re.match(r"^\d{4}-\d\d-\d\d$", inp[k]), inp[k]
            assert all(l in DB["plabels"].values() for l in inp["labelIds"])
            pid = f"proj-{next(ids)}"
            DB["projects"][pid] = inp
            return {"projectCreate": {"project": {"id": pid, "url": f"https://linear.app/x/project/{pid}"}}}
        if "projectMilestoneCreate" in query:
            assert inp["projectId"] in DB["projects"]
            assert inp["name"] and len(inp["name"]) <= 255
            mid = f"ms-{next(ids)}"
            DB["milestones"][mid] = inp
            return {"projectMilestoneCreate": {"projectMilestone": {"id": mid}}}
        if "issueCreate" in query:
            assert inp["teamId"] == "team-1" and inp["projectId"] in DB["projects"]
            assert inp["title"] and len(inp["title"]) <= 255, inp["title"]
            if "projectMilestoneId" in inp:
                assert DB["milestones"][inp["projectMilestoneId"]]["projectId"] == inp["projectId"], "kamień z innego projektu"
            assert all(l in DB["labels"].values() for l in inp["labelIds"])
            assert inp.get("stateId") in ("st-b", "st-t")
            iid = f"iss-{next(ids)}"
            DB["issues"][iid] = inp
            return {"issueCreate": {"issue": {"id": iid, "identifier": f"LEA-{len(DB['issues'])}"}}}
        if "issueRelationCreate" in query:
            a, b = inp["issueId"], inp["relatedIssueId"]
            assert a in DB["issues"] and b in DB["issues"] and a != b and inp["type"] == "blocks"
            assert (a, b) not in DB["relations"], "duplikat relacji"
            DB["relations"].append((a, b))
            return {"issueRelationCreate": {"success": True}}
        raise AssertionError("nieobsłużone zapytanie: " + query[:80])


dl.Linear = FakeLinear
dl.HERE = work
dl.STATE_PATH = os.path.join(work, "linear-deploy-state.json")
os.environ["LINEAR_API_KEY"] = "lin_api_fake"
sys.argv = ["deploy_linear.py", "--plan", os.path.join(work, "linear-plan.json"), "--pause", "0"]
import time
time.sleep = lambda s: None
import contextlib, io
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    try:
        dl.main()
    except Stop:
        print("(przerwano celowo, wznawiam)")
        dl.main()

# --- sprawdzenie wyniku względem planu
I = plan["issues"]
exp_rel = sum(len(i["blockedBy"]) for i in I)
state = json.load(open(dl.STATE_PATH, encoding="utf-8"))
err = []
if len(DB["projects"]) != len(plan["projects"]):
    err.append(f"projekty {len(DB['projects'])} ≠ {len(plan['projects'])}")
if len(DB["milestones"]) != sum(len(p["milestones"]) for p in plan["projects"]):
    err.append("liczba kamieni milowych się nie zgadza")
if len(DB["issues"]) != len(I):
    err.append(f"zadania {len(DB['issues'])} ≠ {len(I)}")
if len(DB["relations"]) != exp_rel:
    err.append(f"relacje {len(DB['relations'])} ≠ {exp_rel}")
inv = {v["id"]: k for k, v in state["issues"].items()}
want = {(b, i["key"]) for i in I for b in i["blockedBy"]}
got = {(inv[a], inv[b]) for a, b in DB["relations"]}
if want != got:
    err.append(f"relacje różnią się od planu: brak {len(want - got)}, nadmiar {len(got - want)}")
todo = sorted(inv[i] for i, d in DB["issues"].items() if d.get("stateId") == "st-t")
if todo != ["S01-START", "S02-START"]:
    err.append(f"Todo: {todo}")
csv = open(os.path.join(work, "mapowanie-kluczy.csv"), encoding="utf-8").read().splitlines()
if len(csv) != len(I) + 1:
    err.append("mapowanie-kluczy.csv ma złą liczbę wierszy")
out = buf.getvalue()
print("\n".join(out.splitlines()[:4]))
print("…")
print("\n".join(out.splitlines()[-3:]))
print(f"Atrapa API: {len(DB['projects'])} projektów, {len(DB['milestones'])} kamieni milowych, {len(DB['issues'])} zadań, "
      f"{len(DB['relations'])} relacji, {len(DB['labels'])} etykiet zadań, {len(DB['plabels'])} etykiet projektów, "
      f"{calls['n']} mutacji" + (f", wznowienie po {interrupt}. mutacji" if interrupt else ""))
print("WYNIK:", "OK" if not err else "BŁĘDY: " + "; ".join(err))
shutil.rmtree(work)
sys.exit(1 if err else 0)
