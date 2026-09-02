# Barra di avanzamento verso la spedizione gratuita

Barra che mostra in tempo reale quanto manca alla soglia di spedizione gratuita,
dentro il drawer del carrello e nella pagina carrello.

File: [`snippets/custom-free-shipping-bar.liquid`](snippets/custom-free-shipping-bar.liquid)

Nessuna app, nessuna libreria, **nessun JavaScript**.

---

## Perche' non e' un blocco Sidekick (a differenza del carosello video)

Il carosello e' contenuto statico: si mette in una sezione, e li' resta. Questa
barra invece deve vivere dentro il carrello, e in Horizon 4.1.5 il carrello non
accetta blocchi. Verificato sui file del tema attivo:

| Contenitore | Accetta blocchi personalizzati? |
|---|---|
| `snippets/cart-drawer.liquid` | **no** — markup fisso, nessun `content_for 'blocks'` |
| `sections/cart-drawer-section.liquid` | **no** — schema senza `blocks` |
| `sections/main-cart.liquid` (pagina carrello) | si, `@theme` — ma i blocchi finiscono in fondo, sotto il riepilogo |
| `sections/header-announcements.liquid` | no, solo `_announcement` |
| `sections/footer.liquid` | no, lista chiusa di tipi + `@app` |
| `sections/header.liquid` | no, solo blocchi `static` |

Il negozio ha `cart_type: "drawer"` e `auto_open_cart_drawer: true`: il drawer
**e'** il carrello, la pagina `/cart` la vede una minoranza. Un blocco generato
da Sidekick potrebbe quindi stare solo nel punto meno utile, in fondo alla
pagina carrello, e mai nel drawer.

L'immunita' agli aggiornamenti dei file `blocks/ai_gen_*` e' reale (l'abbiamo
vista sopravvivere a 4.1.4.09 -> 4.1.4.10 -> 4.1.5.01 -> 4.1.5.02), ma non
serve a niente se il blocco non puo' essere messo dove serve.

**Quello che si perde rinunciando al blocco:** le impostazioni nel
personalizzatore. Qui soglia, testi e colori si cambiano in cima al file (o,
per la soglia, in un metafield: vedi sotto), non con gli slider.

---

## Come funziona l'aggiornamento in tempo reale

Horizon ri-renderizza il carrello lato server a ogni modifica: quando cambi una
quantita' o applichi un codice sconto, `component-cart-items.js` chiede la
sezione aggiornata (`sections: cart-drawer-section`) e ne fonde l'HTML nel DOM
(`morphSection`).

Lo snippet e' dentro `snippets/cart-summary.liquid`, che sta dentro quella
sezione: viene quindi rivalutato da Liquid a ogni modifica, con il totale vero.
Niente listener, niente `fetch('/cart.js')`, niente stato da tenere in sincrono.

Il `morph` aggiorna l'attributo `style` della barra invece di sostituire il
nodo, quindi la transizione CSS sulla larghezza parte da sola.

---

## Installazione

1. Shopify admin -> **Negozio online -> Temi -> ... -> Modifica codice**
2. Cartella `snippets` -> **Aggiungi un nuovo snippet** -> nome
   `custom-free-shipping-bar`
3. Incolla il contenuto di `snippets/custom-free-shipping-bar.liquid` e salva
4. Apri `snippets/cart-summary.liquid` e aggiungi **una riga** dopo
   `{% render 'cart-typography-styles' %}` (riga 8 circa):

   ```liquid
   {% render 'cart-typography-styles' %}

   {% render 'custom-free-shipping-bar', context: 'summary' %}   {%- comment -%} <- riga aggiunta {%- endcomment -%}

   <div class="cart-totals">
   ```

5. Salva.

Questo unico punto di innesto copre **sia il drawer sia la pagina carrello**:
entrambi passano da `cart-summary.liquid`.

La barra finisce in cima al riepilogo, quindi subito sopra il totale e il
pulsante di checkout. Nel drawer il riepilogo e' `position: sticky; bottom: 0`,
quindi la barra resta sempre visibile mentre si scorrono gli articoli.

### Variante: barra in cima al drawer

Se la preferisci sopra la lista dei prodotti invece che sopra il totale, salta
il punto 4 e aggiungi invece la riga in `snippets/cart-drawer.liquid`, subito
dopo `<scroll-hint class="cart-drawer__content" ...>`:

