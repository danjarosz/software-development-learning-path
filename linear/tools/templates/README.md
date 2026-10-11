# Ścieżka nauki inżynierii oprogramowania

Plan nauki umiejętności technicznych potrzebnych do samodzielnego wytwarzania oprogramowania: od pracy z AI i podstawowych narzędzi, przez frontend, backend, testy, architekturę i bezpieczeństwo, po desktop, mobile, AI w produktach i systemy wbudowane. Plan jest rozpisany na projekty, kamienie milowe i zadania w Linear (team **LEA**), a to repozytorium jest jednocześnie miejscem pracy: każdy etap nauki ma tu własny folder na notatki, ćwiczenia i dowody.

**W liczbach:** {proj_txt} · {ms_txt} · {iss_txt} · {n_rel} relacji „blokuje / blokowane przez”.

## Spis treści

- [Jak zbudowany jest plan](#jak-zbudowany-jest-plan)
- [Struktura repozytorium](#struktura-repozytorium)
- [Projekty](#projekty)
- [Jak pracować z repozytorium](#jak-pracować-z-repozytorium)
- [Wdrożenie planu do Linear](#wdrożenie-planu-do-linear)
- [Zmiany w planie](#zmiany-w-planie)
- [Konwencje](#konwencje)

## Jak zbudowany jest plan

| Element planu nauki | Element w Linear | Liczba |
|---|---|---|
| sekcja planu (obszar umiejętności) | projekt | {n_proj} |
| etap ścieżki nauki (także ścieżki uzupełniające) | kamień milowy | {n_ms} |
| punkt startu sekcji | zadanie „Start: …” | {n_start} |
| materiał do przerobienia | zadanie typu „materiał” | {n_mat} |
| dowód etapu, czyli mały projekt potwierdzający umiejętność | zadanie typu „dowód”, zamyka kamień milowy | {n_proof} |
| praktyka ciągła z etapu eksperckiego | zadanie typu „praktyka” | {n_prac} |

Kolejność nauki wynika z relacji między zadaniami:

- Zadanie startowe projektu blokuje wszystkie zadania pierwszego etapu.
- W obrębie etapu materiały są równoległe i blokują dowód etapu, a dowód blokuje materiały kolejnego etapu. Materiały z etykietą `opcjonalne` (alternatywy i uzupełnienia) dowodu nie blokują.
- Zadanie startowe jest blokowane przez dowody tych etapów projektów wstępnych, po których umiejętność jest na poziomie roboczym. Nie trzeba kończyć całego projektu wstępnego, żeby zacząć następny.
- Na starcie dostępne są tylko `S01-START` i `S02-START`.

Pełny opis kolejności, warstw i zależności między projektami jest w [`linear/00-kolejnosc-i-zaleznosci.md`](linear/00-kolejnosc-i-zaleznosci.md).

## Struktura repozytorium

```text
.
├── 01-praca-z-ai-w-chmurze/          # folder roboczy projektu
│   ├── e0-jak-dzialaja-llm-i-agenci-kodujacy/
│   ├── e1-codzienna-praca-z-claude-code/
│   └── …                             # jeden folder na kamień milowy
├── …
├── 22-systemy-wbudowane/
├── linear/
│   ├── 00-kolejnosc-i-zaleznosci.md  # przegląd: kolejność projektów i relacje
│   ├── 01-…md … 22-…md               # opis jednego projektu każdy
│   ├── linear-plan.json              # plan w formie do wdrożenia (źródło prawdy)
│   ├── deploy_linear.py              # skrypt wdrażający plan do Linear
│   └── tools/                        # edycja planu, generowanie Markdown, walidacja, test wdrożenia
├── CLAUDE.md                         # wskazówki dla Claude Code
└── README.md
```

Foldery projektów w katalogu głównym mają nazwy plików sekcji z `linear/`. W każdym jest jeden folder na kamień milowy: `ek-…` dla etapu k ścieżki głównej i `uk-…` dla ścieżki uzupełniającej k. Puste foldery zawierają plik `.gitkeep`, żeby git je zachował.

## Projekty

Projekty są ułożone w warstwy: każdy opiera się wyłącznie na wcześniejszych, a projekty z tej samej warstwy można prowadzić równolegle.

| Projekt | Warstwa | Kamienie milowe | Zadania | Folder roboczy |
|---|---|---|---|---|
{project_rows}

## Jak pracować z repozytorium

1. Wybierz w Linear zadanie, które nie jest już niczym blokowane.
2. Opis zadania kończy się wierszem **Folder roboczy:** ze ścieżką folderu. Tam trafiają notatki z materiałów, ćwiczenia i kod dowodu etapu. Zadanie startowe pracuje w folderze projektu.
3. Po zamknięciu dowodu etapu dodaj w komentarzu do zadania link do repozytorium, raportu lub notatki. Zamknięty dowód odblokowuje kolejny etap.
4. Gdy dodajesz pierwszy plik do pustego folderu, plik `.gitkeep` można usunąć.

## Wdrożenie planu do Linear

Plan jest wdrożony w Linear (team LEA, zadania `LEA-1` do `LEA-1121`). Identyfikatory wszystkich obiektów są w `linear/linear-deploy-state.json`, a mapowanie kluczy na `LEA-…` w `linear/mapowanie-kluczy.csv`. Zasady wprowadzania zmian po wdrożeniu są w [`linear/tools/README.md`](linear/tools/README.md#po-wdrożeniu).

Skrypt wymaga tylko Pythona 3.9+ i biblioteki standardowej.

```bash
# podgląd: kontrola spójności planu, liczby obiektów i stan wznowienia, bez wywołań API
python3 linear/deploy_linear.py --dry-run

# wdrożenie
export LINEAR_API_KEY=lin_api_...
python3 linear/deploy_linear.py            # opcje: --team LEA, --plan, --pause 0.25
```

Przed pierwszym wywołaniem API skrypt sprawdza plan (istnienie blokad i kamieni milowych, etykiety, brak cykli) i przerywa przy błędzie. Potem tworzy kolejno stany teamu, etykiety, projekty z kamieniami milowymi, zadania i relacje „blocks”, a na końcu zapisuje mapowanie kluczy roboczych na identyfikatory `LEA-…` w `linear/mapowanie-kluczy.csv`. Postęp zapisuje po każdym obiekcie w `linear/linear-deploy-state.json`, więc przerwane wdrożenie można wznowić. Nie usuwaj tego pliku po częściowym wdrożeniu, bo kolejne uruchomienie utworzy duplikaty.

Uwagi:

- Plan ma {iss_txt}, a plan Free w Linear pozwala na 250, więc potrzebny jest plan płatny.
- Zależności między projektami nie są ustawione w Linear: kolejność wyznaczają numery projektów (widok projektów sortowany po nazwie), a dokładne warunki startu i etapów są w relacjach między zadaniami. Kolumna „Blokowany przez” w pliku przeglądowym ma charakter informacyjny.

## Zmiany w planie

Źródłem prawdy jest `linear/linear-plan.json`. Pliki Markdown w `linear/`, ten README i foldery robocze są z niego generowane, więc nie edytuje się ich ręcznie. Zmianę zapisuje się jako skrypt edycji i stosuje przez `python3 linear/tools/apply.py edycja.py`: skrypt zapisuje JSON (z przenumerowaniem kluczy), generuje Markdown, tworzy lub usuwa puste foldery etapów i uruchamia walidację. Opis API i przykład są w [`linear/tools/README.md`](linear/tools/README.md).

Po zmianie sprawdź:

- `python3 linear/tools/validate.py` nie zgłasza błędów (uruchamia się też na końcu `apply.py`),
- `python3 linear/tools/mock_deploy.py` kończy się wynikiem OK (wdrożenie na atrapie API Linear),
- `python3 linear/deploy_linear.py --dry-run` kończy się bez błędów i pokazuje oczekiwane liczby,
- bez blokad są tylko `S01-START` i `S02-START`, każdy dowód etapu (poza etapami eksperckimi i opcjonalnymi) coś blokuje, a materiały `opcjonalne` nie blokują dowodu.

Plan nie zawiera dat ani sumarycznych szacunków czasu; jedynym szacunkiem jest pole „Czas” przy każdym materiale.

## Konwencje

- Cała treść planu jest po polsku.
- Klucze robocze zadań: `S06-E2-M3` to projekt 06, etap 2, materiał 3. `U` zamiast `E` oznacza ścieżkę uzupełniającą, `D` dowód etapu, `P` praktykę, `START` zadanie startowe.
- Tytuły zadań: „Przerobić: …”, „Dowód etapu k: …”, „Dowód poziomu E: …”, „Praktyka: …”, „Start: …”.
- Nazwy folderów są bez polskich znaków, małymi literami, ze słowami rozdzielonymi myślnikiem.
