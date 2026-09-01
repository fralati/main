# cliCHair.ch — Architettura target del catalogo

Documento di progetto. Definisce lo stato finale verso cui portare catalogo, collezioni,
attributi e raccomandazioni. Da approvare prima dell'esecuzione.

## Principio guida

Ogni informazione vive in **un solo campo**, e ogni campo ha **un solo asse semantico**.

| Campo | Asse | Esempio |
|---|---|---|
| `vendor` | Brand | NIKA, CODE ZERO, EDELSTEIN, cliCHair |
| `productType` | Che cosa è (merceologia) | Shampoo, Mask, Hair Color, Tools |
| `category` (taxonomy Shopify) | Nodo standard per Shop/Google/feed | …> Shampoo e balsamo > Shampoo |
| metafield `shopify.*` | Facet filtrabili | hold-level, hair-type, gray-coverage-level |
| `tags` | Linea commerciale, bisogno, stato | Fairy Silk, need-frizz, state-outlet |
| Collezioni | Percorsi di navigazione e pagine indicizzabili | /collections/anti-frizz |
| related / complementary | Raccomandazioni in pagina | vedi §5 |

Oggi questi sei livelli sono mescolati: è la causa comune di quasi tutti i problemi dell'audit.

## 1. Product type — asse unico: merceologia

Sostituisce i 15 valori attuali. Un prodotto = un tipo, senza ambiguità.

| Nuovo type | Copre | Da (attuale) |
|---|---|---|
| `Shampoo` | shampoo, shampoo secco, shampoo tecnici | Wash |
| `Conditioner` | balsami, deep conditioner | Wash |
| `Mask` | maschere risciacquo | Wash |
| `Leave-in` | fluidi, sieri, oli, spray senza risciacquo, termoprotettori | Care, Styling |
| `Salon Treatment` | trattamenti in cabina: lisciante, nanoplastia, ricostruzione, permanente | Treatment |
| `Hair Color` | tutte le shade (Vibrant, Grace, Gems) | Colors |
| `Pigment` | pigmenti puri, correttori, stabilizzatori | Colors, Wash |
| `Developer` | ossidanti e attivatori | Oxidizer |
| `Lightener` | decoloranti, extra lift | Bleaching |
| `Styling` | gel, cere, paste, spray, mousse, polveri | Styling |
| `Beard Care` | shampoo barba, oli, balsami barba | Beard |
| `Shaving` | creme e gel da rasatura | Beard |
| `After Shave` | dopobarba, cremagel | After Shave |
| `Skin Care` | igienizzanti, smacchiatori pelle | Sanitizing, Skin Stain Remover |
| `Tools` | spazzole, pettini, ciotole, pennelli, atomizzatori, carrelli | Tools, Styling, Marketing |
| `Salon Wear` | mantelline, kimono, grembiuli, t-shirt, turbanti | Clothing, Tools |
| `Kit` | protocolli e rituali multi-prodotto | Bundle |
| `Retail Display` | espositori, cataloghi, shopper, campioni, discovery box | Marketing |

Regole: nessun prodotto senza type; `Retail Display` esce dai canali di vendita e dai consigli.

## 2. Categoria standard Shopify

Ogni prodotto assegnato alla **foglia** corretta della tassonomia Shopify, non a un nodo intermedio.
Correzioni prioritarie già identificate: decoloranti capelli (oggi classificati come depilatori corpo/viso),
leave-in classificati come fissatori, prodotti su nodo generico "Cura dei capelli", box non categorizzati.

## 3. Facet (metafield `shopify.*`) — completare, non aggiungere

Le definizioni esistono già (49). Il problema è la copertura disomogenea:
uno shampoo ha 10 facet valorizzati, una tinta 4, una spazzola 0.

Copertura minima obbligatoria per tipo:

| Type | Facet obbligatori |
|---|---|
| Shampoo / Conditioner / Mask | suitable-for-hair-type, hair-care-effect, product-form, shampoo-type |
| Leave-in | hair-care-effect, hair-care-finish, application-method |
| Hair Color | hair-color-shade, hair-color-formulation, gray-coverage-level, application-type |
| Developer / Lightener | application-type, chemical-safety-features |
| Styling | hold-level, hair-care-finish, product-form |
| Beard / Shaving / After Shave | suitable-for-skin-type, fragrance-level, product-form |
| Tools / Salon Wear | material, package-type |

