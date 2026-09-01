# cliCHair.ch — Audit del catalogo Shopify

Rilevazione: 1 settembre 2026 · Store: cliCHair.ch (CHF, Svizzera) · Fonte: Shopify Admin API (dati live)

## 1. Numeri di partenza

| Metrica | Valore |
|---|---|
| Prodotti totali | 491 |
| — ACTIVE | 434 |
| — DRAFT | 43 |
| — ARCHIVED | 14 |
| Prodotti "Colors" (shade) | 237 (di cui 29 DRAFT) |
| Prodotti "Marketing" (espositori, cataloghi, campioni, box) | 25 |
| Collezioni | 99 |
| Vendor | 4 (NIKA, CODE ZERO, EDELSTEIN, cliCHair) |
| Product type distinti | 15 |
| Tag distinti | 97 |
| Metafield raccomandazioni | `shopify--discovery--product_recommendation.related_products` / `.complementary_products` (Search & Discovery attivo) |

Il catalogo reale "non colore" è di circa 226 prodotti attivi. Le 237 shade sono un blocco a parte,
molto ripetitivo, che va trattato con regole automatiche e non a mano.

## 2. Problemi rilevati

### 2.1 Product type: tre assi mescolati in un campo solo

I 15 valori attuali non appartengono alla stessa dimensione:

- **funzione/step**: `Wash`, `Care`, `Treatment`, `Styling`, `Bleaching`, `Oxidizer`
- **categoria merceologica**: `Colors`, `Tools`, `Clothing`, `Beard`, `After Shave`, `Sanitizing`, `Skin Stain Remover`
- **natura commerciale**: `Bundle`, `Marketing`

Conseguenze verificate sui dati:

- `Wash` contiene shampoo, balsami e maschere indistintamente (es. `curly-up-mask-1000` e `curly-up-shampoo-1000` hanno lo stesso type).
- La spazzola `flexion-l-brush` ha type `Styling` invece di `Tools`.
- `nika-treatment-trolley` (carrello da salone) ha type `Marketing` ma sta nella collezione `nika-tools`.
- `xflex-atomizer` ha type `Tools` ma vive nella collezione `after-shave`.
- Alcuni prodotti hanno product type vuoto (`basix-neutral-shampoo-1500-ml`, `deflake-anti-dandruff-1500-ml`, `gift-card`).

Il product type alimenta filtri di tema, regole di smart collection e feed (Google/Meta): un campo
ambiguo degrada tutte e tre le cose insieme.

### 2.2 Categoria standard Shopify (taxonomy) inaffidabile

La `category` è quella che alimenta Shop, Google Shopping e i metafield di categoria. Oggi contiene errori:

- `bleach-7-tones` → "Insaponatura e rasatura > Decolorante per peli di corpo e viso" (è un decolorante **capelli**)
- `extender` (leave-in anti-frizz) → "Fissatore in gel, spray e schiuma"
- `argan-native-fluid` → nodo generico "Cura dei capelli", senza foglia
- `ar-discovery-box`, `fb-discovery-box`, `gr-discovery-box` → "Non categorizzato"

### 2.3 Tag: 97 valori senza vocabolario controllato

Quattro patologie compresenti:

1. **Tag universale inutile**: `Hair` è su quasi tutto il catalogo, non discrimina nulla.
2. **Sinonimi che spezzano gli insiemi**: `Reconstruction` / `Reconstructive` / `Repair` / `Regeneration`;
   `Care` / `Treatment`; `Smooth` / `Frizz Free` / `Shape`; `Volume Up` / `Volumizing`; `Color` / `Coloured`;
   `Final` / `Outlet` / `Promo`.
3. **Stato e marketing mescolati agli attributi di prodotto**: `Trending`, `Trend Up`, `Memo`, `Coming Soon`,
   `Beauty`, `Sample`, `Pro`, `Essential`, `Native`, `Finish`, `Body`, `Face`, `Merchandising`.
4. **Brand duplicati nel campo vendor**: `Nika`, `Edelstein`, `Code Zero`, `cliCHair` sono sia vendor sia tag.

Inoltre alcune regole di collezione puntano a **tag che non esistono**:

- `hair-wax` filtra su `Paste` e `Pomade` → nessuno dei due esiste nel vocabolario (funziona solo per `Wax`)
- `bfcm` filtra su `BFCM` → collezione con **0 prodotti**

### 2.4 Collezioni: 99, piatte, sovrapposte, un terzo troppo sottili

**Doppioni semantici** (stesso significato, insiemi diversi, si cannibalizzano tra loro in SERP):

| Gruppo | Collezioni | Prodotti |
|---|---|---|
| Riparazione | `reconstructive` / `reconstruction` / `repair` / `damaged-hair` | 7 / 16 / 8 / 4 |
| Barba | `beard` / `beard-collection` / `shaving` | 3 / 15 / 2 |
| Volume | `volume` / `volume-up` | 2 / 2 |
| Ricci | `curly-hair` / `curl-definition` / `defined-curls` / `curly-up` | 15 / 14 / 7 / 8 |
| Liscio / anti-crespo | `straight-hair` / `silky-smooth` / `anti-frizz` / `frizz-control` / `liss-komplex` | 29 / 6 / 27 / 3 / 12 |
| Promo | `deals-collection` / `final-collection` / `outlet` | 7 / 5 / 54 |
| Forfora | `dandruff` / `inej-dandruff` | 2 / 2 |
| Caduta | `hair-loss` / `inej-loss-control` | 2 / 2 |
| Cute sensibile | `sensitive-scalp` / `sensitive-scalp-1` | 2 / 3 |
| Lucentezza | `shine-gloss` / `color-shine` | 5 / 2 |
| Styling | `styling` / `code-style` / `xflex-style` | 34 / 5 / 23 |

