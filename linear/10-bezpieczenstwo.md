# 10. Bezpieczeństwo: plan wdrożenia w Linear

Team **LEA** (https://linear.app/daankh/team/LEA/overview). Plan do przeglądu przed wdrożeniem: nic nie zostało jeszcze utworzone w Linear. Klucze zadań (np. `S10-E0-M1`) są robocze; po wdrożeniu dostaną identyfikatory `LEA-…`.

**W skrócie:** 9 kamieni milowych, 57 zadań (1 start, 43 materiały, 9 dowodów, 4 praktyki). Plik główny z kolejnością projektów: `00-kolejnosc-i-zaleznosci.md`.

## 1. Projekt

| Pole | Wartość |
|---|---|
| Nazwa | 10. Bezpieczeństwo |
| Team | LEA |
| Podsumowanie (pole „Summary”) | Warstwa 3: ochrona i kontrola. Opiera się na: 3, 4, 5, 8 i 9; etap Rust i desktop także na 12 i 14, a etap ekspercki na 11. Jest podstawą: 11, 20, 21 i 22 oraz publikacji w 18 i 19. |
| Etykiety projektu | `warstwa-3` |
| Blokowany przez (projekty) | 03. Frontend web, 04. Bazy danych i dane, 05. Backend i API, 08. Architektura i projektowanie systemów, 09. DevOps, CI/CD i wydania |
| Blokuje (projekty) | 11. Weryfikacja pracy AI i budowa procesu, 20. Lokalne AI i rozwój modeli, 21. Funkcje AI w aplikacjach, 22. Systemy wbudowane |
| Zależności częściowe (wchodzące) | etap 7 czeka na 12. Rust jako wspólny fundament (etap 5); etap 7 czeka na 14. Desktop: wspólne (etap 1); etap 8 czeka na 11. Weryfikacja pracy AI i budowa procesu (etap 2) |
| Zależności częściowe (wychodzące) | 11. Weryfikacja pracy AI i budowa procesu, etap 4; 18. Android, etap 5; 19. iOS, etap 5 |

### Opis projektu (do wklejenia w Linear)

*Warstwa 3: ochrona i kontrola. Opiera się na: 3, 4, 5, 8 i 9; etap Rust i desktop także na 12 i 14, a etap ekspercki na 11. Jest podstawą: 11, 20, 21 i 22 oraz publikacji w 18 i 19.*

**Zakres umiejętności**

- Web i API: OWASP ASVS (poziom 1 i wybrane wymagania poziomu 2), OWASP Top 10 i API Top 10, nagłówki bezpieczeństwa, CSP.
- Uwierzytelnianie i autoryzacja: OAuth 2.0 i OpenID Connect (RFC 9700), passkeys (WebAuthn), przechowywanie haseł (Argon2id), sesje.
- Kryptografia stosowana: TLS, szyfrowanie danych, zarządzanie kluczami i sekretami (KMS, rotacja).
- Rust i desktop (Tauri): przegląd kodu `unsafe`, zakres capabilities, walidacja wejścia w poleceniach IPC, podpis aktualizacji.
- Chmura i infrastruktura jako kod: błędne konfiguracje, uprawnienia IAM, skanowanie Terraform i Dockerfile.
- Łańcuch dostaw: SBOM w CycloneDX (`cargo-cyclonedx`, `cargo-auditable`, narzędzia dla npm), `cargo-audit`, `cargo-deny`, `cargo-vet`, `osv-scanner`, Dependabot lub Renovate; pochodzenie zależności i artefaktów (SLSA, Sigstore, provenance w npm); priorytety według CVSS, EPSS i KEV.
- Narzędzia: gitleaks, Semgrep, CodeQL, OWASP ZAP; `cargo-geiger` do mapy kodu `unsafe`.
- Modelowanie zagrożeń STRIDE i LINDDUN dla każdej klasy aplikacji.
- Logowanie zdarzeń bezpieczeństwa, reagowanie na incydenty, obowiązki zgłoszeniowe z CRA i NIS2.
- Ryzyka specyficzne dla AI: zależności wymyślone przez model i podszywające się pod nie pakiety (typosquatting), prompt injection w treściach z repozytorium, agenci bez poświadczeń produkcyjnych.

Bezpieczeństwo aplikacji mobilnych (OWASP MASVS i MASTG) jest w sekcji 18, a bezpieczeństwo firmware (secure boot, podpis, ochrona kluczy) w sekcji 22.

**Ścieżka nauki**

Ścieżka ma 9 etapów. Każdy kończy się **dowodem**, czyli małym projektem, który pokazuje, że etap jest opanowany. Dowody odpowiadają usługom z biznesplanu: audyt według ASVS, model zagrożeń, triage podatności i zgłoszenie w trybie CRA. Przy doświadczeniu seniorskim etap 0 można zaliczyć samym dowodem, ale etapy 2, 5 i 6 warto przejść w całości, bo to rdzeń niszy „rescue & hardening”. Ceny materiałów płatnych zmieniają się, więc warto je sprawdzić przed zakupem. Ściągawki OWASP o XSS, CSP i sesjach są w sekcji 3 (etap 6), testy w sekcji 6, bramki CI w sekcji 9, a podpisywanie i atestacje własnych wydań w sekcji 9 (etap 5).

**Definicja ukończenia projektu (dowód poziomu E)**

Samodzielnie, bez agenta, w 2 dni przeprowadzasz audyt nieznanej aplikacji (web z API albo desktop Tauri z rdzeniem w Ruście): status każdego wymagania ASVS L1, model zagrożeń STRIDE, SBOM z triage’em podatności i ocena obowiązków z CRA. Znajdujesz co najmniej jeden błąd kontroli dostępu lub łańcucha dostaw, którego nie zgłosiły Semgrep, CodeQL, ZAP ani `cargo-audit`, potwierdzony testem lub PoC, i przedstawiasz klientowi raport z planem naprawy uszeregowanym według ryzyka.

**Źródło:** dokument „Umiejętności techniczne” w projekcie „JDG: Rozwój oprogramowania”, sekcja 10.

## 2. Kamienie milowe

Jeden kamień milowy na etap ścieżki. Kamień milowy jest zamknięty, gdy zamknięte jest zadanie dowodu tego etapu.

| # | Kamień milowy | Cel | Poziom po etapie | Zadania |
|---|---|---|---|---|
| 1 | Etap 0: podstawy bezpieczeństwa aplikacji | podstawy bezpieczeństwa aplikacji i bezpiecznego kodowania | podstawy | 4 |
| 2 | Etap 1: ataki na web i API w praktyce | ataki na web i API w praktyce | W | 4 |
| 3 | Etap 2: standardy i audyt | standardy i audyt: ASVS, Top 10, API Top 10 | E | 7 |
| 4 | Etap 3: modelowanie zagrożeń | modelowanie zagrożeń: STRIDE i LINDDUN | W | 4 |
| 5 | Etap 4: narzędzia SAST, DAST i wykrywanie sekretów | narzędzia: SAST, DAST, wykrywanie sekretów | W | 7 |
| 6 | Etap 5: łańcuch dostaw i SBOM | łańcuch dostaw: SBOM, zależności, `cargo-vet` | E | 7 |
| 7 | Etap 6: obsługa podatności i CRA | obsługa podatności i CRA: CVSS, EPSS, KEV, zgłoszenia | E | 11 |
| 8 | Etap 7: Rust i desktop (Tauri) | Rust i desktop: `unsafe`, narzędzia Rusta, Tauri (IPC, capabilities, aktualizacje) | W | 4 |
| 9 | Etap 8: ekspert | ekspert: audyty klientów, badania, aktualność | E | 8 |

## 3. Punkt startu

Zadanie **`S10-START` · Start: 10. Bezpieczeństwo** to jedyne wejście do projektu: wszystkie zadania pierwszego etapu są przez nie blokowane.

- **Blokowane przez:** `S03-E2-D`, `S04-E1-D`, `S05-E1-D`, `S08-E1-D`, `S09-E2-D`
- **Odblokowuje:** `S10-E0-M1`, `S10-E0-M2`, `S10-E0-M3`
- **Status początkowy:** Backlog do czasu zamknięcia zadań blokujących, potem Todo

Opis zadania (do wklejenia):

Punkt startu projektu „10. Bezpieczeństwo”.

**Warunki wejścia (zadania blokujące):**

- `S03-E2-D` · Dowód etapu 2: TypeScript — sekcja 3 na poziomie podstawowym do pracy (etap 2)
- `S04-E1-D` · Dowód etapu 1: PostgreSQL w praktyce — sekcja 4 na poziomie podstawowym do pracy (etap 1)
- `S05-E1-D` · Dowód etapu 1: Node.js po stronie serwera — sekcja 5 na poziomie podstawowym do pracy (etap 1)
- `S08-E1-D` · Dowód etapu 1: style architektoniczne, atrybuty jakości i kompromisy — sekcja 8 na poziomie podstawowym do pracy (etap 1)
- `S09-E2-D` · Dowód etapu 2: GitHub Actions i bezpieczeństwo pipeline’u — sekcja 9 na poziomie podstawowym do pracy (etap 2)

**Do zrobienia:**

- przeczytać sekcję 10 dokumentu „Umiejętności techniczne”,
- zaznaczyć etapy, które zaliczasz samym dowodem (zgodnie z akapitem wstępnym ścieżki), i dla nich zamknąć zadania materiałów jako niepotrzebne.

**Folder roboczy:** `10-bezpieczenstwo/`

## 4. Przepływ zależności

Linie ciągłe to zależności wewnątrz projektu, przerywane to zadania z innych projektów. Wewnątrz etapu zadania materiałów są równoległe i wszystkie blokują dowód etapu; dowód etapu blokuje materiały kolejnego etapu.

```mermaid
flowchart TD
  START["10. Start"]
  E0["Etap 0: podstawy bezpieczeństwa aplikacji"]
  E1["Etap 1: ataki na web i API w praktyce"]
  E2["Etap 2: standardy i audyt"]
  E3["Etap 3: modelowanie zagrożeń"]
  E4["Etap 4: narzędzia SAST, DAST i wykrywanie sekretów"]
  E5["Etap 5: łańcuch dostaw i SBOM"]
  E6["Etap 6: obsługa podatności i CRA"]
  E7["Etap 7: Rust i desktop (Tauri)"]
  E8["Etap 8: ekspert"]
  START --> E0
  E0 --> E1
  E1 --> E2
  E2 --> E3
  E3 --> E4
  E4 --> E5
  E5 --> E6
  E6 --> E7
  XS12E5D(["S12-E5-D"]) -.-> E7
  XS14E1D(["S14-E1-D"]) -.-> E7
  E6 --> E8
  E7 --> E8
  XS11E2D(["S11-E2-D"]) -.-> E8
  XS03E2D(["S03-E2-D"]) -.-> START
  XS04E1D(["S04-E1-D"]) -.-> START
  XS05E1D(["S05-E1-D"]) -.-> START
  XS08E1D(["S08-E1-D"]) -.-> START
  XS09E2D(["S09-E2-D"]) -.-> START
```

## 5. Zadania według kamieni milowych

Szablon opisu zadania materiału: nazwa materiału, autor lub wydawca, typ, czas, koszt i link (jak w kolumnach poniżej), zdanie „Gotowe, gdy materiał jest przerobiony w zakresie potrzebnym do dowodu etapu” oraz folder roboczy z kolumny „Folder”. Opisy dowodów i praktyk są podane pod tabelą każdego etapu.

### Etap 0: podstawy bezpieczeństwa aplikacji

Opis kamienia milowego (do wklejenia):

**Cel:** podstawy bezpieczeństwa aplikacji i bezpiecznego kodowania · **Poziom po etapie:** podstawy

**Szczególnie ważne:** zasada najmniejszych uprawnień, obrona warstwowa, walidacja wejścia i kodowanie wyjścia, bezpieczne wartości domyślne, zarządzanie sekretami, różnica między uwierzytelnianiem a autoryzacją.

Wystarczy jedna z dwóch książek Tanyi Janki: „Secure Coding” przy doświadczeniu programistycznym (obowiązkowa), „Application Security” tylko przy starcie od zera (opcjonalna).

**Dowód:** Certyfikat ukończenia LFD121 oraz lista 15 typowych błędów bezpieczeństwa w kodzie generowanym przez AI, każdy z przykładem w TypeScript lub Ruście, poprawką i odesłaniem do kategorii CWE.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|
| `S10-E0-M1` | Przerobić: Developing Secure Software (LFD121) | materiał | 14–18 h | 0 zł | https://openssf.org/training/courses/ | `S10-START` | `S10-E0-D` | `10-bezpieczenstwo/e0-podstawy-bezpieczenstwa-aplikacji/` |
| `S10-E0-M2` | Przerobić: Alice and Bob Learn Application Security… | materiał, płatny, opcjonalne | 12–15 h | płatna | https://shehackspurple.ca/books/ | `S10-START` | — | `10-bezpieczenstwo/e0-podstawy-bezpieczenstwa-aplikacji/` |
| `S10-E0-M3` | Przerobić: Alice and Bob Learn Secure Coding (Wiley 2025) | materiał, płatny | 12–15 h | płatna | https://shehackspurple.ca/books/ | `S10-START` | `S10-E0-D` | `10-bezpieczenstwo/e0-podstawy-bezpieczenstwa-aplikacji/` |
| `S10-E0-D` | Dowód etapu 0: podstawy bezpieczeństwa aplikacji | dowód | — | — | — | `S10-E0-M1`, `S10-E0-M3` | `S10-E1-M1`, `S10-E1-M2`, `S10-E1-M3` | `10-bezpieczenstwo/e0-podstawy-bezpieczenstwa-aplikacji/` |

**`S10-E0-D` · Dowód etapu 0: podstawy bezpieczeństwa aplikacji**

Certyfikat ukończenia LFD121 oraz lista 15 typowych błędów bezpieczeństwa w kodzie generowanym przez AI, każdy z przykładem w TypeScript lub Ruście, poprawką i odesłaniem do kategorii CWE.

**Na co zwrócić uwagę:** zasada najmniejszych uprawnień, obrona warstwowa, walidacja wejścia i kodowanie wyjścia, bezpieczne wartości domyślne, zarządzanie sekretami, różnica między uwierzytelnianiem a autoryzacją.

**Kryterium ukończenia:** certyfikat LFD121 w repozytorium; 15 błędów, każdy z identyfikatorem CWE, kodem podatnym i poprawionym; dla co najmniej 5 z nich test, który nie przechodzi na kodzie podatnym i przechodzi po poprawce.

**Folder roboczy:** `10-bezpieczenstwo/e0-podstawy-bezpieczenstwa-aplikacji/`

### Etap 1: ataki na web i API w praktyce

Opis kamienia milowego (do wklejenia):

**Cel:** ataki na web i API w praktyce · **Poziom po etapie:** W

**Szczególnie ważne:** kontrola dostępu do obiektów (IDOR, BOLA), SSRF, wstrzyknięcia (SQL, polecenia systemowe, szablony), XSS i CSRF, błędy logiki biznesowej, ataki na OAuth i JWT, wyścigi (race conditions); w laboratoriach PortSwigger przede wszystkim kategorie „Access control”, „Authentication”, „SSRF” i „Business logic vulnerabilities”.

**Dowód:** 30 rozwiązanych laboratoriów Web Security Academy (w tym co najmniej 10 na poziomie „Practitioner”) i 40 wyzwań Juice Shop; dla 5 z nich notatka: przyczyna w kodzie, poprawka i test regresyjny.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|
| `S10-E1-M1` | Przerobić: Web Security Academy (ścieżki nauki i laboratoria) | materiał | 50–60 h | 0 zł | https://portswigger.net/web-security | `S10-E0-D` | `S10-E1-D` | `10-bezpieczenstwo/e1-ataki-na-web-i-api-w-praktyce/` |
| `S10-E1-M2` | Przerobić: OWASP Juice Shop i przewodnik „Pwning OWASP Juice Shop” | materiał | 15–20 h | 0 zł | https://owasp.org/www-project-juice-shop/, https://pwning.owasp-juice.shop | `S10-E0-D` | `S10-E1-D` | `10-bezpieczenstwo/e1-ataki-na-web-i-api-w-praktyce/` |
| `S10-E1-M3` | Przerobić: Real-World Bug Hunting: A Field Guide to Web Hacking | materiał, płatny | 10–12 h | płatna | https://nostarch.com/bughunting | `S10-E0-D` | `S10-E1-D` | `10-bezpieczenstwo/e1-ataki-na-web-i-api-w-praktyce/` |
| `S10-E1-D` | Dowód etapu 1: ataki na web i API w praktyce | dowód | — | — | — | `S10-E1-M1`, `S10-E1-M2`, `S10-E1-M3` | `S10-E2-M1`, `S10-E2-M2`, `S10-E2-M3`, `S10-E2-M4`, `S10-E2-M5`, `S10-E2-M6`, `S11-START`, `S20-START`, `S21-START`, `S22-START` | `10-bezpieczenstwo/e1-ataki-na-web-i-api-w-praktyce/` |

**`S10-E1-D` · Dowód etapu 1: ataki na web i API w praktyce**

30 rozwiązanych laboratoriów Web Security Academy (w tym co najmniej 10 na poziomie „Practitioner”) i 40 wyzwań Juice Shop; dla 5 z nich notatka: przyczyna w kodzie, poprawka i test regresyjny.

**Na co zwrócić uwagę:** kontrola dostępu do obiektów (IDOR, BOLA), SSRF, wstrzyknięcia (SQL, polecenia systemowe, szablony), XSS i CSRF, błędy logiki biznesowej, ataki na OAuth i JWT, wyścigi (race conditions); w laboratoriach PortSwigger przede wszystkim kategorie „Access control”, „Authentication”, „SSRF” i „Business logic vulnerabilities”.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki.

**Folder roboczy:** `10-bezpieczenstwo/e1-ataki-na-web-i-api-w-praktyce/`

### Etap 2: standardy i audyt

Opis kamienia milowego (do wklejenia):

**Cel:** standardy i audyt: ASVS, Top 10, API Top 10 · **Poziom po etapie:** E

**Szczególnie ważne:** ASVS 5.0 ma inną numerację niż 4.0.3, więc raporty i listy kontrolne oparte na starej wersji trzeba przemapować. W Top 10:2025 pojawiły się nowe kategorie „Software Supply Chain Failures” (A03) i „Mishandling of Exceptional Conditions” (A10), a kontrola dostępu nadal jest na pierwszym miejscu. Uwierzytelnianie: przepływ Authorization Code z PKCE zamiast Implicit, dokładne dopasowanie `redirect_uri`, walidacja `iss`, `aud` i `nonce` w tokenie ID, passkeys jako metoda odporna na phishing. Kryptografia: Argon2id do haseł, TLS 1.2+ z HSTS, klucze w KMS lub menedżerze sekretów z rotacją, nigdy własne algorytmy.

**Dowód:** Raport z audytu przykładowej aplikacji Next.js z Supabase (np. własnej z sekcji 3 albo aplikacji z vibe codingu) według ASVS L1 i wybranych wymagań L2: tabela wymagań ze statusem (spełnione, niespełnione, nie dotyczy), dowody (zrzuty, żądania, fragmenty kodu), priorytety i plan naprawy zrozumiały dla klienta nietechnicznego; osobna część o uwierzytelnianiu (hasła, sesje, OAuth/OIDC, passkeys) i kryptografii (TLS, przechowywanie haseł, sekrety i klucze).

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|
| `S10-E2-M1` | Przerobić: OWASP ASVS 5.0.0 (wydanie z 30 maja 2025 r., poziomy L1–L3) | materiał | 20–25 h | 0 zł | https://owasp.org/www-project-application-security-verification-standard/, https://github.com/OWASP/ASVS | `S10-E1-D` | `S10-E2-D` | `10-bezpieczenstwo/e2-standardy-i-audyt/` |
| `S10-E2-M2` | Przerobić: OWASP Top 10:2025 | materiał | 5–6 h | 0 zł | https://top10.owasp.org/2025/ | `S10-E1-D` | `S10-E2-D` | `10-bezpieczenstwo/e2-standardy-i-audyt/` |
| `S10-E2-M3` | Przerobić: OWASP API Security Top 10 (edycja 2023) | materiał | 4–5 h | 0 zł | https://api-security.owasp.org | `S10-E1-D` | `S10-E2-D` | `10-bezpieczenstwo/e2-standardy-i-audyt/` |
| `S10-E2-M4` | Przerobić: OAuth 2.0 Security Best Current Practice (RFC 9700), OpenID Connect: „How OpenID Connect Works” i… | materiał | 5–6 h | 0 zł | https://www.rfc-editor.org/rfc/rfc9700, https://openid.net/developers/how-connect-works/, https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html | `S10-E1-D` | `S10-E2-D` | `10-bezpieczenstwo/e2-standardy-i-audyt/` |
| `S10-E2-M5` | Przerobić: Passkeys i uwierzytelnianie: passkeys.dev, NIST SP 800-63B-4, OWASP Authentication Cheat Sheet | materiał | 5–6 h | 0 zł | https://passkeys.dev/docs/, https://pages.nist.gov/800-63-4/sp800-63b.html, https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | `S10-E1-D` | `S10-E2-D` | `10-bezpieczenstwo/e2-standardy-i-audyt/` |
| `S10-E2-M6` | Przerobić: Kryptografia stosowana: OWASP Cheat Sheets „Password Storage”, „Cryptographic Storage”… | materiał | 5–6 h | 0 zł | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html, https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html, https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html, https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html | `S10-E1-D` | `S10-E2-D` | `10-bezpieczenstwo/e2-standardy-i-audyt/` |
| `S10-E2-D` | Dowód etapu 2: standardy i audyt | dowód | — | — | — | `S10-E2-M1`, `S10-E2-M2`, `S10-E2-M3`, `S10-E2-M4`, `S10-E2-M5`, `S10-E2-M6` | `S10-E3-M1`, `S10-E3-M2`, `S10-E3-M3` | `10-bezpieczenstwo/e2-standardy-i-audyt/` |

**`S10-E2-D` · Dowód etapu 2: standardy i audyt**

Raport z audytu przykładowej aplikacji Next.js z Supabase (np. własnej z sekcji 3 albo aplikacji z vibe codingu) według ASVS L1 i wybranych wymagań L2: tabela wymagań ze statusem (spełnione, niespełnione, nie dotyczy), dowody (zrzuty, żądania, fragmenty kodu), priorytety i plan naprawy zrozumiały dla klienta nietechnicznego; osobna część o uwierzytelnianiu (hasła, sesje, OAuth/OIDC, passkeys) i kryptografii (TLS, przechowywanie haseł, sekrety i klucze).

**Na co zwrócić uwagę:** ASVS 5.0 ma inną numerację niż 4.0.3, więc raporty i listy kontrolne oparte na starej wersji trzeba przemapować. W Top 10:2025 pojawiły się nowe kategorie „Software Supply Chain Failures” (A03) i „Mishandling of Exceptional Conditions” (A10), a kontrola dostępu nadal jest na pierwszym miejscu. Uwierzytelnianie: przepływ Authorization Code z PKCE zamiast Implicit, dokładne dopasowanie `redirect_uri`, walidacja `iss`, `aud` i `nonce` w tokenie ID, passkeys jako metoda odporna na phishing. Kryptografia: Argon2id do haseł, TLS 1.2+ z HSTS, klucze w KMS lub menedżerze sekretów z rotacją, nigdy własne algorytmy.

**Kryterium ukończenia:** status przy każdym wymaganiu L1 z rozdziałów o uwierzytelnianiu, sesjach, autoryzacji, OAuth, kryptografii i komunikacji; każde niespełnione wymaganie ma dowód i priorytet; raport ocenia konfigurację TLS (np. wynikiem `testssl.sh`) i sposób przechowywania haseł.

**Folder roboczy:** `10-bezpieczenstwo/e2-standardy-i-audyt/`

### Etap 3: modelowanie zagrożeń

Opis kamienia milowego (do wklejenia):

**Cel:** modelowanie zagrożeń: STRIDE i LINDDUN · **Poziom po etapie:** W

**Szczególnie ważne:** diagram przepływu danych z granicami zaufania, STRIDE dla każdego elementu diagramu, LINDDUN dla danych osobowych (spójność z RODO), zagrożenia wprowadzone przez agentów AI i integracje LLM (zob. sekcja 11, etap 4).

Wydanie 2 książki Shostacka („Threat Modeling: Designing for Security in an AI World”) jest zapowiedziane na luty 2027 r.; do tego czasu podstawą jest wydanie 1.

**Dowód:** Model zagrożeń STRIDE i LINDDUN dla przejmowanej aplikacji klienta przygotowany w 1 dzień: diagram, lista zagrożeń z oceną ryzyka, środki zaradcze przypisane do zadań i decyzje zapisane w ADR.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|
| `S10-E3-M1` | Przerobić: Threat Modeling: Designing for Security (wydanie 1, Wiley 2014) | materiał, płatny | 15–20 h | płatna | https://shostack.org/books/threat-modeling-book | `S10-E2-D` | `S10-E3-D` | `10-bezpieczenstwo/e3-modelowanie-zagrozen/` |
| `S10-E3-M2` | Przerobić: Threat Modeling Manifesto | materiał | 1 h | 0 zł | https://www.threatmodelingmanifesto.org | `S10-E2-D` | `S10-E3-D` | `10-bezpieczenstwo/e3-modelowanie-zagrozen/` |
| `S10-E3-M3` | Przerobić: LINDDUN (wariant uproszczony GO i szczegółowy PRO) | materiał | 6–8 h | 0 zł | https://linddun.org | `S10-E2-D` | `S10-E3-D` | `10-bezpieczenstwo/e3-modelowanie-zagrozen/` |
| `S10-E3-D` | Dowód etapu 3: modelowanie zagrożeń | dowód | — | — | — | `S10-E3-M1`, `S10-E3-M2`, `S10-E3-M3` | `S10-E4-M1`, `S10-E4-M2`, `S10-E4-M3`, `S10-E4-M4`, `S10-E4-M5`, `S10-E4-M6`, `S11-E4-M1`, `S11-E4-M2`, `S11-E4-M3`, `S11-E4-M4` | `10-bezpieczenstwo/e3-modelowanie-zagrozen/` |

**`S10-E3-D` · Dowód etapu 3: modelowanie zagrożeń**

Model zagrożeń STRIDE i LINDDUN dla przejmowanej aplikacji klienta przygotowany w 1 dzień: diagram, lista zagrożeń z oceną ryzyka, środki zaradcze przypisane do zadań i decyzje zapisane w ADR.

**Na co zwrócić uwagę:** diagram przepływu danych z granicami zaufania, STRIDE dla każdego elementu diagramu, LINDDUN dla danych osobowych (spójność z RODO), zagrożenia wprowadzone przez agentów AI i integracje LLM (zob. sekcja 11, etap 4).

**Kryterium ukończenia:** diagram przepływu danych z granicami zaufania; co najmniej 20 zagrożeń, każde z kategorią STRIDE lub LINDDUN, oceną ryzyka i właścicielem; każde zagrożenie wysokiego ryzyka ma zadanie albo ADR z akceptacją ryzyka.

**Folder roboczy:** `10-bezpieczenstwo/e3-modelowanie-zagrozen/`

### Etap 4: narzędzia SAST, DAST i wykrywanie sekretów

Opis kamienia milowego (do wklejenia):

**Cel:** narzędzia: SAST, DAST, wykrywanie sekretów · **Poziom po etapie:** W

**Szczególnie ważne:** odróżnianie fałszywych alarmów od prawdziwych błędów, własne reguły dla wzorców typowych dla kodu z AI (brak autoryzacji w Server Actions, klucz `service_role` Supabase po stronie klienta, `NEXT_PUBLIC_*` z sekretem), skanowanie DAST z zalogowanym użytkownikiem, przegląd całej historii git pod kątem sekretów i ich rotacja; w infrastrukturze: publiczne buckety, zbyt szerokie role IAM, sekrety w stanie Terraform, kontenery uruchamiane jako root.

**Dowód:** Zestaw 5 własnych reguł Semgrep z testami, każda wykrywająca błąd znaleziony w etapie 2; skan ZAP z uwierzytelnieniem uruchamiany w CI (zob. sekcja 9); raport gitleaks z historii repozytorium z planem rotacji kluczy; skan Trivy konfiguracji Terraform i Dockerfile własnej usługi w CI.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|
| `S10-E4-M1` | Przerobić: Semgrep: dokumentacja, w tym pisanie własnych reguł | materiał | 8–10 h | 0 zł (wersja społecznościowa) | https://semgrep.dev/docs | `S10-E3-D` | `S10-E4-D` | `10-bezpieczenstwo/e4-narzedzia-sast-dast-i-wykrywanie-sekretow/` |
| `S10-E4-M2` | Przerobić: CodeQL: dokumentacja i „Learn to write CodeQL” | materiał | 8–10 h | 0 zł dla repozytoriów publicznych | https://codeql.github.com/docs/ | `S10-E3-D` | `S10-E4-D` | `10-bezpieczenstwo/e4-narzedzia-sast-dast-i-wykrywanie-sekretow/` |
| `S10-E4-M3` | Przerobić: ZAP: Getting Started, Automation Framework, uwierzytelnianie | materiał | 8–10 h | 0 zł | https://www.zaproxy.org/docs/ | `S10-E3-D` | `S10-E4-D` | `10-bezpieczenstwo/e4-narzedzia-sast-dast-i-wykrywanie-sekretow/` |
| `S10-E4-M4` | Przerobić: gitleaks | materiał | 2–3 h | 0 zł | https://github.com/gitleaks/gitleaks | `S10-E3-D` | `S10-E4-D` | `10-bezpieczenstwo/e4-narzedzia-sast-dast-i-wykrywanie-sekretow/` |
| `S10-E4-M5` | Przerobić: OWASP Cheat Sheets „Infrastructure as Code Security” i „Secure Cloud Architecture” | materiał | 3–4 h | 0 zł | https://cheatsheetseries.owasp.org/cheatsheets/Infrastructure_as_Code_Security_Cheat_Sheet.html, https://cheatsheetseries.owasp.org/cheatsheets/Secure_Cloud_Architecture_Cheat_Sheet.html | `S10-E3-D` | `S10-E4-D` | `10-bezpieczenstwo/e4-narzedzia-sast-dast-i-wykrywanie-sekretow/` |
| `S10-E4-M6` | Przerobić: Trivy: skanowanie błędnych konfiguracji (Terraform, Dockerfile, Kubernetes) | materiał | 2–3 h | 0 zł | https://trivy.dev/latest/docs/scanner/misconfiguration/ | `S10-E3-D` | `S10-E4-D` | `10-bezpieczenstwo/e4-narzedzia-sast-dast-i-wykrywanie-sekretow/` |
| `S10-E4-D` | Dowód etapu 4: narzędzia SAST, DAST i wykrywanie sekretów | dowód | — | — | — | `S10-E4-M1`, `S10-E4-M2`, `S10-E4-M3`, `S10-E4-M4`, `S10-E4-M5`, `S10-E4-M6` | `S10-E5-M1`, `S10-E5-M2`, `S10-E5-M3`, `S10-E5-M4`, `S10-E5-M5`, `S10-E5-M6` | `10-bezpieczenstwo/e4-narzedzia-sast-dast-i-wykrywanie-sekretow/` |

**`S10-E4-D` · Dowód etapu 4: narzędzia SAST, DAST i wykrywanie sekretów**

Zestaw 5 własnych reguł Semgrep z testami, każda wykrywająca błąd znaleziony w etapie 2; skan ZAP z uwierzytelnieniem uruchamiany w CI (zob. sekcja 9); raport gitleaks z historii repozytorium z planem rotacji kluczy; skan Trivy konfiguracji Terraform i Dockerfile własnej usługi w CI.

**Na co zwrócić uwagę:** odróżnianie fałszywych alarmów od prawdziwych błędów, własne reguły dla wzorców typowych dla kodu z AI (brak autoryzacji w Server Actions, klucz `service_role` Supabase po stronie klienta, `NEXT_PUBLIC_*` z sekretem), skanowanie DAST z zalogowanym użytkownikiem, przegląd całej historii git pod kątem sekretów i ich rotacja; w infrastrukturze: publiczne buckety, zbyt szerokie role IAM, sekrety w stanie Terraform, kontenery uruchamiane jako root.

**Kryterium ukończenia:** 5 reguł z testami (`semgrep --test` przechodzi); ZAP w CI loguje się i skanuje strony za logowaniem; każdy wyciek z gitleaks ma status rotacji; skan Trivy bez nierozpatrzonych znalezisk HIGH i CRITICAL (każde naprawione albo z uzasadnionym wyjątkiem).

**Folder roboczy:** `10-bezpieczenstwo/e4-narzedzia-sast-dast-i-wykrywanie-sekretow/`

### Etap 5: łańcuch dostaw i SBOM

Opis kamienia milowego (do wklejenia):

**Cel:** łańcuch dostaw: SBOM, zależności, `cargo-vet` · **Poziom po etapie:** E

**Szczególnie ważne:** kompletność SBOM (zależności przechodnie, wersje, licencje, identyfikatory PURL), SBOM dla każdego wydania, a nie jednorazowo, ocena nowych zależności przed dodaniem (Scorecard, utrzymanie, liczba opiekunów), pakiety wymyślone przez model i ich podróbki (typosquatting, „slopsquatting”); weryfikacja pochodzenia zależności po stronie odbiorcy (podpisy i atestacje provenance w npm, atestacje SLSA dla binarek), a nie tylko wystawianie ich dla własnych wydań.

**Dowód:** Dla jednej aplikacji z rdzeniem w Ruście i frontendem w TypeScript: SBOM w CycloneDX generowany w CI przy każdym wydaniu, polityka `cargo-deny` i `cargo-vet` z udokumentowanymi wyjątkami, raport Scorecard dla 10 najważniejszych zależności i decyzja dla każdej, `npm audit signatures` w CI i lista zależności bez atestacji pochodzenia z oceną ryzyka.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|
| `S10-E5-M1` | Przerobić: Authoritative Guide to SBOM (wydanie 3) i specyfikacja CycloneDX (ECMA-424) | materiał | 8–10 h | 0 zł | https://cyclonedx.org/guides/, https://cyclonedx.org | `S10-E4-D` | `S10-E5-D` | `10-bezpieczenstwo/e5-lancuch-dostaw-i-sbom/` |
| `S10-E5-M2` | Przerobić: Cargo Vet | materiał | 3–4 h | 0 zł | https://mozilla.github.io/cargo-vet/ | `S10-E4-D` | `S10-E5-D` | `10-bezpieczenstwo/e5-lancuch-dostaw-i-sbom/` |
| `S10-E5-M3` | Przerobić: RustSec Advisory Database i `cargo-audit` | materiał | 2–3 h | 0 zł | https://rustsec.org | `S10-E4-D` | `S10-E5-D` | `10-bezpieczenstwo/e5-lancuch-dostaw-i-sbom/` |
| `S10-E5-M4` | Przerobić: OpenSSF Scorecard | materiał | 2–3 h | 0 zł | https://scorecard.dev | `S10-E4-D` | `S10-E5-D` | `10-bezpieczenstwo/e5-lancuch-dostaw-i-sbom/` |
| `S10-E5-M5` | Przerobić: OSV i `osv-scanner` | materiał | 2–3 h | 0 zł | https://osv.dev | `S10-E4-D` | `S10-E5-D` | `10-bezpieczenstwo/e5-lancuch-dostaw-i-sbom/` |
| `S10-E5-M6` | Przerobić: SLSA v1.2: „Threats & mitigations” i „Verifying artifacts”; Sigstore: weryfikacja podpisów i… | materiał | 4–5 h | 0 zł | https://slsa.dev/spec/v1.2/threats, https://slsa.dev/spec/v1.2/verifying-artifacts, https://docs.sigstore.dev, https://docs.npmjs.com/verifying-registry-signatures | `S10-E4-D` | `S10-E5-D` | `10-bezpieczenstwo/e5-lancuch-dostaw-i-sbom/` |
| `S10-E5-D` | Dowód etapu 5: łańcuch dostaw i SBOM | dowód | — | — | — | `S10-E5-M1`, `S10-E5-M2`, `S10-E5-M3`, `S10-E5-M4`, `S10-E5-M5`, `S10-E5-M6` | `S10-E6-M1`, `S10-E6-M2`, `S10-E6-M3`, `S10-E6-M4`, `S10-E6-M5`, `S10-E6-M6`, `S10-E6-M7`, `S10-E6-M8`, `S10-E6-M9`, `S10-E6-M10` | `10-bezpieczenstwo/e5-lancuch-dostaw-i-sbom/` |

**`S10-E5-D` · Dowód etapu 5: łańcuch dostaw i SBOM**

Dla jednej aplikacji z rdzeniem w Ruście i frontendem w TypeScript: SBOM w CycloneDX generowany w CI przy każdym wydaniu, polityka `cargo-deny` i `cargo-vet` z udokumentowanymi wyjątkami, raport Scorecard dla 10 najważniejszych zależności i decyzja dla każdej, `npm audit signatures` w CI i lista zależności bez atestacji pochodzenia z oceną ryzyka.

**Na co zwrócić uwagę:** kompletność SBOM (zależności przechodnie, wersje, licencje, identyfikatory PURL), SBOM dla każdego wydania, a nie jednorazowo, ocena nowych zależności przed dodaniem (Scorecard, utrzymanie, liczba opiekunów), pakiety wymyślone przez model i ich podróbki (typosquatting, „slopsquatting”); weryfikacja pochodzenia zależności po stronie odbiorcy (podpisy i atestacje provenance w npm, atestacje SLSA dla binarek), a nie tylko wystawianie ich dla własnych wydań.

**Kryterium ukończenia:** SBOM dołączony do każdego wydania i zawierający zależności przechodnie z PURL; `cargo deny check` i `cargo vet` przechodzą w CI; 10 decyzji (przyjąć, zastąpić, usunąć) z uzasadnieniem; `npm audit signatures` bez błędów weryfikacji.

**Folder roboczy:** `10-bezpieczenstwo/e5-lancuch-dostaw-i-sbom/`

### Etap 6: obsługa podatności i CRA

Opis kamienia milowego (do wklejenia):

**Cel:** obsługa podatności i CRA: CVSS, EPSS, KEV, zgłoszenia · **Poziom po etapie:** E

**Szczególnie ważne:** CVSS opisuje dotkliwość, a nie ryzyko, więc kolejność napraw ustala się łącznie z EPSS, obecnością w KEV i kontekstem klienta (czy podatny kod jest osiągalny); terminy z art. 14: wczesne ostrzeżenie w 24 h, zgłoszenie w 72 h i raport końcowy; polityka ujawniania podatności i `security.txt`; okres wsparcia produktu; logi zdarzeń bezpieczeństwa (logowanie, zmiany uprawnień, odmowy dostępu) bez haseł, tokenów i danych osobowych ponad potrzebę; NIS2 zwykle nie obejmuje jednoosobowej firmy wprost, ale obejmuje wielu jej klientów, którzy przenoszą wymagania art. 21 (bezpieczeństwo łańcucha dostaw) na dostawców oprogramowania.

Obowiązki zgłoszeniowe producentów z CRA obowiązują od 11 września 2026 r. i są realizowane przez platformę ENISA; pozostałe obowiązki od 11 grudnia 2027 r.

**Dowód:** Triage 10 rzeczywistych CVE z zależności własnej aplikacji według CVSS 4.0, EPSS i KEV, z uzasadnieniem kolejności i decyzją (naprawa, łagodzenie, brak wpływu z oświadczeniem VEX); ćwiczenie zgłoszenia CRA na czas: od wykrycia aktywnie wykorzystywanej podatności do wypełnionego wczesnego ostrzeżenia w 24 h, z gotowymi szablonami zgłoszenia i komunikatu dla użytkowników; plan reagowania na incydenty według NIST SP 800-61r3 z terminami CRA i NIS2; logowanie zdarzeń bezpieczeństwa w aplikacji według OWASP Logging Vocabulary.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|
| `S10-E6-M1` | Przerobić: CVSS v4.0: specyfikacja i User Guide | materiał | 5–6 h | 0 zł | https://www.first.org/cvss/v4.0/specification-document, https://www.first.org/cvss/v4.0/user-guide | `S10-E5-D` | `S10-E6-D` | `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/` |
| `S10-E6-M2` | Przerobić: EPSS (Exploit Prediction Scoring System) | materiał | 2–3 h | 0 zł | https://www.first.org/epss/ | `S10-E5-D` | `S10-E6-D` | `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/` |
| `S10-E6-M3` | Przerobić: Known Exploited Vulnerabilities Catalog | materiał | 1–2 h | 0 zł | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | `S10-E5-D` | `S10-E6-D` | `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/` |
| `S10-E6-M4` | Przerobić: European Vulnerability Database (EUVD) | materiał | 1–2 h | 0 zł | https://euvd.enisa.europa.eu | `S10-E5-D` | `S10-E6-D` | `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/` |
| `S10-E6-M5` | Przerobić: Rozporządzenie (UE) 2024/2847 (CRA), zwłaszcza art. 13, 14 i załącznik I | materiał | 6–8 h | 0 zł | https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng | `S10-E5-D` | `S10-E6-D` | `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/` |
| `S10-E6-M6` | Przerobić: Wytyczne Komisji do stosowania CRA… | materiał | 6–8 h | 0 zł | https://digital-strategy.ec.europa.eu/en/library/commission-publishes-new-guidance-support-timely-cyber-resilience-act-implementation, https://digital-strategy.ec.europa.eu/en/policies/cra-reporting | `S10-E5-D` | `S10-E6-D` | `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/` |
| `S10-E6-M7` | Przerobić: Single Reporting Platform: FAQ, instrukcje, nagrania | materiał | 2–3 h | 0 zł | https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp | `S10-E5-D` | `S10-E6-D` | `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/` |
| `S10-E6-M8` | Przerobić: Secure by Design and Default Playbook | materiał | 2–3 h | 0 zł | https://www.enisa.europa.eu/publications/enisa-secure-by-design-and-default-playbook | `S10-E5-D` | `S10-E6-D` | `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/` |
| `S10-E6-M9` | Przerobić: NIST SP 800-61 Rev. 3: Incident Response Recommendations and Considerations for Cybersecurity… | materiał | 5–6 h | 0 zł | https://csrc.nist.gov/pubs/sp/800/61/r3/final, https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html, https://cheatsheetseries.owasp.org/cheatsheets/Logging_Vocabulary_Cheat_Sheet.html | `S10-E5-D` | `S10-E6-D` | `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/` |
| `S10-E6-M10` | Przerobić: Dyrektywa (UE) 2022/2555 (NIS2), zwłaszcza art. 21 i 23, oraz wytyczne techniczne ENISA do jej… | materiał | 4–5 h | 0 zł | https://eur-lex.europa.eu/eli/dir/2022/2555/oj, https://www.enisa.europa.eu/publications/nis2-technical-implementation-guidance | `S10-E5-D` | `S10-E6-D` | `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/` |
| `S10-E6-D` | Dowód etapu 6: obsługa podatności i CRA | dowód | — | — | — | `S10-E6-M1`, `S10-E6-M2`, `S10-E6-M3`, `S10-E6-M4`, `S10-E6-M5`, `S10-E6-M6`, `S10-E6-M7`, `S10-E6-M8`, `S10-E6-M9`, `S10-E6-M10` | `S10-E7-M1`, `S10-E7-M2`, `S10-E7-M3`, `S10-E8-M1`, `S10-E8-M2`, `S10-E8-M3`, `S10-E8-P1`, `S10-E8-P2`, `S10-E8-P3`, `S10-E8-P4`, `S18-E5-M1`, `S18-E5-M2`, `S18-E5-M3`, `S18-E5-M4`, `S18-E5-M5`, `S18-E5-M6`, `S18-E5-M7`, `S18-E5-M8`, `S18-E5-M9`, `S18-E5-M10`, `S18-E5-M11`, `S19-E5-M1`, `S19-E5-M2`, `S19-E5-M3`, `S19-E5-M4`, `S19-E5-M5`, `S19-E5-M6`, `S19-E5-M7`, `S19-E5-M8`, `S19-E5-M9`, `S19-E5-M10` | `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/` |

**`S10-E6-D` · Dowód etapu 6: obsługa podatności i CRA**

Triage 10 rzeczywistych CVE z zależności własnej aplikacji według CVSS 4.0, EPSS i KEV, z uzasadnieniem kolejności i decyzją (naprawa, łagodzenie, brak wpływu z oświadczeniem VEX); ćwiczenie zgłoszenia CRA na czas: od wykrycia aktywnie wykorzystywanej podatności do wypełnionego wczesnego ostrzeżenia w 24 h, z gotowymi szablonami zgłoszenia i komunikatu dla użytkowników; plan reagowania na incydenty według NIST SP 800-61r3 z terminami CRA i NIS2; logowanie zdarzeń bezpieczeństwa w aplikacji według OWASP Logging Vocabulary.

**Na co zwrócić uwagę:** CVSS opisuje dotkliwość, a nie ryzyko, więc kolejność napraw ustala się łącznie z EPSS, obecnością w KEV i kontekstem klienta (czy podatny kod jest osiągalny); terminy z art. 14: wczesne ostrzeżenie w 24 h, zgłoszenie w 72 h i raport końcowy; polityka ujawniania podatności i `security.txt`; okres wsparcia produktu; logi zdarzeń bezpieczeństwa (logowanie, zmiany uprawnień, odmowy dostępu) bez haseł, tokenów i danych osobowych ponad potrzebę; NIS2 zwykle nie obejmuje jednoosobowej firmy wprost, ale obejmuje wielu jej klientów, którzy przenoszą wymagania art. 21 (bezpieczeństwo łańcucha dostaw) na dostawców oprogramowania.

**Kryterium ukończenia:** 10 CVE z wynikiem CVSS 4.0, EPSS, obecnością w KEV i decyzją, co najmniej jedno oświadczenie VEX; wczesne ostrzeżenie przygotowane w mniej niż 24 h od startu ćwiczenia; plan incydentów z rolami, kontaktami i terminami; co najmniej 8 typów zdarzeń bezpieczeństwa logowanych, z testem, że logi nie zawierają haseł ani tokenów; polityka ujawniania podatności i `security.txt` opublikowane.

**Folder roboczy:** `10-bezpieczenstwo/e6-obsluga-podatnosci-i-cra/`

### Etap 7: Rust i desktop (Tauri)

Opis kamienia milowego (do wklejenia):

**Cel:** Rust i desktop: `unsafe`, narzędzia Rusta, Tauri (IPC, capabilities, aktualizacje) · **Poziom po etapie:** W

Etap dotyczy audytu rdzenia w Ruście i aplikacji desktopowej Tauri. Bezpieczeństwo aplikacji mobilnych (MASVS, MASTG) jest w sekcji 18, etap 3, a bezpieczeństwo firmware (secure boot, podpis, normy EN 18031 i ETSI EN 303 645) w sekcji 22.

**Szczególnie ważne:** każdy blok `unsafe` z komentarzem `SAFETY:` i uzasadnieniem, `unsafe` w zależnościach jako ryzyko łańcucha dostaw, panika jako odmowa usługi; webview traktowany jako niezaufany, każde polecenie IPC waliduje wejście jak endpoint API, capabilities i zakresy plików zawężone do minimum, CSP bez `unsafe-inline`, klucz podpisu aktualizacji poza repozytorium i poza zmiennymi frontendu.

**Dowód:** Raport z przeglądu bezpieczeństwa własnej aplikacji Tauri z rdzeniem w Ruście: mapa `cargo-geiger` z uzasadnieniem każdego bloku `unsafe` w kodzie własnym i decyzją dla każdej zależności z `unsafe`; tabela wszystkich poleceń IPC z walidacją wejścia; przegląd capabilities, zakresów i CSP z poprawkami; sprawdzenie podpisu i kanału aktualizacji.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|
| `S10-E7-M1` | Przerobić: Secure Rust Guidelines | materiał | 6–8 h | 0 zł | https://anssi-fr.github.io/rust-guide/ | `S10-E6-D`, `S12-E5-D`, `S14-E1-D` | `S10-E7-D` | `10-bezpieczenstwo/e7-rust-i-desktop-tauri/` |
| `S10-E7-M2` | Przerobić: Rust Secure Code Working Group: lista projektów (fuzzery, analizatory, narzędzia zależności) | materiał | 2–3 h | 0 zł | https://github.com/rust-secure-code/projects | `S10-E6-D`, `S12-E5-D`, `S14-E1-D` | `S10-E7-D` | `10-bezpieczenstwo/e7-rust-i-desktop-tauri/` |
| `S10-E7-M3` | Przerobić: Tauri: Security (granice zaufania, IPC, capabilities) | materiał | 4–6 h | 0 zł | https://v2.tauri.app/security/ | `S10-E6-D`, `S12-E5-D`, `S14-E1-D` | `S10-E7-D` | `10-bezpieczenstwo/e7-rust-i-desktop-tauri/` |
| `S10-E7-D` | Dowód etapu 7: Rust i desktop (Tauri) | dowód | — | — | — | `S10-E7-M1`, `S10-E7-M2`, `S10-E7-M3` | `S10-E8-M1`, `S10-E8-M2`, `S10-E8-M3`, `S10-E8-P1`, `S10-E8-P2`, `S10-E8-P3`, `S10-E8-P4` | `10-bezpieczenstwo/e7-rust-i-desktop-tauri/` |

**`S10-E7-D` · Dowód etapu 7: Rust i desktop (Tauri)**

Raport z przeglądu bezpieczeństwa własnej aplikacji Tauri z rdzeniem w Ruście: mapa `cargo-geiger` z uzasadnieniem każdego bloku `unsafe` w kodzie własnym i decyzją dla każdej zależności z `unsafe`; tabela wszystkich poleceń IPC z walidacją wejścia; przegląd capabilities, zakresów i CSP z poprawkami; sprawdzenie podpisu i kanału aktualizacji.

**Na co zwrócić uwagę:** każdy blok `unsafe` z komentarzem `SAFETY:` i uzasadnieniem, `unsafe` w zależnościach jako ryzyko łańcucha dostaw, panika jako odmowa usługi; webview traktowany jako niezaufany, każde polecenie IPC waliduje wejście jak endpoint API, capabilities i zakresy plików zawężone do minimum, CSP bez `unsafe-inline`, klucz podpisu aktualizacji poza repozytorium i poza zmiennymi frontendu.

**Kryterium ukończenia:** każdy blok `unsafe` w kodzie własnym ma komentarz `SAFETY:` (lint `undocumented_unsafe_blocks` przechodzi); każde polecenie IPC ma test odrzucający niepoprawne wejście; żadne okno nie ma uprawnień szerszych niż potrzebne (każde odstępstwo opisane); aktualizacja z niepoprawnym podpisem jest odrzucana w teście.

**Folder roboczy:** `10-bezpieczenstwo/e7-rust-i-desktop-tauri/`

### Etap 8: ekspert

Opis kamienia milowego (do wklejenia):

**Cel:** ekspert: audyty klientów, badania, aktualność · **Poziom po etapie:** E

**Dowód poziomu E:** Samodzielnie, bez agenta, w 2 dni przeprowadzasz audyt nieznanej aplikacji (web z API albo desktop Tauri z rdzeniem w Ruście): status każdego wymagania ASVS L1, model zagrożeń STRIDE, SBOM z triage’em podatności i ocena obowiązków z CRA. Znajdujesz co najmniej jeden błąd kontroli dostępu lub łańcucha dostaw, którego nie zgłosiły Semgrep, CodeQL, ZAP ani `cargo-audit`, potwierdzony testem lub PoC, i przedstawiasz klientowi raport z planem naprawy uszeregowanym według ryzyka.

| Klucz | Tytuł | Typ | Czas | Koszt | Link | Blokowane przez | Blokuje | Folder |
|---|---|---|---|---|---|---|---|---|
| `S10-E8-M1` | Przerobić: Burp Suite Certified Practitioner | materiał, płatny, opcjonalne | 20–40 h przygotowania | płatny | https://portswigger.net/web-security/certification | `S10-E6-D`, `S10-E7-D`, `S11-E2-D` | — | `10-bezpieczenstwo/e8-ekspert/` |
| `S10-E8-M2` | Przerobić: Komunikaty bezpieczeństwa frameworków i zależności, RustSec, EUVD, KEV | materiał | ok. 1 h tygodniowo | 0 zł | https://rustsec.org, https://euvd.enisa.europa.eu | `S10-E6-D`, `S10-E7-D`, `S11-E2-D` | `S10-E8-D` | `10-bezpieczenstwo/e8-ekspert/` |
| `S10-E8-M3` | Przerobić: Zmiany w ASVS, Top 10 i materiałach Komisji i ENISA o CRA | materiał, opcjonalne | wg potrzeb | 0 zł | https://github.com/OWASP/ASVS, https://digital-strategy.ec.europa.eu/en/policies/cra-reporting | `S10-E6-D`, `S10-E7-D`, `S11-E2-D` | — | `10-bezpieczenstwo/e8-ekspert/` |
| `S10-E8-P1` | Praktyka: audyty klientów | praktyka | — | — | — | `S10-E6-D`, `S10-E7-D`, `S11-E2-D` | `S10-E8-D` | `10-bezpieczenstwo/e8-ekspert/` |
| `S10-E8-P2` | Praktyka: recenzja bezpieczeństwa kodu AI | praktyka | — | — | — | `S10-E6-D`, `S10-E7-D`, `S11-E2-D` | `S10-E8-D` | `10-bezpieczenstwo/e8-ekspert/` |
| `S10-E8-P3` | Praktyka: obsługa podatności jako proces | praktyka | — | — | — | `S10-E6-D`, `S10-E7-D`, `S11-E2-D` | `S10-E8-D` | `10-bezpieczenstwo/e8-ekspert/` |
| `S10-E8-P4` | Praktyka: wkład zewnętrzny | praktyka | — | — | — | `S10-E6-D`, `S10-E7-D`, `S11-E2-D` | `S10-E8-D` | `10-bezpieczenstwo/e8-ekspert/` |
| `S10-E8-D` | Dowód poziomu E: ekspert | dowód | — | — | — | `S10-E8-M2`, `S10-E8-P1`, `S10-E8-P2`, `S10-E8-P3`, `S10-E8-P4` | — | `10-bezpieczenstwo/e8-ekspert/` |

**`S10-E8-P1` · Praktyka: audyty klientów**

5 audytów aplikacji z vibe codingu lub no-code według jednego szablonu raportu (ASVS, model zagrożeń, SBOM, plan naprawy), z mierzeniem czasu i poprawianiem szablonu.

Praktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, a nie po jednorazowym wykonaniu.

**Folder roboczy:** `10-bezpieczenstwo/e8-ekspert/`

**`S10-E8-P2` · Praktyka: recenzja bezpieczeństwa kodu AI**

Lista kontrolna bezpieczeństwa wbudowana w vicrafter (własny plugin Claude Code z sekcji 11: hooki i skille) i sprawdzana na 20 pull requestach agentów, z odsetkiem błędów wykrytych przez człowieka, a pominiętych przez narzędzia.

Praktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, a nie po jednorazowym wykonaniu.

**Folder roboczy:** `10-bezpieczenstwo/e8-ekspert/`

**`S10-E8-P3` · Praktyka: obsługa podatności jako proces**

Dyżur nad komunikatami dla wszystkich utrzymywanych aplikacji, ćwiczenie zgłoszenia CRA raz na kwartał.

Praktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, a nie po jednorazowym wykonaniu.

**Folder roboczy:** `10-bezpieczenstwo/e8-ekspert/`

**`S10-E8-P4` · Praktyka: wkład zewnętrzny**

Zgłoszenie odpowiedzialnie ujawnionej podatności w projekcie open source albo reguła Semgrep lub wpis do RustSec.

Praktyka ciągła etapu eksperckiego: oznacz jako gotową, gdy działa jako stały element pracy, a nie po jednorazowym wykonaniu.

**Folder roboczy:** `10-bezpieczenstwo/e8-ekspert/`

**`S10-E8-D` · Dowód poziomu E: ekspert**

Samodzielnie, bez agenta, w 2 dni przeprowadzasz audyt nieznanej aplikacji (web z API albo desktop Tauri z rdzeniem w Ruście): status każdego wymagania ASVS L1, model zagrożeń STRIDE, SBOM z triage’em podatności i ocena obowiązków z CRA. Znajdujesz co najmniej jeden błąd kontroli dostępu lub łańcucha dostaw, którego nie zgłosiły Semgrep, CodeQL, ZAP ani `cargo-audit`, potwierdzony testem lub PoC, i przedstawiasz klientowi raport z planem naprawy uszeregowanym według ryzyka.

**Kryterium ukończenia:** dowód wykonany samodzielnie; w komentarzu link do repozytorium, raportu lub notatki. Bez agenta AI.

**Folder roboczy:** `10-bezpieczenstwo/e8-ekspert/`

## 6. Relacje z innymi projektami

**Wchodzące** (zadanie z innego projektu blokuje zadanie tego projektu):

- `S03-E2-D` (Dowód etapu 2: TypeScript) → `S10-START`
- `S04-E1-D` (Dowód etapu 1: PostgreSQL w praktyce) → `S10-START`
- `S05-E1-D` (Dowód etapu 1: Node.js po stronie serwera) → `S10-START`
- `S08-E1-D` (Dowód etapu 1: style architektoniczne, atrybuty jakości i kompromisy) → `S10-START`
- `S09-E2-D` (Dowód etapu 2: GitHub Actions i bezpieczeństwo pipeline’u) → `S10-START`
- `S12-E5-D` (Dowód etapu 5: `unsafe` i FFI (UniFFI, `cbindgen`, Miri)) → `S10-E7-M1`
- `S14-E1-D` (Dowód etapu 1: Tauri 2) → `S10-E7-M1`
- `S12-E5-D` (Dowód etapu 5: `unsafe` i FFI (UniFFI, `cbindgen`, Miri)) → `S10-E7-M2`
- `S14-E1-D` (Dowód etapu 1: Tauri 2) → `S10-E7-M2`
- `S12-E5-D` (Dowód etapu 5: `unsafe` i FFI (UniFFI, `cbindgen`, Miri)) → `S10-E7-M3`
- `S14-E1-D` (Dowód etapu 1: Tauri 2) → `S10-E7-M3`
- `S11-E2-D` (Dowód etapu 2: recenzja kodu) → `S10-E8-M1`
- `S11-E2-D` (Dowód etapu 2: recenzja kodu) → `S10-E8-M2`
- `S11-E2-D` (Dowód etapu 2: recenzja kodu) → `S10-E8-M3`
- `S11-E2-D` (Dowód etapu 2: recenzja kodu) → `S10-E8-P1`
- `S11-E2-D` (Dowód etapu 2: recenzja kodu) → `S10-E8-P2`
- `S11-E2-D` (Dowód etapu 2: recenzja kodu) → `S10-E8-P3`
- `S11-E2-D` (Dowód etapu 2: recenzja kodu) → `S10-E8-P4`

**Wychodzące** (zadanie tego projektu blokuje zadanie w innym projekcie):

- `S10-E1-D` → `S11-START` (11. Weryfikacja pracy AI i budowa procesu)
- `S10-E1-D` → `S20-START` (20. Lokalne AI i rozwój modeli)
- `S10-E1-D` → `S21-START` (21. Funkcje AI w aplikacjach)
- `S10-E1-D` → `S22-START` (22. Systemy wbudowane)
- `S10-E3-D` → `S11-E4-M1` (11. Weryfikacja pracy AI i budowa procesu)
- `S10-E3-D` → `S11-E4-M2` (11. Weryfikacja pracy AI i budowa procesu)
- `S10-E3-D` → `S11-E4-M3` (11. Weryfikacja pracy AI i budowa procesu)
- `S10-E3-D` → `S11-E4-M4` (11. Weryfikacja pracy AI i budowa procesu)
- `S10-E6-D` → `S18-E5-M1` (18. Android)
- `S10-E6-D` → `S18-E5-M2` (18. Android)
- `S10-E6-D` → `S18-E5-M3` (18. Android)
- `S10-E6-D` → `S18-E5-M4` (18. Android)
- `S10-E6-D` → `S18-E5-M5` (18. Android)
- `S10-E6-D` → `S18-E5-M6` (18. Android)
- `S10-E6-D` → `S18-E5-M7` (18. Android)
- `S10-E6-D` → `S18-E5-M8` (18. Android)
- `S10-E6-D` → `S18-E5-M9` (18. Android)
- `S10-E6-D` → `S18-E5-M10` (18. Android)
- `S10-E6-D` → `S18-E5-M11` (18. Android)
- `S10-E6-D` → `S19-E5-M1` (19. iOS)
- `S10-E6-D` → `S19-E5-M2` (19. iOS)
- `S10-E6-D` → `S19-E5-M3` (19. iOS)
- `S10-E6-D` → `S19-E5-M4` (19. iOS)
- `S10-E6-D` → `S19-E5-M5` (19. iOS)
- `S10-E6-D` → `S19-E5-M6` (19. iOS)
- `S10-E6-D` → `S19-E5-M7` (19. iOS)
- `S10-E6-D` → `S19-E5-M8` (19. iOS)
- `S10-E6-D` → `S19-E5-M9` (19. iOS)
- `S10-E6-D` → `S19-E5-M10` (19. iOS)