Questo è ciò che alimenta i **filtri nativi** del tema: senza copertura piena i filtri mentono
(un prodotto senza facet sparisce dai risultati filtrati).

## 4. Tag — INVARIATI (vincolo di progetto)

I tag non si toccano: nessuna aggiunta, rimozione o rinomina. Il vocabolario attuale (97 valori)
resta esattamente com'è.

Conseguenze operative accettate:

- Le collezioni si costruiscono con i tag **già esistenti**, combinati con `VENDOR`, `TYPE` e
  le regole su metafield (`PRODUCT_METAFIELD_DEFINITION`), non con tag nuovi.
- Dove un bisogno non ha un tag proprio, la regola passa per il **product type** (§1) o per un
  **facet** (§3): sono i due assi su cui possiamo lavorare.
- Le sovrapposizioni semantiche fra tag (`Reconstruction`/`Reconstructive`/`Repair`) restano nei dati:
  si risolvono **a valle**, nella regola della collezione, con un OR fra i tag sinonimi.
  Esempio: `repair` = TAG Reconstruction OR TAG Reconstructive OR TAG Repair.
- Le due regole che puntano a tag inesistenti (`Paste`, `Pomade` in `hair-wax`) e quella su `BFCM`
  si correggono **cambiando la regola**, non creando i tag.
- Il tag resta la chiave primaria delle smart collection: ogni modifica di regola va verificata
  sul conteggio prodotti prima e dopo, perché non abbiamo la leva di ritaggare i prodotti fuori posto.

