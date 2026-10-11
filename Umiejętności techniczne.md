# Umiejętności techniczne: solo twórca AI-native, aplikacje wieloplatformowe z Rustem

Stan na 11 października 2026 r. (wersja z układem warstw) · Na podstawie dokumentów: „Business plan – Daniel Jarosz”, „Profil kompetencji solo AI-native” i „vicrafter – specyfikacja pluginu”, rozszerzonych o siedem platform docelowych i preferencję Rusta dla aplikacji kompilowanych.

**Założenie:** agenci piszą kod, a człowiek zatwierdza specyfikację, plan, recenzję i wydanie. Każdą umiejętność trzeba więc mieć co najmniej na poziomie **W (weryfikacja)**: czytać, oceniać, debugować i wychwytywać błędy agenta. Część trzeba mieć na poziomie **E (ekspert)**, bo przy incydencie, hotfixie albo zablokowanym zadaniu człowiek pisze sam.

**Platformy docelowe:** web (React, Next.js), Android, iOS, desktop Linux, macOS i Windows, systemy wbudowane.

**Układ:** sekcje są ułożone w 9 warstwach, tak że każda opiera się wyłącznie na wcześniejszych (zob. „Mapa warstw”). Każda sekcja ma podsekcję „Ścieżka nauki: od zera do eksperta” z etapami, materiałami i dowodem opanowania. Łączny czas i kolejność według bramek biznesplanu są na końcu dokumentu. Ceny płatnych materiałów nie są podane, bo często się zmieniają.

---

## Gdzie Rust jest możliwy, a gdzie nie

Rust nie pokryje wszystkiego, a weryfikacja wymaga znajomości także warstw, które w Ruście nie powstaną.

| Platforma | Rust | Czego Rust nie zastąpi |
|---|---|---|
| Web | usługi backendowe (Axum), ewentualnie moduły WASM | frontend React i Next.js zostaje w TypeScript, serwer Next.js działa na Node.js |
| Android | wspólny rdzeń logiki (UniFFI, cargo-ndk) albo cała aplikacja w Tauri 2 | natywny interfejs, cykl życia i API systemu: Kotlin, Jetpack Compose |
| iOS | wspólny rdzeń (UniFFI, XCFramework) albo Tauri 2 | natywny interfejs, StoreKit i integracje: Swift, SwiftUI |
| Desktop (3 systemy) | prawie wszystko: Tauri 2 (Rust i webview z Reactem) albo natywny UI w Ruście (Slint, egui, Iced, Dioxus) | instalatory, podpisy i integracje systemowe wymagają wiedzy o każdej platformie |
| Wbudowane | firmware w `no_std` (Embassy, RTIC) na wspieranych układach (STM32, nRF, RP2040/RP2350, ESP32) | SDK producentów, certyfikowane stosy radiowe i Zephyr bywają w C |
| Funkcje AI | wnioskowanie lokalne (llama.cpp, mistral.rs, Candle, `ort`), RAG, pośrednik API, embedded (`tract`) | dostrajanie modeli w ekosystemie Python, systemowe modele Apple i Google przez Swift i Kotlin, AI w przeglądarce przez JavaScript |
| Projekty klientów „rescue” | tylko jeśli klient zamówi przepisanie | przejmowany jest stack klienta: TypeScript, Python, PHP, Supabase, no-code |

**Rekomendowana architektura własnych aplikacji:** jeden rdzeń w Ruście (logika, dane, synchronizacja, licencje), a nad nim cienkie warstwy interfejsu: React na web i desktop (Tauri), Swift i Kotlin na mobile.

---

## Mapa warstw

Sekcje są ułożone tak, że każda opiera się wyłącznie na wcześniejszych. Pod nagłówkiem każdej sekcji jest linia z jej warstwą, sekcjami, na których się opiera, i sekcjami, które na niej stoją. Obszary przekrojowe (testy, wymagania, architektura, CI, bezpieczeństwo, weryfikacja AI, UI/UX) uczy się spiralnie: najpierw na web do poziomu W, a każda kolejna platforma dokłada swój fragment.

| Warstwa | Sekcje | Na czym się opiera |
|---|---|---|
| 0: fundamenty | 1 Praca z AI w chmurze (tor równoległy), 2 Języki i narzędzia podstawowe, 3 Frontend web | — |
| 1: dane i serwer | 4 Bazy danych, 5 Backend i API | 2, 3 |
| 2: jakość i projektowanie | 6 Testowanie, 7 Wymagania i specyfikacje, 8 Architektura i projektowanie systemów, 9 DevOps, CI/CD i wydania | 2–5 |
| 3: ochrona i kontrola | 10 Bezpieczeństwo, 11 Weryfikacja pracy AI i budowa procesu | 1, 3–9 |
| 4: rdzeń kompilowany i produkt | 12 Rust (z C w 12.2), 13 UI/UX | 2, 3, 5, 6, 8, 9 |
| 5: desktop | 14 Desktop: wspólne, 15 Linux, 16 macOS, 17 Windows (z PowerShell w 17.2) | 3, 8, 9, 12, 13 |
| 6: mobile | 18 Android, 19 iOS | 9, 12–14 |
| 7: AI w produktach | 20 Lokalne AI i rozwój modeli (z Pythonem w 20.4), 21 Funkcje AI w aplikacjach | 1, 5, 6, 8, 10, 12, platformy 14–19 |
| 8: sprzęt | 22 Systemy wbudowane | 10, 12 na poziomie E, 12.2 |

Sekcja 1 jest torem równoległym: Claude i Claude Code to narzędzie, którym przechodzi się wszystkie pozostałe warstwy, więc jej etapy 0–2 warto przejść na samym początku, a kolejne równolegle z warstwami 2–3.

---

## 1. Praca z AI w chmurze: Claude i Claude Code

*Warstwa 0: fundamenty, tor równoległy. Opiera się na: —. Jest podstawą: wszystkich pozostałych sekcji.*

W tym modelu biznesowym większość kodu piszą agenci, a człowiek planuje, przekazuje kontekst i weryfikuje wynik. Od tego, jak sprawnie i bezpiecznie pracuje się z Claude i Claude Code, zależą jednocześnie wydajność, jakość audytów, koszt AI (próg 5% przychodu) i zgodność z RODO wobec klientów, których kod i dane trafiają do modelu w chmurze. Ta sekcja obejmuje AI jako narzędzie własnej pracy; konfiguracja i rozszerzanie Claude Code, recenzja kodu z AI, ewaluacje i bezpieczeństwo agentów są w sekcji 11, a API Claude w produktach klientów w sekcji 21.

- Działanie LLM na poziomie użytkownika: tokeny, okno kontekstu i spadek jakości przy jego zapełnianiu, niedeterminizm (to samo polecenie daje różne wyniki), halucynacje (wymyślone API, pakiety, przepisy, źródła), data granicy wiedzy modelu, rozumowanie (extended thinking) i poziom wysiłku.
- Dobór modelu do zadania: model najmocniejszy do planowania, architektury i trudnych błędów, tańszy do rutyny i subagentów, najmniejszy do klasyfikacji; przełączanie w trakcie sesji (`/model`, `/effort`).
- Przekazywanie kontekstu: `CLAUDE.md` (krótki, tylko to, czego agent nie wyczyta z kodu), import plików, `AGENTS.md` w przejmowanych repozytoriach, pamięć automatyczna, specyfikacja w pliku (`SPEC.md`, `PLAN.md`) pisana po wywiadzie prowadzonym przez agenta, odwołania `@plik`, zrzuty ekranu, logi przez potok.
- Cykl pracy: eksploracja, tryb planowania (plan zatwierdzony lub poprawiony przez człowieka), implementacja małymi krokami, weryfikowalne kryterium ukończenia (test, build, linter, zrzut ekranu), commit; agent pokazuje dowód (wynik testów, uruchomione polecenie), a nie tylko deklaruje sukces.
- Zarządzanie sesją i kontekstem: `/clear` między niezwiązanymi zadaniami, `/compact` z instrukcją, co zachować, `/context`, nazwane sesje (`/rename`, `--continue`, `--resume`), punkty kontrolne i `/rewind` (nie zastępują gita), subagenci do eksploracji, żeby nie zaśmiecać głównego kontekstu.
- Praca równoległa: kilka sesji w osobnych worktree gita, wzorzec „autor i recenzent” w dwóch świeżych kontekstach, tryb nieinteraktywny (`claude -p`) do powtarzalnych zadań; granica, przy której człowiek przestaje nadążać z weryfikacją.
- Rozpoznawanie, że agent błądzi, i przerywanie pętli: `Esc` od razu, po dwóch nieudanych poprawkach nowa sesja z lepszym poleceniem, zawężenie zadania, powrót do punktu kontrolnego, samodzielne wykonanie fragmentu.
- Claude w aplikacji (claude.ai, desktop): projekty z wiedzą i instrukcjami dla każdego klienta, research z wyszukiwaniem w sieci, praca na długich dokumentach (umowy, normy, dokumentacja przejmowanej aplikacji), szkice raportów z audytu, ofert i specyfikacji; sprawdzanie każdego cytatu i źródła.
- Pisanie promptów: jasny cel i kontekst, przykłady, struktura (np. znaczniki XML), rola, kryteria sukcesu, prośba o przyznanie się do niewiedzy, łańcuchy promptów zamiast jednego wielkiego; prompty do powtarzalnych zadań przechowywane i wersjonowane jak kod.
- API do automatyzacji własnej pracy: Claude Console, klucze API i obszary robocze (workspaces) z limitami wydatków, limity zapytań i tokenów, przetwarzanie wsadowe tańszych zadań (np. streszczenia wielu plików), liczenie tokenów przed wysłaniem, raport zużycia i kosztów; klucze w menedżerze sekretów, nigdy w repozytorium.
- Dane i prawo: klasyfikacja danych klienta przed wysłaniem do modelu (kod, sekrety, dane osobowe, zrzuty bazy), minimalizacja i pseudonimizacja, plany konsumenckie (Free, Pro, Max: Consumer Terms, ustawienie trenowania na danych, retencja 30 dni lub do 5 lat) a komercyjne (Team, Enterprise, API: Commercial Terms, brak trenowania domyślnie, DPA ze standardowymi klauzulami umownymi, lista podprocesorów), transfery poza EOG, zapis o używaniu AI i podprocesorach w ofercie i umowie powierzenia z klientem; weryfikacja z prawnikiem.
- Koszty i limity: limity planów subskrypcyjnych (okna kilkugodzinne i tygodniowe, wspólne dla czatu i Claude Code), `/usage` i linia statusu, koszt na zadanie i na projekt, miesięczny raport kosztu AI względem progu 5% przychodu, zachowania, które zawyżają zużycie (długie sesje, chybienia cache, wielu agentów równolegle).
- Zależność od jednego dostawcy i plan B: przenośne artefakty (specyfikacje, prompty, testy, ewaluacje), drugi dostawca przez bramkę LLM, model lokalny do danych, które nie mogą wyjść z maszyny (zob. sekcja 20), procedura na wypadek awarii, zmiany cennika lub warunków.
- Uczenie się z AI bez utraty umiejętności: AI jako tutor (wyjaśnienia, pytania sprawdzające) zamiast generatora gotowych rozwiązań w obszarach, które dopiero się poznaje; regularne zadania „bez agenta” jako dowód, że weryfikacja nie jest pozorna.
- Typowe błędy pracy z agentem do wyłapania: sesja „na wszystko” z zaśmieconym kontekstem, wielokrotne poprawianie zamiast nowego startu, rozdęty `CLAUDE.md`, którego agent nie przestrzega, akceptowanie wyniku bez uruchomionej weryfikacji, osłabianie lub usuwanie testów, żeby „przeszły”, niekontrolowana eksploracja setek plików, wymyślone pakiety i API, wklejanie sekretów i danych osobowych klienta do czatu na planie konsumenckim, praca na danych klienta bez podstawy w umowie.

### 1.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 7 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. To tor równoległy: etapy 0–2 warto przejść przed pierwszym projektem klienta, bo przez nie przechodzi praca we wszystkich pozostałych sekcjach, a etapy 4 i 5 przed podpisaniem pierwszej umowy. Przy doświadczeniu seniorskim etap 0 można zaliczyć samym dowodem. Czas podany dla osoby startującej od zera; ceny materiałów płatnych i planów zmieniają się, więc warto je sprawdzić przed zakupem. Dokumentacja Claude Code i warunki planów zmieniają się co kilka tygodni, więc materiały z tej sekcji trzeba czytać w wersji bieżącej, a nie z notatek. Konfiguracja i rozszerzanie Claude Code (uprawnienia, skille, subagenci, hooki, pluginy, MCP) są w sekcji 11, API Claude w produktach w sekcji 21, modele lokalne w sekcji 20.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | jak działają LLM i agenci kodujący | 15–20 h | podstawy |
| 1 | codzienna praca z Claude Code | 30–40 h | W |
| 2 | Claude w aplikacji i pisanie promptów | 15–20 h | W |
| 3 | API Claude do automatyzacji własnej pracy | 15–20 h | W |
| 4 | dane klienta, RODO i umowy | 15–20 h | E |
| 5 | koszty, limity i plan B | 10–15 h | E |
| 6 | ekspert: praca równoległa, pomiar, aktualność | stale, ok. 1 h tygodniowo | E |

Razem od zera do poziomu E: ok. 100–135 h, czyli 2–3 miesiące przy 10–12 h tygodniowo.

#### Etap 0: jak działają LLM i agenci kodujący

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| „Deep Dive into LLMs like ChatGPT” | Andrej Karpathy | wykład wideo, od podstaw | 3–4 h | 0 zł | https://www.youtube.com/watch?v=7xTGNNLPyMI |
| Kursy Anthropic Academy: „Claude 101”, „AI Fluency: Framework & Foundations”, „AI Capabilities and Limitations” | Anthropic | kursy online | 5–7 h | 0 zł | https://anthropic.skilljar.com |
| Dokumentacja Claude Code: „How Claude Code works”, „Explore the context window” | Anthropic | dokumentacja | 2–3 h | 0 zł | https://code.claude.com/docs/en/how-claude-code-works, https://code.claude.com/docs/en/context-window |
| Dokumentacja API: przegląd modeli, „Choosing a model”, okna kontekstu, „Reduce hallucinations” | Anthropic | dokumentacja | 2–3 h | 0 zł | https://platform.claude.com/docs/en/about-claude/models/choosing-a-model, https://platform.claude.com/docs/en/build-with-claude/context-windows, https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations |
| „How AI assistance impacts the formation of coding skills” (styczeń 2026) | Judy Hanwen Shen, Alex Tamkin (Anthropic) | badanie, artykuł | 1 h | 0 zł | https://www.anthropic.com/research/AI-assistance-coding-skills |

Szczególnie ważne: okno kontekstu jako główne ograniczenie, niedeterminizm i jego konsekwencja (jeden udany przebieg niczego nie dowodzi), halucynacje jako normalna cecha, a nie awaria, granica wiedzy modelu przy nowych wersjach frameworków; wniosek z badania Anthropic: osoby, które delegowały pisanie kodu i naprawę błędów, uczyły się wyraźnie słabiej niż te, które prosiły AI o wyjaśnienia, a największa różnica dotyczyła debugowania.

**Dowód:** krótka notatka (1–2 strony) dla siebie i do oferty: jak działa agent kodujący, czego nie widzi, kiedy halucynuje, który model do jakich zadań; plus 5 przypadków halucynacji lub błędów modelu zebranych z własnej pracy, każdy z opisem, jak go wykryto.

#### Etap 1: codzienna praca z Claude Code

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Kursy Anthropic Academy: „Claude Code 101”, „Claude Code in Action” | Anthropic | kursy online | 6–8 h | 0 zł | https://anthropic.skilljar.com |
| Dokumentacja Claude Code: Best practices, Common workflows | Anthropic | dokumentacja | 4–6 h | 0 zł | https://code.claude.com/docs/en/best-practices, https://code.claude.com/docs/en/common-workflows |
| Dokumentacja Claude Code: pamięć i `CLAUDE.md`, sesje, punkty kontrolne, tryb interaktywny | Anthropic | dokumentacja | 3–4 h | 0 zł | https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/sessions, https://code.claude.com/docs/en/checkpointing, https://code.claude.com/docs/en/interactive-mode |
| Dokumentacja Claude Code: worktree, konfiguracja modelu i poziomu wysiłku | Anthropic | dokumentacja | 2–3 h | 0 zł | https://code.claude.com/docs/en/worktrees, https://code.claude.com/docs/en/model-config |
| „Here’s how I use LLMs to help me write code” (marzec 2025) i tag „ai-assisted-programming” | Simon Willison | artykuł i blog | 3–4 h | 0 zł | https://simonwillison.net/2025/Mar/11/using-llms-for-code/, https://simonwillison.net/tags/ai-assisted-programming/ |

Szczególnie ważne: cykl eksploracja, plan, implementacja, commit; tryb planowania tylko tam, gdzie zmiany nie da się opisać jednym zdaniem; weryfikowalne kryteria ukończenia w poleceniu; `/clear` między zadaniami i nowa sesja po dwóch nieudanych poprawkach; `CLAUDE.md` krótki i przycinany, reguły, które muszą zadziałać zawsze, przeniesione do hooków (zob. sekcja 11); punkty kontrolne nie obejmują zmian zrobionych przez polecenia powłoki, więc git pozostaje siatką bezpieczeństwa.

**Dowód:** jedna funkcja w istniejącej aplikacji zrealizowana z Claude Code w cyklu eksploracja, plan, implementacja, commit, z zatwierdzonym przez człowieka planem, testami uruchomionymi przez agenta i notatką: ile poprawek wymagał wynik i dlaczego; do tego `CLAUDE.md` dla repozytorium testowego „przejmowanej” aplikacji (polecenia budowania i testów, pułapki, zakazy) przycięty po tygodniu pracy na podstawie tego, czego agent faktycznie nie przestrzegał.

#### Etap 2: Claude w aplikacji i pisanie promptów

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Prompt engineering: przegląd i „Prompting best practices” | Anthropic | dokumentacja | 3–4 h | 0 zł | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices |
| „Prompt engineering interactive tutorial” | Anthropic | kurs z ćwiczeniami | 6–8 h | 0 zł (zużycie API płatne) | https://github.com/anthropics/prompt-eng-interactive-tutorial |
| Centrum pomocy: „What are projects?”, „Using Research on Claude” | Anthropic | dokumentacja | 1–2 h | 0 zł | https://support.claude.com/en/articles/9517075-what-are-projects, https://support.claude.com/en/articles/11088861-using-research-on-claude |
| Kurs Anthropic Academy „AI Fluency for Small Businesses” | Anthropic | kurs online | 2–3 h | 0 zł | https://anthropic.skilljar.com |

Interaktywny samouczek powstał dla modeli Claude 3; tam, gdzie różni się od „Prompting best practices”, obowiązuje dokumentacja bieżąca.

Szczególnie ważne: jeden projekt na klienta, żeby kontekst jednego klienta nie mieszał się z innym; research jako punkt wyjścia, a nie źródło, więc każde twierdzenie w raporcie sprawdzone w źródle pierwotnym; szablony promptów do powtarzalnych dokumentów (raport z audytu, oferta, specyfikacja) przechowywane w repozytorium.

**Dowód:** szablon raportu z audytu przejmowanej aplikacji przygotowany z Claude w projekcie (struktura, skala oceny znalezisk, streszczenie dla zarządu), wypełniony dla aplikacji testowej; każdy fakt i odwołanie do normy (OWASP ASVS, CRA, RODO) sprawdzone ręcznie, z listą poprawek, które trzeba było wprowadzić po AI.

#### Etap 3: API Claude do automatyzacji własnej pracy

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Get started, klucze API, obszary robocze | Anthropic | dokumentacja | 2–3 h | 0 zł | https://platform.claude.com/docs/en/get-started, https://platform.claude.com/docs/en/get-api-key, https://platform.claude.com/docs/en/manage-claude/workspaces |
| Limity zapytań, liczenie tokenów, przetwarzanie wsadowe, Usage and Cost API | Anthropic | dokumentacja | 3–4 h | 0 zł | https://platform.claude.com/docs/en/api/rate-limits, https://platform.claude.com/docs/en/build-with-claude/token-counting, https://platform.claude.com/docs/en/build-with-claude/batch-processing, https://platform.claude.com/docs/en/manage-claude/usage-cost-api |
| Claude Code w trybie nieinteraktywnym (`claude -p`) | Anthropic | dokumentacja | 1–2 h | 0 zł | https://code.claude.com/docs/en/headless |
| Kurs Anthropic Academy „Claude Platform 101” i kurs „Anthropic API fundamentals” | Anthropic | kursy z ćwiczeniami | 5–7 h | 0 zł (zużycie API płatne) | https://anthropic.skilljar.com, https://github.com/anthropics/courses |

Szczególnie ważne: osobny obszar roboczy i klucz dla każdego zastosowania, limit wydatków na obszar, klucze w menedżerze sekretów; przetwarzanie wsadowe do zadań, które mogą poczekać; zasady z sekcji 4 tej ścieżki obowiązują także skrypty. Użycie API w aplikacjach klientów (tool use, prompt caching, streaming, pośrednik w backendzie) jest w sekcji 21.

**Dowód:** skrypt, który dla repozytorium klienta przygotowuje szkic inwentarza do audytu (streszczenia modułów, lista zależności i punktów wejścia) przez przetwarzanie wsadowe lub `claude -p`, z limitem wydatków na osobnym obszarze roboczym, kluczem poza repozytorium, filtrem plików z sekretami i danymi osobowymi oraz zapisem kosztu przebiegu.

#### Etap 4: dane klienta, RODO i umowy

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Dokumentacja Claude Code: Data usage, Legal and compliance, Zero data retention | Anthropic | dokumentacja | 2–3 h | 0 zł | https://code.claude.com/docs/en/data-usage, https://code.claude.com/docs/en/legal-and-compliance, https://code.claude.com/docs/en/zero-data-retention |
| Consumer Terms, Commercial Terms, Privacy Policy | Anthropic | warunki prawne | 3–4 h | 0 zł | https://www.anthropic.com/legal/consumer-terms, https://www.anthropic.com/legal/commercial-terms, https://www.anthropic.com/legal/privacy |
| Data Processing Addendum (z SCC) i lista podprocesorów | Anthropic | umowa, lista | 2–3 h | 0 zł | https://www.anthropic.com/legal/data-processing-addendum, https://trust.anthropic.com/subprocessors |
| Privacy Center: trenowanie na danych, okresy przechowywania, DPA dla produktów komercyjnych | Anthropic | dokumentacja | 1–2 h | 0 zł | https://privacy.claude.com, https://privacy.claude.com/en/articles/7996862 |
| Data residency w API | Anthropic | dokumentacja | 0,5 h | 0 zł | https://platform.claude.com/docs/en/build-with-claude/data-residency |
| Trust Center (certyfikaty, raporty) | Anthropic | dokumenty zgodności | 1 h | 0 zł | https://trust.anthropic.com |
| „AI Privacy Risks & Mitigations: Large Language Models (LLMs)” (kwiecień 2025) | Isabel Barbera, Support Pool of Experts EDPB | raport (nie stanowisko EDPB) | 3–4 h | 0 zł | https://www.edpb.europa.eu/our-work-tools/our-documents/support-pool-experts-projects/ai-privacy-risks-mitigations-large_en |

Stan na październik 2026 r. według dokumentacji Anthropic:

- **Plany konsumenckie (Free, Pro, Max)**, także przy pracy w Claude Code z tych kont, podlegają Consumer Terms. Dane są używane do trenowania modeli, jeśli użytkownik włączy to w ustawieniach prywatności; wtedy retencja wynosi do 5 lat, bez tej zgody 30 dni. Rozmowy oznaczone przez systemy bezpieczeństwa mogą być przechowywane dłużej (wejścia i wyjścia do 2 lat). DPA Anthropic dotyczy produktów komercyjnych, więc na planie konsumenckim nie ma umowy powierzenia z Anthropic.
- **Plany komercyjne (Team, Enterprise, API)** podlegają Commercial Terms: Anthropic domyślnie nie trenuje na danych, standardowa retencja to 30 dni, DPA ze standardowymi klauzulami umownymi (SCC) jest częścią warunków, a klient jest administratorem, Anthropic podmiotem przetwarzającym. Zero data retention jest dostępne tylko dla wybranych organizacji po uzgodnieniu z Anthropic.
- **Transfery poza EOG**: DPA opiera transfery na SCC; w API dostępne są regiony wnioskowania `global` i `us`, bez opcji UE.
- **Claude Code przechowuje lokalnie** transkrypcje sesji w `~/.claude/projects/` przez 30 dni (ustawienie `cleanupPeriodDays`), a polecenia `/feedback`, `/bug` i zgoda na udostępnienie transkrypcji w ankiecie wysyłają rozmowę z kodem do Anthropic.

Wniosek do weryfikacji z prawnikiem: plan Max założony w biznesplanie wystarcza do pracy na własnym kodzie i na materiałach bez danych osobowych, ale do pracy na repozytoriach i danych klientów, zwłaszcza zawierających dane osobowe, prawdopodobnie potrzebny będzie plan komercyjny (Team lub klucz API), żeby mieć umowę powierzenia z Anthropic jako dalszym podmiotem przetwarzającym i móc wpisać go do umowy z klientem. Dane, które nie mogą opuścić maszyny, zostają przy modelu lokalnym (zob. sekcja 20).

Szczególnie ważne: najpierw klasyfikacja danych, potem wybór narzędzia; zrzuty produkcyjnych baz i pliki `.env` nigdy do modelu w chmurze; zgoda klienta na podprocesora AI zapisana w umowie przed pierwszą sesją; regularne sprawdzanie ustawień prywatności konta i zmian w warunkach.

**Dowód:** „polityka danych dla AI” jako załącznik do oferty i wzoru umowy powierzenia: klasy danych klienta i dozwolone narzędzia dla każdej (Claude na planie komercyjnym, model lokalny, zakaz), podprocesorzy z odnośnikiem do listy Anthropic, podstawa transferu poza EOG, retencja, sposób anonimizacji danych testowych, procedura przy przypadkowym wysłaniu sekretu; dokument przejrzany przez prawnika, z listą zmian po przeglądzie.

#### Etap 5: koszty, limity i plan B

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Dokumentacja Claude Code: „Manage costs effectively”, Monitoring (OpenTelemetry) | Anthropic | dokumentacja | 2–3 h | 0 zł | https://code.claude.com/docs/en/costs, https://code.claude.com/docs/en/monitoring-usage |
| Centrum pomocy: limity planu Max | Anthropic | dokumentacja | 0,5 h | 0 zł | https://support.claude.com/en/articles/11014257-about-claude-s-max-plan-usage |
| Cennik planów i cennik API | Anthropic | strony cenowe | 1 h | 0 zł | https://claude.com/pricing, https://platform.claude.com/docs/en/about-claude/pricing |
| Dokumentacja Claude Code: bramki LLM | Anthropic | dokumentacja | 1–2 h | 0 zł | https://code.claude.com/docs/en/llm-gateway |
| Status usług | Anthropic | strona statusu | wg potrzeb | 0 zł | https://status.claude.com |

Szczególnie ważne: na planach subskrypcyjnych limity działają w oknach czasowych (sesyjnym i tygodniowym) wspólnych dla czatu i Claude Code, a przekroczenie można pokryć płatnymi kredytami z własnym limitem wydatków; `/usage` pokazuje zużycie planu i jego rozkład na skille, subagentów, pluginy i serwery MCP; zużycie najbardziej zawyżają długie sesje, chybienia cache po przerwie i wielu agentów równolegle; Anthropic nie wspiera kierowania Claude Code do modeli innych niż Claude, więc plan B to raczej przenośny proces (specyfikacje, testy, ewaluacje) niż ten sam przepływ na innym modelu.

**Dowód:** miesięczny raport kosztu AI: koszt planu i kredytów, zużycie według projektów i rodzajów zadań, koszt na zadanie dla trzech typowych zadań (audyt modułu, poprawka bezpieczeństwa, raport), udział w przychodzie względem progu 5% i decyzje na kolejny miesiąc; do tego jednostronicowy plan B: co robić przy awarii, wyczerpaniu limitu lub zmianie warunków (drugi dostawca przez bramkę, model lokalny, praca ręczna), sprawdzony w praktyce jednym dniem pracy bez Claude.

#### Etap 6: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Informacje o zmianach Claude Code („What’s new”, changelog) | Anthropic | źródła pierwotne | ok. 0,5 h tygodniowo | 0 zł | https://code.claude.com/docs/en/whats-new, https://code.claude.com/docs/en/changelog |
| Aktualności Anthropic i Privacy Center (zmiany warunków i retencji) | Anthropic | źródła pierwotne | wg potrzeb | 0 zł | https://www.anthropic.com/news, https://privacy.claude.com |
| Simon Willison’s Weblog | Simon Willison | blog | ok. 0,5 h tygodniowo | 0 zł | https://simonwillison.net |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **praca równoległa pod kontrolą:** 2–3 sesje w osobnych worktree przy jednym projekcie klienta, z zasadą, że żadna zmiana nie trafia do gałęzi głównej bez weryfikacji człowieka, i zapisem, przy ilu sesjach jakość weryfikacji zaczyna spadać,
- **pomiar własnej pracy:** co miesiąc koszt na zadanie, odsetek sesji przerwanych lub zaczętych od nowa i przyczyny; wnioski przenoszone do `CLAUDE.md`, szablonów promptów i do vicrafter (zob. sekcja 11),
- **przegląd warunków co kwartał:** ustawienia prywatności konta, Consumer i Commercial Terms, lista podprocesorów, limity planów; zmiany przenoszone do polityki danych dla AI w ofercie,
- **praca bez agenta:** raz w miesiącu zadanie wykonane samodzielnie, a w obszarach, których dopiero się uczysz, AI używane jako tutor (wyjaśnienia, pytania sprawdzające), a nie generator rozwiązań.

**Dowód poziomu E:** przejmujesz nieznaną aplikację klienta i w 1 dzień przeprowadzasz z Claude Code wstępny audyt na danych dopuszczonych polityką danych dla AI: przygotowujesz kontekst (`CLAUDE.md`, specyfikacja zadania), prowadzisz równoległe sesje, przerywasz te, które błądzą, a gotowy raport z audytu zawiera tylko zweryfikowane znaleziska, koszt AI tego dnia i informację, które dane i w jakim narzędziu były przetwarzane; potrafisz też wyjaśnić klientowi, dlaczego tak, a nie inaczej.

---

## 2. Języki i narzędzia podstawowe

*Warstwa 0: fundamenty. Opiera się na: —. Jest podstawą: wszystkich pozostałych sekcji, zwłaszcza 6, 9 i 11.*

Ta sekcja zbiera narzędzia, na których stoją wszystkie pozostałe: powłokę, Gita, formaty konfiguracji i podstawy sieci. Pozostałe języki mają ścieżki w sekcjach, w których się ich używa, żeby uczyć się ich dopiero wtedy, gdy są potrzebne.

| Język | Zastosowanie | Poziom | Ścieżka nauki |
|---|---|---|---|
| Rust | rdzeń aplikacji, backend, desktop, firmware, narzędzia CLI | E | 12.1 |
| TypeScript / JavaScript | React, Next.js, Node.js, warstwa UI w Tauri, większość przejmowanych projektów | E | 3.1 |
| SQL (PostgreSQL) | modele danych, migracje, zapytania, RLS | E | 4.1 |
| Bash, `jq` | hooki vicrafter, skrypty CI, automatyzacja | E | 2.1 |
| HTML, CSS | semantyka, dostępność, Tailwind | E | 3.1 |
| YAML, TOML, JSON Schema | konfiguracje CI, Cargo, kontrakty vicrafter | E | 2.1 |
| Swift | interfejs iOS i macOS, StoreKit, integracja rdzenia Rust | W, drobne poprawki samodzielnie | 19.1 |
| Kotlin | interfejs Android, Play Billing, integracja rdzenia Rust | W, drobne poprawki samodzielnie | 18.1 |
| C | FFI, SDK producentów układów, sterowniki, nagłówki systemowe | W | 12.2 i 22.1 |
| Python | projekty klientów, skrypty, narzędzia bezpieczeństwa, ewaluacja i dostrajanie modeli AI | W, przy rozwoju modeli E | 20.4 |
| PowerShell | budowanie i podpisywanie na Windows | W | 17.2 |
| C++, Java, Objective-C | starszy kod i biblioteki platformowe | czytanie | 12.2 |

- Linux z linii poleceń: procesy, uprawnienia, systemd, logi, SSH, podstawy administracji serwerem.
- Git na poziomie historii: rebase, bisect, worktree, podpisane commity, analiza zmian w cudzym repozytorium.
- Bash i `jq`: skrypty odporne na błędy, przetwarzanie JSON w hookach i CI.
- Formaty konfiguracji: YAML, TOML, JSON Schema jako kontrakty sprawdzane w CI.
- Sieci w praktyce: HTTP, DNS, TLS i certyfikaty, poczta transakcyjna (SPF, DKIM, DMARC).
- Typowe błędy kodu z AI do wyłapania: niecytowane zmienne i połykane kody błędów w skryptach, wymyślone flagi narzędzi, niejawne typy w YAML, nadmierne uprawnienia w workflow.

### 2.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 4 etapy. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przy doświadczeniu seniorskim etapy 0 i 2 można zwykle zaliczyć samym dowodem; etap 1 warto przejść w całości, bo hooki vicrafter i skrypty CI to kod, którego błędy psują cały proces. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | Linux, powłoka, Git, sieci | 50–70 h | podstawy |
| 1 | Bash i `jq` | 20–30 h | E |
| 2 | YAML, TOML, JSON Schema | 15–20 h | E |
| 3 | ekspert: recenzja skryptów i konfiguracji z AI, aktualność | stale, ok. 1 h tygodniowo | E |

Razem od zera do poziomu E: ok. 85–120 h, czyli 2–3 miesiące przy 10–12 h tygodniowo.

#### Etap 0: Linux, powłoka, Git, sieci

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Linux Command Line (siódme wydanie internetowe) | William Shotts | książka, od podstaw | 20–25 h | 0 zł (PDF) | https://linuxcommand.org/tlcl.php |
| The Missing Semester of Your CS Education (edycja 2026) | MIT | kurs z nagraniami | 12–15 h | 0 zł | https://missing.csail.mit.edu |
| Pro Git (wydanie 2) | Scott Chacon, Ben Straub | książka online | 8–10 h | 0 zł | https://git-scm.com/book/en/v2 |
| High Performance Browser Networking | Ilya Grigorik, O’Reilly | książka online, średni | 8–10 h | 0 zł online | https://hpbn.co |

Szczególnie ważne: uprawnienia i procesy, systemd i logi (`journalctl`), skrypty Bash odporne na błędy (`set -euo pipefail`, cytowanie zmiennych), DNS, TLS i certyfikaty, Git na poziomie historii (rebase, bisect, podpisane commity).

**Dowód:** serwer VPS postawiony od zera z linii poleceń: użytkownik bez roota, SSH tylko z kluczem, zapora, usługa systemd z prostą aplikacją (np. z sekcji 5), TLS, domena z poprawnymi rekordami DNS oraz SPF/DKIM/DMARC; wszystko opisane skryptem, który da się uruchomić ponownie.

#### Etap 1: Bash i `jq`

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| BashGuide i BashPitfalls | Greg’s Wiki (Wooledge) | przewodnik i katalog błędów | 6–8 h | 0 zł | https://mywiki.wooledge.org/BashGuide, https://mywiki.wooledge.org/BashPitfalls |
| Bash Reference Manual | GNU | dokumentacja | wg potrzeb | 0 zł | https://www.gnu.org/software/bash/manual/ |
| Shell Style Guide | Google | wytyczne | 1–2 h | 0 zł | https://google.github.io/styleguide/shellguide.html |
| ShellCheck i wiki z opisem reguł | Vidar Holen | narzędzie | 2–3 h | 0 zł | https://www.shellcheck.net |
| jq: Tutorial i Manual (jq 1.8) | jqlang | dokumentacja | 5–6 h | 0 zł | https://jqlang.org/tutorial/, https://jqlang.org/manual/ |

Szczególnie ważne: cytowanie zmiennych i rozdzielanie słów, `set -euo pipefail` i jego ograniczenia, kody wyjścia i potoki, `trap` do sprzątania, bezpieczne pliki tymczasowe, `jq -e` i `--arg` zamiast wklejania danych w filtr, różnice GNU i BSD (`sed -i`, `date`) przy runnerach macOS.

**Dowód:** hook vicrafter lub skrypt CI, który czyta JSON z wejścia przez `jq`, waliduje pola, zwraca właściwe kody wyjścia i przechodzi `shellcheck` bez wyjątków; zestaw testów (np. `bats`) uruchamiany na Linuksie i macOS.

#### Etap 2: YAML, TOML, JSON Schema

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| YAML 1.2.2 (rewizja z 2021 r.) | YAML Language Development Team | specyfikacja | 2–3 h (wybrane rozdziały) | 0 zł | https://yaml.org/spec/1.2.2/ |
| TOML v1.1.0 (grudzień 2025) | toml-lang | specyfikacja | 1 h | 0 zł | https://toml.io/en/v1.1.0 |
| Creating your first schema, Understanding JSON Schema, specyfikacja 2020-12 | JSON Schema | kurs i dokumentacja | 5–6 h | 0 zł | https://json-schema.org/learn/getting-started-step-by-step, https://json-schema.org/understanding-json-schema |
| Workflow syntax for GitHub Actions | GitHub | dokumentacja | 2–3 h | 0 zł | https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax |
| The Cargo Book: The Manifest Format | zespół Cargo | dokumentacja | 1–2 h | 0 zł | https://doc.rust-lang.org/cargo/reference/manifest.html |
| actionlint, zizmor, Taplo | rhysd, William Woodruff, Taplo | narzędzia: lint workflow, audyt bezpieczeństwa GitHub Actions, formatowanie i walidacja TOML | 2–3 h | 0 zł | https://github.com/rhysd/actionlint, https://docs.zizmor.sh, https://taplo.tamasfe.dev |

Szczególnie ważne: niejawne typy w YAML (np. `no`, `on` i liczby ósemkowe w parserach zgodnych z YAML 1.1), kotwice i scalanie, wieloliniowe łańcuchy; w JSON Schema `additionalProperties`, `oneOf` kontra `anyOf`, `$ref` i `$defs`, wersjonowanie schematów. W TOML 1.1 wieloliniowe tabele inline; przed użyciem sprawdzić, czy dany parser (np. Cargo, Taplo) obsługuje już tę wersję.

**Dowód:** schemat JSON Schema 2020-12 dla kontraktu vicrafter z testami poprawnych i błędnych dokumentów, walidowany w CI; workflow GitHub Actions bez ostrzeżeń `actionlint` i `zizmor` (przypięte akcje, minimalne `permissions`).

#### Etap 3: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Wiki ShellCheck (reguły SC) | Vidar Holen i społeczność | katalog błędów | wg potrzeb | 0 zł | https://www.shellcheck.net/wiki/ |
| Informacje o wydaniach Gita | projekt Git | źródło pierwotne | ok. 0,5 h na wydanie | 0 zł | https://git-scm.com/docs/git/RelNotes |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 20 zmian wygenerowanych przez agentów w Bashu i plikach konfiguracji, recenzowanych według listy kontrolnej (niecytowane zmienne, połykane kody błędów, nadmierne `permissions` w workflow, nieprzypięte akcje i zależności, wymyślone flagi narzędzi),
- **automatyzacja jako kod:** wszystkie skrypty i konfiguracje własnych projektów przechodzą lint i walidację schematem w CI,
- **analiza historii:** w każdym przejmowanym repozytorium `git log` i `git blame` jako źródło decyzji do odtworzenia w ADR.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz awarię skryptu CI lub hooka w Bashu w nieznanym projekcie i umiesz wyjaśnić przyczynę osobie nietechnicznej.

---

## 3. Frontend web

*Warstwa 0: fundamenty. Opiera się na: 2. Jest podstawą: 5, 7, 13, 14 i 21.*

- React: komponenty, hooki, stan, efekty i ich pułapki, renderowanie i memoizacja.
- Next.js (App Router): Server Components i Client Components, Server Actions, route handlers, middleware, strategie renderowania i cache, ISR, granica serwer–klient.
- TypeScript w trybie ścisłym, walidacja danych na granicach (Zod).
- Zarządzanie stanem i danymi: TanStack Query, Zustand albo Context; formularze (React Hook Form).
- Stylowanie i komponenty: Tailwind CSS, Radix lub shadcn/ui, design tokens.
- Internacjonalizacja, SEO, metadane, Core Web Vitals, rozmiar paczek, ładowanie obrazów i fontów.
- Bundlery i narzędzia: Turbopack lub Vite, pnpm, ESLint, Prettier.
- Opcjonalnie Rust w przeglądarce: `wasm-bindgen` (od 2025 r. w nowej organizacji `wasm-bindgen` na GitHubie), do ciężkich obliczeń.
- Typowe błędy kodu z AI do wyłapania: sekrety w zmiennych `NEXT_PUBLIC_*`, brak autoryzacji w Server Actions, logika uprawnień wyłącznie po stronie klienta.

### 3.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 8 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przy doświadczeniu seniorskim etapy 0–3 można zaliczyć samym dowodem i wracać do materiałów tylko tam, gdzie dowód nie wychodzi. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | jak działa web: HTML, CSS, przeglądarka, HTTP | 60–80 h | podstawy |
| 1 | JavaScript bez frameworka | 80–100 h | podstawy |
| 2 | TypeScript w trybie ścisłym | 40–60 h | W |
| 3 | React | 60–80 h | W |
| 4 | Next.js (App Router) i jego bezpieczeństwo | 50–70 h | W |
| 5 | ekosystem: dane, formularze, stylowanie, narzędzia | 40–50 h | W |
| 6 | jakość: testy, wydajność, dostępność, bezpieczeństwo | 60–80 h | E |
| 7 | ekspert: mechanizmy wewnętrzne, recenzja kodu AI, aktualność | stale, ok. 2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 400–500 h, czyli 8–12 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: jak działa web

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Learn web development | MDN (Mozilla) | kurs, od podstaw | 30–40 h | 0 zł | https://developer.mozilla.org/en-US/docs/Learn_web_development |
| Learn HTML, Learn CSS, Learn Forms | web.dev (Google) | kursy, podstawowy–średni | 20–25 h | 0 zł | https://web.dev/learn |
| CSS for JavaScript Developers | Josh W. Comeau | kurs interaktywny, średni | 30–40 h | płatny | https://css-for-js.dev |

**Dowód:** responsywna strona wielosekcyjna bez frameworka, z formularzem, poprawną semantyką i obsługą klawiatury; wynik Lighthouse powyżej 90 we wszystkich kategoriach.

#### Etap 1: JavaScript

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Modern JavaScript Tutorial | Ilya Kantor | podręcznik online, od podstaw do zaawansowanego | 40–50 h | 0 zł | https://javascript.info |
| Eloquent JavaScript (wydanie 4) | Marijn Haverbeke | książka z ćwiczeniami | 30–40 h | 0 zł online | https://eloquentjavascript.net |
| You Don’t Know JS Yet | Kyle Simpson | książki, średni–zaawansowany | 15–20 h | 0 zł | https://github.com/getify/You-Dont-Know-JS |

Szczególnie ważne: domknięcia, zakresy, `this`, prototypy, pętla zdarzeń, `Promise` i `async`/`await`, moduły ES, niemutowalność, obsługa błędów.

**Dowód:** aplikacja w czystym JavaScript pobierająca dane z publicznego API, z obsługą błędów sieci, anulowaniem żądań (`AbortController`) i stanami ładowania.

#### Etap 2: TypeScript

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| TypeScript Handbook | Microsoft | dokumentacja, podstawowy–średni | 10–15 h | 0 zł | https://www.typescriptlang.org/docs/handbook/ |
| Total TypeScript (darmowe tutoriale i płatne warsztaty) | Matt Pocock | kurs z ćwiczeniami, średni–zaawansowany | 20–30 h | 0 zł / płatny | https://www.totaltypescript.com |
| Effective TypeScript (wydanie 2) | Dan Vanderkam, O’Reilly | książka, zaawansowany | 12–15 h | płatna | https://effectivetypescript.com |
| type-challenges | społeczność | ćwiczenia z systemu typów | wg potrzeb | 0 zł | https://github.com/type-challenges/type-challenges |

**Dowód:** klient API w trybie `strict`, bez `any`, z typami wyprowadzonymi ze schematów Zod i dyskryminowanymi uniami dla stanów odpowiedzi.

#### Etap 3: React

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| react.dev: Learn i Reference (w całości, z artykułem „You Might Not Need an Effect”) | zespół React | dokumentacja z ćwiczeniami | 20–25 h | 0 zł | https://react.dev/learn |
| The Joy of React | Josh W. Comeau | kurs interaktywny, od podstaw do średniego | 30–40 h | płatny | https://www.joyofreact.com |
| Epic React | Kent C. Dodds | warsztaty, średni–zaawansowany | 40–60 h | płatny | https://www.epicreact.dev |
| overreacted.io | Dan Abramov | artykuły, zaawansowany | 5–10 h | 0 zł | https://overreacted.io |

Wystarczy jeden z dwóch płatnych kursów: The Joy of React przy starcie od zera, Epic React przy doświadczeniu z Reactem.

**Dowód:** aplikacja z formularzami, listą z filtrowaniem, stanem współdzielonym i własnymi hookami, bez zbędnych `useEffect`; komponenty dostępne z klawiatury.

#### Etap 4: Next.js (App Router)

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Next.js Learn (kurs budowy dashboardu) | Vercel | kurs praktyczny, podstawowy–średni | 10–15 h | 0 zł | https://nextjs.org/learn |
| Dokumentacja Next.js: renderowanie, cache, Server Actions, middleware, przewodnik o bezpieczeństwie danych | Vercel | dokumentacja | 15–20 h | 0 zł | https://nextjs.org/docs |
| „How to Think About Security in Next.js” | Sebastian Markbåge, Vercel | artykuł, zaawansowany | 1–2 h | 0 zł | https://nextjs.org/blog/security-nextjs-server-components-actions |
| Komunikaty bezpieczeństwa React i Next.js, m.in. krytyczna podatność RCE w React Server Components (CVE-2025-55182, „React2Shell”, grudzień 2025) | zespół React, Vercel | komunikaty, studium przypadku | 2–3 h | 0 zł | https://react.dev/blog |

Szczególnie ważne: granica serwer–klient, warstwa dostępu do danych (DAL) z autoryzacją w każdej akcji, które zmienne trafiają do przeglądarki, strategie cache i ich unieważnianie, aktualizacja frameworka jako element obsługi podatności (CRA).

**Dowód:** aplikacja z logowaniem, rolami i Server Actions, w której każda akcja sprawdza uprawnienia po stronie serwera; test, który próbuje wywołać akcję bez uprawnień i dostaje odmowę.

#### Etap 5: ekosystem

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| TanStack Query: dokumentacja i blog „Practical React Query” | TanStack, Dominik Dorfmeister (TkDodo) | dokumentacja i artykuły | 8–10 h | 0 zł | https://tanstack.com/query, https://tkdodo.eu/blog/practical-react-query |
| Zod, React Hook Form, Zustand | autorzy bibliotek | dokumentacja | 6–8 h | 0 zł | https://zod.dev, https://react-hook-form.com, https://zustand.docs.pmnd.rs |
| Tailwind CSS, Radix Primitives, shadcn/ui | autorzy bibliotek | dokumentacja | 8–10 h | 0 zł | https://tailwindcss.com/docs, https://www.radix-ui.com/primitives, https://ui.shadcn.com |
| next-intl | Jan Amann | dokumentacja | 3–4 h | 0 zł | https://next-intl.dev |
| Vite, pnpm, typescript-eslint | autorzy narzędzi | dokumentacja | 5–6 h | 0 zł | https://vite.dev, https://pnpm.io, https://typescript-eslint.io |
| patterns.dev | Lydia Hallie, Addy Osmani | książka online, średni–zaawansowany | 8–10 h | 0 zł | https://www.patterns.dev |
| Rust i WebAssembly: `wasm-bindgen` i przewodnik MDN o WebAssembly | zespół wasm-bindgen, MDN | dokumentacja (opcjonalnie) | 8–10 h | 0 zł | https://github.com/wasm-bindgen/wasm-bindgen, https://developer.mozilla.org/en-US/docs/WebAssembly |

Uwaga do Rusta w przeglądarce: organizacja `rustwasm` została zarchiwizowana we wrześniu 2025 r., `wasm-bindgen` przeszedł do nowej organizacji, a `wasm-pack` trafił na listę do archiwizacji. Starsze poradniki oparte na `wasm-pack` trzeba sprawdzać pod kątem aktualności.

**Dowód:** aplikacja wielojęzyczna z formularzem walidowanym tym samym schematem Zod na kliencie i serwerze, cache danych z optymistycznymi aktualizacjami i własnym komponentem dostępnym zbudowanym na Radix.

#### Etap 6: jakość

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Testing Library, Vitest, MSW | autorzy narzędzi | dokumentacja | 8–10 h | 0 zł | https://testing-library.com, https://vitest.dev, https://mswjs.io |
| Playwright (testy E2E, fixtures, trace viewer) | Microsoft | dokumentacja | 8–10 h | 0 zł | https://playwright.dev |
| Testing JavaScript | Kent C. Dodds | kurs, średni | 15–20 h | płatny | https://www.testingjavascript.com |
| Learn Performance, Core Web Vitals | web.dev (Google) | kurs | 8–10 h | 0 zł | https://web.dev/learn/performance |
| Chrome DevTools: Performance, Memory, Network | Google | dokumentacja | 4–6 h | 0 zł | https://developer.chrome.com/docs/devtools |
| Learn Accessibility | web.dev (Google) | kurs | 6–8 h | 0 zł | https://web.dev/learn/accessibility |
| ARIA Authoring Practices Guide, Understanding WCAG 2.2 | W3C WAI | wzorce i norma | 8–10 h | 0 zł | https://www.w3.org/WAI/ARIA/apg/, https://www.w3.org/WAI/WCAG22/Understanding/ |
| OWASP Cheat Sheet Series: XSS, CSP, CSRF, uwierzytelnianie, sesje | OWASP | ściągawki | 6–8 h | 0 zł | https://cheatsheetseries.owasp.org |

**Dowód:** do aplikacji z etapu 4 dodane: testy jednostkowe, komponentów i E2E w CI; budżet wydajności (LCP, INP, CLS) sprawdzany automatycznie; audyt WCAG 2.2 AA z poprawkami i testem czytnikiem ekranu; nagłówki bezpieczeństwa i CSP.

#### Etap 7: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Build your own React | Rodrigo Pombo | samouczek, zaawansowany | 4–6 h | 0 zł | https://pomb.us/build-your-own-react/ |
| Blog React, informacje o wydaniach Next.js, dyskusje i RFC na GitHubie | zespół React, Vercel | źródła pierwotne | ok. 1 h tygodniowo | 0 zł | https://react.dev/blog, https://nextjs.org/blog |
| Kursy zaawansowane (wydajność, architektura frontendu, wewnętrzne mechanizmy) | Frontend Masters | platforma kursów | wg potrzeb | abonament | https://frontendmasters.com |
| Nagrania konferencji React Conf i Next.js Conf | Meta, Vercel | wystąpienia | wg potrzeb | 0 zł | YouTube |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 20 pull requestów wygenerowanych przez agentów, recenzowanych według listy kontrolnej z etapów 4 i 6 (autoryzacja w akcjach, `NEXT_PUBLIC_*`, zbędne efekty, dostępność, testy, które naprawdę coś sprawdzają),
- **przejęcie cudzej aplikacji Next.js:** pierwsza aplikacja z vibe codingu (poligon B z mapy nauki) przeprowadzona przez pełny audyt i stabilizację,
- **śledzenie podatności:** subskrypcja komunikatów bezpieczeństwa React i Next.js oraz ćwiczenie aktualizacji frameworka w 24 h,
- **wkład w open source** w jednej bibliotece z ekosystemu, choćby w dokumentację lub testy.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz błąd wydajności lub bezpieczeństwa w nieznanej aplikacji Next.js i umiesz wyjaśnić przyczynę osobie nietechnicznej.

---

## 4. Bazy danych i dane

*Warstwa 1: dane i serwer. Opiera się na: 2. Jest podstawą: 5, 8, 14, 18, 19 i 22 (dane lokalne).*

- PostgreSQL: modelowanie, indeksy i plany zapytań (`EXPLAIN ANALYZE`), transakcje i poziomy izolacji, ograniczenia integralności, Row-Level Security.
- SQLite lokalnie na desktopie, mobile i w trybie offline; synchronizacja i rozwiązywanie konfliktów.
- Redis lub podobny cache, kolejki.
- Migracje expand–contract, kopie zapasowe z testem odtworzenia, retencja i usuwanie danych (RODO).

### 4.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 8 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przy doświadczeniu seniorskim etapy 0–1 można zaliczyć samym dowodem i wracać do materiałów tylko tam, gdzie dowód nie wychodzi. Dostęp do bazy z Rusta (SQLx, SeaORM) jest w sekcji 5, a szyfrowanie i ochrona sekretów w sekcji 10. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | SQL i modelowanie relacyjne | 50–70 h | podstawy |
| 1 | PostgreSQL w praktyce: typy, ograniczenia, indeksy, plany zapytań | 50–60 h | W |
| 2 | transakcje, izolacja, blokady i Row-Level Security | 30–40 h | E |
| 3 | SQLite lokalnie, local-first i synchronizacja | 40–50 h | W |
| 4 | Redis i cache | 15–20 h | W |
| 5 | migracje bez przestojów (expand–contract) | 15–20 h | E |
| 6 | kopie zapasowe, PITR, retencja i RODO w danych | 30–40 h | E |
| 7 | ekspert: wnętrze PostgreSQL, recenzja kodu AI, aktualność | stale, ok. 2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 230–300 h, czyli 5–7 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: SQL i modelowanie

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Dokumentacja PostgreSQL: część I „Tutorial” i rozdziały o zapytaniach, typach i DDL | PostgreSQL Global Development Group | dokumentacja (wersja 18) | 15–20 h | 0 zł | https://www.postgresql.org/docs/current/ |
| PostgreSQL Exercises | Alisdair Owens | ćwiczenia interaktywne, od podstaw do zaawansowanego | 10–15 h | 0 zł | https://pgexercises.com |
| Modern SQL | Markus Winand | artykuły: CTE, `WITH RECURSIVE`, funkcje okna, `FILTER`, `LATERAL` | 5–8 h | 0 zł | https://modern-sql.com |
| SQL Antipatterns, Volume 1 | Bill Karwin, Pragmatic Bookshelf | książka, średni | 12–15 h | płatna | https://pragprog.com/titles/bksap1/sql-antipatterns-volume-1/ |
| Intro to Database Systems (CMU 15-445/645) | Andy Pavlo, Carnegie Mellon University | kurs uniwersytecki (opcjonalnie, dla podstaw teoretycznych) | 20–30 h wybranych wykładów | 0 zł | https://15445.courses.cs.cmu.edu |

Szczególnie ważne: normalizacja i świadoma denormalizacja, klucze naturalne i sztuczne, `NULL` i logika trójwartościowa, złączenia, agregacje, funkcje okna, CTE, antywzorce z książki Karwina (EAV, listy w kolumnie, polimorficzne klucze obce).

**Dowód:** model danych dla aplikacji abonamentowej z wielodostępnością (najemcy, użytkownicy, role, abonamenty, faktury, zdarzenia płatności) z kluczami obcymi i ograniczeniami; 15 zapytań raportowych, w tym z funkcjami okna; krótka notatka, które antywzorce świadomie ominięto.

#### Etap 1: PostgreSQL w praktyce

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Art of PostgreSQL (wydanie 2, aktualizacja 2026 dla PostgreSQL 10–18) | Dimitri Fontaine | książka, średni–zaawansowany | 20–25 h | płatna | https://theartofpostgresql.com |
| Use The Index, Luke (darmowe wydanie online książki „SQL Performance Explained”) | Markus Winand | książka online, średni | 10–12 h | 0 zł | https://use-the-index-luke.com |
| Dokumentacja PostgreSQL: rozdziały „Indexes” i „Performance Tips” (`EXPLAIN`, statystyki planisty) | PostgreSQL Global Development Group | dokumentacja | 8–10 h | 0 zł | https://www.postgresql.org/docs/current/using-explain.html |
| explain.depesz.com, explain.dalibo.com | Hubert „depesz” Lubaczewski, Dalibo | narzędzia do analizy planów | wg potrzeb | 0 zł | https://explain.depesz.com, https://explain.dalibo.com |
| Postgres Playground: samouczki w przeglądarce (indeksy, partycjonowanie, RLS, analiza wydajności) | Crunchy Data | ćwiczenia interaktywne | 5–8 h | 0 zł | https://www.crunchydata.com/developers/tutorials |

Szczególnie ważne: czytanie `EXPLAIN (ANALYZE, BUFFERS)`, indeksy wielokolumnowe i kolejność kolumn, indeksy częściowe i wyrażeniowe, GIN dla `jsonb`, `CHECK` i ograniczenia wykluczające, kiedy `jsonb` zamiast tabeli, a kiedy nie. Plany zapytań z danymi klienta wklejaj do narzędzi online tylko po anonimizacji albo używaj lokalnej wersji explain.dalibo.com.

**Dowód:** baza z etapu 0 wypełniona milionem wierszy danych syntetycznych; pięć wolnych zapytań przyspieszonych co najmniej dziesięciokrotnie, każde z planem przed i po oraz wyjaśnieniem, dlaczego indeks lub przepisanie zapytania zadziałało.

#### Etap 2: transakcje, izolacja i RLS

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Dokumentacja PostgreSQL: „Concurrency Control” (izolacja transakcji, blokady jawne, blokady doradcze) | PostgreSQL Global Development Group | dokumentacja | 6–8 h | 0 zł | https://www.postgresql.org/docs/current/mvcc.html |
| Dokumentacja PostgreSQL: „Row Security Policies” | PostgreSQL Global Development Group | dokumentacja | 2–3 h | 0 zł | https://www.postgresql.org/docs/current/ddl-rowsecurity.html |
| Hermitage: testy anomalii izolacji w różnych bazach | Martin Kleppmann i współtwórcy | testy i opis | 3–4 h | 0 zł | https://github.com/ept/hermitage |
| Modele spójności (mapa i opisy anomalii) | Jepsen | materiał referencyjny, zaawansowany | 3–4 h | 0 zł | https://jepsen.io/consistency |
| Rozdział o transakcjach w „Designing Data-Intensive Applications” (zob. sekcja 5, etap 8) | Martin Kleppmann, Chris Riccomini, O’Reilly | książka | 4–6 h | płatna | zob. sekcja 5 |

Szczególnie ważne: domyślny `READ COMMITTED` i utracone aktualizacje, `SELECT … FOR UPDATE` i `SKIP LOCKED`, `SERIALIZABLE` z ponawianiem transakcji, zakleszczenia i stała kolejność blokad, długie transakcje blokujące `VACUUM`; w RLS polityki `USING` i `WITH CHECK`, `FORCE ROW LEVEL SECURITY`, role omijające RLS (`BYPASSRLS`, właściciel tabeli), wydajność funkcji w politykach.

**Dowód:** test współbieżności, który dwiema równoległymi transakcjami odtwarza utraconą aktualizację salda lub podwójną rezerwację, a następnie pokazuje dwie poprawki (blokada wiersza oraz `SERIALIZABLE` z ponawianiem); izolacja najemców przez RLS z testem, który jako użytkownik jednego najemcy próbuje czytać i zapisywać dane innego.

#### Etap 3: SQLite, local-first i synchronizacja

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Dokumentacja SQLite: „Isolation In SQLite”, „Write-Ahead Logging”, „STRICT Tables”, „How SQLite Implements Atomic Commit” | SQLite | dokumentacja | 6–8 h | 0 zł | https://www.sqlite.org/docs.html |
| `rusqlite` (albo SQLx z SQLite, zob. sekcja 5) | autorzy biblioteki | dokumentacja | 3–4 h | 0 zł | https://docs.rs/rusqlite |
| „Local-first software: You own your data, in spite of the cloud” | Martin Kleppmann, Adam Wiggins, Peter van Hardenberg, Mark McGranaghan, Ink & Switch | esej, średni | 2–3 h | 0 zł | https://www.inkandswitch.com/essay/local-first/ |
| Automerge 3 (rdzeń w Ruście, wiązania JavaScript przez WebAssembly) | Ink & Switch i społeczność | dokumentacja | 6–8 h | 0 zł | https://automerge.org |
| Yjs i jego port do Rusta `yrs` | Kevin Jahns i społeczność | dokumentacja | 4–6 h | 0 zł | https://docs.yjs.dev, https://github.com/y-crdt/y-crdt |
| Loro (CRDT w Ruście z wiązaniami JS, Swift, Python) | Loro | dokumentacja (opcjonalnie) | 3–4 h | 0 zł | https://loro.dev |
| Silniki synchronizacji PostgreSQL–SQLite: PowerSync (SDK w Ruście w wersji beta), Electric | PowerSync, Electric | dokumentacja (opcjonalnie) | 4–6 h | 0 zł | https://docs.powersync.com, https://electric.ax/docs/intro |

Uwaga do CRDT w SQLite: `cr-sqlite` (vlcn) nie wydał nowej wersji od stycznia 2024 r., a ostatnie zmiany w repozytorium pochodzą z 2024 r. Do nowych projektów lepiej wybrać aktywnie rozwijane rozwiązanie: CRDT na poziomie dokumentu (Automerge, Yjs/`yrs`, Loro) zapisywane w SQLite albo silnik synchronizacji (PowerSync, Electric). Stan tych narzędzi trzeba sprawdzać przed decyzją, bo obszar szybko się zmienia.

Szczególnie ważne: SQLite w trybie WAL, `BEGIN IMMEDIATE` przy zapisie, typy w tabelach `STRICT`, migracje schematu na urządzeniu użytkownika, wybór strategii konfliktów (ostatni zapis wygrywa, scalanie CRDT, rozstrzyganie przez serwer), uprawnienia do danych synchronizowanych na urządzenie, usuwanie danych także z kopii lokalnych.

**Dowód:** prosta aplikacja notatek w Tauri z rdzeniem w Ruście: SQLite lokalnie, praca offline, synchronizacja między dwoma urządzeniami przez Automerge lub `yrs`; test, w którym oba urządzenia edytują ten sam dokument offline, a po połączeniu stan jest identyczny i nic nie ginie; zapisana w ADR decyzja o strategii konfliktów.

#### Etap 4: Redis i cache

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Dokumentacja Redis: typy danych, wygasanie kluczy, Streams, trwałość, Pub/Sub | Redis | dokumentacja | 8–10 h | 0 zł | https://redis.io/docs/latest/develop/ |
| Valkey (otwarty fork Redis na licencji BSD pod Linux Foundation) | Valkey | dokumentacja | 2–3 h | 0 zł | https://valkey.io |
| Crate `redis` (lub `fred`) | autorzy bibliotek | dokumentacja | 2–3 h | 0 zł | https://docs.rs/redis |

Uwaga do licencji: Redis od wersji 8 (maj 2025 r.) jest ponownie dostępny na licencji open source (AGPLv3 jako jedna z opcji), a Valkey powstał w 2024 r. jako fork na licencji BSD. Przy wdrożeniu u klienta trzeba sprawdzić, która wersja i licencja są używane.

Szczególnie ważne: cache-aside i unieważnianie, czas życia kluczy, lawina odświeżeń (stampede), ograniczanie liczby żądań, Redis jako pośrednik kolejki a ryzyko utraty danych, kiedy wystarczy PostgreSQL (kolejka z `SKIP LOCKED`, zob. sekcja 5), dane osobowe w cache i ich wygasanie.

**Dowód:** cache odczytów i limiter żądań w usłudze z sekcji 5 na Redis lub Valkey; test, który pokazuje poprawne unieważnienie po zapisie, ochronę przed lawiną odświeżeń i działanie usługi przy niedostępnym Redisie.

#### Etap 5: migracje bez przestojów

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| „Parallel Change” (expand–contract) | Danilo Sato, martinfowler.com | artykuł | 1 h | 0 zł | https://martinfowler.com/bliki/ParallelChange.html |
| Dokumentacja PostgreSQL: „Explicit Locking” i poziomy blokad poleceń `ALTER TABLE`, `CREATE INDEX CONCURRENTLY` | PostgreSQL Global Development Group | dokumentacja | 4–5 h | 0 zł | https://www.postgresql.org/docs/current/explicit-locking.html |
| pgroll: migracje odwracalne z wieloma wersjami schematu naraz | Xata | narzędzie i dokumentacja (opcjonalnie) | 3–4 h | 0 zł | https://github.com/xataio/pgroll |
| Migracje w SQLx (`sqlx migrate`) lub w SeaORM (zob. sekcja 5) | LaunchBadge, SeaQL | dokumentacja | 2 h | 0 zł | https://docs.rs/sqlx/latest/sqlx/macro.migrate.html |

Szczególnie ważne: każda zmiana w trzech krokach (dodanie, przeniesienie danych i podwójny zapis, usunięcie starego) rozłożonych na osobne wydania, `lock_timeout` przy migracjach, indeksy tworzone `CONCURRENTLY`, wypełnianie danych partiami, ograniczenia dodawane jako `NOT VALID` i walidowane osobno, migracja zgodna wstecz z poprzednią wersją aplikacji, na wypadek wycofania wydania.

**Dowód:** zmiana nazwy i typu kolumny w tabeli z milionem wierszy przeprowadzona metodą expand–contract w trzech wydaniach, podczas ciągłego obciążenia testowego, bez błędów po stronie klientów; wycofanie środkowego wydania bez utraty danych.

#### Etap 6: kopie, PITR, retencja i RODO

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Dokumentacja PostgreSQL: „Backup and Restore”, w tym „Continuous Archiving and Point-in-Time Recovery (PITR)” | PostgreSQL Global Development Group | dokumentacja | 6–8 h | 0 zł | https://www.postgresql.org/docs/current/continuous-archiving.html |
| pgBackRest User Guide | pgBackRest | dokumentacja | 6–8 h | 0 zł | https://pgbackrest.org/user-guide.html |
| WAL-G | społeczność WAL-G | dokumentacja (alternatywa) | 3–4 h | 0 zł | https://github.com/wal-g/wal-g |
| RODO, tekst rozporządzenia 2016/679 (zwłaszcza art. 5, 17, 25, 30, 32, 33) | Unia Europejska | akt prawny | 4–6 h | 0 zł | https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:32016R0679 |
| GDPR developer’s guide | CNIL | przewodnik dla programistów | 4–5 h | 0 zł | https://www.cnil.fr/en/gdpr-developers-guide |
| Wytyczne 4/2019 w sprawie art. 25: uwzględnianie ochrony danych w fazie projektowania i domyślna ochrona danych | Europejska Rada Ochrony Danych (EROD) | wytyczne | 2–3 h | 0 zł | https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-42019-article-25-data-protection-design-and_en |

Uwaga do pgBackRest: w kwietniu 2026 r. dotychczasowy opiekun ogłosił koniec utrzymania projektu, a w maju 2026 r. projekt wznowiono dzięki finansowaniu przez grupę sponsorów; kolejne wydania z serii 2.59 ukazały się od lipca do października 2026 r. Przy wyborze narzędzia trzeba sprawdzić jego stan i mieć opanowaną alternatywę (WAL-G albo wbudowane `pg_basebackup` z archiwizacją WAL).

Szczególnie ważne: RPO i RTO zapisane dla każdej aplikacji, kopia, której odtworzenia nie przetestowano, nie istnieje, kopie zaszyfrowane i poza kontem produkcyjnym, retencja kopii a prawo do usunięcia danych (dane usunięte z bazy żyją w kopiach do końca ich retencji, co trzeba opisać w polityce), pseudonimizacja danych w środowiskach testowych, rejestr czynności przetwarzania, minimalizacja danych w logach i zdarzeniach.

**Dowód:** PITR skonfigurowany dla bazy z poprzednich etapów, comiesięczny automatyczny test odtworzenia do wskazanej chwili z pomiarem czasu (RTO) i utraty danych (RPO), zapisany jako runbook; mapa danych osobowych jednej aplikacji (tabele, kopie, logi, cache, urządzenia) z okresami retencji i procedurą usunięcia na żądanie, przetestowaną od początku do końca.

#### Etap 7: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| PostgreSQL 14 Internals (MVCC, `VACUUM`, WAL, blokady, planista, typy indeksów) | Egor Rogov, Postgres Professional | książka, zaawansowany | 25–30 h | 0 zł (PDF) | https://postgrespro.com/community/books/internals |
| Dokumentacja PostgreSQL: informacje o wydaniach i rozdział o `VACUUM` i autovacuum | PostgreSQL Global Development Group | źródła pierwotne | ok. 1 h tygodniowo | 0 zł | https://www.postgresql.org/docs/release/ |
| Designing Data-Intensive Applications (wydanie 2, rozdziały o replikacji, partycjonowaniu i spójności) | Martin Kleppmann, Chris Riccomini, O’Reilly | książka (zob. sekcja 5, etap 8) | 10–15 h | płatna | zob. sekcja 5 |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 20 pull requestów z migracjami, zapytaniami i politykami RLS wygenerowanymi przez agentów, recenzowanych według listy kontrolnej z etapów 1, 2 i 5 (blokujące migracje, brak indeksu pod nowy filtr, zapytania N+1, transakcje obejmujące wywołania sieciowe, polityki RLS bez `WITH CHECK`, dane osobowe w logach i seedach, testy na SQLite zamiast na prawdziwym PostgreSQL),
- **przejęcie cudzej bazy:** audyt bazy jednej aplikacji z vibe codingu (zwykle Supabase): tabele bez RLS, brakujące indeksy i ograniczenia, brak kopii z testem odtworzenia; raport z priorytetami i poprawki jako migracje,
- **ćwiczenie awarii:** odtworzenie bazy po symulowanym usunięciu tabeli i po utracie serwera, z pomiarem czasu, raz na kwartał,
- **monitorowanie:** `pg_stat_statements`, rozrost tabel i indeksów, opóźnienie autovacuum, długie transakcje; alerty w obserwowalności (zob. sekcja 9).

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz w nieznanej bazie PostgreSQL problem wydajności, blokad albo wycieku danych między najemcami, przygotowujesz bezpieczną migrację naprawczą i umiesz wyjaśnić przyczynę osobie nietechnicznej.

---

## 5. Backend i API

*Warstwa 1: dane i serwer. Opiera się na: 3 i 4; części w Ruście dochodzą po sekcji 12. Jest podstawą: 6, 7, 8, 9, 10 i 21.*

- Rust: Axum, Tower (middleware), Tokio, SQLx lub SeaORM, kolejki i zadania w tle.
- Node.js po stronie serwera Next.js i w przejmowanych projektach.
- Kontrakty API: REST z OpenAPI (np. generowane z kodu przez `utoipa`), opcjonalnie gRPC (`tonic`); wersjonowanie, idempotencja, paginacja, limity, spójne błędy.
- Uwierzytelnianie i autoryzacja: OAuth 2.0 / OIDC, sesje, ciasteczka, pułapki JWT, kontrola dostępu do obiektów, wielodostępność.
- Integracje: webhooki z weryfikacją podpisu, outbox, idempotentni konsumenci, poczta transakcyjna, przechowywanie plików (S3).
- Płatności i licencje: Stripe, pośrednik Merchant of Record, klucze licencyjne, StoreKit 2, Google Play Billing.
- Platformy klientów: Supabase (RLS, Edge Functions, klucze), Firebase (reguły bezpieczeństwa), Vercel, Fly.io.

### 5.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 9 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przy doświadczeniu seniorskim w TypeScript i Node.js etapy 0–1 można zaliczyć samym dowodem i wracać do materiałów tylko tam, gdzie dowód nie wychodzi. Podstawy Rusta są w sekcji 12, bazy danych w sekcji 4, testy w sekcji 6, a bezpieczeństwo API w sekcji 10; tu są tylko elementy właściwe dla backendu. Czas podany dla osoby startującej od zera (przy etapach 2–3 od zera w backendzie, ze znajomością Rusta z sekcji 12); ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | HTTP i REST: semantyka, kody, cache, błędy | 30–40 h | podstawy |
| 1 | Node.js po stronie serwera | 40–60 h | W |
| 2 | backend w Ruście: Tokio, Axum, Tower | 80–100 h | W |
| 3 | dostęp do danych z Rusta: SQLx, SeaORM | 25–35 h | W |
| 4 | kontrakty API: OpenAPI (`utoipa`), gRPC, wytyczne projektowe | 40–50 h | W |
| 5 | uwierzytelnianie i autoryzacja: OAuth 2.0, OIDC, sesje | 50–60 h | E |
| 6 | integracje i niezawodność: webhooki, outbox, kolejki, idempotencja | 40–50 h | E |
| 7 | płatności i platformy klientów: Stripe, Merchant of Record, Supabase, Firebase | 40–50 h | E |
| 8 | ekspert: systemy rozproszone, recenzja kodu AI, aktualność | stale, ok. 2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 350–450 h, czyli 8–10 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: HTTP i REST

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| HTTP: przewodniki (przegląd, cache, CORS, ciasteczka, nagłówki, kody odpowiedzi) | MDN (Mozilla) | dokumentacja, od podstaw | 15–20 h | 0 zł | https://developer.mozilla.org/en-US/docs/Web/HTTP |
| RFC 9110 „HTTP Semantics” (metody, bezpieczeństwo i idempotencja metod, kody, negocjacja treści, żądania warunkowe) | IETF | norma | 8–10 h | 0 zł | https://datatracker.ietf.org/doc/rfc9110/ |
| RFC 9111 „HTTP Caching” | IETF | norma | 3–4 h | 0 zł | https://datatracker.ietf.org/doc/rfc9111/ |
| RFC 9457 „Problem Details for HTTP APIs” | IETF | norma | 1–2 h | 0 zł | https://datatracker.ietf.org/doc/rfc9457/ |

Szczególnie ważne: które metody są bezpieczne i idempotentne, `ETag` i żądania warunkowe (`If-Match`) jako ochrona przed utratą zapisu, różnica 401 i 403, 404 zamiast 403 przy ukrywaniu istnienia obiektu, spójny format błędów.

**Dowód:** prosty serwer HTTP bez frameworka (Node.js `http` albo `hyper`), który obsługuje `GET`, `PUT` z `If-Match`, zwraca błędy w formacie RFC 9457 i poprawne nagłówki cache; zestaw wywołań `curl` pokazujący każdy przypadek.

#### Etap 1: Node.js po stronie serwera

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Learn Node.js: pętla zdarzeń, „Don’t Block the Event Loop”, strumienie i backpressure, wbudowany test runner, diagnostyka, dobre praktyki bezpieczeństwa | Node.js (OpenJS Foundation) | dokumentacja | 12–15 h | 0 zł | https://nodejs.org/en/learn |
| Node.js Design Patterns (wydanie 4, Node.js 24) | Mario Casciaro, Luciano Mammino, Packt | książka, średni–zaawansowany | 25–35 h | płatna | https://www.nodejsdesignpatterns.com |
| Dokumentacja API Node.js: `http`, `stream`, `worker_threads`, `AsyncLocalStorage` | Node.js | dokumentacja referencyjna | 5–8 h | 0 zł | https://nodejs.org/api/ |

Szczególnie ważne: blokowanie pętli zdarzeń, obsługa odrzuconych obietnic, strumienie z backpressure, limity rozmiaru żądań, zamykanie połączeń przy wyłączaniu procesu, kontekst żądania przez `AsyncLocalStorage`. To wiedza potrzebna głównie do audytu przejmowanych aplikacji Next.js i Express.

**Dowód:** audyt fragmentu serwerowego istniejącej aplikacji Node.js (route handlers lub API Express): lista znalezisk z priorytetami, w tym blokowanie pętli zdarzeń, brak limitów i brak łagodnego zamykania; dwie poprawki z testami.

#### Etap 2: backend w Ruście (Tokio, Axum, Tower)

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Tokio Tutorial | zespół Tokio | samouczek, średni | 10–15 h | 0 zł | https://tokio.rs/tokio/tutorial |
| „Inventing the Service trait” | David Pedersen, blog Tokio | artykuł, średni | 1–2 h | 0 zł | https://tokio.rs/blog/2021-05-14-inventing-the-service-trait |
| Dokumentacja Axum i katalog przykładów w repozytorium | zespół Tokio | dokumentacja i przykłady | 12–15 h | 0 zł | https://docs.rs/axum/latest/axum/ |
| Dokumentacja Tower i `tower-http` (timeouty, limity, CORS, kompresja, śledzenie) | zespół Tower | dokumentacja | 5–6 h | 0 zł | https://docs.rs/tower/latest/tower/ |
| Zero To Production in Rust | Luca Palmieri | książka, od podstaw do zaawansowanego | 40–60 h | płatna | https://www.zero2prod.com |

Uwaga: „Zero To Production in Rust” używa `actix-web`, nie Axum. Wartość książki leży w procesie (testy integracyjne, konfiguracja, telemetria z `tracing`, CI, wdrożenie, idempotencja, uwierzytelnianie), który przenosi się na Axum bez zmian w podejściu. Projekt z książki warto przepisać na Axum jako ćwiczenie.

Szczególnie ważne: ekstraktory i kolejność warstw middleware, stan aplikacji, obsługa błędów przez `IntoResponse`, timeouty i limity rozmiaru ciała żądania, łagodne zamykanie, `tracing` z identyfikatorem żądania, kod blokujący w handlerach async.

**Dowód:** usługa w Axum z kilkoma zasobami, warstwami Tower (timeout, limit ciała, śledzenie), spójnymi błędami RFC 9457, konfiguracją z pliku i zmiennych środowiskowych, testami integracyjnymi i łagodnym zamykaniem; wdrożona jako kontener.

#### Etap 3: dostęp do danych z Rusta

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| SQLx (wersja 0.9): zapytania sprawdzane w czasie kompilacji, tryb offline, migracje, pula połączeń | LaunchBadge | dokumentacja i przykłady | 8–10 h | 0 zł | https://docs.rs/sqlx/latest/sqlx/ |
| SeaORM 2.0: dokumentacja, tutorial, cookbook | SeaQL | dokumentacja | 12–15 h | 0 zł | https://www.sea-ql.org/SeaORM/docs/index/ |

Wystarczy dobrze znać jedno z dwóch narzędzi: SQLx jako domyślny wybór dla własnych usług, SeaORM tam, gdzie projekt go już używa. Wiedza o SQL, indeksach i transakcjach jest w sekcji 4.

**Dowód:** warstwa danych usługi z etapu 2 na SQLx: zapytania sprawdzane w kompilacji z cache trybu offline w CI, transakcja obejmująca kilka tabel, test na prawdziwym PostgreSQL w kontenerze, brak zapytań N+1 w liście z relacjami.

#### Etap 4: kontrakty API

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| OpenAPI Learn i specyfikacja OpenAPI (3.1 i 3.2) | OpenAPI Initiative | przewodnik i norma | 8–10 h | 0 zł | https://learn.openapis.org |
| `utoipa` i `utoipa-axum`: OpenAPI generowane z kodu Rust | Juha Kukkonen i współtwórcy | dokumentacja | 4–6 h | 0 zł | https://docs.rs/utoipa/latest/utoipa/ |
| Microsoft REST API Guidelines (ogólne, Azure, Microsoft Graph) | Microsoft | wytyczne | 5–6 h | 0 zł | https://github.com/microsoft/api-guidelines |
| API Improvement Proposals (AIP) | Google | wytyczne | 6–8 h | 0 zł | https://google.aip.dev |
| Zalando RESTful API and Event Guidelines | Zalando | wytyczne | 5–6 h | 0 zł | https://opensource.zalando.com/restful-api-guidelines/ |
| gRPC: Core concepts, Protocol Buffers | gRPC (CNCF), Google | dokumentacja | 4–6 h | 0 zł | https://grpc.io/docs/ |
| `tonic`: przykłady i samouczek routeguide | gRPC Project (dawniej Hyperium) | dokumentacja i przykłady (opcjonalnie) | 5–6 h | 0 zł | https://github.com/grpc/grpc-rust |

Uwaga do gRPC w Ruście: w maju 2026 r. `tonic` przeszedł do projektu gRPC (repozytorium `grpc/grpc-rust`). Dostaje poprawki błędów, ale nie duże nowe funkcje; jego następcą ma być crate `grpc`, który w październiku 2026 r. jest jeszcze w wersjach 0.x. Generowany kod `tonic` ma pozostać wspierany, więc nauka `tonic` nie jest stracona, ale przy nowym projekcie trzeba sprawdzić stan `grpc`.

Szczególnie ważne: wersjonowanie i zmiany niełamiące, paginacja kursorowa, filtrowanie, limity i nagłówki limitów, idempotencja zapisów (np. nagłówek `Idempotency-Key`; propozycja IETF wygasła i nie jest normą), spójne błędy, kontrakt jako źródło prawdy dla klienta TypeScript.

**Dowód:** API z etapu 2 opisane w OpenAPI generowanym przez `utoipa`, z wygenerowanym z niego klientem TypeScript używanym przez aplikację Next.js; test w CI, który blokuje scalenie przy łamiącej zmianie kontraktu; krótki dokument z decyzjami projektowymi odwołującymi się do jednego z trzech zestawów wytycznych.

#### Etap 5: uwierzytelnianie i autoryzacja

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| OAuth 2 in Action | Justin Richer, Antonio Sanso, Manning | książka z kodem, średni–zaawansowany | 20–25 h | płatna | https://www.manning.com/books/oauth-2-in-action |
| RFC 6749 „The OAuth 2.0 Authorization Framework” | IETF | norma | 4–6 h | 0 zł | https://datatracker.ietf.org/doc/rfc6749/ |
| „The OAuth 2.1 Authorization Framework” (draft, wersja 16 z września 2026 r., jeszcze nie RFC) | IETF, grupa OAuth | projekt normy | 3–4 h | 0 zł | https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/ |
| RFC 9700 „Best Current Practice for OAuth 2.0 Security” (styczeń 2025) | IETF | norma (BCP 240) | 3–4 h | 0 zł | https://datatracker.ietf.org/doc/rfc9700/ |
| OpenID Connect Core 1.0 | OpenID Foundation | norma | 4–5 h | 0 zł | https://openid.net/specs/openid-connect-core-1_0.html |
| RFC 8725 „JSON Web Token Best Current Practices” | IETF | norma | 1–2 h | 0 zł | https://datatracker.ietf.org/doc/rfc8725/ |
| Pilcrow’s auth book (następca „The Copenhagen Book”): sesje, hasła, passkeys, CSRF | Pilcrow | przewodnik online | 5–6 h | 0 zł | https://auth.pilcrowonpaper.com |
| Crate’y `oauth2`, `openidconnect`, `tower-sessions`, `axum-login` | autorzy bibliotek | dokumentacja | 4–5 h | 0 zł | https://docs.rs/openidconnect, https://docs.rs/tower-sessions |

Książka „OAuth 2 in Action” jest z 2017 r.: mechanika protokołu jest aktualna, ale zalecenia bezpieczeństwa trzeba czytać razem z RFC 9700 i draftem OAuth 2.1 (PKCE zawsze, bez implicit i password grant, dokładne dopasowanie `redirect_uri`).

Szczególnie ważne: sesje po stronie serwera zamiast JWT w `localStorage`, atrybuty ciasteczek, rotacja identyfikatora sesji po logowaniu, kontrola dostępu do obiektu w każdym zapytaniu (BOLA), izolacja najemców w wielodostępności, unieważnianie sesji i tokenów.

**Dowód:** logowanie przez zewnętrznego dostawcę OIDC (kod autoryzacyjny z PKCE) do usługi w Axum, sesje w ciasteczkach `HttpOnly`, role i izolacja najemców; zestaw testów, który próbuje odczytać i zmienić obiekt innego najemcy, podmienić `state` i użyć wylogowanej sesji, i za każdym razem dostaje odmowę.

#### Etap 6: integracje i niezawodność

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Standard Webhooks: specyfikacja podpisu, identyfikatorów i ponowień | Standard Webhooks (komitet techniczny z m.in. Svix, Supabase, Twilio, Kong) | specyfikacja | 2–3 h | 0 zł | https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md |
| Stripe: odbieranie webhooków (surowe ciało do weryfikacji, ochrona przed powtórzeniem, duplikaty, brak gwarancji kolejności) | Stripe | dokumentacja | 2–3 h | 0 zł | https://docs.stripe.com/webhooks |
| „Pattern: Transactional outbox” i powiązane wzorce (idempotent consumer, saga) | Chris Richardson, microservices.io | opisy wzorców | 3–4 h | 0 zł | https://microservices.io/patterns/data/transactional-outbox.html |
| Kolejki na PostgreSQL: `pgmq`, `SELECT … FOR UPDATE SKIP LOCKED` | pgmq, PostgreSQL | dokumentacja | 4–5 h | 0 zł | https://github.com/pgmq/pgmq |
| Zadania w tle w Ruście: `apalis` (wersja 1.0 w fazie RC) | apalis | dokumentacja (opcjonalnie) | 3–4 h | 0 zł | https://docs.rs/apalis |
| Rozdziały o przetwarzaniu strumieniowym i wsadowym w „Designing Data-Intensive Applications” (zob. etap 8) | Martin Kleppmann, Chris Riccomini | książka | 8–10 h | płatna | zob. etap 8 |

Szczególnie ważne: weryfikacja podpisu na surowym ciele żądania i porównanie w stałym czasie, szybka odpowiedź 2xx i przetwarzanie asynchroniczne, deduplikacja po identyfikatorze zdarzenia, zapis zmiany i zdarzenia w jednej transakcji (outbox), ponawianie z wykładniczym odstępem, kolejka błędów, poczta transakcyjna wysyłana z outboxa, a nie w środku transakcji.

**Dowód:** odbiornik webhooków Stripe w Axum z weryfikacją podpisu, deduplikacją i outboxem w PostgreSQL; test, który wysyła to samo zdarzenie dwa razy, zdarzenia w odwrotnej kolejności i zdarzenie ze złym podpisem, oraz test awarii procesu między zapisem a wysłaniem e-maila, po którym nic nie ginie i nic się nie dubluje.

#### Etap 7: płatności i platformy klientów

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Stripe Billing: abonamenty, okresy próbne, faktury, portal klienta | Stripe | dokumentacja | 8–10 h | 0 zł | https://docs.stripe.com/billing |
| Stripe: żądania idempotentne | Stripe | dokumentacja | 1 h | 0 zł | https://docs.stripe.com/api/idempotent_requests |
| Stripe Managed Payments (Stripe jako Merchant of Record, dostępny m.in. dla firm z Polski; tylko produkty cyfrowe, bez usług profesjonalnych) | Stripe | dokumentacja | 3–4 h | 0 zł | https://docs.stripe.com/payments/managed-payments |
| Paddle Billing (alternatywny Merchant of Record) | Paddle | dokumentacja | 3–4 h | 0 zł | https://developer.paddle.com |
| Supabase: Row Level Security, klucze publishable i secret, Edge Functions | Supabase | dokumentacja | 6–8 h | 0 zł | https://supabase.com/docs/guides/database/postgres/row-level-security |
| Firebase Security Rules | Google | dokumentacja | 4–5 h | 0 zł | https://firebase.google.com/docs/rules |

Szczególnie ważne: stan abonamentu odtwarzany z webhooków, a nie z przekierowania po płatności; uprawnienia w aplikacji wynikające z jednego źródła prawdy; wybór między własnym rozliczaniem VAT (Stripe Billing z Stripe Tax) a pośrednikiem MoR; w projektach Supabase klucz `service_role` lub secret poza przeglądarką i RLS włączone na każdej tabeli; w Firebase reguły, które nie są otwarte „na czas testów”.

**Dowód:** abonament w aplikacji demonstracyjnej przez Stripe Billing lub Managed Payments, z obsługą odnowienia, nieudanej płatności, anulowania i zwrotu, sterowany wyłącznie webhookami z etapu 6; oraz raport z audytu bezpieczeństwa przykładowego projektu Supabase lub Firebase (tabele bez RLS, zbyt szerokie polityki, klucze w kliencie) z poprawkami i testami, czyli wzór usługi audytu z biznesplanu.

#### Etap 8: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Designing Data-Intensive Applications (wydanie 2, 2026) | Martin Kleppmann, Chris Riccomini, O’Reilly | książka, zaawansowany | 40–50 h | płatna | https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/ |
| OWASP API Security Top 10 (edycja 2023) | OWASP | lista ryzyk (zob. sekcja 10) | 3–4 h | 0 zł | https://owasp.org/API-Security/ |
| Komunikaty i wydania: blog Tokio, wydania Axum, SQLx i SeaORM, blog gRPC, changelog Stripe API, grupa robocza OAuth w IETF | autorzy projektów, Stripe, IETF | źródła pierwotne | ok. 1 h tygodniowo | 0 zł | https://tokio.rs/blog, https://grpc.io/blog/, https://docs.stripe.com/changelog, https://datatracker.ietf.org/wg/oauth/documents/ |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 20 pull requestów z kodem backendowym wygenerowanym przez agentów, recenzowanych według listy kontrolnej z etapów 2 i 5–7 (autoryzacja obiektu w każdym zapytaniu, weryfikacja podpisu webhooka na surowym ciele, idempotencja, brak `unwrap()` i kodu blokującego w handlerach, sekrety poza logami, timeouty na wywołaniach zewnętrznych, testy przypadków odmowy),
- **przejęcie cudzego backendu:** jedna aplikacja klienta (Next.js z Supabase albo Node.js z Firebase) przeprowadzona przez audyt API według OWASP API Security Top 10, z poprawkami i SBOM zależności serwerowych,
- **projekt systemu na papierze:** dokument architektury jednej własnej aplikacji (rdzeń w Ruście, API, synchronizacja, płatności) z analizą awarii każdego połączenia i decyzjami zapisanymi w ADR,
- **śledzenie zmian:** subskrypcja komunikatów bezpieczeństwa używanych crate’ów i bibliotek Node.js, ćwiczenie aktualizacji zależności z podatnością w 24 h jako element procesu obsługi podatności (CRA).

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz w nieznanej usłudze błąd autoryzacji, zdublowaną płatność lub zgubione zdarzenie z webhooka, piszesz test, który odtwarza problem, i umiesz wyjaśnić przyczynę osobie nietechnicznej.

---

## 6. Testowanie

*Warstwa 2: jakość i projektowanie. Opiera się na: 3, 4 i 5; części dla Rusta i platform dochodzą przy sekcjach 12–22. Jest podstawą: 7, 8, 9, 11 i każdej platformy.*

- Techniki: TDD, testy charakteryzujące, klasy równoważności, wartości brzegowe, tablice decyzyjne, przejścia stanów, Gherkin.
- Rust: `cargo test`, `cargo-nextest`, `proptest` (testy właściwości), `insta` (snapshoty), `criterion` (wydajność), `cargo-fuzz`, `cargo-mutants` (testy mutacyjne), `cargo-llvm-cov`.
- Web: Vitest, Testing Library, Playwright (E2E i akceptacyjne), MSW, axe (dostępność), regresja wizualna, k6 (obciążenie).
- Mobile: XCTest i XCUITest, testy Compose i Espresso, Maestro; emulatory i realne urządzenia.
- Desktop: WebDriver dla Tauri (`tauri-driver`), testy instalatorów i aktualizacji na czystych maszynach wirtualnych.
- Embedded: testy na hoście, `embedded-test` lub `defmt-test` na urządzeniu, QEMU, testy hardware-in-the-loop.
- Testy kontraktowe API i dane testowe bez danych osobowych.
- Typowe błędy testów pisanych przez AI: testy, które nic nie sprawdzają, mocki ukrywające błąd, testy dopasowane do implementacji zamiast zachowania, wyłączone lub osłabione asercje.

### 6.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 8 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przy doświadczeniu seniorskim etapy 0–2 można zaliczyć samym dowodem i wracać do materiałów tylko tam, gdzie dowód nie wychodzi; nowe będą najpewniej narzędzia Rusta (etap 3) i testy na urządzeniach (etap 6). Testy web (Vitest, Testing Library, MSW, Playwright) są w ścieżce frontendu (zob. sekcja 3.1, etap 6), a testy bezpieczeństwa w sekcji 10. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | podstawy testowania i techniki projektowania testów | 30–40 h | podstawy |
| 1 | testy jednostkowe w Ruście i TDD | 40–50 h | W |
| 2 | projektowanie testów: dublery, granice, co testować | 40–50 h | W |
| 3 | testy właściwości, snapshoty, fuzzing, testy mutacyjne, wydajność | 40–50 h | W |
| 4 | kod zastany i specyfikacja przykładami | 40–50 h | W |
| 5 | testy integracyjne, kontraktowe i obciążeniowe | 25–35 h | W |
| 6 | testy na platformach: mobile, desktop, embedded | 50–70 h | E |
| 7 | ekspert: strategia testów, recenzja testów z AI, aktualność | stale, ok. 1–2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 270–350 h, czyli 6–8 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: podstawy testowania

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Certified Tester Foundation Level, sylabus v4.0 (aktualizacja 4.0.1) | ISTQB | sylabus, podstawowy | 15–20 h | 0 zł (egzamin płatny, opcjonalny) | https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/ |
| Effective Software Testing | Maurício Aniche, Manning | książka, podstawowy–średni | 15–20 h | płatna | https://www.manning.com/books/effective-software-testing |

Szczególnie ważne: klasy równoważności, wartości brzegowe, tablice decyzyjne, przejścia stanów, testowanie oparte na ryzyku, różnica między weryfikacją a walidacją. Certyfikat nie jest potrzebny; sylabus służy jako wspólny słownik z klientami i zespołami QA.

**Dowód:** dla jednej funkcji z wymaganiami (np. naliczanie ceny abonamentu z rabatem i okresem próbnym) rozpisany zestaw przypadków testowych z uzasadnieniem techniką: klasy, granice, tablica decyzyjna.

#### Etap 1: testy jednostkowe w Ruście i TDD

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Rust Programming Language, rozdział 11 „Writing Automated Tests” | zespół Rusta | dokumentacja | 4–6 h | 0 zł | https://doc.rust-lang.org/book/ch11-00-testing.html |
| Test Driven Development: By Example | Kent Beck, Addison-Wesley | książka, podstawowy–średni | 12–15 h | płatna | https://www.informit.com/store/test-driven-development-by-example-9780321146533 |
| „Canon TDD” | Kent Beck | artykuł | 1 h | 0 zł | https://tidyfirst.substack.com/p/canon-tdd |
| cargo-nextest | autorzy narzędzia | dokumentacja | 3–4 h | 0 zł | https://nexte.st |
| cargo-llvm-cov | Taiki Endo | dokumentacja | 2 h | 0 zł | https://github.com/taiki-e/cargo-llvm-cov |

Szczególnie ważne: cykl czerwony–zielony–refaktoryzacja, lista testów jako plan (zgodna ze specyfikacją w procesie spec-driven), testy w module i testy integracyjne w `tests/`, `cargo nextest` (nie uruchamia doctestów, więc w CI osobno `cargo test --doc`), pokrycie jako sygnał, a nie cel.

**Dowód:** biblioteka w Ruście (np. walidacja i aktywacja klucza licencyjnego) napisana metodą TDD, z historią commitów pokazującą cykl test–implementacja, uruchamiana przez `cargo nextest` z raportem pokrycia z `cargo llvm-cov`.

#### Etap 2: projektowanie testów

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Unit Testing Principles, Practices, and Patterns | Vladimir Khorikov, Manning | książka, średni–zaawansowany | 15–20 h | płatna | https://www.manning.com/books/unit-testing |
| Growing Object-Oriented Software, Guided by Tests | Steve Freeman, Nat Pryce, Addison-Wesley | książka, średni–zaawansowany | 15–20 h | płatna | https://www.informit.com/store/growing-object-oriented-software-guided-by-tests-9780321503626 |
| „Mocks Aren’t Stubs” | Martin Fowler | artykuł | 1–2 h | 0 zł | https://martinfowler.com/articles/mocksArentStubs.html |
| „The Practical Test Pyramid” | Ham Vocke, martinfowler.com | artykuł | 2 h | 0 zł | https://martinfowler.com/articles/practical-test-pyramid.html |
| „The Testing Trophy and Testing Classifications” | Kent C. Dodds | artykuł | 1 h | 0 zł | https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications |
| Software Engineering at Google, rozdziały 11–14 (testowanie) | Titus Winters, Tom Manshreck, Hyrum Wright, O’Reilly | książka online | 6–8 h | 0 zł online | https://abseil.io/resources/swe-book |

Szczególnie ważne: testowanie zachowania, a nie implementacji; kiedy dubler (mock, stub, fake) pomaga, a kiedy ukrywa błąd; odporność testu na refaktoryzację; proporcje testów jednostkowych, integracyjnych i E2E. To jest podstawa listy kontrolnej do recenzji testów pisanych przez agentów.

**Dowód:** refaktoryzacja zestawu testów z etapu 1 tak, by zmiana wewnętrznej struktury kodu nie psuła żadnego testu, a celowo wprowadzony błąd zachowania był wykrywany; krótka notatka, które mocki usunięto i dlaczego.

#### Etap 3: zaawansowane techniki w Ruście

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Proptest book | zespół proptest | dokumentacja | 5–6 h | 0 zł | https://proptest-rs.github.io/proptest/ |
| insta | Armin Ronacher | dokumentacja | 2–3 h | 0 zł | https://insta.rs/docs/ |
| Rust Fuzz Book (`cargo-fuzz`, `afl.rs`) | Rust Fuzzing Authority | dokumentacja | 6–8 h | 0 zł | https://rust-fuzz.github.io/book/ |
| cargo-mutants | Martin Pool | dokumentacja | 4–5 h | 0 zł | https://mutants.rs |
| Criterion.rs | autorzy biblioteki | dokumentacja | 3–4 h | 0 zł | https://bheisler.github.io/criterion.rs/book/ |

Szczególnie ważne: własności zamiast przykładów (odwracalność serializacji, niezmienniki), minimalizacja kontrprzykładów, recenzja zmian w snapshotach (`cargo insta review`) zamiast ślepej akceptacji, fuzzing parserów i wszystkiego, co przyjmuje dane z zewnątrz, odsetek przeżywających mutantów jako miara jakości testów.

**Dowód:** do rdzenia z etapu 1 dodane: testy właściwości dla serializacji i synchronizacji, snapshot formatu wyjściowego, cel fuzzingu dla parsera wejścia uruchamiany w CI przez ograniczony czas, raport `cargo mutants` z omówieniem każdego przeżywającego mutanta.

#### Etap 4: kod zastany i specyfikacja przykładami

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Working Effectively with Legacy Code | Michael Feathers, Pearson | książka, średni–zaawansowany | 15–20 h | płatna | https://www.informit.com/store/working-effectively-with-legacy-code-9780131177055 |
| Specification by Example | Gojko Adzic, Manning | książka, średni | 10–12 h | płatna | https://www.manning.com/books/specification-by-example |
| Gherkin Reference | Cucumber | dokumentacja | 1–2 h | 0 zł | https://cucumber.io/docs/gherkin/reference/ |
| Explore It! | Elisabeth Hendrickson, Pragmatic Bookshelf | książka, średni | 8–10 h | płatna | https://pragprog.com/titles/ehxta/explore-it/ |

Szczególnie ważne: testy charakteryzujące (utrwalenie obecnego zachowania przed zmianą), szwy i łamanie zależności, kryteria akceptacji jako przykłady w specyfikacji, testowanie eksploracyjne w sesjach z kartą (charter) przy przejmowaniu aplikacji z vibe codingu.

**Dowód:** przejmowana aplikacja (poligon B z mapy nauki) objęta testami charakteryzującymi krytycznych ścieżek (logowanie, płatność, zapis danych) przed pierwszą zmianą; notatki z dwóch sesji eksploracyjnych z listą znalezionych problemów; trzy kryteria akceptacji kolejnej poprawki zapisane w Gherkinie.

#### Etap 5: testy integracyjne, kontraktowe i obciążeniowe

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Pact: wprowadzenie i przewodnik dla Rusta (`pact_consumer`, `pact_verifier`) | Pact Foundation | dokumentacja | 8–10 h | 0 zł | https://docs.pact.io, https://docs.pact.io/implementation_guides/rust |
| Grafana k6 | Grafana Labs | dokumentacja | 8–10 h | 0 zł | https://grafana.com/docs/k6/latest/ |

Szczególnie ważne: testy integracyjne z prawdziwą bazą w kontenerze zamiast mocków warstwy danych, kontrakt między aplikacją mobilną lub desktopową a API, progi (thresholds) w k6 jako bramka w CI, dane testowe bez danych osobowych.

**Dowód:** API w Axum z testem kontraktowym konsumenta (aplikacja kliencka) i weryfikacją po stronie dostawcy w CI; scenariusz k6 z progami opóźnienia i błędów, który zatrzymuje pipeline po ich przekroczeniu.

#### Etap 6: testy na platformach

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| XCTest (testy jednostkowe, wydajności i UI) i Swift Testing | Apple | dokumentacja | 8–10 h | 0 zł | https://developer.apple.com/documentation/xctest, https://developer.apple.com/xcode/swift-testing/ |
| Test apps on Android, Test your Compose layout, Espresso | Google | dokumentacja | 8–10 h | 0 zł | https://developer.android.com/training/testing, https://developer.android.com/develop/ui/compose/testing |
| Maestro | mobile.dev | dokumentacja | 4–6 h | 0 zł (chmura płatna) | https://docs.maestro.dev |
| Tauri: WebDriver (`tauri-driver`, usługa WebdriverIO) | zespół Tauri | dokumentacja | 4–6 h | 0 zł | https://v2.tauri.app/develop/tests/webdriver/ |
| embedded-test | probe-rs | dokumentacja | 4–6 h | 0 zł | https://github.com/probe-rs/embedded-test |
| QEMU: emulacja systemów Arm | projekt QEMU | dokumentacja | 3–4 h | 0 zł | https://www.qemu.org/docs/master/system/target-arm.html |

Szczególnie ważne: testy rdzenia Rust na hoście jako główna warstwa, a testy platformowe tylko dla integracji i UI; `tauri-driver` bezpośrednio działa na Linuksie i Windows, macOS wymaga ścieżki przez WebdriverIO; `defmt-test` opiera się na wycofanym `probe-run`, dlatego dla nowych projektów `embedded-test` z `probe-rs`; testy instalatora i aktualizacji na czystych maszynach wirtualnych.

**Dowód:** jeden rdzeń w Ruście z testami na hoście oraz po jednym teście integracyjnym na każdej platformie: XCUITest na symulatorze iOS, test Compose na emulatorze Androida, przepływ Maestro przez onboarding, test WebDriver aplikacji Tauri na Linuksie i Windows w CI, test na płytce (np. nRF lub RP2040) uruchamiany przez `probe-rs`.

#### Etap 7: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Wydania i changelogi narzędzi testowych (nextest, proptest, cargo-mutants, Tauri, Maestro) | autorzy narzędzi | źródła pierwotne | ok. 30 min tygodniowo | 0 zł | strony z etapów 1–6 |
| Aktualizacje sylabusów ISTQB (m.in. Advanced Level Test Analyst, Testing with Generative AI) | ISTQB | sylabusy, zaawansowany | wg potrzeb | 0 zł | https://istqb.org |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja testów z AI:** 20 pull requestów z testami wygenerowanymi przez agentów, recenzowanych według listy kontrolnej z etapów 2 i 3 (testy bez asercji lub z asercjami tautologicznymi, mocki ukrywające błąd, testy dopasowane do implementacji, osłabione lub wyłączone asercje, zaakceptowane bez przeglądu snapshoty); przy każdej wątpliwości `cargo mutants` na zmienionym kodzie,
- **TDD z agentem:** człowiek pisze lub zatwierdza listę testów ze specyfikacji, agent implementuje; pomiar, ile błędów wyłapały testy przed recenzją,
- **strategia testów u klienta:** jednostronicowa strategia (ryzyka, warstwy testów, bramki w CI, dane testowe) dla przejmowanej aplikacji,
- **wkład w open source** w jednym narzędziu testowym z ekosystemu Rusta, choćby w dokumentację lub przykłady.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień obejmujesz nieznany moduł przejmowanej aplikacji testami charakteryzującymi, wskazujesz w zestawie testów wygenerowanym przez AI testy, które nic nie sprawdzają (potwierdzone testami mutacyjnymi), i umiesz wyjaśnić osobie nietechnicznej, jakie ryzyko pokrywają testy, a jakiego nie.

---

## 7. Wymagania i specyfikacje

*Warstwa 2: jakość i projektowanie. Opiera się na: 3, 5 i 6. Jest podstawą: 8, 10, 11 i każdego projektu klienta.*

W tym modelu biznesowym specyfikacja jest jednocześnie poleceniem dla agentów, zakresem umowy z klientem i podstawą odbioru. Agenci piszą kod, ale to człowiek pisze i zatwierdza specyfikację, więc jej jakość decyduje o jakości kodu, o tym, czy wycena się broni, i o tym, czy spór o „to miało działać inaczej” da się rozstrzygnąć zapisem, a nie wspomnieniem rozmowy. Przy przejęciu cudzej aplikacji specyfikacji zwykle nie ma wcale, więc trzeba ją odtworzyć z działającego systemu. Ta sekcja obejmuje wymagania od rozmowy z klientem do protokołu odbioru; Gherkin jako format testów akceptacyjnych, testy charakteryzujące i „Specification by Example” są w sekcji 6 (6.1, etap 4), decyzje architektoniczne, ADR i C4 w sekcji 8, a budowa skilli i ewaluacji vicrafter w sekcji 11.

- Wydobywanie wymagań od klienta: wywiad o przeszłych zachowaniach zamiast pytań o opinie, warsztat zdalny z klientem, Jobs-to-be-Done (jaką pracę klient „zatrudnia” aplikację do wykonania), mapa wpływu (cel biznesowy, aktorzy, wpływ, rezultaty), story mapping (szkielet przepływu użytkownika i cięcie na wydania), example mapping (reguły, przykłady, pytania otwarte) jako krótka sesja przed każdą funkcją; notatki z rozmów jako materiał źródłowy dla agenta, a nie gotowa specyfikacja.
- Pisanie wymagań w EARS: pięć wzorców podstawowych (stałe, zdarzeniowe „GDY”, stanowe „DOPÓKI”, niepożądane „JEŚLI … TO”, opcjonalne „GDZIE”) i wzorzec złożony, jedno wymaganie na zdanie, identyfikator R-n, aktor i reakcja systemu nazwane wprost, bez słów nieweryfikowalnych („szybko”, „intuicyjnie”, „odpowiednio”, „itp.”).
- Kryteria akceptacji: dla każdego R-n co najmniej jedno AC-n, przypadki pozytywne, negatywne (niepożądane zachowanie, brak uprawnień, błędne dane) i brzegowe (granice, wartości puste, równoczesność, strefy czasowe); konkretne przykłady z danymi zamiast ogólników; zapis jako scenariusze Zakładając/Gdy/Wtedy (format i automatyzacja: sekcja 6).
- Wymagania niefunkcjonalne według ISO/IEC 25010:2023 (dziewięć charakterystyk, m.in. bezpieczeństwo, niezawodność, wydajność, zdolność interakcji, elastyczność, safety): każde z miarą, progiem, warunkami pomiaru i sposobem weryfikacji (np. „p95 czasu odpowiedzi poniżej 300 ms przy 50 żądaniach na sekundę, mierzone testem k6 w CI”); bazowe NFR projektu w `nfr.md`, NFR funkcji w jej specyfikacji; wymagania bezpieczeństwa z OWASP ASVS (zob. sekcja 10), dostępności z WCAG 2.2 (zob. sekcja 13).
- Wykrywanie niejednoznaczności według kategorii: zakres, dane i ich źródła, błędy i przypadki brzegowe, uprawnienia i role, NFR, zależności od systemów zewnętrznych; „zapachy wymagań” (słowa niejednoznaczne, strona bierna bez aktora, zaimki bez odniesienia, porównania bez punktu odniesienia, „wszystkie”, „zawsze”); znaczniki `[DO WYJAŚNIENIA: …]` zamiast zgadywania i pytania do klienta z propozycją odpowiedzi.
- Rozdział „co i dlaczego” od „jak”: w `spec.md` cel, użytkownicy, wymagania, kryteria akceptacji, NFR i sekcja „Poza zakresem”, bez nazw technologii, tabel, endpointów i klas; „jak” należy do `plan.md` (zob. sekcja 8); test: czy specyfikacja przetrwałaby zmianę frameworka bez edycji.
- Specyfikacja jako zakres umowy i podstawa wyceny: zatwierdzona wersja specyfikacji z sumą kontrolną jako załącznik do zlecenia w pakiecie „Rozwój według specyfikacji”, wycena na podstawie liczby i złożoności wymagań oraz ryzyk z pytań otwartych, jawne założenia i wykluczenia, kryteria odbioru znane przed rozpoczęciem pracy.
- Zarządzanie zmianą: wersjonowanie specyfikacji (`spec_version`), zatwierdzenie przywiązane do treści, każda zmiana zachowania po zatwierdzeniu jako propozycja zmiany (`proposal.md` z powodem, wpływem i wyceną oraz `spec-delta.md` z wymaganiami dodanymi, zmienionymi i usuniętymi), rozróżnienie błędu (kod robi co innego, niż mówi specyfikacja: poprawka w ramach umowy) od luki w specyfikacji lub nowego życzenia (płatna spec-delta).
- Śledzenie powiązań: R-n → AC-n → zadanie T-n → test, wykrywanie wymagań bez kryteriów, kryteriów bez testów i kodu bez wymagania; macierz śledzenia jako dowód dla klienta, że wszystko, za co zapłacił, zostało sprawdzone.
- Odtwarzanie specyfikacji z istniejącego zachowania przy przejęciu: źródła (działająca aplikacja, interfejs, dane w bazie, logi, kod, rozmowa z klientem przy demonstracji), specyfikacje w statusie `reconstructed` tylko dla obszarów zmienianych w najbliższych 90 dniach, opis zachowania obecnego, także wadliwego, z oznaczeniem `[DO WERYFIKACJI Z KLIENTEM]`, testy charakteryzujące jako wykonywalna wersja tej specyfikacji (zob. sekcja 6), zatwierdzenie dopiero po weryfikacji z klientem.
- Specyfikacje jako kontekst dla agentów: jeden dokument czytelny i dla klienta, i dla AI (język klienta, stałe identyfikatory, krótkie zdania, przykłady z danymi, słownik pojęć), samowystarczalność (agent nie zgaduje, czego brakuje), sekcja „Poza zakresem” jako ochrona przed dopisywaniem funkcji, wywiad prowadzony przez agenta przed pisaniem specyfikacji (zob. sekcja 1), narzędzia spec-driven (GitHub Spec Kit, Kiro, OpenSpec) jako wzorce struktury artefaktów.
- Protokół odbioru (UAT): scenariusze odbioru wyprowadzone z AC, sesja z klientem na środowisku testowym z danymi bez danych osobowych, wynik każdego scenariusza, uwagi sklasyfikowane jako błąd, luka w specyfikacji albo nowe życzenie, decyzja (odbiór, odbiór z uwagami, odmowa) i podpis; protokół jako zamknięcie etapu rozliczeniowego.
- Typowe błędy specyfikacji pisanych przez AI do wyłapania: szczegóły implementacji w specyfikacji (tabele, endpointy, biblioteki), wymagania wymyślone ponad intencję klienta i „ulepszenia”, których nikt nie zamawiał, ciche założenia w miejscu pytań (np. przyjęta metoda logowania albo polityka retencji), same przypadki pozytywne bez negatywnych i brzegowych, słowa nieweryfikowalne i NFR bez progów, kryteria akceptacji powtarzające wymaganie innymi słowami zamiast przykładu z danymi, kilka wymagań w jednym zdaniu, niespójne nazwy tego samego pojęcia, wymagania sprzeczne między sekcjami, brak sekcji „Poza zakresem”, rozwlekłość utrudniająca przegląd klientowi, odtworzona specyfikacja, która opisuje to, co kod „powinien” robić, zamiast tego, co robi.

### 7.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 7 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przy doświadczeniu seniorskim etap 0 można zaliczyć samym dowodem; nowe będą najpewniej formalne pisanie wymagań w EARS i wykrywanie niejednoznaczności (etap 2), mierzalne NFR (etap 3) oraz specyfikacja jako zakres umowy, zmiana i odbiór (etap 5), bo w pracy etatowej tę część zwykle wykonują analityk i product owner. Etapy 1–2 i 4 warto przejść przed pierwszym projektem w pakiecie „Rozwój według specyfikacji”, a etap 5 przed podpisaniem pierwszej umowy. „Specification by Example”, Gherkin Reference i „Working Effectively with Legacy Code” są w ścieżce testowania (zob. sekcja 6.1, etap 4) i nie są tu powtarzane. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem. Narzędzia spec-driven zmieniają się co kilka tygodni, więc ich dokumentację trzeba czytać w wersji bieżącej.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | podstawy inżynierii wymagań i wspólny słownik | 20–30 h | podstawy |
| 1 | wydobywanie wymagań od klienta | 30–40 h | W |
| 2 | EARS, kryteria akceptacji i niejednoznaczność | 30–40 h | W |
| 3 | wymagania niefunkcjonalne z mierzalnymi progami | 15–20 h | W |
| 4 | specyfikacje dla agentów: spec-driven w praktyce | 20–30 h | W |
| 5 | umowa, zmiana, przejęcie i odbiór | 30–40 h | E |
| 6 | ekspert: pomiar jakości specyfikacji, recenzja specyfikacji z AI, aktualność | stale, ok. 1 h tygodniowo | E |

Razem od zera do poziomu E: ok. 145–200 h, czyli 3–5 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: podstawy inżynierii wymagań

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| CPRE Foundation Level, sylabus 3.3.0, słownik CPRE 2.2.0 i podręcznik (Handbook) | IREB | sylabus, słownik, podręcznik, podstawowy | 12–15 h | 0 zł (podręcznik po założeniu darmowego konta; egzamin płatny, opcjonalny) | https://cpre.ireb.org/en/downloads-and-resources/downloads |
| Software Requirements Essentials: Core Practices for Successful Business Analysis (2023) | Karl Wiegers, Candase Hokanson, Addison-Wesley | książka, podstawowy–średni | 8–10 h | płatna | https://www.informit.com/store/software-requirements-essentials-core-practices-for-9780138190286 |
| ISO/IEC/IEEE 29148:2018 (procesy i cechy dobrych wymagań; w rewizji, nowe wydanie w fazie DIS) | ISO, IEC, IEEE | norma, wg potrzeb | wg potrzeb | płatna | https://www.iso.org/standard/72089.html |

Szczególnie ważne: rodzaje wymagań (biznesowe, użytkownika, funkcjonalne, jakościowe, ograniczenia), cechy dobrego wymagania (jednoznaczne, weryfikowalne, wykonalne, niezależne od rozwiązania, śledzalne), interesariusze i źródła wymagań, różnica między walidacją (czy to właściwy system) a weryfikacją (czy system spełnia specyfikację). Certyfikat nie jest potrzebny; sylabus i słownik dają wspólny język z klientami, którzy mają własnych analityków. Normę 29148 wystarczy znać z nazwy i struktury; przed zakupem sprawdzić, czy ukazało się nowe wydanie.

**Dowód:** jednostronicowy słownik pojęć do oferty i umowy (wymaganie, kryterium akceptacji, specyfikacja, propozycja zmiany, odbiór, błąd, luka w specyfikacji) oraz rozbiór jednej istniejącej specyfikacji lub zgłoszenia od klienta: każde zdanie sklasyfikowane według rodzaju wymagania i ocenione według cech dobrego wymagania, z listą zdań do przepisania.

#### Etap 1: wydobywanie wymagań od klienta

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Mom Test | Rob Fitzpatrick | książka, podstawowy | 3–4 h | płatna | https://www.momtestbook.com |
| „Know Your Customers’ »Jobs to Be Done«” (wrzesień 2016) | Clayton M. Christensen, Taddy Hall, Karen Dillon, David S. Duncan, Harvard Business Review | artykuł | 1 h | abonament (część artykułów bezpłatnie) | https://hbr.org/2016/09/know-your-customers-jobs-to-be-done |
| User Story Mapping (2014) | Jeff Patton, O’Reilly | książka, podstawowy–średni | 8–10 h | płatna | https://www.oreilly.com/library/view/user-story-mapping/9781491904893/ |
| Impact Mapping (2012) i materiały warsztatowe na stronie projektu | Gojko Adzic | książka i strona (CC BY 4.0) | 3–4 h | książka płatna, strona 0 zł | https://www.impactmapping.org |
| „Introducing Example Mapping” (2015) | Matt Wynne, Cucumber | artykuł | 1 h | 0 zł | https://cucumber.io/blog/bdd/example-mapping-introduction/ |
| CPRE Requirements Elicitation, sylabus 3.2.0 | IREB | sylabus, średni | 6–8 h | 0 zł | https://cpre.ireb.org/en/downloads-and-resources/downloads |

Szczególnie ważne: pytania o to, co klient faktycznie robił i ile go to kosztowało, a nie o to, co by chciał; praca, którą aplikacja ma wykonać za użytkownika, jako filtr dla funkcji; mapa wpływu na start projektu, żeby każda funkcja miała cel biznesowy; story map do cięcia zakresu na wydania i do rozmowy o budżecie; example mapping jako 25-minutowa sesja przed każdą funkcją (czerwone karty, czyli pytania otwarte, to gotowe znaczniki `[DO WYJAŚNIENIA]`); jeśli sesja trwa dłużej, funkcja jest za duża i trzeba ją podzielić.

**Dowód:** dla jednego klienta (lub poligonu z mapy nauki) notatki z dwóch wywiadów, mapa wpływu, story map z zaznaczonym pierwszym wydaniem i example map dla dwóch funkcji; z tego wpisy wejściowe do `/vicrafter:specify` (intencja w kilku zdaniach, reguły, przykłady, pytania otwarte) i lista decyzji, które klient podjął na warsztacie.

#### Etap 2: EARS, kryteria akceptacji i niejednoznaczność

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| EARS: przewodnik i reguły wzorców | Alistair Mavin | strona autora, średni | 3–4 h | 0 zł | https://alistairmavin.com/ears/ |
| „Easy Approach to Requirements Syntax (EARS)” (RE ’09) | Alistair Mavin, Philip Wilkinson, Adrian Harwood, Mark Novak, IEEE | artykuł naukowy | 1–2 h | płatny dostęp przez IEEE | https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/ |
| Writing Great Specifications (2017) | Kamil Nicieja, Manning | książka, średni | 10–12 h | płatna | https://www.manning.com/books/writing-great-specifications |
| Fifty Quick Ideas to Improve Your User Stories | Gojko Adzic, David Evans | książka, średni | 4–5 h | płatna | https://leanpub.com/50quickideas |
| „Rapid quality assurance with Requirements Smells” (2016) | Henning Femmer, Daniel Méndez Fernández, Stefan Wagner, Sebastian Eder | artykuł naukowy | 1–2 h | 0 zł (arXiv) | https://arxiv.org/abs/1611.08847 |
| Guide to Writing Requirements: arkusz podsumowujący (summary sheet) | INCOSE Requirements Working Group | ściągawka (pełny przewodnik płatny) | 1–2 h | 0 zł | https://www.incose.org/communities/working-groups-initiatives/requirements |

Szczególnie ważne: w EARS warunek i wyzwalacz przed reakcją systemu, a wzorzec niepożądany („JEŚLI … TO”) jako miejsce na wszystkie przypadki negatywne; kryterium akceptacji jako konkretny przykład z danymi, a nie przepisane wymaganie; trzy pytania kontrolne dla każdego R-n: co przy błędnych danych, co na granicy, co bez uprawnień; lista zapachów wymagań jako lista kontrolna do recenzji specyfikacji pisanych przez agenta. „Writing Great Specifications” uzupełnia „Specification by Example” z sekcji 6 o pisanie i utrzymanie samej dokumentacji.

**Dowód:** specyfikacja jednej funkcji klienta (rozmiar M, np. rezerwacja z limitem i wygasaniem) z 5–8 wymaganiami w EARS, kryteriami akceptacji pozytywnymi, negatywnymi i brzegowymi dla każdego R-n i sekcją „Poza zakresem”; obok ta sama funkcja w wersji napisanej przez agenta bez wskazówek, z listą znalezionych zapachów wymagań i poprawek, oraz notatka, ile pytań do klienta wynikło z recenzji.

#### Etap 3: wymagania niefunkcjonalne

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| ISO/IEC 25010:2023, model jakości produktu | ISO, IEC | norma | 2–3 h (struktura i definicje) | płatna | https://www.iso.org/standard/78176.html |
| arc42 Quality Model: charakterystyki jakości, przykładowe wymagania jakościowe, opis ISO 25010 | Gernot Starke i współtwórcy (CC BY-SA 4.0) | katalog online | 4–6 h | 0 zł | https://quality.arc42.org, https://quality.arc42.org/standards/iso-25010 |
| Mastering the Requirements Process, wydanie 3 (2012) | Suzanne Robertson, James Robertson, Addison-Wesley | książka, średni | 6–8 h (rozdziały o wymaganiach niefunkcjonalnych i kryteriach dopasowania) | płatna | https://www.informit.com/store/mastering-the-requirements-process-getting-requirements-9780321815743 |

Szczególnie ważne: zmiany w wersji 2023 (dziewięć charakterystyk, nowa „safety”, „zdolność interakcji” zamiast użyteczności, „elastyczność” zamiast przenośności), kryterium dopasowania (fit criterion) jako miara i próg, które pozwalają rozstrzygnąć, czy wymaganie jest spełnione, rozróżnienie wymagań bazowych projektu i wymagań funkcji, NFR, które wynikają z prawa i umowy (RODO, CRA, dostępność), a nie z życzeń. Atrybuty jakości jako drivery decyzji architektonicznych są w sekcji 8, a SLO i ich pomiar w sekcji 9.

**Dowód:** `nfr.md` dla przejmowanej aplikacji klienta: dla każdej istotnej charakterystyki ISO 25010 wymaganie z miarą, progiem, warunkami pomiaru i sposobem weryfikacji (test, narzędzie, przegląd), z oznaczeniem, które progi system dziś spełnia, a których nie (wynik pomiaru), i które z nich trafiają do oferty jako płatne prace stabilizacyjne.

#### Etap 4: specyfikacje dla agentów

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| GitHub Spec Kit: „Specification-Driven Development”, Quickstart, „Existing Projects” | GitHub | narzędzie open source (MIT) i dokumentacja | 6–8 h | 0 zł | https://github.com/github/spec-kit/blob/main/spec-driven.md, https://github.github.io/spec-kit/quickstart.html, https://github.github.io/spec-kit/guides/existing-projects.html |
| Kiro: specyfikacje funkcji i błędów | Amazon (Kiro) | dokumentacja | 2–3 h | 0 zł | https://kiro.dev/docs/specs/, https://kiro.dev/docs/specs/bugfix-specs/ |
| OpenSpec: koncepcje (delta specs) | Fission AI | narzędzie open source i dokumentacja | 2–3 h | 0 zł | https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md |
| „Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl” (październik 2025) | Birgitta Böckeler, martinfowler.com | artykuł | 1 h | 0 zł | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html |
| Spec-driven development w Technology Radar (listopad 2025, pierścień „Assess”) | Thoughtworks | omówienie | 0,5 h | 0 zł | https://www.thoughtworks.com/radar/techniques/spec-driven-development |
| Dokumentacja Claude Code: „Let Claude interview you” (Best practices) | Anthropic | dokumentacja | 0,5 h | 0 zł | https://code.claude.com/docs/en/best-practices |

Szczególnie ważne: w Spec Kit szablon specyfikacji wymusza „co i dlaczego” bez „jak” oraz znaczniki `[NEEDS CLARIFICATION: …]`, a kroki `/speckit-clarify`, `/speckit-checklist` i `/speckit-analyze` (w Claude Code jako skille) to wzorzec dla `clarify` i `analyze` w vicrafter; w Kiro wymagania w `requirements.md` są w notacji EARS, a specyfikacja błędu rozdziela zachowanie obecne, oczekiwane i niezmienione, co dobrze pasuje do przejęć; w OpenSpec zmiana to delta (dodane, zmienione, usunięte wymagania) scalana do specyfikacji głównej, czyli ten sam pomysł co spec-delta. Böckeler i Thoughtworks pokazują ryzyka: rozwlekłe specyfikacje trudne do przeglądu, przerost ceremonii przy małych zmianach, złudne poczucie kontroli; w praktyce trzy poziomy rygoru: spec-first, spec-anchored (vicrafter) i spec-as-source. Wywiad prowadzony przez agenta skraca drogę od intencji do specyfikacji, ale odpowiedzi daje człowiek po rozmowie z klientem, a nie agent.

**Dowód:** ta sama funkcja z etapu 2 przeprowadzona przez Spec Kit w Claude Code (od `/speckit-specify` do `/speckit-analyze`) i przez przepływ vicrafter (`specify`, `clarify`, `approve`), z porównaniem: czas człowieka, liczba pytań wyjaśniających, problemy wykryte w analizie spójności, długość specyfikacji, ocena klienta, czy rozumie dokument bez tłumaczenia; wnioski przeniesione do szablonu `spec.md` (zmiany w skillach vicrafter: sekcja 11).

#### Etap 5: umowa, zmiana, przejęcie i odbiór

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Software Requirements, wydanie 3 (2013) | Karl Wiegers, Joy Beatty, Microsoft Press | książka, średni–zaawansowany | 12–15 h (rozdziały o priorytetyzacji, walidacji, zarządzaniu zmianą, śledzeniu powiązań i projektach przejmowanych) | płatna | https://www.pearson.com/en-us/subject-catalog/p/software-requirements/P200000000686/9780735679665 |
| Object-Oriented Reengineering Patterns | Serge Demeyer, Stéphane Ducasse, Oscar Nierstrasz | książka (CC BY-SA 4.0), średni | 6–8 h (rozdziały o pierwszym kontakcie z systemem i wstępnym zrozumieniu) | 0 zł (PDF) | https://www.oscar.nierstrasz.org/oorp/ |
| Certified Tester Acceptance Testing, sylabus v1.0 (2019) | ISTQB | sylabus, średni | 6–8 h | 0 zł (egzamin płatny, opcjonalny) | https://istqb.org/certifications/certified-tester-acceptance-testing-ct-act/ |
| Software Estimation: Demystifying the Black Art (2006) | Steve McConnell, Microsoft Press | książka, średni | 6–8 h (wybrane rozdziały) | płatna | https://www.microsoftpressstore.com/store/software-estimation-demystifying-the-black-art-9780735605350 |

Szczególnie ważne: zatwierdzona wersja specyfikacji jako załącznik do zlecenia i punkt odniesienia dla odbioru; każda prośba klienta po zatwierdzeniu klasyfikowana jako błąd (w cenie), luka w specyfikacji lub nowe życzenie (płatna spec-delta z wyceną i wpływem na termin); wycena przedziałem z jawnymi założeniami, a pytania otwarte jako ryzyko w cenie lub warunek; przy przejęciu „wywiad podczas demonstracji” (klient pokazuje, jak używa aplikacji, a odtwarzana specyfikacja powstaje na bieżąco) i odtworzenie tylko obszarów, które będą zmieniane; UAT jako weryfikacja z perspektywy użytkownika według scenariuszy z AC, a nie swobodne „klikanie”, z decyzją i podpisem. Zapisy umowne (odpowiedzialność, odbiór milczący, terminy na uwagi) do weryfikacji z prawnikiem.

**Dowód:** komplet dokumentów z jednego projektu klienta lub poligonu: odtworzona specyfikacja w statusie `reconstructed` dla jednego obszaru przejmowanej aplikacji (z oznaczeniami `[DO WERYFIKACJI Z KLIENTEM]` i powiązaniem z testami charakteryzującymi z sekcji 6), specyfikacja nowej funkcji zatwierdzona przez klienta z wyceną, jedna propozycja zmiany (`proposal.md` i `spec-delta.md`) z wyceną i wpływem na termin, macierz śledzenia R → AC → T → test oraz protokół odbioru (`uat-protocol.md`) z sesji z klientem, z uwagami sklasyfikowanymi jako błąd, luka albo nowe życzenie.

#### Etap 6: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Wydania i dokumentacja Spec Kit, Kiro i OpenSpec | GitHub, Amazon, Fission AI | źródła pierwotne | ok. 0,5 h tygodniowo | 0 zł | https://github.com/github/spec-kit/releases, https://kiro.dev/docs/, https://openspec.dev |
| AI4RE (micro-credential, sylabus i przewodnik 1.0.0), RE@Agile, Requirements Modeling | IREB | sylabusy, zaawansowany | wg potrzeb | 0 zł (egzaminy płatne) | https://cpre.ireb.org/en/downloads-and-resources/downloads |
| Kolejne wydanie ISO/IEC/IEEE 29148 (po publikacji) | ISO, IEC, IEEE | norma | wg potrzeb | płatna | https://www.iso.org/standard/72089.html |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja specyfikacji z AI:** 20 specyfikacji i propozycji zmian napisanych przez agenta `requirements`, recenzowanych według listy kontrolnej z etapów 2–4 (szczegóły implementacji, ciche założenia, brak przypadków negatywnych i brzegowych, NFR bez progów, wymagania ponad intencję klienta, niespójne nazwy, brak „Poza zakresem”); powtarzające się błędy przenoszone do skilli i ewaluacji vicrafter (zob. sekcja 11),
- **pomiar jakości specyfikacji:** co miesiąc liczba zadań w `needs_spec`, problemów blokujących w `analyze`, rund `clarify`, uwag klienta przy odbiorze sklasyfikowanych jako luka w specyfikacji oraz udział płatnych spec-delta w przychodzie,
- **warsztat z klientem jako usługa:** stały format example mappingu lub story mappingu na start każdego zlecenia, z notatką i decyzjami wysyłanymi klientowi tego samego dnia,
- **biblioteka wzorców:** zestaw przykładowych wymagań EARS, kryteriów akceptacji i NFR dla powtarzalnych obszarów aplikacji klientów (logowanie, role, płatności, powiadomienia, eksport danych, usuwanie konta), utrzymywany i poprawiany po każdym projekcie.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień po jednym warsztacie z klientem przygotowujesz specyfikację funkcji średniej wielkości (EARS, kryteria akceptacji pozytywne, negatywne i brzegowe, NFR z progami, „Poza zakresem”, lista pytań otwartych), wycenę i propozycję harmonogramu, a klient zatwierdza ją bez dodatkowej rundy wyjaśnień; przy odbiorze nie pojawia się uwaga sklasyfikowana jako luka w specyfikacji, a każdą prośbę zgłoszoną po zatwierdzeniu umiesz w 15 minut zaklasyfikować i wyjaśnić klientowi, czy mieści się w umowie, czy wymaga płatnej propozycji zmiany.

---

## 8. Architektura i projektowanie systemów

*Warstwa 2: jakość i projektowanie. Opiera się na: 4, 5, 6 i 7. Jest podstawą: 10, 11, 12, 14 i 21.*

W tym modelu biznesowym agenci piszą kod, a człowiek podejmuje i zatwierdza decyzje architektoniczne. Aplikacje zbudowane przez AI i no-code rzadko mają przemyślaną architekturę: logika biznesowa jest rozlana po komponentach, moduły nie mają granic, a dane klientów SaaS rozdziela tylko warunek w zapytaniu. Pakiet „Audyt przejęcia” wymaga, by w 2 dni nazwać ten stan (C4, ADR „reconstructed”, rejestr długu) i zaproponować architekturę docelową osiągalną małymi krokami. We własnych aplikacjach ta sama umiejętność decyduje o granicach wspólnego rdzenia w Ruście. W vicrafter architektura to bazowe ADR zatwierdzane z klientem i plan techniczny każdej funkcji. Bez tej sekcji człowiek nie oceni, czy plan przygotowany przez agenta jest dobry, czy tylko wiarygodnie brzmi. Modelowanie danych jest w sekcji 4, kontrakty API, integracje i DDIA w sekcji 5, testy charakteryzujące w sekcji 6, zapis wymagań niefunkcjonalnych w sekcji 7, a modelowanie zagrożeń w sekcji 10.

- Podstawy projektowania: spójność i sprzężenie (także jego siła, odległość i zmienność), moduły głębokie i płytkie, ukrywanie informacji, złożoność jako główny koszt utrzymania, zasady SOLID i ich granice (abstrakcje na zapas, nadmiar warstw), wzorce projektowe jako słownik, a nie cel, idiomy Rusta zamiast przenoszenia wzorców z Javy.
- Style architektoniczne i ich kompromisy: warstwy, monolit modularny, architektura heksagonalna (porty i adaptery), architektura usługowa i mikroserwisy, architektura sterowana zdarzeniami (powiadomienia, przenoszenie stanu w zdarzeniu, event sourcing, CQRS), local-first; „monolit najpierw” jako domyślny wybór dla firmy jednoosobowej.
- Atrybuty jakości jako drivery decyzji: scenariusze atrybutów jakości, identyfikacja charakterystyk kluczowych dla danego systemu, analiza kompromisów (np. spójność kontra dostępność, izolacja kontra koszt), Attribute-Driven Design (ADD 3.0) i ATAM w wersji odchudzonej dla jednej osoby; zapis wymagań jakościowych jest w sekcji 7.
- Dokumentowanie: model C4 (kontekst, kontenery, komponenty, diagramy dynamiczne i wdrożeniowe), arc42 jako szkielet dokumentu, ADR z co najmniej dwiema alternatywami, konsekwencjami i statusem (MADR, Nygard, zastępowanie zamiast edycji), `ARCHITECTURE.md` w repozytorium, docs-as-code i diagramy jako kod (Structurizr DSL, Mermaid).
- DDD: subdomeny (kluczowa, wspierająca, ogólna), bounded contexts, mapa kontekstów i jej wzorce (warstwa antykorupcyjna, open-host service, konformista, wspólne jądro), język wszechobecny i słownik, event storming; w zarysie taktyczne DDD (agregaty, encje, obiekty wartości, zdarzenia domenowe); DDD jako opcja włączana decyzją w ADR (vicrafter, sekcja 18.4 specyfikacji).
- Architektura ewolucyjna: funkcje dopasowania (fitness functions) w CI, testy architektury (`dependency-cruiser`, ArchUnitTS, w Ruście `cargo-modules`, reguły `bans` w `cargo-deny`, granice crate’ów w workspace), strangler fig, branch by abstraction, warstwa antykorupcyjna, migracje inkrementalne z architekturą przejściową.
- Architektura SaaS: modele wielodostępności (silo, pula, model mieszany), izolacja danych na poziomie bazy, schematu lub wiersza (RLS, zob. sekcja 4), kontekst najemcy przekazywany przez wszystkie warstwy (cache, kolejki, pliki, logi), limity i „hałaśliwy sąsiad”, poziomy planów, onboarding najemcy.
- Wspólny rdzeń w Ruście dla wielu platform: podział na crate’y w workspace (domena, porty, adaptery, wiązania), API rdzenia jako kontrakt (zgrubne operacje, własne typy błędów, wersjonowanie), FFI jako granica architektoniczna (UniFFI do Swifta i Kotlina, komendy Tauri, WASM), wzorzec rdzeń i powłoka (np. Crux), co zostaje w powłoce platformowej; szczegóły w sekcjach 12, 14, 18 i 19.
- Odtwarzanie architektury z cudzego kodu: punkty wejścia i budowanie, graf zależności modułów, hotspoty (częstość zmian razy złożoność) i sprzężenie zmian z historii gita, mapa wiedzy (kto zna który moduł), C4 poziomu 1 i 2 oraz ADR w statusie „reconstructed”, rejestr długu technicznego z kosztem i ryzykiem, plan naprawczy w trzech horyzontach (natychmiast, 30, 90 dni), w tym wyjście z platformy no-code.
- Recenzja planów technicznych z AI: zgodność z konstytucją i bazowymi ADR, realne alternatywy zamiast „słomianych”, konsekwencje i koszt zmiany decyzji, wpływ na granice modułów i dane, plan migracji i wycofania, ryzyka, sprawdzenie w kodzie każdego twierdzenia planu o istniejącej strukturze.
- Typowe błędy architektoniczne w kodzie i planach z AI do wyłapania: logika biznesowa w komponentach UI, route handlerach i Server Actions zamiast w module domenowym; importy na skróty przez warstwy i cykle zależności; abstrakcje na zapas (interfejs z jedną implementacją, generyczne repozytoria, fabryki), czyli płytkie moduły; mikroserwisy, kolejki i Kubernetes dla systemu prowadzonego przez jedną osobę; ADR bez alternatyw albo z alternatywami odrzuconymi bez uzasadnienia; plan sprzeczny z istniejącymi ADR lub konstytucją; diagramy C4 z kontenerami, których nie ma w kodzie; propozycja „przepisać od zera” zamiast migracji inkrementalnej; izolacja najemców tylko w warunku `WHERE` w kodzie aplikacji i brak identyfikatora najemcy w kluczach cache, kolejkach i ścieżkach plików; rdzeń w Ruście przyjmujący typy platformy, „gadatliwe” API przez FFI (wiele drobnych wywołań), panika przechodząca przez granicę FFI; ta sama logika powielona w Swifcie, Kotlinie i TypeScripcie zamiast w rdzeniu; plan bez migracji danych i ścieżki wycofania.

### 8.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 8 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Dowody odpowiadają pracy w firmie: raport architektury przejmowanej aplikacji w 2 dni, bazowe ADR dla rdzenia własnej aplikacji, funkcja dopasowania w CI i plan migracji z platformy no-code. Przy doświadczeniu seniorskim etap 0 można zaliczyć samym dowodem, a etapy 4 i 5 warto przejść w całości, bo to rdzeń pakietu „Audyt przejęcia”. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem. Designing Data-Intensive Applications jest w sekcji 5.1 (etap 8), Working Effectively with Legacy Code w sekcji 6.1 (etap 4), ISO/IEC 25010 i zapis wymagań jakościowych w sekcji 7, Release It! w sekcji 9, a modelowanie zagrożeń w sekcji 10.1 (etap 3).

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | podstawy projektowania: złożoność, sprzężenie, modularność, wzorce | 40–50 h | podstawy |
| 1 | style architektoniczne, atrybuty jakości i analiza kompromisów | 70–90 h | W |
| 2 | dokumentowanie: C4, arc42, ADR, diagramy jako kod | 25–35 h | E |
| 3 | DDD strategiczne i event storming | 40–50 h | W |
| 4 | odtwarzanie architektury z cudzego kodu i rejestr długu | 40–50 h | E |
| 5 | architektura ewolucyjna: funkcje dopasowania i migracje inkrementalne | 40–50 h | E |
| 6 | architektura SaaS i wspólny rdzeń w Ruście | 40–50 h | E |
| 7 | ekspert: recenzja planów z AI, przeglądy architektury, aktualność | stale, ok. 2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 295–375 h, czyli 6–8 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: podstawy projektowania

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| A Philosophy of Software Design (wydanie 2, 2021) | John Ousterhout, Yaknyam Press | książka, średni | 8–10 h | płatna | https://web.stanford.edu/~ouster/cgi-bin/book.php |
| „A Philosophy of Software Design vs Clean Code” (dyskusja z lat 2024–2025) | John Ousterhout, Robert C. Martin | zapis dyskusji z przykładami kodu | 2–3 h | 0 zł | https://github.com/johnousterhout/aposd-vs-clean-code |
| Balancing Coupling in Software Design (2024) | Vlad Khononov, Addison-Wesley | książka, średni–zaawansowany | 12–15 h | płatna | https://www.informit.com/store/balancing-coupling-in-software-design-successful-software-9780137353484 |
| Design Patterns (katalog 22 wzorców z przykładami m.in. w TypeScript i Ruście) | Refactoring.Guru | katalog online | 8–10 h | 0 zł (e-book płatny) | https://refactoring.guru/design-patterns |
| Head First Design Patterns (wydanie 2, 2020) | Eric Freeman, Elisabeth Robson, O’Reilly | książka, od podstaw (alternatywa dla katalogu) | 15–20 h | płatna | https://www.oreilly.com/library/view/head-first-design/9781492077992/ |
| Rust Design Patterns (idiomy, wzorce, antywzorce) | rust-unofficial | książka online | 4–6 h | 0 zł | https://rust-unofficial.github.io/patterns/ |

Wystarczy jedno źródło wzorców: katalog Refactoring.Guru przy doświadczeniu programistycznym, Head First przy starcie od zera.

Szczególnie ważne: moduły głębokie (proste API, dużo ukrytej logiki) zamiast płytkich, ukrywanie informacji, przyczyny złożoności (zależności i niejasność), sprzężenie jako kompromis siły, odległości i zmienności, a nie wartość do zminimalizowania za wszelką cenę; SOLID jako heurystyki, które przy przesadzie tworzą abstrakcje na zapas; wzorce jako wspólny słownik w recenzji, a w Ruście najpierw idiomy (typy `enum`, `trait`, newtype, własność) zamiast hierarchii klas.

**Dowód:** w przejmowanej aplikacji Next.js (np. poligon z vibe codingu) jeden obszar z logiką rozlaną po komponentach i route handlerach przeniesiony do modułu domenowego z wąskim API, pod ochroną testów charakteryzujących (zob. sekcja 6.1, etap 4); krótka notatka przed i po: które zależności usunięto, które moduły były płytkie i dlaczego nowy podział zmniejsza koszt kolejnych zmian.

#### Etap 1: style architektoniczne, atrybuty jakości i kompromisy

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Fundamentals of Software Architecture (wydanie 2, marzec 2025) | Mark Richards, Neal Ford, O’Reilly | książka, średni–zaawansowany | 20–25 h | płatna | https://www.oreilly.com/library/view/fundamentals-of-software/9781098175504/ |
| Head First Software Architecture (2024) | Raju Gandhi, Mark Richards, Neal Ford, O’Reilly | książka, od podstaw (opcjonalnie) | 10–12 h | płatna | https://www.oreilly.com/library/view/head-first-software/9781098134341/ |
| Software Architecture: The Hard Parts (2021) | Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, O’Reilly | książka, zaawansowany | 15–20 h | płatna | https://www.oreilly.com/library/view/software-architecture-the/9781492086888/ |
| Designing Software Architectures: A Practical Approach (wydanie 2, 2024; ADD 3.0) | Humberto Cervantes, Rick Kazman, Addison-Wesley | książka, zaawansowany | 15–20 h | płatna | https://www.informit.com/store/designing-software-architectures-a-practical-approach-9780138108106 |
| „Hexagonal architecture” (artykuł źródłowy z 2005 r.) i książka Hexagonal Architecture Explained (zaktualizowane wydanie 1, 2025) | Alistair Cockburn, Juan Manuel Garrido de Paz | artykuł i książka | 1 h + 5–6 h | 0 zł / płatna | https://alistair.cockburn.us/hexagonal-architecture/, https://alistaircockburn.com/Books/ |
| „Master Hexagonal Architecture in Rust” (na przykładzie Axum) | Angus Morrison, How To Code It | przewodnik online | 4–6 h | 0 zł | https://www.howtocodeit.com/articles/master-hexagonal-architecture-rust |
| „Monolith First” (2015), „What do you mean by ‘Event-Driven’?” (2017) | Martin Fowler | artykuły | 1–2 h | 0 zł | https://martinfowler.com/bliki/MonolithFirst.html, https://martinfowler.com/articles/201701-event-driven.html |
| quality.arc42.org: katalog atrybutów jakości i przykładowych wymagań | arc42 | katalog online | 2–3 h | 0 zł | https://quality.arc42.org |
| AWS Well-Architected Framework (wersja z listopada 2024 r.) | Amazon Web Services | ramy i pytania kontrolne | 4–6 h | 0 zł | https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html |

Head First Software Architecture jest tylko dla osób startujących od zera; przy doświadczeniu wystarczy Fundamentals. Z „The Hard Parts” na tym etapie wystarczą rozdziały 1–3 i 15 (sprzężenie, modularność, własna analiza kompromisów); rozdziały o danych rozproszonych i sagach przydają się dopiero przy systemach rozproszonych. Local-first jako styl i jego narzędzia są w sekcji 4.1 (etap 3).

Szczególnie ważne: każdy styl oceniany przez charakterystyki (koszt, prostota, wdrażalność, skalowalność, odporność, testowalność), a nie przez modę; monolit modularny jako domyślny wybór dla jednej osoby i pierwsza odpowiedź na „czy potrzebujemy mikroserwisów”; porty i adaptery jako sposób na odcięcie logiki od frameworka, bazy i platformy; cztery znaczenia „event-driven” u Fowlera i koszt każdego z nich; scenariusz atrybutu jakości (bodziec, środowisko, odpowiedź, miara) jako sposób na zamianę „ma być szybkie” w driver decyzji; jawna lista kompromisów zamiast „najlepszej praktyki”; ADD 3.0 jako iteracyjny proces wyboru, a ATAM tylko jako źródło pytań, bo pełna ocena ATAM to praca zespołu przez kilka dni.

**Dowód:** dla własnej aplikacji (rdzeń w Ruście, web, desktop w Tauri, mobile) lista 5–7 driverów zapisanych jako scenariusze atrybutów jakości, mapa kompromisów między nimi i ADR wyboru stylu (np. monolit modularny z portami i adapterami kontra usługi kontra backend jako usługa), każdy z co najmniej dwiema realnymi alternatywami ocenionymi według charakterystyk z Fundamentals; do tego ta sama analiza dla jednej przejmowanej aplikacji klienta z odpowiedzią, czy obecny styl pasuje do jej driverów.

#### Etap 2: dokumentowanie

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Model C4: abstrakcje, diagramy, notacja, lista kontrolna recenzji diagramu | Simon Brown | dokumentacja | 4–5 h | 0 zł | https://c4model.com |
| The C4 Model: Visualizing Software Architecture (czerwiec 2026) | Simon Brown, O’Reilly | książka, średni | 6–8 h | płatna | https://www.oreilly.com/library/view/the-c4-model/9798341660113/ |
| arc42: szablon (Markdown, AsciiDoc), dokumentacja i przykłady dokumentacji prawdziwych systemów | Gernot Starke, Peter Hruschka i społeczność | szablon i przykłady | 4–5 h | 0 zł | https://arc42.org, https://examples.arc42.org |
| ADR: przegląd, szablony (MADR 4.0.0, Nygard, Y-statement) i narzędzia | społeczność ADR | szablony i przewodnik | 2–3 h | 0 zł | https://adr.github.io, https://adr.github.io/madr/ |
| „Documenting Architecture Decisions” (2011) i „Architecture Decision Record” (marzec 2026) | Michael Nygard, Martin Fowler | artykuły | 1 h | 0 zł | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions, https://martinfowler.com/bliki/ArchitectureDecisionRecord.html |
| Structurizr DSL i polecenie `local` | Simon Brown, Structurizr | dokumentacja narzędzia | 3–4 h | 0 zł | https://docs.structurizr.com/dsl |
| Diagramy C4 w Mermaid (wsparcie eksperymentalne) | Mermaid | dokumentacja | 1 h | 0 zł | https://mermaid.js.org/syntax/c4.html |
| „ARCHITECTURE.md” (2021) | Aleksey Kladov (matklad) | artykuł | 0,5 h | 0 zł | https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html |
| Documenting Software Architectures: Views and Beyond (wydanie 2, 2010) | Paul Clements i współautorzy (SEI), Addison-Wesley | książka referencyjna (opcjonalnie) | wg potrzeb | płatna | https://www.informit.com/store/documenting-software-architectures-views-and-beyond-9780321552686 |

Uwaga do Structurizr: Structurizr Lite, CLI, wersja on-premises i usługa w chmurze są oznaczone jako wycofywane; ich następcami są polecenia `local` (bezpłatne, open source, odpowiednik Lite), `export`, `push`, `pull` i `server`. Starsze poradniki oparte na Structurizr Lite trzeba czytać z tą poprawką. Diagramy C4 w Mermaid są oznaczone jako eksperymentalne, więc składnia może się zmienić.

Szczególnie ważne: C4 poziomu 1 i 2 wystarcza w raporcie przejęcia, a poziom 3 tylko dla modułów, które będą zmieniane; każdy diagram z legendą, tytułem i typem; ADR krótki (około strony), z kontekstem, co najmniej dwiema alternatywami, decyzją i konsekwencjami pozytywnymi i negatywnymi, przechowywany w repozytorium jako numerowany plik Markdown i zastępowany nowym ADR zamiast edycji; arc42 jako lista kontrolna treści, z której w małym projekcie wypełnia się tylko potrzebne sekcje; diagramy jako kod generowane z jednego modelu, żeby widoki nie rozjeżdżały się ze sobą i z kodem.

**Dowód:** szablon dokumentacji architektury do vicrafter i raportu przejęcia: skrócony arc42, `c4.md` z modelem w Structurizr DSL lub Mermaid (poziomy 1 i 2), szablon ADR oparty na MADR z polami statusu (w tym „reconstructed”) i odwołaniem do zastępowanego ADR, `ARCHITECTURE.md`; wypełniony dla własnej aplikacji z etapu 1 i sprawdzony listą kontrolną recenzji diagramu z c4model.com.

#### Etap 3: DDD strategiczne i event storming

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Learning Domain-Driven Design (2021) | Vlad Khononov, O’Reilly | książka, średni | 12–15 h | płatna | https://www.oreilly.com/library/view/learning-domain-driven-design/9781098100124/ |
| Domain-Driven Design Distilled (2016) | Vaughn Vernon, Addison-Wesley | książka, krótki przegląd (alternatywa) | 5–6 h | płatna | https://www.informit.com/store/domain-driven-design-distilled-9780134434421 |
| DDD Reference (definicje wzorców z książki Evansa i nowsze) | Eric Evans, Domain Language | materiał referencyjny | 2–3 h | 0 zł | https://www.domainlanguage.com/ddd/reference/ |
| DDD Crew: Context Mapping, Bounded Context Canvas, DDD Starter Modelling Process | DDD Crew | szablony i przewodniki | 4–5 h | 0 zł | https://github.com/ddd-crew/context-mapping, https://github.com/ddd-crew/bounded-context-canvas, https://github.com/ddd-crew/ddd-starter-modelling-process |
| Introducing EventStorming (niedokończona, ok. 70%, ostatnia aktualizacja 2021) | Alberto Brandolini, Leanpub | książka | 8–10 h | płatna | https://leanpub.com/introducing_eventstorming |
| EventStorming: opis formatów warsztatu i zestaw startowy | Avanscoperta | strona i materiały | 1–2 h | 0 zł | https://www.eventstorming.com |

Wystarczy jedna z dwóch książek: Learning Domain-Driven Design jako podstawa (zawiera też rozdział o event stormingu i studium przypadku), DDD Distilled tylko jako szybki przegląd.

Szczególnie ważne: najpierw subdomeny i ich typ (kluczowa, wspierająca, ogólna), bo od tego zależy, gdzie inwestować w projektowanie, a co kupić lub uprościć; bounded context jako granica modelu i języka, a nie mikroserwis; wzorce mapy kontekstów, zwłaszcza warstwa antykorupcyjna przy integracji z platformą no-code lub cudzym API; słownik terminów jako wspólny język specyfikacji, kodu i rozmów z klientem; event storming w wersji zdalnej (Miro, Excalidraw) jako narzędzie discovery z klientem; taktyczne DDD (agregaty, zdarzenia domenowe) tylko tam, gdzie domena ma dużo reguł, a nie w CRUD.

**Dowód:** dwugodzinna sesja event stormingu (z klientem albo na poligonie) dla jednego procesu przejmowanej aplikacji, z zapisem zdarzeń, poleceń i reguł; na jej podstawie `glossary.md`, `context-map.md` z nazwanymi wzorcami relacji i Bounded Context Canvas dla kontekstu kluczowego; ADR, który włącza albo świadomie odrzuca DDD dla tego projektu (zgodnie z opcją DDD w vicrafter), z uzasadnieniem.

#### Etap 4: odtwarzanie architektury z cudzego kodu

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Your Code as a Crime Scene (wydanie 2, luty 2024) | Adam Tornhill, Pragmatic Bookshelf | książka, średni–zaawansowany | 12–15 h | płatna | https://pragprog.com/titles/atcrime2/your-code-as-a-crime-scene-second-edition/ |
| code-maat (analiza historii repozytorium z linii poleceń, GPL-3.0) | Adam Tornhill | narzędzie | 3–4 h | 0 zł | https://github.com/adamtornhill/code-maat |
| CodeScene: hotspoty, zdrowie kodu, sprzężenie zmian | CodeScene | narzędzie (Community Edition dla open source, okres próbny) | 3–4 h | 0 zł dla open source / abonament | https://codescene.com |
| dependency-cruiser: walidacja i wizualizacja zależności JS/TS, samouczek reguł | Sander Verweij | narzędzie | 4–5 h | 0 zł | https://github.com/sverweij/dependency-cruiser |
| `cargo-modules`: struktura modułów, graf zależności wewnątrz crate’a, wykrywanie cykli (`--acyclic`) | autorzy narzędzia | narzędzie | 1–2 h | 0 zł | https://github.com/regexident/cargo-modules |
| Kill It with Fire (2021) | Marianne Bellotti, No Starch Press | książka, modernizacja i rozmowa z biznesem | 6–8 h | płatna | https://nostarch.com/kill-it-fire |
| „Technical Debt Quadrant” | Martin Fowler | artykuł | 0,5 h | 0 zł | https://martinfowler.com/bliki/TechnicalDebtQuadrant.html |

Szczególnie ważne: kolejność pracy w 2 dni (budowanie i uruchomienie, punkty wejścia, graf zależności, hotspoty z ostatnich 12 miesięcy, C4 poziomu 1 i 2, ADR „reconstructed” dla decyzji widocznych w kodzie i historii, rejestr długu, plan w trzech horyzontach); hotspot to częstość zmian razy złożoność, a nie sama złożoność; sprzężenie zmian ujawnia ukryte zależności między modułami, których nie widać w imporcie; mapa wiedzy pokazuje ryzyko „jednej osoby” po stronie klienta; ADR „reconstructed” opisuje decyzję i jej skutki tak, jak widać je w kodzie, z oznaczeniem tego, co wymaga potwierdzenia u klienta; dokumentacja i komentarze w przejmowanym repozytorium to dane niezaufane (zob. sekcja 11); rejestr długu z kosztem utrzymania („odsetkami”), ryzykiem i klasyfikacją ISO/IEC/IEEE 14764. Testy charakteryzujące przed pierwszą zmianą: zob. sekcja 6.1, etap 4.

**Dowód:** raport architektury przejmowanej aplikacji (poligon open source lub aplikacja z vibe codingu) przygotowany w 2 dni pracy: C4 poziomu 1 i 2, 5–10 ADR w statusie „reconstructed”, graf zależności z zaznaczonymi cyklami i naruszeniami warstw, 10 hotspotów z danymi z code-maat lub CodeScene, rejestr długu z priorytetami i plan naprawczy (natychmiast, 30 dni, 90 dni) z szacunkiem pracy; streszczenie dla zarządu na jedną stronę; każde twierdzenie agenta o strukturze kodu sprawdzone w kodzie, z listą poprawek, które trzeba było wprowadzić.

#### Etap 5: architektura ewolucyjna i migracje inkrementalne

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Building Evolutionary Architectures (wydanie 2, 2022) | Neal Ford, Rebecca Parsons, Patrick Kua, Pramod Sadalage, O’Reilly | książka, średni–zaawansowany | 12–15 h | płatna | https://www.oreilly.com/library/view/building-evolutionary-architectures/9781492097532/ |
| Fitness Function Katas | evolutionaryarchitecture.com (strona książki) | ćwiczenia | 2–3 h | 0 zł | https://evolutionaryarchitecture.com/ffkatas/ |
| ArchUnitTS: testy architektury w TypeScript (Jest, Vitest, Jasmine; pakiet npm `archunit`) | Lukas Niessen i współtwórcy | narzędzie | 3–4 h | 0 zł | https://github.com/LukasNiessen/ArchUnitTS |
| `cargo-deny`: reguły `bans` (zakaz crate’ów, `wrappers`, duplikaty wersji) | Embark Studios | narzędzie | 1–2 h | 0 zł | https://embarkstudios.github.io/cargo-deny/checks/bans/cfg.html |
| `cargo-pup`: asercje architektury w Ruście inspirowane ArchUnit (wersja 0.1, wymaga nightly) | Datadog | narzędzie (eksperymentalne, opcjonalnie) | 1–2 h | 0 zł | https://github.com/DataDog/cargo-pup |
| Monolith to Microservices (2019), rozdziały 2–4 (strangler fig, branch by abstraction, dekompozycja bazy) | Sam Newman, O’Reilly | książka, średni | 8–10 h | płatna | https://www.oreilly.com/library/view/monolith-to-microservices/9781492047834/ |
| „Strangler Fig” (sierpień 2024) i „Patterns of Legacy Displacement” | Martin Fowler; Ian Cartwright, Rob Horn, James Lewis | artykuły i katalog wzorców | 3–4 h | 0 zł | https://martinfowler.com/bliki/StranglerFigApplication.html, https://martinfowler.com/articles/patterns-legacy-displacement/ |
| Strangler Fig pattern (z migracją bazy przez CDC) | Microsoft, Azure Architecture Center | opis wzorca | 1 h | 0 zł | https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig |

Szczególnie ważne: funkcja dopasowania jako automatyczny, obiektywny test cechy architektury (kierunek zależności, brak cykli, brak importu bazy w warstwie UI, budżet rozmiaru paczki, opóźnienie), uruchamiana w CI jako bramka (zob. sekcja 9); granice modułów w TypeScript przez `dependency-cruiser` lub ArchUnitTS, w Ruście najpewniej przez podział na crate’y w workspace (kompilator nie pozwoli na zależność, której nie ma w `Cargo.toml`) i reguły `cargo-deny`; strangler fig z fasadą, która przekierowuje kolejne ścieżki do nowego systemu, i warstwą antykorupcyjną, żeby nowy kod nie przejął modelu starego; architektura przejściowa jako świadomy koszt; migracja danych expand–contract (zob. sekcja 4.1, etap 5); możliwość wycofania na każdym kroku.

**Dowód:** dwie funkcje dopasowania w CI przejmowanej aplikacji (np. reguła `dependency-cruiser` lub ArchUnitTS zakazująca importu klienta bazy w komponentach UI i reguła wykrywająca cykle), najpierw w trybie raportu dla istniejących naruszeń, potem jako bramka dla nowych; plan migracji strangler fig z aplikacji no-code (np. Bubble albo frontend z generatora na Supabase) do własnego kodu: fasada, kolejność przenoszenia funkcji według wartości i ryzyka, warstwa antykorupcyjna, migracja danych, kryteria wyłączenia starej części i plan wycofania dla każdego kroku, zapisany jako ADR i plan w trzech horyzontach.

#### Etap 6: architektura SaaS i wspólny rdzeń w Ruście

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Building Multi-Tenant SaaS Architectures (2024) | Tod Golding, O’Reilly | książka, średni–zaawansowany | 15–18 h | płatna | https://www.oreilly.com/library/view/building-multi-tenant-saas/9781098140632/ |
| Architect multitenant solutions on Azure: rozważania architektoniczne i modele wielodostępności | Microsoft, Azure Architecture Center | przewodnik (wiedza niezależna od Azure) | 4–6 h | 0 zł | https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/overview, https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models |
| SaaS Lens (AWS Well-Architected) | Amazon Web Services | lista kontrolna | 2–3 h | 0 zł | https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/saas-lens.html |
| Crux: rdzeń w Ruście i powłoki w Swift, Kotlin i TypeScript (przed wersją 1.0) | Red Badger i społeczność | dokumentacja i architektura referencyjna | 6–8 h | 0 zł | https://redbadger.github.io/crux/ |
| „Large Rust Workspaces” (2021) | Aleksey Kladov (matklad) | artykuł | 0,5 h | 0 zł | https://matklad.github.io/2021/08/22/large-rust-workspaces.html |

Wiązania UniFFI, `cbindgen` i komendy Tauri są w sekcjach 12.1 (etap 6), 14.1, 18.1 (etap 4) i 19.1 (etap 4); izolacja najemców przez RLS w sekcji 4.1 (etap 2), a w autoryzacji w sekcji 5.1 (etap 5). Tu chodzi o decyzje, nie o mechanikę.

Szczególnie ważne: wybór modelu wielodostępności (osobne wdrożenie, osobna baza, wspólna baza z RLS) jako kompromis izolacji, kosztu i obsługi przez jedną osobę; kontekst najemcy ustalany raz na wejściu i przekazywany jawnie przez wszystkie warstwy, także do cache, kolejek, plików i logów; limity na najemcę i ochrona przed „hałaśliwym sąsiadem”; poziomy planów jako konfiguracja, a nie rozgałęzienia w kodzie; w rdzeniu Rust domena i porty bez zależności od platformy, adaptery i wiązania w osobnych crate’ach; API rdzenia zgrubne i stabilne (mało wywołań przez FFI, własne typy błędów zamiast paniki), wersjonowane jak kontrakt; co zostaje w powłoce (UI, cykl życia, płatności w sklepach, uprawnienia systemowe), a co w rdzeniu (model danych, reguły, synchronizacja, licencje).

**Dowód:** zestaw bazowych ADR dla rdzenia własnej aplikacji: podział na crate’y (domena, porty, adaptery, wiązania), API rdzenia z kontraktem błędów i zasadą wersjonowania, granica FFI dla UniFFI i Tauri, model wielodostępności backendu z uzasadnieniem i testem izolacji najemców; funkcja dopasowania w CI, która pilnuje, że crate domeny nie zależy od żadnego crate’a platformowego ani frameworka; diagram C4 poziomu 2 i 3 dla rdzenia w modelu z etapu 2.

#### Etap 7: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| „Exploring Generative AI” (seria notatek o pracy z agentami, m.in. spec-driven development) | Birgitta Böckeler i inni autorzy Thoughtworks, martinfowler.com | artykuły | ok. 0,5 h tygodniowo | 0 zł | https://martinfowler.com/articles/exploring-gen-ai.html |
| „Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl” (październik 2025) | Birgitta Böckeler | artykuł | 1 h | 0 zł | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html |
| Technology Radar (dwa wydania w roku) | Thoughtworks | przegląd technik i narzędzi | ok. 2 h na wydanie | 0 zł | https://www.thoughtworks.com/radar |
| Software Architecture in Practice (wydanie 4, 2021) | Len Bass, Paul Clements, Rick Kazman, Addison-Wesley | książka referencyjna, zaawansowany | wg potrzeb | płatna | https://www.informit.com/store/software-architecture-in-practice-9780136886099 |
| Kursy i wystąpienia o architekturze | O’Reilly | platforma | wg potrzeb | abonament | https://www.oreilly.com |

Uwaga: na luty 2027 r. zapowiedziana jest książka „Architecture as Code” (Neal Ford, Mark Richards, Jonathan Johnson, O’Reilly) o opisywaniu architektury językiem deklaratywnym i jej pilnowaniu przez agentów AI i funkcje dopasowania; spis treści jest jeszcze roboczy, więc przed zakupem trzeba sprawdzić wydaną wersję.

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja planów z AI:** 20 planów technicznych (`plan.md`) i ADR przygotowanych przez agenta w vicrafter, recenzowanych według listy kontrolnej z tej sekcji (zgodność z konstytucją i bazowymi ADR, realne alternatywy, konsekwencje, granice modułów, model najemców, granica FFI, migracja i wycofanie, twierdzenia o kodzie sprawdzone w kodzie); zapis, które błędy wychwyciła recenzja na innym modelu, a które tylko człowiek (zob. sekcja 11),
- **przeglądy architektury u klientów:** każdy raport przejęcia z porównaniem planu w trzech horyzontach z tym, co faktycznie zrobiono po 30 i 90 dniach, i wnioskami do szablonu raportu,
- **pielęgnacja decyzji:** raz na kwartał przegląd ADR własnych aplikacji: które decyzje się zestarzały, które trzeba zastąpić nowym ADR, które funkcje dopasowania przestały cokolwiek pilnować,
- **architektura na papierze bez agenta:** raz w miesiącu szkic C4 i ADR dla nowego problemu wykonany samodzielnie, a dopiero potem porównany z propozycją agenta,
- **wkład w open source** w jednym narzędziu z tej sekcji (np. `dependency-cruiser`, ArchUnitTS, `cargo-modules`, szablony arc42 lub DDD Crew), choćby w dokumentację lub przykłady.

**Dowód poziomu E:** samodzielnie, bez agenta, w 2 dni przygotowujesz dla nieznanej aplikacji klienta raport architektury z C4 poziomu 1 i 2, ADR w statusie „reconstructed”, rejestrem długu opartym na hotspotach i planem naprawczym w trzech horyzontach, w tym wariantem migracji strangler fig; w recenzji planu technicznego przygotowanego przez agenta wskazujesz błąd architektoniczny, którego nie znalazł recenzent AI, i umiesz wyjaśnić klientowi nietechnicznemu, jakie kompromisy niesie każda z rekomendowanych decyzji.

---

## 9. DevOps, CI/CD i wydania

*Warstwa 2: jakość i projektowanie. Opiera się na: 2 i 6. Jest podstawą: 10, 11 oraz wydań w sekcjach 14–19.*

- GitHub Actions: macierze systemów i targetów, runnery macOS i Windows, cache (`sccache`, `Swatinem/rust-cache`), sekrety i OIDC do chmury.
- Bramki jakości: testy, lint, `clippy`, typecheck, SAST, SCA, SBOM jako warunek scalenia i wydania.
- Automatyzacja wydań: wersjonowanie semantyczne, Conventional Commits, changelog, `tauri-action`, fastlane lub API App Store Connect i Google Play.
- Podpisy w CI: certyfikaty Apple, Windows, klucze aktualizacji Tauri, klucze Androida, GPG dla Linuksa; bezpieczne przechowywanie kluczy.
- Pochodzenie i integralność artefaktów: powtarzalne buildy, SLSA, podpisy Sigstore/cosign.
- Infrastruktura: Linux, Docker, sieci, DNS, TLS, SPF/DKIM/DMARC; czytanie planów Terraform i manifestów Kubernetes.
- Obserwowalność: OpenTelemetry, logi, metryki, SLO, alerty; raportowanie awarii (np. Sentry) z symbolami dSYM, PDB i plików mapowania.
- Koszty: limity i alerty budżetowe w chmurze i u dostawców AI.

### 9.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 7 etapów, numerowanych od 1, bo podstawy Linuksa, powłoki, Gita i sieci są w sekcji 2.1. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przy doświadczeniu seniorskim etap 1 można zaliczyć samym dowodem i wracać do materiałów tylko tam, gdzie dowód nie wychodzi; nowe będą najpewniej wydania na wiele platform (etap 4), pochodzenie artefaktów (etap 5) i SRE (etap 6). Narzędzia SAST, SCA i generowania SBOM są w sekcji 10, a szczegóły podpisów platformowych w sekcjach 15–17; tutaj chodzi o ich wpięcie w pipeline. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 1 | kontenery i infrastruktura jako kod (czytanie) | 30–40 h | podstawy |
| 2 | GitHub Actions i bezpieczeństwo pipeline’u | 30–40 h | W |
| 3 | ciągłe dostarczanie i bramki jakości | 30–40 h | W |
| 4 | wydania: wersjonowanie, changelog, wiele platform, aktualizacje | 40–50 h | W |
| 5 | pochodzenie i integralność artefaktów: SLSA, Sigstore, powtarzalne buildy | 20–30 h | W |
| 6 | obserwowalność, SLO, incydenty | 40–50 h | E |
| 7 | ekspert: recenzja pipeline’ów z AI, ćwiczenia awarii, aktualność | stale, ok. 1–2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 190–250 h, czyli 4–6 miesięcy przy 10–12 h tygodniowo.

#### Etap 1: kontenery i infrastruktura jako kod

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Docker: Get started (pojęcia, budowa obrazów, wieloetapowe buildy) | Docker | dokumentacja | 8–10 h | 0 zł | https://docs.docker.com/get-started/ |
| Terraform Tutorials | HashiCorp | samouczki | 10–12 h | 0 zł | https://developer.hashicorp.com/terraform/tutorials |
| Kubernetes: Concepts (czytanie manifestów, bez administrowania klastrem) | Kubernetes | dokumentacja | 8–10 h | 0 zł | https://kubernetes.io/docs/concepts/ |

Szczególnie ważne: małe obrazy dla binarek Rusta (wieloetapowy build, obraz bazowy distroless lub `scratch`), użytkownik bez roota w kontenerze, czytanie `terraform plan` przed zatwierdzeniem zmian proponowanych przez agenta, stan Terraform i sekrety.

**Dowód:** usługa z sekcji 2.1, etap 0, w obrazie poniżej 30 MB uruchamianym bez roota; infrastruktura (serwer, DNS, bucket na kopie zapasowe) opisana w Terraform, z przejrzanym i skomentowanym planem zmian.

#### Etap 2: GitHub Actions i bezpieczeństwo pipeline’u

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| GitHub Actions: dokumentacja, w tym macierze jobów | GitHub | dokumentacja | 10–12 h | 0 zł | https://docs.github.com/en/actions |
| Secure use reference (dawniej „Security hardening for GitHub Actions”) | GitHub | dokumentacja | 3–4 h | 0 zł | https://docs.github.com/en/actions/reference/security/secure-use |
| OpenID Connect w GitHub Actions | GitHub | dokumentacja | 2–3 h | 0 zł | https://docs.github.com/en/actions/concepts/security/openid-connect |
| `Swatinem/rust-cache`, `sccache` | autorzy narzędzi | dokumentacja | 2–3 h | 0 zł | https://github.com/Swatinem/rust-cache, https://github.com/mozilla/sccache |

Szczególnie ważne: akcje przypięte do pełnego SHA, minimalne uprawnienia `GITHUB_TOKEN` (domyślnie tylko odczyt), ryzyko `pull_request_target` i `workflow_run`, wstrzykiwanie poleceń przez dane z `github.event`, OIDC zamiast długotrwałych kluczy do chmury, środowiska z wymaganym zatwierdzeniem dla sekretów do podpisów.

**Dowód:** workflow budujący rdzeń w Ruście w macierzy Linux, macOS i Windows z cache; wszystkie akcje przypięte do SHA, uprawnienia ustawione per job, wdrożenie do chmury przez OIDC bez zapisanych kluczy; lista kontrolna bezpieczeństwa workflow zastosowana do jednego publicznego repozytorium.

#### Etap 3: ciągłe dostarczanie i bramki jakości

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Continuous Delivery | Jez Humble, David Farley, Addison-Wesley | książka, średni | 15–20 h | płatna | https://www.informit.com/store/continuous-delivery-reliable-software-releases-through-build-9780321601919 |
| Accelerate | Nicole Forsgren, Jez Humble, Gene Kim, IT Revolution | książka, średni | 6–8 h | płatna | https://itrevolution.com/product/accelerate/ |
| DORA: metryki dostarczania i raporty badawcze (m.in. o AI w wytwarzaniu oprogramowania) | DORA (Google Cloud) | raporty, artykuły | 4–6 h | 0 zł | https://dora.dev |

Szczególnie ważne: jeden pipeline jako jedyna droga do produkcji, artefakt budowany raz i promowany między środowiskami, bramki jako warunek scalenia (testy, lint, `clippy`, typecheck, SAST, SCA, SBOM; narzędzia w sekcji 10), cztery metryki DORA mierzone także dla pracy agentów.

**Dowód:** szablon pipeline’u gotowy do wdrożenia u klienta: bramki jakości jako wymagane sprawdzenia w ochronie gałęzi, SBOM w CycloneDX dołączany do każdego buildu, raport bramek w opisie pull requesta, krótka instrukcja wdrożenia szablonu w repozytorium klienta.

#### Etap 4: wydania na wiele platform

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Semantic Versioning 2.0.0, Conventional Commits 1.0.0 | Tom Preston-Werner; społeczność Conventional Commits | specyfikacje | 2 h | 0 zł | https://semver.org, https://www.conventionalcommits.org/en/v1.0.0/ |
| release-plz (wydania crate’ów przez PR z changelogiem) i `cargo-semver-checks` | Marco Ieni; Predrag Gruevski | dokumentacja | 3–4 h | 0 zł | https://release-plz.dev, https://github.com/obi1kenobi/cargo-semver-checks |
| dist (dawniej cargo-dist): instalatory i wydania narzędzi CLI | axo | dokumentacja | 3–4 h | 0 zł | https://axodotdev.github.io/cargo-dist/book/ |
| Tauri: GitHub pipeline (`tauri-action`) i plugin Updater | zespół Tauri | dokumentacja | 5–6 h | 0 zł | https://v2.tauri.app/distribute/pipelines/github/, https://v2.tauri.app/plugin/updater/ |
| fastlane (w tym `match` do certyfikatów Apple) | społeczność fastlane | dokumentacja | 6–8 h | 0 zł | https://docs.fastlane.tools |

Szczególnie ważne: wersja wynikająca z historii commitów, a nie z ręcznej decyzji agenta; klucz podpisu aktualizacji Tauri (utrata oznacza brak aktualizacji dla zainstalowanych kopii, więc kopia zapasowa poza CI); podpisy i notaryzacja wykonywane w CI z sekretami w środowisku chronionym (szczegóły platform w sekcjach 19, 15–17); ścieżki testowe sklepów przed produkcją.

**Dowód:** wydanie aplikacji Tauri na Linux, macOS i Windows z jednego tagu: podpisane instalatory, plik aktualizacji dla Updatera, changelog z Conventional Commits; zainstalowana starsza wersja aktualizuje się automatycznie, a zmodyfikowana paczka aktualizacji jest odrzucana; build mobilny wysłany przez fastlane do TestFlight i ścieżki testów wewnętrznych Google Play.

#### Etap 5: pochodzenie i integralność artefaktów

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| SLSA Specification v1.2 | OpenSSF | specyfikacja | 4–6 h | 0 zł | https://slsa.dev/spec/v1.2/ |
| Sigstore (cosign, Fulcio, Rekor) | OpenSSF | dokumentacja | 4–6 h | 0 zł | https://docs.sigstore.dev |
| GitHub Artifact attestations | GitHub | dokumentacja | 2 h | 0 zł | https://docs.github.com/en/actions/concepts/security/artifact-attestations |
| Reproducible Builds: dokumentacja (`SOURCE_DATE_EPOCH`, uwagi dla Rusta) | projekt Reproducible Builds | dokumentacja | 4–6 h | 0 zł | https://reproducible-builds.org/docs/ |

Szczególnie ważne: poziomy SLSA Build (atestacje GitHub dają poziom 2, poziom 3 wymaga wielokrotnego workflow izolującego build), weryfikacja atestacji i podpisów po stronie odbiorcy, a nie tylko ich wystawienie; powtarzalność jako dowód, że binarka odpowiada kodowi źródłowemu, co wspiera dokumentację techniczną wymaganą przez CRA.

**Dowód:** artefakty wydania z etapu 4 z atestacją pochodzenia i podpisem Sigstore, SBOM dołączonym do wydania i instrukcją weryfikacji dla klienta (`gh attestation verify` lub `cosign verify-blob`); binarka CLI w Ruście zbudowana dwa razy w różnych środowiskach z identyczną sumą kontrolną.

#### Etap 6: obserwowalność, SLO i incydenty

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Site Reliability Engineering, m.in. rozdziały 4 (SLO), 6 (monitorowanie), 14 („Managing Incidents”), 15 („Postmortem Culture”) | Google, O’Reilly | książka online | 12–15 h | 0 zł online | https://sre.google/sre-book/table-of-contents/ |
| The Site Reliability Workbook, rozdziały 2 („Implementing SLOs”) i 5 („Alerting on SLOs”) | Google, O’Reilly | książka online | 6–8 h | 0 zł online | https://sre.google/workbook/table-of-contents/ |
| Observability Engineering (wydanie 2, czerwiec 2026) | Charity Majors, Liz Fong-Jones, George Miranda, O’Reilly | książka, średni–zaawansowany | 12–15 h | płatna (darmowy egzemplarz oferuje Honeycomb) | https://www.oreilly.com/library/view/-/9781098179915/ |
| OpenTelemetry: pojęcia, Collector, Rust | OpenTelemetry (CNCF) | dokumentacja | 6–8 h | 0 zł | https://opentelemetry.io/docs/ |
| Sentry: SDK dla Rusta i plików debugowania (dSYM, PDB, mapowanie ProGuard) | Sentry | dokumentacja | 4–5 h | 0 zł (usługa: plan darmowy i płatne) | https://docs.sentry.io/platforms/rust/, https://docs.sentry.io/cli/dif/ |

Szczególnie ważne: SLO i budżet błędów zamiast alertów na każdą metrykę, alerty wielookienkowe według tempa zużycia budżetu (burn rate), `tracing` w Ruście z eksportem do OpenTelemetry, symbole debugowania wysyłane w pipeline wydania, postmortem bez szukania winnych, zgłaszanie aktywnie wykorzystywanych podatności i poważnych incydentów w terminach CRA (od 11 września 2026 r.).

**Dowód:** usługa produkcyjna z SLO dostępności i opóźnienia, alertem burn rate wysyłanym na telefon, śladami OpenTelemetry i raportami awarii z symbolami z aplikacji desktopowej; ćwiczenie awarii zakończone postmortemem według szablonu z SRE Book, z czasem wykrycia i przywrócenia.

#### Etap 7: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| GitHub Changelog i komunikaty bezpieczeństwa GitHub Actions | GitHub | źródła pierwotne | ok. 30 min tygodniowo | 0 zł | https://github.blog/changelog/ |
| Release It! (wydanie 2) | Michael Nygard, Pragmatic Bookshelf | książka, zaawansowany | 12–15 h | płatna | https://pragprog.com/titles/mnee2/release-it-second-edition/ |
| Implementing Service Level Objectives | Alex Hidalgo, O’Reilly | książka, zaawansowany | 12–15 h | płatna | https://www.oreilly.com/library/view/implementing-service-level/9781492076803/ |
| Building Secure and Reliable Systems | Google, O’Reilly | książka online, zaawansowany | wg potrzeb | 0 zł online | https://google.github.io/building-secure-and-reliable-systems/raw/toc.html |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja pipeline’ów z AI:** 20 zmian w workflow, Dockerfile i Terraform wygenerowanych przez agentów, recenzowanych według listy kontrolnej z etapów 2, 3 i 5 (akcje nieprzypięte do SHA, nadmiarowe uprawnienia, sekrety w logach lub argumentach, wyłączone lub warunkowo pomijane bramki, `continue-on-error` na krokach jakości, cache zatruwany z gałęzi pull requestów, `terraform apply` bez przeglądu planu),
- **ćwiczenie wydania awaryjnego:** poprawka podatności od zgłoszenia do podpisanego wydania na wszystkich platformach w 24 h, z zaktualizowanym SBOM i komunikatem dla użytkowników,
- **ćwiczenie odtworzenia:** odtworzenie infrastruktury i kluczy podpisu z kopii zapasowych na czystym koncie,
- **wkład w open source** w jednym narzędziu wydań lub akcji GitHub z ekosystemu Rusta lub Tauri.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień wdrażasz szablon pipeline’u u klienta (bramki, SBOM, podpisane wydanie, monitoring z alertem SLO), diagnozujesz nieudane wydanie lub fałszywy alarm na podstawie logów i śladów, i umiesz wyjaśnić osobie nietechnicznej, co pipeline gwarantuje, a czego nie.

---

## 10. Bezpieczeństwo

*Warstwa 3: ochrona i kontrola. Opiera się na: 3, 4, 5, 8 i 9; części platformowe dochodzą przy sekcjach 14–22. Jest podstawą: 11, 20, 21 i 22.*

- Web i API: OWASP ASVS (poziom 1 i wybrane wymagania poziomu 2), OWASP Top 10 i API Top 10, nagłówki bezpieczeństwa, CSP.
- Mobile: OWASP MASVS i MASTG, pinning certyfikatów, przechowywanie sekretów, inżynieria wsteczna aplikacji.
- Desktop: zakres capabilities w Tauri, walidacja wejścia w poleceniach IPC, podpis aktualizacji, uprawnienia systemowe.
- Embedded: secure boot, podpis firmware, ochrona kluczy, interfejsy debugowania, aktualizacje bez możliwości cofnięcia do podatnej wersji.
- Łańcuch dostaw: SBOM w CycloneDX (`cargo-cyclonedx`, `cargo-auditable`, narzędzia dla npm), `cargo-audit`, `cargo-deny`, `cargo-vet`, `osv-scanner`, Dependabot lub Renovate; priorytety według CVSS, EPSS i KEV.
- Narzędzia: gitleaks, Semgrep, CodeQL, OWASP ZAP; `cargo-geiger` do mapy kodu `unsafe`.
- Modelowanie zagrożeń STRIDE i LINDDUN dla każdej klasy aplikacji.
- Ryzyka specyficzne dla AI: zależności wymyślone przez model i podszywające się pod nie pakiety (typosquatting), prompt injection w treściach z repozytorium, agenci bez poświadczeń produkcyjnych.

### 10.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 9 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Dowody odpowiadają usługom z biznesplanu: audyt według ASVS, model zagrożeń, triage podatności i zgłoszenie w trybie CRA. Przy doświadczeniu seniorskim etap 0 można zaliczyć samym dowodem, ale etapy 2, 5 i 6 warto przejść w całości, bo to rdzeń niszy „rescue & hardening”. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem. Ściągawki OWASP o XSS, CSP i sesjach są w etapie 6 ścieżki frontendowej (zob. sekcja 3.1), testy w sekcji 6, a bramki CI w sekcji 9.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | podstawy bezpieczeństwa aplikacji i bezpiecznego kodowania | 40–60 h | podstawy |
| 1 | ataki na web i API w praktyce | 80–100 h | W |
| 2 | standardy i audyt: ASVS, Top 10, API Top 10 | 40–50 h | E |
| 3 | modelowanie zagrożeń: STRIDE i LINDDUN | 25–35 h | W |
| 4 | narzędzia: SAST, DAST, wykrywanie sekretów | 30–40 h | W |
| 5 | łańcuch dostaw: SBOM, zależności, `cargo-vet` | 30–40 h | E |
| 6 | obsługa podatności i CRA: CVSS, EPSS, KEV, zgłoszenia | 30–40 h | E |
| 7 | mobile, desktop, Rust i embedded | 50–70 h | W |
| 8 | ekspert: audyty klientów, badania, aktualność | stale, ok. 2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 330–440 h, czyli 7–10 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: podstawy bezpieczeństwa aplikacji

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Developing Secure Software (LFD121) | OpenSSF, Linux Foundation | kurs online z egzaminem i certyfikatem | 14–18 h | 0 zł | https://openssf.org/training/courses/ |
| Alice and Bob Learn Application Security (Wiley 2020; wydanie polskie „Alicja i Bob. Bezpieczeństwo aplikacji w praktyce”, Helion/Onepress 2021) | Tanya Janca | książka, od podstaw | 12–15 h | płatna | https://shehackspurple.ca/books/ |
| Alice and Bob Learn Secure Coding (Wiley 2025) | Tanya Janca | książka, średni | 12–15 h | płatna | https://shehackspurple.ca/books/ |

Wystarczy jedna z dwóch książek Tanyi Janki: „Application Security” przy starcie od zera, „Secure Coding” przy doświadczeniu programistycznym.

Szczególnie ważne: zasada najmniejszych uprawnień, obrona warstwowa, walidacja wejścia i kodowanie wyjścia, bezpieczne wartości domyślne, zarządzanie sekretami, różnica między uwierzytelnianiem a autoryzacją.

**Dowód:** certyfikat ukończenia LFD121 oraz lista 15 typowych błędów bezpieczeństwa w kodzie generowanym przez AI, każdy z przykładem w TypeScript lub Ruście i poprawką.

#### Etap 1: ataki na web i API w praktyce

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Web Security Academy (ścieżki nauki i laboratoria) | PortSwigger | kurs interaktywny z laboratoriami, od podstaw do zaawansowanego | 50–60 h | 0 zł | https://portswigger.net/web-security |
| OWASP Juice Shop i przewodnik „Pwning OWASP Juice Shop” | OWASP | celowo podatna aplikacja (Node.js, Express, Angular) | 15–20 h | 0 zł | https://owasp.org/www-project-juice-shop/, https://pwning.owasp-juice.shop |
| Real-World Bug Hunting: A Field Guide to Web Hacking | Peter Yaworski, No Starch Press (2019) | książka, studia przypadków z programów bug bounty | 10–12 h | płatna | https://nostarch.com/bughunting |

Szczególnie ważne: kontrola dostępu do obiektów (IDOR, BOLA), SSRF, wstrzyknięcia (SQL, polecenia systemowe, szablony), XSS i CSRF, błędy logiki biznesowej, ataki na OAuth i JWT, wyścigi (race conditions); w laboratoriach PortSwigger przede wszystkim kategorie „Access control”, „Authentication”, „SSRF” i „Business logic vulnerabilities”.

**Dowód:** 30 rozwiązanych laboratoriów Web Security Academy (w tym co najmniej 10 na poziomie „Practitioner”) i 40 wyzwań Juice Shop; dla 5 z nich notatka: przyczyna w kodzie, poprawka i test regresyjny.

#### Etap 2: standardy i audyt

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| OWASP ASVS 5.0.0 (wydanie z 30 maja 2025 r., poziomy L1–L3) | OWASP | standard weryfikacji | 20–25 h | 0 zł | https://owasp.org/www-project-application-security-verification-standard/, https://github.com/OWASP/ASVS |
| OWASP Top 10:2025 | OWASP | lista ryzyk z opisami i mapowaniem CWE | 5–6 h | 0 zł | https://top10.owasp.org/2025/ |
| OWASP API Security Top 10 (edycja 2023) | OWASP | lista ryzyk API | 4–5 h | 0 zł | https://api-security.owasp.org |

Szczególnie ważne: ASVS 5.0 ma inną numerację niż 4.0.3, więc raporty i listy kontrolne oparte na starej wersji trzeba przemapować. W Top 10:2025 pojawiły się nowe kategorie „Software Supply Chain Failures” (A03) i „Mishandling of Exceptional Conditions” (A10), a kontrola dostępu nadal jest na pierwszym miejscu.

**Dowód:** raport z audytu przykładowej aplikacji Next.js z Supabase (np. własnej z sekcji 3.1 albo aplikacji z vibe codingu) według ASVS L1 i wybranych wymagań L2: tabela wymagań ze statusem, dowody (zrzuty, żądania, fragmenty kodu), priorytety i plan naprawy zrozumiały dla klienta nietechnicznego.

#### Etap 3: modelowanie zagrożeń

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Threat Modeling: Designing for Security (wydanie 1, Wiley 2014) | Adam Shostack | książka, średni | 15–20 h | płatna | https://shostack.org/books/threat-modeling-book |
| Threat Modeling Manifesto | grupa autorów | zasady i wzorce | 1 h | 0 zł | https://www.threatmodelingmanifesto.org |
| LINDDUN (wariant uproszczony GO i szczegółowy PRO) | DistriNet, KU Leuven | metoda modelowania zagrożeń prywatności | 6–8 h | 0 zł | https://linddun.org |

Wydanie 2 książki Shostacka („Threat Modeling: Designing for Security in an AI World”) jest zapowiedziane na luty 2027 r.; do tego czasu podstawą jest wydanie 1.

Szczególnie ważne: diagram przepływu danych z granicami zaufania, STRIDE dla każdego elementu diagramu, LINDDUN dla danych osobowych (spójność z RODO), zagrożenia wprowadzone przez agentów AI i integracje LLM (zob. sekcja 11.1).

**Dowód:** model zagrożeń STRIDE i LINDDUN dla przejmowanej aplikacji klienta przygotowany w 1 dzień: diagram, lista zagrożeń z oceną ryzyka, środki zaradcze przypisane do zadań i decyzje zapisane w ADR.

#### Etap 4: narzędzia SAST, DAST i wykrywanie sekretów

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Semgrep: dokumentacja, w tym pisanie własnych reguł | Semgrep | dokumentacja | 8–10 h | 0 zł (wersja społecznościowa) | https://semgrep.dev/docs |
| CodeQL: dokumentacja i „Learn to write CodeQL” | GitHub | dokumentacja, średni–zaawansowany | 8–10 h | 0 zł dla repozytoriów publicznych | https://codeql.github.com/docs/ |
| ZAP: Getting Started, Automation Framework, uwierzytelnianie | ZAP by Checkmarx (dawniej OWASP ZAP) | dokumentacja | 8–10 h | 0 zł | https://www.zaproxy.org/docs/ |
| gitleaks | Zachary Rice i społeczność | dokumentacja narzędzia | 2–3 h | 0 zł | https://github.com/gitleaks/gitleaks |

Szczególnie ważne: odróżnianie fałszywych alarmów od prawdziwych błędów, własne reguły dla wzorców typowych dla kodu z AI (brak autoryzacji w Server Actions, klucz `service_role` Supabase po stronie klienta, `NEXT_PUBLIC_*` z sekretem), skanowanie DAST z zalogowanym użytkownikiem, przegląd całej historii git pod kątem sekretów i ich rotacja.

**Dowód:** zestaw 5 własnych reguł Semgrep z testami, każda wykrywająca błąd znaleziony w etapie 2; skan ZAP z uwierzytelnieniem uruchamiany w CI (zob. sekcja 9) i raport gitleaks z historii repozytorium z planem rotacji kluczy.

#### Etap 5: łańcuch dostaw i SBOM

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Authoritative Guide to SBOM (wydanie 3) i specyfikacja CycloneDX (ECMA-424) | OWASP CycloneDX | przewodnik i standard | 8–10 h | 0 zł | https://cyclonedx.org/guides/, https://cyclonedx.org |
| Cargo Vet | Mozilla | dokumentacja narzędzia | 3–4 h | 0 zł | https://mozilla.github.io/cargo-vet/ |
| RustSec Advisory Database i `cargo-audit` | Rust Secure Code WG | baza i narzędzie | 2–3 h | 0 zł | https://rustsec.org |
| OpenSSF Scorecard | OpenSSF | narzędzie oceny praktyk projektów open source | 2–3 h | 0 zł | https://scorecard.dev |
| OSV i `osv-scanner` | Google, OpenSSF | baza podatności i skaner | 2–3 h | 0 zł | https://osv.dev |

Szczególnie ważne: kompletność SBOM (zależności przechodnie, wersje, licencje, identyfikatory PURL), SBOM dla każdego wydania, a nie jednorazowo, ocena nowych zależności przed dodaniem (Scorecard, utrzymanie, liczba opiekunów), pakiety wymyślone przez model i ich podróbki (typosquatting, „slopsquatting”).

**Dowód:** dla jednej aplikacji z rdzeniem w Ruście i frontendem w TypeScript: SBOM w CycloneDX generowany w CI przy każdym wydaniu, polityka `cargo-deny` i `cargo-vet` z udokumentowanymi wyjątkami, raport Scorecard dla 10 najważniejszych zależności i decyzja dla każdej.

#### Etap 6: obsługa podatności i CRA

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| CVSS v4.0: specyfikacja i User Guide | FIRST | standard | 5–6 h | 0 zł | https://www.first.org/cvss/v4.0/specification-document, https://www.first.org/cvss/v4.0/user-guide |
| EPSS (Exploit Prediction Scoring System) | FIRST | model i dane (CSV, API) | 2–3 h | 0 zł | https://www.first.org/epss/ |
| Known Exploited Vulnerabilities Catalog | CISA | katalog podatności wykorzystywanych w atakach | 1–2 h | 0 zł | https://www.cisa.gov/known-exploited-vulnerabilities-catalog |
| European Vulnerability Database (EUVD) | ENISA | europejska baza podatności | 1–2 h | 0 zł | https://euvd.enisa.europa.eu |
| Rozporządzenie (UE) 2024/2847 (CRA), zwłaszcza art. 13, 14 i załącznik I | UE | akt prawny | 6–8 h | 0 zł | https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng |
| Wytyczne Komisji do stosowania CRA (27 lipca 2026 r., 67 przykładów, m.in. dla mikroprzedsiębiorstw) i strona o zgłoszeniach | Komisja Europejska | wytyczne | 6–8 h | 0 zł | https://digital-strategy.ec.europa.eu/en/library/commission-publishes-new-guidance-support-timely-cyber-resilience-act-implementation, https://digital-strategy.ec.europa.eu/en/policies/cra-reporting |
| Single Reporting Platform: FAQ, instrukcje, nagrania | ENISA | platforma zgłoszeń i materiały | 2–3 h | 0 zł | https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp |
| Secure by Design and Default Playbook | ENISA | poradnik dla MŚP | 2–3 h | 0 zł | https://www.enisa.europa.eu/publications/enisa-secure-by-design-and-default-playbook |

Obowiązki zgłoszeniowe producentów z CRA obowiązują od 11 września 2026 r. i są realizowane przez platformę ENISA; pozostałe obowiązki od 11 grudnia 2027 r.

Szczególnie ważne: CVSS opisuje dotkliwość, a nie ryzyko, więc kolejność napraw ustala się łącznie z EPSS, obecnością w KEV i kontekstem klienta (czy podatny kod jest osiągalny); terminy z art. 14: wczesne ostrzeżenie w 24 h, zgłoszenie w 72 h i raport końcowy; polityka ujawniania podatności i `security.txt`; okres wsparcia produktu.

**Dowód:** triage 10 rzeczywistych CVE z zależności własnej aplikacji według CVSS 4.0, EPSS i KEV, z uzasadnieniem kolejności i decyzją (naprawa, łagodzenie, brak wpływu z oświadczeniem VEX); ćwiczenie zgłoszenia CRA na czas: od wykrycia aktywnie wykorzystywanej podatności do wypełnionego wczesnego ostrzeżenia w 24 h, z gotowymi szablonami zgłoszenia i komunikatu dla użytkowników.

#### Etap 7: mobile, desktop, Rust i embedded

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| OWASP MASVS, MASWE i MASTG | OWASP Mobile Application Security | standard, katalog słabości i przewodnik testowania | 20–25 h | 0 zł | https://mas.owasp.org |
| Secure Rust Guidelines | ANSSI | przewodnik bezpiecznego programowania w Ruście | 6–8 h | 0 zł | https://anssi-fr.github.io/rust-guide/ |
| Rust Secure Code Working Group: lista projektów (fuzzery, analizatory, narzędzia zależności) | Rust Secure Code WG | katalog narzędzi | 2–3 h | 0 zł | https://github.com/rust-secure-code/projects |
| Tauri: Security (granice zaufania, IPC, capabilities) | Tauri | dokumentacja | 4–6 h | 0 zł | https://v2.tauri.app/security/ |

Embedded na tym etapie ogranicza się do wymagań z sekcji 22 (secure boot, podpis firmware, blokada debugowania, ochrona przed cofnięciem wersji); szczegółowe normy (EN 18031, ETSI EN 303 645) warto zgłębiać dopiero po decyzji o wejściu w urządzenia.

**Dowód:** test aplikacji mobilnej według MASVS (przechowywanie danych, sieć, platforma) z raportem; przegląd kodu `unsafe` w rdzeniu Rust z mapą `cargo-geiger` i uzasadnieniem każdego bloku; przegląd capabilities i poleceń IPC aplikacji Tauri z poprawkami.

#### Etap 8: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Burp Suite Certified Practitioner | PortSwigger | egzamin praktyczny | 20–40 h przygotowania | płatny | https://portswigger.net/web-security |
| Komunikaty bezpieczeństwa frameworków i zależności, RustSec, EUVD, KEV | autorzy projektów, ENISA, CISA | źródła pierwotne | ok. 1 h tygodniowo | 0 zł | https://rustsec.org, https://euvd.enisa.europa.eu |
| Zmiany w ASVS, Top 10 i materiałach Komisji i ENISA o CRA | OWASP, Komisja Europejska, ENISA | źródła pierwotne | wg potrzeb | 0 zł | https://github.com/OWASP/ASVS, https://digital-strategy.ec.europa.eu/en/policies/cra-reporting |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **audyty klientów:** 5 audytów aplikacji z vibe codingu lub no-code według jednego szablonu raportu (ASVS, model zagrożeń, SBOM, plan naprawy), z mierzeniem czasu i poprawianiem szablonu,
- **recenzja bezpieczeństwa kodu AI:** lista kontrolna bezpieczeństwa wbudowana w vicrafter (hooki i skille) i sprawdzana na 20 pull requestach agentów, z odsetkiem błędów wykrytych przez człowieka, a pominiętych przez narzędzia,
- **obsługa podatności jako proces:** dyżur nad komunikatami dla wszystkich utrzymywanych aplikacji, ćwiczenie zgłoszenia CRA raz na kwartał,
- **wkład zewnętrzny:** zgłoszenie odpowiedzialnie ujawnionej podatności w projekcie open source albo reguła Semgrep lub wpis do RustSec.

**Dowód poziomu E:** samodzielnie, bez agenta, w 2 dni przeprowadzasz audyt nieznanej aplikacji (ASVS L1, model zagrożeń, SBOM i triage podatności), znajdujesz co najmniej jeden błąd kontroli dostępu lub łańcucha dostaw, który przeoczyły narzędzia automatyczne, i przedstawiasz klientowi raport z planem naprawy i oceną obowiązków z CRA.

---

## 11. Weryfikacja pracy AI i budowa procesu

*Warstwa 3: ochrona i kontrola. Opiera się na: 1, 2, 6, 7, 8 i 10. Jest podstawą: pracy z agentami we wszystkich kolejnych sekcjach.*

Codzienna praca z Claude i Claude Code jest w sekcji 1. Ta sekcja dotyczy tego, co na niej zbudowane: własnego procesu z punktami kontrolnymi człowieka i sprawdzania, czy agent pracuje dobrze i bezpiecznie.

- Rozszerzanie Claude Code: skille, subagenci, hooki, MCP, reguły uprawnień, pluginy (fundament vicrafter).
- Ewaluacje pracy agenta i promptów jako testy regresji procesu.
- Bezpieczeństwo agentów: prompt injection przez treści z repozytorium klienta, nadmierna sprawczość, sandbox.
- Czytanie diffów i próbkowa, krytyczna recenzja; rozpoznawanie kodu „prawie dobrego”.
- Recenzja na innym modelu niż autor kodu, lokalne modele jako druga niezależna recenzja (Ollama, llama.cpp, LiteLLM).
- Pomiar: czy proces oszczędza czas, i gotowość do jego uproszczenia.

### 11.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 6 etapów, numerowanych od 1, bo podstawy LLM i codzienna praca z Claude Code są w sekcji 1.1. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Dowody budują kolejne elementy vicrafter: konfigurację uprawnień, hooki i skille, listę kontrolną recenzji, zestaw ewaluacji i recenzję na innym modelu. Etapy 3 i 4 warto przejść w całości, bo bez nich nie da się zmierzyć, czy agent pracuje dobrze ani czy pracuje bezpiecznie. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem. Dokumentacja Claude Code zmienia się co kilka tygodni, więc materiały z tej sekcji trzeba czytać w wersji bieżącej, a nie z notatek. Uruchamianie modeli lokalnych jest w sekcji 20.3, bezpieczeństwo aplikacji w sekcji 10.1.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 1 | konfiguracja i rozszerzanie Claude Code: uprawnienia, skille, subagenci, hooki, pluginy, MCP | 40–50 h | E |
| 2 | recenzja kodu, także kodu z AI | 20–30 h | E |
| 3 | ewaluacje: pomiar jakości pracy agenta i promptów | 40–50 h | E |
| 4 | bezpieczeństwo agentów i integracji LLM | 25–35 h | E |
| 5 | architektura agentów i projektowanie narzędzi | 20–30 h | W |
| 6 | ekspert: pomiar procesu, recenzja krzyżowa, aktualność | stale, ok. 2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 145–195 h, czyli 3–5 miesięcy przy 10–12 h tygodniowo.

#### Etap 1: konfiguracja i rozszerzanie Claude Code

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Dokumentacja: Permissions, Settings, Sandboxing, Security | Anthropic | dokumentacja | 6–8 h | 0 zł | https://code.claude.com/docs/en/permissions, https://code.claude.com/docs/en/settings, https://code.claude.com/docs/en/sandboxing, https://code.claude.com/docs/en/security |
| Dokumentacja: Skills, Subagents, Hooks (przewodnik i referencja), Plugins | Anthropic | dokumentacja | 10–12 h | 0 zł | https://code.claude.com/docs/en/skills, https://code.claude.com/docs/en/sub-agents, https://code.claude.com/docs/en/hooks-guide, https://code.claude.com/docs/en/hooks, https://code.claude.com/docs/en/plugins/overview |
| Dokumentacja: tryb nieinteraktywny, GitHub Actions, monitorowanie (OpenTelemetry) | Anthropic | dokumentacja | 4–6 h | 0 zł | https://code.claude.com/docs/en/headless, https://code.claude.com/docs/en/github-actions, https://code.claude.com/docs/en/monitoring-usage |
| Kursy Anthropic Academy: „Introduction to agent skills”, „Introduction to subagents”, „Introduction to Model Context Protocol”, „Model Context Protocol: Advanced Topics” | Anthropic | kursy online | 8–10 h | 0 zł | https://anthropic.skilljar.com |
| Model Context Protocol: architektura, budowa serwera, specyfikacja | MCP (projekt open source) | dokumentacja i specyfikacja | 6–8 h | 0 zł | https://modelcontextprotocol.io |

Szczególnie ważne: hooki jako jedyny deterministyczny mechanizm (instrukcje w `CLAUDE.md` i skillach są tylko wskazówkami), reguły `allow` i `deny` oraz ich ograniczenia przy dopasowaniu poleceń, sandbox z izolacją sieci, co projekt może uruchomić przed zaufaniem folderowi, serwery MCP spoza repozytorium (pluginy, konektory).

**Dowód:** pierwsza wersja pluginu vicrafter: ustawienia uprawnień dla repozytorium klienta (bez poświadczeń produkcyjnych, sieć tylko do listy domen), hook blokujący zapis w katalogu migracji i hook uruchamiający testy przed zakończeniem pracy, jeden skill i jeden subagent recenzujący; wszystko w repozytorium z opisem, dlaczego dana reguła istnieje.

#### Etap 2: recenzja kodu

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Google Engineering Practices: „How to do a code review” i „The CL author’s guide” | Google | przewodnik | 3–4 h | 0 zł | https://google.github.io/eng-practices/review/ |
| Simon Willison’s Weblog, tag „ai-assisted-programming” | Simon Willison | blog, praktyka pracy z agentami | 8–10 h (wybór wpisów) | 0 zł | https://simonwillison.net/tags/ai-assisted-programming/ |
| Dokumentacja Claude Code: „Add an adversarial review step”, `/code-review`, `/security-review` | Anthropic | dokumentacja | 1–2 h | 0 zł | https://code.claude.com/docs/en/best-practices |

Szczególnie ważne: recenzja według kryteriów, a nie stylu; czytanie diffu od testów i kontraktów; typowe wady kodu „prawie dobrego” (obsłużona ścieżka szczęśliwa, brak przypadków brzegowych, osłabione asercje, wymyślone API i pakiety, niezamierzone zmiany poza zakresem zadania); recenzent w świeżym kontekście nie widzi rozumowania autora, a recenzent poproszony o znalezienie luk zwykle jakieś znajdzie, więc zgłoszenia trzeba filtrować.

**Dowód:** lista kontrolna recenzji kodu z AI (z odesłaniami do sekcji 3.1, 6 i 10.1) i 20 pull requestów agentów zrecenzowanych według niej; dla każdego zapis znalezionych błędów, czasu recenzji i tego, które błędy wychwyciły narzędzia, a które tylko człowiek.

#### Etap 3: ewaluacje

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| „Demystifying evals for AI agents” (styczeń 2026) | Anthropic | artykuł | 1–2 h | 0 zł | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents |
| Kurs „Prompt evaluations” | Anthropic | kurs z ćwiczeniami | 6–8 h | 0 zł (zużycie API płatne) | https://github.com/anthropics/courses |
| „Your AI Product Needs Evals”, „Using LLM-as-a-Judge”, „A Field Guide to Rapidly Improving AI Products”, „AI Evals: Everything You Need to Know” (FAQ) | Hamel Husain, Shreya Shankar | artykuły, średni–zaawansowany | 8–10 h | 0 zł | https://hamel.dev/blog/posts/evals/, https://hamel.dev/blog/posts/evals-faq/ |
| AI Evals For Engineers & PMs | Hamel Husain, Shreya Shankar (Maven) | kurs kohortowy | 30–40 h | płatny | https://maven.com/parlance-labs/evals |
| AI Engineering: Building Applications with Foundation Models (O’Reilly 2025), rozdziały o ewaluacji | Chip Huyen | książka, średni–zaawansowany | 10–12 h (rozdziały 3–4) | płatna | https://huyenchip.com/books/ |

Kurs Maven jest opcjonalny: darmowe artykuły tych samych autorów wystarczą do poziomu W, kurs przyspiesza dojście do E.

Szczególnie ważne: analiza błędów na prawdziwych przebiegach przed pisaniem metryk, zadania z jednoznacznym kryterium sukcesu, oceniacze deterministyczne tam, gdzie się da, LLM-as-judge tylko po sprawdzeniu zgodności z oceną ręczną, wielokrotne uruchomienia z powodu niedeterminizmu, ewaluacje jako testy regresji przy zmianie modelu, promptu lub skilla.

**Dowód:** zestaw ewaluacji vicrafter: 30 zadań z repozytoriów testowych (naprawa błędu, test charakteryzujący, poprawka bezpieczeństwa) z automatycznym oceniaczem, uruchamiany w CI przy każdej zmianie pluginu; raport porównujący dwie wersje skilla lub dwa modele z liczbą powtórzeń i rozrzutem wyników.

#### Etap 4: bezpieczeństwo agentów i integracji LLM

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| OWASP Top 10 for LLM Applications 2025 | OWASP GenAI Security Project | lista ryzyk | 4–5 h | 0 zł | https://genai.owasp.org/llm-top-10/ |
| OWASP Top 10 for Agentic Applications for 2026 (grudzień 2025) | OWASP GenAI Security Project | lista ryzyk | 3–4 h | 0 zł | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ |
| MCP: Security Best Practices | MCP (projekt open source) | dokumentacja | 3–4 h | 0 zł | https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices |
| „The lethal trifecta for AI agents” i tag „prompt-injection” | Simon Willison | artykuły | 4–6 h | 0 zł | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/, https://simonwillison.net/tags/prompt-injection/ |

Szczególnie ważne: „zabójcza trójka” (dostęp do prywatnych danych, niezaufane treści, kanał wysyłki na zewnątrz) i przecinanie kanału wysyłki jako najprostsza ochrona; pośredni prompt injection przez pliki repozytorium klienta, zgłoszenia i strony; nadmierna sprawczość; przekazywanie tokenów i za szerokie zakresy w serwerach MCP; lokalne serwery MCP jako uruchamianie cudzego kodu.

**Dowód:** model zagrożeń STRIDE (zob. sekcja 10.1) dla własnego stanowiska pracy z agentami i vicrafter; 10 przygotowanych przypadków prompt injection umieszczonych w repozytorium testowym (komentarze, README, zgłoszenia) dołączonych do ewaluacji z etapu 3, z wynikiem: które ataki zablokowały uprawnienia, sandbox lub hooki, a które wymagały poprawek.

#### Etap 5: architektura agentów i projektowanie narzędzi

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| „Building effective agents” (grudzień 2024) | Erik Schluntz, Barry Zhang (Anthropic) | artykuł | 1–2 h | 0 zł | https://www.anthropic.com/engineering/building-effective-agents |
| „Writing effective tools for agents — with agents” i „Effective context engineering for AI agents” (2025) | Anthropic | artykuły | 2–3 h | 0 zł | https://www.anthropic.com/engineering/writing-tools-for-agents, https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| Claude Agent SDK | Anthropic | dokumentacja | 4–6 h | 0 zł | https://code.claude.com/docs/en/agent-sdk/overview |
| Kurs „Tool use” | Anthropic | kurs z ćwiczeniami | 4–6 h | 0 zł (zużycie API płatne) | https://github.com/anthropics/courses |
| AI Engineering, rozdziały o agentach, RAG i architekturze | Chip Huyen, O’Reilly | książka | 6–8 h | płatna (ta sama co w etapie 3) | https://huyenchip.com/books/ |

Szczególnie ważne: najprostsze rozwiązanie, które działa (przepływ zamiast agenta, jeśli wystarczy), opisy narzędzi jako część promptu, zwięzłe i jednoznaczne wyniki narzędzi, kontekst jako ograniczony zasób, podział pracy między subagentów.

**Dowód:** jeden przepływ vicrafter (np. triage zgłoszeń klienta albo przygotowanie raportu z audytu) przebudowany według tych zasad, z pomiarem przed i po na zestawie ewaluacji z etapu 3 (jakość, czas, koszt tokenów).

#### Etap 6: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Blog inżynieryjny Anthropic i informacje o zmianach Claude Code | Anthropic | źródła pierwotne | ok. 1 h tygodniowo | 0 zł | https://www.anthropic.com/engineering, https://code.claude.com/docs |
| Simon Willison’s Weblog | Simon Willison | blog | ok. 0,5 h tygodniowo | 0 zł | https://simonwillison.net |
| Specyfikacja MCP (nowe wersje i zmiany w autoryzacji) | MCP | źródło pierwotne | wg potrzeb | 0 zł | https://modelcontextprotocol.io |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja krzyżowa:** każda zmiana w ścieżce krytycznej recenzowana przez inny model niż autor (inny dostawca przez bramkę LLM albo model lokalny, zob. sekcja 20.3), z porównaniem, które błędy wychwycił który recenzent,
- **pomiar procesu:** co miesiąc czas od zadania do scalenia, odsetek zmian odrzuconych lub poprawionych przez człowieka, koszt na zadanie; decyzja o usunięciu kroków vicrafter, które nie poprawiają wyników,
- **aktualizacja ewaluacji:** każdy błąd agenta, który przeszedł do recenzji, staje się nowym przypadkiem w zestawie,
- **praca bez agenta:** raz w miesiącu zadanie wykonane samodzielnie, żeby nie utracić umiejętności, które się weryfikuje.

**Dowód poziomu E:** dla zmiany w nieznanym repozytorium potrafisz w 1 dzień ustalić, czy praca agenta jest poprawna i bezpieczna, wskazać błąd, którego nie znalazł recenzent AI, i wykazać na danych z ewaluacji, czy nowa wersja modelu lub skilla poprawiła, czy pogorszyła wyniki vicrafter.

---

## 12. Rust jako wspólny fundament

*Warstwa 4: rdzeń kompilowany. Opiera się na: 2, 5, 6, 8 i 9. Jest podstawą: 14–22.*

- Własność, pożyczanie, czasy życia, cechy (traits), generyki, obsługa błędów (`Result`, `thiserror`, `anyhow`).
- Programowanie asynchroniczne: Tokio, `Send`/`Sync`, anulowanie, blokowanie w kontekście async, kanały.
- `unsafe` i FFI: kiedy jest uzasadnione, jak je audytować, granice z C, Swift i Kotlinem (UniFFI, `cbindgen`).
- Cargo: workspace’y, features, profile budowania, kompilacja skrośna (targety, `cross`, `cargo-zigbuild`), rozmiar binarki.
- Ekosystem: `serde`, `tracing`, `reqwest`, `sqlx`, `clap`.
- Jakość: `clippy` (także w trybie pedantycznym), `rustfmt`, `miri` dla kodu `unsafe`, `cargo-udeps`.
- Weryfikacja kodu agentów w Ruście: nadmiarowe `.clone()` i `.unwrap()`, ukryte panice, `unsafe` bez uzasadnienia, wymyślone crate’y lub API, blokowanie w kodzie async.

### 12.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 7 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Doświadczenie seniorskie w TypeScript skraca etapy 0 i 1 (narzędzia, składnia, typy algebraiczne, generyki), ale nie etap 2: model własności nie ma odpowiednika w językach z odśmiecaczem pamięci i właśnie tu najłatwiej przeoczyć błąd agenta. Etap 0 można zaliczyć samym dowodem, etap 1 częściowo, pozostałe trzeba przejść z materiałami. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | narzędzia i pierwsze programy: `rustup`, Cargo, edycja 2024 | 10–15 h | podstawy |
| 1 | język: typy, wzorce, cechy, generyki, błędy, iteratory | 60–80 h | podstawy |
| 2 | własność, pożyczanie, czasy życia, idiomy | 50–70 h | W |
| 3 | projektowanie API i jakość: Clippy, testy, dokumentacja, crate’y | 40–50 h | W |
| 4 | async i współbieżność: Tokio, `Send`/`Sync`, atomiki | 50–70 h | W |
| 5 | aplikacja produkcyjna: backend, obserwowalność, CI, łańcuch dostaw | 60–80 h | E |
| 6 | ekspert: `unsafe`, FFI (UniFFI, `cbindgen`), wydajność, recenzja kodu AI | stale, ok. 2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 300–400 h, czyli 7–10 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: narzędzia i pierwsze programy

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Strona „Learn” i instalacja przez `rustup` | zespół Rusta | dokumentacja | 1–2 h | 0 zł | https://www.rust-lang.org/learn |
| The Cargo Book: rozdziały „Getting Started” i „Cargo Guide” | zespół Cargo | dokumentacja | 3–4 h | 0 zł | https://doc.rust-lang.org/cargo/ |
| The Rust Edition Guide: Rust 2024 | zespół Rusta | dokumentacja | 1–2 h | 0 zł | https://doc.rust-lang.org/edition-guide/rust-2024/index.html |
| rust-analyzer | zespół Rusta | narzędzie, dokumentacja | 1 h | 0 zł | https://rust-analyzer.github.io |

**Dowód:** narzędzie CLI w `clap` (np. walidator plików JSON lub CSV) w edycji 2024, z `cargo fmt`, `cargo clippy` i `cargo test` uruchamianymi w CI na Linuksie, macOS i Windows.

#### Etap 1: język

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Rust Programming Language (online; wydanie 3 drukiem, No Starch Press, marzec 2026, edycja 2024) | Steve Klabnik, Carol Nichols, Chris Krycho | książka, od podstaw do średniego | 30–40 h | 0 zł online / płatna (druk) | https://doc.rust-lang.org/book/ |
| Wersja interaktywna tej książki z quizami i wizualizacjami własności | Brown University (Will Crichton, Shriram Krishnamurthi) | książka z quizami | zamiast wersji wyżej | 0 zł | https://rust-book.cs.brown.edu |
| Rustlings | zespół Rusta | ćwiczenia w terminalu | 10–15 h | 0 zł | https://rustlings.rust-lang.org |
| Rust by Example | zespół Rusta | przykłady do uruchamiania | 8–10 h | 0 zł | https://doc.rust-lang.org/rust-by-example/ |
| 100 Exercises To Learn Rust | Luca Palmieri, Mainmatter | kurs z ćwiczeniami, od podstaw do średniego | 15–20 h | 0 zł | https://rust-exercises.com/100-exercises/ |
| Comprehensive Rust: Rust Fundamentals (4 dni) | Google (zespół Androida) | kurs, od podstaw do średniego | 20–25 h | 0 zł | https://google.github.io/comprehensive-rust/ |

Wystarczy jedno z dwóch: Rustlings z Rust by Example albo 100 Exercises To Learn Rust; Comprehensive Rust jest zwięzłą alternatywą dla osoby z doświadczeniem w innych językach. Szczególnie ważne: `enum` i `match` jako odpowiednik dyskryminowanych unii z TypeScriptu, `Option` i `Result` z operatorem `?`, cechy i generyki, iteratory i domknięcia, moduły i widoczność, `String` kontra `&str`, `Vec` kontra wycinki.

**Dowód:** parser i walidator małego formatu (np. pliku konfiguracji) z typami błędów w `thiserror`, bez `unwrap()` poza testami, z testami jednostkowymi i dokumentacją `cargo doc`.

#### Etap 2: własność, pożyczanie, czasy życia

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Programming Rust (wydanie 3, edycja 2024, październik 2026) | Jim Blandy, Jason Orendorff, Leonora F. S. Tindall, O’Reilly | książka, średni–zaawansowany | 30–40 h | płatna | https://www.oreilly.com/library/view/programming-rust-3rd/9781098176228/ |
| Effective Rust | David Drysdale, O’Reilly (bezpłatnie online) | książka, średni | 10–12 h | 0 zł online / płatna (druk) | https://effective-rust.com |
| Learning Rust With Entirely Too Many Linked Lists | Aria Desires (rust-unofficial) | samouczek, średni–zaawansowany | 8–10 h | 0 zł | https://rust-unofficial.github.io/too-many-lists/ |
| Rust Design Patterns | rust-unofficial | książka online: idiomy, wzorce, antywzorce | 5–6 h | 0 zł | https://rust-unofficial.github.io/patterns/ |
| Rust Language Cheat Sheet | Ralf Biedert | ściągawka | wg potrzeb | 0 zł | https://cheats.rs |

Szczególnie ważne: przenoszenie, pożyczanie współdzielone i wyłączne, elizja i jawne czasy życia, `Box`, `Rc`, `Arc`, `RefCell` i `Mutex` oraz kiedy ich użycie maskuje zły projekt, `Clone` kontra `Copy`, `Cow`, cechy `From`/`Into`, `AsRef`, `Deref`, `Drop`. Rozdział o antywzorcach w Rust Design Patterns (np. `clone()` dla uciszenia borrow checkera) to gotowa lista do recenzji kodu agentów.

**Dowód:** model domeny rdzenia własnej aplikacji (np. dokumenty, licencje, synchronizacja) z poprawnym podziałem własności, bez zbędnych `.clone()` i `Rc<RefCell<…>>`, z jednym typem z jawnymi czasami życia (np. parser bez kopiowania danych wejściowych).

#### Etap 3: projektowanie API i jakość

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Rust for Rustaceans | Jon Gjengset, No Starch Press | książka, zaawansowany | 15–20 h | płatna | https://rust-for-rustaceans.com |
| Rust API Guidelines | zespół bibliotek Rusta | wytyczne z listą kontrolną | 4–5 h | 0 zł | https://rust-lang.github.io/api-guidelines/ |
| Clippy: lista lintów i grupy (`correctness`, `suspicious`, `pedantic`, `restriction` i inne) | zespół Clippy | dokumentacja | 3–4 h | 0 zł | https://rust-lang.github.io/rust-clippy/stable/index.html |
| The Cargo Book: features, workspace’y, profile, publikowanie | zespół Cargo | dokumentacja | 4–5 h | 0 zł | https://doc.rust-lang.org/cargo/ |
| The rustdoc book | zespół Rusta | dokumentacja | 2 h | 0 zł | https://doc.rust-lang.org/rustdoc/ |
| The Little Book of Rust Macros (część o makrach proceduralnych niepełna) | Lukas Wirth (pierwotnie Daniel Keep) | książka online, zaawansowany | 4–6 h | 0 zł | https://lukaswirth.dev/tlborm/ |
| Nagrania „Crust of Rust” | Jon Gjengset | wideo, średni–zaawansowany | wg potrzeb | 0 zł | https://www.youtube.com/@jonhoo |

Szczególnie ważne: typy błędów w bibliotece (`thiserror`) i w aplikacji (`anyhow`), semver i zmiany łamiące zgodność, cechy domyślne i addytywność features, testy integracyjne i doctesty, konfiguracja lintów w `[lints]` w `Cargo.toml`. Techniki i narzędzia testowe (`proptest`, `insta`, `cargo-nextest`, `cargo-mutants`): zob. sekcja 6.

**Dowód:** biblioteka w workspace z rdzeniem aplikacji, z udokumentowanym publicznym API zgodnym z listą kontrolną API Guidelines, `#![deny(missing_docs)]`, wybranymi lintami `pedantic` w `[lints]`, testami właściwości i sprawdzeniem semver (`cargo-semver-checks`) w CI.

#### Etap 4: async i współbieżność

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Tokio Tutorial i rozdziały „Bridging with sync code”, „Graceful Shutdown”, „Tracing” | zespół Tokio | samouczek | 10–12 h | 0 zł | https://tokio.rs/tokio/tutorial |
| Asynchronous Programming in Rust (w trakcie przepisywania, niekompletna) | zespół Rusta (Async WG) | książka online | 4–6 h | 0 zł | https://rust-lang.github.io/async-book/ |
| Async Rust | Maxwell Flitton, Caroline Morton, O’Reilly (2024) | książka, średni–zaawansowany | 12–15 h | płatna | https://www.oreilly.com/library/view/async-rust/9781098149086/ |
| Rust Atomics and Locks | Mara Bos, O’Reilly (bezpłatnie online) | książka, zaawansowany | 12–15 h | 0 zł online / płatna (druk) | https://mara.nl/atomics/ |
| Comprehensive Rust: Concurrency (1 dzień) | Google | kurs | 6–8 h | 0 zł | https://google.github.io/comprehensive-rust/ |

Książka zespołu Rusta o async jest przepisywana i ma luki, więc podstawą jest samouczek Tokio, a „Async Rust” jest opcjonalna. Szczególnie ważne: `Future` i `Pin`, `Send` i `Sync` w zadaniach, blokowanie w kontekście async (`spawn_blocking`), anulowanie i bezpieczeństwo anulowania w `select!`, kanały i przeciwciśnienie, `Mutex` z `std` kontra z Tokio, porządki pamięci w atomikach.

**Dowód:** usługa w Tokio z kolejką zadań w tle, limitem współbieżności, łagodnym zamykaniem i anulowaniem, z testami (`#[tokio::test]`, kontrola czasu przez `tokio::time::pause`) i bez blokujących wywołań w kodzie async; jedna struktura danych z atomikami opisana komentarzem uzasadniającym wybrane porządki pamięci.

#### Etap 5: aplikacja produkcyjna

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Zero To Production in Rust | Luca Palmieri | książka, średni–zaawansowany (aktualizowana co ok. 3 miesiące) | 40–50 h | płatna (darmowa próbka) | https://www.zero2prod.com |
| Dokumentacja i przykłady Axum | zespół Tokio | dokumentacja | 6–8 h | 0 zł | https://docs.rs/axum, https://github.com/tokio-rs/axum/tree/main/examples |
| Command Line Applications in Rust | Rust CLI WG | książka online | 4–5 h | 0 zł | https://rust-cli.github.io/book/ |
| Secure Rust Guidelines | ANSSI | wytyczne bezpieczeństwa | 3–4 h | 0 zł | https://anssi-fr.github.io/rust-guide/ |

Zero To Production prowadzi przez budowę backendu od zera do wdrożenia (testy, błędy, logi strukturalne, uwierzytelnianie, CI/CD), ale nie na Axum; przy przenoszeniu wzorców pomaga dokumentacja Axum. Szczegóły Axum, Tower i SQLx: zob. sekcja 5; SBOM, `cargo-audit`, `cargo-deny`, `cargo-vet`: zob. sekcja 10; kompilacja skrośna i wydania: zob. sekcja 9.

**Dowód:** backend Axum z SQLx dla własnej aplikacji (licencje lub synchronizacja), z testami integracyjnymi na prawdziwej bazie, `tracing` z OpenTelemetry, obsługą błędów bez paniki na ścieżce żądania, binarkami dla trzech systemów z CI oraz SBOM CycloneDX i `cargo-deny` jako bramką wydania (CRA).

#### Etap 6: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Rustonomicon | zespół Rusta | książka online, zaawansowany | 10–15 h | 0 zł | https://doc.rust-lang.org/nomicon/ |
| The Rust Reference | zespół Rusta | specyfikacja języka | wg potrzeb | 0 zł | https://doc.rust-lang.org/reference/ |
| Safety comments policy (zasady komentarzy `SAFETY:`) | Standard library developers Guide | wytyczne | 1 h | 0 zł | https://std-dev-guide.rust-lang.org/policy/safety-comments.html |
| Miri | zespół Rusta | narzędzie do wykrywania niezdefiniowanego zachowania | 2–3 h | 0 zł | https://github.com/rust-lang/miri |
| Comprehensive Rust: Unsafe Rust (z ćwiczeniem FFI) | Google | kurs | 2 h | 0 zł | https://google.github.io/comprehensive-rust/unsafe-rust.html |
| The UniFFI User Guide (Kotlin, Swift, Python) | Mozilla | dokumentacja | 6–8 h | 0 zł | https://mozilla.github.io/uniffi-rs/latest/ |
| cbindgen: dokumentacja | Mozilla | dokumentacja | 2–3 h | 0 zł | https://github.com/mozilla/cbindgen/blob/main/docs.md |
| The Rust Performance Book | Nicholas Nethercote i inni | książka online | 4–5 h | 0 zł | https://nnethercote.github.io/perf-book/ |
| Rust Fuzz Book (`cargo-fuzz`, `afl.rs`) | rust-fuzz | dokumentacja | 3–4 h | 0 zł | https://rust-fuzz.github.io/book/ |
| Blog Rusta, informacje o wydaniach, RFC | zespół Rusta | źródła pierwotne | ok. 1 h tygodniowo | 0 zł | https://blog.rust-lang.org |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 20 pull requestów w Ruście wygenerowanych przez agentów, recenzowanych według listy kontrolnej z sekcji 12 (nadmiarowe `.clone()` i `.unwrap()`, ukryte panice przez indeksowanie i `expect`, `unsafe` bez komentarza `SAFETY:`, wymyślone crate’y, features lub API, blokowanie w async, zbędne `Arc<Mutex<…>>`, typy błędów gubiące kontekst) oraz z lintami Clippy `undocumented_unsafe_blocks` i `unwrap_used`,
- **`unsafe` i FFI w praktyce:** rdzeń aplikacji wystawiony przez UniFFI do Swifta i Kotlina oraz przez `cbindgen` do C, z testami pod Miri dla kodu `unsafe` i mapą `unsafe` w zależnościach (`cargo-geiger`, zob. sekcja 10),
- **wydajność:** profilowanie (`cargo flamegraph`, `perf` lub Instruments), benchmarki w `criterion` jako regresja w CI, redukcja rozmiaru binarki,
- **przegląd zależności:** audyt nowych crate’ów przed dodaniem (utrzymanie, `unsafe`, licencja), wpisy w `cargo-vet`,
- **wkład w open source** w jednym crate z używanego ekosystemu.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz w nieznanym kodzie Rusta błąd niezdefiniowanego zachowania wykryty przez Miri, zakleszczenie w async albo awarię na granicy FFI z aplikacją mobilną i umiesz wyjaśnić przyczynę osobie nietechnicznej.

### 12.2 Ścieżka uzupełniająca: C i inne języki systemowe

Etap 1 warto przejść przed etapem 6 ścieżki 12.1 (`unsafe` i FFI), bo bez czytania C nie da się ocenić granicy FFI ani wiązań generowanych przez agenta. Etap 2 robi się w miarę potrzeby: Javę przed sekcją 18, Objective-C przed sekcją 19, C++ przy bibliotekach natywnych w sekcjach 20 i 22. Czas podany dla osoby startującej od zera.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 1 | C ogólnie i FFI z Rustem | 60–80 h | W |
| 2 | czytanie C++, Javy i Objective-C | 20–30 h | czytanie |

#### Etap 1: C ogólnie i FFI z Rustem

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Beej’s Guide to C Programming | Brian „Beej” Hall | podręcznik online, od podstaw | 15–20 h | 0 zł | https://beej.us/guide/bgc/ |
| Modern C (wydanie 3, C23) | Jens Gustedt, Manning | książka, średni–zaawansowany | 20–25 h | 0 zł (PDF autora) / płatna (druk) | https://gustedt.gitlabpages.inria.fr/modern-c/ |
| Effective C (wydanie 2, C23) | Robert C. Seacord, No Starch Press | książka, średni | 12–15 h | płatna | https://nostarch.com/effective-c-2nd-edition |
| SEI CERT C Coding Standard | Carnegie Mellon University, SEI | norma kodowania | wg potrzeb | 0 zł | https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard |
| AddressSanitizer i pokrewne sanitizery | LLVM | dokumentacja | 2–3 h | 0 zł | https://clang.llvm.org/docs/AddressSanitizer.html |
| The Rustonomicon: rozdział FFI; The bindgen User Guide | zespół Rusta | dokumentacja | 4–6 h | 0 zł | https://doc.rust-lang.org/nomicon/ffi.html, https://rust-lang.github.io/rust-bindgen/ |

Szczególnie ważne: wskaźniki i arytmetyka wskaźników, czas życia i własność pamięci (kto zwalnia), niezdefiniowane zachowanie, łańcuchy zakończone zerem, układ struktur i wyrównanie, nagłówki i makra preprocesora, konwencje wywołań, `errno` i kody błędów. Po stronie Rusta: `bindgen` do wiązań z nagłówków C, `#[repr(C)]`, `CStr` i `CString`. Wystawianie API Rusta dla C (`cbindgen`) i UniFFI: zob. sekcja 12.1, C w firmware: zob. sekcja 22.

**Dowód:** bezpieczna obudowa w Ruście dla małej biblioteki C (np. kompresji lub parsera) przez `bindgen`, z testami uruchamianymi pod AddressSanitizer po stronie C i notatką, kto i kiedy zwalnia każdy zasób.

#### Etap 2: czytanie C++, Javy i Objective-C

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| LearnCpp.com (rozdziały o wskaźnikach, referencjach, klasach, szablonach, RAII i inteligentnych wskaźnikach) | Alex, LearnCpp.com | kurs online | 8–10 h | 0 zł | https://www.learncpp.com |
| C++ Core Guidelines | Bjarne Stroustrup, Herb Sutter | wytyczne | 2–3 h (wybrane sekcje) | 0 zł | https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines |
| Learn Java | Oracle, dev.java | kurs online | 5–8 h | 0 zł | https://dev.java/learn/ |
| Programming with Objective-C (archiwum Apple, ostatnia aktualizacja 2014 r., nadal aktualne pojęciowo) | Apple | przewodnik | 3–4 h | 0 zł | https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html |
| Importing Objective-C into Swift | Apple | dokumentacja | 1 h | 0 zł | https://developer.apple.com/documentation/swift/importing-objective-c-into-swift |

Celem jest czytanie, nie pisanie: zrozumieć, co robi fragment biblioteki platformowej, skąd bierze się wyciek lub awaria i jak API przekłada się na wiązanie w Ruście, Kotlinie lub Swifcie. Szczególnie ważne: w C++ RAII, szablony i wyjątki na granicy FFI; w Javie wątki, wyjątki kontrolowane i JNI; w Objective-C wysyłanie komunikatów, ARC i cykle referencji, adnotacje nullability.

**Dowód:** notatka z analizy fragmentu cudzego kodu w każdym z trzech języków (np. biblioteki C++ używanej przez llama.cpp, klasy Javy z Android SDK, starego modułu Objective-C w przejmowanej aplikacji iOS), opisująca przepływ danych, własność pamięci i miejsca ryzyka.

---

## 13. UI/UX

*Warstwa 4: rdzeń kompilowany i produkt. Opiera się na: 3. Jest podstawą: 14–19 i 21.*

- Proces: przepływy użytkownika, makiety, prototypy (Figma), testy użyteczności, UX writing.
- Systemy projektowe i tokeny, spójne między web, desktop i mobile.
- Wytyczne platform: Apple Human Interface Guidelines, Material Design 3, Fluent (Windows), GNOME HIG.
- Stany ekranów (pusty, ładowanie, błąd, sukces, offline), tryb ciemny, responsywność, lokalizacja.
- Dostępność: WCAG 2.2, Europejski akt o dostępności, technologie wspomagające na każdej platformie (VoiceOver, TalkBack, Narrator, Orca), dostępność natywnych UI w Ruście.
- Onboarding, paywalle i ekrany zakupu zgodne z regułami sklepów i prawem konsumenckim.

### 13.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 9 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przy doświadczeniu seniorskim we frontendzie etapy 0–1 można zaliczyć samym dowodem i wracać do materiałów tylko tam, gdzie dowód nie wychodzi; etapy o badaniach, wytycznych platform natywnych i dostępności poza webem zwykle są nowe. Dostępność web (WCAG 2.2, ARIA, testy w przeglądarce) jest w sekcji 3, tutaj chodzi o proces projektowy, platformy natywne i prawo. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | podstawy użyteczności i psychologii interfejsu | 30–40 h | podstawy |
| 1 | projektowanie wizualne i Figma | 40–50 h | podstawy |
| 2 | badania i testy użyteczności | 25–35 h | W |
| 3 | wytyczne platform: Apple, Google, Microsoft, GNOME | 40–50 h | W |
| 4 | systemy projektowe i tokeny dla wielu platform | 25–35 h | W |
| 5 | UX writing i mikroteksty | 15–20 h | W |
| 6 | dostępność na wszystkich platformach i prawo | 40–50 h | E |
| 7 | onboarding, paywalle i etyka: reguły sklepów i prawo konsumenckie | 20–25 h | E |
| 8 | ekspert: audyty, recenzja interfejsów z AI, aktualność | stale, ok. 1–2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 235–305 h, czyli 5–7 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: podstawy użyteczności

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Don’t Make Me Think, Revisited (wydanie 3) | Steve Krug, New Riders | książka, od podstaw | 5–6 h | płatna | https://sensible.com/dont-make-me-think/ |
| The Design of Everyday Things (wydanie poprawione i rozszerzone) | Don Norman, Basic Books | książka, podstawowy–średni | 10–12 h | płatna | https://www.hachettebookgroup.com/titles/don-norman/the-design-of-everyday-things-revised-and-expanded-edition/9780465050659/ |
| 10 Usability Heuristics for User Interface Design i artykuły pokrewne | Jakob Nielsen, Nielsen Norman Group | artykuły | 6–8 h | 0 zł | https://www.nngroup.com/articles/ten-usability-heuristics/ |
| Laws of UX (strona) i książka Laws of UX (wydanie 2, 2024) | Jon Yablonski, O’Reilly | strona i książka, podstawowy–średni | 6–8 h | 0 zł / płatna | https://lawsofux.com, https://www.oreilly.com/library/view/laws-of-ux/9781098146955/ |

Szczególnie ważne: afordancje i sygnifikatory, informacja zwrotna, model mentalny użytkownika, zapobieganie błędom zamiast komunikatów o błędach, prawa Hicka, Fittsa i Jakoba, obciążenie poznawcze.

**Dowód:** ocena heurystyczna jednej istniejącej aplikacji (najlepiej z portfolio przejmowanych projektów): 15–20 problemów przypisanych do heurystyk Nielsena, z oceną wagi i propozycją poprawki dla każdego.

#### Etap 1: projektowanie wizualne i Figma

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Refactoring UI | Adam Wathan, Steve Schoger | książka PDF z materiałami, od podstaw do średniego | 8–10 h | płatna (2 rozdziały za darmo) | https://www.refactoringui.com |
| Figma Learn: Figma Design for beginners, kursy i dokumentacja (auto layout, komponenty, warianty, zmienne, Dev Mode) | Figma | kurs i dokumentacja | 20–25 h | 0 zł (narzędzie z planem darmowym i płatnymi) | https://help.figma.com/hc/en-us |
| Practical Typography | Matthew Butterick | książka online, podstawowy–średni | 5–6 h | 0 zł | https://practicaltypography.com |

Szczególnie ważne: hierarchia wizualna, siatka i rytm odstępów, skala typograficzna, palety kolorów z kontrastem od początku, stany komponentów, tryb ciemny, komponenty i warianty w Figmie zamiast kopiowania ramek.

**Dowód:** w Figmie projekt 5–7 ekranów jednej własnej aplikacji (lista, szczegóły, formularz, ustawienia, ekran zakupu) w wersji mobilnej i desktopowej, z jasnym i ciemnym motywem, zbudowany z własnych komponentów z wariantami i z prototypem klikanym.

#### Etap 2: badania i testy użyteczności

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Rocket Surgery Made Easy | Steve Krug, New Riders | książka, od podstaw | 4–5 h | płatna | https://sensible.com/rocket-surgery-made-easy/ |
| Just Enough Research (wydanie 2) | Erika Hall | książka, podstawowy–średni | 4–5 h | płatna | https://abookapart.com/blogs/press/just-enough-research-2nd-edition-is-now-available |
| Artykuły NN/g o badaniach (testy moderowane i zdalne, wywiady, liczba uczestników, ankiety) | Nielsen Norman Group | artykuły | 8–10 h | 0 zł | https://www.nngroup.com/articles/ |
| Kursy UX Nielsen Norman Group (opcjonalnie, z certyfikacją) | Nielsen Norman Group | kursy online na żywo i do samodzielnej nauki | wg potrzeb | płatne | https://www.nngroup.com/courses/ |

Szczególnie ważne: pytania bez sugerowania odpowiedzi, scenariusz zadań zamiast pytania o opinię, 5 uczestników na rundę i kolejne rundy po poprawkach, analityka produktowa jako uzupełnienie, a nie zamiennik rozmów, zgody i dane osobowe uczestników (RODO).

**Dowód:** dwie rundy testów użyteczności (po 5 osób) prototypu z etapu 1: scenariusz, nagrania za zgodą, lista problemów z częstością i wagą, poprawki między rundami i porównanie wyników.

#### Etap 3: wytyczne platform

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Human Interface Guidelines | Apple | wytyczne iOS, iPadOS, macOS i pozostałych platform Apple | 12–15 h | 0 zł | https://developer.apple.com/design/human-interface-guidelines/ |
| Material Design 3 | Google | system projektowy i wytyczne Androida | 10–12 h | 0 zł | https://m3.material.io |
| Fluent 2 Design System | Microsoft | wytyczne i komponenty: Windows, web, iOS, Android | 6–8 h | 0 zł | https://fluent2.microsoft.design |
| GNOME Human Interface Guidelines | GNOME | wytyczne GTK 4 i Libadwaita | 4–6 h | 0 zł | https://developer.gnome.org/hig/ |

Szczególnie ważne: nawigacja i gesty specyficzne dla platformy (wstecz w Androidzie, paski kart i arkusze w iOS, menu i skróty klawiaturowe na desktopie), dynamiczny rozmiar tekstu, obszary dotyku, okna i ich rozmiary na desktopie, kiedy Tauri z Reactem może wyglądać „tak samo wszędzie”, a kiedy użytkownik oczekuje wyglądu natywnego.

**Dowód:** ten sam przepływ (np. zakup i ustawienia) zaprojektowany w trzech wariantach: iOS, Android i desktop, z notatką, które różnice wynikają z wytycznych platformy, a które są świadomym odstępstwem i dlaczego.

#### Etap 4: systemy projektowe i tokeny

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Design Tokens Format Module 2025.10 (pierwsza stabilna wersja, październik 2025) | Design Tokens Community Group (W3C) | specyfikacja | 4–6 h | 0 zł | https://www.designtokens.org/tr/2025.10/format/ |
| Figma Learn: zmienne, tryby i biblioteki | Figma | dokumentacja | 4–5 h | 0 zł | https://help.figma.com/hc/en-us |
| Fluent 2 i Material Design 3: rozdziały o tokenach i motywach | Microsoft, Google | dokumentacja jako wzorzec | 4–6 h | 0 zł | https://fluent2.microsoft.design, https://m3.material.io |

Specyfikacja DTCG jest raportem grupy społecznościowej W3C, a nie standardem W3C, ale jest stabilna i stała się wspólnym formatem wymiany między narzędziami. Tokeny i komponenty web (Tailwind, Radix, shadcn/ui) są w sekcji 3.

**Dowód:** jedno źródło tokenów w formacie DTCG (kolory z trybami jasnym i ciemnym, typografia, odstępy, promienie) generowane w CI do zmiennych CSS i motywu Tailwind, stałych Swift, zasobów Kotlin/Compose i motywu natywnego UI w Ruście (np. Slint); zmiana jednego tokenu widoczna na wszystkich platformach po jednym buildzie.

#### Etap 5: UX writing

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Strategic Writing for UX (wydanie 2, 2025) | Torrey Podmajersky, O’Reilly | książka, podstawowy–średni | 6–8 h | płatna | https://www.oreilly.com/library/view/strategic-writing-for/9781098174323/ |
| Microcopy: The Complete Guide | Kinneret Yifrah | książka, podstawowy | 5–6 h | płatna | https://www.microcopybook.com |
| Wytyczne pisania w HIG, Material Design 3 i GNOME HIG | Apple, Google, GNOME | wytyczne | 2–3 h | 0 zł | jak w etapie 3 |

Szczególnie ważne: komunikaty błędów mówiące, co zrobić dalej, stany puste, przyciski nazwane czynnością, spójny słownik w całym produkcie, teksty przygotowane do lokalizacji (długość, liczba mnoga, płeć gramatyczna w polskim), prosty język jako element dostępności.

**Dowód:** przepisany komplet tekstów jednej aplikacji (onboarding, błędy, stany puste, paywall, potwierdzenia) z krótkim przewodnikiem stylu i słownikiem, w dwóch językach przez pliki tłumaczeń, bez tekstów wpisanych na stałe w kodzie.

#### Etap 6: dostępność na wszystkich platformach i prawo

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Inclusive Components | Heydon Pickering | artykuły (0 zł) i książka (płatna), średni | 6–8 h | 0 zł / płatna | https://inclusive-components.design |
| Deque University: pakiet z kursem dostępności aplikacji natywnych (Android, iOS) | Deque Systems | kursy online | 20–30 h | abonament | https://dequeuniversity.com/online-courses/ |
| Accessibility (dokumentacja dla deweloperów) i Accessibility Nutrition Labels w App Store Connect | Apple | dokumentacja | 3–4 h | 0 zł | https://developer.apple.com/accessibility/, https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels |
| Build accessible apps, dostępność w Jetpack Compose | Google | dokumentacja | 3–4 h | 0 zł | https://developer.android.com/guide/topics/ui/accessibility |
| Accessibility overview: Windows apps (UI Automation, wysoki kontrast) i Accessibility Insights | Microsoft | dokumentacja i narzędzie | 2–3 h | 0 zł | https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility, https://accessibilityinsights.io |
| AccessKit: dostępność UI rysowanych w Ruście (egui, Slint i inne) | projekt AccessKit | dokumentacja | 1–2 h | 0 zł | https://accesskit.dev |
| WCAG-EM: metodyka oceny zgodności i Easy Checks | W3C WAI | metodyka | 2–3 h | 0 zł | https://www.w3.org/WAI/test-evaluate/ |
| Dyrektywa (UE) 2019/882 (Europejski akt o dostępności) | UE (EUR-Lex) | akt prawny | 3–4 h | 0 zł | https://eur-lex.europa.eu/eli/dir/2019/882/oj |
| Ustawa z 26 kwietnia 2024 r. o zapewnianiu spełniania wymagań dostępności niektórych produktów i usług przez podmioty gospodarcze (Dz.U. 2024 poz. 731) | Sejm RP | akt prawny | 3–4 h | 0 zł | https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20240000731 |
| EN 301 549 V4.1.1 (wrzesień 2026) | ETSI, CEN, CENELEC | norma zharmonizowana w przygotowaniu | 4–6 h | 0 zł | https://www.etsi.org |

Stan na 11 października 2026 r.: polska ustawa wdrażająca EAA obowiązuje od 28 czerwca 2025 r.; EN 301 549 V4.1.1, oparta na WCAG 2.2 AA z dodatkowymi kryteriami, została opublikowana 2 września 2026 r., ale domniemanie zgodności z EAA da dopiero jej publikacja w Dzienniku Urzędowym UE. Apple pokazuje w App Store etykiety dostępności (Accessibility Nutrition Labels); na razie są dobrowolne, a Apple zapowiada, że staną się obowiązkowe. Mikroprzedsiębiorcy świadczący usługi są zwolnieni z części obowiązków ustawy, ale klienci firmy zwykle nie są.

**Dowód:** audyt dostępności własnej aplikacji na trzech platformach (web, iOS lub Android, desktop): przejście kluczowych zadań (pierwsze uruchomienie, logowanie, zakup, ustawienia) z VoiceOver lub TalkBack, Narratorem lub Orca, powiększonym tekstem i samą klawiaturą; raport według WCAG-EM z poprawkami i uczciwie wypełnione etykiety dostępności w App Store Connect.

#### Etap 7: onboarding, paywalle i etyka

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| App Review Guidelines, sekcja 3.1 Payments (zakupy w aplikacji, subskrypcje, linki zewnętrzne) | Apple | zasady sklepu | 3–4 h | 0 zł | https://developer.apple.com/app-store/review/guidelines/ |
| Payments i Create and manage subscriptions (przejrzystość ofert) | Google Play Console Help | zasady sklepu | 2–3 h | 0 zł | https://support.google.com/googleplay/android-developer/answer/9858738, https://support.google.com/googleplay/android-developer/answer/140504 |
| Deceptive Patterns | Harry Brignull | książka i katalog wzorców, średni | 5–6 h | płatna (katalog online 0 zł) | https://deceptive.design |
| Dyrektywa (UE) 2023/2673 (m.in. przycisk odstąpienia od umowy zawartej online, stosowany od 19 czerwca 2026 r.) | UE (EUR-Lex) | akt prawny | 2–3 h | 0 zł | https://eur-lex.europa.eu/eli/dir/2023/2673/oj |
| Artykuły NN/g o onboardingu, paywallach i formularzach | Nielsen Norman Group | artykuły | 3–4 h | 0 zł | https://www.nngroup.com/articles/ |

Szczególnie ważne: cena, okres rozliczenia, warunki okresu próbnego i sposób anulowania widoczne przed zakupem, przywracanie zakupów, brak zatrzymywania użytkownika przy rezygnacji, różnice zasad między sklepami i kanałem web (Merchant of Record), wzorce zwodnicze jako ryzyko prawne, a nie tylko etyczne. Implementacja zakupów i licencji jest w sekcjach 5, 18 i 19.

**Dowód:** onboarding i paywall jednej własnej aplikacji w trzech kanałach (App Store, Google Play, web), sprawdzone punkt po punkcie z sekcją 3.1 App Review Guidelines, zasadami Google Play i przepisami o prawach konsumenta; rezygnacja z abonamentu osiągalna w nie więcej krokach niż zakup; przejście przez recenzję w obu sklepach bez odrzucenia za płatności.

#### Etap 8: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Nowe artykuły i badania NN/g | Nielsen Norman Group | źródło na bieżąco | ok. 1 h tygodniowo | 0 zł | https://www.nngroup.com/articles/ |
| Zmiany w HIG, Material Design i Fluent oraz sesje projektowe z konferencji WWDC i Google I/O | Apple, Google, Microsoft | źródła pierwotne | wg potrzeb | 0 zł | https://developer.apple.com/design/, https://m3.material.io |
| Zmiany w zasadach sklepów i prawie (EAA, EN 301 549, prawa konsumenta) | Apple, Google, UE | źródła pierwotne | ok. 1 h miesięcznie | 0 zł | jak w etapach 6 i 7 |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja interfejsów z AI:** 20 ekranów lub pull requestów z UI wygenerowanych przez agentów, ocenianych według listy kontrolnej z etapów 3–7 (brakujące stany pusty, błędu i offline, wartości wpisane zamiast tokenów, wzorce z innej platformy, ikony bez etykiet dostępności, teksty na stałe w kodzie, wzorce zwodnicze w paywallu, „ładne, ale nieużyteczne” układy),
- **audyt UX i dostępności przejmowanej aplikacji:** pierwsza aplikacja klienta przeprowadzona przez ocenę heurystyczną, test z 5 użytkownikami i audyt dostępności, z planem poprawek uszeregowanym według wpływu i kosztu,
- **system projektowy w praktyce:** tokeny i komponenty używane przez wszystkie własne aplikacje, z dokumentacją, którą agenci czytają jako kontekst,
- **pomiar:** jedna zmiana UX na kwartał zweryfikowana danymi (konwersja paywalla, ukończenie onboardingu, zgłoszenia do wsparcia).

**Dowód poziomu E:** samodzielnie, bez agenta, w 2 dni przeprowadzasz audyt UX i dostępności nieznanej aplikacji klienta na dwóch platformach, z testem z co najmniej 3 użytkownikami, raportem z priorytetami, oceną zgodności z EAA i regułami sklepów oraz poprawionym projektem najważniejszego przepływu, i umiesz obronić rekomendacje przed osobą nietechniczną.

---

## 14. Desktop: wspólne

*Warstwa 5: desktop. Opiera się na: 3, 8, 12 i 13. Jest podstawą: 15–17 i rdzenia współdzielonego z mobile.*

- Tauri 2: architektura (proces Rust i webview), polecenia IPC, system capabilities i uprawnień, pluginy, Content Security Policy, aktualizacje z podpisem.
- Alternatywy natywne w Ruście: Slint, egui, Iced, Dioxus; kryteria wyboru (rozmiar, wygląd natywny, dostępność).
- Praca offline, lokalne przechowywanie, bezpieczne sekrety (Keychain, Windows Credential Manager/DPAPI, libsecret).
- Licencjonowanie offline i online, aktywacja, automatyczne aktualizacje, raportowanie awarii z symbolami.

### 14.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 6 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Wszystkie dowody budują kolejne wersje tego samego produktu: desktopowego narzędzia, które skanuje repozytoria pod kątem sekretów, licencji i podatnych zależności. Przy doświadczeniu seniorskim z Reactem etap 1 można zaliczyć samym dowodem, ale etapów 2 i 4 nie warto skracać, bo tam leżą błędy, których agent najczęściej nie widzi. Czas podany dla osoby startującej od zera, przy opanowanym Ruście (zob. sekcja 12); ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem. Stan dokumentacji: Tauri 2.12 (wrzesień 2026).

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | system operacyjny pod aplikacją: procesy, pamięć, pliki, uprawnienia | 30–40 h | podstawy |
| 1 | Tauri 2: architektura, IPC, pluginy | 30–40 h | W |
| 2 | bezpieczeństwo Tauri: uprawnienia, capabilities, zakresy, CSP | 20–25 h | W |
| 3 | natywny UI w Ruście i kryteria wyboru | 30–40 h | W |
| 4 | infrastruktura produktu: sekrety, dane lokalne, licencje, aktualizacje, awarie | 30–40 h | E |
| 5 | ekspert: podatności, model zagrożeń aktualizacji, recenzja kodu AI | stale, ok. 1–2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 140–185 h, czyli 4–5 miesięcy przy 8–10 h tygodniowo. Szczegóły każdego systemu (instalatory, podpisy, sklepy) są w sekcjach 15–17.

#### Etap 0: system operacyjny pod aplikacją

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Operating Systems: Three Easy Pieces (części o procesach, pamięci wirtualnej, współbieżności i systemach plików) | Remzi H. Arpaci-Dusseau, Andrea C. Arpaci-Dusseau | podręcznik, od podstaw do średniego | 30–40 h | 0 zł (PDF), druk płatny | https://pages.cs.wisc.edu/~remzi/OSTEP/ |

Szczególnie ważne: proces a wątek, przestrzeń adresowa, deskryptory plików, uprawnienia użytkownika, sygnały i zakończenie procesu, komunikacja międzyprocesowa. To język, którym opisane są capabilities Tauri, sandboxy i instalatory.

**Dowód:** narzędzie CLI w Ruście, które rekurencyjnie przechodzi katalog repozytorium, pomija `.git` i dowiązania symboliczne prowadzące poza katalog, obsługuje brak uprawnień do pliku bez paniki i działa tak samo na Linuksie, macOS i Windows (ścieżki, wielkość liter, końce linii).

#### Etap 1: Tauri 2

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Dokumentacja Tauri 2: Quick Start, Prerequisites, Core Concepts (Architecture, Process Model, App Size, Inter-Process Communication) | Tauri | dokumentacja, podstawowy–średni | 10–12 h | 0 zł | https://v2.tauri.app/start/, https://v2.tauri.app/concept/ |
| Calling Rust from the Frontend, Calling the Frontend from Rust (polecenia, zdarzenia, kanały) | Tauri | dokumentacja | 4–6 h | 0 zł | https://v2.tauri.app/develop/calling-rust/ |
| Plugins: przegląd oficjalnych pluginów (File System, Dialog, Store, SQL, Single Instance, Deep Linking, Autostart, Window State, Updater) | Tauri | dokumentacja | 6–8 h | 0 zł | https://v2.tauri.app/plugin/ |
| Plugin Development | Tauri | dokumentacja, zaawansowany | 4–6 h | 0 zł | https://v2.tauri.app/develop/plugins/ |
| Releases (changelogi `tauri`, `tauri-cli` i pluginów) | Tauri | źródło pierwotne | 1–2 h | 0 zł | https://v2.tauri.app/release/ |

Szczególnie ważne: Tauri używa webview systemu (WebView2 na Windows, WKWebView na macOS, WebKitGTK na Linuksie), więc ten sam frontend może zachowywać się różnie na trzech systemach; długie operacje nie mogą blokować wątku głównego; dane do frontendu idą kanałem lub zdarzeniami, a nie jednym ogromnym wynikiem polecenia.

**Dowód:** aplikacja Tauri 2 z frontendem React: wybór katalogu repozytorium okienkiem systemowym, skan w Ruście uruchomiony asynchronicznie, postęp przesyłany kanałem, możliwość anulowania, wynik w tabeli; działa jedna instancja aplikacji, a stan okna jest pamiętany między uruchomieniami.

#### Etap 2: bezpieczeństwo Tauri

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Security: Overview, Permissions, Command Scopes, Capabilities, Runtime Authority, Asset protocol scope, CSP, HTTP Headers | Tauri | dokumentacja | 8–10 h | 0 zł | https://v2.tauri.app/security/ |
| Isolation Pattern, Brownfield Pattern | Tauri | dokumentacja, zaawansowany | 2–3 h | 0 zł | https://v2.tauri.app/concept/inter-process-communication/isolation/ |
| Application Lifecycle Threats, Tauri Ecosystem Security | Tauri | dokumentacja | 2–3 h | 0 zł | https://v2.tauri.app/security/lifecycle/ |
| Electron Security: lista kontrolna (jako porównanie zagrożeń aplikacji z webview) | OpenJS Foundation, Electron | dokumentacja | 2–3 h | 0 zł | https://www.electronjs.org/docs/latest/tutorial/security |
| Komunikaty bezpieczeństwa Tauri (GitHub Security Advisories), m.in. obejście kontroli pochodzenia przez iframe (2024), wywołanie lokalnych poleceń IPC ze zdalnej strony (2026), wyciek klucza prywatnego updatera przez zmienne środowiskowe Vite (2023) | Tauri | źródło pierwotne, studium przypadków | 2–3 h | 0 zł | https://github.com/tauri-apps/tauri/security/advisories |

Szczególnie ważne: webview traktowany jako niezaufany; każde polecenie IPC waliduje wejście tak, jak endpoint API; capabilities przypisane do konkretnych okien; zakresy plików zawężone do katalogów wybranych przez użytkownika; brak `unsafe-inline` w CSP; zdalna treść nigdy nie dostaje dostępu do poleceń. Ogólne zasady bezpieczeństwa i modelowanie zagrożeń: zob. sekcja 10.

**Dowód:** aplikacja z etapu 1 z minimalnymi capabilities (osobne dla okna głównego i okna ustawień), zakresem systemu plików ograniczonym do wybranego repozytorium i ścisłą CSP; test, w którym kod wstrzyknięty do webview próbuje odczytać `~/.ssh` i wywołać polecenie spoza capability, i dostaje odmowę; krótki dokument z granicami zaufania.

#### Etap 3: natywny UI w Ruście

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Slint: dokumentacja, Quickstart, Rust API (`slint` 1.18) | SixtyFPS GmbH | dokumentacja z tutorialem | 10–12 h | 0 zł; licencja royalty-free na desktop, embedded płatny lub GPLv3 | https://docs.slint.dev |
| egui i eframe, szablon `eframe_template` | Emil Ernerfeldt | dokumentacja i szablon | 6–8 h | 0 zł | https://docs.rs/egui, https://github.com/emilk/eframe_template |
| The iced book (niedokończony) i dokumentacja `iced` 0.14 | zespół iced | książka online i dokumentacja | 5–6 h | 0 zł | https://book.iced.rs, https://docs.rs/iced |
| Dioxus 0.7: Desktop (system WebView przez `wry`) | DioxusLabs | dokumentacja | 3–4 h | 0 zł | https://dioxuslabs.com/learn/0.7/ |
| AccessKit: infrastruktura dostępności dla toolkitów rysujących własny UI | projekt AccessKit | dokumentacja | 1–2 h | 0 zł | https://accesskit.dev |
| „A 2025 Survey of Rust GUI Libraries” (test czytnika ekranu i IME w 43 bibliotekach) | boringcactus | artykuł, przegląd | 2–3 h | 0 zł | https://www.boringcactus.com/2025/04/13/2025-survey-of-rust-gui-libraries.html |

Szczególnie ważne: kryteria wyboru zapisane w ADR, a nie gust: dostępność (AccessKit w Slint i egui), obsługa IME, wygląd natywny, rozmiar i czas startu, licencja, dojrzałość API (iced i Dioxus zmieniają API między wersjami 0.x). Dioxus na desktopie renderuje przez webview, więc nie jest „natywnym” UI w tym samym sensie co Slint czy egui.

**Dowód:** ten sam rdzeń skanera (osobny crate bez zależności od UI) z drugim interfejsem w Slint albo egui; porównanie z wersją Tauri: rozmiar instalatora, czas startu, zużycie pamięci, test z czytnikiem ekranu na każdym systemie; ADR z decyzją dla własnej aplikacji.

#### Etap 4: infrastruktura produktu

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| `keyring` 4 i `keyring-core` z osobnymi magazynami dla Keychain, Windows Credential Manager i Secret Service | Daniel Brotsky i współautorzy | dokumentacja crate’ów | 2–3 h | 0 zł | https://docs.rs/keyring |
| Keychain services, CryptProtectData (DPAPI), CredWriteW, Secret Service API | Apple, Microsoft, freedesktop.org | dokumentacja systemowa | 4–5 h | 0 zł | https://developer.apple.com/documentation/security/keychain-services, https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata, https://specifications.freedesktop.org/secret-service/latest/ |
| Tauri Updater: klucze, format manifestu, serwer statyczny i dynamiczny, podpis nie do wyłączenia | Tauri | dokumentacja | 3–4 h | 0 zł | https://v2.tauri.app/plugin/updater/ |
| The Update Framework (TUF): specyfikacja i model zagrożeń aktualizacji | CNCF | specyfikacja, zaawansowany | 4–6 h | 0 zł | https://theupdateframework.io |
| Keygen: licencjonowanie offline (podpisane pliki licencji, Ed25519), aktywacja urządzeń | Keygen | dokumentacja | 4–5 h | 0 zł | https://keygen.sh/docs/choosing-a-licensing-model/offline-licenses/ |
| Sentry for Native i Minidumps; crate’y `crash-handler` i `minidumper` | Sentry, Embark Studios | dokumentacja | 4–6 h | 0 zł | https://docs.sentry.io/platforms/native/guides/minidumps/, https://docs.rs/crash-handler, https://docs.rs/minidumper |
| Distribute: przegląd formatów i pipeline’ów | Tauri | dokumentacja | 2–3 h | 0 zł | https://v2.tauri.app/distribute/ |

Szczególnie ważne: sekrety użytkownika (tokeny API, klucz licencji) tylko w magazynie systemu, nigdy w pliku konfiguracyjnym ani w `localStorage` webview; licencja weryfikowana kluczem publicznym wbudowanym w aplikację, z łaskawym okresem offline; aktualizacja z kanałami (stabilny, beta), możliwością wycofania i ochroną przed cofnięciem do podatnej wersji (wymóg CRA dotyczący poprawek bezpieczeństwa); od wersji 2.10 plugin updater Tauri obsługuje także pakiety `.deb` i `.rpm`. Integracja z Merchant of Record po stronie serwera: zob. sekcja 5; podpisy i klucze w CI: zob. sekcja 9.

**Dowód:** narzędzie z etapu 2 sprzedawane „na niby”: zakup w środowisku testowym MoR wywołuje webhook, który wystawia podpisaną licencję; aplikacja weryfikuje ją offline i trzyma w magazynie systemu; aktualizacja z podpisem przechodzi ze stabilnej wersji N do N+1 na trzech systemach, a próba podsunięcia niepodpisanej lub starszej paczki kończy się odmową; wymuszona awaria procesu daje minidump z czytelnym, zsymbolizowanym stosem.

#### Etap 5: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Blog i informacje o wydaniach Tauri, komunikaty bezpieczeństwa | Tauri | źródła pierwotne | ok. 30 min tygodniowo | 0 zł | https://v2.tauri.app/blog/, https://v2.tauri.app/release/ |
| Komunikaty bezpieczeństwa silników webview: WebKitGTK Security Advisories, informacje o wydaniach WebView2 | WebKitGTK, Microsoft | źródła pierwotne | ok. 15 min tygodniowo | 0 zł | https://webkitgtk.org/security.html, https://learn.microsoft.com/en-us/microsoft-edge/webview2/ |
| Kod źródłowy `tauri`, `wry` i `tao` (obsługa IPC, capabilities, updater) | Tauri | kod źródłowy | wg potrzeb | 0 zł | https://github.com/tauri-apps |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 20 pull requestów wygenerowanych przez agentów w aplikacji desktopowej, recenzowanych według listy kontrolnej z etapów 2 i 4: rozszerzone capabilities „żeby zadziałało”, polecenia IPC bez walidacji ścieżek, `unwrap()` w poleceniach (panika zabija proces), blokujące operacje na wątku głównym, sekrety w plikach lub w webview, wyłączona CSP, wymyślone opcje `tauri.conf.json` i nieistniejące API pluginów,
- **ćwiczenie incydentu:** podatność w zależności lub w webview, od komunikatu do podpisanej aktualizacji u użytkowników w 24 h, z zapisem przebiegu do dokumentacji CRA,
- **macierz testowa:** najstarsze i najnowsze wspierane wersje trzech systemów na czystych maszynach wirtualnych, instalacja, aktualizacja i odinstalowanie (zob. sekcja 6),
- **wkład w open source** w Tauri lub jeden z toolkitów UI, choćby w dokumentację lub test błędu.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz błąd, który występuje tylko na jednym systemie (np. różnica webview, ścieżek albo uprawnień), wydajesz poprawkę przez podpisaną aktualizację i umiesz wyjaśnić przyczynę osobie nietechnicznej.

---

## 15. Linux

*Warstwa 5: desktop. Opiera się na: 9 i 14.*

- Formaty: `.deb`, `.rpm`, AppImage, Flatpak (Flathub), Snap; repozytoria pakietów z podpisem GPG.
- Zgodność glibc między dystrybucjami, zależności webview (WebKitGTK), Wayland i X11.
- Standardy freedesktop: pliki `.desktop`, ścieżki XDG, powiadomienia, autostart; systemd dla usług.

### 15.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 4 etapy. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Wszystkie dowody dotyczą tej samej aplikacji z sekcji 14.1: narzędzia desktopowego do kontroli sekretów, licencji i zależności w repozytoriach, sprzedawanego poza sklepem przez Merchant of Record. Przy codziennej pracy na Linuksie etap 0 można zaliczyć samym dowodem. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | Linux od strony aplikacji: system plików, procesy, biblioteki, systemd | 30–40 h | podstawy |
| 1 | integracja z pulpitem: standardy freedesktop, portale, Wayland i X11 | 15–20 h | W |
| 2 | pakiety i repozytoria: `.deb`, `.rpm`, AppImage, Flatpak, Snap | 35–45 h | W |
| 3 | ekspert: zgodność między dystrybucjami, utrzymanie repozytoriów, recenzja kodu AI | stale, ok. 1 h tygodniowo | E |

Razem od zera do poziomu E: ok. 80–105 h, czyli 2–3 miesiące przy 8–10 h tygodniowo.

#### Etap 0: Linux od strony aplikacji

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| How Linux Works, 3rd Edition | Brian Ward, No Starch Press | książka, podstawowy–średni | 20–25 h | płatna | https://nostarch.com/howlinuxworks3 |
| The Linux Programming Interface (wybrane rozdziały: procesy, pliki, sygnały, biblioteki współdzielone) | Michael Kerrisk, No Starch Press | książka, zaawansowany, jako kompendium | 8–10 h | płatna | https://man7.org/tlpi/ |
| systemd: dokumentacja i strony podręcznika (`systemd.unit`, `systemd.service`, usługi użytkownika) | projekt systemd | dokumentacja | 3–4 h | 0 zł | https://systemd.io |

Szczególnie ważne: hierarchia katalogów, uprawnienia i właściciele plików, dynamiczne łączenie i wersje symboli glibc (`ldd`, `objdump -T`), zmienne środowiskowe, a w szczególności to, że aplikacje graficzne nie dziedziczą `$PATH` z plików powłoki.

**Dowód:** binarka skanera z sekcji 14.1 uruchamiana jako usługa użytkownika systemd z timerem (nocny skan wybranych repozytoriów), logami w journald i poprawnym zakończeniem po `SIGTERM`; lista symboli glibc, od których zależy binarka, z najwyższą wymaganą wersją.

#### Etap 1: integracja z pulpitem

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Specyfikacje freedesktop.org: Desktop Entry, Base Directory, Autostart, Notification, Icon Theme, Secret Service | freedesktop.org | specyfikacje | 6–8 h | 0 zł | https://specifications.freedesktop.org |
| XDG Desktop Portal: dokumentacja API (File Chooser, Secret, Background, Notification, OpenURI) | projekt Flatpak, freedesktop.org | dokumentacja | 4–5 h | 0 zł | https://flatpak.github.io/xdg-desktop-portal/docs/ |
| The Wayland Protocol | Drew DeVault | książka online, średni | 4–6 h | 0 zł | https://wayland-book.com |
| AppStream: format metadanych MetaInfo | freedesktop.org | dokumentacja | 1–2 h | 0 zł | https://www.freedesktop.org/software/appstream/docs/ |

Szczególnie ważne: pliki aplikacji w `$XDG_CONFIG_HOME`, `$XDG_DATA_HOME` i `$XDG_CACHE_HOME`, a nie w katalogu domowym; zachowanie pod Wayland (brak globalnych skrótów i pozycjonowania okien bez portali, inne skalowanie); portal Secret i Secret Service zamiast plików z tokenami; różnice między GNOME i KDE w zasobniku systemowym. Wytyczne GNOME HIG: zob. sekcja 13.

**Dowód:** aplikacja Tauri z sekcji 14.1 z poprawnym plikiem `.desktop`, ikonami w kilku rozmiarach, plikiem MetaInfo przechodzącym walidację, danymi w ścieżkach XDG, autostartem przez plik autostart i powiadomieniem o wykrytym sekrecie; przetestowana w sesji Wayland i X11 na GNOME oraz KDE.

#### Etap 2: pakiety i repozytoria

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Guide for Debian Maintainers (następca Debian New Maintainers’ Guide) | Osamu Aoki, Debian | podręcznik, średni | 6–8 h | 0 zł | https://www.debian.org/doc/manuals/debmake-doc/ |
| Debian Policy Manual (rozdziały o plikach kontrolnych, zależnościach, skryptach maintainera) | Debian | norma, jako kompendium | 4–6 h | 0 zł | https://www.debian.org/doc/debian-policy/ |
| `apt-secure(8)`: podpisane pliki `Release`/`InRelease` i `Signed-By` | Debian | dokumentacja | 1–2 h | 0 zł | https://manpages.debian.org/apt-secure |
| RPM Packaging Guide | Adam Miller, Maxim Svistunov, Marie Doleželová i in. (Red Hat) | podręcznik, średni | 5–6 h | 0 zł | https://rpm-packaging-guide.github.io |
| Fedora Packaging Guidelines, w tym Rust Packaging Guidelines | Fedora Project | wytyczne | 3–4 h | 0 zł | https://docs.fedoraproject.org/en-US/packaging-guidelines/ |
| Dokumentacja AppImage: Packaging Guide, Best practices, aktualizacje przez zsync | projekt AppImage | dokumentacja | 3–4 h | 0 zł | https://docs.appimage.org |
| Dokumentacja Flatpak: Building, Sandbox Permissions, Portals, Publishing | projekt Flatpak | dokumentacja | 6–8 h | 0 zł | https://docs.flatpak.org/en/latest/ |
| Flathub dla autorów: Requirements, MetaInfo Guidelines, Submission, Verification, zasady monetyzacji | Flathub | dokumentacja | 3–4 h | 0 zł | https://docs.flathub.org/docs/for-app-authors/requirements |
| Snap documentation | Canonical | dokumentacja | 2–3 h | 0 zł | https://snapcraft.io/docs |
| Tauri: Debian, RPM, AppImage, Flathub, Snapcraft, AUR, Linux Code Signing | Tauri | dokumentacja | 2–3 h | 0 zł | https://v2.tauri.app/distribute/ |
| `cargo-deb`, `cargo-generate-rpm` (pakiety dla aplikacji bez Tauri) | Kornel Lesiński; cat-in-136 | dokumentacja narzędzi | 1–2 h | 0 zł | https://docs.rs/cargo-deb, https://github.com/cat-in-136/cargo-generate-rpm |

Szczególnie ważne: budowanie na najstarszym wspieranym systemie, który ma jeszcze WebKitGTK 4.1 (Tauri podaje Ubuntu 22.04 i Debian 12), bo nowsza glibc zawęża krąg odbiorców; podpis pakietów i repozytoriów (GPG dla `.rpm` i plików `Release`), a podpis AppImage nie jest sprawdzany automatycznie; Flathub wymaga sandboxa z minimalnymi uprawnieniami i portali, nie przyjmuje aplikacji uruchamianych tylko z zasobnika, zabrania treści generowanych przez AI w manifestach, a płatne aplikacje podlegają osobnym zasadom monetyzacji; w Flatpaku aktualizacje dostarcza Flathub, więc w tej wersji aplikacji własny updater powinien być wyłączony. Klucze GPG w CI: zob. sekcja 9.

**Dowód:** narzędzie z sekcji 14.1 wydane jako `.deb`, `.rpm`, AppImage i Flatpak, zbudowane w CI na obrazie bazowym najstarszej wspieranej dystrybucji; własne repozytorium APT i RPM z podpisanym indeksem, instrukcją z `Signed-By` i działającą aktualizacją przez `apt upgrade` i `dnf upgrade`; manifest Flatpak przechodzący `flatpak-builder-lint`, z dostępem do repozytoriów tylko przez portal File Chooser.

#### Etap 3: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Komunikaty bezpieczeństwa WebKitGTK i informacje o wydaniach dystrybucji (Debian, Ubuntu, Fedora) | WebKitGTK, dystrybucje | źródła pierwotne | ok. 30 min tygodniowo | 0 zł | https://webkitgtk.org/security.html |
| Open Build Service: budowanie pakietów dla wielu dystrybucji | openSUSE | dokumentacja (opcjonalnie) | 4–6 h | 0 zł | https://openbuildservice.org/help/manuals/obs-user-guide/ |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 10 pull requestów agentów dotyczących pakowania i integracji z Linuksem, recenzowanych pod kątem: twardych ścieżek zamiast XDG, zależności dopisanych „na zapas” do pakietu, skryptów `postinst` z `sudo` lub `curl | sh`, nadmiarowych uprawnień Flatpak (`--filesystem=home`, `--talk-name` bez potrzeby), kluczy repozytorium dodawanych do globalnego zaufania zamiast `Signed-By`,
- **macierz zgodności:** czyste maszyny wirtualne z najstarszą i najnowszą wersją Ubuntu LTS, Debiana i Fedory, test instalacji, aktualizacji i odinstalowania każdego formatu,
- **rotacja klucza repozytorium:** przećwiczona wymiana klucza GPG bez utraty aktualizacji u istniejących użytkowników.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz błąd zgłoszony przez użytkownika jednej dystrybucji (np. brakująca biblioteka, zbyt nowa glibc, problem z Wayland lub portalem), wydajesz poprawione pakiety we wszystkich kanałach i umiesz wyjaśnić przyczynę osobie nietechnicznej.

---

## 16. macOS

*Warstwa 5: desktop. Opiera się na: 9 i 14.*

- Uniwersalne binarki (aarch64 i x86_64), struktura pakietu `.app`, DMG.
- Podpis kodu, hardened runtime, entitlements, notaryzacja (`notarytool`), staple.
- Mac App Store: sandbox, zakupy w aplikacji, recenzja.
- Integracje systemowe: menu, pasek menu, uprawnienia prywatności (TCC), Keychain.

### 16.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 4 etapy. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Wszystkie dowody dotyczą tej samej aplikacji z sekcji 14.1: narzędzia desktopowego do kontroli sekretów, licencji i zależności w repozytoriach, sprzedawanego poza sklepem przez Merchant of Record (podpis Developer ID i notaryzacja) oraz w Mac App Store. Przy codziennej pracy na Macu etap 0 można przejść szybciej, ale etapu 1 nie warto skracać: podpis, entitlements i notaryzacja to miejsce, w którym agent najczęściej „naprawia” błąd przez wyłączenie zabezpieczenia. Czas podany dla osoby startującej od zera; członkostwo w Apple Developer Program jest płatne (abonament roczny), a bez niego nie da się notaryzować aplikacji.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | budowa aplikacji na macOS: pakiet `.app`, uniwersalne binarki, integracje systemowe | 20–25 h | podstawy |
| 1 | podpis kodu, hardened runtime, entitlements, notaryzacja i dystrybucja poza sklepem | 25–30 h | W |
| 2 | Mac App Store: App Sandbox, recenzja, osobny wariant aplikacji | 15–20 h | W |
| 3 | ekspert: Gatekeeper i mechanizmy ochrony systemu, recenzja kodu AI | stale, ok. 1 h tygodniowo | E |

Razem od zera do poziomu E: ok. 60–75 h, czyli ok. 2 miesiące przy 8–10 h tygodniowo.

#### Etap 0: budowa aplikacji na macOS

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Placing content in a bundle (struktura `.app`, `Info.plist`, zasoby) | Apple | dokumentacja | 2–3 h | 0 zł | https://developer.apple.com/documentation/bundleresources/placing-content-in-a-bundle |
| Building a universal macOS binary (`lipo`, `arm64` i `x86_64`) | Apple | dokumentacja | 1–2 h | 0 zł | https://developer.apple.com/documentation/apple-silicon/building-a-universal-macos-binary |
| Tauri: macOS Application Bundle, DMG | Tauri | dokumentacja | 2–3 h | 0 zł | https://v2.tauri.app/distribute/macos-application-bundle/, https://v2.tauri.app/distribute/dmg/ |
| Keychain services | Apple | dokumentacja | 2–3 h | 0 zł | https://developer.apple.com/documentation/security/keychain-services |
| SMAppService (elementy logowania i usługi w tle) | Apple | dokumentacja | 1–2 h | 0 zł | https://developer.apple.com/documentation/servicemanagement/smappservice |
| AppKit i crate’y `objc2`, `objc2-app-kit` (wywołania API systemu z Rusta, gdy plugin nie wystarcza) | Apple; Mads Marquart i współautorzy | dokumentacja | 6–8 h | 0 zł | https://developer.apple.com/documentation/appkit, https://docs.rs/objc2 |

Szczególnie ważne: target `universal-apple-darwin` w Tauri albo łączenie dwóch binarek przez `lipo`; `minimumSystemVersion` zgodne z użytymi API; opisy użycia w `Info.plist` dla każdego zasobu chronionego przez TCC (dostęp do folderów, automatyzacja); aplikacje graficzne nie dziedziczą `$PATH` z powłoki, więc wywołanie `git` z aplikacji wymaga jawnej ścieżki. Wytyczne Apple Human Interface Guidelines: zob. sekcja 13.

**Dowód:** narzędzie z sekcji 14.1 jako uniwersalna binarka w DMG, z menu aplikacji zgodnym z konwencjami macOS, ikoną w pasku menu pokazującą wynik ostatniego skanu, tokenami w Keychain i opcjonalnym uruchamianiem przy logowaniu przez `SMAppService`; `lipo -info` potwierdza obie architektury.

#### Etap 1: podpis, notaryzacja i dystrybucja poza sklepem

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Signing Mac Software with Developer ID | Apple | przewodnik | 1 h | 0 zł | https://developer.apple.com/developer-id/ |
| Creating distribution-signed code for macOS | Apple | dokumentacja | 2–3 h | 0 zł | https://developer.apple.com/documentation/xcode/creating-distribution-signed-code-for-the-mac |
| Hardened Runtime | Apple | dokumentacja | 1–2 h | 0 zł | https://developer.apple.com/documentation/security/hardened-runtime |
| Notarizing macOS software before distribution, Customizing the notarization workflow, Resolving common notarization issues | Apple | dokumentacja | 3–4 h | 0 zł | https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution |
| Packaging Mac software for distribution (ZIP, DMG, PKG) | Apple | dokumentacja | 1–2 h | 0 zł | https://developer.apple.com/documentation/xcode/packaging-mac-software-for-distribution |
| TN3125, TN3126, TN3127: Inside Code Signing (profile, skróty, wymagania) | Apple | noty techniczne, zaawansowany | 4–5 h | 0 zł | https://developer.apple.com/documentation/technotes/tn3127-inside-code-signing-requirements |
| Code Signing: strona wsparcia z odnośnikami do przewodników i wątków forum | Apple | zbiór materiałów | 1–2 h | 0 zł | https://developer.apple.com/support/code-signing/ |
| „Resolving Trusted Execution Problems” | Quinn „The Eskimo!”, Apple Developer Technical Support | wątek forum, zaawansowany | 2–3 h | 0 zł | https://developer.apple.com/forums/thread/706442 |
| Tauri: macOS Code Signing (Developer ID, klucz API App Store Connect, zmienne dla CI) | Tauri | dokumentacja | 1–2 h | 0 zł | https://v2.tauri.app/distribute/sign/macos/ |
| Sparkle: dokumentacja (podpis EdDSA aktualizacji; dla aplikacji natywnych bez Tauri) | projekt Sparkle | dokumentacja | 2 h | 0 zł | https://sparkle-project.github.io/documentation/ |
| Apple Code Signing (`rcodesign`: podpis i notaryzacja z Linuksa) | Gregory Szorc | dokumentacja narzędzia (opcjonalnie) | 1–2 h | 0 zł | https://gregoryszorc.com/docs/apple-codesign/stable/ |

Szczególnie ważne: certyfikat Developer ID Application dla dystrybucji poza sklepem, Apple Distribution dla sklepu; hardened runtime jest warunkiem notaryzacji; `altool` nie jest już przyjmowany do notaryzacji, obowiązuje `notarytool`; staple biletu do DMG, żeby pierwsze uruchomienie działało offline; designated requirement musi być stały między wersjami, inaczej użytkownik traci dostęp do Keychain i zgody TCC po aktualizacji; każdy entitlement typu `com.apple.security.cs.disable-library-validation` lub `allow-unsigned-executable-memory` wymaga uzasadnienia. Certyfikaty i klucze w CI: zob. sekcja 9.

**Dowód:** DMG z aplikacją podpisaną Developer ID, z hardened runtime i minimalnym zestawem entitlements, notaryzowaną przez `notarytool` z kluczem API App Store Connect i ze zszytym biletem; na czystym Macu bez sieci aplikacja otwiera się bez ostrzeżenia Gatekeepera; `codesign --verify --deep --strict` i `spctl --assess` przechodzą; aktualizacja z N do N+1 zachowuje wpisy w Keychain i zgody prywatności.

#### Etap 2: Mac App Store

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| App Sandbox, Configuring the macOS App Sandbox | Apple | dokumentacja | 3–4 h | 0 zł | https://developer.apple.com/documentation/security/app-sandbox |
| App Review Guidelines (zwłaszcza 2.4.5 o aplikacjach na Maca, 3.1 o płatnościach, 5.1 o prywatności) | Apple | zasady | 3–4 h | 0 zł | https://developer.apple.com/app-store/review/guidelines/ |
| Tauri: App Store (entitlements sandboxa, profil provisioningu, paczka `.pkg`, wysyłka) | Tauri | dokumentacja | 2–3 h | 0 zł | https://v2.tauri.app/distribute/app-store/ |

Szczególnie ważne: aplikacja z Mac App Store musi działać w sandboxie i aktualizować się wyłącznie przez sklep, więc wariant sklepowy nie ma własnego updatera ani zewnętrznej licencji kupowanej poza sklepem bez zgodności z zasadami płatności; dostęp do repozytoriów tylko do folderów wskazanych przez użytkownika, z zakładkami bezpieczeństwa (security-scoped bookmarks) zapamiętującymi dostęp między uruchomieniami; wywoływanie zewnętrznych narzędzi (np. `git`) z sandboxa jest ograniczone. StoreKit i rozliczenia: zob. sekcja 19.

**Dowód:** osobny wariant budowania (flaga Cargo i osobny plik konfiguracji) bez updatera, z sandboxem, dostępem do repozytorium wybranego okienkiem systemowym i zapamiętanym przez zakładkę bezpieczeństwa; wariant przechodzi walidację w App Store Connect i trafia do testów w TestFlight; lista różnic między wariantem sklepowym a wariantem Developer ID w dokumentacji wydania.

#### Etap 3: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Apple Platform Security | Apple | przewodnik, zaawansowany | 8–10 h | 0 zł | https://support.apple.com/guide/security/welcome/web |
| The Art of Mac Malware, tom I i II | Patrick Wardle (Objective-See Foundation) | książki, zaawansowany | 15–20 h | 0 zł online, druk płatny | https://taomm.org |
| The Eclectic Light Company (Gatekeeper, XProtect, podpisy, zmiany w kolejnych wersjach macOS) | Howard Oakley | blog | ok. 30 min tygodniowo | 0 zł | https://eclecticlight.co |
| Informacje o wydaniach Xcode i macOS, forum Apple Developer (tagi Code Signing, Notarization) | Apple | źródła pierwotne | ok. 30 min tygodniowo | 0 zł | https://developer.apple.com/forums/tags/code-signing |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 10 pull requestów agentów dotyczących budowania, podpisu i integracji z macOS, recenzowanych pod kątem: dopisanych entitlements wyłączających ochrony hardened runtime, `--deep` jako sposobu na błędy podpisu zagnieżdżonego kodu, usuwania atrybutu kwarantanny w instrukcjach dla użytkownika, sekretów w `UserDefaults` lub plikach zamiast w Keychain, nieuzasadnionych próśb o pełny dostęp do dysku,
- **macierz wersji:** najstarsza wspierana i najnowsza wersja macOS na Apple Silicon i Intelu, test pierwszego uruchomienia z kwarantanną, aktualizacji i odinstalowania,
- **ćwiczenie wygaśnięcia lub unieważnienia certyfikatu:** plan, co dzieje się z wydanymi wersjami i jak wydać kolejną bez przerwy w aktualizacjach.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz odrzuconą notaryzację albo problem z uruchomieniem zgłoszony przez użytkownika (log notaryzacji, `codesign`, `spctl`, logi systemowe), wydajesz poprawioną wersję i umiesz wyjaśnić przyczynę osobie nietechnicznej.

---

## 17. Windows

*Warstwa 5: desktop. Opiera się na: 9 i 14.*

- Toolchain MSVC, `windows-rs`, WebView2 (dystrybucja i wersje).
- Instalatory: MSI (WiX), NSIS, MSIX; podpis Authenticode certyfikatem lub usługą podpisu w chmurze Microsoftu, reputacja SmartScreen.
- Microsoft Store: pakiety MSIX, płatności Microsoft lub własne.
- Specyfika systemu: rejestr, uprawnienia UAC, ścieżki, pułapka DLL hijacking, Defender i fałszywe alarmy antywirusów.

### 17.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 4 etapy. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Wszystkie dowody dotyczą tej samej aplikacji z sekcji 14.1: narzędzia desktopowego do kontroli sekretów, licencji i zależności w repozytoriach, sprzedawanego poza sklepem przez Merchant of Record i w Microsoft Store. Przy doświadczeniu z Windows etap 0 można zaliczyć samym dowodem, ale etapu 2 nie warto skracać: podpis, reputacja SmartScreen i fałszywe alarmy antywirusów decydują o tym, czy klient w ogóle uruchomi aplikację. Czas podany dla osoby startującej od zera; ceny materiałów płatnych i certyfikatów zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | Windows od strony aplikacji: toolchain MSVC, `windows-rs`, WebView2 | 25–30 h | podstawy |
| 1 | instalatory: MSI (WiX), NSIS, MSIX | 20–25 h | W |
| 2 | podpis Authenticode, SmartScreen, Defender, Microsoft Store | 15–20 h | W |
| 3 | ekspert: mechanizmy systemu, diagnoza, recenzja kodu AI | stale, ok. 1 h tygodniowo | E |

Razem od zera do poziomu E: ok. 60–75 h, czyli ok. 2 miesiące przy 8–10 h tygodniowo.

#### Etap 0: Windows od strony aplikacji

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Overview of developing on Windows with Rust, Set up your Rust development environment, Rust for Windows and the windows crate | Microsoft | dokumentacja | 3–4 h | 0 zł | https://learn.microsoft.com/en-us/windows/dev-environment/rust/ |
| Crate’y `windows` i `windows-sys` | Microsoft (Kenny Kerr i współautorzy) | dokumentacja | 3–4 h | 0 zł | https://docs.rs/windows, https://github.com/microsoft/windows-rs |
| Introduction to Microsoft Edge WebView2, Distribute your app and the WebView2 Runtime (Evergreen i Fixed Version) | Microsoft | dokumentacja | 3–4 h | 0 zł | https://learn.microsoft.com/en-us/microsoft-edge/webview2/, https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution |
| Windows 10 System Programming, Part 1 (procesy, wątki, pamięć, bezpieczeństwo) | Pavel Yosifovich | książka, średni–zaawansowany | 12–15 h | płatna | https://leanpub.com/windows10systemprogramming |
| CryptProtectData (DPAPI), CredWriteW (Credential Manager) | Microsoft | dokumentacja API | 1–2 h | 0 zł | https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata |

Szczególnie ważne: target `x86_64-pc-windows-msvc` i `aarch64-pc-windows-msvc` (Windows na ARM), Visual Studio Build Tools; Smart App Control w trybie wymuszania potrafi zablokować niepodpisane narzędzia, także toolchain Rusta; WebView2 w trybie Evergreen aktualizuje się sam, ale aplikacja musi sprawdzić, czy runtime jest zainstalowany; ścieżki z ukośnikiem wstecznym, limit długości ścieżki, wielkość liter, `%APPDATA%` i `%LOCALAPPDATA%` zamiast katalogu programu. Wytyczne Fluent: zob. sekcja 13.

**Dowód:** narzędzie z sekcji 14.1 zbudowane na Windows x64 i ARM64, z tokenami w Credential Manager, danymi w `%LOCALAPPDATA%`, wykrywaniem braku WebView2 z czytelnym komunikatem i jednym wywołaniem API systemu przez `windows-rs` (np. powiadomienie systemowe albo odczyt ustawienia rejestru) z obsługą błędów zamiast `unwrap()`.

#### Etap 1: instalatory

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Windows Installer (model MSI: komponenty, akcje, aktualizacje, kontekst na użytkownika i na maszynę) | Microsoft | dokumentacja | 4–5 h | 0 zł | https://learn.microsoft.com/en-us/windows/win32/msi/windows-installer-portal |
| WiX Toolset: dokumentacja (wersja 7 z kwietnia 2026 r.; wersja 3 nie jest już wspierana) | FireGiant, społeczność WiX | dokumentacja | 4–6 h | 0 zł; firmy z przychodem od 10 tys. USD rocznie objęte opłatą Open Source Maintenance Fee | https://docs.firegiant.com/wix/ |
| NSIS: dokumentacja | projekt NSIS | dokumentacja | 2–3 h | 0 zł | https://nsis.sourceforge.io/Docs/ |
| MSIX: dokumentacja (What is MSIX, kontenery, App Installer, Packaging Tool) | Microsoft | dokumentacja | 4–5 h | 0 zł | https://learn.microsoft.com/en-us/windows/msix/ |
| Package and deploy Windows apps (wybór modelu pakowania i ścieżki dystrybucji) | Microsoft | przewodnik | 1–2 h | 0 zł | https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/ |
| Tauri: Windows Installer (WiX, NSIS, tryby instalacji WebView2, kompilacja skrośna NSIS z Linuksa) | Tauri | dokumentacja | 2 h | 0 zł | https://v2.tauri.app/distribute/windows-installer/ |

Szczególnie ważne: Tauri buduje MSI na WiX v3, który FireGiant oznacza jako przestarzały, a MSI powstaje tylko na Windows, więc w CI potrzebny jest runner Windows; Tauri nie generuje MSIX; wybór trybu WebView2 (`downloadBootstrapper`, `offlineInstaller`, `fixedVersion`) to kompromis rozmiaru, pracy offline i odpowiedzialności za łatki silnika; instalacja na użytkownika bez uprawnień administratora jest zwykle lepsza dla narzędzia deweloperskiego; poprawne odinstalowanie i stały `UpgradeCode` w MSI.

**Dowód:** narzędzie wydane jako instalator NSIS (na użytkownika) i MSI (na maszynę, do wdrożeń firmowych), oba z cichą instalacją (`/S`, `/quiet`), wpisem w „Aplikacje i funkcje” z poprawnym wydawcą i wersją, czystym odinstalowaniem bez pozostałości oraz aktualizacją z N do N+1 przez updater z sekcji 14.1; test na czystej maszynie wirtualnej Windows 10 i 11.

#### Etap 2: podpis, reputacja i Microsoft Store

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Code signing options for Windows app developers | Microsoft | przewodnik | 1–2 h | 0 zł | https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/code-signing-options |
| SmartScreen reputation for Windows app developers | Microsoft | przewodnik | 1 h | 0 zł | https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation |
| Artifact Signing (dawniej Trusted Signing): przegląd, quickstart, FAQ, modele zaufania | Microsoft | dokumentacja | 3–4 h | usługa płatna (abonament) | https://learn.microsoft.com/en-us/azure/artifact-signing/ |
| Smart App Control overview | Microsoft | dokumentacja | 1 h | 0 zł | https://learn.microsoft.com/en-us/windows/apps/develop/smart-app-control/overview |
| Tauri: Windows Code Signing (certyfikat OV, Azure Key Vault, Artifact Signing, własne `signCommand`) | Tauri | dokumentacja | 1–2 h | 0 zł | https://v2.tauri.app/distribute/sign/windows/ |
| Publish apps and games to Microsoft Store, proces certyfikacji aplikacji MSI/EXE, Microsoft Store Policies (wersja 7.20) | Microsoft | dokumentacja i zasady | 4–5 h | 0 zł; konto indywidualne bezpłatne | https://learn.microsoft.com/en-us/windows/apps/publish/, https://learn.microsoft.com/en-us/windows/apps/publish/store-policies |
| Tauri: Microsoft Store (zgłoszenie EXE/MSI, instalator offline, wydawca) | Tauri | dokumentacja | 1 h | 0 zł | https://v2.tauri.app/distribute/microsoft-store/ |
| Submit a file for malware analysis (zgłaszanie fałszywych alarmów Defendera jako „Software developer”) | Microsoft Security Intelligence | formularz i instrukcja | 0,5 h | 0 zł | https://www.microsoft.com/en-us/wdsi/filesubmission |

Szczególnie ważne: Artifact Signing dla osób fizycznych działa tylko w USA i Kanadzie, a organizacje z UE muszą przejść walidację jako podmiot prawny, więc dla JDG trzeba sprawdzić, czy przejdzie walidację jako organizacja, a w razie odmowy kupić certyfikat OV z kluczem na HSM lub tokenie; certyfikat EV od 2024 r. nie omija już SmartScreen, a reputację buduje się stałą tożsamością podpisu między wydaniami; podpisane muszą być instalator i wszystkie pliki PE w środku, z ważnym znacznikiem czasu; Microsoft Store przyjmuje MSI i EXE z wersjonowanego adresu HTTPS, z cichą instalacją i bez pobierania plików podczas instalacji, a aplikacje niebędące grami mogą używać własnego systemu płatności. Klucze i podpis w CI: zob. sekcja 9.

**Dowód:** instalatory z etapu 1 podpisane (Artifact Signing albo certyfikat OV) ze znacznikiem czasu, sprawdzone przez `signtool verify /pa /all`; na czystej maszynie z włączonym SmartScreen i Defenderem instalacja przebiega bez blokady albo z udokumentowanym ostrzeżeniem i planem budowy reputacji; zgłoszenie aplikacji do Microsoft Store przechodzi certyfikację; procedura zgłaszania fałszywego alarmu antywirusa opisana w dokumentacji wydania.

#### Etap 3: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Windows Internals, 7th Edition, Part 1 i Part 2 | Pavel Yosifovich, Alex Ionescu, Mark Russinovich, David Solomon; Andrea Allievi (Part 2); Microsoft Press | książki, zaawansowany, jako kompendium | 20–30 h (wybrane rozdziały) | płatna | https://learn.microsoft.com/en-us/sysinternals/resources/windows-internals |
| Sysinternals: Process Monitor, Process Explorer, Autoruns, Sigcheck | Microsoft (Mark Russinovich) | narzędzia i dokumentacja | 4–6 h | 0 zł | https://learn.microsoft.com/en-us/sysinternals/ |
| Dynamic-Link Library Security (DLL preloading i kolejność wyszukiwania) | Microsoft | dokumentacja | 1–2 h | 0 zł | https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-security |
| User Account Control | Microsoft | dokumentacja | 1 h | 0 zł | https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/ |
| The Old New Thing | Raymond Chen, Microsoft | blog | ok. 30 min tygodniowo | 0 zł | https://devblogs.microsoft.com/oldnewthing/ |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 10 pull requestów agentów dotyczących budowania, instalatora i integracji z Windows, recenzowanych pod kątem: `LoadLibrary` bez pełnej ścieżki, żądania uprawnień administratora bez potrzeby (manifest `requireAdministrator`), zapisu do `Program Files` w czasie działania, sekretów w rejestrze lub plikach zamiast w Credential Manager albo DPAPI, `unsafe` przy wywołaniach Win32 bez sprawdzenia kodów błędów, wyłączenia sprawdzania WebView2,
- **diagnoza Process Monitorem:** sprawdzenie, czy aplikacja i instalator nie ładują DLL z katalogu bieżącego lub katalogu pobierania,
- **macierz wersji:** Windows 10 i 11, x64 i ARM64, konto standardowe i administrator, z WebView2 i bez niego.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz problem zgłoszony przez użytkownika Windows (np. blokada SmartScreen lub Defendera, nieudana aktualizacja przez MSI, brak WebView2, błąd uprawnień), wydajesz podpisaną poprawkę i umiesz wyjaśnić przyczynę osobie nietechnicznej.

### 17.2 Ścieżka uzupełniająca: PowerShell

PowerShell jest potrzebny do skryptów budowania i podpisywania na runnerach Windows. Wystarczy go opanować przed pierwszym wydaniem na Windows; ok. 15–20 h od zera, poziom W.

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| PowerShell 101 | Mike F. Robbins, Microsoft Learn | książka online, od podstaw | 5–6 h | 0 zł | https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/00-introduction |
| Learn PowerShell in a Month of Lunches (wydanie 4) | Travis Plunk, James Petty, Tyler Leonhardt, Jeffery Hicks, Manning | książka, od podstaw do średniego | 10–15 h | płatna | https://www.manning.com/books/learn-powershell-in-a-month-of-lunches |
| PSScriptAnalyzer | Microsoft | linter, dokumentacja | 1–2 h | 0 zł | https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview |
| Pester | społeczność Pester | framework testów | 2–3 h | 0 zł | https://pester.dev |

Książka Manninga jest opcjonalna; do poziomu W zwykle wystarcza PowerShell 101 i praca na skryptach budowania. Szczególnie ważne: potok obiektów zamiast tekstu, `$ErrorActionPreference = 'Stop'` i `try`/`catch`, polityka wykonywania skryptów, różnice Windows PowerShell 5.1 i PowerShell 7. Podpisywanie i instalatory: zob. sekcja 17.

**Dowód:** skrypt PowerShell 7 na runnerze Windows w GitHub Actions, który buduje instalator, podpisuje go i weryfikuje podpis, kończy się błędem przy każdym niepowodzeniu kroku i przechodzi PSScriptAnalyzer oraz testy w Pester.

---

## 18. Android

*Warstwa 6: mobile. Opiera się na: 9, 12, 13 i 14 (rdzeń w Ruście). Jest podstawą: 21.*

- Kotlin, Jetpack Compose, cykl życia aktywności i procesów, WorkManager, uprawnienia.
- Gradle, Android SDK i NDK, targety ABI, budowanie biblioteki Rust (`cargo-ndk`) i wiązania UniFFI.
- Alternatywnie Tauri 2 na Androidzie: ograniczenia webview i pluginy natywne.
- Android App Bundle, podpisywanie (Play App Signing), Play Console, ścieżki testowe, wymagania docelowego poziomu API.
- Google Play Billing (abonamenty, zakup jednorazowy), polityki sklepu, sekcja bezpieczeństwa danych.
- Bezpieczne przechowywanie: Android Keystore i szyfrowane magazyny danych.

### 18.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 7 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przy doświadczeniu seniorskim w TypeScript, React i Rust etap 0 można zaliczyć samym dowodem (Kotlin jest bliski obu językom), a w etapie 1 wystarczą jednostki 4–7 kursu, bo model Compose odpowiada Reactowi. Etapy 4 i 5 są obowiązkowe w całości: to w nich powstaje rdzeń Rust na Androidzie i przychód. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | Kotlin i korutyny | 40–60 h | podstawy |
| 1 | pierwsze aplikacje: Android i Jetpack Compose | 80–100 h | podstawy |
| 2 | Compose w głębi i architektura aplikacji | 50–60 h | W |
| 3 | platforma: procesy, praca w tle, uprawnienia, dane, Keystore | 40–50 h | W |
| 4 | rdzeń Rust: UniFFI, `cargo-ndk`, alternatywnie Tauri 2 | 30–40 h | E |
| 5 | publikacja i monetyzacja w Google Play | 30–40 h | E |
| 6 | ekspert: wydajność, mechanizmy wewnętrzne, recenzja kodu AI, aktualność | stale, ok. 2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 270–350 h, czyli 6–8 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: Kotlin

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Kotlin tour i dokumentacja języka | JetBrains | samouczek interaktywny i dokumentacja | 10–15 h | 0 zł | https://kotlinlang.org/docs/kotlin-tour-welcome.html, https://kotlinlang.org/docs/home.html |
| Kotlin Koans | JetBrains | ćwiczenia w przeglądarce lub IDE | 6–8 h | 0 zł | https://play.kotlinlang.org/koans |
| Kotlin in Action (wydanie 2, 2024) | Sebastian Aigner, Roman Elizarov, Svetlana Isakova, Dmitry Jemerov, Manning | książka, od podstaw do zaawansowanego | 20–25 h | płatna | https://www.manning.com/books/kotlin-in-action-second-edition |
| Coroutines guide | JetBrains | dokumentacja | 6–8 h | 0 zł | https://kotlinlang.org/docs/coroutines-guide.html |

Szczególnie ważne: null safety, klasy `data` i `sealed`, funkcje rozszerzające, lambdy z odbiorcą, korutyny strukturalne, anulowanie, `Flow` i `StateFlow`, różnice wobec `async`/`await` w TypeScript i Tokio w Ruście.

**Dowód:** narzędzie konsolowe w Kotlinie pobierające dane z publicznego API przez korutyny, z anulowaniem po przekroczeniu czasu, wynikami jako `sealed` hierarchią i testami jednostkowymi.

#### Etap 1: Android i Jetpack Compose

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Android Basics with Compose (8 jednostek: UI, listy, nawigacja, architektura, sieć, Room, WorkManager, interoperacyjność z View) | Google | kurs, od podstaw | 80–100 h | 0 zł | https://developer.android.com/courses/android-basics-compose/course |
| Dokumentacja Jetpack Compose: „Thinking in Compose”, stan, efekty uboczne, Material 3 | Google | dokumentacja | 6–8 h | 0 zł | https://developer.android.com/develop/ui/compose/documentation |

Szczególnie ważne: rekompozycja i `remember`, wynoszenie stanu (state hoisting), `ViewModel`, nawigacja, różnice między efektami w Compose a `useEffect` w React.

**Dowód:** aplikacja offline-first z listą, edycją i wyszukiwaniem (np. notatki lub nawyki), z danymi w Room, odświeżaniem z sieci i obsługą obrotu ekranu bez utraty stanu.

#### Etap 2: Compose w głębi i architektura

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Guide to app architecture: warstwy UI i danych, jedno źródło prawdy, przepływ jednokierunkowy | Google | dokumentacja | 6–8 h | 0 zł | https://developer.android.com/topic/architecture |
| Now in Android (z dokumentami „Architecture Learning Journey” i „Modularization Learning Journey”) | Google | przykładowa aplikacja referencyjna | 10–15 h | 0 zł | https://github.com/android/nowinandroid |
| Best practices for coroutines in Android | Google | dokumentacja | 2–3 h | 0 zł | https://developer.android.com/kotlin/coroutines/coroutines-best-practices |
| Jetpack Compose for Android Developers (5 ścieżek; materiały z 2022 r., API sprawdzać w dokumentacji) | Google | kurs, średni | 15–20 h | 0 zł | https://developer.android.com/courses/jetpack-compose/course |
| Kotlin Coroutines: Deep Dive | Marcin Moskała, Kt. Academy | książka, zaawansowany | 12–15 h | płatna | https://leanpub.com/coroutines |
| Effective Kotlin | Marcin Moskała, Kt. Academy | książka, średni–zaawansowany | 10–12 h | płatna | https://kt.academy/book/effectivekotlin |

Szczególnie ważne: wstrzykiwanie dispatcherów i zakresów, niemutowalny stan UI, układy adaptacyjne (telefon, tablet, składane), modularyzacja Gradle, katalog wersji i Compose BOM.

**Dowód:** aplikacja z etapu 1 przebudowana na warstwy (UI, dane, opcjonalnie domena) i moduły Gradle, z `StateFlow` jako jedynym źródłem stanu ekranu, układem list–szczegóły na tablecie i testami `ViewModel` z `runTest` (zob. sekcja 6).

#### Etap 3: platforma Android

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Processes and app lifecycle | Google | dokumentacja | 2–3 h | 0 zł | https://developer.android.com/guide/components/activities/process-lifecycle |
| WorkManager: trwała praca w tle | Google | dokumentacja | 4–6 h | 0 zł | https://developer.android.com/develop/background-work/background-tasks/persistent |
| Request runtime permissions | Google | dokumentacja | 2–3 h | 0 zł | https://developer.android.com/training/permissions/requesting |
| Room (od wersji 3.0 pakiet `androidx.room3`, wymaga KSP) | Google | dokumentacja | 4–6 h | 0 zł | https://developer.android.com/training/data-storage/room |
| Android Keystore system | Google | dokumentacja | 3–4 h | 0 zł | https://developer.android.com/privacy-and-security/keystore |

Szczególnie ważne: system może zabić proces w każdej chwili, `onDestroy()` nie jest gwarantowane, ograniczenia pracy w tle i trybu Doze, jednorazowe i automatycznie cofane uprawnienia, klucze sprzętowe (TEE, StrongBox) i uwierzytelnianie biometryczne. Testy bezpieczeństwa według MASVS: zob. sekcja 10.

**Dowód:** synchronizacja danych aplikacji przez `CoroutineWorker` z ograniczeniami sieci i baterii, przeżywająca ubicie procesu i restart urządzenia; token sesji zaszyfrowany kluczem z Android Keystore; funkcja wymagająca uprawnienia działa w trybie ograniczonym po odmowie.

#### Etap 4: rdzeń Rust na Androidzie

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The UniFFI user guide: model typów, proc-macros, async, interfejsy zwrotne, rozdziały Kotlin i „Integrating with Gradle” | Mozilla | dokumentacja | 8–10 h | 0 zł | https://mozilla.github.io/uniffi-rs/latest/ |
| `cargo-ndk` | Brendan Molloy i społeczność | narzędzie i README | 1–2 h | 0 zł | https://github.com/bbqsrc/cargo-ndk |
| JNI tips (wątki, `JNIEnv`, ładowanie bibliotek, `UnsatisfiedLinkError`) | Google | dokumentacja | 2–3 h | 0 zł | https://developer.android.com/ndk/guides/jni-tips |
| Support 16 KB page sizes | Google | dokumentacja | 1–2 h | 0 zł | https://developer.android.com/guide/practices/page-sizes |
| uniffi-starter (rdzeń Rust, Gradle z `cargo-ndk`, Swift Package) | Ian Wagner | szablon projektu | 3–4 h | 0 zł | https://github.com/ianthetechie/uniffi-starter |
| application-services (komponenty Firefoksa współdzielone przez UniFFI z Androidem i iOS) | Mozilla | kod referencyjny w produkcji | 3–5 h | 0 zł | https://github.com/mozilla/application-services |
| Tauri 2 na Androidzie: wymagania (SDK, NDK, targety `rustup`) i pluginy mobilne w Kotlinie | Tauri | dokumentacja (ścieżka alternatywna) | 6–8 h | 0 zł | https://v2.tauri.app/start/prerequisites/, https://v2.tauri.app/develop/plugins/develop-mobile/ |

Szczególnie ważne: granica FFI jako kontrakt (błędy Rust zamienione na wyjątki Kotlina, brak paniki przez granicę), wątki Rust wywołujące Kotlina, async po obu stronach, rozmiar `.so` na każde ABI, wyrównanie bibliotek do stron 16 KB (blokada aktualizacji w Google Play bez tego wsparcia od 1 lutego 2027 r.), wersjonowanie rdzenia wspólnego z iOS i desktopem. Opcjonalnie Gobley (https://gobley.dev) przy projekcie Kotlin Multiplatform.

**Dowód:** ten sam crate z rdzeniem (model danych, walidacja, logika licencji i synchronizacji) używany przez aplikację z etapu 3 przez wiązania UniFFI, budowany w Gradle dla `arm64-v8a` i `x86_64`; błąd z Rusta obsłużony w UI jako wyjątek Kotlina; biblioteka `.so` zweryfikowana pod kątem wyrównania 16 KB. Rdzeń wchodzi do SBOM aplikacji (zob. sekcja 10).

#### Etap 5: publikacja i monetyzacja w Google Play

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Play Console Help: konto dewelopera, ścieżki testów, wymóg testu zamkniętego (12 testerów przez 14 dni dla nowych kont osobistych) | Google | dokumentacja | 4–6 h | 0 zł | https://support.google.com/googleplay/android-developer/answer/14151465 |
| Android App Bundle, Play App Signing (klucz podpisu i klucz przesyłania) | Google | dokumentacja | 2–3 h | 0 zł | https://developer.android.com/guide/app-bundle, https://developer.android.com/studio/publish/app-signing |
| Wymagania docelowego API (od 31 sierpnia 2026 r. Android 16, API 36 dla nowych aplikacji i aktualizacji) | Google | dokumentacja | 1 h | 0 zł | https://developer.android.com/google/play/requirements/target-sdk |
| Google Play Billing: integracja, abonamenty, produkty jednorazowe, migracja do Billing Library 9 (wersja 8 lub nowsza wymagana od 31 sierpnia 2026 r.) | Google | dokumentacja | 8–10 h | 0 zł | https://developer.android.com/google/play/billing |
| Real-time developer notifications (RTDN) i weryfikacja zakupów na serwerze | Google | dokumentacja | 3–4 h | 0 zł | https://developer.android.com/google/play/billing/rtdn-reference |
| Play Integrity API | Google | dokumentacja | 2–3 h | 0 zł | https://developer.android.com/google/play/integrity |
| Polityki programu dla deweloperów, sekcja bezpieczeństwa danych, weryfikacja deweloperów Androida | Google | polityki | 4–6 h | 0 zł | https://play.google/developer-content-policy/, https://support.google.com/googleplay/android-developer/answer/10787469, https://developer.android.com/developer-verification |
| Google Play Academy | Google | kursy, podstawowy–średni | wg potrzeb | 0 zł | https://playacademy.withgoogle.com |
| Tauri 2: publikacja w Google Play (AAB, architektury) | Tauri | dokumentacja (ścieżka alternatywna) | 1–2 h | 0 zł | https://v2.tauri.app/distribute/google-play/ |

Szczególnie ważne: potwierdzenie zakupu w ciągu 3 dni (inaczej automatyczny zwrot), uprawnienia przyznawane dopiero po weryfikacji tokenu na serwerze, stany abonamentu (okres karencji, wstrzymanie, odzyskanie), zgodność ekranu zakupu z polityką i prawem konsumenckim (zob. sekcja 13), automatyzacja wydań przez API Google Play (zob. sekcja 9).

**Dowód:** aplikacja z rdzeniem Rust opublikowana w Google Play po teście zamkniętym, z abonamentem i zakupem jednorazowym; backend w Rust (Axum) weryfikuje tokeny, odbiera RTDN przez Pub/Sub i jest jedynym źródłem uprawnień; sekcja bezpieczeństwa danych zgodna z faktycznym przetwarzaniem; proces zgłaszania podatności zgodny z CRA opisany na stronie produktu.

#### Etap 6: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Jetpack Compose Performance, fazy Compose, stabilność | Google | dokumentacja | 4–6 h | 0 zł | https://developer.android.com/develop/ui/compose/performance |
| Baseline Profiles i Macrobenchmark | Google | dokumentacja | 6–8 h | 0 zł | https://developer.android.com/topic/performance/baselineprofiles/overview, https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview |
| Android vitals (progi złego zachowania: awarie, ANR, pamięć) | Google | dokumentacja | 2–3 h | 0 zł | https://developer.android.com/topic/performance/vitals |
| Jetpack Compose Internals (wydanie z 2022 r.) | Jorge Castillo | książka, zaawansowany | 10–12 h | płatna | https://leanpub.com/composeinternals |
| Android Developers Blog, Android Code Search | Google | źródła pierwotne | ok. 1 h tygodniowo | 0 zł | https://android-developers.googleblog.com, https://cs.android.com |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 20 pull requestów wygenerowanych przez agentów, recenzowanych według listy kontrolnej z etapów 2–5 (zbędne rekompozycje i niestabilne parametry, `GlobalScope` i zakodowane dispatchery, połknięte `CancellationException`, praca w tle bez WorkManagera, nadmiarowe uprawnienia, zakupy bez potwierdzenia i weryfikacji na serwerze, panika Rusta przez granicę FFI, wymyślone API Androida),
- **wydajność:** Baseline Profile i Macrobenchmark w CI dla uruchomienia i przewijania; awarie i ANR poniżej progów Android vitals,
- **śledzenie zmian platformy:** coroczna aktualizacja docelowego API, wersji Billing Library i wymogów weryfikacji deweloperów, przećwiczona przed terminem Google,
- **wkład w open source** w UniFFI, `cargo-ndk` lub bibliotece Jetpack, choćby w dokumentację lub testy.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz ANR, wyciek pamięci albo błąd zakupów w aplikacji z rdzeniem Rust, korzystając z Perfetto, profilera Android Studio i logów RTDN, i umiesz wyjaśnić przyczynę osobie nietechnicznej.

---

## 19. iOS

*Warstwa 6: mobile. Opiera się na: 9, 12, 13 i 14 (rdzeń w Ruście). Jest podstawą: 21.*

- Swift, SwiftUI, cykl życia aplikacji, zadania w tle, uprawnienia.
- Xcode, certyfikaty, profile provisioningu, XCFramework z biblioteką Rust i wiązaniami UniFFI.
- Alternatywnie Tauri 2 na iOS i jego ograniczenia.
- StoreKit 2, App Store Connect, TestFlight, zasady recenzji Apple, manifest prywatności, regulacje UE dla dystrybucji.
- Keychain, ochrona danych na urządzeniu, App Transport Security.

### 19.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 7 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przy doświadczeniu seniorskim w TypeScript, React i Rust etap 0 można zaliczyć samym dowodem (Swift ma wiele wspólnego z Rustem: enumy z danymi, protokoły podobne do cech, typy wartościowe), a etap 1 skrócić do „100 Days of SwiftUI” od dnia 16 albo wybranych wykładów CS193p. Etap 2 (współbieżność Swift 6) oraz etapy 4 i 5 są obowiązkowe w całości: tu najczęściej mylą się agenci i tu powstaje przychód. Do budowania na iOS potrzebny jest Mac z Xcode. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | język Swift | 40–60 h | podstawy |
| 1 | pierwsze aplikacje: SwiftUI i Xcode | 80–100 h | podstawy |
| 2 | współbieżność Swift 6 i architektura | 40–50 h | W |
| 3 | platforma: cykl życia, praca w tle, dane, Keychain, prywatność | 30–40 h | W |
| 4 | rdzeń Rust: UniFFI i XCFramework, alternatywnie Tauri 2 | 30–40 h | E |
| 5 | publikacja i monetyzacja w App Store | 30–40 h | E |
| 6 | ekspert: wydajność, mechanizmy wewnętrzne, recenzja kodu AI, aktualność | stale, ok. 2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 250–330 h, czyli 6–8 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: Swift

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Swift Programming Language (rozdziały do „Generics” włącznie) | swift.org (Apple i społeczność) | książka online | 20–25 h | 0 zł | https://docs.swift.org/swift-book/documentation/the-swift-programming-language/ |
| 100 Days of SwiftUI, dni 1–15 (podstawy języka) | Paul Hudson, Hacking with Swift | kurs wideo z testami | 15–20 h | 0 zł | https://www.hackingwithswift.com/100/swiftui |
| API Design Guidelines | swift.org | wytyczne | 1–2 h | 0 zł | https://www.swift.org/documentation/api-design-guidelines/ |

Szczególnie ważne: typy wartościowe i referencyjne (`struct` a `class`), opcjonalne, enumy z wartościami powiązanymi, protokoły i rozszerzenia, generyki, `some` i `any`, obsługa błędów (`throws`, typowane błędy), zarządzanie pamięcią przez ARC i cykle referencji.

**Dowód:** pakiet Swift Package Manager z modelem domeny aplikacji (np. abonamenty i limity), z błędami jako enumami i testami jednostkowymi uruchamianymi przez `swift test`.

#### Etap 1: SwiftUI i Xcode

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Develop in Swift Tutorials | Apple | samouczki, od podstaw | 10–15 h | 0 zł | https://developer.apple.com/tutorials/develop-in-swift |
| SwiftUI Tutorials („Introducing SwiftUI”) | Apple | samouczki | 6–8 h | 0 zł | https://developer.apple.com/tutorials/swiftui |
| 100 Days of SwiftUI, dni 16–100 (z rozwiązaniami wyzwań w płatnym abonamencie Hacking with Swift+) | Paul Hudson, Hacking with Swift | kurs projektowy | 60–80 h | 0 zł / abonament | https://www.hackingwithswift.com/100/swiftui |
| CS193p Developing Apps for iOS (edycja Spring 2025, 16 wykładów, SwiftUI i SwiftData) | Stanford University | wykłady uniwersyteckie | 30–40 h | 0 zł | https://cs193p.stanford.edu |

Wystarczy jedna ścieżka: 100 Days of SwiftUI przy starcie od zera, CS193p przy doświadczeniu z innym frameworkiem deklaratywnym. Materiały CS193p powstały przed Xcode 26; kod jest w większości zgodny.

Szczególnie ważne: przepływ danych (`@State`, `@Binding`, `@Observable`, `@Environment`), tożsamość widoków i ich odświeżanie, nawigacja (`NavigationStack`), listy i formularze, SwiftData, podgląd w Xcode, różnice wobec modelu Reacta.

**Dowód:** aplikacja z listą, edycją, wyszukiwaniem i trwałym zapisem w SwiftData, poprawna na iPhonie i iPadzie, w trybie ciemnym i z Dynamic Type.

#### Etap 2: współbieżność Swift 6 i architektura

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Swift Programming Language: rozdział „Concurrency” | swift.org | dokumentacja | 3–4 h | 0 zł | https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/ |
| Swift Concurrency Migration Guide (tryb języka Swift 6, bezpieczeństwo wyścigów danych) | swift.org | przewodnik | 6–8 h | 0 zł | https://www.swift.org/migration/documentation/migrationguide/ |
| Swift 6.2 Released (Approachable Concurrency, izolacja domyślna do `MainActor`, `@concurrent`) | swift.org | artykuł | 1 h | 0 zł | https://swift.org/blog/swift-6.2-released/ |
| „Embracing Swift concurrency” (WWDC25, sesja 268) | Apple | wykład | 1 h | 0 zł | https://developer.apple.com/videos/play/wwdc2025/268/ |
| Swift Concurrency by Example | Paul Hudson, Hacking with Swift | książka online | 8–10 h | 0 zł | https://www.hackingwithswift.com/quick-start/concurrency |
| Point-Free: kolekcje Concurrency, Dependencies, SwiftUI, Modern Persistence | Brandon Williams, Stephen Celis | odcinki wideo, zaawansowany | 15–20 h | abonament (część odcinków 0 zł) | https://www.pointfree.co |
| Thinking in SwiftUI (aktualizacja dla iOS 17) | Chris Eidhof, Florian Kugler, objc.io | książka, średni–zaawansowany | 6–8 h | płatna | https://www.objc.io/books/thinking-in-swiftui/ |

Szczególnie ważne: izolacja aktorów i `Sendable`, `@MainActor` jako domyślna izolacja w nowych projektach Xcode 26, `nonisolated` i `@concurrent`, anulowanie zadań strukturalnych, wstrzykiwanie zależności w testach, model `@Observable` zamiast `ObservableObject`.

**Dowód:** aplikacja z etapu 1 skompilowana w trybie języka Swift 6 z pełnym sprawdzaniem współbieżności, bez ostrzeżeń i bez `@unchecked Sendable` bez uzasadnienia; ciężka praca wyniesiona do `@concurrent` lub aktora; zależności (sieć, czas, magazyn) wstrzykiwane i podmieniane w testach (zob. sekcja 6).

#### Etap 3: platforma iOS

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Managing your app’s life cycle | Apple | dokumentacja | 2–3 h | 0 zł | https://developer.apple.com/documentation/uikit/managing-your-app-s-life-cycle |
| BackgroundTasks (`BGAppRefreshTask`, `BGProcessingTask`) | Apple | dokumentacja | 3–4 h | 0 zł | https://developer.apple.com/documentation/backgroundtasks |
| SwiftData | Apple | dokumentacja | 4–6 h | 0 zł | https://developer.apple.com/documentation/swiftdata |
| Keychain services | Apple | dokumentacja | 3–4 h | 0 zł | https://developer.apple.com/documentation/security/keychain-services |
| Privacy manifest files (API wymagające uzasadnienia, manifesty SDK) | Apple | dokumentacja | 2–3 h | 0 zł | https://developer.apple.com/documentation/bundleresources/privacy-manifest-files |

Szczególnie ważne: system zawiesza i kończy aplikację bez ostrzeżenia, praca w tle jest planowana przez system, a nie przez aplikację, klasy ochrony danych i dostępności elementów Keychain, prośby o uprawnienia w kontekście, App Transport Security. Testy bezpieczeństwa według MASVS: zob. sekcja 10.

**Dowód:** synchronizacja danych przez `BGAppRefreshTask` odporna na zakończenie aplikacji; token sesji w Keychain z odpowiednią klasą dostępności; manifest prywatności zgodny z faktycznie używanymi API, także przez dołączone biblioteki.

#### Etap 4: rdzeń Rust na iOS

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The UniFFI user guide: rozdziały Swift („Compiling a Swift module”, „Integrating with Xcode”, `uniffi-bindgen-swift`) | Mozilla | dokumentacja | 4–6 h | 0 zł | https://mozilla.github.io/uniffi-rs/latest/swift/xcode.html |
| Creating a multiplatform binary framework bundle (XCFramework) | Apple | dokumentacja | 1–2 h | 0 zł | https://developer.apple.com/documentation/xcode/creating-a-multi-platform-binary-framework-bundle |
| „Ferrostar: Building a Cross-Platform Navigation SDK in Rust (Part 2 – iOS Packaging)” | Ian Wagner, Stadia Maps | studium przypadku | 1–2 h | 0 zł | https://stadiamaps.com/blog/ferrostar-building-a-cross-platform-navigation-sdk-in-rust-part-2/ |
| `cargo-swift` (budowa pakietu Swift z crate’a z UniFFI) | Antonius Naumann | narzędzie | 2–3 h | 0 zł | https://github.com/antoniusnaumann/cargo-swift |
| uniffi-starter (rdzeń Rust, skrypt XCFramework, Swift Package, wspólny z Androidem) | Ian Wagner | szablon projektu | 3–4 h | 0 zł | https://github.com/ianthetechie/uniffi-starter |
| Tauri 2 na iOS: wymagania, pluginy mobilne w Swifcie, publikacja w App Store | Tauri | dokumentacja (ścieżka alternatywna) | 6–8 h | 0 zł | https://v2.tauri.app/develop/plugins/develop-mobile/, https://v2.tauri.app/distribute/app-store/ |

Szczególnie ważne: targety `aarch64-apple-ios` i `aarch64-apple-ios-sim` (plus `x86_64-apple-ios` dla starszych Maców), łączenie bibliotek symulatora przez `lipo`, dystrybucja XCFramework jako `binaryTarget` z sumą kontrolną w `Package.swift`, mapowanie błędów Rusta na `throws`, funkcje async Rusta jako `async` w Swifcie, zgodność typów z UniFFI z `Sendable`, symbole debugowania rdzenia w raportach awarii, manifest prywatności także dla kodu Rust. Ten sam crate co na Androidzie (zob. sekcja 18.1, etap 4).

**Dowód:** rdzeń z sekcji 18.1 (model danych, walidacja, logika licencji i synchronizacji) dołączony do aplikacji z etapu 3 jako lokalny pakiet Swift z XCFramework, zbudowany jednym skryptem dla urządzenia i symulatora; błąd z Rusta obsłużony w UI jako `throws`; kompilacja w trybie Swift 6 bez ostrzeżeń współbieżności po stronie wiązań.

#### Etap 5: publikacja i monetyzacja w App Store

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| App Store Connect Help: rekord aplikacji, przesyłanie buildów, ceny, abonamenty, umowy i podatki | Apple | dokumentacja | 4–6 h | 0 zł | https://developer.apple.com/help/app-store-connect/ |
| TestFlight | Apple | dokumentacja | 1–2 h | 0 zł | https://developer.apple.com/testflight/ |
| App Review Guidelines (zwłaszcza 3.1.1 zakupy w aplikacji, 3.1.2 abonamenty, 5.1 prywatność) | Apple | zasady | 3–4 h | 0 zł | https://developer.apple.com/app-store/review/guidelines/ |
| StoreKit 2: przegląd, widoki sklepu, testowanie w Xcode, „Meet StoreKit 2” (WWDC21) | Apple | dokumentacja i wykład | 8–10 h | 0 zł | https://developer.apple.com/storekit/, https://developer.apple.com/videos/play/wwdc2021/10114/ |
| App Store Server API, App Store Server Notifications, App Store Server Library | Apple | dokumentacja i biblioteka | 4–6 h | 0 zł | https://developer.apple.com/documentation/appstoreservernotifications, https://github.com/apple/app-store-server-library-swift |
| App Privacy Details (etykiety prywatności) | Apple | dokumentacja | 1–2 h | 0 zł | https://developer.apple.com/app-store/app-privacy-details/ |
| Dystrybucja aplikacji w UE (alternatywne sklepy, dystrybucja przez stronę, warunki handlowe) | Apple | dokumentacja | 2–3 h | 0 zł | https://developer.apple.com/support/dma-and-apps-in-the-eu/ |
| App Store Small Business Program | Apple | program | 0,5 h | 0 zł | https://developer.apple.com/app-store/small-business-program/ |
| Upcoming requirements (minimalne SDK, np. Xcode 26 i SDK iOS 26 od 28 kwietnia 2026 r.) | Apple | komunikaty | ok. 0,5 h miesięcznie | 0 zł | https://developer.apple.com/news/upcoming-requirements/ |

Szczególnie ważne: przywracanie zakupów, nasłuch `Transaction.updates` od startu aplikacji, `Transaction.currentEntitlements` jako źródło uprawnień na urządzeniu, weryfikacja podpisanych transakcji JWS na serwerze, stany abonamentu (okres karencji, problemy z płatnością, zwroty), status przedsiębiorcy z DSA w UE, zasady linkowania do zakupów poza aplikacją różne dla sklepów USA, UE i reszty świata, ekran zakupu zgodny z regułami sklepu i prawem konsumenckim (zob. sekcja 13), automatyzacja wydań przez API App Store Connect (zob. sekcja 9).

**Dowód:** aplikacja z rdzeniem Rust przeszła recenzję Apple i jest dostępna w App Store, z abonamentem i zakupem jednorazowym w StoreKit 2; backend w Rust (Axum) odbiera App Store Server Notifications V2, weryfikuje podpisy i jest jedynym źródłem uprawnień, wspólnym z Google Play; etykieta prywatności i manifest prywatności zgodne z faktycznym przetwarzaniem; proces zgłaszania podatności zgodny z CRA opisany na stronie produktu.

#### Etap 6: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Improving your app’s performance (Instruments, metryki, `os_signpost`) | Apple | dokumentacja | 4–6 h | 0 zł | https://developer.apple.com/documentation/xcode/improving-your-app-s-performance |
| Sesje WWDC (SwiftUI, współbieżność, StoreKit, wydajność) | Apple | wykłady | ok. 10 h rocznie | 0 zł | https://developer.apple.com/videos/ |
| Swift Evolution i fora Swift | swift.org | źródła pierwotne | ok. 1 h tygodniowo | 0 zł | https://github.com/swiftlang/swift-evolution, https://forums.swift.org |
| Point-Free: zaawansowane serie (architektura, testowanie, mechanizmy wewnętrzne) | Brandon Williams, Stephen Celis | odcinki wideo | wg potrzeb | abonament | https://www.pointfree.co |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 20 pull requestów wygenerowanych przez agentów, recenzowanych według listy kontrolnej z etapów 2–5 (`@unchecked Sendable` i `nonisolated(unsafe)` bez uzasadnienia, `Task {}` bez anulowania, praca na `MainActor` blokująca UI, cykle referencji w domknięciach, wymuszone rozpakowanie `!`, starsze API zamiast StoreKit 2 i `@Observable`, brak przywracania zakupów, sekrety w `UserDefaults` zamiast Keychain, wymyślone API Apple),
- **wydajność:** profil uruchomienia i przewijania w Instruments, monitorowanie zawieszeń i awarii w Xcode Organizer z symbolami dSYM rdzenia Rust,
- **śledzenie zmian platformy:** coroczna migracja na nowe Xcode i SDK przed terminem Apple, przegląd zmian w zasadach recenzji i warunkach UE po każdej aktualizacji,
- **wkład w open source** w UniFFI, `cargo-swift` lub bibliotece Swift, choćby w dokumentację lub testy.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz zawieszenie UI, awarię na granicy Swift–Rust albo błąd uprawnień po zakupie w aplikacji z rdzeniem Rust, korzystając z Instruments, raportów awarii i powiadomień serwerowych App Store, i umiesz wyjaśnić przyczynę osobie nietechnicznej.

---

## 20. Lokalne AI i rozwój modeli

*Warstwa 7: AI w produktach. Opiera się na: 1, 6, 10 i 12. Jest podstawą: 21.*

Ta sekcja obejmuje pracę z modelami uruchamianymi na własnej maszynie oraz rozwój i dostosowanie modeli. Wbudowywanie AI w aplikacje, także przez API modeli w chmurze, jest w sekcji 21, a codzienna praca z Claude i Claude Code w sekcji 1. Zasada jest ta sama co w reszcie dokumentu: człowiek musi umieć ocenić, czy to, co przygotował agent, jest poprawne, bezpieczne i zgodne z przepisami.

### 20.1 Praca z lokalnym AI na maszynie

**Po co w tym modelu biznesowym:** praca na kodzie i danych klienta, które nie mogą opuścić maszyny (RODO, umowa), niezależność od jednego dostawcy AI i tańsze wykonywanie prostych, powtarzalnych zadań.

- Środowiska uruchomieniowe: Ollama, LM Studio, llama.cpp (`llama-server`), MLX na Apple Silicon; kiedy potrzebny jest serwer typu vLLM.
- Sprzęt i zasoby: VRAM, pamięć zunifikowana na Macu, przepustowość pamięci jako ograniczenie szybkości, backendy CUDA, Metal, ROCm i Vulkan, NPU w nowszych laptopach; szacowanie, jaki model zmieści się na danej maszynie.
- Formaty i kwantyzacja: GGUF, MLX, AWQ, GPTQ; poziomy kwantyzacji i ich wpływ na jakość; długość kontekstu i koszt pamięci podręcznej KV.
- Dobór modelu do zadania: modele do kodu z otwartymi wagami, modele ogólne, małe modele do klasyfikacji, modele embeddingowe; architektury MoE.
- Integracja z narzędziami: podłączenie Claude Code do lokalnego modelu przez endpoint zgodny z API Anthropic (`ANTHROPIC_BASE_URL`) albo przez bramkę LLM (np. LiteLLM), routing części zadań lokalnie, a części do Claude; endpointy zgodne z OpenAI.
- Podział ról: co może robić model lokalny (triage, klasyfikacja, streszczenia, wyszukiwanie w repozytorium, druga niezależna recenzja), a czego nie powinien robić bez nadzoru (zmiany w ścieżkach krytycznych).
- Bezpieczeństwo stanowiska: pochodzenie wag (zaufani wydawcy, formaty bez wykonywalnego kodu, np. `safetensors` zamiast `pickle`), serwer modelu nasłuchujący tylko lokalnie, odróżnianie modeli lokalnych od wariantów chmurowych w tych samych narzędziach, licencje modeli.

### 20.2 Rozwój i dostosowanie modeli lokalnych

- Ewaluacja: własny zestaw zadań i przypadków granicznych, metryki dopasowane do zadania, porównanie modeli i wersji, ocena przez model (LLM-as-judge) z kontrolą jego trafności na próbce ocenionej ręcznie.
- RAG: podział dokumentów na fragmenty, modele embeddingowe, wyszukiwanie wektorowe i hybrydowe (wektor i słowa kluczowe), reranking, ocena trafności wyszukiwania i odpowiedzi; bazy wektorowe (pgvector, Qdrant, LanceDB, sqlite-vec).
- Dostrajanie: LoRA i QLoRA, przygotowanie i czyszczenie zbiorów danych, podział na zbiory treningowy i testowy, wykrywanie przeuczenia i regresji; narzędzia ekosystemu Python (Hugging Face Transformers, PEFT, Unsloth lub podobne) oraz MLX na Macu.
- Destylacja i kompresja: przenoszenie umiejętności z dużego modelu do małego, kwantyzacja po dostrojeniu, konwersja do GGUF, ONNX lub formatów platformowych.
- Rust w ML: Candle, Burn, mistral.rs, wiązania llama.cpp, `ort` (ONNX Runtime), `tract`; tokenizery (`tokenizers`); biblioteki do embeddingów (np. `fastembed`); frameworki agentowe w Ruście (np. Rig).
- Dokumentacja modelu: karta modelu, dane treningowe i ich licencje, znane ograniczenia, wyniki ewaluacji; wpis modelu w SBOM jako ML-BOM (CycloneDX).
- Granica opłacalności: kiedy dostrajanie ma sens, a kiedy wystarczy lepszy prompt, RAG albo model chmurowy.

### 20.3 Ścieżka nauki: od zera do eksperta

Ścieżka ma 6 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Przed etapem 0 warto mieć Pythona na poziomie W (ścieżka uzupełniająca 20.4). Przy doświadczeniu seniorskim etap 0 można zaliczyć samym dowodem, a etap 1 warto przejść w całości, bo bezpośrednio przekłada się na pracę z kodem klientów, który nie może opuścić maszyny. Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem. Ewaluacje agentów i bezpieczeństwo LLM są w sekcji 11.1, OpenTelemetry ogólnie w sekcji 9.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | podstawy uczenia maszynowego i sieci neuronowych | 60–80 h | podstawy |
| 1 | modele lokalne na stanowisku pracy | 25–35 h | E |
| 2 | jak działa LLM od środka | 50–70 h | W |
| 3 | dostrajanie, RAG i ewaluacja modeli | 50–70 h | W, przy rozwoju modeli E |
| 4 | Rust w ML: Candle, Burn, mistral.rs, `ort` | 30–40 h | W |
| 5 | ekspert: modele lokalne w pracy z klientem, aktualność | stale, ok. 1–2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 215–295 h, czyli 5–7 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: podstawy uczenia maszynowego

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Practical Deep Learning for Coders, część 1 | Jeremy Howard, fast.ai | kurs wideo z notatnikami | 25–35 h | 0 zł | https://course.fast.ai |
| Neural Networks: Zero to Hero (od micrograd do GPT i tokenizera) | Andrej Karpathy | wykłady z kodem | 20–30 h | 0 zł | https://karpathy.ai/zero-to-hero.html |
| LLM Course, rozdziały 0–6 | Hugging Face | kurs online | 15–20 h | 0 zł | https://huggingface.co/learn/llm-course |

Szczególnie ważne: zbiór treningowy, walidacyjny i testowy, przeuczenie, funkcja straty i propagacja wsteczna, tokenizacja (źródło wielu dziwnych zachowań modeli), embeddingi, mechanizm uwagi.

**Dowód:** samodzielnie wytrenowany mały model (np. klasyfikator tekstu z fast.ai i bigramowy model językowy z wykładów Karpathy’ego) z poprawnym podziałem danych i wykresem straty, z opisem, po czym widać przeuczenie.

#### Etap 1: modele lokalne na stanowisku pracy

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Ollama: dokumentacja, API (w tym zgodność z OpenAI i Anthropic Messages API od wersji 0.14), integracja z Claude Code | Ollama | dokumentacja | 4–6 h | 0 zł | https://docs.ollama.com, https://docs.ollama.com/integrations/claude-code |
| llama.cpp: budowanie, `llama-server`, kwantyzacja GGUF | ggml-org | dokumentacja w repozytorium | 6–8 h | 0 zł | https://github.com/ggml-org/llama.cpp, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md |
| LM Studio: aplikacja, CLI `lms`, API | LM Studio | dokumentacja | 2–3 h | 0 zł | https://lmstudio.ai/docs |
| MLX i MLX LM (Apple Silicon) | Apple (ml-explore) | dokumentacja | 3–4 h | 0 zł | https://ml-explore.github.io/mlx/build/html/index.html, https://github.com/ml-explore/mlx-lm |
| vLLM | projekt vLLM | dokumentacja serwera wnioskowania | 3–4 h | 0 zł | https://docs.vllm.ai |
| LiteLLM: bramka (proxy) i endpoint `/v1/messages` | BerriAI | dokumentacja | 3–4 h | 0 zł | https://docs.litellm.ai/docs/, https://docs.litellm.ai/docs/anthropic_unified |

Uwaga do Claude Code: dokumentacja Anthropic o bramkach LLM zaznacza, że kierowanie Claude Code do modeli innych niż Claude nie jest przez Anthropic wspierane. Integracja przez Ollama czy LiteLLM działa, ale wyniki trzeba sprawdzać własnymi ewaluacjami (zob. sekcja 11.1).

Szczególnie ważne: szacowanie pamięci (wagi po kwantyzacji i pamięć podręczna KV dla danej długości kontekstu), wpływ poziomu kwantyzacji na jakość, serwer nasłuchujący tylko na `127.0.0.1`, odróżnianie modeli lokalnych od chmurowych w tym samym narzędziu (np. modele chmurowe Ollama), licencje wag.

**Dowód:** model lokalny wykonuje drugą, niezależną recenzję kodu klienta bez wysyłania danych poza maszynę: `llama-server` lub Ollama za bramką LiteLLM, sprawdzenie ruchu sieciowego (brak połączeń wychodzących), porównanie z recenzją Claude na 10 pull requestach z zapisem trafień i fałszywych alarmów oraz tabela: model, kwantyzacja, pamięć, tokeny na sekundę.

#### Etap 2: jak działa LLM od środka

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Build a Large Language Model (From Scratch) | Sebastian Raschka, Manning (2024) | książka z kodem, średni–zaawansowany | 30–40 h | płatna | https://www.manning.com/books/build-a-large-language-model-from-scratch |
| Hands-On Large Language Models | Jay Alammar, Maarten Grootendorst, O’Reilly (2024) | książka z ilustracjami i kodem, średni | 15–20 h | płatna | https://www.llm-book.com |
| LLM Course, rozdziały 7–12 (dostrajanie LLM, modele rozumujące) | Hugging Face | kurs online | 10–15 h | 0 zł | https://huggingface.co/learn/llm-course |

Szczególnie ważne: architektura transformera dekodującego, pretrening a dostrajanie instrukcyjne, próbkowanie (temperatura, top-p), embeddingi i ich zastosowanie w wyszukiwaniu.

**Dowód:** własna implementacja małego modelu GPT według książki Raschki, wczytanie do niej wag GPT-2 i dostrojenie do klasyfikacji tekstu, z notatką, które elementy odpowiadają parametrom widocznym w llama.cpp (kontekst, kwantyzacja, próbkowanie).

#### Etap 3: dostrajanie, RAG i ewaluacja modeli

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Transformers, PEFT (LoRA), TRL (`SFTTrainer`, `DPOTrainer`, `GRPOTrainer`) | Hugging Face | dokumentacja | 15–20 h | 0 zł | https://huggingface.co/docs/transformers, https://huggingface.co/docs/peft, https://huggingface.co/docs/trl |
| Unsloth: przewodnik dostrajania, eksport do GGUF | Unsloth | dokumentacja | 6–8 h | 0 zł | https://unsloth.ai/docs |
| MLX LM: dostrajanie LoRA na Macu | Apple (ml-explore) | dokumentacja w repozytorium | 3–4 h | 0 zł | https://github.com/ml-explore/mlx-lm |
| AI Engineering: Building Applications with Foundation Models, rozdziały o RAG, dostrajaniu i danych | Chip Huyen, O’Reilly (2025) | książka | 10–12 h | płatna | https://huyenchip.com/books/ |

Szczególnie ważne: najpierw prompt i RAG, dostrajanie dopiero gdy ewaluacja pokazuje, że to nie wystarcza; jakość i licencje danych treningowych; zbiór testowy rozdzielony od treningowego przed pierwszym eksperymentem; sprawdzanie regresji w zadaniach ogólnych po dostrojeniu.

**Dowód:** mały model dostrojony metodą LoRA lub QLoRA do zadania z niszy (np. klasyfikacja zgłoszeń bezpieczeństwa lub ocena wagi znalezisk z audytu), wyeksportowany do GGUF i uruchomiony w llama.cpp; raport ewaluacji przed i po dostrojeniu na wydzielonym zbiorze testowym oraz porównanie z wersją „prompt i RAG” bez dostrajania.

#### Etap 4: Rust w ML

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Candle: książka i przykłady | Hugging Face | dokumentacja | 8–10 h | 0 zł | https://huggingface.github.io/candle/, https://github.com/huggingface/candle |
| The Burn Book | Tracel AI | książka online | 8–10 h | 0 zł | https://burn.dev/books/burn/ |
| mistral.rs | Eric Buehler i społeczność | dokumentacja | 4–6 h | 0 zł | https://github.com/EricLBuehler/mistral.rs, https://docs.mistralrs.dev |
| `ort` (wiązania ONNX Runtime; wersja 2.0 w fazie RC) | pyke | dokumentacja | 4–6 h | 0 zł | https://ort.pyke.io |

Szczególnie ważne: kiedy wystarczy biblioteka w Ruście, a kiedy lepiej uruchomić llama.cpp jako proces poboczny; zgodność formatów (safetensors, GGUF, ONNX); akceleracja (CUDA, Metal) i jej wpływ na budowanie na trzech systemach (zob. sekcja 9); niestabilne API przed wersją 1.0.

**Dowód:** narzędzie CLI w Ruście, które liczy embeddingi plików repozytorium (Candle lub `ort`) i odpowiada na pytania przez mistral.rs lub llama.cpp, działające offline na Linuksie i macOS, z testem porównującym wyniki z referencyjną implementacją w Pythonie.

#### Etap 5: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Informacje o wydaniach llama.cpp, Ollama, ONNX Runtime, mistral.rs, MLX | autorzy projektów | źródła pierwotne | ok. 0,5 h tygodniowo | 0 zł | https://github.com/ggml-org/llama.cpp/releases |
| Blog i dokumentacja Hugging Face (nowe modele z otwartymi wagami, karty modeli) | Hugging Face | źródła pierwotne | ok. 0,5 h tygodniowo | 0 zł | https://huggingface.co/blog |
| Practical Deep Learning for Coders, część 2 (od podstaw do Stable Diffusion) | fast.ai | kurs wideo, zaawansowany | wg potrzeb | 0 zł | https://course.fast.ai |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **modele lokalne w pracy z klientem:** stały przepływ, w którym kod objęty umową poufności jest analizowany wyłącznie lokalnie, z zapisem w umowie i w ofercie,
- **przegląd co kwartał:** porównanie nowych modeli z otwartymi wagami na własnym zestawie ewaluacji (zob. sekcja 11.1) i decyzja o wymianie,
- **podatności środowisk uruchomieniowych:** llama.cpp, ONNX Runtime i biblioteki tokenizerów objęte tym samym procesem obsługi podatności co reszta zależności (zob. sekcja 10.1).

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień dobierasz model lokalny do zadania i sprzętu, oceniasz go na własnym zestawie ewaluacji względem modelu w chmurze i podłączasz do przepływu recenzji tak, że kod klienta nie opuszcza maszyny, a decyzję zapisujesz w ADR.

### 20.4 Ścieżka uzupełniająca: Python

Python jest potrzebny przed etapem 0 ścieżki 20.3, bo cały ekosystem ML (Transformers, PEFT, dostrajanie) jest w Pythonie. Przyda się też wcześniej, przy przejmowanych projektach klientów napisanych w Pythonie. Ok. 50–70 h od zera do poziomu W.

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Python Tutorial | Python Software Foundation | dokumentacja, od podstaw | 10–15 h | 0 zł | https://docs.python.org/3/tutorial/ |
| Effective Python (wydanie 3, do Pythona 3.13) | Brett Slatkin, Addison-Wesley | książka, średni–zaawansowany | 15–20 h | płatna | https://effectivepython.com |
| Fluent Python (wydanie 2) | Luciano Ramalho, O’Reilly | książka, zaawansowany | 20–25 h | płatna | https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/ |
| Static Typing with Python | Python Typing Team | dokumentacja i specyfikacja typowania | 4–5 h | 0 zł | https://typing.python.org |
| uv, Ruff, pytest | Astral, zespół pytest | dokumentacja narzędzi | 4–6 h | 0 zł | https://docs.astral.sh/uv/, https://docs.astral.sh/ruff/, https://docs.pytest.org |
| PyO3 i maturin (wywoływanie Rusta z Pythona) | zespół PyO3 | dokumentacja (opcjonalnie) | 4–6 h | 0 zł | https://pyo3.rs, https://www.maturin.rs |

Wystarczy jedna z dwóch płatnych książek: Effective Python przy pracy na cudzych projektach, Fluent Python przy głębszym zrozumieniu modelu danych języka. Ekosystem ML (Transformers, PEFT, dostrajanie): zob. sekcja 20.3, etap 3.

Szczególnie ważne: środowiska wirtualne i blokowanie zależności (`uv.lock`), adnotacje typów i sprawdzanie typów w CI, wyjątki i menedżery kontekstu, `async` w Pythonie, typowe podatności w przejmowanych projektach (`pickle`, `eval`, `subprocess` z `shell=True`, `yaml.load`).

**Dowód:** przejęty skrypt lub mała usługa w Pythonie przeprowadzona przez stabilizację: zależności zablokowane przez `uv`, Ruff i sprawdzanie typów bez błędów, testy w pytest dla ścieżek krytycznych i SBOM wygenerowany dla środowiska.

---

## 21. Funkcje AI w aplikacjach

*Warstwa 7: AI w produktach. Opiera się na: 1, 5, 6, 8, 10, 20 i platformach 14–19; etap 2 (TinyML) także na sekcji 22.*

Ta sekcja dotyczy AI jako części Twoich produktów i aplikacji klientów: modelu w chmurze wywoływanego przez API, modeli na urządzeniu i obowiązków, które z tego wynikają. Praca z AI jako narzędziem jest w sekcji 1, modele lokalne na stanowisku i ich rozwój w sekcji 20.

**Architektura i wybór miejsca wykonania**

- Decyzja chmura, urządzenie czy hybryda: prywatność, koszt na użytkownika, opóźnienie, praca offline, rozmiar aplikacji, jakość; zapisana w ADR.
- Model w chmurze: API Anthropic i innych dostawców (oficjalne SDK w TypeScript, klient HTTP w Ruście), streaming, tool use, wyjście strukturalne ze schematem, prompt caching, przetwarzanie wsadowe, limity i ponawianie.
- Backend jako pośrednik: klucze API nigdy w aplikacji klienckiej, limity per użytkownik, kontrola kosztów, cache odpowiedzi, wymiana modelu bez wydania aplikacji.
- Agenci i narzędzia w produkcie: projektowanie narzędzi, minimalne uprawnienia, potwierdzenie przez człowieka dla działań nieodwracalnych, MCP jako interfejs do danych.

**Modele na urządzeniu, według platformy**

- Web: WebGPU i WASM w przeglądarce (np. Transformers.js, WebLLM, ONNX Runtime Web), ograniczenia pamięci i pobierania modelu, Vercel AI SDK lub podobne do streamingu UI w Next.js.
- Desktop (Tauri, Rust): llama.cpp lub mistral.rs jako biblioteka albo proces poboczny, ONNX Runtime z akceleracją (CoreML, DirectML), pobieranie i aktualizacja modeli poza instalatorem, weryfikacja sum kontrolnych.
- macOS i iOS: Core ML, MLX, systemowe modele Apple (framework Foundation Models) i ich dostępność zależna od urządzenia i wersji systemu.
- Android: systemowe modele Google na urządzeniu (Gemini Nano przez ML Kit i AICore) i ich dostępność, LiteRT (dawniej TensorFlow Lite), ONNX Runtime Mobile, MediaPipe.
- Windows: Windows ML i akceleracja NPU, DirectML.
- Systemy wbudowane: TinyML (LiteRT for Microcontrollers, narzędzia typu Edge Impulse), modele w Ruście `no_std` (np. `tract` lub własne sieci po kwantyzacji int8), budżet pamięci, energii i czasu wnioskowania, akceleratory w mikrokontrolerach.

**Bezpieczeństwo funkcji AI**

- OWASP Top 10 dla aplikacji LLM: prompt injection bezpośredni i pośredni, niebezpieczna obsługa wyjścia modelu, wyciek danych i promptu systemowego, nadmierna sprawczość agentów, zatrucie danych RAG.
- Treści z zewnątrz (dokumenty, strony, e-maile) traktowane jako dane, nie instrukcje; separacja uprawnień między modelem a narzędziami.
- Walidacja wyjścia modelu przed użyciem (schemat, sanitacja HTML, zakaz wykonywania kodu z odpowiedzi bez piaskownicy).
- Ochrona modeli dostarczanych z aplikacją: podpis i integralność plików modelu, licencje wag, ryzyko ekstrakcji modelu z aplikacji.

**Jakość, testy i obserwowalność**

- Testowanie niedeterministycznych funkcji: zestawy referencyjne, progi jakości jako bramka w CI, testy regresji przy zmianie modelu lub promptu, testy adwersarialne (próby prompt injection).
- Wersjonowanie promptów, modeli i konfiguracji razem z kodem; możliwość wycofania.
- Obserwowalność: śledzenie wywołań LLM (np. konwencje OpenTelemetry dla GenAI, Langfuse lub podobne), koszt, opóźnienie, odsetek błędów i odmów, informacja zwrotna od użytkowników; bez zapisywania danych osobowych w logach.
- Ekonomia funkcji: koszt na aktywnego użytkownika wpisany w cenę abonamentu, limity w planach, degradacja do tańszego modelu.

**UX funkcji AI**

- Streaming i stany pośrednie, możliwość przerwania, edycji i ponowienia.
- Komunikowanie niepewności i ograniczeń, źródła przy odpowiedziach z RAG, kontrola człowieka przed skutkami.
- Ścieżka zastępcza, gdy model jest niedostępny, offline lub urządzenie go nie obsługuje.
- Dostępność interfejsów konwersacyjnych i treści generowanych.

**Prawo i zgodność**

- AI Act: obowiązki przejrzystości z art. 50 (informowanie o interakcji z AI, oznaczanie treści generowanych), rozpoznawanie zastosowań wysokiego ryzyka przed wejściem w budowę (kryterium z biznesplanu), obowiązki dostawców modeli ogólnego przeznaczenia przy publikacji własnych dostrojonych modeli.
- RODO: podstawa prawna przetwarzania przez AI, umowy powierzenia z dostawcami API, transfery poza EOG, retencja danych u dostawcy, prawo do sprzeciwu i wyjaśnienia; przewaga przetwarzania na urządzeniu.
- CRA: model jako element produktu z elementami cyfrowymi, podatności w środowiskach uruchomieniowych (llama.cpp, ONNX Runtime) objęte procesem obsługi podatności i SBOM.
- Zasady sklepów: wymagania Apple i Google dla treści generowanych przez AI, zgłaszanie treści przez użytkowników, deklaracje w sekcjach prywatności.
- Licencje modeli z otwartymi wagami: ograniczenia komercyjne, obowiązki przypisania, zakazy zastosowań.

### 21.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 5 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Etapy 0 i 3 warto przejść w całości, bo bezpośrednio przekładają się na usługi i produkty z biznesplanu. Etap 1 wymaga znajomości platform z sekcji 14–19, więc robi się go po nich. Etap 2 (embedded) robi się po sekcji 22 i jest opcjonalny do czasu decyzji o wejściu w urządzenia (zob. „Gdzie najpewniej będą luki”). Czas podany dla osoby startującej od zera; ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | funkcje AI w aplikacjach: API, streaming, obserwowalność | 30–40 h | E |
| 1 | AI na urządzeniu: web, desktop, iOS, Android, Windows | 50–70 h | W |
| 2 | TinyML na mikrokontrolerach (opcjonalnie) | 40–60 h | W |
| 3 | prawo i dokumentacja: AI Act art. 50, ML-BOM | 15–20 h | E |
| 4 | ekspert: produkt z funkcją AI, aktualność | stale, ok. 1–2 h tygodniowo | E |

Razem od zera do poziomu E: ok. 135–190 h (bez etapu 2: 95–130 h), czyli 3–5 miesięcy przy 10–12 h tygodniowo.

#### Etap 0: funkcje AI w aplikacjach

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Claude API: tool use, prompt caching, wyjście strukturalne, przetwarzanie wsadowe | Anthropic | dokumentacja | 8–10 h | 0 zł (zużycie API płatne) | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview, https://platform.claude.com/docs/en/build-with-claude/prompt-caching |
| Kurs „Building with the Claude API” | Anthropic Academy | kurs online | 6–8 h | 0 zł | https://anthropic.skilljar.com |
| AI SDK | Vercel | dokumentacja | 5–6 h | 0 zł | https://ai-sdk.dev/docs |
| Langfuse: śledzenie, ewaluacje, wersjonowanie promptów (open source, możliwy własny hosting) | Langfuse | dokumentacja | 4–5 h | 0 zł (własny hosting) / abonament (chmura) | https://langfuse.com/docs |
| Konwencje semantyczne OpenTelemetry dla GenAI (status „Development”, od czerwca 2026 r. w osobnym repozytorium) | OpenTelemetry | specyfikacja | 2–3 h | 0 zł | https://github.com/open-telemetry/semantic-conventions-genai |

Szczególnie ważne: klucz API tylko na backendzie, limity per użytkownik i budżet, cache promptów a koszt na aktywnego użytkownika, walidacja wyjścia modelu schematem przed użyciem, ścieżka zastępcza przy niedostępności modelu, nazwy atrybutów `gen_ai.*` mogą się zmieniać, więc wersję konwencji trzeba przypiąć.

**Dowód:** funkcja AI w aplikacji Next.js (np. streszczenie raportu z audytu dla klienta) z backendem pośredniczącym, streamingiem, wyjściem strukturalnym, śledzeniem w Langfuse lub przez OpenTelemetry bez danych osobowych w logach i bramką jakości w CI: zestaw referencyjny z progiem, który blokuje scalenie przy spadku wyników.

#### Etap 1: AI na urządzeniu

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Transformers.js (WebGPU i WASM) | Hugging Face | dokumentacja | 4–6 h | 0 zł | https://huggingface.co/docs/transformers.js |
| WebLLM | MLC AI | dokumentacja | 2–3 h | 0 zł | https://webllm.mlc.ai/docs/ |
| ONNX Runtime: Web, Mobile, dostawcy wykonania (CoreML, DirectML, NNAPI, QNN) | Microsoft | dokumentacja | 8–10 h | 0 zł | https://onnxruntime.ai/docs/ |
| Foundation Models framework | Apple | dokumentacja | 4–6 h | 0 zł | https://developer.apple.com/documentation/foundationmodels |
| Core ML | Apple | dokumentacja | 4–6 h | 0 zł | https://developer.apple.com/documentation/coreml |
| ML Kit GenAI APIs (Gemini Nano przez AICore, w tym Prompt API) | Google | dokumentacja | 4–6 h | 0 zł | https://developers.google.com/ml-kit/genai |
| LiteRT (dawniej TensorFlow Lite) i LiteRT-LM | Google AI Edge | dokumentacja | 6–8 h | 0 zł | https://developers.google.com/edge/litert |
| Windows ML (oparty na ONNX Runtime, akceleracja NPU) | Microsoft | dokumentacja | 4–6 h | 0 zł | https://learn.microsoft.com/windows/ai/new-windows-ml/overview |

Szczególnie ważne: dostępność modeli systemowych zależy od urządzenia, wersji systemu i regionu (Apple Intelligence, lista urządzeń z Gemini Nano), więc ścieżka zastępcza jest obowiązkowa; rozmiar pobieranego modelu i jego aktualizacja poza sklepem; weryfikacja sum kontrolnych i podpisu plików modelu.

**Dowód:** jedna funkcja (np. streszczenie lub klasyfikacja notatki) działająca na urządzeniu na trzech platformach: w przeglądarce (Transformers.js), na iOS (Foundation Models) i na Androidzie (ML Kit GenAI), ze ścieżką zastępczą do backendu i tabelą: dostępność, opóźnienie, rozmiar, jakość na wspólnym zestawie testowym.

#### Etap 2: TinyML na mikrokontrolerach (opcjonalnie)

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Tiny Machine Learning (Fundamentals, Applications, Deploying TinyML) | HarvardX (edX) | kursy online | 30–40 h | 0 zł (audyt) / płatny (certyfikat) | https://harvardonline.harvard.edu/course/fundamentals-tinyml |
| Machine Learning Systems (podręcznik, otwarty dostęp) | Harvard, MIT Press (2026) | książka online | wg potrzeb | 0 zł online | https://mlsysbook.ai |
| LiteRT for Microcontrollers | Google AI Edge | dokumentacja | 4–6 h | 0 zł | https://developers.google.com/edge/litert/microcontrollers/overview |
| Edge Impulse | Edge Impulse | dokumentacja i platforma | 6–8 h | 0 zł (plan Developer) / płatny (Enterprise) | https://docs.edgeimpulse.com |

Książka „TinyML” (Pete Warden, Daniel Situnayake, O’Reilly 2019) dobrze tłumaczy podstawy, ale opisuje TensorFlow Lite for Microcontrollers sprzed zmiany nazwy na LiteRT, więc przykłady kodu trzeba sprawdzać z bieżącą dokumentacją.

**Dowód:** model wykrywania słowa kluczowego lub gestu skwantyzowany do int8 i uruchomiony na mikrokontrolerze z sekcji 22 (np. nRF lub ESP32), z pomiarem pamięci, czasu wnioskowania i poboru energii; wersja w Ruście `no_std` z `tract` lub uzasadnienie, dlaczego zostaje C.

#### Etap 3: prawo i dokumentacja modeli

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Rozporządzenie (UE) 2024/1689 (AI Act), zwłaszcza art. 3, 6, 50 i załącznik III | UE | akt prawny | 4–6 h | 0 zł | https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng |
| Wytyczne w sprawie obowiązków przejrzystości dostawców i podmiotów stosujących systemy AI (art. 50, 20 lipca 2026 r.) | Komisja Europejska | wytyczne (niewiążące) | 3–4 h | 0 zł | https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems |
| Kodeks praktyk dotyczący oznaczania i etykietowania treści generowanych przez AI (10 czerwca 2026 r.) i FAQ | Komisja Europejska | kodeks praktyk (dobrowolny) | 3–4 h | 0 zł | https://digital-strategy.ec.europa.eu/en/news/commission-publishes-code-practice-marking-and-labelling-ai-generated-content, https://digital-strategy.ec.europa.eu/en/faqs/code-practice-transparency-ai-generated-content |
| CycloneDX ML-BOM i „Authoritative Guide to AI/ML-BOM” | OWASP CycloneDX | standard i przewodnik | 3–4 h | 0 zł | https://cyclonedx.org/capabilities/mlbom/, https://cyclonedx.org/guides/ |

Obowiązki przejrzystości z art. 50 stosuje się od 2 sierpnia 2026 r.; według FAQ Komisji systemy wprowadzone do obrotu przed tą datą mają czas na oznaczanie treści (art. 50 ust. 2) do 2 grudnia 2026 r. Pakiet „Digital Omnibus” zmienia część terminów AI Act, więc przed wdrożeniem trzeba sprawdzić tekst obowiązujący w danym dniu.

**Dowód:** dla funkcji AI z etapu 0: notatka kwalifikacyjna (czy to system wysokiego ryzyka, które ustępy art. 50 mają zastosowanie, kto jest dostawcą, a kto podmiotem stosującym), wdrożone informowanie użytkownika o interakcji z AI i oznaczenie treści generowanych zgodnie z kodeksem praktyk, wpis ML-BOM w SBOM wydania oraz karta modelu dla modelu dostrojonego w sekcji 20.3, etap 3.

#### Etap 4: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Strony Komisji o AI Act i o kodeksach praktyk | Komisja Europejska | źródła pierwotne | wg potrzeb | 0 zł | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **produkt z funkcją AI:** jedna własna aplikacja z funkcją AI wydana na co najmniej dwóch platformach, z kosztem na aktywnego użytkownika wpisanym w cenę i ścieżką zastępczą,
- **podatności środowisk uruchomieniowych:** llama.cpp, ONNX Runtime i biblioteki tokenizerów objęte tym samym procesem obsługi podatności co reszta zależności (zob. sekcja 10.1),
- **koszt funkcji AI:** co miesiąc koszt na aktywnego użytkownika względem ceny planu i decyzja o zmianie modelu, cache lub limitów.

**Dowód poziomu E:** samodzielnie, bez agenta, w 2 dni dodajesz do istniejącej aplikacji funkcję AI z wyborem miejsca wykonania uzasadnionym w ADR (chmura, urządzenie lub model lokalny), bramką jakości w CI, obserwowalnością bez danych osobowych, oznaczeniem zgodnym z art. 50 i wpisem ML-BOM, i umiesz wyjaśnić klientowi koszt, ryzyka i ograniczenia tej funkcji.

---

## 22. Systemy wbudowane

*Warstwa 8: sprzęt. Opiera się na: 10 i 12 na poziomie E oraz 12.2 (C).*

- Rust embedded: `no_std`, `embedded-hal`, warstwy PAC i HAL, Embassy (async), RTIC, `probe-rs`, `defmt`, `heapless`.
- Architektura sprzętu: Cortex-M, RISC-V, Xtensa; pamięć, linker scripts, przerwania, DMA, zegary, tryby oszczędzania energii.
- Protokoły: GPIO, I2C, SPI, UART, CAN, USB; BLE, Wi-Fi, MQTT, CoAP.
- Bootloadery i aktualizacje OTA z podpisem (np. `embassy-boot`, MCUboot), secure boot, szyfrowanie flash, blokada portów debugowania.
- Sprzęt w praktyce: czytanie not katalogowych i schematów, oscyloskop, analizator stanów logicznych.
- Opcjonalnie embedded Linux (Yocto, Buildroot) i Zephyr, jeśli urządzenia będą większe.
- Regulacje szczególnie ważne dla urządzeń: CRA dla produktów z elementami cyfrowymi, akt delegowany dyrektywy RED (cyberbezpieczeństwo urządzeń radiowych, normy EN 18031), ETSI EN 303 645 dla IoT konsumenckiego; przy zastosowaniach bezpieczeństwa funkcjonalnego IEC 61508 lub ISO 26262 (np. kompilator Ferrocene).

### 22.1 Ścieżka nauki: od zera do eksperta

Ścieżka ma 9 etapów, w tym jeden opcjonalny (embedded Linux). Każdy kończy się **dowodem**, czyli małym projektem na prawdziwym sprzęcie, który pokazuje, że etap jest opanowany. Doświadczenie seniora full-stack niewiele tu skraca: elektronika, pamięć bez systemu operacyjnego, przerwania i regulacje urządzeń to wiedza od zera, więc etapów 0–3 nie warto zaliczać samym dowodem. Skraca się tylko część o Ruście, jeśli sekcja 12 jest już opanowana. Czas podany dla osoby startującej od zera; ceny materiałów płatnych i sprzętu zmieniają się, więc warto je sprawdzić przed zakupem. Potrzebny sprzęt (płatny): micro:bit v2, płytka nRF52840 DK, płytka z ESP32-C3 lub ESP32-C6, sonda debugująca, multimetr, tani analizator stanów logicznych, płytka stykowa z zestawem elementów; oscyloskop od etapu 4.

| Etap | Cel | Czas od zera | Poziom po etapie |
|---|---|---|---|
| 0 | elektronika i sprzęt: prąd, napięcie, elementy, schematy, pomiary | 70–90 h | podstawy |
| 1 | pierwszy firmware w Ruście na micro:bit v2 | 40–50 h | podstawy |
| 2 | fundamenty: `no_std`, pamięć, linker, przerwania, architektura firmware | 50–70 h | W |
| 3 | współbieżność i narzędzia: Embassy, RTIC, `probe-rs`, `defmt` | 50–60 h | W |
| 4 | łączność: BLE, Wi-Fi, MQTT na nRF i ESP32 | 50–60 h | W |
| 5 | bezpieczne aktualizacje i produkcja: bootloader, OTA z podpisem, secure boot | 40–50 h | E |
| 6 | regulacje: CRA, RED i EN 18031, ETSI EN 303 645 | 30–40 h | W |
| 7 | opcjonalnie: embedded Linux i Zephyr | 60–80 h | W |
| 8 | ekspert: diagnostyka w terenie, recenzja kodu AI, aktualność | stale, ok. 2 h tygodniowo | E |

Razem od zera do poziomu E bez etapu 7: ok. 330–420 h, czyli 7–10 miesięcy przy 10–12 h tygodniowo; z etapem 7 o 1,5–2 miesiąca dłużej.

#### Etap 0: elektronika i sprzęt

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Lessons in Electric Circuits: tomy Direct Current, Semiconductors, Digital Circuits | All About Circuits | podręcznik online, od podstaw | 30–40 h | 0 zł | https://www.allaboutcircuits.com/textbook/ |
| Practical Electronics for Inventors (wydanie 4) | Paul Scherz, Simon Monk, McGraw Hill | książka, od podstaw do średniego | 25–30 h (wybrane rozdziały) | płatna | https://www.mheducation.com/highered/product/practical-electronics-inventors-fourth-edition-scherz-monk/9781259587542.html |
| Getting Started in KiCad (dokumentacja KiCad 10) | KiCad | dokumentacja, podstawowy | 6–8 h | 0 zł | https://docs.kicad.org |
| PulseView (sigrok): analizator stanów logicznych z dekoderami protokołów | sigrok | narzędzie i dokumentacja | 3–4 h | 0 zł | https://sigrok.org/wiki/PulseView |
| The Art of Electronics (wydanie 3), opcjonalnie z „Learning the Art of Electronics” | Paul Horowitz, Winfield Hill, Cambridge University Press | książka, zaawansowany, jako źródło referencyjne | wg potrzeb | płatna | https://artofelectronics.net |

Szczególnie ważne: prawo Ohma i dzielnik napięcia, rezystory podciągające, poziomy logiczne 3,3 V i 5 V, kondensatory odsprzęgające, tranzystor jako przełącznik, zasilanie i stabilizatory, czytanie noty katalogowej i schematu płytki rozwojowej, bezpieczna praca z zasilaczem i lutownicą.

**Dowód:** na płytce stykowej układ z diodą LED sterowaną tranzystorem, przyciskiem z rezystorem podciągającym i czujnikiem I2C, podłączony do gotowej płytki z mikrokontrolerem; schemat narysowany w KiCad, napięcia i prądy zmierzone multimetrem i zgodne z obliczeniami, transmisja I2C przechwycona i zdekodowana w PulseView.

#### Etap 1: pierwszy firmware w Ruście

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| micro:bit v2 Embedded Discovery Book | Rust Embedded Working Group | książka z ćwiczeniami na micro:bit v2, od podstaw | 25–30 h | 0 zł | https://docs.rust-embedded.org/discovery-mb2/ |
| Bare Metal Rust (część kursu Comprehensive Rust) | Google | kurs jednodniowy, micro:bit v2 i procesory aplikacyjne | 8–10 h | 0 zł | https://google.github.io/comprehensive-rust/bare-metal.html |

Podstawy samego Rusta są w sekcji 12. Starsza wersja Discovery (`docs.rust-embedded.org/discovery/microbit/`) jest zastąpiona wydaniem dla micro:bit v2.

**Dowód:** gra lub instrument na micro:bit v2 (matryca LED, przyciski, akcelerometr przez I2C), zbudowany i wgrany z `probe-rs`, z logami przez RTT; umiesz wskazać na schemacie płytki każdy użyty pin.

#### Etap 2: fundamenty

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Embedded Rust Book | Rust Embedded Working Group | książka, podstawowy–średni (przykłady na STM32F3DISCOVERY) | 12–15 h | 0 zł | https://docs.rust-embedded.org/book/ |
| The Embedonomicon | Rust Embedded Working Group | książka, zaawansowany: `no_std` od zera, linker scripts, runtime | 10–12 h | 0 zł | https://docs.rust-embedded.org/embedonomicon/ |
| Making Embedded Systems (wydanie 2, 2024) | Elecia White, O’Reilly | książka, średni: architektura, przerwania, energia, wzorce | 15–20 h | płatna | https://www.oreilly.com/library/view/-/9781098151539/ |
| Ogłoszenie `embedded-hal` 1.0 | Rust Embedded Working Group | artykuł, źródło pierwotne | 1 h | 0 zł | https://blog.rust-embedded.org/embedded-hal-v1/ |

Szczególnie ważne: warstwy PAC, HAL i BSP, cechy `embedded-hal` 1.0 jako granica sterownika, mapa pamięci i sekcje linkera, tablica wektorów przerwań, sekcje krytyczne, `static` i współdzielenie stanu z przerwaniem, DMA i jego zasady własności bufora, budżet RAM i flash (`cargo size`, `cargo bloat`), zachowanie po panice.

**Dowód:** sterownik czujnika I2C napisany wyłącznie na cechach `embedded-hal` 1.0, działający bez zmian na micro:bit i nRF52840 DK, z testami na hoście (zob. sekcja 6); notatka z mapą pamięci programu i uzasadnieniem każdego bloku `unsafe`.

#### Etap 3: współbieżność i narzędzia

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Embassy Book | zespół Embassy | dokumentacja: executor, przerwania, czas, HAL, bootloader | 10–12 h | 0 zł | https://embassy.dev/book/ |
| RTIC Book (v2) | zespół RTIC | dokumentacja, średni–zaawansowany | 6–8 h | 0 zł | https://rtic.rs/2/book/en/ |
| probe-rs: dokumentacja | zespół probe-rs | narzędzie: wgrywanie, debugowanie SWD/JTAG, RTT, VS Code | 3–4 h | 0 zł | https://probe.rs/docs/ |
| defmt book | Ferrous Systems | dokumentacja | 2–3 h | 0 zł | https://defmt.ferrous-systems.com |
| Rust Exercises: ćwiczenia nRF52 (BSP, radio, USB) | Ferrous Systems | ćwiczenia z materiałów szkoleniowych, CC BY-SA 4.0 | 15–20 h | 0 zł | https://rust-exercises.ferrous-systems.com/latest/book/ |

Szczególnie ważne: kiedy Embassy (async, wiele zadań, sterowniki async), a kiedy RTIC (twarde priorytety, analiza czasu); blokowanie executora i zagłodzenie zadań, priorytety przerwań, tryby uśpienia i pomiar poboru prądu, krokowe debugowanie i odczyt rejestrów, czytanie HardFault.

**Dowód:** na nRF52840 DK firmware w Embassy z co najmniej trzema zadaniami (czujnik, przycisk z eliminacją drgań, komunikacja USB lub radio), logi przez `defmt`; zmierzony pobór prądu w uśpieniu i porównany z notą katalogową; ten sam fragment przepisany w RTIC z krótkim porównaniem.

#### Etap 4: łączność

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| The Rust on ESP Book | Espressif, esp-rs | książka: ekosystem, narzędzia, `no_std` na ESP32 | 8–10 h | 0 zł | https://docs.espressif.com/projects/rust/book/ |
| Ogłoszenie esp-hal 1.0 i dokumentacja API | Espressif | artykuł i dokumentacja, źródło pierwotne | 2–3 h | 0 zł | https://developer.espressif.com/blog/2025/10/esp-hal-1/, https://docs.espressif.com/projects/rust/ |
| Embedded Rust (no_std) on Espressif | Espressif | warsztat na ESP32-C3 | 6–8 h | 0 zł | https://docs.espressif.com/projects/rust/no_std-training/ |
| Bluetooth Low Energy Fundamentals | Nordic Semiconductor (Nordic Developer Academy) | kurs, podstawowy–średni (przykłady w nRF Connect SDK, C) | 15–20 h | 0 zł | https://academy.nordicsemi.com |
| Interrupt | Memfault | blog: łączność, logowanie, diagnostyka w produkcji | 5–8 h (wybrane artykuły) | 0 zł | https://interrupt.memfault.com |

Uwaga do ESP32: esp-hal 1.0 (30 października 2025 r.) stabilizuje tylko inicjalizację, GPIO, UART, SPI, I2C, moduł czasu i konfigurację; reszta, w tym obsługa radia, jest za flagą `unstable`, więc API może się zmieniać między wersjami. Warsztat `no_std-training` jest oznaczony jako nieaktualny i przepisywany, dlatego przykłady trzeba porównywać z bieżącą dokumentacją. Kurs BLE od Nordic uczy protokołu (GAP, GATT, parowanie, oszczędzanie energii), a nie Rusta; w Ruście ten sam zakres realizuje stos BLE na Embassy.

**Dowód:** na ESP32-C3 lub ESP32-C6 czujnik wysyłający dane przez Wi-Fi do brokera MQTT z TLS i ponawianiem po utracie sieci, plus konfiguracja przez BLE z telefonu; zapis z analizatora lub oscyloskopu pokazujący zachowanie zasilania przy nadawaniu.

#### Etap 5: bezpieczne aktualizacje i produkcja

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Embassy Book: rozdział o bootloaderze (`embassy-boot`, podpis ed25519, próbny rozruch i wycofanie) | zespół Embassy | dokumentacja | 3–4 h | 0 zł | https://embassy.dev/book/dev/bootloader.html |
| MCUboot: projekt, `imgtool` (podpis obrazów, zarządzanie kluczami) | MCUboot (Linaro) | dokumentacja | 6–8 h | 0 zł | https://docs.mcuboot.com |
| Interrupt: artykuły o aktualizacjach firmware, bootloaderach i analizie awarii | Memfault | blog | 6–8 h | 0 zł | https://interrupt.memfault.com |
| Noty producentów o secure boot, szyfrowaniu flash i blokadzie debugowania (np. APPROTECT w nRF, Secure Boot i Flash Encryption w ESP32) | Nordic Semiconductor, Espressif | dokumentacja producenta | 6–8 h | 0 zł | dokumentacja wybranego układu |

Szczególnie ważne: układ partycji i odporność na zanik zasilania w trakcie aktualizacji, przechowywanie klucza prywatnego poza repozytorium i CI bez dostępu agenta, ochrona przed cofnięciem do podatnej wersji, blokada portów debugowania w produkcji, numer seryjny i identyfikacja wersji w terenie, SBOM firmware (zob. sekcja 10).

**Dowód:** urządzenie z etapu 4 z aktualizacją OTA podpisaną kluczem z bezpiecznego magazynu: niepodpisany lub zmodyfikowany obraz zostaje odrzucony, przerwanie zasilania w trakcie aktualizacji nie psuje urządzenia, nieudany rozruch nowej wersji wraca do poprzedniej, starsza wersja nie daje się wgrać; port debugowania zablokowany, SBOM w CycloneDX dołączany do każdego wydania.

#### Etap 6: regulacje

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Rozporządzenie (UE) 2024/2847 (Cyber Resilience Act) | UE (EUR-Lex) | akt prawny | 8–10 h | 0 zł | https://eur-lex.europa.eu/eli/reg/2024/2847/oj |
| Rozporządzenie delegowane (UE) 2022/30 do dyrektywy RED i zmieniające je rozporządzenie (UE) 2023/2444 (stosowanie od 1 sierpnia 2025 r.) | Komisja Europejska (EUR-Lex) | akty prawne | 2–3 h | 0 zł | https://eur-lex.europa.eu/eli/reg_del/2022/30/oj, https://eur-lex.europa.eu/eli/reg_del/2023/2444/oj |
| Decyzja wykonawcza (UE) 2025/138: normy zharmonizowane EN 18031-1, -2, -3 z ograniczeniami | Komisja Europejska (EUR-Lex) | akt prawny | 1–2 h | 0 zł | https://eur-lex.europa.eu/eli/dec_impl/2025/138/oj/eng |
| EN 18031-1, -2, -3 | CEN-CENELEC (w Polsce przez PKN) | normy | 10–12 h | płatne | sklep PKN lub krajowej jednostki normalizacyjnej |
| ETSI EN 303 645 V3.1.3 (2024): cyberbezpieczeństwo IoT konsumenckiego | ETSI | norma | 4–6 h | 0 zł | https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf |
| IEC 62443-4-1 i 4-2 (opcjonalnie, urządzenia przemysłowe) | IEC, ISA | normy | wg potrzeb | płatne | https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards |
| Ferrocene (opcjonalnie, bezpieczeństwo funkcjonalne: ISO 26262, IEC 61508, IEC 62304) | Ferrous Systems | kwalifikowany toolchain Rust, otwarte źródła | 2–3 h | 0 zł (wsparcie płatne) | https://ferrocene.dev, https://public-docs.ferrocene.dev/main/index.html |

Kalendarz na dzień 11 października 2026 r.: wymogi cyberbezpieczeństwa RED obowiązują od 1 sierpnia 2025 r.; obowiązki CRA dotyczące zgłaszania aktywnie wykorzystywanych podatności i poważnych incydentów obowiązują od 11 września 2026 r., także dla produktów już na rynku; pełne stosowanie CRA (wymagania zasadnicze, ocena zgodności, oznakowanie CE) od 11 grudnia 2027 r. Komisja zaproponowała uchylenie rozporządzenia 2022/30 z tym samym dniem, tak aby urządzenia radiowe przeszły pod CRA; przed planowaniem zgodności trzeba sprawdzić, czy akt uchylający został przyjęty. Normy EN 18031 dają domniemanie zgodności tylko poza wskazanymi w decyzji 2025/138 ograniczeniami (m.in. dopuszczenie braku hasła, kontrola rodzicielska, płatności).

**Dowód:** teczka zgodności dla urządzenia z etapu 5: zakres (czy RED, czy CRA, czy oba), ocena ryzyka, mapowanie wymagań EN 18031-1 na rozwiązania w firmware (aktualizacje, uwierzytelnianie, ochrona danych, porty debugowania), deklarowany okres wsparcia, polityka ujawniania podatności z kontaktem i procedurą zgłoszeń w terminach CRA, SBOM i instrukcja bezpiecznej konfiguracji dla użytkownika.

#### Etap 7: embedded Linux i Zephyr (opcjonalnie)

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Szkolenia: Embedded Linux, Yocto Project i OpenEmbedded, Buildroot (slajdy i ćwiczenia) | Bootlin | materiały szkoleniowe, CC BY-SA 3.0 | 30–40 h | 0 zł | https://bootlin.com/docs/ |
| Yocto Project Documentation (Quick Build, Overview and Concepts) | Yocto Project | dokumentacja | 10–15 h | 0 zł | https://docs.yoctoproject.org |
| Zephyr Project Documentation | Zephyr Project (Linux Foundation) | dokumentacja | 10–15 h | 0 zł | https://docs.zephyrproject.org/latest/ |
| nRF Connect SDK Fundamentals | Nordic Semiconductor (Nordic Developer Academy) | kurs na Zephyrze, podstawowy–średni | 15–20 h | 0 zł | https://academy.nordicsemi.com |

Etap ma sens dopiero wtedy, gdy klient lub produkt wymaga procesora aplikacyjnego z Linuksem albo certyfikowanego stosu radiowego dostępnego tylko w Zephyrze. Kod w C czyta się tu na poziomie W (zob. sekcja 16.2).

**Dowód:** obraz Yocto lub Buildroot dla płytki z materiałów Bootlin z własną aplikacją w Ruście jako usługą systemd, aktualizacją obrazu w schemacie A/B i SBOM; albo aplikacja Zephyr z MCUboot na nRF52840 DK.

#### Etap 8: ekspert

| Materiał | Autor / wydawca | Typ | Czas | Koszt | Link |
|---|---|---|---|---|---|
| Blog i newsletter Rust Embedded Working Group, lista awesome-embedded-rust | Rust Embedded Working Group | źródła pierwotne | ok. 1 h tygodniowo | 0 zł | https://blog.rust-embedded.org, https://github.com/rust-embedded/awesome-embedded-rust |
| Blog Embassy i informacje o wydaniach esp-hal | zespół Embassy, Espressif | źródła pierwotne | wg potrzeb | 0 zł | https://embassy.dev/blog/, https://developer.espressif.com/blog/ |
| Interrupt (wszystkie nowe artykuły i podsumowania lektur) | Memfault | blog | ok. 1 h tygodniowo | 0 zł | https://interrupt.memfault.com |
| Materiały szkoleniowe Ferrous Systems (pełny zestaw ćwiczeń) | Ferrous Systems | ćwiczenia | wg potrzeb | 0 zł | https://rust-exercises.ferrous-systems.com/latest/book/ |
| Errata i noty aplikacyjne używanych układów | producenci układów | dokumentacja producenta | wg potrzeb | 0 zł | dokumentacja wybranego układu |

Na tym etapie najważniejsza jest praktyka, a nie materiały:

- **recenzja kodu AI:** 20 pull requestów firmware wygenerowanych przez agentów, recenzowanych według listy kontrolnej z etapów 2–5: `unsafe` i `static mut` bez uzasadnienia, blokujące pętle w zadaniach async, błędne priorytety przerwań, rejestry i piny niezgodne z notą katalogową lub schematem (agent często wymyśla adresy i nazwy pól), brak obsługi zaniku zasilania, sekrety w obrazie, wyłączona weryfikacja podpisu,
- **testy na prawdziwym sprzęcie:** stanowisko hardware-in-the-loop w CI dla jednego urządzenia (zob. sekcja 6),
- **diagnostyka w terenie:** zbieranie zrzutów awarii i metryk z urządzeń oraz ćwiczenie wydania poprawki bezpieczeństwa przez OTA w 24 h,
- **śledzenie regulacji:** status uchylenia rozporządzenia 2022/30, normy zharmonizowane do CRA i wytyczne Komisji,
- **wkład w open source** w jednym crate’cie HAL lub sterowniku, choćby w obsługę nowego czujnika lub poprawkę dokumentacji.

**Dowód poziomu E:** samodzielnie, bez agenta, w 1 dzień diagnozujesz i naprawiasz błąd w nieznanym firmware (zawieszanie, HardFault, nadmierny pobór prądu albo błąd protokołu) z użyciem sondy, analizatora i not katalogowych, wydajesz poprawkę jako podpisaną aktualizację OTA i umiesz wyjaśnić klientowi, jak to wpływa na jego obowiązki z CRA.

---

## Gdzie najpewniej będą luki

Biznesplan zakłada stack TypeScript, React i Next.js jako potwierdzony. Nowe obszary to głównie:

- **praca z AI w chmurze na danych klientów** (sekcja 1): plany konsumenckie, w tym Max z biznesplanu, nie mają umowy powierzenia z Anthropic, a do pracy na repozytoriach i danych klientów prawdopodobnie potrzebny jest plan komercyjny (Team, Enterprise lub API); do weryfikacji z prawnikiem przed pierwszą umową,
- **wymagania i architektura** (sekcje 7–8): rdzeń pakietu „Audyt przejęcia” i procesu vicrafter; „Profil kompetencji” wymienia je jako osobne obszary, a dopiero ta wersja planu ma dla nich ścieżki nauki,
- **Rust na poziomie eksperta** (sekcja 12), bo staje się wspólnym rdzeniem wszystkich aplikacji kompilowanych,
- **dystrybucja i podpisy na 5 platformach** (sekcje 15–19),
- **systemy wbudowane** (sekcja 22), które wymagają też wiedzy sprzętowej i osobnych regulacji (RED, CRA dla urządzeń),
- **funkcje AI w aplikacjach** (sekcje 20–21), zwłaszcza bezpieczeństwo (prompt injection, obsługa wyjścia modelu), testowanie zachowań niedeterministycznych i obowiązki z AI Act; lokalne uruchamianie modeli jest już w profilu kompetencji, ale dostrajanie i wnioskowanie na urządzeniach mobilnych i wbudowanych to nowy zakres.

Embedded nie pojawia się w biznesplanie ani wśród kandydatów na własne aplikacje. Warto świadomie zdecydować, czy wchodzi do oferty w 2027 r., czy później: to największy koszt nauki przy najmniejszym związku z obecną niszą.

---

## Łączny czas nauki i kolejność

Suma ścieżek od zera do poziomu E we wszystkich 22 sekcjach to ok. **4 750–6 250 h**. Przy 10–12 h tygodniowo to wiele lat, więc całości nie da się przejść przed startem firmy i nie trzeba. Po odjęciu obszarów, które senior full-stack ma już opanowane (zwykle sekcje 2–5, część 6, 8, 9 i 13), zostaje realnie ok. 2 300–3 200 h.

| Warstwa | Sekcje | Czas od zera |
|---|---|---|
| 0 | 1, 2, 3 | 585–755 h |
| 1 | 4, 5 | 580–750 h |
| 2 | 6, 7, 8, 9 | 900–1 175 h |
| 3 | 10, 11 | 475–635 h |
| 4 | 12 (z 12.2), 13 | 615–815 h |
| 5 | 14, 15, 16, 17 (z 17.2) | 355–460 h |
| 6 | 18, 19 | 520–680 h |
| 7 | 20 (z 20.4), 21 | 400–555 h |
| 8 | 22 | 330–420 h |

Kolejność warstw zgadza się z bramkami biznesplanu. Jako senior masz w dużej części warstwy 0–1, więc przed startem pracujesz głównie nad sekcją 1 i warstwami 2–3, czyli dokładnie tym, czego wymaga bramka startowa.

| Okres | Bramka w biznesplanie | Sekcje w pierwszej kolejności | Cel poziomu |
|---|---|---|---|
| lis–gru 2026 | start: 3 chętnych klientów, szkielet vicrafter | 1 (etapy 0–2 oraz dane i umowy z etapu 4), 6 (testy charakteryzujące), 7 (do EARS i kryteriów akceptacji), 9 (pipeline z bramkami), 10 (do ASVS i SBOM), 11 (pierwsza wersja procesu) | W, w sekcjach 1 i 10 częściowo E |
| sty–mar 2027 | 2 opłacone projekty | dokończenie 1, 10 i 11; 7 do poziomu E; 8 do etapu 4 (odtwarzanie architektury przejmowanych aplikacji); 4 i 5 w zakresie audytu; 3.1 etap 4 (bezpieczeństwo Next.js) | E w obszarach audytu |
| kwi–cze 2027 | przygotowanie MVP własnej aplikacji | 12 (Rust do poziomu W, z 12.2 etap 1), 8 etapy 5–6 (architektura ewolucyjna, SaaS i wspólny rdzeń), 13, 14 i jedna platforma z 15–17 zgodnie z wynikiem discovery | W |
| lip–gru 2027 | MVP od lipca, roczna bramka | 12 do poziomu E, pozostałe platformy desktopowe, 20 etap 1 (modele lokalne w pracy z klientem) | E w Ruście |
| 2028 | portfel 2–3 aplikacji, desktop i mobile | 18 i 19 (mobile), 20 i 21 (AI w produktach) | W–E |
| od 2029 | decyzja o skali | 22 (embedded), jeśli wejdzie do oferty | według decyzji |

Zasada: uczysz się tego, co jest potrzebne w najbliższym projekcie lub bramce, a dowód z danej ścieżki robisz na realnej pracy (porzucony projekt open source, poligony z mapy nauki, własna aplikacja). Ścieżki z tego dokumentu warto przenieść do „Mapy nauki” w tej kolejności, z terminami.
