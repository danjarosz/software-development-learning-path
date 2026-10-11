# 13. UI/UX: plan wdrożenia w Linear

Team **LEA** (https://linear.app/daankh/team/LEA/overview). Plan do przeglądu przed wdrożeniem: nic nie zostało jeszcze utworzone w Linear. Klucze zadań (np. `S13-E0-M1`) są robocze; po wdrożeniu dostaną identyfikatory `LEA-…`.

**W skrócie:** 9 kamieni milowych, 53 zadania (1 start, 39 materiałów, 9 dowodów, 4 praktyki). Plik główny z kolejnością projektów: `00-kolejnosc-i-zaleznosci.md`.

## 1. Projekt

| Pole | Wartość |
|---|---|
| Nazwa | 13. UI/UX |
| Team | LEA |
| Podsumowanie (pole „Summary”) | Warstwa 4: rdzeń kompilowany i produkt. Opiera się na: 3. Jest podstawą: 14–19 i 21. |
| Proponowany start | 2027-04-01 |
| Proponowany termin | 2027-06-30 |
| Etykiety projektu | `warstwa-4` |
| Blokowany przez (projekty) | 03. Frontend web |
| Blokuje (projekty) | 14. Desktop: wspólne, 18. Android, 19. iOS |
| Czas od zera | 235–305 h |

### Opis projektu (do wklejenia w Linear)

*Warstwa 4: rdzeń kompilowany i produkt. Opiera się na: 3. Jest podstawą: 14–19 i 21.*

**Zakres umiejętności**

- Proces: przepływy użytkownika, makiety, prototypy (Figma), testy użyteczności, UX writing.
- Systemy projektowe i tokeny, spójne między web, desktop i mobile.
- Wytyczne platform: Apple Human Interface Guidelines, Material Design 3, Fluent (Windows), GNOME HIG.
- Stany ekranów (pusty, ładowanie, błąd, sukces, offline), tryb ciemny, responsywność, lokalizacja.
- Dostępność: WCAG 2.2, Europejski akt o dostępności, technologie wspomagające na każdej platformie (VoiceOver, TalkBack, Narrator, Orca), dostępność natywnych UI w Ruście.
- Onboarding, paywalle i ekrany zakupu zgodne z regułami sklepów i prawem konsumenckim.

**Ścieżka nauki**

Ścieżka ma 9 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przy doświadczeniu seniorskim we frontendzie etapy 0–1 można zaliczyć samym dowodem i wracać do materiałów tylko tam, gdzie dowód nie wychodzi; etapy o badaniach, wytycznych platform natywnych i dostępności poza webem zwykle są nowe. Dostępność web (WCAG 2.2, ARIA, testy w przeglądarce) jest w sekcji 3, tutaj chodzi o proces projektowy, platformy natywne i prawo. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

Razem od zera do poziomu E: ok. 235–305 h, czyli 5–7 miesięcy przy 10–12 h tygodniowo.

**Definicja ukończenia projektu (dowód poziomu E)**

Samodzielnie, bez agenta, w 2 dni przeprowadzasz audyt UX i dostępności nieznanej aplikacji klienta na dwóch platformach, z testem z co najmniej 3 użytkownikami, raportem z priorytetami, oceną zgodności z EAA i regułami sklepów oraz poprawionym projektem najważniejszego przepływu, i umiesz obronić rekomendacje przed osobą nietechniczną.

**Źródło:** dokument „Umiejętności techniczne” w projekcie „JDG: Rozwój oprogramowania”, sekcja 13.

## 2. Kamienie milowe

Jeden kamień milowy na etap ścieżki. Kamień milowy jest zamknięty, gdy zamknięte jest zadanie dowodu tego etapu. Daty kamieni milowych ustawiasz przy wdrożeniu według kolejności z pliku głównego.

| # | Kamień milowy | Cel | Czas od zera | Poziom po etapie | Zadania |
|---|---|---|---|---|---|
| 1 | Etap 0: podstawy użyteczności | podstawy użyteczności i psychologii interfejsu | 30–40 h | podstawy | 5 |
| 2 | Etap 1: projektowanie wizualne i Figma | projektowanie wizualne i Figma | 40–50 h | podstawy | 4 |
| 3 | Etap 2: badania i testy użyteczności | badania i testy użyteczności | 25–35 h | W | 5 |
| 4 | Etap 3: wytyczne platform | wytyczne platform: Apple, Google, Microsoft, GNOME | 40–50 h | W | 5 |
| 5 | Etap 4: systemy projektowe i tokeny | systemy projektowe i tokeny dla wielu platform | 25–35 h | W | 4 |
| 6 | Etap 5: UX writing | UX writing i mikroteksty | 15–20 h | W | 4 |
| 7 | Etap 6: dostępność na wszystkich platformach i prawo | dostępność na wszystkich platformach i prawo | 40–50 h | E | 11 |
| 8 | Etap 7: onboarding, paywalle i etyka | onboarding, paywalle i etyka: reguły sklepów i prawo konsumenckie | 20–25 h | E | 6 |
| 9 | Etap 8: ekspert | ekspert: audyty, recenzja interfejsów z AI, aktualność | stale, ok. 1–2 h tygodniowo | E | 8 |

## 3. Punkt startu

Zadanie **`S13-START` · Start: 13. UI/UX** to jedyne wejście do projektu: wszystkie zadania pierwszego etapu są przez nie blokowane.

- **Blokowane przez:** `S03-E2-D`
- **Odblokowuje:** `S13-E0-M1`, `S13-E0-M2`, `S13-E0-M3`, `S13-E0-M4`
- **Status początkowy:** Backlog do czasu zamknięcia zadań blokujących, potem Todo

Opis zadania (do wklejenia):

Punkt startu projektu „13. UI/UX”.

**Warunki wejścia (zadania blokujące):**

- `S03-E2-D` · Dowód etapu 2: TypeScript — sekcja 3 na poziomie podstawowym do pracy (etap 2)

**Do zrobienia:**

- przeczytać sekcję 13 dokumentu „Umiejętności techniczne”,
- zaznaczyć etapy, które zaliczasz samym dowodem (zgodnie z akapitem wstępnym ścieżki), i dla nich zamknąć zadania materiałów jako niepotrzebne,
- ustawić daty kamieni milowych zgodnie z kolejnością z pliku głównego.

## 4. Przepływ zależności

Linie ciągłe to zależności wewnątrz projektu, przerywane to zadania z innych projektów. Wewnątrz etapu zadania materiałów są równoległe i wszystkie blokują dowód etapu; dowód etapu blokuje materiały kolejnego etapu.

```mermaid
flowchart TD
  START["13. Start"]
  E0["Etap 0: podstawy użyteczności"]
  E1["Etap 1: projektowanie wizualne i Figma"]
  E2["Etap 2: badania i testy użyteczności"]
  E3["Etap 3: wytyczne platform"]
  E4["Etap 4: systemy projektowe i tokeny"]
  E5["Etap 5: UX writing"]
  E6["Etap 6: dostępność na wszystkich platformach i prawo"]
  E7["Etap 7: onboarding, paywalle i etyka"]
  E8["Etap 8: ekspert"]
  START --> E0
  E0 --> E1
  E1 --> E2
  E2 --> E3
  E3 --> E4
  E4 --> E5
  E5 --> E6
  E6 --> E7
  E7 --> E8
  XS03E2D(["S03-E2-D"]) -.-> START
```

## 5. Zadania według kamieni milowych

Szablon opisu zadania materiału: nazwa materiału, autor lub wydawca, typ, czas, koszt i link (jak w kolumnach poniżej) oraz zdanie „Gotowe, gdy materiał jest przerobiony w zakresie potrzebnym do dowodu etapu”. Opisy dowodów i praktyk są podane pod tabelą każdego etapu.

### Etap 0: podstawy użyteczności

Opis kamienia milowego (do wklejenia):

**Cel:** podstawy użyteczności i psychologii interfejsu · **Czas od zera:** 30–40 h · **Poziom po etapie:** podstawy

**Szczególnie ważne:** afordancje i sygnifikatory, informacja zwrotna, model mentalny użytkownika, zapobieganie błędom zamiast komunikatów o błędach, prawa Hicka, Fittsa i Jakoba, obciążenie poznawcze.

**Dowód:** Ocena heurystyczna jednej istniejącej aplikacji (najlepiej z portfolio przejmowanych projektów): 15–20 problemów przypisanych do heurystyk Nielsena, z oceną wagi i propozycją poprawki dla każdego.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje |
|---|---|---|---|---|---|---|---|
| `S13-E0-M1` | Przerobić: Don’t Make Me Think, Revisited (wydanie 3) | materiał, płatny | 5–6 h | płatna | https://sensible.com/dont-make-me-think/ | `S13-START` | `S13-E0-D` |
| `S13-E0-M2` | Przerobić: The Design of Everyday Things (wydanie poprawione i rozszerzone) | materiał, płatny | 10–12 h | płatna | https://www.hachettebookgroup.com/titles/don-norman/the-design-of-everyday-things-revised-and-expanded-edition/9780465050659/ | `S13-START` | `S13-E0-D` |
| `S13-E0-M3` | Przerobić: 10 Usability Heuristics for User Interface Design i artykuły pokrewne | materiał | 6–8 h | 0 zł | https://www.nngroup.com/articles/ten-usability-heuristics/ | `S13-START` | `S13-E0-D` |
| `S13-E0-M4` | Przerobić: Laws of UX (strona) i książka Laws of UX (wydanie 2, 2024) | materiał, płatny | 6–8 h | 0 zł / płatna | https://lawsofux.com, https://www.oreilly.com/library/view/laws-of-ux/9781098146955/ | `S13-START` | `S13-E0-D` |
| `S13-E0-D` | Dowód etapu 0: podstawy użyteczności | dowód | — | — | — | `S13-E0-M1`, `S13-E0-M2`, `S13-E0-M3`, `S13-E0-M4` | `S13-E1-M1`, `S13-E1-M2`, `S13-E1-M3` |

**`S13-E0-D` · Dowód etapu 0: podstawy użyteczności**

Ocena heurystyczna jednej istniejącej aplikacji (najlepiej z portfolio przejmowanych projektów): 15–20 problemów przypisanych do heurystyk Nielsena, z oceną wagi i propozycją poprawki dla każdego.

**Na co zwrócić uwagę:** afordancje i sygnifikatory, informacja zwrotna, model mentalny użytkownika, zapobieganie błędom zamiast komunikatów o błędach, prawa Hicka, Fittsa i Jakoba, obciążenie poznawcze.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.

### Etap 1: projektowanie wizualne i Figma

Opis kamienia milowego (do wklejenia):

**Cel:** projektowanie wizualne i Figma · **Czas od zera:** 40–50 h · **Poziom po etapie:** podstawy

**Szczególnie ważne:** hierarchia wizualna, siatka i rytm odstępów, skala typograficzna, palety kolorów z kontrastem od początku, stany komponentów, tryb ciemny, komponenty i warianty w Figmie zamiast kopiowania ramek.

**Dowód:** W Figmie projekt 5–7 ekranów jednej własnej aplikacji (lista, szczegóły, formularz, ustawienia, ekran zakupu) w wersji mobilnej i desktopowej, z jasnym i ciemnym motywem, zbudowany z własnych komponentów z wariantami i z prototypem klikanym.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje |
|---|---|---|---|---|---|---|---|
| `S13-E1-M1` | Przerobić: Refactoring UI | materiał, płatny | 8–10 h | płatna (2 rozdziały za darmo) | https://www.refactoringui.com | `S13-E0-D` | `S13-E1-D` |
| `S13-E1-M2` | Przerobić: Figma Learn: Figma Design for beginners, kursy i dokumentacja | materiał, płatny | 20–25 h | 0 zł (narzędzie z planem darmowym i płatnymi) | https://help.figma.com/hc/en-us | `S13-E0-D` | `S13-E1-D` |
| `S13-E1-M3` | Przerobić: Practical Typography | materiał | 5–6 h | 0 zł | https://practicaltypography.com | `S13-E0-D` | `S13-E1-D` |
| `S13-E1-D` | Dowód etapu 1: projektowanie wizualne i Figma | dowód | — | — | — | `S13-E1-M1`, `S13-E1-M2`, `S13-E1-M3` | `S13-E2-M1`, `S13-E2-M2`, `S13-E2-M3`, `S13-E2-M4` |

**`S13-E1-D` · Dowód etapu 1: projektowanie wizualne i Figma**

W Figmie projekt 5–7 ekranów jednej własnej aplikacji (lista, szczegóły, formularz, ustawienia, ekran zakupu) w wersji mobilnej i desktopowej, z jasnym i ciemnym motywem, zbudowany z własnych komponentów z wariantami i z prototypem klikanym.

**Na co zwrócić uwagę:** hierarchia wizualna, siatka i rytm odstępów, skala typograficzna, palety kolorów z kontrastem od początku, stany komponentów, tryb ciemny, komponenty i warianty w Figmie zamiast kopiowania ramek.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.

### Etap 2: badania i testy użyteczności

Opis kamienia milowego (do wklejenia):

**Cel:** badania i testy użyteczności · **Czas od zera:** 25–35 h · **Poziom po etapie:** W

**Szczególnie ważne:** pytania bez sugerowania odpowiedzi, scenariusz zadań zamiast pytania o opinię, 5 uczestników na rundę i kolejne rundy po poprawkach, analityka produktowa jako uzupełnienie, a nie zamiennik rozmów, zgody i dane osobowe uczestników (RODO).

**Dowód:** Dwie rundy testów użyteczności (po 5 osób) prototypu z etapu 1: scenariusz, nagrania za zgodą, lista problemów z częstością i wagą, poprawki między rundami i porównanie wyników.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje |
|---|---|---|---|---|---|---|---|
| `S13-E2-M1` | Przerobić: Rocket Surgery Made Easy | materiał, płatny | 4–5 h | płatna | https://sensible.com/rocket-surgery-made-easy/ | `S13-E1-D` | `S13-E2-D` |
| `S13-E2-M2` | Przerobić: Just Enough Research (wydanie 2) | materiał, płatny | 4–5 h | płatna | https://abookapart.com/blogs/press/just-enough-research-2nd-edition-is-now-available | `S13-E1-D` | `S13-E2-D` |
| `S13-E2-M3` | Przerobić: Artykuły NN/g o badaniach | materiał | 8–10 h | 0 zł | https://www.nngroup.com/articles/ | `S13-E1-D` | `S13-E2-D` |
| `S13-E2-M4` | Przerobić: Kursy UX Nielsen Norman Group (opcjonalnie, z certyfikacją) | materiał, płatny | wg potrzeb | płatne | https://www.nngroup.com/courses/ | `S13-E1-D` | `S13-E2-D` |
| `S13-E2-D` | Dowód etapu 2: badania i testy użyteczności | dowód | — | — | — | `S13-E2-M1`, `S13-E2-M2`, `S13-E2-M3`, `S13-E2-M4` | `S13-E3-M1`, `S13-E3-M2`, `S13-E3-M3`, `S13-E3-M4`, `S14-START`, `S18-START`, `S19-START` |

**`S13-E2-D` · Dowód etapu 2: badania i testy użyteczności**

Dwie rundy testów użyteczności (po 5 osób) prototypu z etapu 1: scenariusz, nagrania za zgodą, lista problemów z częstością i wagą, poprawki między rundami i porównanie wyników.

**Na co zwrócić uwagę:** pytania bez sugerowania odpowiedzi, scenariusz zadań zamiast pytania o opinię, 5 uczestników na rundę i kolejne rundy po poprawkach, analityka produktowa jako uzupełnienie, a nie zamiennik rozmów, zgody i dane osobowe uczestników (RODO).

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.

### Etap 3: wytyczne platform

Opis kamienia milowego (do wklejenia):

**Cel:** wytyczne platform: Apple, Google, Microsoft, GNOME · **Czas od zera:** 40–50 h · **Poziom po etapie:** W

**Szczególnie ważne:** nawigacja i gesty specyficzne dla platformy (wstecz w Androidzie, paski kart i arkusze w iOS, menu i skróty klawiaturowe na desktopie), dynamiczny rozmiar tekstu, obszary dotyku, okna i ich rozmiary na desktopie, kiedy Tauri z Reactem może wyglądać „tak samo wszędzie”, a kiedy użytkownik oczekuje wyglądu natywnego.

**Dowód:** Ten sam przepływ (np. zakup i ustawienia) zaprojektowany w trzech wariantach: iOS, Android i desktop, z notatką, które różnice wynikają z wytycznych platformy, a które są świadomym odstępstwem i dlaczego.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje |
|---|---|---|---|---|---|---|---|
| `S13-E3-M1` | Przerobić: Human Interface Guidelines | materiał | 12–15 h | 0 zł | https://developer.apple.com/design/human-interface-guidelines/ | `S13-E2-D` | `S13-E3-D` |
| `S13-E3-M2` | Przerobić: Material Design 3 | materiał | 10–12 h | 0 zł | https://m3.material.io | `S13-E2-D` | `S13-E3-D` |
| `S13-E3-M3` | Przerobić: Fluent 2 Design System | materiał | 6–8 h | 0 zł | https://fluent2.microsoft.design | `S13-E2-D` | `S13-E3-D` |
| `S13-E3-M4` | Przerobić: GNOME Human Interface Guidelines | materiał | 4–6 h | 0 zł | https://developer.gnome.org/hig/ | `S13-E2-D` | `S13-E3-D` |
| `S13-E3-D` | Dowód etapu 3: wytyczne platform | dowód | — | — | — | `S13-E3-M1`, `S13-E3-M2`, `S13-E3-M3`, `S13-E3-M4` | `S13-E4-M1`, `S13-E4-M2`, `S13-E4-M3` |

**`S13-E3-D` · Dowód etapu 3: wytyczne platform**

Ten sam przepływ (np. zakup i ustawienia) zaprojektowany w trzech wariantach: iOS, Android i desktop, z notatką, które różnice wynikają z wytycznych platformy, a które są świadomym odstępstwem i dlaczego.

**Na co zwrócić uwagę:** nawigacja i gesty specyficzne dla platformy (wstecz w Androidzie, paski kart i arkusze w iOS, menu i skróty klawiaturowe na desktopie), dynamiczny rozmiar tekstu, obszary dotyku, okna i ich rozmiary na desktopie, kiedy Tauri z Reactem może wyglądać „tak samo wszędzie”, a kiedy użytkownik oczekuje wyglądu natywnego.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.

### Etap 4: systemy projektowe i tokeny

Opis kamienia milowego (do wklejenia):

**Cel:** systemy projektowe i tokeny dla wielu platform · **Czas od zera:** 25–35 h · **Poziom po etapie:** W

Specyfikacja DTCG jest raportem grupy społecznościowej W3C, a nie standardem W3C, ale jest stabilna i stała się wspólnym formatem wymiany między narzędziami. Tokeny i komponenty web (Tailwind, Radix, shadcn/ui) są w sekcji 3.

**Dowód:** Jedno źródło tokenów w formacie DTCG (kolory z trybami jasnym i ciemnym, typografia, odstępy, promienie) generowane w CI do zmiennych CSS i motywu Tailwind, stałych Swift, zasobów Kotlin/Compose i motywu natywnego UI w Ruście (np. Slint); zmiana jednego tokenu widoczna na wszystkich platformach po jednym buildzie.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje |
|---|---|---|---|---|---|---|---|
| `S13-E4-M1` | Przerobić: Design Tokens Format Module 2025.10 | materiał | 4–6 h | 0 zł | https://www.designtokens.org/tr/2025.10/format/ | `S13-E3-D` | `S13-E4-D` |
| `S13-E4-M2` | Przerobić: Figma Learn: zmienne, tryby i biblioteki | materiał | 4–5 h | 0 zł | https://help.figma.com/hc/en-us | `S13-E3-D` | `S13-E4-D` |
| `S13-E4-M3` | Przerobić: Fluent 2 i Material Design 3: rozdziały o tokenach i motywach | materiał | 4–6 h | 0 zł | https://fluent2.microsoft.design, https://m3.material.io | `S13-E3-D` | `S13-E4-D` |
| `S13-E4-D` | Dowód etapu 4: systemy projektowe i tokeny | dowód | — | — | — | `S13-E4-M1`, `S13-E4-M2`, `S13-E4-M3` | `S13-E5-M1`, `S13-E5-M2`, `S13-E5-M3` |

**`S13-E4-D` · Dowód etapu 4: systemy projektowe i tokeny**

Jedno źródło tokenów w formacie DTCG (kolory z trybami jasnym i ciemnym, typografia, odstępy, promienie) generowane w CI do zmiennych CSS i motywu Tailwind, stałych Swift, zasobów Kotlin/Compose i motywu natywnego UI w Ruście (np. Slint); zmiana jednego tokenu widoczna na wszystkich platformach po jednym buildzie.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.

### Etap 5: UX writing

Opis kamienia milowego (do wklejenia):

**Cel:** UX writing i mikroteksty · **Czas od zera:** 15–20 h · **Poziom po etapie:** W

**Szczególnie ważne:** komunikaty błędów mówiące, co zrobić dalej, stany puste, przyciski nazwane czynnością, spójny słownik w całym produkcie, teksty przygotowane do lokalizacji (długość, liczba mnoga, płeć gramatyczna w polskim), prosty język jako element dostępności.

**Dowód:** Przepisany komplet tekstów jednej aplikacji (onboarding, błędy, stany puste, paywall, potwierdzenia) z krótkim przewodnikiem stylu i słownikiem, w dwóch językach przez pliki tłumaczeń, bez tekstów wpisanych na stałe w kodzie.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje |
|---|---|---|---|---|---|---|---|
| `S13-E5-M1` | Przerobić: Strategic Writing for UX (wydanie 2, 2025) | materiał, płatny | 6–8 h | płatna | https://www.oreilly.com/library/view/strategic-writing-for/9781098174323/ | `S13-E4-D` | `S13-E5-D` |
| `S13-E5-M2` | Przerobić: Microcopy: The Complete Guide | materiał, płatny | 5–6 h | płatna | https://www.microcopybook.com | `S13-E4-D` | `S13-E5-D` |
| `S13-E5-M3` | Przerobić: Wytyczne pisania w HIG, Material Design 3 i GNOME HIG | materiał | 2–3 h | 0 zł | jak w etapie 3 | `S13-E4-D` | `S13-E5-D` |
| `S13-E5-D` | Dowód etapu 5: UX writing | dowód | — | — | — | `S13-E5-M1`, `S13-E5-M2`, `S13-E5-M3` | `S13-E6-M1`, `S13-E6-M2`, `S13-E6-M3`, `S13-E6-M4`, `S13-E6-M5`, `S13-E6-M6`, `S13-E6-M7`, `S13-E6-M8`, `S13-E6-M9`, `S13-E6-M10` |

**`S13-E5-D` · Dowód etapu 5: UX writing**

Przepisany komplet tekstów jednej aplikacji (onboarding, błędy, stany puste, paywall, potwierdzenia) z krótkim przewodnikiem stylu i słownikiem, w dwóch językach przez pliki tłumaczeń, bez tekstów wpisanych na stałe w kodzie.

**Na co zwrócić uwagę:** komunikaty błędów mówiące, co zrobić dalej, stany puste, przyciski nazwane czynnością, spójny słownik w całym produkcie, teksty przygotowane do lokalizacji (długość, liczba mnoga, płeć gramatyczna w polskim), prosty język jako element dostępności.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.

### Etap 6: dostępność na wszystkich platformach i prawo

Opis kamienia milowego (do wklejenia):

**Cel:** dostępność na wszystkich platformach i prawo · **Czas od zera:** 40–50 h · **Poziom po etapie:** E

Stan na 11 października 2026 r.: polska ustawa wdrażająca EAA obowiązuje od 28 czerwca 2025 r.; EN 301 549 V4.1.1, oparta na WCAG 2.2 AA z dodatkowymi kryteriami, została opublikowana 2 września 2026 r., ale domniemanie zgodności z EAA da dopiero jej publikacja w Dzienniku Urzędowym UE. Apple pokazuje w App Store etykiety dostępności (Accessibility Nutrition Labels); na razie są dobrowolne, a Apple zapowiada, że staną się obowiązkowe. Mikroprzedsiębiorcy świadczący usługi są zwolnieni z części obowiązków ustawy, ale klienci firmy zwykle nie są.

**Dowód:** Audyt dostępności własnej aplikacji na trzech platformach (web, iOS lub Android, desktop): przejście kluczowych zadań (pierwsze uruchomienie, logowanie, zakup, ustawienia) z VoiceOver lub TalkBack, Narratorem lub Orca, powiększonym tekstem i samą klawiaturą; raport według WCAG-EM z poprawkami i uczciwie wypełnione etykiety dostępności w App Store Connect.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje |
|---|---|---|---|---|---|---|---|
| `S13-E6-M1` | Przerobić: Inclusive Components | materiał, płatny | 6–8 h | 0 zł / płatna | https://inclusive-components.design | `S13-E5-D` | `S13-E6-D` |
| `S13-E6-M2` | Przerobić: Deque University: pakiet z kursem dostępności aplikacji natywnych | materiał, płatny | 20–30 h | abonament | https://dequeuniversity.com/online-courses/ | `S13-E5-D` | `S13-E6-D` |
| `S13-E6-M3` | Przerobić: Accessibility (dokumentacja dla deweloperów) i Accessibility Nutrition Labels w App Store Connect | materiał | 3–4 h | 0 zł | https://developer.apple.com/accessibility/, https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels | `S13-E5-D` | `S13-E6-D` |
| `S13-E6-M4` | Przerobić: Build accessible apps, dostępność w Jetpack Compose | materiał | 3–4 h | 0 zł | https://developer.android.com/guide/topics/ui/accessibility | `S13-E5-D` | `S13-E6-D` |
| `S13-E6-M5` | Przerobić: Accessibility overview: Windows apps (UI Automation, wysoki kontrast) i Accessibility Insights | materiał | 2–3 h | 0 zł | https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility, https://accessibilityinsights.io | `S13-E5-D` | `S13-E6-D` |
| `S13-E6-M6` | Przerobić: AccessKit: dostępność UI rysowanych w Ruście (egui, Slint i inne) | materiał | 1–2 h | 0 zł | https://accesskit.dev | `S13-E5-D` | `S13-E6-D` |
| `S13-E6-M7` | Przerobić: WCAG-EM: metodyka oceny zgodności i Easy Checks | materiał | 2–3 h | 0 zł | https://www.w3.org/WAI/test-evaluate/ | `S13-E5-D` | `S13-E6-D` |
| `S13-E6-M8` | Przerobić: Dyrektywa (UE) 2019/882 (Europejski akt o dostępności) | materiał | 3–4 h | 0 zł | https://eur-lex.europa.eu/eli/dir/2019/882/oj | `S13-E5-D` | `S13-E6-D` |
| `S13-E6-M9` | Przerobić: Ustawa z 26 kwietnia 2024 r. o zapewnianiu spełniania wymagań dostępności niektórych produktów i… | materiał | 3–4 h | 0 zł | https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20240000731 | `S13-E5-D` | `S13-E6-D` |
| `S13-E6-M10` | Przerobić: EN 301 549 V4.1.1 (wrzesień 2026) | materiał | 4–6 h | 0 zł | https://www.etsi.org | `S13-E5-D` | `S13-E6-D` |
| `S13-E6-D` | Dowód etapu 6: dostępność na wszystkich platformach i prawo | dowód | — | — | — | `S13-E6-M1`, `S13-E6-M2`, `S13-E6-M3`, `S13-E6-M4`, `S13-E6-M5`, `S13-E6-M6`, `S13-E6-M7`, `S13-E6-M8`, `S13-E6-M9`, `S13-E6-M10` | `S13-E7-M1`, `S13-E7-M2`, `S13-E7-M3`, `S13-E7-M4`, `S13-E7-M5` |

**`S13-E6-D` · Dowód etapu 6: dostępność na wszystkich platformach i prawo**

Audyt dostępności własnej aplikacji na trzech platformach (web, iOS lub Android, desktop): przejście kluczowych zadań (pierwsze uruchomienie, logowanie, zakup, ustawienia) z VoiceOver lub TalkBack, Narratorem lub Orca, powiększonym tekstem i samą klawiaturą; raport według WCAG-EM z poprawkami i uczciwie wypełnione etykiety dostępności w App Store Connect.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.

### Etap 7: onboarding, paywalle i etyka

Opis kamienia milowego (do wklejenia):

**Cel:** onboarding, paywalle i etyka: reguły sklepów i prawo konsumenckie · **Czas od zera:** 20–25 h · **Poziom po etapie:** E

**Szczególnie ważne:** cena, okres rozliczenia, warunki okresu próbnego i sposób anulowania widoczne przed zakupem, przywracanie zakupów, brak zatrzymywania użytkownika przy rezygnacji, różnice zasad między sklepami i kanałem web (Merchant of Record), wzorce zwodnicze jako ryzyko prawne, a nie tylko etyczne. Implementacja zakupów i licencji jest w sekcjach 5, 18 i 19.

**Dowód:** Onboarding i paywall jednej własnej aplikacji w trzech kanałach (App Store, Google Play, web), sprawdzone punkt po punkcie z sekcją 3.1 App Review Guidelines, zasadami Google Play i przepisami o prawach konsumenta; rezygnacja z abonamentu osiągalna w nie więcej krokach niż zakup; przejście przez recenzję w obu sklepach bez odrzucenia za płatności.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje |
|---|---|---|---|---|---|---|---|
| `S13-E7-M1` | Przerobić: App Review Guidelines, sekcja 3.1 Payments | materiał | 3–4 h | 0 zł | https://developer.apple.com/app-store/review/guidelines/ | `S13-E6-D` | `S13-E7-D` |
| `S13-E7-M2` | Przerobić: Payments i Create and manage subscriptions (przejrzystość ofert) | materiał | 2–3 h | 0 zł | https://support.google.com/googleplay/android-developer/answer/9858738, https://support.google.com/googleplay/android-developer/answer/140504 | `S13-E6-D` | `S13-E7-D` |
| `S13-E7-M3` | Przerobić: Deceptive Patterns | materiał, płatny | 5–6 h | płatna (katalog online 0 zł) | https://deceptive.design | `S13-E6-D` | `S13-E7-D` |
| `S13-E7-M4` | Przerobić: Dyrektywa (UE) 2023/2673 | materiał | 2–3 h | 0 zł | https://eur-lex.europa.eu/eli/dir/2023/2673/oj | `S13-E6-D` | `S13-E7-D` |
| `S13-E7-M5` | Przerobić: Artykuły NN/g o onboardingu, paywallach i formularzach | materiał | 3–4 h | 0 zł | https://www.nngroup.com/articles/ | `S13-E6-D` | `S13-E7-D` |
| `S13-E7-D` | Dowód etapu 7: onboarding, paywalle i etyka | dowód | — | — | — | `S13-E7-M1`, `S13-E7-M2`, `S13-E7-M3`, `S13-E7-M4`, `S13-E7-M5` | `S13-E8-M1`, `S13-E8-M2`, `S13-E8-M3`, `S13-E8-P1`, `S13-E8-P2`, `S13-E8-P3`, `S13-E8-P4` |

**`S13-E7-D` · Dowód etapu 7: onboarding, paywalle i etyka**

Onboarding i paywall jednej własnej aplikacji w trzech kanałach (App Store, Google Play, web), sprawdzone punkt po punkcie z sekcją 3.1 App Review Guidelines, zasadami Google Play i przepisami o prawach konsumenta; rezygnacja z abonamentu osiągalna w nie więcej krokach niż zakup; przejście przez recenzję w obu sklepach bez odrzucenia za płatności.

**Na co zwrócić uwagę:** cena, okres rozliczenia, warunki okresu próbnego i sposób anulowania widoczne przed zakupem, przywracanie zakupów, brak zatrzymywania użytkownika przy rezygnacji, różnice zasad między sklepami i kanałem web (Merchant of Record), wzorce zwodnicze jako ryzyko prawne, a nie tylko etyczne. Implementacja zakupów i licencji jest w sekcjach 5, 18 i 19.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.

### Etap 8: ekspert

Opis kamienia milowego (do wklejenia):

**Cel:** ekspert: audyty, recenzja interfejsów z AI, aktualność · **Czas od zera:** stale, ok. 1–2 h tygodniowo · **Poziom po etapie:** E

**Dowód poziomu E:** Samodzielnie, bez agenta, w 2 dni przeprowadzasz audyt UX i dostępności nieznanej aplikacji klienta na dwóch platformach, z testem z co najmniej 3 użytkownikami, raportem z priorytetami, oceną zgodności z EAA i regułami sklepów oraz poprawionym projektem najważniejszego przepływu, i umiesz obronić rekomendacje przed osobą nietechniczną.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje |
|---|---|---|---|---|---|---|---|
| `S13-E8-M1` | Przerobić: Nowe artykuły i badania NN/g | materiał | ok. 1 h tygodniowo | 0 zł | https://www.nngroup.com/articles/ | `S13-E7-D` | `S13-E8-D` |
| `S13-E8-M2` | Przerobić: Zmiany w HIG, Material Design i Fluent oraz sesje projektowe z konferencji WWDC i Google I/O | materiał | wg potrzeb | 0 zł | https://developer.apple.com/design/, https://m3.material.io | `S13-E7-D` | `S13-E8-D` |
| `S13-E8-M3` | Przerobić: Zmiany w zasadach sklepów i prawie (EAA, EN 301 549, prawa konsumenta) | materiał | ok. 1 h miesięcznie | 0 zł | jak w etapach 6 i 7 | `S13-E7-D` | `S13-E8-D` |
| `S13-E8-P1` | Praktyka: recenzja interfejsów z AI | praktyka | — | — | — | `S13-E7-D` | `S13-E8-D` |
| `S13-E8-P2` | Praktyka: audyt UX i dostępności przejmowanej aplikacji | praktyka | — | — | — | `S13-E7-D` | `S13-E8-D` |
| `S13-E8-P3` | Praktyka: system projektowy w praktyce | praktyka | — | — | — | `S13-E7-D` | `S13-E8-D` |
| `S13-E8-P4` | Praktyka: pomiar | praktyka | — | — | — | `S13-E7-D` | `S13-E8-D` |
| `S13-E8-D` | Dowód poziomu E: ekspert | dowód | — | — | — | `S13-E8-M1`, `S13-E8-M2`, `S13-E8-M3`, `S13-E8-P1`, `S13-E8-P2`, `S13-E8-P3`, `S13-E8-P4` | — |

**`S13-E8-P1` · Praktyka: recenzja interfejsów z AI**

20 ekranów lub pull requestów z UI wygenerowanych przez agentów, ocenianych według listy kontrolnej z etapów 3–7 (brakujące stany pusty, błędu i offline, wartości wpisane zamiast tokenów, wzorce z innej platformy, ikony bez etykiet dostępności, teksty na stałe w kodzie, wzorce zwodnicze w paywallu, „ładne, ale nieużyteczne” układy).

Praktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, a nie po jednorazowym wykonaniu.

**`S13-E8-P2` · Praktyka: audyt UX i dostępności przejmowanej aplikacji**

Pierwsza aplikacja klienta przeprowadzona przez ocenę heurystyczną, test z 5 użytkownikami i audyt dostępności, z planem poprawek uszeregowanym według wpływu i kosztu.

Praktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, a nie po jednorazowym wykonaniu.

**`S13-E8-P3` · Praktyka: system projektowy w praktyce**

Tokeny i komponenty używane przez wszystkie własne aplikacje, z dokumentacją, którą agenci czytają jako kontekst.

Praktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, a nie po jednorazowym wykonaniu.

**`S13-E8-P4` · Praktyka: pomiar**

Jedna zmiana UX na kwartał zweryfikowana danymi (konwersja paywalla, ukończenie onboardingu, zgłoszenia do wsparcia).

Praktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, a nie po jednorazowym wykonaniu.

**`S13-E8-D` · Dowód poziomu E: ekspert**

Samodzielnie, bez agenta, w 2 dni przeprowadzasz audyt UX i dostępności nieznanej aplikacji klienta na dwóch platformach, z testem z co najmniej 3 użytkownikami, raportem z priorytetami, oceną zgodności z EAA i regułami sklepów oraz poprawionym projektem najważniejszego przepływu, i umiesz obronić rekomendacje przed osobą nietechniczną.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki. Bez agenta AI.

## 6. Relacje z innymi projektami

**Wchodzące** (zadanie z innego projektu blokuje zadanie tego projektu):

- `S03-E2-D` (Dowód etapu 2: TypeScript) → `S13-START`

**Wychodzące** (zadanie tego projektu blokuje zadanie w innym projekcie):

- `S13-E2-D` → `S14-START` (14. Desktop: wspólne)
- `S13-E2-D` → `S18-START` (18. Android)
- `S13-E2-D` → `S19-START` (19. iOS)