**Limite tecnico da tenere presente**: una smart collection Shopify applica un solo operatore a tutte
le sue regole (`appliedDisjunctively` è o AND o OR, non entrambi). Quindi *«vendor NIKA E (tag A o tag B)»*
non è esprimibile in una regola sola. Dove serve quella logica le opzioni sono due: sfruttare il nuovo
`productType` (che possiamo assegnare noi, ed è l'asse più pulito) oppure tenere la collezione manuale.
Questo è il motivo per cui, con i tag congelati, **il product type diventa la leva principale**.

## 5. Collezioni — da 99 piatte a ~55 su tre livelli

### Livello 1 — Brand (4 pagine)
`nika` · `code-zero` · `edelstein` · `clichair` *(nuova: oggi il marchio proprio non ha casa)*
Regola: `VENDOR EQUALS <brand>`, con i tag brand esistenti come fallback dove il vendor non coincide (es. Xflex è vendor EDELSTEIN + tag Xflex).

### Livello 2 — Linea (una per linea reale, ~24 pagine)
Regola: `VENDOR = brand` AND `TAG = <linea>`. Sono le pagine che convertono: hanno un racconto,
un protocollo e un set di prodotti coerente.

### Livello 3 — Bisogno e categoria trasversale (~27 pagine)
Sono le pagine che intercettano la domanda di ricerca. Regola su OR di tag esistenti sinonimi, oppure su `productType` (nuovo, §1), oppure su facet.

Colore: `colouring` · `ammonia-free-colors` · `low-ammonia-colors` · `semi-permanent` · `bleaching` ·
`developers` · `pigments` · `color-care`
Cura: `repair` *(assorbe reconstructive + reconstruction + damaged-hair)* · `hydration` ·
`anti-frizz` *(assorbe frizz-control + silky-smooth)* · `curls` *(assorbe curly-hair + curl-definition + defined-curls)* ·
`volume` *(assorbe volume-up)* · `blonde` *(assorbe perfect-blonde + blonde-essential)* · `grey-hair` ·
`anti-age` · `scalp-care` *(assorbe dandruff + oily-scalp + sensitive-scalp ×2 + hair-loss)* · `split-ends` · `shine`
Styling: `styling` *(assorbe code-style + xflex-style)* · `hair-gel` · `hair-wax` · `hair-spray` · `hair-mousse`
Uomo: `men` *(assorbe beard + beard-collection + shaving + scalp-shaved + shave-aftercare + ice-experience)*
Salone: `tools` · `salon-wear` · `kits`
Commerciale: `outlet` *(assorbe deals + final)* · `trending`

### Regole trasversali
- Ogni collezione è **smart** (rule-based). Zero collezioni manuali: oggi ne esistono 18 che non si aggiornano da sole.
- Nessuna collezione pubblicata sotto i 4 prodotti. Oggi ne esistono 30 (una vuota).
- Ogni collezione dismessa riceve un **redirect 301** verso quella che la assorbe: nessun 404, il valore SEO si trasferisce.
- Ogni collezione ha titolo SEO, meta description e descrizione introduttiva (già buone su gran parte delle attuali: si conservano e si fondono).
- I 4 prodotti attivi orfani (`chimono`, `cliform`, `necks-cover`, `gift-card`) entrano in `salon-wear` / esclusione esplicita.

## 6. Prodotti correlati e complementari

### Definizioni operative
- **Related** = *alternative allo stesso bisogno*. Chi guarda A potrebbe comprare B **al posto di** A.
  Stesso product type, stesso `need-*`, linea/brand/formato diverso. 4-6 prodotti.
- **Complementary** = *si usano insieme ad A*. Step successivo del protocollo, tool necessario,
  mantenimento a casa. Mai un sostituto. 3-5 prodotti.

### Regole per famiglia

| Famiglia | Related | Complementary |
|---|---|---|
| Shampoo | shampoo stesso `need-*`, altre linee + altri formati | conditioner/mask della stessa linea, leave-in, trattamento |
| Conditioner / Mask | maschere stesso `need-*` | shampoo stessa linea, leave-in |
| Leave-in | leave-in stesso `need-*` | shampoo + mask stessa linea |
| **Hair Color (shade)** | **4 shade vicine: stesso livello ±1 e stesso riflesso; poi stesso livello, riflessi affini** | developer della linea, shampoo post-colore (Color Fixx pH 5.5), Balancer pH 2.5, smacchiatore (Remov Up) |
| Developer | altri volumi | shade più vendute della linea, bowl, pennello |
| Lightener | altri decoloranti | developer, bond protector (Pure Verve), anti-giallo |
| Styling | stessa funzione (gel↔gel, cera↔cera, spray↔spray) | termoprotettore, shampoo detox |
| Salon Treatment | trattamenti stesso bisogno | home care della stessa linea |
| Kit | altri kit stesso bisogno | i singoli prodotti del protocollo |
| Tools | tools stessa categoria | i prodotti chimici che li richiedono |
| Salon Wear / Retail Display | — | esclusi dal motore dei consigli |

### Filtri globali (non negoziabili)
1. Mai raccomandare prodotti `DRAFT` o `ARCHIVED` *(oggi violato: `defrizzit`, archiviato, è ancora raccomandato)*
2. Mai raccomandare `Retail Display` da un prodotto vendibile
3. Mai auto-referenza
4. Simmetria dei related dove ha senso (se A è alternativa di B, B è alternativa di A)
5. Copertura 100%: nessun prodotto attivo con liste `null` o vuote

### Il caso colore (237 prodotti, priorità 1)
Oggi tutte le shade condividono lo stesso set di related: valore informativo nullo.
La regola tonale si deriva dal codice shade già presente nel titolo (`5.22`, `10.1`, `4.07`):
la cifra prima del punto è il livello, quelle dopo il riflesso. Related = shade con livello ±1 e
riflesso identico, poi stesso livello con riflesso della stessa famiglia. È deterministico e
applicabile in blocco a tutte e 237.

## 7. Ricerca interna

- `shopify--discovery--product_search_boost.queries`: valorizzare sui prodotti di punta con i termini
  commerciali reali (per linea, bisogno e lingua).
- Sinonimi in Search & Discovery: il catalogo è in inglese ma il mercato è svizzero (IT/DE/FR).
  Servono le mappature per i termini di ricerca nelle lingue del negozio.
- I filtri nativi dipendono dai facet del §3: si attivano solo dopo il completamento della copertura.

## 8. Ordine di esecuzione

| Fase | Contenuto | Rischio | Reversibile |
|---|---|---|---|
| 1 | Pulizia: 29 duplicati DRAFT, link a prodotti archiviati, regole di collezione morte | basso | sì |
| 2 | Product type + category standard su 491 prodotti | basso | sì |
| 3 | ~~Tag~~ — fuori perimetro per scelta: i tag restano invariati | — | — |
| 4 | Collezioni: merge, gerarchia, redirect 301 | **alto (SEO)** | parziale |
| 5 | Facet `shopify.*`: completamento copertura per tipo | basso | sì |
| 6 | Related + complementary: 237 shade con regola tonale, poi 226 prodotti per famiglia | basso | sì |
| 7 | Search boost e sinonimi | basso | sì |

Ogni fase produce un diff verificabile prima della scrittura e un rapporto dopo.
La fase 4 è l'unica che tocca URL pubblici: va eseguita con i redirect creati nella stessa transazione.