```liquid
{% render 'custom-free-shipping-bar', context: 'drawer' %}
```

In quel caso serve un secondo innesto in `cart-summary.liquid` o in
`sections/main-cart.liquid` per la pagina carrello. Due file invece di uno:
per questo il default e' il riepilogo.

---

## Impostazioni consigliate

### 1. La soglia

Situazione attuale, letta da Impostazioni -> Spedizioni:

| Zona | Tariffa | Gratis da |
|---|---|---|
| SHIP-Z0 (Svizzera) | DHL Express Priority 5.80 CHF | **99.00 CHF** |
| SHIP-Z2 (export) | DHL Express Export 129.90 / 99.90 / 69.90 EUR | 1890.00 EUR |

Distribuzione dei 27 ordini B2C degli ultimi 12 mesi (esclusi quelli con
azienda collegata):

```
24.80  25.60  28.80  28.80  29.60  32.80  35.43  38.40  39.36  41.04
42.58  44.40  50.30  51.28  59.20  63.80  69.40  81.20  89.00  98.40
99.66  121.29  133.20  134.40  156.30  160.98  378.16
```

- mediana **51.28 CHF**, media 79.93 CHF
- **20 ordini su 27 (74%) sotto i 99 CHF**
- distanza media dalla soglia per chi sta sotto: **50.30 CHF**
- solo 4 ordini su 27 sono arrivati entro 30 CHF dalla soglia

Questo e' il dato che conta. Una barra converte quando il cliente vede una
distanza colmabile con un prodotto in piu'. A 99 CHF, con una mediana di 51, il
messaggio tipico sara' "ti mancano 48 CHF": e' un secondo prodotto intero, non
un'aggiunta d'impulso, e per la maggior parte delle sessioni la barra risultera'
ferma a meta'.

Riferimento di settore: soglia tra 1.2x e 1.5x il valore mediano dell'ordine.
Qui sono **62 - 77 CHF**.

**Consiglio:**

- **Ora:** installa la barra con la soglia attuale a 99 CHF. Non cambiare due
  variabili insieme, altrimenti non saprai cosa ha funzionato.
