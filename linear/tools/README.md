# Narzędzia planu

Źródłem prawdy jest `linear/linear-plan.json`. Pliki Markdown (`linear/00-…md`, `linear/01-…md` do `linear/22-…md`, `README.md`) i foldery robocze są z niego generowane, więc nie edytuje się ich ręcznie. Wszystkie narzędzia wymagają tylko Pythona 3.9+ i biblioteki standardowej.

| Plik | Do czego |
|---|---|
| `apply.py` | stosuje skrypty edycji, zapisuje JSON, generuje Markdown, synchronizuje foldery i uruchamia walidację |
| `model.py` | model planu na poziomie etapów i API do edycji (zob. niżej) |
| `render.py` | generuje Markdown z JSON, `meta.json` i szablonów |
| `validate.py` | sprawdza graf zależności, reguły etapów, etykiety, foldery i brak szacunków czasu |
| `mock_deploy.py` | uruchamia `deploy_linear.py` na atrapie API Linear (także z przerwaniem i wznowieniem) i porównuje wynik z planem |
| `meta.json` | dane spoza JSON: pliki sekcji, nazwy warstw, powody relacji częściowych (aktualizowane przez `apply.py`) |
| `templates/` | szablony `00-kolejnosc-i-zaleznosci.md` i `README.md` (proza i miejsca na tabele i liczby) |

## Jak zmienić plan

1. Napisz skrypt edycji, np. `/tmp/edycja.py`, z funkcją `apply(pl)` (przykład niżej).
2. Wypróbuj go na kopii repozytorium: `python3 linear/tools/apply.py --root /tmp/kopia /tmp/edycja.py`.
3. Zastosuj w repozytorium: `python3 linear/tools/apply.py /tmp/edycja.py`. Skrypt wypisze zmienione klucze zadań.
4. Sprawdź wdrożenie: `python3 linear/tools/mock_deploy.py` (oraz `--interrupt 1500`) i `python3 linear/deploy_linear.py --dry-run`.

Samo `python3 linear/tools/apply.py` (bez edycji) przegenerowuje Markdown i foldery z bieżącego JSON; na niezmienionym planie nie zmienia żadnego pliku. Zmiana prozy w pliku 00 lub w README to edycja szablonu w `templates/` i to samo polecenie.

Klucze (`S05-E2-M3`) wynikają z kolejności etapów i zadań, więc dodanie lub przestawienie etapu przenumerowuje klucze. Po częściowym wdrożeniu do Linear nie zmieniaj kluczy (stan wznowienia `linear-deploy-state.json` opiera się na nich). Gdy folder etapu z treścią przestaje pasować do planu, `apply.py` go nie usuwa, tylko ostrzega: treść trzeba przenieść ręcznie.

Przykład:

```python
def apply(pl):
    # materiał opcjonalny w etapie NestJS (etap o kluczu S05-E2 w chwili wczytania)
    pl.add_material("S05-E2", "Dokumentacja NestJS: „Microservices”", "NestJS", "dokumentacja, średni",
                    "3–4 h", "0 zł", "https://docs.nestjs.com/microservices/basics",
                    optional=True, note="Przy integracji usług przez kolejki.")
    # nowa blokada z innego projektu, zawsze z powodem
    pl.add_entry("S14-E3", "S13-E4-D", reason="natywny UI korzysta z tokenów projektowych z sekcji 13")
```

## Identyfikatory i odwołania

- Etapy i zadania mają identyfikatory równe kluczom z JSON w chwili wczytania (np. etap `S05-E2`, materiał `S05-E2-M3`, praktyka `S05-E11-P1`). Pozostają stałe przez całą edycję, nawet gdy etapy zmieniają kolejność. Nowe etapy i zadania dostają identyfikatory nadane przy dodawaniu (np. etap `S05-NOWY`).
- Odwołania do blokad: `'S05-START'` (zadanie startowe) albo `'<id etapu>-D'` (dowód etapu).
- Etap ma listę wejściową `entry`: wszystkie jego materiały i praktyki są blokowane przez te odwołania. Dowód etapu jest automatycznie blokowany przez wszystkie nieopcjonalne materiały i praktyki etapu (etap bez nich: przez wejście).
- Nazwę kamienia milowego („Etap k: …”), numer w tytule dowodu, zdanie „Część kamienia milowego „…””, wiersz „**Folder roboczy:**”, numer etapu w powodach blokad startu i zdanie „Ścieżka ma N etapów” generator ustawia sam.
- Etykieta `płatny` wynika z pola „Koszt”: koszt zaczynający się od „0 zł” oznacza materiał bezpłatny (chyba że zawiera „zużycie API płatne”, „chmura płatna”, „abonament” albo „0 zł / płatn…”).
- Pole `blockedBy` projektu i jego podsumowanie nie są wyliczane: po zmianie blokad startu popraw je w skrypcie edycji (`pl.project(pk).blockedBy`, podsumowanie przez `replace_in`), walidator wskaże rozbieżność.

## API (`pl`)

