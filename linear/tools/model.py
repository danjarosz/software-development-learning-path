"""Model planu na poziomie etapów: wczytanie z linear-plan.json, edycje i zapis z nową numeracją kluczy.

Odwołania (ref) do blokad używają kluczy w postaci zadania:
  'S05-START'      zadanie startowe projektu S05,
  'S12-E2-D'       dowód etapu o identyfikatorze 'S12-E2'.
Identyfikatory etapów i zadań to klucze z JSON w chwili wczytania (stałe przez całą edycję, nawet gdy etapy
zmieniają kolejność) albo identyfikatory nadane przy dodawaniu (np. etap 'S05-NEST', materiał 'S05-NEST-M1').
Nowe klucze powstają dopiero w emit(), według kolejności etapów i zadań.
"""
import copy, json, re, unicodedata

MAT_DONE = "Gotowe, gdy materiał jest przerobiony w zakresie potrzebnym do dowodu etapu."
OPT_NOTE = "Materiał opcjonalny: nie blokuje dowodu etapu."
FREE_BLOCKERS = ("zużycie API płatne", "chmura płatna", "abonament", "0 zł / płatn")


def is_paid(cost):
    c = cost.strip()
    if not c.startswith("0 zł"):
        return True
    return any(s in c for s in FREE_BLOCKERS)


def slugify(s):
    s = s.lower().replace("ł", "l")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def balanced_trunc(text, limit=110):
    if len(text) <= limit:
        return text
    cut = text[:limit - 1]
    cut = cut[:cut.rfind(" ")] if " " in cut else cut
    cut = cut.rstrip(",;:·–- ")
    # domknięcie lub odcięcie niezamkniętego cudzysłowu „…”
    if cut.count("„") > cut.count("”"):
        cut = cut[:cut.rfind("„")].rstrip(",;:·–- ")
    if cut.count("(") > cut.count(")"):
        cut = cut[:cut.rfind("(")].rstrip(",;:·–- ")
    if cut.count("`") % 2:
        cut = cut[:cut.rfind("`")].rstrip(",;:·–- ")
    return cut + "…"


class Item:
    def __init__(self, id, kind, title, description, labels):
        self.id, self.kind, self.title, self.description, self.labels = id, kind, title, description, list(labels)

    @property
    def optional(self):
        return "opcjonalne" in self.labels

    def field(self, name):
        m = re.search(r"\*\*" + re.escape(name) + r":\*\* (.*?)(?:  \n|\n|$)", self.description)
        return m.group(1).strip() if m else None

    def set_field(self, name, value):
        new, n = re.subn(r"(\*\*" + re.escape(name) + r":\*\* )(.*?)(  \n|\n|$)",
                         lambda m: m.group(1) + value + m.group(3), self.description, count=1)
        assert n == 1, (self.id, name)
        self.description = new
        if name == "Materiał":
            self.title = balanced_trunc("Przerobić: " + value)


class Stage:
    def __init__(self, id, kind, prefix, rest, description, optional):
        self.id, self.kind, self.prefix, self.rest = id, kind, prefix, rest
        self.description = description
        self.optional = optional
        self.entry = []          # lista ref
        self.reasons = {}        # ref -> powód (dla ref spoza projektu)
        self.items = []          # M..., P..., D (D zawsze ostatni)

    @property
    def proof(self):
        return self.items[-1]

    @property
    def expert(self):
        return self.proof.title.startswith("Dowód poziomu E")


class Project:
    def __init__(self, d):
        self.key = d["key"]
        self.name, self.summary, self.description = d["name"], d["summary"], d["description"]
        self.label = d["label"]
        self.blockedBy = list(d["blockedBy"])
        self.stages = []
        self.start = None        # dict(title, description, status, blockers=[ref], reasons={ref: str})
        self.base = 0