- **Fra 4-6 settimane:** guarda quanti ordini si spostano nella fascia 80-99.
  Se non si muove niente, prova **79 CHF**: resta sopra la mediana (quindi
  spinge comunque verso l'alto), ma il messaggio diventa "ti mancano 28 CHF",
  cioe' un prodotto singolo del catalogo.
- **Margine:** la spedizione costa 5.80 CHF al cliente e con DHL Express di
  piu' a te. Scendere a 79 significa regalare la spedizione su ordini che oggi
  la pagano: da mettere a bilancio contro l'aumento di scontrino medio.

Nota sul campione: 27 ordini B2C sono pochi per una decisione statistica. Il
segnale (74% sotto soglia, distanza media 50 CHF) e' pero' abbastanza netto da
essere indicativo.

### 2. Mercati e valute

**Non mostrare 1890 EUR come soglia sul mercato export.** Chiedere a un cliente
D2C 1750 EUR in piu' non e' un incentivo, e' un muro.

Il file di default definisce **solo CHF**. Una valuta senza soglia = barra
nascosta in quel mercato. Per aggiungerne una, o per cambiare la soglia senza
toccare il codice, crea il metafield shop:

- Impostazioni -> **Dati personalizzati -> Negozio** -> Aggiungi definizione
- Namespace e chiave: `custom.free_shipping_thresholds`
- Tipo: **JSON**
- Valore: `{"CHF": 9900}` (importi in centesimi)

Il metafield vive fuori dal tema: sopravvive agli aggiornamenti al 100% e si
modifica dall'admin senza passare dal codice. Se e' presente, vince sui valori
scritti nel file.

### 3. Su quale importo si misura

Lo snippet usa `cart.total_price`, cioe' il totale **dopo** gli sconti di riga
e di carrello. E' la stessa base che Shopify usa per la condizione di prezzo
della tariffa di spedizione.

E' il punto in cui questi widget sbagliano piu' spesso: usando
`items_subtotal_price` (prima degli sconti di carrello), un cliente con un
codice -10% vedrebbe "spedizione gratuita sbloccata" e poi si troverebbe i 5.80
CHF al checkout. Con `show_add_discount_code: true` attivo nel tema, il caso
capita davvero.

### 4. Quando la barra non si mostra

Per scelta, in questi casi non compare niente:

- carrello vuoto (il riepilogo di Horizon non viene nemmeno renderizzato)
- carrello di sole gift card o prodotti digitali (`requires_shipping` falso su
  tutte le righe): non c'e' spedizione da regalare
- valuta senza soglia configurata
- se un codice sconto ha gia' azzerato la spedizione, la barra passa
  direttamente allo stato "sbloccata" invece di chiedere altri soldi

### 5. Testi

Quattro lingue nel file: **EN** (default), IT, DE, FR, scelte su
`request.locale.iso_code`. Sono in cima allo snippet, in un blocco `case`.

Testo attuale della fascia annunci: `FREE DHL EXPRESS OVER CHF 99`. I testi
della barra sono coerenti (citano DHL Express), in maiuscoletto naturale invece
che tutto maiuscolo perche' qui la frase e' piu' lunga. Per allinearli alla
fascia, aggiungi `text-transform: uppercase;` a `.custom-fsb__text`.

### 6. Aspetto

Di default la barra usa le variabili CSS del tema, quindi segue da sola la
palette (`#1a1a1a` su traccia al 12%) e il font Inter. Tre valori in cima al
CSS per cambiare tutto:

```css
--fsb-height: 6px;                                  /* spessore */
--fsb-fill: var(--color-foreground, #1a1a1a);       /* riempimento */
--fsb-fill-reached: var(--color-foreground, #1a1a1a); /* stato sbloccato */
```

Il default e' monocromatico, in linea con il resto del sito. Se vuoi che lo
stato raggiunto salti all'occhio, l'unica riga da cambiare e':

```css
--fsb-fill-reached: #2e6f4e;
```

La transizione della larghezza e' disattivata per chi ha *riduci animazioni*
nel sistema operativo.

### 7. Accessibilita'

Il testo ha `aria-live="polite"`: uno screen reader annuncia il nuovo importo
mancante quando cambi quantita'. La barra grafica e' `aria-hidden`, perche'
l'informazione e' gia' interamente nel testo e un `progressbar` in piu'
la farebbe annunciare due volte.

---

## Cosa succede quando aggiorni il tema

Il punto va capito bene, perche' su questo negozio i temi si aggiornano spesso
(4.1.4.09 -> 4.1.4.10 -> 4.1.5.01 -> 4.1.5.02 in cinque giorni).

**Aggiornare non tocca il sito.** Shopify non sovrascrive il tema attivo: crea
un tema nuovo, non pubblicato, con dentro i tuoi settaggi migrati. Il sito
continua a girare sul vecchio finche' non pubblichi. La barra sparisce solo nel
momento in cui **pubblichi** il tema nuovo senza averla reinstallata.

Quello che il migratore di Shopify porta con se' e quello che lascia indietro,
verificato sui tuoi temi:

| | Sopravvive? | Verifica |
|---|---|---|
| `config/settings_data.json` (settaggi, app embed) | si | judge.me, zipchat, Forms e checkout-blocks sono ancora li' dopo tre aggiornamenti |
| `templates/*.json`, `sections/*-group.json` (blocchi piazzati) | si | la fascia annunci con "FREE DHL EXPRESS OVER CHF 99" ha attraversato tutti i temi |
| `blocks/ai_gen_*.liquid` (blocchi Sidekick) | si | `168a139`, `80b6619`, `c80aa7c` sono identici in tutti e quattro i temi |
| file aggiunti a mano (`snippets/custom-*`, `sections/custom-*`) | **no** | vanno ricopiati |
| modifiche a file del tema (la riga in `cart-summary.liquid`) | **no** | vanno rimesse |

La regola dietro la tabella: **sopravvive tutto cio' che e' configurazione,
non sopravvive niente di cio' che e' codice.**

### Perche' nessuna scelta evita del tutto il problema

Per arrivare **dentro il drawer** serve per forza toccare un file del tema:
`snippets/cart-drawer.liquid` e `sections/cart-drawer-section.liquid` non
accettano blocchi. E i file del tema vengono sostituiti. Non c'e' configurazione
che aggiri questo, ne' con Sidekick ne' senza.

Le alternative reali, con il loro prezzo:

| Strada | Nel drawer? | Manutenzione a ogni pubblicazione |
|---|---|---|
| **Questa (snippet + 1 riga)** | si | 1 file da ricopiare + 1 riga da rimettere, ~2 minuti |
| Blocco Sidekick sulla pagina /cart | **no**, solo su /cart | nessuna |
| App dallo store (app embed) | si | nessuna, ma canone mensile e JavaScript in piu' |
| Tema collegato a GitHub | si | nessuna, ma cambia il modo di lavorare sul tema |

Il blocco Sidekick sopravviverebbe davvero, file e piazzamento. Ma finirebbe
solo in fondo alla pagina `/cart`, che con `cart_type: "drawer"` e
`auto_open_cart_drawer: true` vede una minoranza dei clienti. E' manutenzione
zero su una barra che quasi nessuno guarda.

### Come non restare mai scoperti

La reinstallazione si fa **sul tema nuovo prima di pubblicarlo**, non dopo.
L'Admin API scrive sui temi non pubblicati, quindi la sequenza e':

1. aggiorni il tema (Shopify crea il tema nuovo, non pubblicato)
2. reinstalli la barra sul tema nuovo
3. pubblichi

Cosi' il sito non passa mai un secondo senza la barra. Il momento pericoloso e'
solo pubblicare al punto 2 saltando il 3.

Il modo piu' veloce per il punto 2: aprire una sessione con il connettore
Shopify e chiedere *"reinstalla la barra spedizione gratuita sul tema
&lt;nome&gt;"*. Sono due chiamate API, sotto il minuto. In alternativa, a mano,
i due passaggi dell'Installazione qui sopra.

---

## Sopravvivere agli aggiornamenti del tema

Su Shopify un aggiornamento **installa un tema nuovo**: i file aggiunti a mano
non vengono copiati.

- `snippets/custom-free-shipping-bar.liquid` -> prefisso `custom-`, nessun file
  di Horizon si chiamera' mai cosi'. Da ricopiare dopo ogni aggiornamento.
- **una riga** in `snippets/cart-summary.liquid` -> da riaggiungere a mano.
- La soglia, se la metti nel metafield, non e' nel tema: non si perde mai.

### Reinstallazione via Admin API

Funziona solo su temi **non pubblicati** (Shopify blocca le scritture sul tema
live: pubblicare dopo l'installazione).

```graphql
mutation Reinstall($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    upsertedThemeFiles { filename }
    userErrors { filename code message }
  }
}
```

```json
{
  "themeId": "gid://shopify/OnlineStoreTheme/<ID-DEL-TEMA-NUOVO>",
  "files": [{
    "filename": "snippets/custom-free-shipping-bar.liquid",
    "body": {
      "type": "URL",
      "value": "https://raw.githubusercontent.com/fralati/main/claude/shopify-free-shipping-progress-bar-68u0ta/shopify/snippets/custom-free-shipping-bar.liquid"
    }
  }]
}
```

La riga in `cart-summary.liquid` va rimessa a mano (o rileggendo il file,
inserendo la riga e riscrivendolo con la stessa mutation).

### La soluzione definitiva

Collegare il tema a un repo GitHub (Temi -> Aggiungi tema -> Connetti da
GitHub). Il tema diventa versionato e i file personalizzati vivono nel repo in
modo permanente. Cambia pero' il modo di lavorare sul tema.

---

## Se vuoi comunque le impostazioni nel personalizzatore

Esiste una via di mezzo, piu' complessa: far generare a Sidekick un blocco
`ai_gen_*` con le impostazioni (soglia, testi, colori) e renderizzarlo come
blocco statico dal riepilogo:

```liquid
{% content_for 'block', id: 'free-shipping-bar', type: 'ai_gen_block_xxxxxxx' %}
```

E' lo stesso meccanismo che Horizon usa per `_cart-title` e `_cart-summary` in
`sections/main-cart.liquid`. Si otterrebbero gli slider nel personalizzatore e
un file blocco che sopravvive agli aggiornamenti, ma **la riga di innesto nel
file del tema resta comunque necessaria**: il costo di reinstallazione e' lo
stesso di adesso, con in piu' un file e un vincolo (non far mai rigenerare il
blocco a Sidekick, lo sovrascrive).

Ha senso solo se vuoi cambiare soglia e testi dal personalizzatore piu' volte.
Per due valori che si toccano una volta ogni sei mesi, il metafield fa lo
stesso lavoro con meno pezzi.
