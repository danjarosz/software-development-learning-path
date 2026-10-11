# Ścieżka nauki inżynierii oprogramowania

Plan nauki umiejętności technicznych potrzebnych do samodzielnego wytwarzania oprogramowania: od pracy z AI i podstawowych narzędzi, przez frontend, backend, testy, architekturę i bezpieczeństwo, po desktop, mobile, AI w produktach i systemy wbudowane. Plan jest rozpisany na projekty, kamienie milowe i zadania w Linear (team **LEA**), a to repozytorium jest jednocześnie miejscem pracy: każdy etap nauki ma tu własny folder na notatki, ćwiczenia i dowody.

**W liczbach:** 22 projekty · 160 kamieni milowych · 1121 zadań · 2139 relacji „blokuje / blokowane przez”.

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
| sekcja planu (obszar umiejętności) | projekt | 22 |
| etap ścieżki nauki (także ścieżki uzupełniające) | kamień milowy | 160 |
| punkt startu sekcji | zadanie „Start: …” | 22 |
| materiał do przerobienia | zadanie typu „materiał” | 864 |
| dowód etapu, czyli mały projekt potwierdzający umiejętność | zadanie typu „dowód”, zamyka kamień milowy | 160 |
| praktyka ciągła z etapu eksperckiego | zadanie typu „praktyka” | 75 |

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
| [01. Praca z AI w chmurze: Claude i Claude Code](linear/01-praca-z-ai-w-chmurze.md) | 0: fundamenty | 7 | 50 | [`01-praca-z-ai-w-chmurze/`](01-praca-z-ai-w-chmurze/) |
| [02. Języki i narzędzia podstawowe](linear/02-jezyki-i-narzedzia-podstawowe.md) | 0: fundamenty | 5 | 42 | [`02-jezyki-i-narzedzia-podstawowe/`](02-jezyki-i-narzedzia-podstawowe/) |
| [03. Frontend web](linear/03-frontend-web.md) | 0: fundamenty | 8 | 53 | [`03-frontend-web/`](03-frontend-web/) |
| [04. Bazy danych i dane](linear/04-bazy-danych-i-dane.md) | 1: dane i serwer | 9 | 56 | [`04-bazy-danych-i-dane/`](04-bazy-danych-i-dane/) |
| [05. Backend i API](linear/05-backend-i-api.md) | 1: dane i serwer | 12 | 92 | [`05-backend-i-api/`](05-backend-i-api/) |
| [06. Testowanie](linear/06-testowanie.md) | 2: jakość i projektowanie | 8 | 50 | [`06-testowanie/`](06-testowanie/) |
| [07. Wymagania i specyfikacje](linear/07-wymagania-i-specyfikacje.md) | 2: jakość i projektowanie | 7 | 47 | [`07-wymagania-i-specyfikacje/`](07-wymagania-i-specyfikacje/) |
| [08. Architektura i projektowanie systemów](linear/08-architektura-i-projektowanie-systemow.md) | 2: jakość i projektowanie | 8 | 70 | [`08-architektura-i-projektowanie-systemow/`](08-architektura-i-projektowanie-systemow/) |
| [09. DevOps, CI/CD i wydania](linear/09-devops-ci-cd-i-wydania.md) | 2: jakość i projektowanie | 7 | 46 | [`09-devops-ci-cd-i-wydania/`](09-devops-ci-cd-i-wydania/) |
| [10. Bezpieczeństwo](linear/10-bezpieczenstwo.md) | 3: ochrona i kontrola | 9 | 57 | [`10-bezpieczenstwo/`](10-bezpieczenstwo/) |
| [11. Weryfikacja pracy AI i budowa procesu](linear/11-weryfikacja-pracy-ai-i-budowa-procesu.md) | 3: ochrona i kontrola | 6 | 40 | [`11-weryfikacja-pracy-ai-i-budowa-procesu/`](11-weryfikacja-pracy-ai-i-budowa-procesu/) |
| [12. Rust jako wspólny fundament](linear/12-rust-jako-wspolny-fundament.md) | 4: rdzeń kompilowany i produkt | 10 | 68 | [`12-rust-jako-wspolny-fundament/`](12-rust-jako-wspolny-fundament/) |
| [13. UI/UX](linear/13-ui-ux.md) | 4: rdzeń kompilowany i produkt | 9 | 61 | [`13-ui-ux/`](13-ui-ux/) |
| [14. Desktop: wspólne](linear/14-desktop.md) | 5: desktop | 6 | 39 | [`14-desktop/`](14-desktop/) |
| [15. Linux](linear/15-linux.md) | 5: desktop | 4 | 31 | [`15-linux/`](15-linux/) |
| [16. macOS](linear/16-macos.md) | 5: desktop | 4 | 33 | [`16-macos/`](16-macos/) |
| [17. Windows](linear/17-windows.md) | 5: desktop | 5 | 38 | [`17-windows/`](17-windows/) |
| [18. Android](linear/18-android.md) | 6: mobile | 7 | 58 | [`18-android/`](18-android/) |
| [19. iOS](linear/19-ios.md) | 6: mobile | 7 | 54 | [`19-ios/`](19-ios/) |
| [20. Lokalne AI i rozwój modeli](linear/20-lokalne-ai-i-rozwoj-modeli.md) | 7: AI w produktach | 6 | 40 | [`20-lokalne-ai-i-rozwoj-modeli/`](20-lokalne-ai-i-rozwoj-modeli/) |
| [21. Funkcje AI w aplikacjach](linear/21-funkcje-ai-w-aplikacjach.md) | 7: AI w produktach | 5 | 31 | [`21-funkcje-ai-w-aplikacjach/`](21-funkcje-ai-w-aplikacjach/) |
| [22. Systemy wbudowane](linear/22-systemy-wbudowane.md) | 8: sprzęt | 11 | 65 | [`22-systemy-wbudowane/`](22-systemy-wbudowane/) |

## Jak pracować z repozytorium

1. Wybierz w Linear zadanie, które nie jest już niczym blokowane.
2. Opis zadania kończy się wierszem **Folder roboczy:** ze ścieżką folderu. Tam trafiają notatki z materiałów, ćwiczenia i kod dowodu etapu. Zadanie startowe pracuje w folderze projektu.
3. Po zamknięciu dowodu etapu dodaj w komentarzu do zadania link do repozytorium, raportu lub notatki. Zamknięty dowód odblokowuje kolejny etap.
4. Gdy dodajesz pierwszy plik do pustego folderu, plik `.gitkeep` można usunąć.

## Wdrożenie planu do Linear

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

- Plan ma 1121 zadań, a plan Free w Linear pozwala na 250, więc potrzebny jest plan płatny.
- Skrypt nie tworzy zależności między projektami. Trzeba je dodać ręcznie według kolumny „Blokowany przez” w pliku przeglądowym.

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