**Manutenibilità**: 18 collezioni sono manuali senza alcuna regola (`ruleSet: null`) — un prodotto nuovo non
ci entra mai da solo: `grey-hair`, `hair-loss`, `dandruff`, `damaged-hair`, `oily-scalp`, `dry-hair`,
`sensitive-scalp-1`, `perfect-blonde`, `frizz-control`, `volume`, `defined-curls`, `silky-smooth`,
`color-shine`, `shine-gloss`, `scalp-shaved`, `ice-experience`, `shave-aftercare`, `advanced-care`.

**Thin content**: 30 collezioni su 99 hanno 3 prodotti o meno (di cui `bfcm` a zero). Pagine con 1-3 prodotti
non si posizionano e diluiscono il crawl budget.

**Nessuna gerarchia**: 99 collezioni tutte sullo stesso piano, senza percorso brand → linea → bisogno.
Non c'è internal linking strutturato, che è il fattore principale di indicizzabilità di un catalogo.

**Vendor cliCHair senza casa**: non esiste una collezione `cliCHair`; i prodotti a marchio proprio sono
orfani o dispersi (`cuticles-access-system-gloss`, vendor cliCHair, vive tra collezioni Edelstein).

**Prodotti attivi fuori da ogni collezione** (4): `chimono`, `cliform`, `necks-cover`, `gift-card`.

### 2.5 Prodotti correlati e complementari: semantica invertita e link morti

Questo è il punto che pesa di più sui consigli in pagina.

**a) I due campi sono usati in modo intercambiabile.** La semantica corretta è:
*related* = alternative allo stesso bisogno (stessa famiglia, formato o brand diverso);
*complementary* = si usano insieme (step successivo del protocollo, tool necessario).
Oggi è spesso invertita:

- `sanitising-hand-gel` (igienizzante): related = ciotole, pennelli, mantelline → sono complementari, non alternative
- `chimono` (mantellina): related = ciotole e pennelli → idem
- `flexion-l-brush`: related = 1 solo prodotto; i complementari sono corretti ma la lista related è inutilizzabile
- `nika-activator`: related = 1 prodotto, complementary = 9 shade Grace (corretto in direzione, ma sbilanciato)

**b) Link verso prodotti non acquistabili.** Diversi complementari puntano a prodotti ARCHIVED,
per esempio `defrizzit` (`gid://…/4746057318538`, ARCHIVED) è ancora raccomandato da `flexion-l-brush`.
Il visitatore atterra su una pagina che non può comprare.

**c) Copertura incompleta.** Hanno `related`/`complementary` a `null`: `nika-beauty-box`, `bleach-7-tones`,
`basix-neutral-shampoo-1500-ml`, `deflake-anti-dandruff-1500-ml`, `clinner`, `fb-discovery-box`,
`gr-discovery-box`, `flyers-prospect-flexion-shimmer`. Hanno `complementary` vuoto: `sanitising-hand-gel`, `gift-card`.

**d) Il blocco colore è tutto uguale.** Tutte le 237 shade condividono lo stesso set di related
(le stesse 4-5 shade fisse) e lo stesso complementary. Per una tinta il correlato utile è la
**shade vicina per livello e riflesso**, non cinque shade a caso identiche per tutto il catalogo.
È il singolo intervento con il maggior ritorno: 237 prodotti, oggi con raccomandazioni prive di informazione.

### 2.6 Duplicati di prodotto

29 shade Grace esistono due volte: una ACTIVE e una DRAFT con lo stesso titolo e handle con suffisso `-1`
(es. `grace-color-1-0-black` ACTIVE + `grace-color-1-0-black-1` DRAFT;
`grace-5-22-light-deep-violet-natural-brown` + `…-1`). Se venissero pubblicate genererebbero
contenuto duplicato e cannibalizzazione interna.

## 3. Sintesi

La struttura non è rotta, è **stratificata**: tre generazioni di logiche (per brand, per linea, per bisogno)
convivono senza che nessuna sia stata completata. Il catalogo funziona per chi sa già cosa cerca e
funziona male per ricerca interna, filtri, raccomandazioni e motori di ricerca.

Gli interventi, in ordine di ritorno decrescente:

1. Raccomandazioni per le 237 shade con regola tonale (oggi: valore informativo nullo)
2. Consolidamento collezioni doppie + gerarchia a 3 livelli (oggi: cannibalizzazione e thin content)
3. Vocabolario tag controllato (abilita tutto il resto: smart collection, filtri, boost di ricerca)
4. Product type su un asse solo + category standard corretta (feed, filtri, Shop)
5. Related/complementary con semantica corretta sui 226 prodotti non-colore
6. Pulizia: 29 duplicati DRAFT, prodotti Marketing, link a prodotti archiviati