class Plan:
    def __init__(self, plan, meta):
        self.team = plan["team"]
        self.meta = meta
        self.projects = []
        self.P = {}
        self.S = {}
        self.ITEM = {}
        issues = plan["issues"]
        for d in plan["projects"]:
            p = Project(d)
            self.projects.append(p)
            self.P[p.key] = p
            for m in d["milestones"]:
                sk = m["key"].split("-")[1]
                kind = sk[0]
                if kind == "E":
                    rest = re.sub(r"^Etap \d+: ", "", m["name"])
                    prefix = None
                else:
                    mm = re.match(r"Uzupełniająca ([\d.]+) · (.*)", m["name"])
                    prefix, rest = mm.group(1), mm.group(2)
                st = Stage(m["key"], kind, prefix, rest, m["description"], "(opcjonalnie)" in m["name"])
                p.stages.append(st)
                self.S[st.id] = st
            es = [s for s in p.stages if s.kind == "E"]
            p.base = int(es[0].id.split("-")[1][1:])
        for i in issues:
            parts = i["key"].split("-")
            if parts[1] == "START":
                p = self.P[i["project"]]
                reasons = {}
                for b in i["blockedBy"]:
                    mm = re.search(r"- `" + re.escape(b) + r"` · .*? — (.*)", i["description"])
                    reasons[b] = mm.group(1)
                p.start = dict(title=i["title"], description=i["description"], status=i["status"],
                               blockers=list(i["blockedBy"]), reasons=reasons)
                continue
            st = self.S[i["milestone"]]
            it = Item(i["key"], parts[2][0], i["title"], i["description"], i["labels"])
            st.items.append(it)
            self.ITEM[it.id] = it
            if it.kind != "D" and not st.entry:
                st.entry = list(i["blockedBy"])
        for p in self.projects:
            for st in p.stages:
                for r in st.entry:
                    if r[:3] != p.key:
                        st.reasons[r] = meta["partialReasons"].get(f"{r}>{st.id}", "")
                st.items.sort(key=lambda it: (it.kind == "D", it.kind == "P"))

    # ---------- wyszukiwanie
    def project(self, pk):
        return self.P[pk]

    def stage(self, sid):
        return self.S[sid]

    def item(self, iid):
        return self.ITEM[iid]

    def stage_of_item(self, iid):
        for st in self.S.values():
            for it in st.items:
                if it.id == iid:
                    return st
        raise KeyError(iid)

    def project_of_stage(self, sid):
        return self.P[sid[:3]] if sid[:3] in self.P and self.S[sid] in self.P[sid[:3]].stages else \
            next(p for p in self.projects if self.S[sid] in p.stages)

    # ---------- etapy
    def add_stage(self, pk, sid, rest, cel, poziom, szczegolnie, dowod, attention=None, after=None, before=None,
                  entry=None, kind="E", prefix=None, optional=False, proof_title=None, criterion=None):
        p = self.P[pk]
        assert sid not in self.S, sid
        desc = f"**Cel:** {cel} · **Poziom po etapie:** {poziom}\n\n"
        if szczegolnie:
            desc += f"**Szczególnie ważne:** {szczegolnie}\n\n"
        desc += f"**Dowód:** {dowod}"
        st = Stage(sid, kind, prefix, rest, desc, optional)
        st.entry = list(entry or [])
        title = proof_title or ("Dowód etapu 0: " + rest if kind == "E" else f"Dowód ({prefix}): {rest}")
        pd = dowod + "\n\n"
        pd += f"**Na co zwrócić uwagę:** {attention or szczegolnie}\n\n"
        pd += "**Kryterium ukończenia:** " + (criterion or "dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.")
        pd += "\n\n**Folder roboczy:** `x`"
        labels = ["dowód"] + (["opcjonalne"] if optional else []) + (["ścieżka uzupełniająca"] if kind == "U" else [])
        proof = Item(sid + "-D", "D", title, pd, labels)
        st.items.append(proof)
        self.ITEM[proof.id] = proof
        self.S[sid] = st
        self._place(p.stages, st, after, before)
        return st

    def _place(self, lst, obj, after=None, before=None):
        if obj in lst:
            lst.remove(obj)
        if after:
            idx = [getattr(x, "id", None) for x in lst].index(after) + 1
        elif before:
            idx = [getattr(x, "id", None) for x in lst].index(before)
        else:
            idx = len(lst)
        lst.insert(idx, obj)

    def move_stage(self, sid, after=None, before=None, to_project=None):
        st = self.S[sid]
        src = self.project_of_stage(sid)
        dst = self.P[to_project] if to_project else src
        src.stages.remove(st)
        if after is None and before is None:
            dst.stages.append(st)
        else:
            self._place(dst.stages, st, after, before)
        return st

    def remove_stage(self, sid):
        st = self.S[sid]
        self.project_of_stage(sid).stages.remove(st)
        del self.S[sid]
        for it in st.items:
            self.ITEM.pop(it.id, None)
        ref = sid + "-D"
        for s in self.S.values():
            assert ref not in s.entry, f"{ref} nadal blokuje {s.id}"
        for p in self.projects:
            assert ref not in p.start["blockers"], f"{ref} nadal blokuje start {p.key}"

    def rename_stage_id(self, old, new):
        """Zmienia wewnętrzny identyfikator etapu (np. po przeniesieniu do innego projektu)."""
        st = self.S.pop(old)
        st.id = new
        self.S[new] = st
        self.replace_entry(old + "-D", new + "-D")
        return st

    def set_entry(self, sid, refs, reasons=None):
        st = self.S[sid]
        st.entry = list(refs)
        for r, why in (reasons or {}).items():
            st.reasons[r] = why

    def add_entry(self, sid, ref, reason=None):
        st = self.S[sid]
        if ref not in st.entry:
            st.entry.append(ref)
        if reason:
            st.reasons[ref] = reason

    def replace_entry_in(self, sid, old, new, reason=None):
        st = self.S[sid]
        st.entry[st.entry.index(old)] = new
        st.reasons.pop(old, None)
        if reason:
            st.reasons[new] = reason

    def remove_entry(self, sid, ref):
        st = self.S[sid]
        st.entry.remove(ref)
        st.reasons.pop(ref, None)

    def replace_entry(self, old, new, reason=None):
        """Zamienia ref we wszystkich wejściach etapów i startach."""
        for st in self.S.values():
            if old in st.entry:
                st.entry[st.entry.index(old)] = new
                if old in st.reasons:
                    st.reasons[new] = reason or st.reasons.pop(old)
        for p in self.projects:
            if old in p.start["blockers"]:
                p.start["blockers"][p.start["blockers"].index(old)] = new
                p.start["reasons"][new] = reason or p.start["reasons"].pop(old)
            if old in p.start["reasons"] and old not in p.start["blockers"]:
                p.start["reasons"].pop(old)

    def set_start_blockers(self, pk, pairs):
        p = self.P[pk]
        p.start["blockers"] = [r for r, _ in pairs]
        p.start["reasons"] = {r: why for r, why in pairs}

    def add_start_blocker(self, pk, ref, reason):
        p = self.P[pk]
        if ref not in p.start["blockers"]:
            p.start["blockers"].append(ref)
        p.start["reasons"][ref] = reason

    def remove_start_blocker(self, pk, ref):
        p = self.P[pk]
        p.start["blockers"].remove(ref)
        p.start["reasons"].pop(ref)

    # ---------- dowód etapu
    def set_proof(self, sid, text, attention=None, criterion=None):
        """Ustawia treść dowodu w opisie kamienia milowego i w zadaniu dowodu."""
        st = self.S[sid]
        label = "**Dowód poziomu E:** " if st.expert else "**Dowód:** "
        new, n = re.subn(r"\*\*Dowód(?: poziomu E)?:\*\* .*?(?=\n\n|$)", lambda m: label + text, st.description, flags=re.S)
        assert n == 1, sid
        st.description = new
        pr = st.proof
        parts = pr.description.split("\n\n")
        parts[0] = text
        if attention is not None:
            idx = next(i for i, x in enumerate(parts) if x.startswith("**Na co zwrócić uwagę:**"))
            parts[idx] = "**Na co zwrócić uwagę:** " + attention
        if criterion is not None:
            idx = next(i for i, x in enumerate(parts) if x.startswith("**Kryterium ukończenia:**"))
            parts[idx] = "**Kryterium ukończenia:** " + criterion
        pr.description = "\n\n".join(parts)

    def set_attention(self, sid, text):
        """Ustawia „Szczególnie ważne” w kamieniu i „Na co zwrócić uwagę” w dowodzie."""
        st = self.S[sid]
        if "**Szczególnie ważne:**" in st.description:
            st.description = re.sub(r"\*\*Szczególnie ważne:\*\* .*?(?=\n\n|$)", lambda m: "**Szczególnie ważne:** " + text,
                                    st.description, count=1, flags=re.S)
        else:
            st.description = st.description.replace("\n\n**Dowód", f"\n\n**Szczególnie ważne:** {text}\n\n**Dowód", 1)
        self.set_proof(sid, st.proof.description.split("\n\n")[0], attention=text)

    def set_stage_field(self, sid, name, value):
        st = self.S[sid]
        new, n = re.subn(r"(\*\*" + re.escape(name) + r":\*\* )(.*?)( · \*\*|\n|$)", lambda m: m.group(1) + value + m.group(3),
                         st.description, count=1)
        assert n == 1, (sid, name)
        st.description = new

    def rename_stage(self, sid, rest, cel=None):
        st = self.S[sid]
        old = st.rest
        st.rest = rest
        pr = st.proof
        if pr.title.endswith(": " + old):
            pr.title = pr.title[: -len(old)] + rest
        if cel:
            self.set_stage_field(sid, "Cel", cel)

    # ---------- zadania
    def add_material(self, sid, name, author, typ, czas, koszt, link, optional=False, note=None, iid=None, after=None, before=None):
        st = self.S[sid]
        iid = iid or f"{sid}-NEW{len(self.ITEM)}"
        assert iid not in self.ITEM, iid
        desc = (f"**Materiał:** {name}  \n**Autor / wydawca:** {author}  \n**Typ:** {typ}  \n**Czas:** {czas}  \n"
                f"**Koszt:** {koszt}  \n**Link:** {link}\n\nCzęść kamienia milowego „x”. {MAT_DONE}\n\n**Folder roboczy:** `x`")
        it = Item(iid, "M", balanced_trunc("Przerobić: " + name), desc, ["materiał"])
        if optional:
            self.set_optional(it, note)
        ms = [x for x in st.items if x.kind == "M"]
        if after or before:
            self._place(st.items, it, after, before)
        else:
            st.items.insert(len(ms), it)
        self.ITEM[iid] = it
        return it

    def add_practice(self, sid, title, text, iid=None):
        st = self.S[sid]
        iid = iid or f"{sid}-NEWP{len(self.ITEM)}"
        desc = (text + "\n\nPraktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, "
                "a nie po jednorazowym wykonaniu.\n\n**Folder roboczy:** `x`")
        it = Item(iid, "P", "Praktyka: " + title, desc, ["praktyka"])
        st.items.insert(len(st.items) - 1, it)
        self.ITEM[iid] = it
        return it

    def set_optional(self, item, note=None):
        it = self.ITEM[item] if isinstance(item, str) else item
        assert it.kind == "M"
        if "opcjonalne" not in it.labels:
            it.labels.append("opcjonalne")
        sentence = OPT_NOTE + (" " + note if note else "")
        if MAT_DONE in it.description:
            it.description = it.description.replace(MAT_DONE, sentence)
        elif OPT_NOTE not in it.description:
            it.description = it.description.replace("\n\n**Folder roboczy:**", f" {sentence}\n\n**Folder roboczy:**")
        return it

    def remove_item(self, iid):
        st = self.stage_of_item(iid)
        st.items = [x for x in st.items if x.id != iid]
        del self.ITEM[iid]

    def move_item(self, iid, to_sid, after=None, before=None):
        it = self.ITEM[iid]
        st = self.stage_of_item(iid)
        st.items.remove(it)
        dst = self.S[to_sid]
        if after or before:
            self._place(dst.items, it, after, before)
        else:
            dst.items.insert(len([x for x in dst.items if x.kind == "M"]), it)
        return it

    def replace_in(self, target, old, new, count=1):
        """Zamiana tekstu w opisie: target = id projektu ('S05'), etapu ('S05-E2'), zadania lub 'S05-START'."""
        if target.endswith("-START"):
            obj, attr = self.P[target[:3]].start, None
            assert old in obj["description"], (target, old)
            obj["description"] = obj["description"].replace(old, new, count)
            return
        if target in self.P:
            obj = self.P[target]
            if old in obj.description:
                obj.description = obj.description.replace(old, new, count)
                if old in obj.summary:
                    obj.summary = obj.summary.replace(old, new, count)
                return
            assert old in obj.summary, (target, old)
            obj.summary = obj.summary.replace(old, new, count)
            return
        obj = self.S.get(target) or self.ITEM[target]
        assert old in obj.description, (target, old)
        obj.description = obj.description.replace(old, new, count)

    # ---------- zapis
    def emit(self):
        """Nadaje nowe klucze i zwraca (plan_json, mapowanie id->klucz, nowe partialReasons)."""
        keymap = {}
        msmap = {}
        for p in self.projects:
            keymap[p.key + "-START"] = p.key + "-START"
            e = p.base
            u = 1
            for st in p.stages:
                if st.kind == "E":
                    sk = f"{p.key}-E{e}"
                    st._num = e
                    e += 1
                else:
                    sk = f"{p.key}-U{u}"
                    st._num = u
                    u += 1
                msmap[st.id] = sk
                nm = np = 0
                for it in st.items:
                    if it.kind == "M":
                        nm += 1
                        keymap[it.id] = f"{sk}-M{nm}"
                    elif it.kind == "P":
                        np += 1
                        keymap[it.id] = f"{sk}-P{np}"
                    else:
                        keymap[it.id] = f"{sk}-D"

        def R(ref):
            if ref.endswith("-START"):
                return ref
            assert ref.endswith("-D"), ref
            sid = ref[:-2]
            assert sid in msmap, f"nieznany etap w odwołaniu {ref}"
            return msmap[sid] + "-D"

        projects, issues, reasons = [], [], {}
        for p in self.projects:
            folder = self.meta["projects"][p.key]["file"][:-3]
            n_e = sum(1 for s in p.stages if s.kind == "E")
            desc = re.sub(r"Ścieżka ma \d+ etap(?:y|ów)", f"Ścieżka ma {n_e} " + ("etapy" if n_e in (2, 3, 4) else "etapów"), p.description, count=1)
            pj = dict(key=p.key, name=p.name, summary=p.summary, description=desc, label=p.label,
                      blockedBy=list(p.blockedBy), milestones=[])
            projects.append(pj)
            start_key = p.key + "-START"
            def fix_reason(r, why):
                k = R(r)
                if k.endswith("-START"):
                    return why
                part = k.split("-")[1]
                if part[0] == "E":
                    return re.sub(r"\(etap \d+\)$", f"(etap {part[1:]})", why)
                return re.sub(r"etap \d+\)$", f"etap {part[1:]})", why)
            lines = [f"- `{R(r)}` · {{TITLE:{R(r)}}} — {fix_reason(r, p.start['reasons'][r])}" for r in p.start["blockers"]]
            sd = p.start["description"]
            sd = re.sub(r"(\*\*Warunki wejścia \(zadania blokujące\):\*\*\n\n)(?:- .*\n)+", lambda m: m.group(1) + "\n".join(lines) + "\n", sd)
            sd = re.sub(r"\*\*Folder roboczy:\*\* `.*?`", f"**Folder roboczy:** `{folder}/`", sd)
            issues.append(dict(key=start_key, project=p.key, milestone=None, title=p.start["title"], description=sd,
                               labels=["start"], status=p.start["status"], blockedBy=[R(r) for r in p.start["blockers"]]))
            for r in p.start["blockers"]:
                pass
            for st in p.stages:
                mk = msmap[st.id]
                if st.kind == "E":
                    name = f"Etap {st._num}: {st.rest}"
                else:
                    name = f"Uzupełniająca {st.prefix} · {st.rest}"
                pj["milestones"].append(dict(key=mk, name=name, description=st.description))
                slug = mk.split("-")[1].lower() + "-" + slugify(st.rest)
                mfolder = f"{folder}/{slug}/"
                entry = [R(r) for r in st.entry]
                for r in st.entry:
                    if r[:3] != p.key and not r.endswith("-START"):
                        reasons[f"{R(r)}>{mk}"] = st.reasons.get(r, "")
                blocking = []
                for it in st.items:
                    k = keymap[it.id]
                    d = re.sub(r"\*\*Folder roboczy:\*\* `.*?`", f"**Folder roboczy:** `{mfolder}`", it.description)
                    d = re.sub(r"Część kamienia milowego „.*?”\.", f"Część kamienia milowego „{name}”.", d)
                    title = it.title
                    if it.kind == "D":
                        title = re.sub(r"^Dowód etapu \d+:", f"Dowód etapu {st._num}:", title)
                    labels = [l for l in it.labels]
                    if it.kind == "M":
                        cost = it.field("Koszt") or ""
                        paid = is_paid(cost)
                        labels = [l for l in labels if l != "płatny"]
                        if paid:
                            labels.insert(1, "płatny")
                    if st.optional and "opcjonalne" not in labels:
                        labels.append("opcjonalne")
                    if st.kind == "U" and "ścieżka uzupełniająca" not in labels:
                        labels.append("ścieżka uzupełniająca")
                    order = ["start", "materiał", "dowód", "praktyka", "płatny", "ścieżka uzupełniająca", "opcjonalne"]
                    labels = sorted(set(labels), key=order.index)
                    if it.kind == "D":
                        bb = blocking or entry
                    else:
                        bb = entry
                        if not (it.kind == "M" and "opcjonalne" in it.labels and not st.optional):
                            blocking.append(k)
                    issues.append(dict(key=k, project=p.key, milestone=mk, title=title, description=d,
                                       labels=labels, status="Backlog", blockedBy=list(bb)))
        byk = {i["key"]: i for i in issues}
        for i in issues:
            if i["key"].endswith("-START"):
                i["description"] = re.sub(r"\{TITLE:(.*?)\}", lambda m: byk[m.group(1)]["title"], i["description"])
        for i in issues:
            i["status"] = "Todo" if i["key"] in ("S01-START", "S02-START") else "Backlog"
        return dict(team=self.team, projects=projects, issues=issues), keymap, msmap, reasons
