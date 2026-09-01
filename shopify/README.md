# Carosello video verticale (stile Reels) per Shopify

Ricostruzione della sezione **"Carrousel vidéo"** del vecchio tema *Hyperflow v1.16*,
riscritta per funzionare su qualsiasi tema Online Store 2.0 (Dawn e derivati inclusi).

File: [`sections/custom-video-carousel-reels.liquid`](sections/custom-video-carousel-reels.liquid)

## Installazione

1. Shopify admin → **Negozio online → Temi → ⋯ → Modifica codice**
2. Nella cartella `sections` → **Aggiungi una nuova sezione** → nome `custom-video-carousel-reels`
3. Incolla il contenuto di `sections/custom-video-carousel-reels.liquid` (sostituendo tutto) e salva
4. Nel personalizzatore → **Aggiungi sezione → Carosello video verticale**

Nessun file aggiuntivo, nessuna app, nessuna libreria da caricare.

## Cosa cambia rispetto all'originale

| | Hyperflow | Questa versione |
|---|---|---|
| Slider | Swiper 11 da CDN (~150 KB) + `lazyload.min.js` | scroll-snap nativo, 0 dipendenze |
| Markup | ogni blocco duplicato 4 volte per simulare il loop | un nodo per blocco |
| Caricamento video | `data-src` con la sorgente fissa `sources[1]` | sorgente scelta in base alla larghezza reale della card e al DPR, caricata solo all'ingresso nel viewport |
| CSS | ~700 righe rigenerate per ogni istanza della sezione | classi statiche + variabili CSS |
| Audio | nessun coordinamento | un solo video con audio attivo alla volta, si rimuta all'uscita dallo schermo |
| Accessibilità | `div` cliccabili | `button` con `aria-pressed` / `aria-label`, focus visibile, `prefers-reduced-motion` |
| Video esterni | iframe sempre presente nel DOM | iframe YouTube/Vimeo creato solo alla riproduzione |

## Funzioni

- formato card configurabile: **9:16 (reels)**, 3:4, 4:5, 1:1, 16:9
- numero di video visibili separato per desktop / tablet / mobile (su mobile accetta
  valori decimali, es. `1.2`, per far intravedere la card successiva)
- autoplay muto solo quando la card è visibile, pausa automatica all'uscita
- pulsanti audio e play/pausa su ogni card, click sul video per play/pausa
- modalità **card centrata** con le altre rimpicciolite (equivalente dell'effetto
  coverflow dell'originale)
- frecce, puntini, swipe su touch e trascinamento col mouse
- per ogni card: video caricato o URL YouTube/Vimeo, copertina, titolo, testo,
  valutazione a stelle (con mezze stelle) e pulsante con link

## Note

- I video verticali vanno caricati in **9:16** (es. 1080×1920). Consigliati `.mp4`
  H.264 o `.webm` sotto i 10 MB: il file resta comunque il costo principale della sezione.
- I video caricati su Shopify hanno più risoluzioni: la sezione sceglie da sola la più
  adatta, quindi non serve caricare versioni ridotte a mano.
- I video YouTube/Vimeo non partono in autoplay su tutti i browser e sono più pesanti:
  se possibile carica il file direttamente su Shopify.
- L'autoplay viene disattivato per chi ha impostato *riduci animazioni* nel sistema
  operativo: resta la copertina con il pulsante play.

## Sopravvivere agli aggiornamenti del tema

Su Shopify un aggiornamento di tema **installa un tema nuovo**: i file aggiunti a
mano non vengono copiati. Non esiste un modo, dentro Shopify, per rendere una
sezione personalizzata immune agli aggiornamenti. Quello che si può fare:

- **La sorgente sta qui, non nel tema.** Questo repo è la copia di riferimento;
  il file nel tema è solo una installazione.
- **Prefisso `custom-`.** Nessun file di Horizon si chiamerà mai così, quindi un
  aggiornamento non può sovrascriverlo per collisione di nome.
- **Intestazione nel file.** Chi apre il codice del tema vede da dove viene e che
  va reinstallato.
- **Reinstallazione.** Dopo ogni aggiornamento, ricopiare il file dal repo nel
  tema nuovo (2 minuti a mano, oppure via Admin API come sotto).

### Reinstallazione via Admin API

Funziona solo su temi **non pubblicati** (Shopify blocca le scritture sul tema
live: pubblicare il tema dopo l'installazione).

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
    "filename": "sections/custom-video-carousel-reels.liquid",
    "body": {
      "type": "URL",
      "value": "https://raw.githubusercontent.com/fralati/main/claude/shopify-portrait-video-carousel-fi7fdb/shopify/sections/custom-video-carousel-reels.liquid"
    }
  }]
}
```

### La soluzione definitiva

Collegare il tema a un repo GitHub (Shopify admin -> Temi -> Aggiungi tema ->
Connetti da GitHub). Il tema diventa versionato e i file personalizzati vivono
nel repo in modo permanente: gli aggiornamenti si gestiscono con git e non si
perde più nulla. Cambia però il modo di lavorare sul tema.

## Note su Horizon

Il tema attivo è Horizon, non più Hyperflow. La sezione è stata adattata alle sue
convenzioni: nessun `tag`/`class` nello schema (Horizon applica da solo la classe
`.section` con la propria larghezza e spaziatura, che si sarebbe sommata alla
nostra), CSS in `{% stylesheet %}` così viene emesso una volta sola per tutto il
tema invece che a ogni istanza, e dimensione del titolo in px perché le classi
`.h1`/`.h2`/`.h3` esistono in Dawn ma non in Horizon.

## Blocco AI (percorso Sidekick)

`blocks/ai_gen_block_58478e9.liquid` è il blocco generato da Sidekick nel tema
Horizon 4.1.5.02, con il corpo riscritto. Gli ID delle impostazioni sono
invariati rispetto alla generazione originale (gli slot passano da 6 a 10), così
i contenuti già configurati non si perdono.

Motivo di questo percorso: sui temi di questo store i file `blocks/ai_gen_*`
hanno attraversato tutti gli aggiornamenti (4.1.4.09 -> 4.1.4.10 -> 4.1.5.01 ->
4.1.5.02), e in 4.1.5.01 sono stati riscritti 94 secondi dopo i file base del
tema, cioè ri-applicati come passaggio a sé dopo l'aggiornamento. Tutto sta in
un unico file proprio per restare una sola unità che viaggia negli aggiornamenti:
per questo gli slot sono fissi e non blocchi annidati, che avrebbero richiesto un
secondo file non coperto da quel meccanismo.

Correzioni rispetto al codice generato:

| Problema nel codice generato | Correzione |
|---|---|
| `src="{{ video.sources[1].url }}"`: vuoto se il video ha una sola sorgente | sorgente scelta da larghezza card e DPR |
| `preventDefault` su `touchmove` globale: bloccava lo scroll verticale su mobile | scroll-snap nativo, nessun preventDefault |
| `currentX` non azzerato: salto di slide al semplice click | nessuno stato di drag da azzerare |
| `slidesPerView` 1.5 produceva un indice frazionario | navigazione per posizione, non per indice |
| tutti i video con `src` e `preload="metadata"` al caricamento | sorgente agganciata all'ingresso nel viewport |
| nessun listener di resize | ricalcolo su resize e orientationchange |
| larghezza mobile senza `- 1` nella formula | formula uniforme sui tre breakpoint |
| audio restava "attivo" dopo l'uscita dallo schermo | si rimuta all'uscita |
| `aria-label` in inglese | etichette in italiano |

NON chiedere a Sidekick di modificare questo blocco: rigenerandolo sovrascrive
il codice.
