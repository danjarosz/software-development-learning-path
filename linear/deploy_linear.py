#!/usr/bin/env python3
"""Wdrożenie planu nauki do Linear (team LEA) na podstawie linear-plan.json.

Użycie:
    export LINEAR_API_KEY=lin_api_...      # klucz osobisty: Linear > Settings > Security & access > API keys
    python3 deploy_linear.py --dry-run      # tylko podsumowanie, bez zmian w Linear
    python3 deploy_linear.py                # wdrożenie

Skrypt jest wznawialny: identyfikatory utworzonych obiektów zapisuje w pliku
linear-deploy-state.json obok skryptu. Po przerwaniu (limit zapytań, błąd sieci)
uruchom go ponownie, a pominie to, co już powstało.

Wymaga tylko Pythona 3.9+ (bez dodatkowych pakietów).
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://api.linear.app/graphql"
HERE = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(HERE, "linear-deploy-state.json")
ISSUE_LABELS = {
    "start": "#5E6AD2",
    "materiał": "#26B5CE",
    "dowód": "#4CB782",
    "praktyka": "#F2994A",
    "płatny": "#EB5757",
    "opcjonalne": "#95A2B3",
    "ścieżka uzupełniająca": "#BB87FC",
}


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"labels": {}, "projectLabels": {}, "projects": {}, "milestones": {}, "issues": {}, "relations": []}


def save_state(state):
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STATE_PATH)


class Linear:
    def __init__(self, key, pause):
        self.key = key
        self.pause = pause
        self.calls = 0

    def gql(self, query, variables=None):
        body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        for attempt in range(8):
            req = urllib.request.Request(API, data=body, method="POST", headers={
                "Content-Type": "application/json",
                "Authorization": self.key,
            })
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                text = e.read().decode("utf-8", "replace")
                if e.code in (429, 502, 503, 504) or "RATELIMITED" in text:
                    wait = 60 * (attempt + 1)
                    print(f"  limit lub błąd serwera ({e.code}), czekam {wait} s…", flush=True)
                    time.sleep(wait)
                    continue
                raise SystemExit(f"Błąd HTTP {e.code}: {text}")
            except urllib.error.URLError as e:
                wait = 15 * (attempt + 1)
                print(f"  błąd sieci ({e.reason}), czekam {wait} s…", flush=True)
                time.sleep(wait)
                continue
            if data.get("errors"):
                msg = json.dumps(data["errors"], ensure_ascii=False)
                if "RATELIMITED" in msg or "ratelimit" in msg.lower():
                    wait = 60 * (attempt + 1)
                    print(f"  limit zapytań, czekam {wait} s…", flush=True)
                    time.sleep(wait)
                    continue
                raise SystemExit(f"Błąd GraphQL: {msg}")
            self.calls += 1
            time.sleep(self.pause)
            return data["data"]
        raise SystemExit("Zbyt wiele nieudanych prób. Uruchom skrypt ponownie później; postęp jest zapisany.")


def check_plan(plan):
    """Zwraca listę błędów, przez które wdrożenie zakończyłoby się w połowie albo utworzyło złe relacje."""
    problems = []
    projects = {p["key"]: p for p in plan["projects"]}
    milestones = {m["key"]: p["key"] for p in plan["projects"] for m in p["milestones"]}
    issues = {}
    for it in plan["issues"]:
        if it["key"] in issues:
            problems.append(f"zduplikowany klucz zadania {it['key']}")
        issues[it["key"]] = it
    if len(milestones) != sum(len(p["milestones"]) for p in plan["projects"]):
        problems.append("zduplikowane klucze kamieni milowych")
    for p in plan["projects"]:
        if not p.get("label"):
            problems.append(f"{p['key']}: brak etykiety projektu")
    for it in plan["issues"]:
        k = it["key"]
        if it["project"] not in projects:
            problems.append(f"{k}: nieznany projekt {it['project']}")
        if it.get("milestone") and milestones.get(it["milestone"]) != it["project"]:
            problems.append(f"{k}: kamień milowy {it['milestone']} nie należy do projektu {it['project']}")
        for l in it["labels"]:
            if l not in ISSUE_LABELS:
                problems.append(f"{k}: etykieta „{l}” spoza ISSUE_LABELS")
        if it["status"] not in ("Todo", "Backlog"):
            problems.append(f"{k}: nieznany status {it['status']}")
        for b in it["blockedBy"]:
            if b not in issues:
                problems.append(f"{k}: blokada {b} nie istnieje")
    # cykle (algorytm Kahna)
    indeg = {k: 0 for k in issues}
    out = {k: [] for k in issues}
    for it in plan["issues"]:
        for b in it["blockedBy"]:
            if b in issues:
                out[b].append(it["key"])
                indeg[it["key"]] += 1
    queue = [k for k, n in indeg.items() if n == 0]
    seen = 0
    while queue:
        k = queue.pop()
        seen += 1
        for t in out[k]:
            indeg[t] -= 1
            if indeg[t] == 0:
                queue.append(t)
    if seen != len(issues):
        problems.append(f"graf blokad ma cykl ({len(issues) - seen} zadań)")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", default=os.path.join(HERE, "linear-plan.json"))
    ap.add_argument("--team", default="LEA")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--pause", type=float, default=0.25, help="przerwa między zapytaniami w sekundach")
    args = ap.parse_args()

    with open(args.plan, encoding="utf-8") as f:
        plan = json.load(f)
    projects = plan["projects"]
    issues = plan["issues"]
    n_ms = sum(len(p["milestones"]) for p in projects)
    n_rel = sum(len(i["blockedBy"]) for i in issues)
    print(f"Plan: {len(projects)} projektów, {n_ms} kamieni milowych, {len(issues)} zadań, {n_rel} relacji „blocks”.")
    print("Uwaga: plan Free w Linear ma limit 250 zgłoszeń; ten plan wymaga planu płatnego.")
    problems = check_plan(plan)
    if problems:
        for msg in problems:
            print(f"  błąd planu: {msg}")
        raise SystemExit(f"Plan ma {len(problems)} błędów; popraw linear-plan.json przed wdrożeniem.")
    print("Kontrola planu: klucze, blokady, etykiety i kamienie milowe są spójne, graf nie ma cykli.")
    if args.dry_run:
        state = load_state()
        print(f"Stan wznowienia: {len(state['projects'])} projektów, {len(state['milestones'])} kamieni milowych, "
              f"{len(state['issues'])} zadań i {len(state['relations'])} relacji już utworzonych.")
        print("Tryb próbny: nic nie zostało zmienione.")
        return

    key = os.environ.get("LINEAR_API_KEY")
    if not key:
        raise SystemExit("Ustaw zmienną środowiskową LINEAR_API_KEY.")
    lin = Linear(key, args.pause)
    state = load_state()

    # --- team i statusy
    d = lin.gql("""query($key: String!) { teams(filter: { key: { eq: $key } }) {
        nodes { id name states { nodes { id name type position } } } } }""", {"key": args.team})
    nodes = d["teams"]["nodes"]
    if not nodes:
        raise SystemExit(f"Nie znaleziono teamu o kluczu {args.team}.")
    team = nodes[0]
    states = team["states"]["nodes"]
    def pick_state(name, typ):
        for s in states:
            if s["name"].lower() == name.lower():
                return s["id"]
        cands = sorted((s for s in states if s["type"] == typ), key=lambda s: s["position"])
        return cands[0]["id"] if cands else None
    state_ids = {"Todo": pick_state("Todo", "unstarted"), "Backlog": pick_state("Backlog", "backlog")}
    print(f"Team: {team['name']} ({team['id']})")

    # --- etykiety zadań (w teamie)
    d = lin.gql("""query($id: String!) { team(id: $id) { labels(first: 250) { nodes { id name } } } }""", {"id": team["id"]})
    existing = {n["name"]: n["id"] for n in d["team"]["labels"]["nodes"]}
    for name, color in ISSUE_LABELS.items():
        if name in state["labels"]:
            continue
        if name in existing:
            state["labels"][name] = existing[name]
        else:
            r = lin.gql("""mutation($input: IssueLabelCreateInput!) { issueLabelCreate(input: $input) { issueLabel { id } } }""",
                        {"input": {"name": name, "color": color, "teamId": team["id"]}})
            state["labels"][name] = r["issueLabelCreate"]["issueLabel"]["id"]
        save_state(state)
    print("Etykiety zadań gotowe.")

    # --- etykiety projektów (warstwy)
    d = lin.gql("""query { projectLabels(first: 250) { nodes { id name } } }""")
    existing = {n["name"]: n["id"] for n in d["projectLabels"]["nodes"]}
    for p in projects:
        name = p["label"]
        if name in state["projectLabels"]:
            continue
        if name in existing:
            state["projectLabels"][name] = existing[name]
        else:
            r = lin.gql("""mutation($input: ProjectLabelCreateInput!) { projectLabelCreate(input: $input) { projectLabel { id } } }""",
                        {"input": {"name": name}})
            state["projectLabels"][name] = r["projectLabelCreate"]["projectLabel"]["id"]
        save_state(state)
    print("Etykiety projektów gotowe.")

    # --- projekty i kamienie milowe
    for p in projects:
        if p["key"] not in state["projects"]:
            inp = {"name": p["name"], "teamIds": [team["id"]], "description": p["summary"][:255],
                   "content": p["description"], "labelIds": [state["projectLabels"][p["label"]]]}
            if p.get("start"):
                inp["startDate"] = p["start"]
            if p.get("target"):
                inp["targetDate"] = p["target"]
            r = lin.gql("""mutation($input: ProjectCreateInput!) { projectCreate(input: $input) { project { id url } } }""",
                        {"input": inp})
            state["projects"][p["key"]] = r["projectCreate"]["project"]["id"]
            save_state(state)
            print(f"Projekt: {p['name']}  {r['projectCreate']['project']['url']}")
        for i, m in enumerate(p["milestones"]):
            if m["key"] in state["milestones"]:
                continue
            r = lin.gql("""mutation($input: ProjectMilestoneCreateInput!) { projectMilestoneCreate(input: $input) { projectMilestone { id } } }""",
                        {"input": {"projectId": state["projects"][p["key"]], "name": m["name"],
                                   "description": m["description"], "sortOrder": float(i)}})
            state["milestones"][m["key"]] = r["projectMilestoneCreate"]["projectMilestone"]["id"]
            save_state(state)
    print("Projekty i kamienie milowe gotowe.")

    # --- zadania
    total = len(issues)
    for n, it in enumerate(issues, 1):
        if it["key"] in state["issues"]:
            continue
        inp = {"teamId": team["id"], "projectId": state["projects"][it["project"]],
               "title": it["title"], "description": it["description"],
               "labelIds": [state["labels"][l] for l in it["labels"]]}
        if it.get("milestone"):
            inp["projectMilestoneId"] = state["milestones"][it["milestone"]]
        sid = state_ids.get(it["status"])
        if sid:
            inp["stateId"] = sid
        r = lin.gql("""mutation($input: IssueCreateInput!) { issueCreate(input: $input) { issue { id identifier } } }""",
                    {"input": inp})
        iss = r["issueCreate"]["issue"]
        state["issues"][it["key"]] = {"id": iss["id"], "identifier": iss["identifier"]}
        save_state(state)
        if n % 25 == 0 or n == total:
            print(f"Zadania: {n}/{total}", flush=True)

    # --- relacje „blocks”
    done = {tuple(x) for x in state["relations"]}
    rels = [(b, it["key"]) for it in issues for b in it["blockedBy"]]
    for n, (blocker, blocked) in enumerate(rels, 1):
        if (blocker, blocked) in done:
            continue
        lin.gql("""mutation($input: IssueRelationCreateInput!) { issueRelationCreate(input: $input) { success } }""",
                {"input": {"issueId": state["issues"][blocker]["id"],
                           "relatedIssueId": state["issues"][blocked]["id"], "type": "blocks"}})
        state["relations"].append([blocker, blocked])
        done.add((blocker, blocked))
        save_state(state)
        if n % 50 == 0 or n == len(rels):
            print(f"Relacje: {n}/{len(rels)}", flush=True)

    # --- mapowanie kluczy na identyfikatory LEA
    mp = os.path.join(HERE, "mapowanie-kluczy.csv")
    with open(mp, "w", encoding="utf-8") as f:
        f.write("klucz,identyfikator\n")
        for it in issues:
            f.write(f"{it['key']},{state['issues'][it['key']]['identifier']}\n")
    print(f"Gotowe. Zapytań w tym uruchomieniu: {lin.calls}. Mapowanie kluczy: {mp}")
    print("Zależności między projektami nie są tworzone; kolejność wyznaczają numery projektów i relacje między zadaniami.")


if __name__ == "__main__":
    main()
