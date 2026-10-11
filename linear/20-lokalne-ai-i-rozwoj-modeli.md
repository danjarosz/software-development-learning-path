# 20. Lokalne AI i rozwój modeli: plan wdrożenia w Linear

Team **LEA** (https://linear.app/daankh/team/LEA/overview). Plan jest wdrożony w Linear. Klucze zadań (np. `S20-E0-M1`) są robocze, a identyfikator każdego zadania w Linear (`LEA-…`) jest w kolumnie „Linear” tabel zadań i w pliku `mapowanie-kluczy.csv`.

**W skrócie:** 6 kamieni milowych, 40 zadań (1 start, 30 materiałów, 6 dowodów, 3 praktyki). Plik główny z kolejnością projektów: `00-kolejnosc-i-zaleznosci.md`.

## 1. Projekt

| Pole | Wartość |
|---|---|
| Nazwa | 20. Lokalne AI i rozwój modeli |
| Team | LEA |
| Podsumowanie (pole „Summary”) | Warstwa 7: AI w produktach. Opiera się na: 1, 6, 10 i 12; etap podstaw uczenia maszynowego także na Pythonie z sekcji 2. Jest podstawą: 21 i etapu eksperckiego w 11. |
| Etykiety projektu | `warstwa-7` |
| Blokowany przez (projekty) | 01. Praca z AI w chmurze: Claude i Claude Code, 06. Testowanie, 10. Bezpieczeństwo, 12. Rust jako wspólny fundament |
| Blokuje (projekty) | 21. Funkcje AI w aplikacjach |
| Zależności częściowe (wchodzące) | etap 1 czeka na 02. Języki i narzędzia podstawowe (etap 3) |
| Zależności częściowe (wychodzące) | 11. Weryfikacja pracy AI i budowa procesu, etap 6; 21. Funkcje AI w aplikacjach, etap 3 |

### Opis projektu (do wklejenia w Linear)

*Warstwa 7: AI w produktach. Opiera się na: 1, 6, 10 i 12; etap podstaw uczenia maszynowego także na Pythonie z sekcji 2. Jest podstawą: 21 i etapu eksperckiego w 11.*

**Zakres umiejętności**

**Po co w tym modelu biznesowym:** praca na kodzie i danych klienta, które nie mogą opuścić maszyny (RODO, umowa), niezależność od jednego dostawcy AI i tańsze wykonywanie prostych, powtarzalnych zadań.
- Środowiska uruchomieniowe: Ollama, LM Studio, llama.cpp (`llama-server`), MLX na Apple Silicon; kiedy potrzebny jest serwer typu vLLM.
- Sprzęt i zasoby: VRAM, pamięć zunifikowana na Macu, przepustowość pamięci jako ograniczenie szybkości, backendy CUDA, Metal, ROCm i Vulkan, NPU w nowszych laptopach; szacowanie, jaki model zmieści się na danej maszynie.
- Formaty i kwantyzacja: GGUF, MLX, AWQ, GPTQ; poziomy kwantyzacji i ich wpływ na jakość; długość kontekstu i koszt pamięci podręcznej KV.
- Dobór modelu do zadania: modele do kodu z otwartymi wagami, modele ogólne, małe modele do klasyfikacji, modele embeddingowe; architektury MoE.
- Integracja z narzędziami: podłączenie Claude Code do lokalnego modelu przez endpoint zgodny z API Anthropic (`ANTHROPIC_BASE_URL`) albo przez bramkę LLM (np. LiteLLM), routing części zadań lokalnie, a części do Claude; endpointy zgodne z OpenAI.
- Podział ról: co może robić model lokalny (triage, klasyfikacja, streszczenia, wyszukiwanie w repozytorium, druga niezależna recenzja), a czego nie powinien robić bez nadzoru (zmiany w ścieżkach krytycznych).
- Bezpieczeństwo stanowiska: pochodzenie wag (zaufani wydawcy, formaty bez wykonywalnego kodu, np. `safetensors` zamiast `pickle`), serwer modelu nasłuchujący tylko lokalnie, odróżnianie modeli lokalnych od wariantów chmurowych w tych samych narzędziach, licencje modeli.
- Ewaluacja: własny zestaw zadań i przypadków granicznych, metryki dopasowane do zadania, porównanie modeli i wersji, ocena przez model (LLM-as-judge) z kontrolą jego trafności na próbce ocenionej ręcznie.
- RAG: podział dokumentów na fragmenty, modele embeddingowe, wyszukiwanie wektorowe i hybrydowe (wektor i słowa kluczowe), reranking, ocena trafności wyszukiwania i odpowiedzi; bazy wektorowe (pgvector, Qdrant, LanceDB, sqlite-vec).
- Dostrajanie: LoRA i QLoRA, przygotowanie i czyszczenie zbiorów danych, podział na zbiory treningowy i testowy, wykrywanie przeuczenia i regresji; narzędzia ekosystemu Python (Hugging Face Transformers, PEFT, Unsloth lub podobne) oraz MLX na Macu.
- Destylacja i kompresja: przenoszenie umiejętności z dużego modelu do małego (np. destylacja wiedzy w TRL, materiał opcjonalny w etapie dostrajania), kwantyzacja po dostrojeniu, konwersja do GGUF, ONNX lub formatów platformowych.
- Rust w ML: Candle, Burn, mistral.rs, wiązania llama.cpp, `ort` (ONNX Runtime), `tract`; tokenizery (`tokenizers`); biblioteki do embeddingów (np. `fastembed`); frameworki agentowe w Ruście (np. Rig).
- Dokumentacja modelu: karta modelu, dane treningowe i ich licencje, znane ograniczenia, wyniki ewaluacji; wpis modelu w SBOM jako ML-BOM (CycloneDX).
- Granica opłacalności: kiedy dostrajanie ma sens, a kiedy wystarczy lepszy prompt, RAG albo model chmurowy.

**Ścieżka nauki**

Ścieżka ma 6 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Pierwszy jest etap modeli lokalnych na stanowisku pracy: warto go przejść w całości, bo bezpośrednio przekłada się na pracę z kodem klientów, który nie może opuścić maszyny, i od niego zależy start sekcji 21. Od etapu podstaw uczenia maszynowego potrzebny jest Python na poziomie W (sekcja 2, etap Python), bo cały ekosystem ML (Transformers, PEFT, dostrajanie) jest w Pythonie. Przy doświadczeniu seniorskim etap podstaw uczenia maszynowego można zaliczyć samym dowodem. Ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem. Ewaluacje agentów i bezpieczeństwo LLM są w sekcji 11, OpenTelemetry ogólnie w sekcji 9.

**Definicja ukończenia projektu (dowód poziomu E)**

Samodzielnie, bez agenta, w 1 dzień dobierasz model lokalny do zadania i sprzętu, oceniasz go na własnym zestawie ewaluacji względem modelu w chmurze i podłączasz do przepływu recenzji tak, że kod klienta nie opuszcza maszyny, a decyzję zapisujesz w ADR.

**Źródło:** dokument „Umiejętności techniczne” w projekcie „JDG: Rozwój oprogramowania”, sekcja 20.

## 2. Kamienie milowe

Jeden kamień milowy na etap ścieżki. Kamień milowy jest zamknięty, gdy zamknięte jest zadanie dowodu tego etapu.

| # | Kamień milowy | Cel | Poziom po etapie | Zadania |
|---|---|---|---|---|
| 1 | Etap 0: modele lokalne na stanowisku pracy | modele lokalne na stanowisku pracy | W | 7 |
| 2 | Etap 1: podstawy uczenia maszynowego | podstawy uczenia maszynowego i sieci neuronowych | W | 4 |
| 3 | Etap 2: jak działa LLM od środka | jak działa LLM od środka | W | 4 |
| 4 | Etap 3: dostrajanie, RAG i ewaluacja modeli | dostrajanie, RAG i ewaluacja modeli | W | 11 |
| 5 | Etap 4: Rust w ML | Rust w ML: Candle, Burn, mistral.rs, `ort` | W | 6 |
| 6 | Etap 5: ekspert | ekspert: modele lokalne w pracy z klientem, aktualność | E | 7 |

## 3. Punkt startu

Zadanie **`S20-START` · Start: 20. Lokalne AI i rozwój modeli** (LEA-876 w Linear) to jedyne wejście do projektu: wszystkie zadania pierwszego etapu są przez nie blokowane.

- **Blokowane przez:** `S01-E1-D`, `S06-E1-D`, `S10-E1-D`, `S12-E2-D`
- **Odblokowuje:** `S20-E0-M1`, `S20-E0-M2`, `S20-E0-M3`, `S20-E0-M4`, `S20-E0-M5`, `S20-E0-M6`
- **Status początkowy:** Backlog do czasu zamknięcia zadań blokujących, potem Todo

Opis zadania (do wklejenia):

Punkt startu projektu „20. Lokalne AI i rozwój modeli”.

**Warunki wejścia (zadania blokujące):**

- `S01-E1-D` · Dowód etapu 1: codzienna praca z Claude Code — sekcja 1 na poziomie podstawowym do pracy (etap 1)
- `S06-E1-D` · Dowód etapu 1: projektowanie testów i TDD — sekcja 6 na poziomie podstawowym do pracy (etap 1)
- `S10-E1-D` · Dowód etapu 1: ataki na web i API w praktyce — sekcja 10 na poziomie podstawowym do pracy (etap 1)
- `S12-E2-D` · Dowód etapu 2: własność, pożyczanie, czasy życia — sekcja 12 na poziomie podstawowym do pracy (etap 2)

**Do zrobienia:**

- przeczytać sekcję 20 dokumentu „Umiejętności techniczne”,
- zaznaczyć etapy, które zaliczasz samym dowodem (zgodnie z akapitem wstępnym ścieżki), i dla nich zamknąć zadania materiałów jako niepotrzebne.

**Folder roboczy:** `20-lokalne-ai-i-rozwoj-modeli/`

## 4. Przepływ zależności

Linie ciągłe to zależności wewnątrz projektu, przerywane to zadania z innych projektów. Wewnątrz etapu zadania materiałów są równoległe i wszystkie blokują dowód etapu; dowód etapu blokuje materiały kolejnego etapu.

```mermaid
flowchart TD
  START["20. Start"]
  E0["Etap 0: modele lokalne na stanowisku pracy"]
  E1["Etap 1: podstawy uczenia maszynowego"]
  E2["Etap 2: jak działa LLM od środka"]
  E3["Etap 3: dostrajanie, RAG i ewaluacja modeli"]
  E4["Etap 4: Rust w ML"]
  E5["Etap 5: ekspert"]
  START --> E0
  E0 --> E1
  XS02E3D(["S02-E3-D"]) -.-> E1
  E1 --> E2
  E2 --> E3
  E3 --> E4
  E4 --> E5
  XS01E1D(["S01-E1-D"]) -.-> START
  XS06E1D(["S06-E1-D"]) -.-> START
  XS10E1D(["S10-E1-D"]) -.-> START
  XS12E2D(["S12-E2-D"]) -.-> START
```

## 5. Zadania według kamieni milowych

Szablon opisu zadania materiału: nazwa materiału, autor lub wydawca, typ, czas, koszt i link (jak w kolumnach poniżej), zdanie „Gotowe, gdy materiał jest przerobiony w zakresie potrzebnym do dowodu etapu” oraz folder roboczy z kolumny „Folder”. Opisy dowodów i praktyk są podane pod tabelą każdego etapu.

### Etap 0: modele lokalne na stanowisku pracy

Opis kamienia milowego (do wklejenia):

**Cel:** modele lokalne na stanowisku pracy · **Poziom po etapie:** W

**Szczególnie ważne:** szacowanie pamięci (wagi po kwantyzacji i pamięć podręczna KV dla danej długości kontekstu), wpływ poziomu kwantyzacji na jakość, serwer nasłuchujący tylko na `127.0.0.1`, odróżnianie modeli lokalnych od chmurowych w tym samym narzędziu (np. modele chmurowe Ollama), licencje wag.

Uwaga do Claude Code: dokumentacja Anthropic o bramkach LLM zaznacza, że kierowanie Claude Code do modeli innych niż Claude nie jest przez Anthropic wspierane. Integracja przez Ollama czy LiteLLM działa, ale wyniki trzeba sprawdzać własnymi ewaluacjami (zob. sekcja 11).

**Dowód:** Model lokalny wykonuje drugą, niezależną recenzję kodu klienta bez wysyłania danych poza maszynę: `llama-server` lub Ollama za bramką LiteLLM, sprawdzenie ruchu sieciowego (brak połączeń wychodzących), porównanie z recenzją Claude na 10 pull requestach z zapisem trafień i fałszywych alarmów oraz tabela: model, kwantyzacja, pamięć, tokeny na sekundę.

| Klucz | Linear | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|---|
| `S20-E0-M1` | LEA-933 | Przerobić: Ollama: dokumentacja, API (w tym zgodność z OpenAI i Anthropic Messages API od wersji 0.14)… | materiał | 4–6 h | 0 zł | https://docs.ollama.com, https://docs.ollama.com/integrations/claude-code | `S20-START` | `S20-E0-D` | `20-lokalne-ai-i-rozwoj-modeli/e0-modele-lokalne-na-stanowisku-pracy/` |
| `S20-E0-M2` | LEA-936 | Przerobić: llama.cpp: budowanie, `llama-server`, kwantyzacja GGUF | materiał | 6–8 h | 0 zł | https://github.com/ggml-org/llama.cpp, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | `S20-START` | `S20-E0-D` | `20-lokalne-ai-i-rozwoj-modeli/e0-modele-lokalne-na-stanowisku-pracy/` |
| `S20-E0-M3` | LEA-939 | Przerobić: LM Studio: aplikacja, CLI `lms`, API | materiał | 2–3 h | 0 zł | https://lmstudio.ai/docs | `S20-START` | `S20-E0-D` | `20-lokalne-ai-i-rozwoj-modeli/e0-modele-lokalne-na-stanowisku-pracy/` |
| `S20-E0-M4` | LEA-941 | Przerobić: MLX i MLX LM (Apple Silicon) | materiał | 3–4 h | 0 zł | https://ml-explore.github.io/mlx/build/html/index.html, https://github.com/ml-explore/mlx-lm | `S20-START` | `S20-E0-D` | `20-lokalne-ai-i-rozwoj-modeli/e0-modele-lokalne-na-stanowisku-pracy/` |
| `S20-E0-M5` | LEA-943 | Przerobić: vLLM | materiał | 3–4 h | 0 zł | https://docs.vllm.ai | `S20-START` | `S20-E0-D` | `20-lokalne-ai-i-rozwoj-modeli/e0-modele-lokalne-na-stanowisku-pracy/` |
| `S20-E0-M6` | LEA-945 | Przerobić: LiteLLM: bramka (proxy) i endpoint `/v1/messages` | materiał | 3–4 h | 0 zł | https://docs.litellm.ai/docs/, https://docs.litellm.ai/docs/anthropic_unified | `S20-START` | `S20-E0-D` | `20-lokalne-ai-i-rozwoj-modeli/e0-modele-lokalne-na-stanowisku-pracy/` |
| `S20-E0-D` | LEA-959 | Dowód etapu 0: modele lokalne na stanowisku pracy | dowód | — | — | — | `S20-E0-M1`, `S20-E0-M2`, `S20-E0-M3`, `S20-E0-M4`, `S20-E0-M5`, `S20-E0-M6` | `S11-E6-M1`, `S11-E6-M2`, `S11-E6-M3`, `S11-E6-M4`, `S11-E6-P1`, `S11-E6-P2`, `S11-E6-P3`, `S11-E6-P4`, `S20-E1-M1`, `S20-E1-M2`, `S20-E1-M3`, `S21-START` | `20-lokalne-ai-i-rozwoj-modeli/e0-modele-lokalne-na-stanowisku-pracy/` |

**`S20-E0-D` · Dowód etapu 0: modele lokalne na stanowisku pracy**

Model lokalny wykonuje drugą, niezależną recenzję kodu klienta bez wysyłania danych poza maszynę: `llama-server` lub Ollama za bramką LiteLLM, sprawdzenie ruchu sieciowego (brak połączeń wychodzących), porównanie z recenzją Claude na 10 pull requestach z zapisem trafień i fałszywych alarmów oraz tabela: model, kwantyzacja, pamięć, tokeny na sekundę.

**Na co zwrócić uwagę:** szacowanie pamięci (wagi po kwantyzacji i pamięć podręczna KV dla danej długości kontekstu), wpływ poziomu kwantyzacji na jakość, serwer nasłuchujący tylko na `127.0.0.1`, odróżnianie modeli lokalnych od chmurowych w tym samym narzędziu (np. modele chmurowe Ollama), licencje wag.

**Kryterium ukończenia:** serwer modelu nasłuchuje tylko na `127.0.0.1`, zapis ruchu sieciowego z recenzji nie zawiera połączeń wychodzących, tabela porównania obejmuje 10 pull requestów i co najmniej dwa modele lub dwie kwantyzacje.

**Folder roboczy:** `20-lokalne-ai-i-rozwoj-modeli/e0-modele-lokalne-na-stanowisku-pracy/`

### Etap 1: podstawy uczenia maszynowego

Opis kamienia milowego (do wklejenia):

**Cel:** podstawy uczenia maszynowego i sieci neuronowych · **Poziom po etapie:** W

**Szczególnie ważne:** zbiór treningowy, walidacyjny i testowy, przeuczenie, funkcja straty i propagacja wsteczna, tokenizacja (źródło wielu dziwnych zachowań modeli), embeddingi, mechanizm uwagi.

**Dowód:** Samodzielnie wytrenowany mały model (np. klasyfikator tekstu z fast.ai i bigramowy model językowy z wykładów Karpathy’ego) z poprawnym podziałem danych i wykresem straty, z opisem, po czym widać przeuczenie.

| Klucz | Linear | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|---|
| `S20-E1-M1` | LEA-973 | Przerobić: Practical Deep Learning for Coders, część 1 | materiał | 25–35 h | 0 zł | https://course.fast.ai | `S20-E0-D`, `S02-E3-D` | `S20-E1-D` | `20-lokalne-ai-i-rozwoj-modeli/e1-podstawy-uczenia-maszynowego/` |
| `S20-E1-M2` | LEA-974 | Przerobić: Neural Networks: Zero to Hero (od micrograd do GPT i tokenizera) | materiał | 20–30 h | 0 zł | https://karpathy.ai/zero-to-hero.html | `S20-E0-D`, `S02-E3-D` | `S20-E1-D` | `20-lokalne-ai-i-rozwoj-modeli/e1-podstawy-uczenia-maszynowego/` |
| `S20-E1-M3` | LEA-975 | Przerobić: LLM Course, rozdziały 0–6 | materiał | 15–20 h | 0 zł | https://huggingface.co/learn/llm-course | `S20-E0-D`, `S02-E3-D` | `S20-E1-D` | `20-lokalne-ai-i-rozwoj-modeli/e1-podstawy-uczenia-maszynowego/` |
| `S20-E1-D` | LEA-1004 | Dowód etapu 1: podstawy uczenia maszynowego | dowód | — | — | — | `S20-E1-M1`, `S20-E1-M2`, `S20-E1-M3` | `S20-E2-M1`, `S20-E2-M2`, `S20-E2-M3` | `20-lokalne-ai-i-rozwoj-modeli/e1-podstawy-uczenia-maszynowego/` |

**`S20-E1-D` · Dowód etapu 1: podstawy uczenia maszynowego**

Samodzielnie wytrenowany mały model (np. klasyfikator tekstu z fast.ai i bigramowy model językowy z wykładów Karpathy’ego) z poprawnym podziałem danych i wykresem straty, z opisem, po czym widać przeuczenie.

**Na co zwrócić uwagę:** zbiór treningowy, walidacyjny i testowy, przeuczenie, funkcja straty i propagacja wsteczna, tokenizacja (źródło wielu dziwnych zachowań modeli), embeddingi, mechanizm uwagi.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.

**Folder roboczy:** `20-lokalne-ai-i-rozwoj-modeli/e1-podstawy-uczenia-maszynowego/`

### Etap 2: jak działa LLM od środka

Opis kamienia milowego (do wklejenia):

**Cel:** jak działa LLM od środka · **Poziom po etapie:** W

**Szczególnie ważne:** architektura transformera dekodującego, pretrening a dostrajanie instrukcyjne, próbkowanie (temperatura, top-p), embeddingi i ich zastosowanie w wyszukiwaniu.

**Dowód:** Własna implementacja małego modelu GPT według książki Raschki, wczytanie do niej wag GPT-2 i dostrojenie do klasyfikacji tekstu, z notatką, które elementy odpowiadają parametrom widocznym w llama.cpp (kontekst, kwantyzacja, próbkowanie).

| Klucz | Linear | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|---|
| `S20-E2-M1` | LEA-1021 | Przerobić: Build a Large Language Model (From Scratch) | materiał, płatny | 30–40 h | płatna | https://www.manning.com/books/build-a-large-language-model-from-scratch | `S20-E1-D` | `S20-E2-D` | `20-lokalne-ai-i-rozwoj-modeli/e2-jak-dziala-llm-od-srodka/` |
| `S20-E2-M2` | LEA-1022 | Przerobić: Hands-On Large Language Models | materiał, płatny, opcjonalne | 15–20 h | płatna | https://www.llm-book.com | `S20-E1-D` | — | `20-lokalne-ai-i-rozwoj-modeli/e2-jak-dziala-llm-od-srodka/` |
| `S20-E2-M3` | LEA-1023 | Przerobić: LLM Course, rozdziały 7–12 (dostrajanie LLM, modele rozumujące) | materiał | 10–15 h | 0 zł | https://huggingface.co/learn/llm-course | `S20-E1-D` | `S20-E2-D` | `20-lokalne-ai-i-rozwoj-modeli/e2-jak-dziala-llm-od-srodka/` |
| `S20-E2-D` | LEA-1024 | Dowód etapu 2: jak działa LLM od środka | dowód | — | — | — | `S20-E2-M1`, `S20-E2-M3` | `S20-E3-M1`, `S20-E3-M2`, `S20-E3-M3`, `S20-E3-M4`, `S20-E3-M5`, `S20-E3-M6`, `S20-E3-M7`, `S20-E3-M8`, `S20-E3-M9`, `S20-E3-M10` | `20-lokalne-ai-i-rozwoj-modeli/e2-jak-dziala-llm-od-srodka/` |

**`S20-E2-D` · Dowód etapu 2: jak działa LLM od środka**

Własna implementacja małego modelu GPT według książki Raschki, wczytanie do niej wag GPT-2 i dostrojenie do klasyfikacji tekstu, z notatką, które elementy odpowiadają parametrom widocznym w llama.cpp (kontekst, kwantyzacja, próbkowanie).

**Na co zwrócić uwagę:** architektura transformera dekodującego, pretrening a dostrajanie instrukcyjne, próbkowanie (temperatura, top-p), embeddingi i ich zastosowanie w wyszukiwaniu.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.

**Folder roboczy:** `20-lokalne-ai-i-rozwoj-modeli/e2-jak-dziala-llm-od-srodka/`

### Etap 3: dostrajanie, RAG i ewaluacja modeli

Opis kamienia milowego (do wklejenia):

**Cel:** dostrajanie, RAG i ewaluacja modeli · **Poziom po etapie:** W

**Szczególnie ważne:** najpierw prompt i RAG, dostrajanie dopiero gdy ewaluacja pokazuje, że to nie wystarcza; rozmiar fragmentów i ich kontekst, ocena wyszukiwania osobno od oceny odpowiedzi; jakość i licencje danych treningowych; zbiór testowy rozdzielony od treningowego przed pierwszym eksperymentem; sprawdzanie regresji w zadaniach ogólnych po dostrojeniu.

**Dowód:** Mały model dostrojony metodą LoRA lub QLoRA do zadania z niszy (np. klasyfikacja zgłoszeń bezpieczeństwa lub ocena wagi znalezisk z audytu), wyeksportowany do GGUF i uruchomiony w llama.cpp, z raportem ewaluacji przed i po dostrojeniu na wydzielonym zbiorze testowym. Porównanie z wersją „prompt i RAG” bez dostrajania: RAG na pgvector z lokalnym modelem embeddingowym, chunkingiem, wyszukiwaniem hybrydowym (wektor i BM25 lub pełnotekstowe) i rerankingiem, oceniony na co najmniej 50 pytaniach z oznaczonymi właściwymi fragmentami: recall@5 i MRR dla trzech wariantów (sam wektor, hybryda, hybryda z rerankingiem).

| Klucz | Linear | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|---|
| `S20-E3-M1` | LEA-1041 | Przerobić: Transformers, PEFT (LoRA), TRL (`SFTTrainer`, `DPOTrainer`, `GRPOTrainer`) | materiał | 15–20 h | 0 zł | https://huggingface.co/docs/transformers, https://huggingface.co/docs/peft, https://huggingface.co/docs/trl | `S20-E2-D` | `S20-E3-D` | `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/` |
| `S20-E3-M2` | LEA-1043 | Przerobić: Unsloth: przewodnik dostrajania, eksport do GGUF | materiał | 6–8 h | 0 zł | https://unsloth.ai/docs | `S20-E2-D` | `S20-E3-D` | `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/` |
| `S20-E3-M3` | LEA-1045 | Przerobić: MLX LM: dostrajanie LoRA na Macu | materiał | 3–4 h | 0 zł | https://github.com/ml-explore/mlx-lm | `S20-E2-D` | `S20-E3-D` | `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/` |
| `S20-E3-M4` | LEA-1046 | Przerobić: AI Engineering: Building Applications with Foundation Models, rozdziały o RAG, dostrajaniu i danych | materiał, płatny | 10–12 h | płatna | https://huyenchip.com/books/ | `S20-E2-D` | `S20-E3-D` | `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/` |
| `S20-E3-M5` | LEA-1047 | Przerobić: Sentence Transformers: modele embeddingowe, wyszukiwanie semantyczne i reranking (`CrossEncoder`) | materiał | 5–6 h | 0 zł | https://sbert.net, https://www.sbert.net/docs/cross_encoder/usage/usage.html | `S20-E2-D` | `S20-E3-D` | `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/` |
| `S20-E3-M6` | LEA-1048 | Przerobić: MTEB: ranking modeli embeddingowych (wybór modelu do języka i zadania) | materiał | 1–2 h | 0 zł | https://huggingface.co/spaces/mteb/leaderboard | `S20-E2-D` | `S20-E3-D` | `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/` |
| `S20-E3-M7` | LEA-1049 | Przerobić: pgvector: indeksy HNSW i IVFFlat, wyszukiwanie hybrydowe z pełnotekstowym w PostgreSQL | materiał | 3–4 h | 0 zł | https://github.com/pgvector/pgvector | `S20-E2-D` | `S20-E3-D` | `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/` |
| `S20-E3-M8` | LEA-1051 | Przerobić: Contextual Retrieval: chunking z kontekstem, BM25 i embeddingi, reranking, ocena recall@k | materiał | 1–2 h | 0 zł | https://www.anthropic.com/news/contextual-retrieval | `S20-E2-D` | `S20-E3-D` | `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/` |
| `S20-E3-M9` | LEA-1060 | Przerobić: LanceDB i Qdrant: bazy wektorowe wbudowana i serwerowa | materiał, opcjonalne | 3–4 h | 0 zł | https://lancedb.com/docs, https://qdrant.tech/documentation/ | `S20-E2-D` | — | `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/` |
| `S20-E3-M10` | LEA-1062 | Przerobić: TRL: `GKDTrainer` (destylacja wiedzy z dużego modelu do małego) | materiał, opcjonalne | 3–4 h | 0 zł | https://huggingface.co/docs/trl/gkd_trainer | `S20-E2-D` | — | `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/` |
| `S20-E3-D` | LEA-1065 | Dowód etapu 3: dostrajanie, RAG i ewaluacja modeli | dowód | — | — | — | `S20-E3-M1`, `S20-E3-M2`, `S20-E3-M3`, `S20-E3-M4`, `S20-E3-M5`, `S20-E3-M6`, `S20-E3-M7`, `S20-E3-M8` | `S20-E4-M1`, `S20-E4-M2`, `S20-E4-M3`, `S20-E4-M4`, `S20-E4-M5`, `S21-E3-M1`, `S21-E3-M2`, `S21-E3-M3`, `S21-E3-M4` | `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/` |

**`S20-E3-D` · Dowód etapu 3: dostrajanie, RAG i ewaluacja modeli**

Mały model dostrojony metodą LoRA lub QLoRA do zadania z niszy (np. klasyfikacja zgłoszeń bezpieczeństwa lub ocena wagi znalezisk z audytu), wyeksportowany do GGUF i uruchomiony w llama.cpp, z raportem ewaluacji przed i po dostrojeniu na wydzielonym zbiorze testowym. Porównanie z wersją „prompt i RAG” bez dostrajania: RAG na pgvector z lokalnym modelem embeddingowym, chunkingiem, wyszukiwaniem hybrydowym (wektor i BM25 lub pełnotekstowe) i rerankingiem, oceniony na co najmniej 50 pytaniach z oznaczonymi właściwymi fragmentami: recall@5 i MRR dla trzech wariantów (sam wektor, hybryda, hybryda z rerankingiem).

**Na co zwrócić uwagę:** najpierw prompt i RAG, dostrajanie dopiero gdy ewaluacja pokazuje, że to nie wystarcza; rozmiar fragmentów i ich kontekst, ocena wyszukiwania osobno od oceny odpowiedzi; jakość i licencje danych treningowych; zbiór testowy rozdzielony od treningowego przed pierwszym eksperymentem; sprawdzanie regresji w zadaniach ogólnych po dostrojeniu.

**Kryterium ukończenia:** raport zawiera wyniki modelu przed i po dostrojeniu na tym samym zbiorze testowym, tabelę recall@5 i MRR dla trzech wariantów RAG na co najmniej 50 pytaniach oraz decyzję: dostrajanie, RAG czy oba, z uzasadnieniem liczbami.

**Folder roboczy:** `20-lokalne-ai-i-rozwoj-modeli/e3-dostrajanie-rag-i-ewaluacja-modeli/`

### Etap 4: Rust w ML

Opis kamienia milowego (do wklejenia):

**Cel:** Rust w ML: Candle, Burn, mistral.rs, `ort` · **Poziom po etapie:** W

**Szczególnie ważne:** kiedy wystarczy biblioteka w Ruście, a kiedy lepiej uruchomić llama.cpp jako proces poboczny; zgodność formatów (safetensors, GGUF, ONNX); akceleracja (CUDA, Metal) i jej wpływ na budowanie na trzech systemach (zob. sekcja 9); niestabilne API przed wersją 1.0.

**Dowód:** Narzędzie CLI w Ruście, które liczy embeddingi plików repozytorium (Candle lub `ort`) i odpowiada na pytania przez mistral.rs lub llama.cpp, działające offline na Linuksie i macOS. Ta sama funkcja embeddingu wystawiona do Pythona przez PyO3 i maturin, a test w `pytest` porównuje jej wyniki z referencyjną implementacją w Pythonie (np. Sentence Transformers).

| Klucz | Linear | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|---|
| `S20-E4-M1` | LEA-1076 | Przerobić: Candle: książka i przykłady | materiał | 8–10 h | 0 zł | https://huggingface.github.io/candle/, https://github.com/huggingface/candle | `S20-E3-D` | `S20-E4-D` | `20-lokalne-ai-i-rozwoj-modeli/e4-rust-w-ml/` |
| `S20-E4-M2` | LEA-1077 | Przerobić: The Burn Book | materiał, opcjonalne | 8–10 h | 0 zł | https://burn.dev/books/burn/ | `S20-E3-D` | — | `20-lokalne-ai-i-rozwoj-modeli/e4-rust-w-ml/` |
| `S20-E4-M3` | LEA-1078 | Przerobić: mistral.rs | materiał | 4–6 h | 0 zł | https://github.com/EricLBuehler/mistral.rs, https://docs.mistralrs.dev | `S20-E3-D` | `S20-E4-D` | `20-lokalne-ai-i-rozwoj-modeli/e4-rust-w-ml/` |
| `S20-E4-M4` | LEA-1079 | Przerobić: `ort`… | materiał | 4–6 h | 0 zł | https://ort.pyke.io | `S20-E3-D` | `S20-E4-D` | `20-lokalne-ai-i-rozwoj-modeli/e4-rust-w-ml/` |
| `S20-E4-M5` | LEA-1080 | Przerobić: PyO3 i maturin (wywoływanie Rusta z Pythona) | materiał | 4–6 h | 0 zł | https://pyo3.rs, https://www.maturin.rs | `S20-E3-D` | `S20-E4-D` | `20-lokalne-ai-i-rozwoj-modeli/e4-rust-w-ml/` |
| `S20-E4-D` | LEA-1082 | Dowód etapu 4: Rust w ML | dowód | — | — | — | `S20-E4-M1`, `S20-E4-M3`, `S20-E4-M4`, `S20-E4-M5` | `S20-E5-M1`, `S20-E5-M2`, `S20-E5-M3`, `S20-E5-P1`, `S20-E5-P2`, `S20-E5-P3` | `20-lokalne-ai-i-rozwoj-modeli/e4-rust-w-ml/` |

**`S20-E4-D` · Dowód etapu 4: Rust w ML**

Narzędzie CLI w Ruście, które liczy embeddingi plików repozytorium (Candle lub `ort`) i odpowiada na pytania przez mistral.rs lub llama.cpp, działające offline na Linuksie i macOS. Ta sama funkcja embeddingu wystawiona do Pythona przez PyO3 i maturin, a test w `pytest` porównuje jej wyniki z referencyjną implementacją w Pythonie (np. Sentence Transformers).

**Na co zwrócić uwagę:** kiedy wystarczy biblioteka w Ruście, a kiedy lepiej uruchomić llama.cpp jako proces poboczny; zgodność formatów (safetensors, GGUF, ONNX); akceleracja (CUDA, Metal) i jej wpływ na budowanie na trzech systemach (zob. sekcja 9); niestabilne API przed wersją 1.0.

**Kryterium ukończenia:** narzędzie działa bez sieci na Linuksie i macOS; test w `pytest` przechodzi na co najmniej 20 tekstach z podobieństwem cosinusowym do referencji co najmniej 0,99; wersje `ort` lub Candle przypięte w `Cargo.lock`.

**Folder roboczy:** `20-lokalne-ai-i-rozwoj-modeli/e4-rust-w-ml/`

### Etap 5: ekspert

Opis kamienia milowego (do wklejenia):

**Cel:** ekspert: modele lokalne w pracy z klientem, aktualność · **Poziom po etapie:** E

**Dowód poziomu E:** Samodzielnie, bez agenta, w 1 dzień dobierasz model lokalny do zadania i sprzętu, oceniasz go na własnym zestawie ewaluacji względem modelu w chmurze i podłączasz do przepływu recenzji tak, że kod klienta nie opuszcza maszyny, a decyzję zapisujesz w ADR.

| Klucz | Linear | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|---|
| `S20-E5-M1` | LEA-1096 | Przerobić: Informacje o wydaniach llama.cpp, Ollama, ONNX Runtime, mistral.rs, MLX | materiał | ok. 0,5 h tygodniowo | 0 zł | https://github.com/ggml-org/llama.cpp/releases | `S20-E4-D` | `S20-E5-D` | `20-lokalne-ai-i-rozwoj-modeli/e5-ekspert/` |
| `S20-E5-M2` | LEA-1099 | Przerobić: Blog i dokumentacja Hugging Face (nowe modele z otwartymi wagami, karty modeli) | materiał | ok. 0,5 h tygodniowo | 0 zł | https://huggingface.co/blog | `S20-E4-D` | `S20-E5-D` | `20-lokalne-ai-i-rozwoj-modeli/e5-ekspert/` |
| `S20-E5-M3` | LEA-1101 | Przerobić: Practical Deep Learning for Coders, część 2 (od podstaw do Stable Diffusion) | materiał, opcjonalne | wg potrzeb | 0 zł | https://course.fast.ai | `S20-E4-D` | — | `20-lokalne-ai-i-rozwoj-modeli/e5-ekspert/` |
| `S20-E5-P1` | LEA-1102 | Praktyka: modele lokalne w pracy z klientem | praktyka | — | — | — | `S20-E4-D` | `S20-E5-D` | `20-lokalne-ai-i-rozwoj-modeli/e5-ekspert/` |
| `S20-E5-P2` | LEA-1103 | Praktyka: przegląd co kwartał | praktyka | — | — | — | `S20-E4-D` | `S20-E5-D` | `20-lokalne-ai-i-rozwoj-modeli/e5-ekspert/` |
| `S20-E5-P3` | LEA-1104 | Praktyka: podatności środowisk uruchomieniowych | praktyka | — | — | — | `S20-E4-D` | `S20-E5-D` | `20-lokalne-ai-i-rozwoj-modeli/e5-ekspert/` |
| `S20-E5-D` | LEA-1108 | Dowód poziomu E: ekspert | dowód | — | — | — | `S20-E5-M1`, `S20-E5-M2`, `S20-E5-P1`, `S20-E5-P2`, `S20-E5-P3` | — | `20-lokalne-ai-i-rozwoj-modeli/e5-ekspert/` |

**`S20-E5-P1` · Praktyka: modele lokalne w pracy z klientem**

Stały przepływ, w którym kod objęty umową poufności jest analizowany wyłącznie lokalnie, z zapisem w umowie i w ofercie.

Praktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, a nie po jednorazowym wykonaniu.

**Folder roboczy:** `20-lokalne-ai-i-rozwoj-modeli/e5-ekspert/`

**`S20-E5-P2` · Praktyka: przegląd co kwartał**

Porównanie nowych modeli z otwartymi wagami na własnym zestawie ewaluacji (zob. sekcja 11) i decyzja o wymianie.

Praktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, a nie po jednorazowym wykonaniu.

**Folder roboczy:** `20-lokalne-ai-i-rozwoj-modeli/e5-ekspert/`

**`S20-E5-P3` · Praktyka: podatności środowisk uruchomieniowych**

Llama.cpp, ONNX Runtime i biblioteki tokenizerów objęte tym samym procesem obsługi podatności co reszta zależności (zob. sekcja 10).

Praktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, a nie po jednorazowym wykonaniu.

**Folder roboczy:** `20-lokalne-ai-i-rozwoj-modeli/e5-ekspert/`

**`S20-E5-D` · Dowód poziomu E: ekspert**

Samodzielnie, bez agenta, w 1 dzień dobierasz model lokalny do zadania i sprzętu, oceniasz go na własnym zestawie ewaluacji względem modelu w chmurze i podłączasz do przepływu recenzji tak, że kod klienta nie opuszcza maszyny, a decyzję zapisujesz w ADR.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki. Bez agenta AI.

**Folder roboczy:** `20-lokalne-ai-i-rozwoj-modeli/e5-ekspert/`

## 6. Relacje z innymi projektami

**Wchodzące** (zadanie z innego projektu blokuje zadanie tego projektu):

- `S01-E1-D` (Dowód etapu 1: codzienna praca z Claude Code) → `S20-START`
- `S06-E1-D` (Dowód etapu 1: projektowanie testów i TDD) → `S20-START`
- `S10-E1-D` (Dowód etapu 1: ataki na web i API w praktyce) → `S20-START`
- `S12-E2-D` (Dowód etapu 2: własność, pożyczanie, czasy życia) → `S20-START`
- `S02-E3-D` (Dowód etapu 3: Python) → `S20-E1-M1`
- `S02-E3-D` (Dowód etapu 3: Python) → `S20-E1-M2`
- `S02-E3-D` (Dowód etapu 3: Python) → `S20-E1-M3`

**Wychodzące** (zadanie tego projektu blokuje zadanie w innym projekcie):

- `S20-E0-D` → `S11-E6-M1` (11. Weryfikacja pracy AI i budowa procesu)
- `S20-E0-D` → `S11-E6-M2` (11. Weryfikacja pracy AI i budowa procesu)
- `S20-E0-D` → `S11-E6-M3` (11. Weryfikacja pracy AI i budowa procesu)
- `S20-E0-D` → `S11-E6-M4` (11. Weryfikacja pracy AI i budowa procesu)
- `S20-E0-D` → `S11-E6-P1` (11. Weryfikacja pracy AI i budowa procesu)
- `S20-E0-D` → `S11-E6-P2` (11. Weryfikacja pracy AI i budowa procesu)
- `S20-E0-D` → `S11-E6-P3` (11. Weryfikacja pracy AI i budowa procesu)
- `S20-E0-D` → `S11-E6-P4` (11. Weryfikacja pracy AI i budowa procesu)
- `S20-E0-D` → `S21-START` (21. Funkcje AI w aplikacjach)
- `S20-E3-D` → `S21-E3-M1` (21. Funkcje AI w aplikacjach)
- `S20-E3-D` → `S21-E3-M2` (21. Funkcje AI w aplikacjach)
- `S20-E3-D` → `S21-E3-M3` (21. Funkcje AI w aplikacjach)
- `S20-E3-D` → `S21-E3-M4` (21. Funkcje AI w aplikacjach)