Wyszukiwanie: `pl.project('S05')`, `pl.stage('S05-E2')`, `pl.item('S05-E2-M3')`.
Obiekt etapu: `.rest` (nazwa bez „Etap k: ”), `.description` (opis kamienia), `.entry`, `.items`, `.proof`, `.optional`.
Obiekt zadania: `.title`, `.description`, `.labels`, `.field('Czas')`, `.set_field('Czas', '10–12 h')`
(dla 'Materiał' ustawia też tytuł „Przerobić: …”).
Projekt: `.description`, `.summary`, `.stages` (lista etapów w kolejności).

Etapy:
- `pl.add_stage(pk, sid, rest, cel, poziom, szczegolnie, dowod, attention=None, after=None, before=None, entry=[...], optional=False, proof_title=None, criterion=None)`
  tworzy etap z dowodem. `cel` = krótki cel do tabeli („HTTP i REST: semantyka, kody”), `poziom` = „podstawy” / „W” / „E”,
  `szczegolnie` = treść „Szczególnie ważne”, `dowod` = treść dowodu (1–3 zdania, konkretny artefakt), `attention` = „Na co zwrócić uwagę”
  (domyślnie = `szczegolnie`), `criterion` = kryterium ukończenia (domyślnie ogólne). Dla etapu eksperckiego podaj
  `proof_title="Dowód poziomu E: ekspert"`.
- `pl.move_stage(sid, after=..., before=..., to_project=None)` — zmiana kolejności.
- `pl.remove_stage(sid)` — usuwa etap z zadaniami (najpierw usuń odwołania do jego dowodu).
- `pl.rename_stage(sid, rest, cel=None)` — nowa nazwa etapu (tytuł dowodu też się zmieni).
- `pl.set_stage_field(sid, 'Cel' | 'Poziom po etapie', value)`.
- `pl.set_proof(sid, text, attention=None, criterion=None)` — treść dowodu w opisie kamienia i w zadaniu dowodu.
- `pl.set_attention(sid, text)` — „Szczególnie ważne” w kamieniu i „Na co zwrócić uwagę” w dowodzie.
- `pl.set_entry(sid, refs, reasons={ref: powód})`, `pl.add_entry(sid, ref, reason=None)`, `pl.remove_entry(sid, ref)`.
  Dla odwołań do **innego projektu** zawsze podaj powód (krótko, np. „backend w Ruście wymaga Rusta na poziomie W”).
- `pl.add_start_blocker(pk, ref, reason)`, `pl.remove_start_blocker(pk, ref)` — warunki wejścia projektu.
- `pl.replace_entry_in(sid, old, new, reason=None)` — zamiana jednej blokady wejścia etapu; `pl.replace_entry(old, new, reason=None)` — zamiana odwołania we wszystkich etapach i startach.
- `pl.rename_stage_id(old, new)` — nowy identyfikator etapu (np. po przeniesieniu do innego projektu przez `move_stage(..., to_project=...)`).

Zadania:
- `pl.add_material(sid, name, author, typ, czas, koszt, link, optional=False, note=None, iid=None, after=None, before=None)`.
  `typ` np. „dokumentacja, średni”, „książka, zaawansowany”, „kurs wideo, podstawowy”; `czas` np. „8–10 h”; `koszt` „0 zł” / „płatna” / „abonament”;
  `link` pełny URL. `note` (dla opcjonalnych) = krótkie zdanie, kiedy go przerobić.
- `pl.set_optional(iid, note=None)` — materiał opcjonalny: etykieta `opcjonalne`, **nie blokuje dowodu**. Używaj dla materiałów
  opisanych jako alternatywne („wystarczy jeden z…”, „wg potrzeb”, „tylko od zera”), dublujących się albo nadmiarowych.
  Przy parze alternatyw jeden zostaje obowiązkowy, drugi opcjonalny.
- `pl.add_practice(sid, title, text)` — praktyka ciągła (tylko etap ekspercki).
- `pl.remove_item(iid)`, `pl.move_item(iid, to_sid, after=None, before=None)`.
- `pl.replace_in(target, old, new)` — zamiana fragmentu tekstu (asercja, że `old` istnieje). `target`: 'S05' (opis projektu i podsumowanie),
  'S05-E2' (opis kamienia), id zadania, 'S05-START' (opis startu). Używaj do poprawiania prozy (np. „Ścieżka ma… Etapy 0–1 można…”,
  zakres umiejętności). Zdanie „Ścieżka ma N etapów” generator poprawia sam.
- Tekst zadania możesz też ustawić wprost: `pl.item(x).description = ...` (zachowaj strukturę: dowód = treść, „**Na co zwrócić uwagę:** …”,
  „**Kryterium ukończenia:** …”, „**Folder roboczy:** `x`”; materiał = pola + zdanie + folder).

## Zasady treści

- Wszystko po polsku, styl istniejących plików: cudzysłowy „…”, kod w backtickach, separator `·`.
- Bez dat, harmonogramów i sumarycznych szacunków czasu. Jedyny czas to pole „Czas” pojedynczego materiału.
- Materiały istnieją naprawdę: nazwa, autor lub wydawca, działający link; wydanie lub wersja, gdy ma znaczenie.
- Dowód etapu jest mierzalny (konkretny artefakt i warunek zaliczenia), wykonalny samodzielnie i nie wymaga umiejętności spoza swoich (pośrednich) blokad.
- Materiały alternatywne, „wg potrzeb” i dublujące się są opcjonalne (`set_optional`), więc nie blokują dowodu.
